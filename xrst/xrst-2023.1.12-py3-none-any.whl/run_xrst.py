#! /usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Bradley M. Bell <bradbell@seanet.com>
# SPDX-FileContributor: 2020-23 Bradley M. Bell
# ----------------------------------------------------------------------------
"""
{xrst_begin run_xrst user}
{xrst_spell
   config
   dev
   furo
   github
   jax
   pdf
   pyspellchecker
   rtd
   thet
   toc
   toml
   txt
   wil
}

Run Extract Sphinx RST And Sphinx
#################################

Syntax
******
It may be helpful to remove the :ref:`config_file@directory@html_directory`
before running the command below.
This will check for error messages that are not repeated due
to caching the results of previous builds.

| ``xrst`` \\
| |tab| [ ``--version`` ] \\
| |tab| [ ``--local_toc`` ] \\
| |tab| [ ``--page_source`` ] \\
| |tab| [ ``--rst_line_numbers`` ] \\
| |tab| [ ``--rst_only`` ] \\
| |tab| [ ``--index_page_name`` *index_page_name* ] \\
| |tab| [ ``--config_file``     *config_file* ] \\
| |tab| [ ``--html_theme``      *html_theme* ] \\
| |tab| [ ``--target``          *target* ]  \\
| |tab| [ ``--group_list``      *group_name_1* *group_name_2* ... ] \\
| |tab| [ ``--rename_group``    *old_group_name* *new_group_name* ] \\
| |tab| [ ``--replace_spell_commands`` ] \\
{xrst_comment --------------------------------------------------------------- }

version
*******
If ``--version`` is present on the command line,
the version of xrst is printed and none of the other arguments matter.
{xrst_comment --------------------------------------------------------------- }

local_toc
*********
If this option is present on the command line,
a table of contents for the Headings in the current page
is included at the top of every page.
The page name and page title are not in this table of contents.

Some :ref:`html themes<run_xrst@html_theme>` include this information
on a side bar; e.g., ``furo`` and ``sphinx_book_theme`` .
{xrst_comment --------------------------------------------------------------- }

page_source
***********
If this option is present and *target* is ``html`` ,
a link to the xrst source code is included at the top of each page.
Some :ref:`html themes<run_xrst@html_theme>` include this link; e.g.,
``sphinx_rtd_theme`` .

If this option is present and *target* is ``tex`` ,
the xrst source code file is reported at the beginning of each page.
{xrst_comment --------------------------------------------------------------- }

rst_line_numbers
****************
Normally sphinx error and warning messages are reported using line numbers
in the xrst source code files.
If this option is present, these messages are reported
using the line numbers in the RST files created by xrst.
In addition the :ref:`run_xrst@page_source` links to the rst files,
instead of the xrst source files.
This may be helpful if you have an error or warning for a sphinx command
and it does not make sense using xrst source code line numbers.
It is also helpful for determining if an incorrect line number is due to
sphinx or xrst.
{xrst_comment --------------------------------------------------------------- }

rst_only
********
Normally, after extraction the RST files,
xrst automatically runs sphinx to produce the target output (html or tex).
If this option is present, sphinx not run.
Only the rst files, and their corresponding sources,
are generated; i.e.,

| |tab| :ref:`config_file@directory@rst_directory`/\*.rst
| |tab| *rst_directory*\ /_sources/\*.txt

This may be useful when creating rst files for uses else where; e.g.,
for use with `Read the Docs <https://docs.readthedocs.io>`_ .
The sphinx commands are printed after xrst finishes and can be executed
by hand.
This may be useful if there is a problem during these commands.
{xrst_comment --------------------------------------------------------------- }

index_page_name
***************
This option has no effect when *target* is ``tex`` .
If *target* is ``html``,
the file ``index.html`` in the
:ref:`config_file@directory@html_directory` will be a redirect
to the page specified by *index_page_name* .
If this option is not present, ``index.html`` wil be a redirect
to the root of the documentation tree.
{xrst_comment --------------------------------------------------------------- }

config_file
***********
The command line argument *config_file* specifies the location of the
:ref:`config_file-name` for this project.
This can be an absolute path or
relative to the directory where :ref:`xrst<run_xrst-name>` is run.

xrst.toml
=========
If *config_file* is not present on the command line,
the default value ``xrst.toml`` is used for *config_file* .
{xrst_comment --------------------------------------------------------------- }

html_theme
**********
This the html_theme_ that is used.
The default value for *html_theme* is ``furo`` .

.. _html_theme: https://sphinx-themes.org/

Theme Choices
=============
The following is a list of some themes that work well with the
default settings in :ref:`config_file@html_theme_options` .
If you have a theme together with html_theme_options
that work well with xrst,
please post an issue on github so that it can be added to the list below.

{xrst_spell_off}
.. csv-table:: Sphinx Themes
   :header: name,  local_toc

   sphinx_rtd_theme,     yes
   furo,                 no
   sphinx_book_theme,    no
   pydata_sphinx_theme,  no
   piccolo_theme,        no
{xrst_spell_on}

sphinx_rtd_theme
================
The sphinx_rtd theme builds faster than some of the other themes,
so it is suggested to use it for testing (with the ``--local_toc`` option).
A special modification is made to this theme when *target* is html,
so that it displays wider than its normal limit.
This modification may be removed in the future.
{xrst_comment --------------------------------------------------------------- }

target
******
The optional command line argument *target* must be ``html`` or ``tex``.
It specifies the type of type output you plan to generate using sphinx.
Note thet :ref:`config_file@directory@html_directory` and
:ref:`config_file@directory@tex_directory` will determine the location
of the corresponding output files.
The default value for *target* is ``html`` .

tex
===
If you choose this target, xrst will create the file
*project_name*\ ``.tex`` in the :ref:`config_file@directory@tex_directory` .
There are two reasons to build this file.
One is to create the file *project_name*\ ``.pdf``
which is a pdf version of the documentation.
The other is to test for errors in the latex sections of the documentation.
(MathJax displays latex errors in red, but one has to check
every page that has latex to find all the errors this way.)
Once you have built *project_name*\ ``.tex``, the following command
executed in :ref:`config_file@directory@project_directory`
will accomplish both purposes:

   make -C *tex_directory* *project_name*\ ``.pdf``

#. The :ref:`config_file@project_name` is specified in the configuration file.
#. The resulting output file will be *project*\ ``.pdf`` in the
   *tex_directory* .
#. If a Latex error is encountered, the pdf build will stop with a message
   at the ``?`` prompt. If you enter ``q`` at this prompt, it will complete
   its processing in batch mode. You will be able to find the error messages
   in the file *project_name*\ ``.log`` in the *tex_directory* .
#. Translating Latex errors to the corresponding xrst input file:

   #. Latex error messages are reported using line numbers in
      the file *project*\ ``.tex`` .
   #. You may be able to find the corresponding xrst input file
      using by using ``grep`` to find text that is near the error.
   #. The page numbers in the :ref:`xrst_table_of_contents-title` are
      present in the latex input (often near ``section*{`` above the error)
      and may help translate these line numbers to page names.
   #. Given a page name, the corresponding xrst input file can
      be found at the top of the html version of the page.
{xrst_comment --------------------------------------------------------------- }

group_list
**********
It is possible to select one or more groups of pages
to include in the output using this optional argument.

#. The *group_list* is a list of one or more
   :ref:`group names<begin_cmd@group_name>`.
#. The :ref:`begin_cmd@group_name@Default Group` is represented by
   the group name ``default`` .
#. The order of the group names determines their order in the resulting output.
#. The default value for *group_list* is ``default`` .

For each group name in the *group_list*
there must be an entry in :ref:`config_file@root_file` specifying the
root file for that group name.

The xrst examples are a subset of its user documentation
and its user documentation is a subset of its developer documentation.
For each command, the same source code file provides both the
user and developer documentation. In addition, the developer documentation
has links to the user documentation and the user documentation has links
to the examples.

Example
=======
The examples commands below assume you have cloned the
`xrst git repository <https://github.com/bradbell/xrst>`_
and it is your current working directory.

#. The xrst examples use the default group
   and their documentation can be built using

      ``xrst --group_list default``

#. The xrst user documentation uses the default and user groups
   and its documentation can be built using

      ``xrst --group_list default user``

#. The xrst developer documentation uses the default, user, and dev
   groups and its documentation can be built using

      ``xrst --group_list default user dev``
{xrst_comment --------------------------------------------------------------- }

rename_group
************
If this option is present on the command line,
the :ref:`begin_cmd@group_name` in a subset of the source code, is changed.
This option replaces the :ref:`run_xrst@group_list`
by the list whose only entry is *new_group_name* .
None of the output files are created when rename_group is present;
e.g., the \*.rst and \*.html files.

old_group_name
==============
is the old group name for the pages that will have their group name replaced.
Use ``default``, instead of the empty group name, for the
:ref:`begin_cmd@group_name@Default Group` .

new_group_name
==============
Only the pages below the :ref:`config_file@root_file`
for *new_group_name* are modified.
You can rename a subset of the old group by making the root file
for the new group different than the root file for the old group.
Each page in the old group, and below the root file for the new group,
will have its group name changed from *old_group_name* to *new_group_name*.
Use ``default``, instead of the empty group name, for the
:ref:`begin_cmd@group_name@Default Group` .
{xrst_comment --------------------------------------------------------------- }

replace_spell_commands
**********************
If this option is present on the command line, the source code
:ref:`spell commands<spell_cmd-name>` are replaced in such a way that the
there will be no spelling warnings during future processing by xrst.
This is useful when there are no spelling warnings before a change
to the :ref:`config_file@project_dictionary` or when there is an update
of the pyspellchecker_ package (which is used to do the spell checking).
If this option is present,
none of the output files are created; e.g., the \*.rst and \*.html files.

.. _pyspellchecker: https://pypi.org/project/pyspellchecker

{xrst_end run_xrst}
"""
# ---------------------------------------------------------------------------
# imports
# ---------------------------------------------------------------------------
import sys
import re
import os
import toml
import string
import shutil
import filecmp
import argparse
import subprocess
# ---------------------------------------------------------------------------
# system_exit
# Error messages in this file do not use xrst.system_exit because
# they do not have file names that are relative to the project_directory.
def system_exit(msg) :
   # assert False, msg
   sys.exit(msg)
