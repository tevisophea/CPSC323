# Import the Python regex module
import re

# Given a line of input, returns a list with the token, lexeme pair
def lex(line, num):
	# Strip comments out before continuing
	line = re.sub('!.*!', '', line)

	length = len(line)
	position = 0
	pairs = []

	# Continue trying to find a matching state while there is still more to process
	while (position < length):

		# Separators
		if (line[position] == " "):
			position = position + 1
		elif (line[position] == "{"):
			pairs.append(['separator', line[position], num])
			position = position + 1
		elif (line[position] == "}"):
			pairs.append(['separator', line[position], num])
			position = position + 1
		elif (line[position] == "("):
			pairs.append(['separator', line[position], num])
			position = position + 1
		elif (line[position] == ")"):
			pairs.append(['separator', line[position], num])
			position = position + 1
		elif (line[position] == ":"):
			pairs.append(['separator', line[position], num])
			position = position + 1
		elif (line[position] == ";"):
			pairs.append(['separator', line[position], num])
			position = position + 1
		elif (line[position] == "["):
			pairs.append(['separator', line[position], num])
			position = position + 1
		elif (line[position] == "]"):
			pairs.append(['separator', line[position], num])
			position = position + 1
		elif (line[position] == "%"):
			pairs.append(['separator', line[position], num])
			position = position + 1
		elif (line[position] == ","):
			pairs.append(['separator', line[position], num])
			position = position + 1

		# Operators
		elif (line[position:position+2] == "=="):
			pairs.append(['operator', line[position:position+2], num])
			position = position + 2
		elif (line[position:position+2] == "<="):
			pairs.append(['operator', line[position:position+2], num])
			position = position + 2
		elif (line[position:position+2] == ">="):
			pairs.append(['operator', line[position:position+2], num])
			position = position + 2
		elif (line[position:position+2] == "^="):
			pairs.append(['operator', line[position:position+2], num])
			position = position + 2
		elif (line[position] == "="):
			pairs.append(['operator', line[position], num])
			position = position + 1
		elif (line[position] == ">"):
			pairs.append(['operator', line[position], num])
			position = position + 1
		elif (line[position] == "<"):
			pairs.append(['operator', line[position], num])
			position = position + 1
		elif (line[position] == "+"):
			pairs.append(['operator', line[position], num])
			position = position + 1
		elif (line[position] == "-"):
			pairs.append(['operator', line[position], num])
			position = position + 1
		elif (line[position] == "*"):
			pairs.append(['operator', line[position], num])
			position = position + 1
		elif (line[position] == "/"):
			pairs.append(['operator', line[position], num])
			position = position + 1

		# Keywords
		elif (line[position:position+2] == "if"):
			pairs.append(['keyword', line[position:position+2], num])
			position = position + 3
		elif (line[position:position+3] == "int"):
			pairs.append(['keyword', line[position:position+3], num])
			position = position + 3
		elif (line[position:position+3] == "get"):
			pairs.append(['keyword', line[position:position+3], num])
			position = position + 3
		elif (line[position:position+3] == "put"):
			pairs.append(['keyword', line[position:position+3], num])
			position = position + 3
		elif (line[position:position+4] == "true"):
			pairs.append(['boolean', line[position:position+4], num])
			position = position + 4
		elif (line[position:position+4] == "else"):
			pairs.append(['keyword', line[position:position+4], num])
			position = position + 4
		elif (line[position:position+5] == "while"):
			pairs.append(['keyword', line[position:position+5], num])
			position = position + 5
		elif (line[position:position+5] == "endif"):
			pairs.append(['keyword', line[position:position+5], num])
			position = position + 5
		elif (line[position:position+5] == "false"):
			pairs.append(['boolean', line[position:position+5], num])
			position = position + 5
		elif (line[position:position+6] == "return"):
			pairs.append(['keyword', line[position:position+6], num])
			position = position + 6
		elif (line[position:position+7] == "boolean"):
			pairs.append(['keyword', line[position:position+7], num])
			position = position + 7
		elif (line[position:position+8] == "function"):
			pairs.append(['keyword', line[position:position+8], num])
			position = position + 8
		else:
			# Only Identifier, Integer and Real remain

			# Integer and Real
			if (re.match('[0-9]', line[position])):

				num_pos = position
				is_real = False

				while (num_pos < length):
					if (re.match('[0-9]', line[num_pos])):
						num_pos = num_pos + 1
					elif (line[num_pos] == "."):
						is_real = True
						num_pos = num_pos + 1
					else:
						break

				if (is_real):
					pairs.append(['real', line[position:num_pos], num])
				else:
					pairs.append(['integer', line[position:num_pos], num])

				position = num_pos

			# Identifier
			elif (re.match('[a-zA-Z]', line[position])):

				id_pos = position

				while (id_pos < length):
					if (line[id_pos] == "$"):
						id_pos = id_pos + 1
						break
					elif (re.match('[a-zA-Z0-9]', line[id_pos])):
						id_pos = id_pos + 1
					else:
						break

				pairs.append(['identifier', line[position:id_pos], num])
				position = id_pos

			else:
				# Input is probably a whitespace or other non-printing char
				position = position + 1

	if not pairs:
		return None
	else:
		return pairs
