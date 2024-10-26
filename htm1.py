from enum import Enum

command_kinds = [
	("null", 0),	# ignore
	("push", 2),	# x = stack, y  = data
	("pop", 2),		# x = stack from, y = stack to
	("op", 2),		# x = stack, y = opcode
	("break", 0),	#
	("input", 1),	# x = stack
	("output", 1),	# x = stack
	("if", 1),		# x = stack
	("loop", 0),	#
	("flip", 1),	# x = stack
]

operation_kinds = [
	"+",
	"-",
	"*",
	"/",
	"delete",
	"duplicate",
]

