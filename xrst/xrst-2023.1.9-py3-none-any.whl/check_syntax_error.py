# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Bradley M. Bell <bradbell@seanet.com>
# SPDX-FileContributor: 2020-22 Bradley M. Bell
# ----------------------------------------------------------------------------
import re
import xrst
# {xrst_begin check_syntax_error dev}
# {xrst_comment_ch #}
#
#
# Check that an xrst command has been removed
# ###########################################
#
# command_name
# ************
# is the name of the xrst command; i.e., the following pattern
# constitute a match for this command
#
# - ``[^\\]\{xrst_`` *command_name* ``[^z-a]``
#
# data
# ****
# is the data for this page.
#
# file_name
# *********
# is the input that this page appears in (used for error reporting).
#
# page_name
# *********
# is ``None`` or the name of this page (used for error reporting).
#
# {xrst_code py}
def check_syntax_error(command_name, data, file_name, page_name) :
   assert type(command_name) == str
   assert type(data) == str
   assert type(file_name) == str
   assert type(page_name) == str or page_name == None
   # {xrst_code}
   # {xrst_end check_syntax_error}
   #
   pattern = r'[^\\]{xrst_' + command_name + r'[^a-z]'
   m_error = re.search(pattern, data)
   if m_error :
      msg = f'syntax error in xrst {command_name} command'
      xrst.system_exit(msg,
         file_name    = file_name ,
         page_name    = page_name ,
         m_obj        = m_error ,
         data         = data ,
      )
   #
   return