# ---------------------------------------------------------------------------
# Execute a system command
#
# command:
# the command to execute
#
# warning:
# If a warning is printed, this flag is set True
#
# page_name2line_pair
# a mapping from page name to to a list of line number pairs.
# The first number is the pair is a line number in the rst file for this page.
# The secon number is a corresponding xrst input line number.
#
# page_name2file_in
# a mapping from page name to the correspoind xrst input file.
#
def system_command(
      command                    ,
      warning                    ,
      page_name2line_pair = None ,
      page_name2file_in   = None ,
) :
   assert type(command) == str
   #
   assert type(warning) == list
   assert len(warning) == 1
   assert type(warning[0]) == bool
   #
   if page_name2line_pair != None :
      assert type(page_name2line_pair) == dict
      assert type(page_name2file_in) == dict
   #
   # subprocess.run, stderr
   print(command)
   command = command.split(' ')
   result = subprocess.run(command, capture_output = True)
   stderr = result.stderr.decode('utf-8')
   ok     =  result.returncode == 0 and stderr == ''
   if ok :
      return
   if page_name2line_pair == None :
      message  = stderr
      if result.returncode == 0 :
         message  += 'Warning: see system command message above.\n'
         sys.stderr.write(message)
         warning[0] = True
         return
      message  += 'Error: see system command message above.\n'
      system_exit(message)
   #
   # pattern_error
   pattern_error = re.compile( r'.*/rst/([a-z0-9_.]+).rst:([0-9]+):' )
   #
   # message
   message = ''
   #
   # error
   stderr_list = stderr.split('\n')
   for error in stderr_list :
      #
      # m_rst_error
      m_rst_error = pattern_error.search(error)
      if m_rst_error == None :
            if error != '' :
               # This should not happen
               # breakpoint()
               pass
      else :
         #
         # page_name
         page_name = m_rst_error.group(1)
         if not page_name in page_name2line_pair :
            assert page_name == 'xrst_table_of_contents'
         else :
            #
            # rst_line
            rst_line  = int( m_rst_error.group(2) )
            #
            # file_in, line_pair
            file_in   = page_name2file_in[page_name]
            line_pair = page_name2line_pair[page_name]
            #
            # n_pair
            n_pair = len(line_pair)
            #
            # index
            index  = 0
            while index < n_pair and line_pair[index][0] < rst_line :
                  index += 1
            #
            # line_before, line_after
            if index == n_pair :
               line_before = str( line_pair[n_pair-1][1] )
               line_after  = '?'
            elif line_pair[index][0] == rst_line :
               line_before = line_pair[index][1]
               line_after  = line_pair[index][1]
            elif 0 == index :
               line_before = '?'
               line_after  = line_pair[index][1]
            else :
               line_before = line_pair[index-1][1]
               line_after  = line_pair[index][1]
            #
            # error
            msg   = error[ m_rst_error.end()  : ]
            if line_before == line_after :
               error = f'{file_in}:{line_before}:{msg}'
            else :
               error = f'{file_in}:{line_before}-{line_after}:{msg}'
      #
      # message
      message += '\n' + error
   #
   if result.returncode == 0 :
      message  += 'Warning: see system command message above.\n'
      sys.stderr.write(message)
      warning[0] = True
      return
   message  += 'Error: see system command message above.\n'
   system_exit(message)
