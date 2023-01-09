# -----------------------------------------------------------------------------
#                      xrst: Extract Sphinx RST Files
#          Copyright (C) 2020-22 Bradley M. Bell (bradbell@seanet.com)
#              This program is distributed under the terms of the
#              GNU General Public License version 3.0 or later see
#                    https://www.gnu.org/licenses/gpl-3.0.txt
# ----------------------------------------------------------------------------
import re
# {xrst_begin xrst.pattern dev}
# {xrst_spell
#     arg
#     dir
#     lin
#     toc
# }
# {xrst_comment_ch #}
#
# The xrst.pattern Dictionary
# ###########################
#
# pattern
# *******
# This dictionary contains compiled regular expressions.
# It does not change after its initial setting when this file is imported.
# {xrst_code py}
pattern = dict()
# {xrst_code}
#
# begin
# *****
# Pattern for the begin command.
#
# 0. preceding character or empty + the command.
# 1. preceding character or empty
# 2. begin or begin_parent
# 3. the page name (without leading or trailing spaces or tabs)
# 4. the group name (with leading and trailing spaces and tabs)
#
# {xrst_code py}
pattern['begin'] = re.compile(
   r'(^|[^\\])\{xrst_(begin|begin_parent)[ \t]+([^ \t}]*)([^}]*)}'
)
# {xrst_code}
#
# toc
# ***
# Patterns for the toc_hidden, toc_list, and toc_table commands.
#
# 0. preceding character + the command.
# 1. command name; i.e., hidden, list, or table
# 2. the rest of the command that comes after the command name.
#    This is a list of file names with one name per line.
#    The } at the end of the command is not included.
#    This pattern may be empty.
#
# If you change this pattern, check pattern_toc in process_children.py
# {xrst_code py}
pattern['toc']   = re.compile(
   r'[^\\]\{xrst_toc_(hidden|list|table)([^}]*)}'
)
# {xrst_code}
#
# code
# ****
# Pattern for code command.
#
# 0. the entire line for the command with newline at front.
# 1. the indent for the command (spaces and tabs)
# 2. is the command with or without characters in front
# 3. This is the non space characters after the indent and before
#    command (or None)
# 4. the language argument which is empty (just white space)
#    for the second code command in each pair.
# 5. the line number for this line; see pattern['line'] above.
#
# {xrst_code py}
pattern['code'] = re.compile(
   r'\n([ \t]*)(\{xrst_code *|([^\n]*[^\n\\])\{xrst_code *)' +
   r'([^}]*)}[^\n]*\{xrst_line ([0-9]+)@'
)
# {xrst_code}
#
# comment_ch
# **********
# Pattern for comment_ch command
#
# 1. empty or character before command + the command
# 2. is the character (matched as any number of not space, tab or }
#
# {xrst_code py}
pattern['comment_ch'] = re.compile(
   r'(^|[^\\])\{xrst_comment_ch\s+([^} \t]*)\s*}'
)
# {xrst_code}
#
# dir
# ***
# Pattern for dir command
#
# 1. Is either empty of character before command
# 2. Is the file_name in the command
#
# {xrst_code py}
# pattern_dir
pattern['dir'] = re.compile(
   r'(^|[^\\]){xrst_dir[ \t]+([^}]*)}'
)
# {xrst_code}
#
# end
# ***
# Pattern for end command
#
# 0. preceding character + white space + the command.
# 1. the page name.
#
# {xrst_code py}
pattern['end'] = re.compile( r'[^\\]\{xrst_end\s+([^}]*)}' )
# {xrst_code}
#
#
# line
# ****
# Pattern for line numbers are added to the input by add_line_number
#
# 0. the line command.
# 1. the line_number.
#
# {xrst_code py}
pattern['line'] = re.compile( r'\{xrst_line ([0-9]+)@' )
# {xrst_code}
#
# arg, lin
# ********
#
# literal_0
# *********
# xrst_literal with no arguments
#
# 0. preceding newline + white space + the command.
# 1. line number where } at end of command appears
#
# {xrst_code py}
lin = r'[ \t]*\{xrst_line ([0-9]+)@\n'
pattern['literal_0'] = re.compile(
   r'[^\\]\{xrst_literal}' + lin
)
# {xrst_code}
#
# literal_1
# *********
# xrst_literal with display_file
#
# 0. preceding newline + white space + the command.
# 1. the line number where this command starts
# 2. the display file
# 3. line number where display file appears
# 4. line number where } at end of command appears
#
# {xrst_code py}
arg = r'([^{]*)\{xrst_line ([0-9]+)@\n'
pattern['literal_1']  = re.compile(
   r'[^\\]\{xrst_literal' + lin + arg + r'[ \t]*}' + lin
)
# {xrst_code}
#
# literal_2
# *********
# xrst_literal with start, stop
#
# 0. preceding newline + white space + the command.
# 1. the line number where this command starts
# 2. the start text + surrounding white space
# 3. line number where start text appears
# 4. the stop text + surrounding white space
# 5. the line number where stop text appears
# 6. line number where } at end of command appears
#
# {xrst_code py}
pattern['literal_2']  = re.compile(
   r'[^\\]\{xrst_literal' + lin + arg + arg + r'[ \t]*}' + lin
)
# {xrst_code}
#
# literal_3
# *********
# xrst_literal with start, stop, display_file
#
# 0. preceding character + the command.
# 1. the line number where this command starts
# 2. the display file
# 3. line number where display file appears
# 4. the start text + surrounding white space
# 5. line number where start text appears
# 6. the stop text + surrounding white space
# 7. the line number where stop text appears
# 8. line number where } at end of command appears
#
# {xrst_code py}
pattern['literal_3']  = re.compile(
   r'[^\\]\{xrst_literal' + lin + arg + arg + arg + r'[ \t]*}' + lin
)
# {xrst_code}
# {xrst_end xrst.pattern}
