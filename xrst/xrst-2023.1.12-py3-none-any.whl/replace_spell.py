# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Bradley M. Bell <bradbell@seanet.com>
# SPDX-FileContributor: 2020-22 Bradley M. Bell
# ----------------------------------------------------------------------------
import re
import toml
import xrst
# {xrst_begin replace_spell dev}
# {xrst_spell
#     dir
#     tmp
#     toml
# }
# {xrst_comment_ch #}
#
# Replace spelling commands
# #########################
#
# tmp_dir
# *******
# is the directory where spell.toml is located
#
# spell.toml
# **********
# The file *tmp_dir* ``/spell.toml`` contains the information below.
# For each file that was included in the documentation,
# for each page in that file::
#
#     [file_name.page_name]
#     begin_line  = integer line number where begin command is located
#     start_spell = integer line number where the spell command starts
#     end_spell   = integer line number where the spell command ends
#     unknown     = array of strings (words) that are not in dictionary
#
# It is called spell.tom because it is written by the
# :ref:`spell_cmd_dev-name` one page at a time.
#
# #.  file_name and page_name are strings.
# #.  file_name is relative to the
#     :ref:`config_file@directory@project_directory` .
# #.  Descriptions to the left (right) of the equal signs are literal text
#     (replaced by their values).
# #.  Line numbers start at one and are for the specified file.
# #.  The line number zero is used for start_spell and end_spell when
#     there is no spell command for this page.
# #.  The spell start and end lines do not overlap the begin line.
#
# {xrst_code py}
def replace_spell(tmp_dir) :
   assert type(tmp_dir) == str
   # {xrst_code}
   # {xrst_end replace_spell}
   #
   # spell_toml
   file_obj  = open( f'{tmp_dir}/spell.toml' )
   file_data = file_obj.read()
   spell_toml = toml.loads(file_data)
   #
   # file_name
   for file_name in spell_toml :
      #
      # page_list
      page_list = list()
      for page_name in spell_toml[file_name] :
         pair = (page_name , spell_toml[file_name][page_name] )
         page_list.append( pair )
      #
      # page_list
      order_fun    = lambda page_pair : page_pair[1]['begin_line']
      page_list = sorted(page_list, key = order_fun )
      #
      # data_in
      file_obj = open(file_name, 'r')
      data_in  = file_obj.read()
      file_obj.close()
      #
      # page_list
      # add begin_index, start_index, end_index
      line_number = 0
      for m_newline in re.finditer( r'(^|\n)',  data_in) :
         line_number += 1
         for page_name, page_info in page_list :
            if page_info['begin_line'] + 1 == line_number :
               page_info['begin_index'] = m_newline.start()
            if page_info['start_spell'] == line_number :
               page_info['start_index'] = m_newline.start() + 1
            if page_info['end_spell'] + 1 == line_number :
               page_info['end_index'] = m_newline.start() + 1
      #
      # data_copy
      data_copy = data_in
      data_copy = xrst.add_line_numbers(data_copy)
      #
      # data_out
      data_out      = ''
      data_in_index = 0
      #
      # page_name, page_info
      for page_name, page_info in page_list :
         #
         # m_begin
         m_begin = xrst.pattern['begin'].search(data_copy)
         while m_begin.group(3) != page_name :
            m_begin = xrst.pattern['begin'].search(data_copy, m_begin.end())
         #
         # m_end
         m_end = xrst.pattern['end'].search(data_copy, m_begin.end() )
         #
         # page_data
         page_data = data_copy[m_begin.end() : m_end.start() ]
         #
         # indent
         not_used, indent = xrst.remove_indent(
            page_data, file_name, page_name
         )
         #
         # comment_ch
         not_used, comment_ch = xrst.comment_ch_command(
            page_data, file_name, page_name
         )
         #
         # begin_line, indent_line
         if comment_ch :
            begin_line  = '\n' + indent + comment_ch + ' '
            indent_line = begin_line + 4 * ' '
         else :
            begin_line  = '\n' + indent
            indent_line = begin_line + 3 * ' '
         #
         # data_out, data_in_index
         begin_index   = page_info['begin_index']
         data_out     += data_in[data_in_index : begin_index]
         data_in_index = begin_index
         #
         # data_out
         unknown = page_info['unknown']
         if len(unknown) > 0 :
            data_out += begin_line + '{xrst_spell'
            unknown   = sorted(unknown)
            i         = 0
            while i < len(unknown) :
               word = unknown[i]
               if i + 1 < len(unknown) and word == unknown[i+1] :
                  data_out += indent_line + word + ' ' + word
                  i         = i + 2
               else :
                  data_out += indent_line + word
                  i         = i + 1
            data_out += begin_line + '}'
         #
         # data_out, data_in_index
         if 'start_index' in page_info :
            start_index  = page_info['start_index']
            end_index    = page_info['end_index']
            #
            data_out     += data_in[data_in_index : start_index]
            data_in_index = end_index
      #
      # data_out
      data_out += data_in[data_in_index :]
      #
      # file_name
      file_obj = open(file_name, 'w')
      file_obj.write( data_out )
      file_obj.close()
   #
   return
