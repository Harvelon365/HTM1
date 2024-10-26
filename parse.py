from html.parser import HTMLParser
from htm1 import command_kinds

op_list = []

class HTMLParser(HTMLParser):
	def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
		op = ()
		id_attr = [i for i in attrs if "id" in i]
		if len(id_attr) > 0:
			op = command_kinds[len(id_attr[0][1])]
		else:
			op = command_kinds[len(tag)]

		match op[1]:
			case 0:
				op_list.append((op[0]))
			case 1:
				class_attr = [i for i in attrs if "class" in i][0]
				raw_params = class_attr[1].split(" ")

				digits = raw_params[0].split("-")
				number = ""
				for digit in digits:
					number = str(number) + str(len(digit))

				op_list.append((op[0], int(number)))
				
			case 2:
				class_attr = [i for i in attrs if "class" in i][0]
				raw_params = class_attr[1].split(" ")

				params = []
				for param in raw_params:
					digits = param.split("-")
					number = ""
					for digit in digits:
						number = str(number) + str(len(digit))
					params.append(int(number))

				op_list.append((op[0], params[0], params[1]))
					

def parseHTML(html):
	parser = HTMLParser()
	parser.feed(html)
	return op_list

print(parseHTML('<iftyu live="death" class="hello people" src="test"> <div id="test" class="lonely gay"> <span id="abcdefgh" class="house">'))
