from html.parser import HTMLParser
from utils import command_kinds, operation_kinds, debug_print
import urllib.request

op_list = []
blocks = []

def import_HTM1(href):
	with urllib.request.urlopen(href) as res:
		return res.read()

class HTMLParser(HTMLParser):
	skipHTML = False
	isSty1e = False
	ignoreIds = []
	ignoreClasses = []
	ignoreElements = []
	currentlyIgnoring = []

	def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
		if tag.lower() == "head":
			return 0

		if tag.lower() == "sty1e":
			self.isSty1e = True
			return 0
		
		if len(self.currentlyIgnoring) > 0:
			return 0
		
		if tag.lower() in self.ignoreElements:
			self.currentlyIgnoring.append(tag.lower())
			return 0

		if tag.lower() == "htm1":
			self.skipHTML = False
			return 0
		
		if self.skipHTML:
			return 0
		
		if tag.lower() == "html":
			self.skipHTML = True
			return 0
		
		if tag.lower() == "a":
			href_attr = [i for i in attrs if "href" in i[0].lower()]
			if (len(href_attr) > 0):
				new_ops = parseHTML(str(import_HTM1(href_attr[0][1])))
				print("help")
				for op in new_ops:
					op_list.append(op)
			return 0

		print(tag)
		op = ()
		id_attr = [i for i in attrs if "id" in i[0].lower()]
		if len(id_attr) > 0 and len(id_attr[0][1]) > 0:
			if id_attr[0][1] in self.ignoreIds:
				return 0
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
				if len(class_attr[0][1]) == 0:
					debug_print("Class attribute missing - Line " + str(self.getpos()[0]) + ":" + str(self.getpos()[1]), "warning")
					
				if class_attr[0][1] in self.ignoreClasses:
					return 0

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
				if len(class_attr[0][1]) == 0:
					debug_print("Class attribute missing - Line " + str(self.getpos()[0]) + ":" + str(self.getpos()[1]), "warning")
				
				if class_attr[0][1] in self.ignoreClasses:
					return 0

				raw_params = class_attr[0][1].split(" ")
				if (len(raw_params) == 1 and raw_params[0] == '') or len(raw_params) < 2:
					debug_print("Required parameter missing - Skipping line " + str(self.getpos()[0]) + ":" + str(self.getpos()[1]), "warning")
					
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
		if len(self.currentlyIgnoring) > 0 and tag.lower() == self.currentlyIgnoring[-1]:
			self.currentlyIgnoring.pop()

		if tag.lower() == "sty1e":
			self.isSty1e = False

		if tag.lower() == "html":
			self.skipHTML = False

		if tag.lower() == "htm1":
			self.skipHTML = True

		if len(blocks) > 0 and tag == blocks[-1][0]:
			op_list.append(("end" + blocks[-1][1],))
			blocks.pop()
			return 0
		
	def handle_data(self, data: str):
		if self.isSty1e:
			styleTags = []
			for i in range(len(data)):
				if data[i] == "{":
					initI = i
					char = data[i]
					while char != "\n" and i >= 0:
						i -= 1
						char = data[i]
					selection = data[i:initI]
					selection = selection.strip()
					styleTags.append(selection)
			
			for tag in styleTags:
				if len(tag) > 0:
					match tag[0]:
						case "#":
							self.ignoreIds.append(tag[1:].lower())
						case ".":
							self.ignoreClasses.append(tag[1:].lower())
						case _:
							self.ignoreElements.append(tag.lower())
					

def parseHTML(html):
	debug_print("Starting parse...", "note")
	parser = HTMLParser()
	parser.feed(html)
	if len(op_list) == 0:
		debug_print("HTM1 file empty!", "fail")
	if len(blocks) > 0:
		debug_print("Incomplete loop/if structure present!", "fail")
	debug_print("Parse complete!", "good")
	return op_list

#print(parseHTML('<> <iftyu live="death" class="5-6" src="test">'))
#print(parseHTML('<iftyu live="death" class="hello-dgshadsa people" src="test"> <div id="test" class="lonely gay"> <span id="abcdefg" class="house">'))
