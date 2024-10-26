from html.parser import HTMLParser
from utils import command_kinds, operation_kinds, debug_print

op_list = []
blocks = []

class HTMLParser(HTMLParser):
	skipHTML = False

	def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
		if tag.lower() == "htm1":
			self.skipHTML = False
			return 0
		
		if self.skipHTML:
			return 0
		
		if tag.lower() == "html":
			self.skipHTML = True
			return 0

		op = ()
		id_attr = [i for i in attrs if "id" in i[0].lower()]
		if len(id_attr) > 0 and len(id_attr[0][1]) > 0:
			op = command_kinds[len(id_attr[0][1])]
		else:
			op = command_kinds[len(tag)]

		if (op[0] == "loop" or op[0] == "if"):
			blocks.append((tag, op[0]))

		match op[1]:
			case 0:
				op_list.append((op[0],))
			case 1:
				class_attr = [i for i in attrs if "class" in i[0].lower()]
				if len(class_attr) == 0:
					debug_print("Class attribute missing - Line " + str(self.getpos()[0]) + ":" + str(self.getpos()[1]), "fail")
					quit()

				raw_params = class_attr[0][1].split(" ")
				if len(raw_params) == 1 and raw_params[0] == '':
					debug_print("Required parameter missing - Skipping line " + str(self.getpos()[0]) + ":" + str(self.getpos()[1]), "warning")
					return 0

				digits = raw_params[0].split("-")
				number = ""
				for digit in digits:
					if digit.isnumeric() and len(digit) == 1:
						number = str(number) + digit
					else:
						number = str(number) + str(len(digit))

				op_list.append((op[0], int(number)))
				
			case 2:
				class_attr = [i for i in attrs if "class" in i[0].lower()]
				if len(class_attr) == 0:
					debug_print("Class attribute missing - Line " + str(self.getpos()[0]) + ":" + str(self.getpos()[1]), "fail")
					quit()

				raw_params = class_attr[0][1].split(" ")
				if (len(raw_params) == 1 and raw_params[0] == '') or len(raw_params) < 2:
					debug_print("Required parameter missing - Skipping line " + str(self.getpos()[0]) + ":" + str(self.getpos()[1]), "warning")
					quit()

				params = []
				for param in raw_params:
					digits = param.split("-")
					number = ""
					for digit in digits:
						if digit.isnumeric() and len(digit) == 1:
							number = str(number) + digit
						else:
							number = str(number) + str(len(digit))
					params.append(int(number))

				if (op[0] == "op"):
					op_list.append((op[0], params[0], operation_kinds[params[1]]))
				else:
					op_list.append((op[0], params[0], params[1]))

	def handle_endtag(self, tag: str):
		if tag.lower() == "html":
			self.skipHTML = False

		if tag.lower() == "htm1":
			self.skipHTML = True

		if len(blocks) > 0 and tag == blocks[-1][0]:
			op_list.append(("end" + blocks[-1][1],))
			blocks.pop()
			return 0
					

def parseHTML(html):
	debug_print("Starting parse...", "note")
	parser = HTMLParser()
	parser.feed(html)
	if len(op_list) == 0:
		debug_print("HTM1 file empty!", "warning")
		quit()
	if len(blocks) > 0:
		debug_print("Incomplete loop/if structure present!", "fail")
		quit()
	debug_print("Parse complete!", "good")
	return op_list

#print(parseHTML('<> <iftyu live="death" class="5-6" src="test">'))
#print(parseHTML('<iftyu live="death" class="hello-dgshadsa people" src="test"> <div id="test" class="lonely gay"> <span id="abcdefg" class="house">'))