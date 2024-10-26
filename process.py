from sys import stdin
from utils import *

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
		for i in range(len(self.stax)):
			if i not in self.stax:
				accum += "_"
			else:
				accum += chr(self.stax[i][-1])
			accum += " "
		debug_note(accum)

	def print_stax_ints(self):
		accum = "stax: "
		for i in range(len(self.stax)):
			if i not in self.stax:
				accum += "_"
			else:
				accum += str(self.stax[i])
			accum += " "
		debug_note(accum)

	def cmd(self, command):
		self.print_stax_ints()
		match command:
			case ("null",):
				debug_fail("how the fuck")
			case ("push", x, y):
				debug_note(f"({self.pc}) pushing {y} to S{x}")
				self.cmd_push(x, y)
			case ("pop", x, y):
				debug_note(f"({self.pc}) popping from S{x} to S{y}")
				self.cmd_pop(x, y)
			case ("op", x, y):
				debug_note(f"({self.pc}) applying {y} to S{x}")
				self.cmd_op(x, y)
			case ("break",):
				debug_note(f"({self.pc}) breaking")
				self.cmd_break()
			case ("input", x, y):
				debug_note(f"({self.pc}) inputting to S{x} mode {y}")
				self.cmd_input(x, y)
			case ("output", x, y):
				debug_note(f"({self.pc}) outputting from S{x} mode {y}")
				self.cmd_output(x, y)
			case ("if", x, y):
				debug_note(f"({self.pc}) test S{x} == S{y}")
				self.cmd_if(x, y)
			case ("endif",):
				debug_note(f"({self.pc}) end if")
				self.cmd_endif()
			case ("loop",):
				debug_note(f"({self.pc}) looping")
				self.cmd_loop()
			case ("endloop",):
				debug_note(f"({self.pc}) end loop")
				self.cmd_endloop()
			case ("flip", x):
				debug_note(f"({self.pc}) flipping S{x}")
				self.cmd_flip(x)
			case _:
				debug_warning(f"unrecognised command {command}")
		self.pc += 1

	def cmd_push(self, x, y):
		if x not in self.stax:
			self.stax[x] = []
		self.stax[x].append(y)

	def cmd_pop(self, x, y):
		if x in self.stax:
			if len(self.stax[x]) > 0:
				popped = self.stax[x].pop()
				self.cmd_push(y, popped)

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

	def cmd_input(self, x, y):
		if y == 0:
			ch = stdin.read(1)
			self.cmd_push(x, ord(ch))
		else:
			n = int(input())
			self.cmd_push(x, n)

	def cmd_output(self, x, y):
		n = 0
		if x in self.stax and len(self.stax[x]) > 0:
			n = self.stax[x][-1]
		if y == 0:
			print(chr(n), end="")
		else:
			print(n)

	def cmd_if(self, x, y):
		if x in self.stax and y in self.stax:
			if self.stax[x] != self.stax[y]:
				while self.code[self.pc][0] != "endif":
					#debug_print(f"pc is {self.pc}", "note")
					self.pc += 1
					if self.pc >= len(self.code):
						debug_fail("missing endif, fell off end of program")

	def cmd_endif(self):
		pass

	def cmd_loop(self):
		pass

	def cmd_endloop(self):
		while self.code[self.pc][0] != "loop":
			self.pc -= 1
			if self.pc >= len(self.code):
				debug_fail("missing endloop, fell off end of program")

	def cmd_flip(self, x):
		if x in self.stax:
			self.stax[x].reverse()
