from utils import is_debug
from parse import parseHTML
from process import exe_htm1
import argparse

def main():
    exe_htm1(parseHTML('<iftyu live="death" class="5-6" src="test">'))

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(prog="HTM1 Interpreter", description="An interpreter system for the HTM1 esoteric programming language")
    argparser.add_argument("filename")
    argparser.add_argument("-d", "--debug", help="Enable debug mode")
    main()