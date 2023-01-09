# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Bradley M. Bell <bradbell@seanet.com>
# SPDX-FileContributor: 2020-22 Bradley M. Bell
# ----------------------------------------------------------------------------
import re
import toml
import xrst
# ----------------------------------------------------------------------------
# {xrst_begin rename_group dev}
# {xrst_spell
#     dir
#     tmp
#     toml
# }
# {xrst_comment_ch #}
#
# Rename a Subset of a Group
# ##########################
#
# tmp_dir
# *******
# is the directory where spell.toml is located
#
# old_group_name
# **************
# is the old name that we are replacing in the xrst begin commands.
#
# new_group_name
# **************
# is the new name that we are using in the xrst begin commands.
#
# spell.toml
# **********
# see :ref:`replace_spell@spell.toml` .
#
# {xrst_code py}
def rename_group(tmp_dir, old_group_name, new_group_name) :
   assert type(tmp_dir) == str
   assert type(old_group_name) == str
   assert type(new_group_name) == str
   # {xrst_code}
   # {xrst_end rename_group}
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
      # data_out
      data_out      = ''
      data_in_index = 0
      #
      # page_name, page_info
      for page_name, page_info in page_list :
         #
         # m_begin
         m_begin = xrst.pattern['begin'].search(data_in, data_in_index)
         while m_begin.group(3) != page_name :
            m_begin = xrst.pattern['begin'].search(data_copy, m_begin.end())
         #
         # before_begin
         before_begin = m_begin.group(1)
         #
         # begin_type
         begin_type = m_begin.group(2)
         #
         # this_page_name
         this_page_name = m_begin.group(3)
         assert this_page_name == page_name
         #
         # this_group_name
         this_group_name = m_begin.group(4).strip()
         if this_group_name == '' :
            this_group_name = 'default'
         assert this_group_name == old_group_name
         #
         # data_before, data_after
         data_before = data_in[data_in_index : m_begin.start() ]
         #
         # begin_command
         begin_command = before_begin + '{' + \
               f'xrst_{begin_type} {page_name} {new_group_name}' + \
         '}'
         #
         # data_out
         data_out += data_before + begin_command
         #
         # data_in_index
         data_in_index = m_begin.end()
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
