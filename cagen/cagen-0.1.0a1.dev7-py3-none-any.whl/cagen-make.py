#!/usr/bin/env python
import argparse

maketemplate = """
# Default template
TMPHTML5 = templates/schema.tmpl

# Select all markdowns file except index.md
MARKDOWNS = $(shell find . -type f -name "*.md" ! -name "index.md")

# Replace the extension.
# By default HTML5
MARKDOWNS_HTML5 = $(MARKDOWNS:.md=.html)

# Commands

SSG = ./cagen.py

# Processing

.PHONY: all clean

all: $(MARKDOWNS_HTML5)

# .MD.HTML -> .HTML
%.html: %.md
\t$(SSG) $< $@ $(TMPHTML5) 

clean:
\trm $(MARKDOWNS_HTML5)
"""


parser = argparse.ArgumentParser(prog = "cagen-make", description="creates a Makefile file for using GNU Make to generate HTML5 files using cagen")
parser.add_argument("--init", action='store_true', help="creates the Makefile")
args = parser.parse_args()

if args.init:
    with open("Makefile", "w") as f:
        f.write(maketemplate)
else:
    print("See --help for hints")

