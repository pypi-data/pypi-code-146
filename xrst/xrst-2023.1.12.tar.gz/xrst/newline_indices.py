# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Bradley M. Bell <bradbell@seanet.com>
# SPDX-FileContributor: 2020-23 Bradley M. Bell
# ----------------------------------------------------------------------------
import re
# {xrst_begin newline_indices dev}
# {xrst_comment_ch #}
#
# Find index of all the newlines in a string
# ##########################################
#
# Arguments
# *********
#
# data
# ====
# The string we are searching for newlines.
#
# Results
# *******
#
# newline_list
# ============
# The return newline_list is the list of indices in data that
# represent all of the newlines; i.e. '\n'.
#
# {xrst_code py}
def newline_indices(data) :
   assert type(data) == str
   # {xrst_code}
   # {xrst_literal
   #  BEGIN_return
   #  END_return
   # }
   # {xrst_end newline_indices}

   pattern_newline  = re.compile( r'\n')
   newline_itr      = pattern_newline.finditer(data)
   newline_list     = list()
   for m_obj in newline_itr :
      next_index = m_obj.start()
      newline_list.append( next_index )
   # BEGIN_return
   assert type(newline_list) == list
   if 0 < len( newline_list) :
      assert type(newline_list[0]) == int
   return newline_list
   # END_return
