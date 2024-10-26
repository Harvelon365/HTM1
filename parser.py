from bs4 import BeautifulSoup, Tag
from utils import command_kinds, operation_kinds, debug_print
import urllib.request

# the new parser, using beatifulsoup

op_list = []
ignoreIds = []
ignoreElements = []
ignoreClasses = []

def import_HTM1(href):
	with urllib.request.urlopen(href) as res:
		return res.read()

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

def parse_commands(elem):
	if elem.name != None:
		print("tag", elem.name)
	if type(elem) == Tag:
		for i in elem.contents:
			parse_commands(i)

def convertToInstruction(element):
	if element.name in ignoreElements or element.id in ignoreIds or element['class'] in ignoreClasses:
		return 0

def parseHTM1(htm1):
	debug_print("Starting parse...", "note")
	# parse the htm1
	soup = BeautifulSoup(htm1, "html.parser")
	ignore_selectors = ["sty1e"]
	for i in soup.css.select("sty1e"):
		ignore_selectors.append(parse_selectors(i.string))
	#convertToInstruction(soup.body)
	commands = parse_commands(soup.contents[0])
	# build the op_list
	if len(op_list) == 0:
		debug_print("HTM1 file empty!", "fail")
	if len(blocks) > 0:
		debug_print("Incomplete loop/if structure present!", "fail")
	debug_print("Parse complete!", "good")
	return op_list

#parseHTM1('<head><sty1e>span {}</sty1e></head><body id="hello"> <iftyu live="death" class="hello-dgshadsa people" src="test"> <div id="test" class="lonely gay"> <span id="abcdefg" class="house"></body>')
