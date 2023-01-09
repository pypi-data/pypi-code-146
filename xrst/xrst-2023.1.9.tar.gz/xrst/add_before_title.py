# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Bradley M. Bell <bradbell@seanet.com>
# SPDX-FileContributor: 2020-23 Bradley M. Bell
# ----------------------------------------------------------------------------
import re
import xrst
#
# {xrst_begin add_before_title dev}
# {xrst_spell
#     overline
# }
# {xrst_comment_ch #}
#
# If PDF, Add Page Number and Name to Title
# #########################################
#
# Arguments
# *********
#
# data_in
# =======
# data for this page before replacement.
#
#  #. data_in must contain '\\n{xrst_before_title}'
#     which is referred to as the command below.
#  #. The page title must come directly after the command
#     and start with a newline.
#  #. The page title may have an rst overline directly before the
#     heading text and must have an underline directly after it.
#  #. If both an overline and underline follow, they must be equal.
#
# target
# ======
# if *target* is ``html`` , the command is removed and no other action
# is taken. Otherwise, the *page_number* following by the *page_name* is
# added at the font of the title for this page.
# The underline (and overline if present) are extended by the number of
# characters added to the title.
#
# page_number
# ===========
# This is a page number that identifies this page in the table of contents.
#
# page_name
# =========
# This is the name of the page.
#
# Returns
# *******
#
# data_out
# ========
# the return data_out is the data after replacement.
#
# {xrst_code py}
def add_before_title(data_in, target, page_number, page_name) :
   assert type(data_in) == str
   assert target == 'html' or target == 'tex'
   assert type(page_number) == str
   assert type(page_name) == str
   # {xrst_code}
   # {xrst_literal
   #  BEGIN_return
   #  END_return
   # }
   # {xrst_end add_before_title}
   #
   # pattern
   pattern   = '\n{xrst_before_title}'
   #
   # punctuation
   # Headings uses repeated copies of one of these characters
   punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
   #
   # start_cmd
   start_cmd = data_in.find(pattern)
   assert 0 <= start_cmd
   index = data_in.find(pattern, start_cmd + len(pattern))
   if 0 <= index :
      msg = '{xrst_before_title} cannot appear at beginning of a line'
      xrst.system_exit(msg, page_name = page_name)
   #
   # data_out
   if target == 'html' :
      return data_in.replace(pattern,'')
   #
   # add_text
   if page_number == '' :
      add_text = f'{page_name}:'
   else :
      add_text = f'{page_number} {page_name}:'
   #
   # first_newline
   first_newline = start_cmd + len(pattern)
   assert data_in[first_newline] == '\n'
   #
   # second_newline
   second_newline = data_in.index('\n', first_newline + 1)
   #
   # third_newline
   third_newline  = data_in.index('\n', second_newline + 1)
   #
   # first_line, second_line
   first_line   = data_in[first_newline + 1 : second_newline ]
   second_line  = data_in[second_newline + 1 : third_newline ]
   #
   # overline
   # check for an overline directly after the command
   overline = False
   if first_line[0] * len(first_line) == first_line :
      if first_line[0] in punctuation :
         overline = True
   #
   if not overline :
      # If no overline the page title follows the command and then
      # an underline after the title.
      assert second_line[0] in punctuation
      #
      # new version of first and second lines
      first_line   = add_text + ' ' + first_line
      second_line += second_line[0] * ( len(add_text) + 1 )
      #
   else :
      # fourth_newline
      fourth_newline = data_in.index('\n', third_newline + 1)
      #
      # third_line
      third_line   = data_in[third_newline + 1 : fourth_newline]
      assert first_line == third_line
      #
      # new version of first, second, and third lines
      first_line += first_line[0] * ( len(add_text) + 1 )
      second_line = add_text + ' ' + second_line
      third_line  = first_line
   #
   # data_out
   data_out  = data_in[: start_cmd] + '\n'
   data_out += first_line + '\n'
   data_out += second_line + '\n'
   if overline :
      data_out += third_line + '\n'
      data_out += data_in[fourth_newline :]
   else :
      data_out += data_in[third_newline :]
   # BEGIN_return
   assert type(data_out) == str
   #
   return data_out
   # END_return
