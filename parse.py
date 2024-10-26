from html.parser import HTMLParser
from htm1 import command_kinds

op_list = []

class HTMLParser(HTMLParser):
	def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
		i = -1
		while True:
			i += 1
			op = ()
			if attrs[i][0].lower() == 'id':
				op = commands[len(attrs[i][1])]
			else:
				op = commands[len(tag)]

			match op[1]:
					case 0:
						continue
					case 1:
						i += 1
						op_list.append(len(attrs[i][1]))


def parseHTML(html):
	parser = HTMLParser()
	parser.feed(html)
	return stack
