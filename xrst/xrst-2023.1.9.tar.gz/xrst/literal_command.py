# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Bradley M. Bell <bradbell@seanet.com>
# SPDX-FileContributor: 2020-23 Bradley M. Bell
# ----------------------------------------------------------------------------
"""
{xrst_begin literal_cmd user}
{xrst_spell
   dir
   literalinclude
}

Literal Command
###############

Syntax
******

-  ``\{xrst_literal}``

-  | ``\{xrst_literal``
   |     *display_file*
   | ``}``

-  | ``\{xrst_literal``
   |     *start_after*
   |     *end_before*
   | ``}``

-  | ``\{xrst_literal``
   |     *display_file*
   |     *start_after*
   |     *end_before*
   | ``}``

Purpose
*******
A code block, from any where in any file,
can be included by the command above.

literalinclude
**************
This command is similar to the following sphinx directive
(see :ref:`dir_cmd-name`) :

| |tab| .. literalinclude:: \{xrst_dir *display_file*}
| |tab| |tab| :start-after: *start_after*
| |tab| |tab| :end-before: *end_before*

The xrst literal command has the following difference:

#. If the *display_file* is not specified, the current input file is used.
#. The copy of *start_after* and *end_before* in the command is not considered
   a match for the corresponding text. This makes it possible to put the
   command above the text when *display_file* is the current input file.
#. It is an error for there to be more than one copy of *start_after*
   or *end_before* in the *display_file* (not counting the copy in the
   command when the display file is the current input file).
   This makes sure that the intended section of *display_file* is displayed.

White Space
***********
Leading and trailing white space is not included in
*start_after*, *end_before* or *display_file*.
The new line character separates these tokens.
The line containing the ``}`` must have nothing but white space after it.

display_file
************
If *display_file* is not in the syntax,
the code block is in the current input file.
Otherwise, the code block is in *display_file*.
The file name *display_file* is relative to the
:ref:`config_file@directory@project_directory` .

1. This may seem verbose, but it makes it easier to write scripts
   that move files and automatically change references to them.
2. Note that if you use the sphinx ``literalinclude`` directive,
   the corresponding file name will be relative to the
   :ref:`config_file@directory@rst_directory` , which is a path relative
   to the project_directory.

No start or end
***************
In the case where there is no *start_after* or *end_before*,
the entire display file is displayed.
In the case of the ``\{xrst_literal}`` syntax,
the entire current input file is displayed.

start_after
***********
The code block starts with the line following the occurrence
of the text *start_after* in *display_file*.
If this is the same as the file containing the command,
the text *start_after* will not match any text in the command.
There must be one and only one occurrence of *start_after* in *display_file*,
not counting the command itself when the files are the same.

end_before
**********
The code block ends with the line before the occurrence
of the text *end_before* in *display_file*.
If this is the same as the file containing the command,
the text *end_before* will not match any text in the command.
There must be one and only one occurrence of *end_before* in *display_file*,
not counting the command itself when the files are the same.

Spell Checking
**************
Spell checking is **not** done for these code blocks.


Example
*******
see :ref:`literal_example-name` .

{xrst_end literal_cmd}
"""
# ----------------------------------------------------------------------------
import os
import re
import xrst
#
# ----------------------------------------------------------------------------
#
# extension_map
# map cases that pygments has trouble with
extension_map = {
   'xrst' : 'rst'    ,
   'hpp'  : 'cpp'    ,
   'm'    : 'matlab' ,
   'txt'  : ''       ,
}
def file_extension(display_file) :
   index = display_file.rfind('.')
   extension = ''
   if 0 <= index and index + 1 < len(display_file) :
      extension = display_file[index + 1 :]
      if extension in extension_map :
         extension = extension_map[extension]
   return extension
