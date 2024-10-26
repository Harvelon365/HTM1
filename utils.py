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
    ("endif", 0),	#
    ("endloop", 0), #
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

debug_colors = {
    "note": '\033[96m',
    "good": '\033[92m',
	"warning": '\033[93m',
    "fail": '\033[91m',
    "end": '\033[0m'
}

is_debug = True

def debug_print(msg, msgKind):
	if is_debug:
		match msgKind:
			case "note":
				print(debug_colors["note"] + "☝ " + msg + debug_colors["end"])
			case "good":
				print(debug_colors["good"] + "😎 " + msg + debug_colors["end"])
			case "warning":
				print(debug_colors["warning"] + "😬 " + msg + debug_colors["end"])
			case "fail":
				print(debug_colors["fail"] + "💀 " + msg + debug_colors["end"])
