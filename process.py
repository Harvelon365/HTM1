import sys.stdin
from utils import debug_print

test_code1 = [
	("push", 1, ord("a")),
	("push", 1, 2),
	("op", 1, "+"),
	("output", 1),
]

test_code2 = [
	()
]

class HTM1Process():

	def __init__(self, code):
		self.code = code
		self.stax = {}
		self.pc = 0

	def run(self):
		while True:
			if self.pc == len(self.code):
				break
			else:
				command = self.code[self.pc]
				self.cmd(command)

	def print_stax_chars(self):
		accum = "stax: "
		print(self.stax)
		for i in range(len(self.stax)):
			if i + 1 not in self.stax:
				accum += "_"
			else:
				accum += chr(self.stax[i + 1][-1])
			accum += " "
		debug_print(accum, "note")

	def print_stax_ints(self):
		accum = "stax: "
		for i in range(len(self.stax)):
			if i + 1 not in self.stax:
				accum += "_"
			else:
				accum += str(self.stax[i + 1][-1])
			accum += " "
		debug_print(accum, "note")

	def cmd(self, command):
		self.print_stax_ints()
		match command:
			case ("null"):
				print("how the fuck")
			case ("push", x, y):
				self.cmd_push(x, y)
			case ("pop", x, y):
				self.cmd_pop(x, y)
			case ("op", x, y):
				self.cmd_op(x, y)
			case ("break"):
				pass
			case ("input", x):
				pass
			case ("output", x):
				self.cmd_output(x)
			case ("if", x):
				pass
			case ("endif", x):
				pass
			case ("loop"):
				pass
			case ("endloop", x):
				pass
			case ("flip", x):
				pass
		self.pc += 1

	def cmd_push(self, x, y):
		if x not in self.stax:
			self.stax[x] = []
		self.stax[x].append(y)

	def cmd_pop(self, x, y):
		if x in self.stax:
			if len(self.stax[x]) > 0:
				popped = stax[x].pop()
				cmd_push(y, popped)

	def cmd_op(self, x, y):
		if x not in self.stax:
			self.stax[x] = []
		s = self.stax[x]
		match y:
			case "+":
				if len(s) >= 2:
					a = s.pop()
					b = s.pop()
					self.cmd_push(x, a+b)

	def cmd_break(self):
		while self.code[pc] != "endloop":
			self.pc += 1

	def cmd_input(self, x):
		ch = sys.stdin.read(1)
		self.cmd_push(x, ord(ch))

	def cmd_output(self, x):
		if x in self.stax and len(self.stax[x]) > 0:
			print(chr(self.stax[x][-1]))

def startProcessing(html):
	proc = HTM1Process(html)
	proc.run()
