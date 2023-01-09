# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Bradley M. Bell <bradbell@seanet.com>
# SPDX-FileContributor: 2020-23 Bradley M. Bell
# ----------------------------------------------------------------------------
import os
import re
import subprocess
# ----------------------------------------------------------------------------
def get_index_page_name() :
   file_obj  = open('.readthedocs.yaml', 'r')
   file_data = file_obj.read()
   pattern   = r'\n *--index_page_name *([-._a-zA-Z0-9]*)'
   m_obj     = re.search(pattern, file_data)
   file_obj.close()
   return m_obj.group(1)
# ----------------------------------------------------------------------------
def get_rst_directory() :
   file_obj  = open('xrst.toml', 'r')
   file_data = file_obj.read()
   pattern   = r"\nrst_directory *= *'([^']*)'"
   m_obj     = re.search(pattern, file_data)
   file_obj.close()
   return m_obj.group(1)
# ----------------------------------------------------------------------------
def run_xrst() :
   index_page_name = get_index_page_name()
   #
   # This command should be the same as the one in bin/check_xrst.sh
   # that's used to keep the test_rst directory up to date.
   command = [
      'python3', '-m', 'xrst',
      '--local_toc',
      '--rst_only',
      '--config_file',     'xrst.toml',
      '--index_page_name', index_page_name,
      '--group_list',      'default', 'user', 'dev',
      '--html_theme',      'sphinx_rtd_theme',
   ]
   result = subprocess.run(command)
   assert result.returncode == 0
# ----------------------------------------------------------------------------
def run_test() :
   run_xrst()
   #
   # rst_list
   rst_directory = get_rst_directory()
   rst_list      = list()
   for entry in os.listdir(rst_directory) :
      if entry.endswith('.rst') :
         rst_list.append(entry)
   rst_list = sorted(rst_list)
   #
   # check_list
   check_list = sorted( os.listdir('test_rst') )
   #
   # rst_index, check_index
   rst_index   = 0
   check_index = 0
   while rst_index < len(rst_list) and check_index < len(check_list) :
      #
      # rst_name, check_name
      rst_name   = rst_list[rst_index]
      check_name = check_list[check_index]
      if rst_name < check_name :
         rst_index += 1
         assert False, f'{rst_name} is in {rst_directory} but not test_rst'
      elif check_name < rst_name :
         check_index += 1
         assert False, f'{check_name} is in test_rst but not {rst_directory}'
      else :
         #
         # rst_index, check_index
         rst_index     += 1
         check_index   += 1
         #
         # rst_file_data, check_file_data
         rst_file      = f'{rst_directory}/{rst_name}'
         check_file    = f'test_rst/{check_name}'
         #
         rst_file_obj   = open(rst_file, 'r')
         check_file_obj = open(check_file, 'r')
         #
         rst_data      = rst_file_obj.read()
         check_data    = check_file_obj.read()
         #
         rst_file_obj.close()
         check_file_obj.close()
         #
         if rst_data == check_data :
            print( f'{rst_name}: OK' )
         else :
            msg = f'{rst_file} is different from {check_file}'
            breakpoint()
            assert False, msg
# ----------------------------------------------------------------------------
def test_rst() :
   if not os.path.exists('xrst.toml') :
      assert False, 'test_rst.py: must start in the xrst top source directory'
   else :
      run_test()
# ----------------------------------------------------------------------------
if __name__ == '__main__' :
   test_rst()
