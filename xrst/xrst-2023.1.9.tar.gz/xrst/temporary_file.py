# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Bradley M. Bell <bradbell@seanet.com>
# SPDX-FileContributor: 2020-22 Bradley M. Bell
# ----------------------------------------------------------------------------
import re
import xrst
pattern_line_number     = re.compile( r'\n[ \t]*{xrst_line [0-9]+@' )
pattern_newline_3       = re.compile( r'(\n[ \t]*){2,}\n' )
pattern_ref_page_name_1 = re.compile( r':ref:`([._A-Za-z0-9]+)-name`' )
pattern_ref_page_name_2 = re.compile( r':ref:`([^`<]*)<([._A-Za-z0-9]+)-name>`' )
# ----------------------------------------------------------------------------
# {xrst_begin temporary_file dev}
# {xrst_spell
#     bool
#     dir
#     tmp
# }
# {xrst_comment_ch #}
#
# Write the temporary RST file for a page
# #######################################
#
# page_source
# ***********
# If *page_source* is true and *target* is html,
# a link to the xrst source code is included at the
# top of each page.
# If *page_source* is true and *target* is tex,
# the location of the xrst source code is reported at the
# top of each page.
#
# target
# ******
# If the :ref:`run_xrst@target` command line argument.
#
# pseudo_heading
# **************
# is the :ref:`process_headings@Returns@pseudo_heading` for this page.
#
# file_in
# *******
# is the name of the xrst input file for this page.
#
# tmp_dir
# *******
# is the directory where the output file will be saved.
#
# page_name
# *********
# is the name of this page.
#
# file_out
# ********
# The temporary file written by the routine, *file_out* , is
# tmp_dir/page_name.rst.

# data_in
# *******
# is the data for this page with all the xrst commands converted to
# their sphinx RST values, except the \\n{xrst_before_title} command.
# The following is added to this data before writing it to the output file:
#
#  #. The preamble is included at the beginning.
#  #. If *target* is ``html``
#
#     #. The *page_name* ``-name`` label is added next.
#     #. The pseudo heading is added next.
#     #. The name of the input file *file_in* is added next.
#
#  #. If *target* is ``tex```
#
#     #. All cross references of the form
#        :ref:\` *page_name* -name \` ,
#        are changed to :ref:\` *page_name* < *page_name* -title >\` .
#        Note that the page name will be added to the title when
#        :ref:`add_before_title-name` is called during
#        :ref:`table_of_contents-name` .
#
#  #. Any sequence of more than 2 lines
#     with only tabs or space are converted to 2 empty lines.
#  #. Empty lines at the end are removed
#  #. The xrst_line_number entries are removed.
#  #. The text ``\\{xrst_`` is replaced by ``\{xrst_`` .
#
# line_pair
# *********
# This is the value returned by ``temporary_file`` .
# For each *index*, *line_pair* [ *index* ] is the a pair of line numbers.
#
# -   The first number in a pair is a line number in *file_out*
#     These line numbers to not count `{xrst_before_title}` lines
#     because they are removed before the final rst output is created.
#
# -   The second number in a pair is the corresponding line number in *file_in*
#
# -   The first (second) line number is increasing (no-decreasing)
#     with respect to *index* .
#
# {xrst_code py}
# line_pair =
def temporary_file(
   page_source,
   target,
   pseudo_heading,
   file_in,
   tmp_dir,
   page_name,
   data_in,
) :
   assert target == 'html' or target == 'tex'
   assert type(page_source) == bool
   assert type(pseudo_heading) == str
   assert type(file_in) == str
   assert type(page_name) == str
   assert type(data_in) == str
   # {xrst_code}
   #
   # {xrst_literal
   #  BEGIN_RETURN
   #  END_RETURN
   # }
   # {xrst_end temporary_file}
   #
   # punctuation
   # Headings uses repeated copies of one of these characters
   punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
   #
   # label
   # label that displays page name (which is text in pseudo heading)
   label = f'.. _{page_name}-name:\n\n'
   #
   # data_out
   if target == 'html' :
      before   = label
      before  += pseudo_heading
      if page_source :
         if page_name.endswith('.rst') :
            destination = f'_sources/{page_name}.txt'
         else :
            destination = f'_sources/{page_name}.rst.txt'
         raw_html  = '.. raw:: html\n\n' + 3 * ' '
         raw_html += f'<a href="{destination}">View page source</a>\n\n'
         before   += raw_html
      data_out  = before + data_in
   else :
      if page_source :
         new_text   = f'xrst input file: {file_in}\n'
         #
         index      = data_in.find('\n{xrst_before_title}')
         first_line = index + len('\n{xrst_before_title}')
         assert data_in[first_line] == '\n'
         second_line = data_in.find('\n', first_line + 1)
         third_line  = data_in.find('\n', second_line + 1)
         fourth_line = data_in.find('\n', third_line + 1)
         #
         line     = data_in[first_line + 1 : second_line]
         overline = line[0] * len(line) == line and line[0] in punctuation
         if overline :
            text_index = fourth_line + 1
         else :
            text_index = third_line + 1
         data_before = data_in[: text_index]
         data_after  = data_in[text_index :]
         data_out    = data_before + new_text + data_after
      #
      data_out   = pattern_ref_page_name_1.sub(
         r':ref:`\1<\1-title>`' , data_out
      )
      data_out   = pattern_ref_page_name_2.sub(
         r':ref:`\1<\2-title>`' , data_out
      )
   #
   # data_out
   #
   # data_out
   # Convert three or more sequential emtpty lines to two empty lines.
   data_out = pattern_line_number.sub('\n', data_out)
   data_out = pattern_newline_3.sub('\n\n', data_out)
   #
   # data_out
   # remove empty lines at the end
   while data_out[-2 :] == '\n\n' :
      data_out = data_out[: -1]
   #
   # data_out
   # The last step removing line numbers. This is done last for two reasons:
   # 1. So mapping from output to input line number is correct.
   # 2. We are no longer able to give line numbers for errors after this.
   data_out, line_pair = xrst.remove_line_numbers(data_out)
   #
   # data_out
   data_out = data_out.replace( r'\{xrst_', '{xrst_' )
   #
   # file_out
   if page_name.endswith('.rst') :
      file_out = tmp_dir + '/' + page_name
   else :
      file_out = tmp_dir + '/' + page_name + '.rst'
   file_obj = open(file_out, 'w')
   file_obj.write(data_out)
   file_obj.close()
   #
   # BEGIN_RETURN
   assert type(line_pair) == list
   assert type( line_pair[0] ) == tuple
   assert len( line_pair[0] ) == 2
   assert type( line_pair[0][0] ) == int
   assert type( line_pair[0][1] ) == int
   return line_pair
   # END_RETURN
