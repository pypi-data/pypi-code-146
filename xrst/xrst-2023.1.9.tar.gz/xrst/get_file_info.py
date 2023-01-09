# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Bradley M. Bell <bradbell@seanet.com>
# SPDX-FileContributor: 2020-23 Bradley M. Bell
# ----------------------------------------------------------------------------
"""
{xrst_begin begin_cmd user}
{xrst_spell
   genindex
   toc
   underbar
}

Begin and End Commands
######################

Syntax
******
- ``\{xrst_begin_parent`` *page_name* *group_name* ``}``
- ``\{xrst_begin``        *page_name* *group_name* ``}``
- ``\{xrst_end``          *page_name* ``}``

Page
****
The start (end) of a page of the input file is indicated by a
begin (end) command.

page_name
*********
A *page_name* must satisfy the following conditions:

#. It must be a non-empty sequence of the following characters:
   dash ``-``, period ``.``, underbar ``_``, the letters A-Z, letters a-z,
   and decimal digits 0-9.
#. The page name can not be ``index`` or ``genindex`` ,
   and it can not begin with the characters ``xrst_``.
#. The lower case version of two page names cannot be equal.

A link is included in the index under the page name to the page.
The page name is also added to the html keyword meta data.

group_name
**********
The *group_name* can be empty or a sequence of the letters a-z.
This is the group that this page belongs to; see
:ref:`run_xrst@group_list`.

Default Group
=============
The default value for *group_name* is ``default``; i.e.,
if *group_name* is the empty string, this page is part of the default group.

Output File
***********
The output file corresponding to *page_name* is

   *rst_directory*\ /\ *page_name*\ /``.rst``

see :ref:`config_file@directory@rst_directory` .

Parent Page
***********
The following conditions hold for each *group_name*:

#. There can be at most one begin parent command in an input file.
#. If there is a begin parent command, it must be the first begin command
   in the file and there must be other pages in the file.
#. The other pages are children of the parent page.
#. The parent page is a child
   of the page that included this file using a
   :ref:`toc command<toc_cmd-name>`.
#. If there is no begin parent command in an input file,
   all the pages in the file are children
   of the page that included this file using a
   :ref:`toc command<toc_cmd-name>`.

Note that there can be more than one begin parent command in a file if
they have different group names. Also note that pages are only children
of pages that have the same group name.

{xrst_end begin_cmd}
"""
# ---------------------------------------------------------------------------
import xrst
import re
pattern_group_name  = re.compile( r'[^ \t]+' )
pattern_group_valid = re.compile( r'[a-z]+' )
# ---------------------------------------------------------------------------
# {xrst_begin get_file_info dev}
# {xrst_spell
#     len
# }
# {xrst_comment_ch #}
#
# Get information for all pages in a file
# #######################################
#
# Arguments
# *********
#
# all_page_info
# =============
# a list of with information for pages that came before this file.
# For each list index, all_page_info[index] is a dict and
# all_page_info[index]['page_name'] is an str
# containing the name of a page that came before this file.
# This includes pages for all the groups that came before this group.
#
# group_name
# ==========
# We are only retrieving information for pages in this group.
# (This is non-empty because default is used for the empty group name.)
#
# parent_file
# ===========
# name of the file that included file_in.
#
# file_in
# =======
# is the name of the file we are getting all the information for.
#
# Returns
# *******
#
# file_page_info
# ==============
# The value file_page_info is a list of dict.
# Each dict contains the information
# for one page in this file. We use info below for one element of the list:
#
# info['page_name']
# -----------------
# is an str containing the name of a page in this file.
#
# info['page_data']
# -----------------
# is an str containing the data for this page.
#
#  #. Line numbers have been added using :ref:`add_line_numbers-name` .
#     This is the first operation done on a page and other operations
#     assume that line numbers are present. They are removed near the end
#     when the temporary file corresponding to a page is created.
#  #. If present for this page, the comment character and possible space
#     after have been removed.
#  #. The xrst begin and end commands are not include in this data.
#  #. The first (last) line number corresponds to the begin (end) command
#  #. The suspend / resume commands and data between such pairs
#     have been removed.
#  #. If there is a common :ref`indent` for the entire page,
#     it has been removed.
#
# info['is_parent']
# -----------------
# is true (false) if this is (is not) the parent page for the other
# pages in this file. The parent page must be the first for this group,
# and hence have index zero in file_info. In addition,
# if there is a parent page, there must be at least one other page;
# i.e., len(file_info) >= 2.
#
# info['is_child']
# ----------------
# is true (false) if this is (is not) a child of the first page in
# this file.
#
# info['begin_line']
# is the line number in *file_in* where this page begins; i.e.,
# the line number where the begin command is located.
#
# info['end_line']
# is the line number in *file_in* where this page ends; i.e.,
# the line number where the end command is located.
#
# {xrst_code py}
def get_file_info(
      all_page_info,
      group_name,
      parent_file,
      file_in,
) :
   assert type(all_page_info) == list
   if 0 < len(all_page_info) :
      type( all_page_info[0] ) == dict
   assert type(group_name) == str
   assert group_name != ''
   assert type(parent_file) == str or parent_file == None
   assert type(file_in) == str
   # {xrst_code}
   # {xrst_literal
   #  BEGIN_return
   #  END_return
   # }
   # {xrst_end get_file_info}
   #
   # file_data
   file_obj   = open(file_in, 'r')
   file_data  = file_obj.read()
   file_obj.close()
   #
   # file_data
   file_data = xrst.add_line_numbers(file_data)
   #
   # file_page_info
   file_page_info = list()
   #
   # parent_page_name
   parent_page_name = None
   #
   # data_index
   # index to start search for next pattern in file_data
   data_index  = 0
   #
   # found_group_name
   found_group_name = False
   #
   # for each page in this file
   while data_index < len(file_data) :
      #
      # m_begin
      m_begin = xrst.pattern['begin'].search(file_data, data_index)
      #
      # this_group_name
      if m_begin != None :
         #
         this_group_name = m_begin.group(4)
         m_group         = pattern_group_name.search(this_group_name)
         if m_group == None :
            this_group_name = 'default'
         else :
            this_group_name = m_group.group(0)
            m_group    = pattern_group_valid.search(this_group_name)
            if this_group_name != m_group.group(0) :
               msg = f'"{this_group_name}" is not a valid group name'
               xrst.system_exit(msg,
                  file_name = file_in,
                  m_obj     = m_begin,
                  data      = file_data,
               )
      if m_begin == None :
         if not found_group_name :
            msg  = 'can not find a begin command with \n'
            if group_name == '' :
               msg += 'the empty group name and '
            else :
               msg += f'group_name = {group_name} and '
            msg += f'parent file = {parent_file}'
            xrst.system_exit(msg, file_name=file_in)
         #
         # data_index
         # set so that the page loop for this file terminates
         data_index = len(file_data)
      elif this_group_name != group_name :
         #
         # data_index
         # place to start search for next page
         data_index = m_begin.end()
      else :
         #
         # found_group_name
         found_group_name = True
         #
         # page_name, is_parent
         page_name = m_begin.group(3)
         is_parent = m_begin.group(2) == 'begin_parent'
         #
         # check_page_name
         xrst.check_page_name(
            page_name,
            file_name     = file_in,
            m_obj         = m_begin,
            data          = file_data
         )
         #
         # check if page_name appears multiple times in this file
         for info in file_page_info :
            previous_page_name = info['page_name']
            if page_name.lower() == previous_page_name.lower() :
               msg  = 'Lower case version of two page names are equal.\n'
               msg += f'previous page_name = {previous_page_name}\n'
               msg += f'previous_file      = {file_in}\n'
               xrst.system_exit(msg,
                  file_name      = file_in,
                  page_name      = page_name,
                  m_obj          = m_begin,
                  data           = file_data
               )
         #
         # check if page_name appears in another file
         for info in all_page_info :
            previous_page_name = info['page_name']
            if page_name.lower() == previous_page_name.lower() :
               msg  = 'Lower case version of two page names are equal.\n'
               msg += f'previous_page_name  = "{previous_page_name}"\n'
               msg += 'previous_file        = ' +  info['file_in'] + '\n'
               xrst.system_exit(msg,
                  file_name = file_in  ,
                  page_name = page_name
               );
         #
         # check if parent pages is the first page in this file
         if is_parent :
            if len(file_page_info) != 0 :
               msg  = 'xrst_begin_parent'
               msg += ' is not the first begin command in this file'
               xrst.system_exit(msg,
                  file_name     = file_in,
                  page_name     = page_name,
                  m_obj         = m_begin,
                  data          = file_data
               )
            #
            # parent_page_name
            parent_page_name = page_name
         #
         # is_child
         is_child = (not is_parent) and (parent_page_name != None)
         #
         # data_index
         data_index = m_begin.end()
         #
         # begin_line
         m_line     = xrst.pattern['line'].search(file_data, data_index)
         begin_line = int( m_line.group(1) )
         #
         # m_end
         m_end     = xrst.pattern['end'].search(file_data, data_index)
         #
         if m_end == None :
            msg  = 'Could not find the followig text:\n'
            msg += '    {xrst_end ' + page_name + '}'
            xrst.system_exit(
               msg, file_name=file_in, page_name=page_name
            )
         if m_end.group(1) != page_name :
            msg  = 'begin and end page names do not match\n'
            msg += 'begin name = ' + page_name + '\n'
            msg += 'end name   = ' + m_end.group(1)
            xrst.system_exit(msg,
               file_name = file_in,
               m_obj     = m_end,
               data      = file_data
            )
         #
         # end_line
         m_line     = xrst.pattern['line'].search(file_data, m_end.start())
         end_line = int( m_line.group(1) )
         #
         #
         # page_data
         page_start = data_index
         page_end   = m_end.start() + 1
         page_data  = file_data[ page_start : page_end ]
         #
         # page_data
         # order of these operations is important
         page_data  = xrst.suspend_command(
            page_data, file_in, page_name
         )
         page_data, indent = xrst.remove_indent(
            page_data, file_in, page_name
         )
         #
         # page_data
         page_data, comment_ch = xrst.comment_ch_command(
            page_data, file_in, page_name
         )
         if comment_ch :
            pattern_ch  = re.compile( r'\n[ \t]*[' + comment_ch + r'] ?' )
            page_data   = pattern_ch.sub(r'\n', page_data)
         #
         # file_page_info
         file_page_info.append( {
            'page_name'    : page_name,
            'page_data'    : page_data,
            'is_parent'    : is_parent,
            'is_child'     : is_child,
            'begin_line'   : begin_line,
            'end_line'     : end_line,
         } )
         #
         # data_index
         # place to start search for next page
         data_index = m_end.end()
   #
   if parent_page_name != None and len(file_page_info) < 2 :
      msg  = 'begin_parent command appears with '
      if group_name == '' :
         msg += 'the empty group name\n'
      else :
         msg += f'group_name = {group_name}\n'
      msg += 'and this file only has one page with that group name.'
      xrst.system_exit(
         msg, file_name=file_in, page_name=parent_page_name
      )
   #
   # file_data
   file_data = xrst.pattern['begin'].sub('', file_data)
   file_data = xrst.pattern['end'].sub('', file_data)
   #
   for command_name in [ 'begin' , 'end' ] :
      xrst.check_syntax_error(
         command_name   = command_name,
         data           = file_data,
         file_name      = file_in,
         page_name   = None,
      )
   #
   # BEGIN_return
   assert type(file_page_info) == list
   assert type(file_page_info[0]) == dict
   #
   return file_page_info
   # END_return
