from sys import stdin
from utils import debug_print

class HTM1Process():

	def __init__(self, code):
		self.code = code
		self.stax = {}
		self.pc = 0

	def run(self):
		while True:
			if self.pc >= len(self.code):
				break
			else:
				command = self.code[self.pc]
				self.cmd(command)
		self.print_stax_ints()

	def print_stax_chars(self):
		accum = "stax: "
		print(self.stax)
		for i in range(len(self.stax)):
			if i not in self.stax:
				accum += "_"
			else:
				accum += chr(self.stax[i][-1])
			accum += " "
		debug_print(accum, "note")

	def print_stax_ints(self):
		accum = "stax: "
		for i in range(len(self.stax)):
			if i not in self.stax:
				accum += "_"
			else:
				accum += str(self.stax[i])
			accum += " "
		debug_print(accum, "note")

	def cmd(self, command):
		self.print_stax_ints()
		match command:
			case ("null",):
				debug_print("how the fuck", "fail")
			case ("push", x, y):
				debug_print(f"({self.pc}) pushing {y} to S{x}", "note")
				self.cmd_push(x, y)
			case ("pop", x, y):
				debug_print(f"({self.pc}) popping from S{x} to S{y}", "note")
				self.cmd_pop(x, y)
			case ("op", x, y):
				debug_print(f"({self.pc}) applying {y} to S{x}", "note")
				self.cmd_op(x, y)
			case ("break",):
				debug_print(f"({self.pc}) breaking", "note")
				self.cmd_break()
			case ("input", x):
				debug_print(f"({self.pc}) inputting to S{x}", "note")
				self.cmd_input(x)
			case ("output", x):
				debug_print(f"({self.pc}) outputting from S{x}", "note")
				self.cmd_output(x)
			case ("if", x, y):
				debug_print(f"({self.pc}) test S{x} == S{y}", "note")
				self.cmd_if(x, y)
			case ("endif",):
				debug_print(f"({self.pc}) end if", "note")
				self.cmd_endif()
			case ("loop",):
				debug_print(f"({self.pc}) looping", "note")
				self.cmd_loop()
			case ("endloop",):
				debug_print(f"({self.pc}) end loop", "note")
				self.cmd_endloop()
			case ("flip", x):
				debug_print(f"({self.pc}) flipping S{x}", "note")
				self.cmd_flip(x)
			case _:
				debug_print("unrecognised command", "warning")
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
			case "-":
				if len(s) >= 2:
					a = s.pop()
					b = s.pop()
					self.cmd_push(x, a-b)
			case "*":
				if len(s) >= 2:
					a = s.pop()
					b = s.pop()
					self.cmd_push(x, a*b)
			case "/":
				if len(s) >= 2:
					a = s.pop()
					b = s.pop()
					self.cmd_push(x, a//b)
			case "rm":
				if len(s) >= 1:
					s.pop()
			case "dup":
				if len(s) >= 1:
					a = s.pop()
					self.cmd_push(x, a)
					self.cmd_push(x, a)
			case "!":
				if len(s) >= 1:
					a = s.pop() != 0
					self.cmd_push(x, 1 if a else 0)
			case "=":
				if len(s) >= 2:
					a = s.pop()
					b = s.pop()
					self.cmd_push(x, 1 if a == b else 0)
			case "<":
				if len(s) >= 2:
					a = s.pop()
					b = s.pop()
					self.cmd_push(x, 1 if a < b else 0)

	def cmd_break(self):
		#debug_print(f"pc is {self.pc}, code is {self.code}", "note")
		while self.code[self.pc][0] != "endloop":
			self.pc += 1

	def cmd_input(self, x):
		ch = sys.stdin.read(1)
		self.cmd_push(x, ord(ch))

	def cmd_output(self, x):
		if x in self.stax and len(self.stax[x]) > 0:
			print(chr(self.stax[x][-1]), end="")

	def cmd_if(self, x, y):
		if x in self.stax and y in self.stax:
			if self.stax[x] != self.stax[y]:
				while self.code[self.pc][0] != "endif":
					#debug_print(f"pc is {self.pc}", "note")
					self.pc += 1
					if self.pc >= len(self.code):
						debug_print("missing endif, fell off end of program", "fail")
						break;

	def cmd_endif(self):
		pass

	def cmd_loop(self):
		pass

	def cmd_endloop(self):
		while self.code[self.pc][0] != "loop":
			self.pc -= 1
			if self.pc >= len(self.code):
				debug_print("missing endloop, fell off end of program", "fail")
				break;

	def cmd_flip(self, x):
		if x in self.stax:
			self.stax[x].reverse()