# ----------------------------------------------------------------------------
# {xrst_begin literal_cmd_dev dev}
# {xrst_spell
#     dir
# }
# {xrst_comment_ch #}
#
# Process the literal commands in a page
# ######################################
#
# Arguments
# *********
#
# data_in
# =======
# is the data for a page before the
# :ref:`literal commands <literal_cmd-name>` have been removed.
#
# file_name
# =========
# is the name of the file that this data comes from. This is used
# for error reporting and for the display file (when the display file
# is not included in the command).
#
# page_name
# =========
# is the name of the page that this data is in. This is only used
# for error reporting.
#
# rst2project_dir
# ===============
# is a relative path from the :ref:`config_file@directory@rst_directory`
# to the :ref:`config_file@directory@project_directory` .
#
# Returns
# *******
#
# data_out
# ========
# Each xrst literal command is converted to its corresponding sphinx commands.
#
# {xrst_code py}
def literal_command(data_in, file_name, page_name, rst2project_dir) :
   assert type(data_in) == str
   assert type(file_name) == str
   assert type(page_name) == str
   assert type(rst2project_dir) == str
   # {xrst_code}
   # {xrst_literal
   #  BEGIN_return
   #  END_return
   # }
   # {xrst_end literal_cmd_dev}
   #
   assert xrst.pattern['literal_0'].groups == 1
   assert xrst.pattern['literal_1'].groups == 4
   assert xrst.pattern['literal_2'].groups == 6
   assert xrst.pattern['literal_3'].groups == 8
   #
   # data_out
   data_out = data_in
   #
   # key
   for key in [ 'literal_0', 'literal_1' ] :
      #
      # m_file
      m_file  = xrst.pattern[key].search(data_out)
      while m_file != None :
         #
         # display_file
         if key == 'literal_0' :
            display_file = file_name
         else :
            display_file = m_file.group(2).strip()
            if not os.path.isfile(display_file) :
               msg  = 'literal command: can not find the display_file.\n'
               msg += f'display_file = {display_file}'
               xrst.system_exit(msg,
                  file_name    = file_name,
                  page_name = page_name,
                  m_obj        = m_file,
                  data         = data_out
               )
            if os.path.samefile(display_file, file_name) :
               display_file = file_name
         #
         # cmd
         display_path = os.path.join(rst2project_dir, display_file)
         cmd          = f'.. literalinclude:: {display_path}\n'
         extension = file_extension( display_file )
         if extension != '' :
            cmd += 3 * ' ' + f':language: {extension}\n'
         cmd = '\n' + cmd + '\n'
         if data_out[m_file.start() ] != '\n' :
            cmd = '\n' + cmd
         #
         # data_out
         data_tmp  = data_out[: m_file.start() + 1 ]
         data_tmp += cmd
         data_tmp += data_out[ m_file.end() : ]
         data_out  = data_tmp
         #
         # m_file
         m_file  = xrst.pattern[key].search(data_out)
         if m_file and key == 'literal_0' :
            msg  = 'More than one {xrst_literal} command in this page.\n'
            msg += 'This command includes the entire current input file.'
            xrst.system_exit(msg,
               file_name    = file_name,
               page_name = page_name,
               m_obj        = m_file,
               data         = data_out
            )
   #
   # key
   for key in [ 'literal_2', 'literal_3' ] :
      #
      # m_file
      m_file  = xrst.pattern[key].search(data_out)
      while m_file != None :
         #
         # display_file, start_after, end_before, display_file, cmd_line
         if key == 'literal_2' :
            display_file  = file_name
            start_after   = m_file.group(2).strip()
            end_before    = m_file.group(4) .strip()
            cmd_end_line = int( m_file.group(6) )
         else :
            display_file  = m_file.group(2).strip()
            start_after   = m_file.group(4).strip()
            end_before    = m_file.group(6) .strip()
            cmd_end_line = int( m_file.group(8) )
            if not os.path.isfile(display_file) :
               msg  = 'literal command: can not find the display_file.\n'
               msg += f'display_file = {display_file}'
               xrst.system_exit(msg,
                  file_name    = file_name,
                  page_name = page_name,
                  m_obj        = m_file,
                  data         = data_out
               )
            same_file   = os.path.samefile(display_file, file_name)
            if same_file :
               display_file = file_name
         cmd_start_line = int( m_file.group(1) )
         cmd_line       = (cmd_start_line, cmd_end_line)
         #
         # start_line, end_line
         start_line, end_line = xrst.start_end_file(
            file_cmd     = file_name,
            page_name = page_name,
            display_file = display_file,
            cmd_line     = cmd_line,
            start_after  = start_after,
            end_before   = end_before
         )
         #
         # locations in display_file
         start_line  = start_line + 1
         end_line    = end_line  - 1
         #
         # cmd
         display_path = os.path.join(rst2project_dir, display_file)
         cmd          = f'.. literalinclude:: {display_path}\n'
         cmd         += 3 * ' ' + f':lines: {start_line}-{end_line}\n'
         #
         # cmd
         # Add language to literalinclude, sphinx seems to be brain
         # dead and does not do this automatically.
         extension = file_extension( display_file )
         if extension != '' :
            cmd += 3 * ' ' + f':language: {extension}\n'
         cmd = '\n' + cmd + '\n\n'
         if m_file.start() > 0 :
            if data_out[m_file.start() - 1] != '\n' :
               cmd = '\n' + cmd
         #
         # data_out
         data_tmp  = data_out[: m_file.start() + 1 ]
         data_tmp += cmd
         data_tmp += data_out[ m_file.end() : ]
         data_out  = data_tmp
         #
         # m_file
         m_file  = xrst.pattern[key].search(data_out)
         #
   #
   xrst.check_syntax_error(
      command_name    = 'literal',
      data            = data_out,
      file_name       = file_name,
      page_name    = page_name,
   )
   # BEGIN_return
   assert type(data_out) == str
   #
   return data_out
   # END_return
