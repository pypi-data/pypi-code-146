#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#


__version__ = "41"


import unittest
import doctest
import sys
import os

#curdir = os.path.abspath(".")
curdir = os.getcwd()
sys.path.insert(0, curdir + os.sep)
sys.path.insert(0, curdir + os.sep + '..' + os.sep)

needs_sphinx='1.1'
nitpick_ignore=[
                ('py:class', 'builtins.BaseException'),
               ]

extensions=[
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.viewcode',
    #'rst2pdf.pdfbuilder'
]
autosummary_generate=True
autodoc_default_flags=['members', 'undoc-members', 'private-members', "imported-members", 'show-inheritance']
autodoc_member_order='alphabetical'
autodoc_member_order='groupwise'
autodoc_docstring_signature=True
autoclass_content="class"
doctest_global_setup=""
doctest_global_cleanup=""
doctest_test_doctest_blocks="default"
trim_doctest_flags=True
doctest_flags=doctest.REPORT_UDIFF
templates_path=['_templates',]
source_suffix = '.rst'
source_encoding = 'utf-8-sig'
master_doc = 'index'
project = "KAMER"
copyright = 'Public Domain'
version = '%s' % __version__
release = '%s' % __version__
language = ''
today = ''
today_fmt = '%B %d, %Y'
exclude_patterns = ['_build', "_sources", "_templates"]
default_role = ''
add_function_parentheses = True
add_module_names = False
show_authors = True
pygments_style = 'sphinx'
modindex_common_prefix = [""]
keep_warnings = True
html_theme = "bizstyle"
html_theme_options = {
     "nosidebar": True,
}
html_theme_path = []
html_short_title = "KAMER %s" % __version__
html_favicon = "jpg/aes.ico"
html_static_path = []
html_extra_path = []
html_last_updated_fmt = '%Y-%b-%d'
html_additional_pages = {}
html_domain_indices = True
html_use_index = True
html_split_index = True
html_show_sourcelink = False
html_show_sphinx = False
html_show_copyright = False
html_copy_source = False
html_use_opensearch = 'http://kamer.rtfd.io/'
html_file_suffix = '.html'
htmlhelp_basename = 'pydoc'
intersphinx_mapping = {
                       'python': ('https://docs.python.org/3', 'objects.inv'),
                       'sphinx': ('http://sphinx.pocoo.org/', None),
                      }
intersphinx_cache_limit=1
rst_prolog = """.. image:: bewijsgif4.jpg
    :height: 2.2cm
    :width: 100%
    :target: index.html
    
.. title:: Prosecutor. Court, Reconsider OTP-CT-117/19.

""" 

rst_epilog = """.. raw:: html

    <br>
    <center><b>


:ref:`home <home>` - :ref:`source <source>`


.. raw:: html

    </b></center>
"""
