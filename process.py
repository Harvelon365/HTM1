from sys import stdin
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

	def command_str(self, cmd):
		accum = cmd[0]
		if len(cmd) >= 2:
			accum += f" {cmd[1]}"
		if len(cmd) >= 3:
			accum += f" {cmd[2]}"
		return accum

	def cmd(self, command):
		self.print_stax_ints()
		debug_print("exec: " + self.command_str(command), "note")
		match command:
			case ("null"):
				debug_print("how the fuck", "fail")
			case ("push", x, y):
				self.cmd_push(x, y)
			case ("pop", x, y):
				self.cmd_pop(x, y)
			case ("op", x, y):
				self.cmd_op(x, y)
			case ("break"):
				self.cmd_break()
			case ("input", x):
				self.cmd_input(x)
			case ("output", x):
				self.cmd_output(x)
			case ("if", x):
				self.cmd_if(x)
			case ("endif"):
				self.cmd_endif()
			case ("loop"):
				self.cmd_loop()
			case ("endloop"):
				self.cmd_endloop()
			case ("flip", x):
				self.cmd_flip(x)
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

	def cmd_if(self, x):
		if x in self.stax:
			if self.stax[x] == 0:
				while self.code[pc] != "endif":
					self.pc += 1

	def cmd_endif(self):
		pass

	def cmd_loop(self):
		pass

	def cmd_endloop(self):
		while self.code[pc] != "loop":
			self.pc -= 1

	def cmd_flip(self, x):
		if x in self.stax:
			self.stax[x].reverse()

def startProcessing(html):
	proc = HTM1Process(html)
	proc.run()

startProcessing(test_code1)
