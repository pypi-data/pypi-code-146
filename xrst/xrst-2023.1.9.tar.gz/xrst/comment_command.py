# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Bradley M. Bell <bradbell@seanet.com>
# SPDX-FileContributor: 2020-23 Bradley M. Bell
# ----------------------------------------------------------------------------
"""
{xrst_begin comment_cmd user}

Comment Command
###############

Syntax
******
``\{xrst_comment`` *text* ``}``

Purpose
*******
This command adds *text* to the xrst input file that
does not appear in the rst output file.

Example
*******
:ref:`comment_example-name`

{xrst_end comment_cmd}
"""
# ----------------------------------------------------------------------------
import re
import xrst
#
# pattern
pattern = re.compile(
   r'([^\n]*[^\\]){xrst_comment[^a-z_][^}]*}([^\n]*\n)'
)
# {xrst_begin comment_cmd_dev dev}
# {xrst_comment_ch #}
#
# Remove all comment commands
# ###########################
#
# Arguments
# *********
#
# data_in
# =======
# is the data for this page.
#
# Returns
# *******
#
# data_out
# ========
# The return data_out is a copy of data_in except that the comment
# commands have been removed.
#
# {xrst_code py}
def comment_command(data_in) :
   assert type(data_in) == str
   # {xrst_code}
   # {xrst_literal
   #  BEGIN_return
   #  END_return
   # }
   # {xrst_end comment_cmd_dev}
   #
   # data_out
   data_out = data_in
   #
   # m_obj
   m_obj = pattern.search(data_out)
   while m_obj :
      # data_before, data_after
      data_before = data_out[: m_obj.start()]
      data_after  = data_out[m_obj.end() :]
      #
      # text_before, text_after
      text_before = m_obj.group(1).rstrip(' \t')
      text_after  = m_obj.group(2).lstrip(' \t')
      #
      # data_before, text_before
      if text_before.endswith('\n') :
         data_before += text_before
         text_before  = ''
      #
      # data_after, text_after
      if text_before == '' and text_after.startswith('{xrst_line ') :
         text_after = ''
      #
      # data_out
      if text_before != '' and text_after != '' :
         other_text = text_before + ' ' + text_after
      else :
         other_text = text_before + text_after
      data_out   = data_before + other_text +  data_after
      #
      # m_obj
      m_obj = pattern.search(data_out, m_obj.start())
   #
   # check_syntax_error
   # Cannot check for a syntax error in this command unless
   # the comment_ch commands have already been processed.
   #
   # BEGIN_return
   assert type(data_out) == str
   return data_out
   # END_return