# ---------------------------------------------------------------------------
def fix_latex(latex_dir, project_name) :
   assert type(latex_dir) == str
   assert type(project_name) == str
   #
   # file_name
   file_name = f'{latex_dir}/{project_name}.tex'
   #
   # file_data
   file_obj  = open(file_name, 'r')
   file_data = file_obj.read()
   file_obj.close()
   #
   # file_data
   pattern   = re.compile( r'\n\\section{' )
   file_data = pattern.sub( r'\n\\section*{', file_data)
   #
   # file_data
   pattern   = re.compile( r'\n\\subsection{' )
   file_data = pattern.sub( r'\n\\subsection*{', file_data)
   #
   # file_data
   pattern   = re.compile( r'\n\\subsubsection{' )
   file_data = pattern.sub( r'\n\\subsubsection*{', file_data)
   #
   # file_name
   file_obj  = open(file_name, 'w')
   file_obj.write(file_data)
   file_obj.close()
   #
   return
# ---------------------------------------------------------------------------
# sys.path
# used so that we can test before installing
if( os.getcwd().endswith('/xrst.git') ) :
   if( os.path.isdir('xrst') ) :
      sys.path.insert(0, os.getcwd() )
#
import xrst
#
# version
# The script that updates version numbers expects version at begining of line
# and to have the value surrounded by single quotes.
version = '2023.1.12'
#
def run_xrst() :
   #
   # execution_directory
   execution_directory = os.getcwd()
   #
   # parser
   parser = argparse.ArgumentParser(
      prog='xrst', description='extract Sphinx RST files'
   )
   parser.add_argument('--version', action='store_true',
      help='just print version of xrst'
   )
   parser.add_argument('--local_toc', action='store_true',
      help='add a local table of contents at the top of each page'
   )
   parser.add_argument('--page_source', action='store_true',
      help='add link to the xrst source code be included at top of each page'
   )
   parser.add_argument(
      '--index_page_name', metavar='index_page_name', default='xrst_root_doc',
      help='The file index.html will be a redirect to this page' + \
         '(default is root of documentation tree)'
   )
   parser.add_argument(
      '--config_file', metavar='config_file', default='xrst.toml',
      help='location of the xrst configuration file which is in toml format' + \
         '(default is .)'
   )
   parser.add_argument(
      '--html_theme', metavar='html_theme', default='furo',
      help='sphinx html_theme that is used to display web pages ' + \
         '(default is furo)',
   )
   parser.add_argument(
      '--group_list', nargs='+', default='default',
      metavar= 'group_name' ,
      help='list of group_names to include in this build (default is default)'
   )
   parser.add_argument(
      '--rename_group', nargs=2, default=None,
      metavar=('old_group_name', 'new_group_name'),
      help='list of group_names to include in this build (default is default)'
   )
   parser.add_argument(
      '--target', metavar='target', choices=['html', 'tex'], default='html',
      help='type of output files, choices are html or tex (default is html)'
   )
   parser.add_argument('--replace_spell_commands', action='store_true',
      help='replace the xrst spell commands in source code files'
   )
   parser.add_argument('--rst_line_numbers', action='store_true',
      help='report sphinx errors and warnings using rst file line numbers'
   )
   parser.add_argument('--rst_only', action='store_true',
      help='report sphinx errors and warnings using rst file line numbers'
   )
   #
   # arguments
   arguments = parser.parse_args()
   #
   if arguments.version :
      print(version)
      sys.exit(0)
   #
   # local_toc
   local_toc = arguments.local_toc
   #
   # page_source
   page_source = arguments.page_source
   #
   # index_page_name
   index_page_name = arguments.index_page_name
   #
   # config_file
   # can not use system_exit until os.getcwd() returns project_directory
   config_file = arguments.config_file
   if not os.path.isfile(config_file) :
      msg  = 'xsrst: Error\n'
      msg += f'config_file = {config_file}\n'
      if config_file[0] == '/' :
         msg += 'is not a file\n'
      else :
         msg += f'is not a file relative to the execution directory\n'
         msg += execution_directory
      system_exit(msg)
   #
   # conf_dict
   conf_dict  = xrst.get_conf_dict(config_file)
   #
   # config_dir
   index = config_file.rfind('/')
   if 0 <= index :
      config_dir = config_file[: index]
      os.chdir(config_dir)
   #
   # project_directory
   project_directory = conf_dict['directory']['project_directory']
   #
   # make project directory the current working directory
   os.chdir(project_directory)
   #
   # replace_spell_commands
   replace_spell_commands = arguments.replace_spell_commands
   #
   # rst_line_numbers
   rst_line_numbers = arguments.rst_line_numbers
   #
   # rst_only
   rst_only = arguments.rst_only
   #
   # html_theme
   html_theme = arguments.html_theme
   #
   # group_list
   group_list = arguments.group_list
   if type(group_list) == str :
      group_list = [ group_list ]
   #
   # rename_group, group_list
   rename_group = arguments.rename_group
   if rename_group != None :
      group_list = [ rename_group[1] ]
      #
      if rename_group[0] == '' :
         msg = 'xrst rename_group: old_group_name is empty.\n'
         msg += 'Use "default" for the empty group name.'
         system_exit(msg)
      if rename_group[1] == '' :
         msg = 'xrst rename_group: new_group_name is empty.\n'
         msg += 'Use "default" for the empty group name.'
         system_exit(msg)
   #
   # replace_spell_commands or rename_group
   if replace_spell_commands or rename_group != None :
      if replace_spell_commands :
         option = 'replace_spell_commands'
      else :
         option = 'rename_group'
      #
      cwd      = os.getcwd()
      prompt   = f'\nThe {option} option will change some of \n'
      prompt  += 'the files read by xrst. Make sure that you have a backup\n'
      prompt  += f'of source files in {cwd}\n'
      prompt  += 'before contining this operation: continue [yes/no] ? '
      response = None
      while response not in [ 'yes', 'no' ]:
         response = input(prompt)
      if response != 'yes' :
         system_exit( f'xrst: aborting {option}' )
   #
   # target
   target = arguments.target
   #
   # target_directory
   if target == 'html' :
      target_directory = conf_dict['directory']['html_directory']
   else :
      assert target == 'tex'
      target_directory = conf_dict['directory']['tex_directory']
   #
   # rst_directory
   rst_directory = conf_dict['directory']['rst_directory']
   if rst_directory[0] == '/' :
      msg  = 'rst_directory = ' + rst_directory + '\n'
      msg += 'must be a path relative to the project_directory'
      xrst.system_exit(msg)
   #
   if not os.path.isdir(rst_directory) :
      os.makedirs(rst_directory)
   #
   # rst2project_directory
   # relative path from the rst_directory to the project directory
   rst2project_directory = os.path.relpath(
      os.getcwd() , rst_directory
   )
   #
   # tmp_dir
   tmp_dir = rst_directory + '/tmp'
   if os.path.isdir(tmp_dir) :
      shutil.rmtree(tmp_dir)
   os.mkdir(tmp_dir)
   #
   # _sources
   if not os.path.isdir(rst_directory + '/_sources') :
      os.mkdir(rst_directory + '/_sources')
   #
   # spell_checker
   spell_list  = list()
   for entry in conf_dict['project_dictionary']['data'] :
      word_list = entry.split('\n')
      for word in word_list :
         word = word.strip(' \t')
         if len(word) > 0 :
            spell_list.append(word)
   package       = conf_dict['spell_package']['data']
   spell_checker = xrst.get_spell_checker(spell_list, package)
   #
   # not_in_index_list
   not_in_index_list = list()
   for entry in conf_dict['not_in_index']['data'] :
      pattern_list = entry.split('\n')
      for pattern in pattern_list :
         pattern = pattern.strip(' \t')
         try :
            not_in_index_list.append( re.compile(pattern) )
         except :
            msg  = f'not_in_index table in config_file = {config_file}\n'
            msg += f'The regular expression "{pattern}" would not compile'
            system_exit(msg)
   # -------------------------------------------------------------------------
   #
   # input_file_list
   input_file_list = None
   #
   # root_file
   root_file = conf_dict['root_file']
   #
   # project_name
   project_name = conf_dict['project_name']['data']
   #
   # all_page_info
   # This list accumulates over all the group names
   all_page_info  = list()
   #
   # root_page_list
   # Each group has a root secion (in root_file) at the top if its tree.
   root_page_list = list()
   #
   # page_name2line_pair, page_name2file_in
   # Each rst page name has a corresponding input file and mapping from
   # rst file line nubmers to input file line numbers.
   page_name2line_pair = dict()
   page_name2file_in   = dict()
   #
   # any_warning
   any_warning = [ False ]
   #
   # group_name
   for group_name in group_list :
      #
      # old_group_name, new_group_name
      if rename_group == None :
         old_group_name = group_name
         new_group_name = group_name
      else :
         old_group_name = rename_group[0]
         new_group_name = rename_group[1]
         assert new_group_name == group_name
      #
      if new_group_name not in root_file :
         msg  = f'The group name {new_group_name} is '
         if rename_group == None :
            msg += 'in --group_list\n'
         else :
            msg += 'is new_group_name in --rename_group\n'
         msg += 'but it is not a valid key for the root_file table of\n'
         msg += f'the configuration file {config_file}'
         xrst.system_exit(msg)
      #
      if not os.path.isfile( root_file[new_group_name] ) :
         file_name = root_file[new_group_name]
         msg  = f'The root_file for group_name {new_group_name} is not a file\n'
         msg += f'file name = {file_name}'
         xrst.system_exit(msg)
      #
      # finfo_stack, finfo_done
      # This information is by file, not page
      finfo_stack      = list()
      finfo_done       = list()
      finfo = {
         'file_in'        : root_file[new_group_name],
         'parent_file'    : None,
         'parent_page'    : None,
      }
      finfo_stack.append(finfo)
      #
      while 0 < len(finfo_stack) :
         #
         # finfo
         # pop first element of stack so that order in tex file and
         # table of contents is correct
         finfo  = finfo_stack.pop(0)
         #
         for finfo_tmp in finfo_done :
            if finfo_tmp['file_in'] == finfo['file_in'] :
               msg  = 'The file ' + finfo['file_in']
               msg += '\nis included twice with '
               msg += f'group_name = "{old_group_name}"\n'
               msg += 'Once in ' + finfo_tmp['parent_file'] + '\n'
               msg += 'and again in ' + finfo['parent_file'] + '\n'
               xrst.system_exit(msg)
         finfo_done.append(finfo)
         #
         file_in              = finfo['file_in']
         parent_file          = finfo['parent_file']
         parent_file_page  = finfo['parent_page']
         assert os.path.isfile(file_in)
         #
         # get xrst docuemntation in this file
         file_page_info = xrst.get_file_info(
            all_page_info,
            old_group_name,
            parent_file,
            file_in,
         )
         #
         # root_page_list
         if finfo['parent_file'] == None :
            assert file_in == root_file[new_group_name]
            if file_page_info[0]['is_parent'] :
               n_page = 1
            else :
               n_page = len( file_page_info )
            for i_page in range( n_page ) :
               page_name = file_page_info[i_page]['page_name']
               root_page_list.append(page_name)
         #
         # parent_page_file_in
         # index in all_page_info of parent page for this file
         parent_page_file_in = None
         if file_page_info[0]['is_parent'] :
            parent_page_file_in = len(all_page_info)
         #
         # add this files pages to all_page_info
         for i_page in range( len(file_page_info) ) :
            # ------------------------------------------------------------
            # page_name, page_data, is_parent, begin_line
            page_name  = file_page_info[i_page]['page_name']
            page_data  = file_page_info[i_page]['page_data']
            is_parent  = file_page_info[i_page]['is_parent']
            is_child   = file_page_info[i_page]['is_child']
            begin_line = file_page_info[i_page]['begin_line']
            end_line   = file_page_info[i_page]['end_line']
            #
            # parent_page
            if is_parent or parent_page_file_in is None :
               parent_page = parent_file_page
            else :
               parent_page = parent_page_file_in
            #
            # all_page_info
            all_page_info.append( {
               'page_name'      : page_name,
               'file_in'        : file_in,
               'parent_page'    : parent_page,
               'in_parent_file' : is_child,
               'begin_line'     : begin_line,
               'end_line'       : end_line,
            } )
            # -------------------------------------------------------------
            # comment_command
            page_data = xrst.comment_command(page_data)
            # -------------------------------------------------------------
            # spell_command
            # do after suspend and before other commands to help ignore
            # pages of text that do not need spell checking
            page_data, spell_warning = xrst.spell_command(
               tmp_dir,
               page_data,
               file_in,
               page_name,
               begin_line,
               spell_checker,
            )
            if spell_warning :
               any_warning[0] = True
            # -------------------------------------------------------------
            # dir commands
            page_data = xrst.dir_command(page_data, rst2project_directory)
            # -------------------------------------------------------------
            # toc commands
            page_data, child_file, child_page_list = \
               xrst.toc_commands(
                  page_data,
                  file_in,
                  page_name,
                  old_group_name,
            )
            #
            # page_index, finfo_stack
            page_index = len(all_page_info) - 1
            for file_tmp in child_file :
               finfo_stack.append( {
                  'file_in'        : file_tmp,
                  'parent_file'    : file_in,
                  'parent_page'    : page_index,
               } )
            # ------------------------------------------------------------
            # code commands
            page_data = xrst.code_command(
               page_data,
               file_in,
               page_name,
               rst2project_directory,
            )
            # ------------------------------------------------------------
            # literal command
            page_data = xrst.literal_command(
               page_data,
               file_in,
               page_name,
               rst2project_directory,
            )
            # ------------------------------------------------------------
            # process headings
            #
            # pseudo_heading, all_page_info
            page_data, page_title, pseudo_heading = \
            xrst.process_headings(
               local_toc,
               page_data,
               file_in,
               page_name,
               not_in_index_list,
            )
            # all_page_info
            # page title is used by table_of_contents
            all_page_info[page_index]['page_title'] = page_title
            # -------------------------------------------------------------
            # list_children
            # page_name for each of the children of the current page
            list_children = child_page_list
            if is_parent :
               for i in range( len(file_page_info) ) :
                  if i != i_page :
                     list_children.append(
                        file_page_info[i]['page_name']
                     )
            # -------------------------------------------------------------
            # process children
            # want this as late as possible so toctree at end of input
            page_data = xrst.process_children(
               page_name,
               page_data,
               list_children,
            )
            # -------------------------------------------------------------
            #
            # line_pair and file tmp_dir/page_name.rst
            line_pair = xrst.temporary_file(
               page_source,
               target,
               pseudo_heading,
               file_in,
               tmp_dir,
               page_name,
               page_data,
            )
            #
            # page_name2line_pair, page_name2file_in
            page_name2line_pair[page_name] = line_pair
            page_name2file_in[page_name]   = file_in
      #
      # check_input_files
      if rename_group == None :
         toc_file_set = set()
         for finfo_tmp in finfo_done :
            toc_file_set.add( finfo_tmp['file_in'] )
         input_file_list, file_list_warning = xrst.check_input_files(
            config_file, conf_dict, group_name, toc_file_set, input_file_list
         )
         if file_list_warning :
            any_warning[0] = True
   #
   # index_page_name
   ok = index_page_name == 'xrst_root_doc' or target == 'tex'
   for page_info in all_page_info :
      ok = ok or page_info['page_name'] == index_page_name
   if not ok :
      msg = f'index_page_name = {index_page_name} is not a valid page name.'
      xrst.system_exit(msg)
   #
   # rename_group
   if rename_group != None :
      xrst.rename_group(tmp_dir, rename_group[0], rename_group[1])
      #
      # tmp_dir
      # reset tmp_dir because rmtree is such a dangerous command
      tmp_dir = f'{rst_directory}/tmp'
      shutil.rmtree(tmp_dir)
      print('xrst --rename_group: OK')
      return
   #
   # replace_spell_commands
   if replace_spell_commands :
      xrst.replace_spell(tmp_dir)
      #
      # tmp_dir
      # reset tmp_dir because rmtree is such a dangerous command
      tmp_dir = f'{rst_directory}/tmp'
      shutil.rmtree(tmp_dir)
      print('xrst --replace_spell_commands: OK')
      return
   #
   # auto_file
   xrst.auto_file(
      conf_dict, html_theme, target, all_page_info, root_page_list
   )
   #
   # -------------------------------------------------------------------------
   #
   # rst_directory/*.rst
   tmp_list = os.listdir(tmp_dir)
   rst_list = os.listdir(rst_directory)
   for name in tmp_list :
      src = f'{tmp_dir}/{name}'
      des = f'{rst_directory}/{name}'
      if name.endswith('.rst') :
         if name not in rst_list :
               shutil.copyfile(src, des)
         else :
            if not filecmp.cmp(src, des, shallow=False) :
               os.replace(src, des)
   for name in rst_list :
      if name.endswith('.rst') :
         if name not in tmp_list :
            os.remove( f'{rst_directory}/{name}' )
   #
   # tmp_dir
   # reset tmp_dir because rmtree is such a dangerous command
   tmp_dir = f'{rst_directory}/tmp'
   shutil.rmtree(tmp_dir)
   # -------------------------------------------------------------------------
   if rst_only :
      print('xrst rst_only: OK')
      indent = '\n' + 3 * ' '
      if target == 'html' :
         txt  = f'The following commands will build the html:'
         txt += indent
         txt += f'sphinx-build -b html {rst_directory} {target_directory}'
         txt += indent
         txt += f'rm -r {target_directory}/_sources'
         txt += indent
         txt += f'mv {rst_directory}/_sources {target_directory}/_sources'
         if html_theme == 'sphinx_rtd_theme' :
            txt += '\nThis will not modify the sphinx_rtd_theme maximum width'
      else :
         assert target == 'tex'
         latex_dir = f'{target_directory}'
         txt  = f'The following command will build the tex:'
         txt += indent
         txt += f'sphinx-build -b latex {rst_directory} {latex_dir}'
         txt += '\n'
         txt += f'The following command will build the pdf from the tex:'
         txt += indent
         txt += f'make -C {project_directory}/{latex_dir} {project_name}.pdf'
      print(txt)
      return
   #
   # -------------------------------------------------------------------------
   if target == 'html' :
      command = f'sphinx-build -b html {rst_directory} {target_directory}'
      if rst_line_numbers :
         system_command(command, any_warning)
      else :
         system_command(
            command, any_warning, page_name2line_pair, page_name2file_in
         )
         #
         # target_directory/_sources
         # replace sphinx _sources directory with proper xrst sources
         if not rst_line_numbers :
            src_dir = f'{rst_directory}/_sources'
            des_dir = f'{target_directory}/_sources'
            print( f'rm -r {des_dir}' )
            shutil.rmtree(des_dir)
            print( f'cp -r {src_dir} {des_dir}' )
            shutil.copytree(src_dir, des_dir)
         #
         # target_directory/index.html
         src_file = f'{target_directory}/{index_page_name}.html'
         des_file = f'{target_directory}/index.html'
         shutil.copyfile(src_file, des_file)

   else :
      assert target == 'tex'
      #
      latex_dir = f'{target_directory}'
      command = f'sphinx-build -b latex {rst_directory} {latex_dir}'
      if rst_line_numbers :
         system_command(command, any_warning)
      else :
         system_command(
            command, any_warning, page_name2line_pair, page_name2file_in
         )
      #
      # latex_dir/project_name.tex
      fix_latex(latex_dir, project_name)
      #
      print('The following command will build the pdf from the latex:')
      print( f'   make -C {project_directory}/{latex_dir} {project_name}.pdf' )
   # -------------------------------------------------------------------------
   # target_directory/_static/css/theme.css
   # see https://stackoverflow.com/questions/23211695/
   #  modifying-content-width-of-the-sphinx-theme-read-the-docs
   if html_theme == 'sphinx_rtd_theme' and target == 'html' :
      pattern = dict()
      pattern['content'] = re.compile(
         r'([.]wy-nav-content[{][^}]*;max-width):[^;]*;'
      )
      pattern['sidebar'] = re.compile(
         r'([.]wy-nav-side[{][^}]*;width):[^;]*;'
      )
      pattern['search'] = re.compile(
         r'([.]wy-side-nav-search[{][^}]*;width):[^;]*;'
      )
      new_value = { 'content':'100%', 'sidebar':'250px', 'search':'250px' }
      file_name = f'{target_directory}/_static/css/theme.css'
      if os.path.exists(file_name + '.bak' ) :
        shutil.copyfile(file_name + '.bak', file_name)
      else :
        shutil.copyfile(file_name, file_name + '.bak')
      try :
         file_obj  = open(file_name, 'r')
         ok        = True
      except :
         ok        = False
      if ok :
         data_in   = file_obj.read()
         file_obj.close()
         match     = dict()
         for key in pattern :
            match[key] = pattern[key].search(data_in)
            ok         = match[key] != None
      if ok :
         for key in pattern :
            match[key] = pattern[key].search(data_in, match[key].end())
            ok        = match[key] == None
      if ok :
         data_out = data_in
         for key in pattern :
            data_tmp  = data_out
            value     = new_value[key]
            data_out  = pattern[key].sub( f'\\1:{value};', data_tmp)
            ok        = data_out != data_tmp
      if not ok :
         msg       = 'warning: cannot modify widths in sphinx_rtd_theme\n'
         sys.stderr.write(msg)
         any_warning[0] = True
      else :
         file_obj  = open(file_name, 'w')
         file_obj.write(data_out)
         file_obj.close()
   # -------------------------------------------------------------------------
   if any_warning[0] :
      system_exit('xrst: See warnings above')
   else :
      print('xrst: OK')
