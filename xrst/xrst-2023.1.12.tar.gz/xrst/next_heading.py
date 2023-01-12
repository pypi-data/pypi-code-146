# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Bradley M. Bell <bradbell@seanet.com>
# SPDX-FileContributor: 2020-23 Bradley M. Bell
# ----------------------------------------------------------------------------
import xrst
# {xrst_begin next_heading dev}
# {xrst_spell
#     overline
# }
# {xrst_comment_ch #}
#
# Return location of the next heading in a page
# #############################################
#
# Arguments
# *********
#
# data
# ====
# is the data that we are searching for a heading in. The heading text must
# have at least one character and be followed by an underline of at least the
# same length. The heading text may be proceeded by an overline.
#
# data_index
# ==========
# is the index in the data where the search starts. This must be zero
# or directly after a newline.
#
# file_name
# =========
# name of the file that contains the input data for this page.
# This is only used for error reporting.
#
# page_name
# =========
# is the name of this page.
# This is only used for error reporting.
#
# Results
# *******
#
# heading_index
# =============
# If there is an overline, this is the index in data of the beginning of the
# overline. Otherwise, it is the index of the beginning of the heading text.
# If 0 < heading_index, there is a newline just before heading_index; i.e.,
# data[heading_index]=='\n'.  If heading_index is -1, there is no heading
# in data that begins at or after data_index.
#
# heading_text
# ============
# if 0 <= heading_index, this is the heading text.
#
# underline_text
# ==============
# if 0 <= heading_index, this is the underline text.
# If there is an overline present, it is the same as the underline text.
#
# {xrst_code py}
def next_heading(data, data_index, file_name, page_name) :
   assert type(data) == str
   assert type(data_index) == int
   if data_index != 0 :
      assert data[data_index-1] == '\n'
   assert type(file_name) == str
   assert type(page_name) == str
   # {xrst_code}
   # {xrst_literal
   #  BEGIN_return
   #  END_return
   # }
   # {xrst_end next_heading}
   #
   # punctuation
   punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
   assert len(punctuation) == 34 - 2 # two escape sequences
   #
   # next_start, next_newline
   next_start       = data_index
   next_newline     = data.find('\n', next_start)
   #
   # state
   state  = 'before_overline'
   #
   while 0 <= next_newline :
      #
      # next_line
      next_line = data[next_start : next_newline]
      next_line = xrst.pattern['line'].sub('', next_line)
      next_line = next_line.rstrip(' \t')
      #
      # next_len
      next_len  = len(next_line)
      #
      if next_len < 1 :
         # next_line cannot be an overline, heading, or underline
         state = 'before_overline'
      #
      elif state == 'before_overline' :
         #
         # heading_index
         heading_index = next_start
         #
         ch = next_line[0]
         if ch in punctuation and next_line == ch * next_len :
            # next_line can be an overline but not an underline
            state         = 'before_heading'
            overline_text = next_line
         else :
            # next_line can be a heading, but not overline or underline
            state         = 'before_underline'
            overline_text = None
            heading_text  = next_line
      #
      elif state == 'before_heading' :
         # next_line can be a heading
         state = 'before_underline'
         heading_text    = next_line
      #
      elif state == 'before_underline' :
         underline_ch = next_line[0]
         if underline_ch not in punctuation :
            state = 'before_overline'
         elif next_line != underline_ch * next_len :
            state = 'before_overline'
         elif len(next_line) < len(heading_text) :
            state = 'before_overline'
         else :
            m_line = xrst.pattern['line'].search(data[next_start :])
            line   = m_line.group(1)
            msg = ''
            if len(heading_text) < len(next_line) :
               msg = 'underline text is longer than line above it'
            elif overline_text is not None and overline_text != next_line:
               msg = 'overline text is non-empty and not equal underline text'
            if msg != '' :
               xrst.system_exit(
                     msg,
                     file_name = file_name,
                     page_name = page_name,
                     line      = line,
               )
            #
            # underline_text
            underline_text = next_line
            #
            return heading_index, heading_text, underline_text
      #
      # next_start, next_newline
      next_start   = next_newline + 1
      next_newline = data.find('\n', next_start)
   #
   # heading_index, heading_text, underline_text
   heading_index = -1
   heading_text  = ''
   underline_text  = ''
   #
   # BEGIN_return
   assert type(heading_index) == int
   assert type(heading_text) == str
   assert type(underline_text) == str
   #
   return heading_index, heading_text, underline_text
   # END_return
