from Lexer import *
from Tables import *

rules = [
"ERROR: Rules are not zero indexed! FIXME!",
"R1. <Rat18S> ::= %% <Opt Declaration List> <Statement List> ",
"R2. <Qualifier> ::= int | boolean ",
"R3. <Body> ::= { <Statement List> }",
"R4. <Opt Declaration List> ::= <Declaration List> | E",
"R5. <Declaration List> ::= <Declaration><Declaration List'>",
"R6. <Declaration List'> ::= <Declaration List> | E",
"R7. <Declaration> ::= <Qualifier> <IDs> ",
"R8. <IDs> ::= <Identifier> <IDs’>",
"R9. <IDs'> ::= <IDs> | E",
"R10. <Statement List> ::= <Statement><Statement List’>",
"R11. <Statement List'> ::= <Statement List> | E",
"R12. <Statement> ::= <Compound> | <Assign> | <If> | <Return> | <Print> | <Scan> | <While> ",
"R13. <Compound> ::= { <Statement List> } ",
"R14. <Assign> ::= <Identifier> = <Expression> ;",
"R15. <If> ::= if ( <Condition> ) <Statement> endif | if ( <Condition> ) <Statement> else <Statement> endif ",
"R16. <Return> ::= return ; | return <Expression> ;",
"R17. <Print> ::= put ( <Expression> );",
"R18. <Scan> ::= get ( <IDs> );",
"R19. <While> ::= while ( <Condition> ) <Statement> ",
"R20. <Condition> ::= <Expression> <Relop> <Expression>",
"R21. <Relop> ::= == | ^= | > | < | => | =< ",
"R22. <Expression> ::= <Term> <Expression'>",
"R23. <Expression'> ::= + <Term> <Expression'> | - <Term> <Expression'> | E",
"R24. <Term> ::= <Factor> <Term'>",
"R25. <Term'> ::= * <Factor> <Term'> | / <Factor> <Term'> | E",
"R26. <Factor> ::= - <Primary> | <Primary>",
"R27. <Primary> ::= <Identifier> | <Integer> | <Identifier> ( <IDs> ) | ( <Expression> ) | true | false"
]

# Create a list for the token lexeme pairs
pairs = []

# This is our symbol table
symtable = SymbolTable()

index = 0

backtrack_stack = []

rule_stack = []

verbose = False
debug = False

message = None

current_type = None
current_identifier = None

# Called when there is a safe index to backtrack back to
def btsafe():
	global backtrack_stack 
	global index 
	backtrack_stack.append(index)

def backtrack():
	global backtrack_stack 
	global index 
	old_index = index
	index = backtrack_stack.pop()
	print("DEBUG: Backtracking from", old_index, "(", pairs[old_index][1], ")", "to", index, "(", pairs[index][1], ")")

def error(msg):
	global message
	global pairs
	global index

	if index < len(pairs):
		message = "ERROR: " + str(msg) + "\t@ Token: " + str(pairs[index][0]) + "\tLexeme: " + str(pairs[index][1]) + " on line " + str(pairs[index][2])

def rule(num):
	global rules
	global rule_stack

	rule_stack.append(rules[num])

def advance():
	global pairs
	global index
	global debug

	if (index - 1) >= (len(pairs)):
		return False
	else:
		if debug:
			print("Accepted Token:", pairs[index][0], "\tLexeme:", pairs[index][1])
		index += 1
		return True

def accept(test, token = False):
	global index
	global backtrack_stack
	global debug

	if token:
		offset = 0
	else:
		offset = 1

	if index == len(pairs):
		return False

	if pairs[index][offset] == test:
		if advance():
			return True
		else:
			# FIXME: Figure out what to do here
			error("End of input")
			return False
	else:
		if debug:
			print()
			print("DEBUG: failed \"" + str(pairs[index][offset]) + "\" != \"" + str(test) + "\"", "\ttoken: ", pairs[index][0], "\tlexeme:", pairs[index][1])

		# If we can't accept the input and we're not at a safe index...
		if index not in backtrack_stack:
			# Backtrack back to the last safe index
			backtrack()

		return False

