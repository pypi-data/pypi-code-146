# -*- coding: utf-8 -*-
# @copyright: MIT License
#   Copyright (c) 2018 syntactic (Pastèque Ho)
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#   The above copyright notice and this permission notice shall be included in all
#   copies or substantial portions of the Software.
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#   SOFTWARE.
# @summary: This file generates all strings described by a non-recursive JSGF grammar.
#   Run it by entering into the command line: python DeterministicGenerator.py <grammarFile>
#   where <grammarFile> is the path to the JSGF grammar.
# @since: 2014/06/02

"""
This file deterministically generates strings from a JSGF Grammar, whether there are \
        weights defined in rules or not. It requires one argument: the path to the JSGF\
        Grammar file. You can run this on the included grammar IdeasNonRecursive.gram:\


        ``python DeterministicGenerator.py IdeasNonRecursive.gram``

This will generate all strings defined by the public rules of IdeasNonRecursive.gram.\
        It is important that the grammar used by the generator is not recursive (rules \
        should not directly or indirectly reference themselves), so that the generator\
        terminates. Otherwise, you may get a maximum recursion depth exceeded error or \
        a segmentation fault.
"""

import sys, itertools
from parser import *
from grammar import *
from ParseUtils import processRHS


if __name__ == '__main__':
    fileStream = open(sys.argv[1])
    grammar = parser.getGrammarObject(fileStream)
    for rule in grammar.publicRules:
        expansions = processRHS(rule.rhs, grammar)
        for expansion in expansions:
            print(expansion)
