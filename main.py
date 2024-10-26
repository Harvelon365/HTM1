import utils
from parse import parseHTML
from process import startProcessing
import argparse
import pathlib

argparser = argparse.ArgumentParser(prog="HTM1 Interpreter", description="An interpreter system for the HTM1 esoteric programming language")
argparser.add_argument("filename", type=pathlib.Path)
argparser.add_argument("-d", "--debug", help="enable debug mode", action="store_true")

def main():
    startProcessing(parseHTML('<iftyu live="death" class="5-6" src="test">'))

if __name__ == '__main__':
    args = argparser.parse_args()
    if (args.debug):
        utils.is_debug = True
        print("debug")
    else:
        utils.is_debug = False
    main()