# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Bradley M. Bell <bradbell@seanet.com>
# SPDX-FileContributor: 2020-23 Bradley M. Bell
# ----------------------------------------------------------------------------
import re
import xrst
# {xrst_begin check_page_name dev}
# {xrst_spell
#     genindex
#     underbar
# }
# {xrst_comment_ch #}
#
# Check the rules for a page name
# ###############################
#
# page_name
# *********
# The page_name appears in *m_obj* in one of the following ways
#
# #.  \{xrst_begin_parent page_name user}
# #.  \{xrst_begin page_name user}
# #.  \{xrst_end page_name}
#
# A valid page name must satisfy the following conditions:
#
# #.  The valid characters in a page name are [A-Z], [a-z], [0-9],
#     dash, period and underbar.
# #.  A page name cannot begin with ``xrst_`` .
# #.  A page name cannot be ``index`` or ``genindex`` .
#
# If *page_name* does not follow
# these rules, a message is printed and the program exits.
#
# file_name
# *********
# is the name of the original input file that data appears in
# (used for error reporting).
#
# m_obj
# *****
# is the match object corresponding to *page_name*
#
# data
# ****
# is that data that was searched to get the match object.
#
# {xrst_code py}
def check_page_name(page_name, file_name, m_obj, data) :
   assert type(page_name) == str
   assert type(file_name) == str
   assert m_obj
   assert type(data) == str
   # {xrst_code}
   # {xrst_end check_page_name}
   #
   m_page_name = re.search('[-._A-Za-z0-9]+', page_name)
   if m_page_name.group(0) != page_name :
      msg  = f'begin command: page_name = "{page_name}"'
      msg += '\nIt must be non-empty and only contain the following'
      msg += ' characters: -, ., _, A-Z, a-z, 0-9'
      xrst.system_exit(msg,
         file_name=file_name, m_obj=m_obj, data=data
      )
   if page_name.startswith('xrst_') :
      msg = 'page_name cannot start with xrst_'
      xrst.system_exit(msg,
         file_name=file_name, m_obj=m_obj, data=data
      )
   if page_name == 'index' or page_name == 'genindex' :
      msg = 'page_name cannot be index or genindex'
      xrst.system_exit(msg,
         file_name=file_name, m_obj=m_obj, data=data
      )
