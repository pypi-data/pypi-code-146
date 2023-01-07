###############################################################################
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program. If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

__author__ = 'Donovan Parks'
__copyright__ = 'Copyright 2015'
__credits__ = ['Donovan Parks']
__license__ = 'GPL3'
__maintainer__ = 'Donovan Parks'
__email__ = 'donovan.parks@gmail.com'

import csv
import hashlib
import re


def sha256(input_file):
    """Calculate the SHA256 hash for a specific file.

    :param input_file: str, Name of file.

    :return: str, SHA256 hash.

    """

    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with open(input_file, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)

    return hasher.hexdigest()

def sha256_rb(input_file):
    """Calculate SHA256 hash for a specific file with a binary format.

    :param input_file: str, Name of file.

    :return: str, SHA256 hash.

    """

    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with input_file as onefile:
        buf = onefile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = onefile.read(BLOCKSIZE)

    return hasher.hexdigest()

def select_delimiter(input_file):
    """Select delimiter for a specific file (.csv,.tsv,...).

    :param input_file: str, Name of file.

    :return: str, Delimiter.

    """
    with open(input_file) as f:
        first_line = f.readline()
        # detect the separator
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(first_line)
        return dialect.delimiter

def matching_brackets(line):
    """Split a string to a list with matching brackets.
    a string a split into substrings based on matching brackets. so we can return nested brackets.

    :param line: str, line to be processed.

    :return: list, list of strings.
    """

    result, start_parens_count, end_parens_count, term = [], 0, 0, ""
    for x in re.split(r"([\[\]])", line):
        if not x.strip():
            continue
        elif x == "[":
            if start_parens_count > 0:
                term += "["
            start_parens_count += 1
        elif x == "]":
            end_parens_count += 1
            if end_parens_count == start_parens_count:
                result.append(term)
                end_parens_count, start_parens_count, term = 0, 0, ""
            else:
                term += "]"
        elif start_parens_count > end_parens_count:
            term += x
        else:
            result.extend(x.strip(" ").split(" "))


    return result