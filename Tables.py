class Symbol:
	def __init__(self, name, stype):
		self.name = name
		self.type = stype
		self.location = 0
	
	def __str__(self):
		return str(str(self.name) + "\t" + str(self.type) + "\t" + str(self.location))

class SymbolTable:
	def __init__(self):
		self.last = 1999
		self.symbols = []

	def insert(self, sym):
		if self.lookup(sym.name) is None:
			sym.location = self.last + 1
			self.last += 1
			self.symbols.append(sym)

	def lookup(self, name):
		for sym in self.symbols:
			if sym.name == name:
				return sym
		return None

	def list(self):
		print("Name\tType\tMemory Location")
		for sym in self.symbols:
			print(sym)
class Instruction:
	def __init__(self, op, operand):
		self.address = 0
		self.op = op
		self.operand = operand
	
	def __str__(self):
		return str(str(self.address) + "\t" + str(self.op) + "\t" + str(self.operand))

class InstructionTable:
	def __init__(self):
		self.last = 0
		self.instructions = []

	def insert(self, inst):
		inst.address = self.last + 1
		self.last += 1
		self.instructions.append(inst)
		return inst

	def set(self, addr, jump):
		for inst in self.instructions:
			if inst.address == addr:
				inst.operand = jump

	def peek_end(self):
		return self.instructions[len(self.instructions) - 1]

	def list(self):
		print("Address\tOp\tOperand")
		for inst in self.instructions:
			print(inst)

symbtable = SymbolTable()

insttable = InstructionTable()

jumpstack = []

def push_jumpstack(addr):
	global jumpstack
	jumpstack.append(addr)

def backpatch():
	global jumpstack
	global insttable
	jump_addr = insttable.peek_end().address
	addr = jumpstack.pop()
	insttable.set(addr, jump_addr)

def gen_instr(op, operand):
	global insttable
	return insttable.insert(Instruction(op, operand)).address

def get_address(name):
	global symbtable
	return symbtable.lookup(name).location

def add_symbol(name, stype):
	global symbtable
	symbtable.insert(Symbol(name, stype))

def print_symbols():
	global symbtable
	symbtable.list()

def print_instructions():
	global insttable
	insttable.list()
