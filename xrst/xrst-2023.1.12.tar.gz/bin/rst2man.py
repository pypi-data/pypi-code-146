#! /usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Bradley M. Bell <bradbell@seanet.com>
# SPDX-FileContributor: 2020-23 Bradley M. Bell
# -----------------------------------------------------------------------------
import re
import sys
import os
import toml
import tempfile
import subprocess
#
# pattern
pattern = dict()
pattern['index'] = re.compile( r'\n[.][.] index::[^\n]*' )
pattern['ref<>'] = re.compile( r':ref:`([^<`]*)<[^>`]*>`' )
pattern['ref@']  = re.compile( r':ref:`[^<`]*@([^<`@]*)`' )
pattern['ref-']  = re.compile( r':ref:`([^<@`]*)-(name|title)`' )
#
# main
def main() :
   #
   # rst_file, man_file
   if len(sys.argv) != 3 :
      msg = 'usage: bin/rst2man.py rst_file man_file'
      sys.exit(msg)
   rst_file = sys.argv[1]
   man_file = sys.argv[2]
   #
   if not os.path.isfile(rst_file) :
      msg = f'rst_file = {rst_file} is not a file'
      sys.exit(msg)
   #
   # rst_prolog
   if not os.path.isfile('xrst.toml') :
      msg = f'Cannot find xrst.toml in current directory'
      sys.exit(msg)
   file_obj    = open('xrst.toml', 'r')
   file_data   = file_obj.read()
   conf_dict   = toml.loads(file_data)
   rst_prolog  = conf_dict['include_all']['rst_prolog']
   file_obj.close()
   #
   # rst_data
   file_obj  = open(rst_file, 'r')
   rst_data  = file_obj.read()
   file_obj.close()
   #
   # temp_data
   temp_data = rst_prolog + rst_data
   temp_data = pattern['index'].sub(r'', temp_data)
   temp_data = pattern['ref<>'].sub(r'\1', temp_data)
   temp_data = pattern['ref@'].sub(r'\1', temp_data)
   temp_data = pattern['ref-'].sub(r'\1', temp_data)
   #
   # temp_file
   (fd, temp_file) = tempfile.mkstemp(
      suffix='.rst', prefix='rst2man_', dir='build', text=True
   )
   os.close(fd)
   file_obj  = open(temp_file, 'w')
   file_obj.write(temp_data)
   file_obj.close()
   #
   # man_file
   command = [ 'rst2man', temp_file, man_file ]
   subprocess.run(command)
   #
   # temp_file
   os.remove(temp_file)
#
main()
