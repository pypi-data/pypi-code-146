# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Bradley M. Bell <bradbell@seanet.com>
# SPDX-FileContributor: 2020-23 Bradley M. Bell
# ----------------------------------------------------------------------------
import xrst
# ----------------------------------------------------------------------------
# page_index =
def page_name2index(all_page_info, page_name) :
   for (page_index, info) in enumerate(all_page_info) :
      if info['page_name'] == page_name :
         return page_index
   return None

# ----------------------------------------------------------------------------
# Create the table of contents and replace the '{xrst_before_title}'
# for this page and all its child pages.
#
# tmp_dir
# is the temporary directory where the rst files are written.
#
# target:
# is either 'html' or 'tex'. If target is 'tex',  in the temporary files
# tmp_dir/page_name.rst, the text {xrst_before_title}
# is removed and  page number followed by page name is added to the
# title. The page number includes the counter for each level.
# If target is 'html', {xrst_before_title} is removed without other changes.
#
# count:
# is a list where each element is a non-negative int.
#
# count[-1] - 1 is the number of pages at the level of this page and
# before this page.
#
# count[-2] - 1 is the number of pages at the level of this pages parent and
# before this pages parent.
# ...
#
# If this count is the empty list, this page is the root of the table of
# contents tree.
#
# page_index:
# is the index of this page in all_page_info
#
# all_page_info:
# is a list with length equal to the number of pages.
# The value all_page_info[page_index] is a dictionary for this page
# with the following key, value pairs (all the keys are strings:
# key            value
# page_name   a str continaing the name of this page.
# page_title  a str containing the title for this page.
# parent_page an int index in page_info for the parent of this page.
# in_parent_file True if this page in same input file as its parent.
#
# content:
# The return content is the table of contents entries for this page
# and all the pages below this page.
#
# content =
def page_table_of_contents(
   tmp_dir, target, count, all_page_info, page_index
) :
   assert type(tmp_dir) == str
   assert type(target) == str
   assert type(count) == list
   assert type(all_page_info) == list
   assert type(page_index) == int
   #
   assert target in [ 'html', 'tex' ]
   #
   # page_name, page_title
   page_name   = all_page_info[page_index]['page_name']
   page_title  = all_page_info[page_index]['page_title']
   #
   # page_number, content
   page_number = ''
   if 0 == len(count) :
      content = ''
   else :
      content = '| '
   if 0 < len(count) :
      assert type( count[-1] ) == int
      for i in range( len(count) - 1 ) :
         content += 3 * ' '
      for (i, c) in enumerate(count) :
         page_number += str(c)
         if i + 1 < len(count) :
            page_number += '.'
   #
   # content
   if len(count) == 0 :
      content  += f':ref:`{page_name}-title`' '\n\n'
   else :
      content  += f':ref:`{page_number}<{page_name}-title>` '
      content  += page_title + '\n'
   #
   # file_name
   # temporary file corresponding to this page name
   if page_name.endswith('.rst') :
      file_name = tmp_dir + '/' + page_name
   else :
      file_name = tmp_dir + '/' + page_name + '.rst'
   #
   # page_data
   file_obj  = open(file_name, 'r')
   page_data = file_obj.read()
   file_obj.close()
   page_data = xrst.add_before_title(
      page_data, target, page_number, page_name
   )
   #
   # file_name
   file_obj  = open(file_name, 'w')
   file_obj.write(page_data)
   file_obj.close()
   #
   # in_parent_file_list, in_toc_cmd_list
   in_parent_file_list = list()
   in_toc_cmd_list   = list()
   for child_index in range( len( all_page_info ) ) :
      if all_page_info[child_index]['parent_page'] == page_index :
         if all_page_info[child_index]['in_parent_file'] :
            in_parent_file_list.append(child_index)
         else :
            in_toc_cmd_list.append(child_index)
   #
   # child_content
   child_content = ''
   child_count   = count + [0]
   for child_index in in_toc_cmd_list + in_parent_file_list :
      #
      # child_count
      child_count[-1] += 1
      child_content += page_table_of_contents(
         tmp_dir, target, child_count, all_page_info, child_index
      )
   #
   # content
   content += child_content
   #
   return content
# ----------------------------------------------------------------------------
# {xrst_begin table_of_contents dev}
# {xrst_spell
#     bool
#     dir
#     tmp
# }
# {xrst_comment_ch #}
#
# Create the table of contents and Modify Titles
# ##############################################
#
# Arguments
# *********
#
# tmp_dir
# =======
# is the temporary directory where the temporary rst files are written.
#
# target
# ======
# is either 'html' or 'tex'.
#
# tex
# ---
# If target is 'tex',  for each temporary file
# tmp_dir/page_name.rst the text \\n{xrst_before_title}
# is removed and  the page number followed by the page name is added
# at the front of the title for the page.
# The page number includes the counter for each level.
#
# html
# ----
# If target is 'html',
# \\n{xrst_before_title} is removed without other changes.
#
# all_page_info
# =============
# is a list with length equal to the number of pages.
# The value all_page_info[page_index] is a dictionary for this page
# with the following key, value pairs (all the keys are strings):
#
# ..  csv-table::
#     :header: key, value, type
#
#     page_name, contains the name of this page, str
#     page_title,  contains the title for this page, str
#     parent_page, index in all_page_info for the parent of this page, int
#     in_parent_file, is this page in same input file as its parent, bool
#
# root_page_list
# ==============
# is a list of strings containing the root page name for each group.
# The order of the root page names determine the order of the groups
# int the table of contents.
#
# Returns
# *******
#
# content
# =======
# The return content is the table of contents entries for all the pages.
# The title Table of Contents and the label xrst_table_of_contents
# are placed at the beginning of the of content.
#
# {xrst_code py}
def table_of_contents(
   tmp_dir, target, all_page_info, root_page_list
) :
   assert type(tmp_dir) == str
   assert type(target) == str
   assert target in [ 'html', 'tex']
   assert type(all_page_info) == list
   assert type(all_page_info[0]) == dict
   assert type(root_page_list) == list
   assert type(root_page_list[0]) == str
   # {xrst_code}
   # {xrst_literal
   #  BEGIN_return
   #  END_return
   # }
   # {xrst_end table_of_contents}
   #
   # content
   content  = '.. _xrst_table_of_contents-title:\n\n'
   content += 'Table of Contents\n'
   content += '*****************\n'
   #
   # content
   if len(root_page_list) == 1 :
      count = []
      page_name  = root_page_list[0]
      page_index = page_name2index(all_page_info, page_name)
      content += page_table_of_contents(
         tmp_dir, target, count, all_page_info, page_index
      )
   else :
      count = [0]
      for page_name in  root_page_list :
         page_index = page_name2index(all_page_info, page_name)
         count[0]     += 1
         content      += page_table_of_contents(
            tmp_dir, target, count, all_page_info, page_index
         )
   #
   # BEGIN_return
   assert type(content) == str
   return content
   # END_return
