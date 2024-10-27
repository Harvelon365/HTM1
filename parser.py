from bs4 import BeautifulSoup, Tag
from utils import *
import urllib.request
import time

# the new parser, using beatifulsoup

ignoreIds = []
ignoreElements = []
ignoreClasses = []
hold = ""
soup = []

def import_HTM1(href):
	with urllib.request.urlopen(href) as res:
		return res.read() #).decode("utf-8").replace("\\n", "\n")

def parse_selectors(css):
	selectors = []
	for i in range(len(css)):
		if css[i] == "{":
			initI = i
			char = css[i]
			while char != "\n" and i >= 0:
				i -= 1
				char = css[i]
			selection = css[i:initI]
			selection = selection.strip()
			selectors.append(selection)
	return selectors

def parse_command(elem):
	ignore_me = False
	commands = []
	if type(elem) == Tag:

		if elem.name == "a" and "href" in elem.attrs.keys():
			parseHTM1(import_HTM1(elem["href"]), len(soup))
			ignore_me = True

		command_id = 0
		if "id" in elem.attrs.keys():
			command_id = len(elem["id"])
		else:
			command_id = len(elem.name)
		command = (command_kinds[command_id][0],)

		expected_n_params = command_kinds[command_id][1]

		if "class" in elem.attrs.keys():
			classes = elem["class"]
			if len(classes) < expected_n_params:
				debug_warning("Incorrect amount of classes found. Skipping element '" + elem.name + "'")
				ignore_me = True
		else:
			if expected_n_params != 0:
				debug_warning("Incorrect amount of classes found. Skipping element '" + elem.name + "'")
				ignore_me = True

		if not ignore_me:
			if expected_n_params > 0:
				command += (parse_class(classes[0]),)
			if expected_n_params > 1:
				if command[0] == "op":
					command += (operation_kinds[parse_class(classes[1])],)
				else:
					command += (parse_class(classes[1]),)

			debug_note(f"parsed {elem.name.rjust(12)} -> {command}")
			commands.append(command)


		for i in elem.contents:
			if type(i) == Tag:
				commands.extend(parse_command(i))

		#time.sleep(0.1 * len(elem.contents))
		if command[0] == "if" or command[0] == "loop":
			commands.append(("end" + command[0],))
		return commands

def parse_class(class_name):
	digits = []
	i = 0
	while i < len(class_name):
		if class_name[i].isnumeric():
			digits.append(class_name[i])
		elif class_name[i] == "_" or class_name[i] == "-":
			pass
		else:
			if i == 0 or class_name[i - 1].isnumeric() or class_name[i - 1] == "_" or class_name[i - 1] == "-":
				digits.append(0)
			digits[-1] += 1
		i += 1
	if len(digits) == 0:
		digits = [0]
	digits = [str(i) for i in digits]
	total = int("".join(digits))
	return total

def classify_int(n):
	class_name = ""
	digits = list(str(n))
	if n == 0:
		return "_"
	class_name += ("a" * int(digits.pop(0)))
	for i in digits:
		class_name += i
	return class_name
def htm1ify_commands(commands):
	elems = ""
	for i in commands:
		match i:
			case ("null",):
				pass
			case ("pop", x, y):
				elems += f"<p class='{classify_int(x)} {classify_int(y)}'></p>"
			case ("op", x, y):
				opcode = operation_kinds.index(y)
				elems += f"<li class='{classify_int(x)} {classify_int(opcode)}'></li>"
			case ("break",):
				elems += f"<div class=''></div>"
			case ("push", x, y):
				elems += f"<span class='{classify_int(x)} {classify_int(y)}'></span>"
			case ("input", x, y):
				elems += f"<aside class='{classify_int(x)} {classify_int(y)}'></aside>"
			case ("output", x, y):
				elems += f"<script class='{classify_int(x)} {classify_int(y)}'></script>"
			case ("if", x, y):
				elems += f"<section class='{classify_int(x)} {classify_int(y)}'>"
			case ("loop",):
				elems += f"<p id='aaaaaaaa'>"
			case ("flip", x):
				elems += f"<p id='aaaaaaaaa' class='{classify_int(x)}'></p>"
			case ("endif",):
				elems += f"</section>"
			case ("endloop",):
				elems += f"</p>"
		elems += "\n"
	return elems

def parseHTM1(htm1, s):

	debug_good("Starting parse...")
	global soup
	# parse the htm1
	soup.append(BeautifulSoup(htm1, "html.parser"))

	# deal with sty1esheets
	# TODO <1ink>
	ignore_selectors = ["sty1e"]
	for i in soup[s].css.select("sty1e"):
		ignore_selectors.extend(parse_selectors(i.string))
	for i in ignore_selectors:
		for j in soup[s].css.select(i):
			j.decompose()
	soup[s].smooth()

	commands = parse_command(soup[s].contents[0])

	if len(commands) == 0:
		debug_fail("HTM1 file empty!")
	debug_good("Parse complete!")

	#print(commands)
	#for c in commands:
		#print(c)
	#print(soup)
	return commands

#parseHTM1('<head><sty1e>span {}</sty1e></head><body id="hello"> <iftyu live="death" class="hello-dgshadsa people" src="test"> <div id="test" class="lonely gay"> <span id="abcdefg" class="house"></body>')

