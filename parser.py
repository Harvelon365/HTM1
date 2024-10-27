from bs4 import BeautifulSoup, Tag
from utils import *
import urllib.request

# the new parser, using beatifulsoup

commands = []
ignoreIds = []
ignoreElements = []
ignoreClasses = []

def import_HTM1(href):
	with urllib.request.urlopen(href) as res:
		return str(res.read()).replace("\\n", "\n")

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
	if type(elem) == Tag:
		debug_note(f"parsing {elem.name}")

		if elem.name == "a" and "href" in elem.attrs.keys():
			commands.extend(parseHTM1(import_HTM1(elem["href"])))
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

			commands.append(command)

		for i in elem.contents:
			parse_command(i)

		if command[0] == "if" or command[0] == "loop":
			commands.append(("end" + command[0],))

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
	digits = [str(i) for i in digits]
	total = int("".join(digits))
	return total

def parseHTM1(htm1):

	debug_good("Starting parse...")
	# parse the htm1
	soup = BeautifulSoup(htm1, "html.parser")

	# deal with sty1esheets
	# TODO <1ink>
	ignore_selectors = ["sty1e"]
	for i in soup.css.select("sty1e"):
		ignore_selectors.extend(parse_selectors(i.string))
	for i in ignore_selectors:
		for j in soup.css.select(i):
			j.decompose()
	soup.smooth()

	parse_command(soup.contents[0])

	if len(commands) == 0:
		debug_fail("HTM1 file empty!")
	debug_good("Parse complete!")

	#print(commands)
	for c in commands:
		print(c)
	return commands

#parseHTM1('<head><sty1e>span {}</sty1e></head><body id="hello"> <iftyu live="death" class="hello-dgshadsa people" src="test"> <div id="test" class="lonely gay"> <span id="abcdefg" class="house"></body>')
