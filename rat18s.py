#!/usr/bin/env python3

import argparse
import os.path
import sys

from Parser import *

# Create our argument parser object
argparser = argparse.ArgumentParser(description='A Python3 compiler for the Rat18s language')

# Add our arguments to the parser
argparser.add_argument("file", help="Path to the file to compile")
argparser.add_argument("-v", "--verbose", help="Prints extra information", action='store_true')
argparser.add_argument("-d", "--debug", help="Turns on debug output", action='store_true')

# Make sure we have enough arguments, if not print the help message
if len(sys.argv) < 1:
	argparser.print_help()
	sys.exit(1)

# Actually parse the arguments
arguments = argparser.parse_args()

# Check that the file actually exists before continuing
if not os.path.exists(arguments.file):
	print(arguments.file, ": No such file exists!")
	sys.exit(1)

parser(arguments.file, arguments.verbose, arguments.debug)
