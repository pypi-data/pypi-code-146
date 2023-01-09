# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Bradley M. Bell <bradbell@seanet.com>
# SPDX-FileContributor: 2020-23 Bradley M. Bell
# -----------------------------------------------------------------------------
import re
import sys
import subprocess
# -----------------------------------------------------------------------------
# {xrst_begin check_input_files dev}
# {xrst_spell
#     conf
#     config
#     fullmatch
#     len
#     toc
# }
# {xrst_comment_ch #}
#
# Check That Expected xrst Input Files Are Included
# #################################################
#
# config_file
# ***********
# is the name of the configuration file.
#
# conf_dict
# *********
# is a python dictionary representation of the configuration file.
#
# group_name
# **********
# is the name of the group that we are checking
#
# toc_file_set
# ************
# is the set of files that were included by toc commands starting
# at the root file for this group.
# A warning is printed if a file has a begin command for this group
# and it is not in *toc_file_set*.
#
# file_list_in
# ************
# If file_list_in is None, the :ref:`config_file@input_files` commands
# will be executed to determine the file list.
# Otherwise, *file_list_in* will be used as the output of the first
# successful command.
#
# file_list_out
# *************
# This is a value that can be used for *file_list_in* to avoid
# having to re-execute the input_files commands.
#
# file_list_warning
# *****************
# This is true (false) if an input file list warning is (is not) printed
#
# Prototype
# *********
# {xrst_code py}
# file_list_out, file_list_warning =
def check_input_files(
   config_file, conf_dict, group_name, toc_file_set, file_list_in
) :
   #
   assert type(config_file) == str
   assert type(conf_dict) == dict
   assert type(group_name) == str
   assert type(toc_file_set) == set
   if file_list_in != None :
      assert type(file_list_in) == list
      if len(file_list_in) > 0 :
         assert type( file_list_in[0] ) == str
   #
   assert group_name != ''
   p_group_name = re.compile( r'[a-z]+' )
   assert p_group_name.fullmatch( group_name )
   # {xrst_code}
   # {xrst_literal
   #     # BEGIN_RETURN
   #     # END_RETURN
   # }
   # {xrst_end check_input_files}
   #
   # input_files
   input_files = conf_dict['input_files']['data']
   #
   # file_list_out
   if file_list_in != None :
      file_list_out = file_list_in
   elif len(input_files) == 0 :
      file_list_out = list()
   else :
      file_list_out = None
      command       = None
      for cmd in input_files :
         try :
            result  = subprocess.run(
               cmd,
               stdout   = subprocess.PIPE,
               stderr   = subprocess.PIPE,
               encoding = 'utf-8',
            )
         except:
            result = None
         if result == None :
            pass
         elif result.returncode == 0 :
            command       = cmd
            file_list_out = result.stdout
            if 0 <= file_list_out.find('"')  or 0 <= file_list_out.find("'") :
               msg  = 'warning: single or double quote in output of '
               msg += f'the input_files command: {command}\n'
               msg += 'This feature is not yet supported\n'
               sys.write(msg)
               file_list_out == list()
            else :
               file_list_out = file_list_out.split()
      if file_list_out != None :
         command = ' '.join(command)
         msg = f'Using following input_files: {command}\n'
         sys.stdout.write(msg)
      elif len(input_files) > 0 :
         msg  = 'warning: None of the commands in '
         msg += f'{config_file}.input_files succeeded\n'
         sys.stderr.write(msg)
         file_list_out = list()
   #
   # p_empty
   p_empty  = r'(^|[^\\])\{xrst_(begin|begin_parent)[ \t]+([^ \t}]*)[ \t]*}'
   p_empty  = re.compile(p_empty)
   #
   # p_non_empty
   p_non_empty  = r'(^|[^\\])\{xrst_(begin|begin_parent)[ \t]+([^ \t}]*)[ \t]+'
   p_non_empty += group_name
   p_non_empty += r'[ \t]*}'
   p_non_empty  = re.compile( p_non_empty )
   #
   # group_file_set
   group_file_set = set()
   #
   # warning_count
   warning_count = 0
   #
   # file_name
   for file_name in file_list_out :
      if warning_count < 10 :
         #
         # file_data
         try :
            file_obj     = open(file_name, 'r')
            file_data    = file_obj.read()
            file_obj.close()
         except :
            file_data = ''
         #
         # m_non_empty
         m_non_empty = p_non_empty.search( file_data )
         if m_non_empty != None :
            if file_name not in toc_file_set :
               if warning_count == 0 :
                  msg  = '\nwarning: group_name = ' + group_name + '\n'
                  msg += 'The following files have pages with this group name '
                  msg += 'but they are not in any xrst_toc commands '
                  msg += 'starting at the root_file for this group\n'
                  sys.stderr.write(msg)
               msg = 3 * ' ' +file_name + '\n'
               sys.stderr.write(msg)
               warning_count += 1
         #
         # m_empty
         elif group_name == 'default' :
            m_empty = p_empty.search( file_data )
            if m_empty != None :
               if file_name not in toc_file_set :
                  if warning_count == 0 :
                     msg  = '\nwarning: group_name = ' + group_name + '\n'
                     msg += 'The following files have pages with '
                     msg += 'the empty group name\n'
                     msg += 'but they are not in any xrst_toc commands '
                     msg += 'starting at the root_file for the default group\n'
                     sys.stderr.write(msg)
                  msg = 3 * ' ' +file_name + '\n'
                  sys.stderr.write(msg)
                  warning_count += 1
            #
            if warning_count == 10 :
               msg+= f'Surpressing this warning after {warning_count} files.\n'
               sys.stderr.write(msg)
   file_list_warning = 0 < warning_count
   # BEGIN_RETURN
   assert type(file_list_warning) == bool
   assert type(file_list_out) == list
   if len(file_list_out) > 0 :
      assert type( file_list_out[0] ) == str
   return file_list_out, file_list_warning
   # END_RETURN
