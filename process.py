test_code = [
	("push", 1, ord("a")),
	("push", 1, 2),
	("op", 1, "+"),
	("output", 1),
]

class Htm1Process(code):
	self.code = code
	self.stax = {}
	self.trace = []

	def run(self):
		for i in self.code:
			self.cmd(i)

	def cmd(self, command):
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
				pass
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

	def output(self, x):
		print()

def exe_htm1(htm1_code):
	proc = Htm1Process(htm1_code)
	proc.run()
