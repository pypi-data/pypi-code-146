"""Tools to create country lists.

Helpers that can retrieve files from ISO servers with current ISO
codes and country names.

Also helpers for turning this lists into a runnable Python module
(countries.py) are provided.

These helpers are meant to be used from the debug schell. You can use
them like this::

  $ ./bin/kofactl debug
  >>> from waeup.kofa.utils.country_helpers import update_list
  >>> from waeup.kofa.utils.country_helpers import update_module
  >>> update_list()
  >>> update_module()

This will retrieve a current list of countries and their ISO codes
from iso-committee servers, store the file locally (countries.txt) and
afterwards compile a valid Python module (countries.py) out of the
list.

"""
import datetime
import os
import urllib

SRC_URL = 'http://www.iso.org/iso/list-en1-semic-3.txt'
COUNTRY_LIST = os.path.join(os.path.dirname(__file__), 'countries.txt')
COUNTRY_MODULE = os.path.join(os.path.dirname(__file__), 'countries.py')

TEMPLATE = """# -*- coding: utf-8 -*-
#
# This file was automatically generated. Please do not edit
#
from waeup.kofa.interfaces import MessageFactory as _

COUNTRIES = ${COUNTRY_LIST}
"""

def mangle_country_name(name):
    """Turn uppercase country names into capitalized.

    Some special cases are handled as well ('of', 'the', etc.)
    """
    name = name.replace('(', '( ') # handle letters following brackets
    name = ' '.join([x.capitalize() for x in name.split(' ')])
    name = name.replace('( ', '(')
    for term in ['Of', ' And', 'The']:
        name = name.replace(term, term.lower())
    name = name.replace('U.s.', 'U.S.')
    name = name.replace("D'i", "d'I") # Cote d'Ivoire
    return name

def update_list():
    """Update the local country.txt list.

    File is received from iso-servers.
    """
    print "Receiving list from %s" % SRC_URL
    contents = urllib.urlopen(SRC_URL).read()
    print "Storing list at %s" % COUNTRY_LIST
    fp = open(COUNTRY_LIST, 'wb')
    fp.write('Received on %s \r\nfrom %s\r\n-----------------\r\n' % (
        datetime.datetime.now(), SRC_URL))
    fp.write(contents)
    fp.close()
    print "Done."
    return

def mangle_list():
    """Read country list and extract countries and their ISO-codes.

    Returns an iterable of tuples (<COUNTRY>, <ISO-CODE>).
    """
    lines = open(COUNTRY_LIST, 'rb').readlines()
    read_header = False
    for num, line in enumerate(lines):
        if read_header is False and line != '\r\n':
            continue
        if read_header is False:
            read_header = True
            continue
        if line == '\r\n':
            continue
        line = line.decode('iso-8859-1').strip()
        try:
            country, code = line.split(';', 1)
        except:
            print "Could not process: line %s:", num, line
            continue
        yield mangle_country_name(country), code

def update_module(template=TEMPLATE, module_path=COUNTRY_MODULE):
    """Update local countries.py with data from countries.txt
    """
    print "Parsing countries and their ISO codes..."
    c_list = "(\n"
    for country, code in mangle_list():
        c_list = c_list + u'    (_(u"%s"), u"%s"),\n' % (country, code)
    c_list += ')\n'
    contents = template.replace('${COUNTRY_LIST}', c_list)
    contents = contents.encode('utf-8')
    print "Write new module:", module_path
    open(module_path, 'wb').write(contents)
    print "Done."
    return
