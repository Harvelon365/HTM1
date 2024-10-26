from html.parser import HTMLParser
from utils import command_kinds, debug_print

op_list = []

class HTMLParser(HTMLParser):
	def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
		op = ()
		id_attr = [i for i in attrs if "id" in i]
		if len(id_attr) > 0 and len(id_attr[0][1]) > 0:
			op = command_kinds[len(id_attr[0][1])]
		else:
			op = command_kinds[len(tag)]

		match op[1]:
			case 0:
				op_list.append((op[0],))
			case 1:
				class_attr = [i for i in attrs if "class" in i]
				if len(class_attr) == 0:
					debug_print("Class attribute missing - Line " + str(self.getpos()[0]) + ":" + str(self.getpos()[1]), "fail")
					quit()

				raw_params = class_attr[0][1].split(" ")
				if len(raw_params) == 1 and raw_params[0] == '':
					debug_print("Required parameter missing - Line " + str(self.getpos()[0]) + ":" + str(self.getpos()[1]), "fail")
					quit()

				digits = raw_params[0].split("-")
				number = ""
				for digit in digits:
					if digit.isnumeric() and len(digit) == 1:
						number = str(number) + digit
					else:
						number = str(number) + str(len(digit))

				op_list.append((op[0], int(number)))
				
			case 2:
				class_attr = [i for i in attrs if "class" in i]
				if len(class_attr) == 0:
					debug_print("Class attribute missing - Line " + str(self.getpos()[0]) + ":" + str(self.getpos()[1]), "fail")
					quit()

				raw_params = class_attr[0][1].split(" ")
				if (len(raw_params) == 1 and raw_params[0] == '') or len(raw_params) < 2:
					debug_print("Required parameter missing - Line " + str(self.getpos()[0]) + ":" + str(self.getpos()[1]), "fail")
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

				op_list.append((op[0], params[0], params[1]))
					

def parseHTML(html):
	debug_print("Starting parse...", "note")
	parser = HTMLParser()
	parser.feed(html)
	if len(op_list) == 0:
		debug_print("HTM1 file empty!", "warning")
		quit()
	debug_print("Parse complete!", "good")
	return op_list

print(parseHTML('<> <iftyu live="death" class="5-6" src="test">'))
#print(parseHTML('<iftyu live="death" class="hello-dgshadsa people" src="test"> <div id="test" class="lonely gay"> <span id="abcdefg" class="house">'))