import sys

command_kinds = [
	("null", 0),	# ignore						0
	("pop", 2),		# x = stack from, y = stack to	1	p i b
	("op", 2),		# x = stack, y = opcode			2	em ul ol li
	("break", 0),	#								3	div nav pre var
	("push", 2),	# x = stack, y  = data			4	code main span
	("input", 2),	# x = stack, y = is long str	5	aside title
	("output", 2),	# x = stack, y = is long str	6	figure header script
	("if", 2),		# x = stack a, y = stack b		7	article caption section
	("loop", 0),	#								8	noscript textarea
	("flip", 1),	# x = stack						9
    ("endif", 0),	#								10
    ("endloop", 0), #				 				11
]

operation_kinds = [
	"+",	# 0
	"-",	# 1
	"*",	# 2
	"/",	# 3
	"rm",	# 4
	"dup",	# 5
	"!",	# 6
	"=",	# 7
	"<",	# 8
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

	# prime number test, written up in examples/is_prime.htm1
	[
		("input", 0, 1), # S0 = n
		("push", 1, 1), # S1 = is prime
		("push", 2, 2), # S2 = i
		("op", 0, "dup"), # S3 = n / 2
		("pop", 0, 3),
		("push", 3, 2),
		("op", 3, "/"),
		#("push", 3, 1),
		#("op", 3, "+"),
		("push", 5, 1), # S5 = 1
		("loop",),
			("op", 3, "dup"), # S4 = S3 < S2
			("pop", 3, 4),
			("op", 2, "dup"),
			("pop", 2, 4),
			("op", 4, "<"),
			("if", 4, 5), # if S4, so S3 < S2, so n / 2 < i then break
				("break",),
			("endif",),
			("op", 4, "rm"),
			("op", 0, "dup"), # S6 = rem = n n i / i * -
			("pop", 0, 6),
			("op", 0, "dup"),
			("pop", 0, 6),
			("op", 2, "dup"),
			("pop", 2, 6),
			("op", 6, "/"),
			("op", 2, "dup"),
			("pop", 2, 6),
			("op", 6, "*"),
			("op", 6, "-"),
			("push", 7, 0), # S7 = rem == 0
			("if", 6, 7),
				("op", 1, "rm"), # is prime = 0
				("push", 1, 0),
				("break",),
			("endif",),
			("op", 7, "rm"),
			("op", 6, "rm"),
			("push", 2, 1),
			("op", 2, "+"),
		("endloop",),
		("output", 1, 1), # output is prime
		("op", 5, "rm"), # if is prime == 0
		("push", 5, 0),
		("if", 1, 5),
			("output", 2, 1), # factor
		("endif",),
	],
]

def set_debug(status):
	global is_debug
	is_debug = status

def debug_note(msg):
	if is_debug == 2:
		print(debug_colors["note"] + "☝ " + msg + debug_colors["end"])
	return

def debug_good(msg):
	if is_debug > 0:
		print(debug_colors["good"] + "😎 " + msg + debug_colors["end"])
	return

def debug_warning(msg):
	if is_debug > 0:
		print(debug_colors["warning"] + "😨 " + msg + debug_colors["end"])
	return

def debug_fail(msg):
	if is_debug > 0:
		print(debug_colors["fail"] + "💀 " + msg + debug_colors["end"])
	sys.exit(-1)
