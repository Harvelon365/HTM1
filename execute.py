test_code = [
	("push", 1, 3),
	("push", 1, 2),
	("op", 1, "+"),
	("output", 1),
]

class Htm1Process(code):
	self.code = code
	self.stax = {}
	self.trace = []

	def run():
		for i in self.code:
			self.cmd(i)

	def cmd(command):
		match command:
			case ("null"):
				print("how the fuck")
			case ("push", x, y):
				self.cmd_push(x, y)
			case ("pop", x, y):
				pass
			case ("op", x, y):
				pass
			case ("break"):
				pass
			case ("input", x):
				pass
			case ("output", x):
				pass
			case ("if", x):
				pass
			case ("loop"):
				pass
			case ("flip", x):
				pass

	def cmd_push(stax, x, y):
		if x not in stax:
			stax[x] = []
		stax[x].append(y)

def exe_htm1(htm1_code):
	proc = Htm1Process(htm1_code)
	proc.run()