def p_ids_prime():
	btsafe()
	if accept(",") and p_ids():
		rule(9)
		return True

	return True

def p_identifier(declare = False):
	global pairs
	global index
	global current_type
	global current_identifier

	btsafe()
	if accept("identifier", token = True):
		current_identifier = pairs[index - 1][1]
		add_symbol(pairs[index - 1][1], current_type)
		if declare:
			gen_instr("PUSHI", 0)
			
		gen_instr("PUSHM", get_address(current_identifier))
		return True
	else:
		return False

def p_ids(declare=False):
	btsafe()
	if p_identifier(declare) and p_ids_prime():
		rule(8)
		return True
	else:
		return False

def p_qualifier():
	global pairs
	global index
	global current_type

	btsafe()
	if accept("int"):
		current_type = "int"
		rule(2)
		return True

	btsafe()
	if accept("boolean"):
		current_type = "int"
		rule(2)
		return True

	error("Expected int or boolean qualifier")
	return False

def p_declaration():
	btsafe()
	if p_qualifier() and p_ids(declare=True):
		rule(7)
		return True
	else:
		return False

def p_decl_list_prime():
	btsafe()
	if p_decl_list() and accept(";"):
		rule(6)
		return True

	rule(6)
	return True

def p_decl_list():
	btsafe()
	if p_declaration() and accept(";") and p_decl_list_prime():
		rule(5)
		return True
	else:
		return False

def p_opt_decl_list():
	btsafe()
	p_decl_list()
	rule(4)
	return True

def p_term_prime():
	btsafe()
	if accept("*") and p_factor() and p_term_prime():
		gen_instr("MUL", "nil")
		rule(25)
		return True

	btsafe()
	if accept("/") and p_factor() and p_term_prime():
		gen_instr("DIV", "nil")
		rule(25)
		return True
	
	return True

def p_primary():
	global pairs
	global index

	btsafe()
	if p_identifier():
		rule(27)
		return True

	btsafe()
	if accept("integer", token=True):
		gen_instr("PUSHI", pairs[index - 1][1])
		rule(27)
		return True

	btsafe()
	if p_identifier() and accept("(") and p_ids() and accept(")"):
		rule(27)
		return True

	btsafe()
	if accept("(") and p_expression() and accept(")"):
		rule(27)
		return True

	btsafe()
	if accept("true") or accept("false"):
		rule(27)
		return True

	return False

def p_factor():
	btsafe()
	if accept("-") and p_primary():
		rule(26)
		return True

	btsafe()
	if p_primary():
		rule(26)
		return True
	
	return False

def p_term():
	btsafe()
	if p_factor() and p_term_prime():
		rule(24)
		return True
	else:
		return False

def p_expression_prime():
	btsafe()
	if accept("+") and p_term() and p_expression_prime():
		gen_instr("ADD", "nil")
		rule(23)
		return True

	btsafe()
	if accept("-") and p_term() and p_expression_prime():
		gen_instr("SUB", "nil")
		rule(23)
		return True

	return True

def p_expression():
	btsafe()
	if p_term() and p_expression_prime():
		rule(22)
		return True
	else:
		return False

def p_compound():
	btsafe()
	if accept("{") and p_statement_list() and accept("}"):
		rule(13)
		return True
	else:
		return False

def p_assign():
	global current_identifier

	btsafe()
	if p_identifier() and accept("=") and p_expression() and accept(";"):
		if current_identifier is not None:
			gen_instr("POPM", get_address(current_identifier))
		rule(14)
		return True
	else:
		return False

