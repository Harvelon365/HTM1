import sys

command_kinds = [
	("null", 0),	# ignore						0
	("pop", 2),		# x = stack from, y = stack to	1
	("op", 2),		# x = stack, y = opcode			2
	("break", 0),	#								3
	("push", 2),	# x = stack, y  = data			4
	("input", 1),	# x = stack						5
	("output", 1),	# x = stack						6
	("if", 2),		# x = stack a, y = stack b		7
	("loop", 0),	#								8
	("flip", 1),	# x = stack						9
    ("endif", 0),	#								10
    ("endloop", 0), #								11
]

operation_kinds = [
	"+",
	"-",
	"*",
	"/",
	"rm",
	"dup",
	"!",
	"=",
	"<",
]

debug_colors = {
    "note": '\033[96m',
    "good": '\033[92m',
	"warning": '\033[93m',
    "fail": '\033[91m',
    "end": '\033[0m'
}

is_debug = True

test_programs = [
	# add two numbers
	[
		("push", 1, ord("a")),
		("push", 1, 2),
		("op", 1, "+"),
		("output", 1),
	],

	# count to 5
	[
		("push", 0, 0),
		("push", 1, 5),
		("loop",),
		("if", 0, 1),
		("break",),
		("endif",),
		("push", 0, 1),
		("op", 0, "+"),
		("endloop",),
	],

	# prime number test
	[

	],
]

def debug_print(msg, msgKind):
	if is_debug:
		match msgKind:
			case "note":
				print(debug_colors["note"] + "☝ " + msg + debug_colors["end"])
			case "good":
				print(debug_colors["good"] + "😎 " + msg + debug_colors["end"])
			case "warning":
				print(debug_colors["warning"] + "😨 " + msg + debug_colors["end"])
			case "fail":
				print(debug_colors["fail"] + "💀 " + msg + debug_colors["end"])
				sys.exit(-1)
