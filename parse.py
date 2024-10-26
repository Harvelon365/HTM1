from html.parser import HTMLParser
import htm1.py

stack = []

class HTMLParser(HTMLParser):
	def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
		i = -1
		while True:
			i += 1
			op = ()
			if attrs[i][0].lower() == 'id':
				# get op from id length
			else:
				# get op from tag length
				continue
			match op[1]:
					case 0:
						continue
					case 1:
						i += 1
						stack.append(len(attrs[i][1]))


def parseHTML(html):
	parser = HTMLParser()
	parser.feed(html)
	return stack
