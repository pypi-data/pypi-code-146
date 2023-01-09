#!/usr/bin/env python3

import os

# VARIABLES

PLATFORM_WIN = os.name == 'nt'

version = '1.0.0'
author = 'Pigeon Nation (+ Others - See PyPi page for Full Credits)'

# DATA

styles = {
	# Plain
	'standard': 0,
	'plain': 6,
	'bare': 9,
	
	# Standard
	'bold': 1,
	'italic': 3,
	'underline': 4,
	
	# Coloured
	'success': 2,
	'highlight-warn': 7,
	
	# Animated
	'blink': 5,
	
	# Other
	'invisible': 8
	
}

fgcolours = {
	# Grey-Scale
	'black': 30,
	'grey': 90,
	'white': 97,
	'dim-white': 37,
	
	# Standards
	'red': 31,
	'green': 32,
	'yellow': 93,
	'orange': 33,
	'blue': 34,
	'pink': 35,
	'aqua': 96,
	
	# Light Variants
	'light-blue': 36,
	
	# Bright Variants
	'bright-red': 91,
	'bright-green': 92,
	'bright-blue': 94,
	'bright-pink': 95
}

bgcolours = {
	# Grey-Scale
	'black': 40,
	'grey': 100,
	'white': 107,
	'dim-white': 47,
	
	# Standards
	'red': 41,
	'green': 42,
	'yellow': 103,
	'orange': 43,
	'blue': 44,
	'pink': 45,
	'aqua': 106,
	
	# Light Variants
	'light-blue': 46,
	
	# Bright-Variants
	'bright-red': 101,
	'bright-green': 102,
	'bight-blue': 104,
	'bright-pink': 105
	
}

_backend = {
	'end': '\033[0m'
}

# FUNCTIONS

# FROM STACKOVERFLOW - See PyPi page for credits.
def progress(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', ofill='-', printEnd = "\r"):
	"""
	Call in a loop to create terminal progress bar
	@params:
		iterable    - Required  : iterable object (Iterable)
		prefix      - Optional  : prefix string (Str)
		suffix      - Optional  : suffix string (Str)
		decimals    - Optional  : positive number of decimals in percent complete (Int)
		length      - Optional  : character length of bar (Int)
		fill        - Optional  : bar fill character (Str)
		printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
	"""
	
	total = len(iterable)
	
	# Progress Bar Printing Function
	def printProgressBar (iteration):
		percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
		filledLength = int(length * iteration // total)
		bar = fill * filledLength + ofill * (length - filledLength)
		print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
		
	# Initial Call
	printProgressBar(0)
	
	# Update Progress Bar
	for i, item in enumerate(iterable):
		yield item
		printProgressBar(i + 1)
		
	# Print New Line on Complete
	print()

def makecolour(text, *colours, endcolour=_backend['end']):
	return '\033[' + ';'.join([str(colour) for colour in colours])  + 'm' + text + endcolour

def clearscreen():
	os.system('cls' if PLATFORM_WIN else 'clear')

def outlog(*a, **k):
	print(*a, **k, file=sys.stdout)

def errlog(*a, **k):
	print(*a, **k, file=sys.stderr)

def inplog(*a, **k):
	return input(*a, **k,)