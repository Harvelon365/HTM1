#!/usr/bin/env python3

import utils
from utils import debug_print
from parser import parseHTM1
from process import HTM1Process
import argparse
import pathlib
import time

argparser = argparse.ArgumentParser(prog="HTM1 Interpreter", 
									description="An interpreter system for the HTM1 esoteric programming language",
									epilog="Visit https://github.com/Harvelon365/HTM1 to see the full readme and docs")
argparser.add_argument("-f","--filename", type=pathlib.Path, default=None, help="the .htm1 file you want to execute")
argparser.add_argument("-d", "--debug", help="enable debug mode", action="store_true")
argparser.add_argument("-t", "--test", type=int, help="run test program with id")
args = argparser.parse_args()

def main():
	if args.filename != None:
		f = open(args.filename, "r")
		proc = HTM1Process(parseHTM1(f.read()))
		proc.run()
	elif args.test != None:
		proc = HTM1Process(utils.test_programs[args.test])
		proc.run()
	else:
		debug_print("no program", "fail")

if __name__ == '__main__':
	if (args.debug):
		utils.is_debug = True
	else:
		utils.is_debug = False
	main()
