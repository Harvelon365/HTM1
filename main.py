#!/usr/bin/env .venv/bin/python3

from utils import *
from parser import parseHTM1
from process import HTM1Process
import argparse
import pathlib

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
		proc = HTM1Process(test_programs[args.test])
		proc.run()
	else:
		debug_fail("No program specified")

if __name__ == '__main__':
	if (args.debug):
		is_debug = True
	else:
		is_debug = False
	main()
