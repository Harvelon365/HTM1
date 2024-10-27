from bs4 import BeautifulSoup, Tag
from utils import *
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

def parse_command(elem):
	if type(elem) == Tag:
		debug_note(f"parsing {elem.name}")
		for i in elem.contents:
			parse_command(i)

def convertToInstruction(element):
	if element.name in ignoreElements or element.id in ignoreIds or element['class'] in ignoreClasses:
		return 0

def parseHTM1(htm1):
	debug_note("Starting parse...")
	# parse the htm1
	soup = BeautifulSoup(htm1, "html.parser")

	# deal with sty1esheets
	# TODO <1ink>
	ignore_selectors = ["sty1e"]
	for i in soup.css.select("sty1e"):
		ignore_selectors.extend(parse_selectors(i.string))
	for i in ignore_selectors:
		print(soup.css.select(i))
		for j in soup.css.select(i):
			j.decompose()
	soup.smooth()

	commands = parse_command(soup.contents[0])

	if len(op_list) == 0:
		debug_fail("HTM1 file empty!")
	if len(blocks) > 0:
		debug_fail("Incomplete loop/if structure present!")
	debug_good("Parse complete!")

	return op_list

#parseHTM1('<head><sty1e>span {}</sty1e></head><body id="hello"> <iftyu live="death" class="hello-dgshadsa people" src="test"> <div id="test" class="lonely gay"> <span id="abcdefg" class="house"></body>')
