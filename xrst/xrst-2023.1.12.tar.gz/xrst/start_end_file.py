# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Bradley M. Bell <bradbell@seanet.com>
# SPDX-FileContributor: 2020-23 Bradley M. Bell
# ----------------------------------------------------------------------------
import xrst
# {xrst_begin start_end_file dev}
# {xrst_spell
#     cmd
# }
# {xrst_comment_ch #}
#
# Convert literal command start, end from text to line numbers
# ############################################################
#
# Arguments
# *********
#
# file_cmd
# ========
# is the name of the file where the xrst_literal command appears.
#
# page_name
# =========
# is the name of the page where the xrst_literal command appears.
#
# display_file
# ============
# is the name of the file that we are displaying. If it is not the same as
# file_cmd, then it must have appeared in the xrst_literal command.
#
# cmd_line
# ========
# If file_cmd is equal to display_file, the lines of the file
# between line numbers cmd_line[0] and cmd_line[1] inclusive
# are in the xrst_literal command and are excluded from the search.
#
# start_after
# ===========
# is the starting text. There must be one and only one copy of this text in the
# file (not counting the excluded text). This text has no newlines and cannot
# be empty.  If not, an the error is reported and the program stops.
#
# end_before
# ==========
# is the stopping text. There must be one and only one copy of this text in the
# file (not counting the excluded text). This text has no newlines and cannot
# be empty.  Furthermore, the stopping text must come after the end of the
# starting text. If not, an the error is reported and the program stops.
#
# Returns
# *******
#
# start_line
# ==========
# is the line number where start_after appears.
#
# end_line
# ========
# is the line number where end_before appears.
#
# {xrst_code py}
def start_end_file(
   file_cmd,
   page_name,
   display_file,
   cmd_line,
   start_after,
   end_before
) :
   assert type(file_cmd) == str
   assert type(page_name) == str
   assert type(display_file) == str
   assert type(cmd_line[0]) == int
   assert type(cmd_line[1]) == int
   assert cmd_line[0] <= cmd_line[1]
   assert type(start_after) == str
   assert type(end_before) == str
   # {xrst_code}
   # {xrst_literal
   #  BEGIN_return
   #  END_return
   # }
   # {xrst_end start_end_file}
   # ------------------------------------------------------------------------
   # exclude_line
   if file_cmd == display_file :
      exclude_line = cmd_line
   else :
      exclude_line = (0, 0)
   #
   # msg
   msg  = f'in literal command:'
   #
   if start_after == '' :
      msg += ' start_after is empty'
      xrst.system_exit(msg,
         file_name=file_cmd, page_name=page_name, line = cmd_line[0]
      )
   if end_before == '' :
      msg += ' end_before is empty'
      xrst.system_exit(msg,
         file_name=file_cmd, page_name=page_name, line = cmd_line[0]
      )
   if 0 <= start_after.find('\n') :
      msg += ' a newline appears in start_after'
      xrst.system_exit(msg,
         file_name=file_cmd, page_name=page_name, line = cmd_line[0]
      )
   if 0 <= end_before.find('\n') :
      msg += ' a newline appears in end_before'
      xrst.system_exit(msg,
         file_name=file_cmd, page_name=page_name, line = cmd_line[0]
      )
   #
   # data
   file_obj  = open(display_file, 'r')
   data      = file_obj.read()
   file_obj.close()
   #
   # start_line
   start_index = data.find(start_after)
   count = 0
   while 0 <= start_index :
      line = data[: start_index].count('\n') + 1
      if  line < exclude_line[0] or exclude_line[1] < line :
         start_line = line
         count      = count + 1
      start_index = data.find(start_after, start_index + len(start_after) )
   if count != 1 :
      msg += f'\nstart_after   = "{start_after}"'
      msg += f'\ndisplay_file  =  {display_file}'
      msg += f'\nfound {count} matches expected 1'
      if file_cmd == display_file :
         msg += ' not counting the literal command'
      xrst.system_exit(msg,
         file_name=file_cmd, page_name=page_name, line = cmd_line[0]
      )
   #
   # end_line
   stop_index = data.find(end_before)
   count = 0
   while 0 <= stop_index :
      line = data[: stop_index].count('\n') + 1
      if  line < exclude_line[0] or exclude_line[1] < line :
         end_line = line
         count     = count + 1
      stop_index = data.find(end_before, stop_index + len(end_before) )
   if count != 1 :
      msg += f'\nend_before   = "{end_before}"'
      msg += f'\ndisplay_file =  {display_file}'
      msg += f'\nfound {count} matches expected 1'
      if file_cmd == display_file :
         msg += ' not counting the literal command'
      xrst.system_exit(msg,
         file_name=file_cmd, page_name=page_name, line = cmd_line[0]
      )
   # ------------------------------------------------------------------------
   # BEGIN_return
   assert type(start_line) == int
   assert type(end_line) == int
   #
   return start_line, end_line
   # END_return