def p_relop():
	global pairs
	global index

	btsafe()
	if accept("operator", token = True):
		if pairs[index - 1][1] == ">":
			gen_instr("GRT", "nil")
		else:
			gen_instr("LES", "nil")

		push_jumpstack(gen_instr("JUMPZ", "nil"))
		rule(21)
		return True

	btsafe()
	if accept("operator", token = True) and accept("operator", token = True):
		if (str(pairs[index - 2][1]) + str(pairs[index - 1][1])) == "==":
			gen_instr("EQU", "nil")
		elif (str(pairs[index - 2][1]) + str(pairs[index - 1][1])) == "^=":
			gen_instr("NEQ", "nil")
		elif (str(pairs[index - 2][1]) + str(pairs[index - 1][1])) == "=>":
			gen_instr("GEQ", "nil")
		else:
			gen_instr("LEQ", "nil")

		push_jumpstack(gen_instr("JUMPZ", "nil"))
		rule(21)
		return True

	return False

def p_condition():
	btsafe()
	if p_expression() and p_relop() and p_expression():
		rule(20)
		return True
	return False

def p_if():
	btsafe()
	if accept("if") and accept("(") and p_condition() and accept(")") and p_statement() and accept("endif"):
		rule(15)
		backpatch()
		return True

	btsafe()
	if accept("if") and accept("(") and p_condition() and accept(")") and p_statement() and accept("else"):
		backpatch()
		if p_statement() and accept("endif"):
			rule(15)
			return True

	return False

def p_return():
	btsafe()
	if accept("return") and accept(";"):
		rule(16)
		return True

	btsafe()
	if accept("return") and p_expression() and accept(";"):
		rule(16)
		return True

	return False

def p_scan():
	btsafe()
	if accept("get") and accept("(") and p_ids() and accept(")") and accept(";"):
		gen_instr("STDIN", "nil")
		rule(18)
		return True
	else:
		return False


def p_print():
	btsafe()
	if accept("put") and accept("(") and p_expression() and accept(")") and accept(";"):
		gen_instr("STDOUT", "nil")
		rule(17)
		return True
	else:
		return False

def p_while():
	btsafe()
	if accept("while"):
		push_jumpstack(gen_instr("LABEL", "nil"))
		if accept("(") and p_condition() and accept(")") and p_statement():
			gen_instr("JUMP", "nil")
			backpatch()
			rule(19)
			return True

	error("Could not parse while loop")
	return False

def p_statement():
	btsafe()
	if p_compound():
		rule(12)
		return True

	btsafe()
	if p_assign():
		rule(12)
		return True

	btsafe()
	if p_if():
		rule(12)
		return True

	btsafe()
	if p_return():
		rule(12)
		return True

	btsafe()
	if p_print():
		rule(12)
		return True

	btsafe()
	if p_scan():
		rule(12)
		return True

	btsafe()
	if p_while():
		rule(12)
		return True

	error("Could not parse statement")
	return False

def p_statement_list_prime():
	btsafe()
	p_statement_list()
	rule(11)
	return True

def p_statement_list():
	btsafe()
	if p_statement() and p_statement_list_prime():
		rule(10)
		return True
	else:
		error("Could not parse statement list")
		return False

def p_rat18s():
	if accept("%") and accept("%") and p_opt_decl_list() and p_statement_list():
		rule(1)
		return True
	else:
		error("Could not parse Rat18s")
		return False

# Given a list of token-lexeme pairs attempt to parse the syntax
def parse():
	global pairs
	global message

	if not p_rat18s():

		# If we can't parse rat18s, then print the last error message
		print(message)

# Given a file to lex, print out the tokens and lexemes for each line
def parser(source_file, verbosity, debugging):
	with open(source_file, 'r') as file_in:
		global verbose 
		global debug 
		global rule_stack
		verbose = verbosity
		debug = debugging

		global pairs

		index = 0

		# Call lex() for each line and build our list of token, lexeme pairs
		for line in file_in:
			result = lex(line, index)
			index += 1

			if result:
				pairs = pairs + result

		parse()

		# Print the used rules if we are in verbose mode
		if verbose:
			rule_stack.reverse()
			for rule in rule_stack:
				print(rule)

		print("Symbol Table:")
		print_symbols()
		print()
		print("Instruction Table:")
		print_instructions()
