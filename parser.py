from bs4 import BeautifulSoup
import cssutils
from utils import command_kinds, operation_kinds, debug_print
import urllib.request

op_list = []
blocks = []
ignoreIds = []
ignoreElements = []
ignoreClasses = []

def import_HTM1(href):
    with urllib.request.urlopen(href) as res:
        return res.read()
    
def computeSty1e(styleText):
    styleTags = []
    for i in range(len(styleText)):
        if styleText[i] == "{":
            initI = i
            char = styleText[i]
            while char != "\n" and i >= 0:
                i -= 1
                char = styleText[i]
            selection = styleText[i:initI]
            selection = selection.strip()
            styleTags.append(selection)
    
    for tag in styleTags:
        if len(tag) > 0:
            match tag[0]:
                case "#":
                    ignoreIds.append(tag[1:].lower())
                case ".":
                    ignoreClasses.append(tag[1:].lower())
                case _:
                    ignoreElements.append(tag.lower())
    
def convertToInstruction(element):
    if element.name in ignoreElements or element.id in ignoreIds or element['class'] in ignoreClasses:
        return 0
    
def parseHTM1(htm1):
    debug_print("Starting parse...", "note")
    # parse the htm1
    soup = BeautifulSoup(htm1, "html.parser")
    computeSty1e(soup.sty1e.string)
    convertToInstruction(soup.body)
    # build the op_list
    if len(op_list) == 0:
        debug_print("HTM1 file empty!", "fail")
    if len(blocks) > 0:
        debug_print("Incomplete loop/if structure present!", "fail")
    debug_print("Parse complete!", "good")
    return op_list

#parseHTM1('<head></head><body id="hello"> <iftyu live="death" class="hello-dgshadsa people" src="test"> <div id="test" class="lonely gay"> <span id="abcdefg" class="house"></body>')