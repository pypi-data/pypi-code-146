#! /usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Bradley M. Bell <bradbell@seanet.com>
# SPDX-FileContributor: 2020-22 Bradley M. Bell
# ----------------------------------------------------------------------------
#
import sys
import re
import os
import xrst
#
# usage
usage = \
'''
usage: update_xrst.py operation file_in file_out

operation: is one of the following: dot2atsign
file_in:   is the name of the file we are updating.
file_out:  is the name of the updated file. It can be the samle as file_in.

comment_ch:
Change comment_ch command from file scope to page scope.

ref_section_2:
Change :ref:`section_name-0` -> :ref:`section_name-0`,

literal_order:
{xrst_literal start stop display_file}->{xrst_literal display_file start stop}

tab3space:
Change tabs to 3 spaces.

space4to3:
Change tab stop from 4 spaces to 3 spaces.

file2literal:
change xrst_file -> xrst_literal.

child2toc:
Change xrst_children ->, xrst_toc_hidden, xrst_child_list -> xrst_toc_list,
and xrst_child_table -> xrst_toc_table.

ref_section:
Change :ref:`section_name-name` -> :ref:`section_name-0`,
Change :ref:`section_name<section_name-name>` -> :ref:`section_name-name`

dot2atsign:
Change the '.' to '@' character in all text of the form :ref:`text-name` and
text of the form (at the betinning of a line) .. _text:

xsrst2xrst:
Change 'xsrst' to 'xrst' in all the text.

'''
#
#
# abort
def abort(msg) :
   msg = '\nupdate_xstst.py: ' + msg
   sys.exit(msg)
#
# ref_section_2
def ref_section_2(data_in) :
   #
   # pattern
   pattern = re.compile( r':ref:`@([._a-z0-9]+)`' )
   #
   # data_out
   data_out  = pattern.sub( r':ref:`\1-0`', data_in)
   return data_out
#
# comment_ch:
def comment_ch(data_in) :
   # data_out
   data_out = data_in
   #
   # command
   pattern = re.compile(
      r'(^|[^\\])\{xrst_comment_ch\s+([^} \t]*)\s*}'
   )
   m_obj = pattern.search(data_out)
   if m_obj == None :
      return data_out
   comment_ch = m_obj.group(2)
   command    = comment_ch + ' {xrst_comment_ch ' + comment_ch + '}\n'
   #
   # data_out
   start = m_obj.start() - 1
   while start > 0 and data_out[start] in '[ \t]' :
      start -= 1
   assert data_out[start] == comment_ch
   end   = m_obj.end()
   while data_out[end] in '[ \t]' :
      end += 1
   assert data_out[end] == '\n'
   data_out = data_out[: start] + data_out[end +1 :]
   #
   # pattern
   pattern = re.compile(
      r'([^\\]{xrst_(begin|begin_parent)[ \t]+[^}]*}[^\n]*\n)([ \t]*)'
   )
   #
   # m_begin
   m_begin = pattern.search(data_out)
   while m_begin :
      #
      # indent
      indent = m_begin.group(3)
      #
      # data_out
      end      = m_begin.end()
      data_out = data_out[: end] + command + indent + data_out[end :]
      #
      m_begin = pattern.search(data_in, end + len(command))
   return data_out
#
# literal_order:
def literal_order(data_in) :
   # data_out
   data_out = data_in
   #
   # pattern
   pattern = re.compile(
      r'{xrst_literal[ \t]*\n([^}\n]*)\n([^}\n]*)\n([^}\n]*)\n([^}]*)}'
   )
   #
   # m_obj
   m_obj = pattern.search(data_out)
   while m_obj :
      #
      # command
      command  = '{xrst_literal\n'
      command += m_obj.group(3) + '\n'
      command += m_obj.group(1) + '\n'
      command += m_obj.group(2) + '\n'
      command += m_obj.group(4) + '}'
      #
      # data_out, data_left
      data_before = data_out[:  m_obj.start()]
      data_left   = data_before + command
      data_after  = data_out[m_obj.end() :]
      data_out    = data_before + command + data_after
      #
      # m_obj
      m_obj = pattern.search(data_out, len(data_left) )
   #
   return data_out
#
# tab3space:
def tab3space(data_in) :
   # data_out
   data_out = data_in
   #
   # pattern
   # group(1): start of line
   # group(2): possible newline_ch character
   # group(3): one or more of tabs
   pattern  = re.compile( r'(^|\n)([^\n\t]?)(\t{1,})' )
   #
   # m_obj
   m_obj   = pattern.search(data_out)
   #
   # data_out
   while m_obj :
      #
      # n_tab
      n_tab = len( m_obj.group(3) )
      assert 0 < n_tab
      #
      # replace
      if m_obj.group(2) == '' :
         replace  = m_obj.group(1) + n_tab * (3 * ' ')
      else :
         replace  = m_obj.group(1) + m_obj.group(2) + 2 * ' '
         replace += (n_tab - 1) * (3 * ' ')
      #
      # data_left, data_out
      data_left  = data_out[: m_obj.start()] + replace
      data_right = data_out[m_obj.end() :]
      data_out   = data_left + data_right
      #
      # m_obj
      m_obj    = pattern.search(data_out, len(data_left) )
   #
   # pattern
   # group(1): one non newline or tab
   # group(2): one or more tabs
   pattern  = re.compile( r'([^\n\t])(\t{1,})' )
   #
   # m_obj
   m_obj = pattern.search(data_out)
   #
   # data_out
   while m_obj :
      #
      # n_tab
      n_tab = len( m_obj.group(2) )
      assert 0 < n_tab
      #
      # replace
      replace  = m_obj.group(1) + 2 * ' '
      replace += (n_tab - 1) * (3 * ' ')
      #
      #
      # data_left, data_out
      data_left  = data_out[: m_obj.start()] + replace
      data_right = data_out[m_obj.end() :]
      data_out   = data_left + data_right
      #
      # m_obj
      m_obj    = pattern.search(data_out, len(data_left) )
   #
   if 0 <= data_out.find('\t') :
      msg = 'update_xrst.py tab3space: not all tabs have been replaced'
      assert False, msg
   #
   return data_out
#
# space4to3:
def space4to3(data_in) :
   # data_out
   data_out = data_in
   #
   # data_out
   pattern  = re.compile( r'(^|\n)([0-9#.]\.)  ([^ ])' )
   data_out = pattern.sub(r'\1\2 \3', data_out)
   #
   # data_out
   pattern = re.compile( r'(^|\n)-   ([^ ])' )
   data_out = pattern.sub(r'\1-  \2', data_out)
   #
   # pattern
   pattern = re.compile( r'(^|\n)([# ]   (    ){0,})[^ ]' )
   #
   # m_obj
   m_obj   = pattern.search(data_out)
   while m_obj :
      #
      # start, end
      start = m_obj.start() + len( m_obj.group(1) )
      end   = m_obj.end() - 1
      assert end - start == len( m_obj.group(2) )
      #
      # n_indent
      n_indent = int ( (end - start) / 4 )
      assert (end - start) == n_indent * 4
      #
      # data_out
      replace  = n_indent * '   '
      if data_out[start] != ' ' :
         replace = data_out[start] + replace[1 :]
      data_out = data_out[: start] + replace + data_out[end :]
      #
      # m_obj
      m_obj    = pattern.search(data_out, start + n_indent * 3 )
   #
   # data_out
   pattern = re.compile( r'(^|\n)((   ){0,}){   ([^ ])' )
   data_out = pattern.sub( r'\1\2{  \4', data_out )
   #
   pattern  = re.compile( r'(\n# {8})(Copyright \(C\))' )
   data_out = pattern.sub( r'\1   \2', data_out )
   #
   pattern  = re.compile( r'(\n {3})(GNU Affero General Public)' )
   data_out = pattern.sub( r'\1 \2', data_out )
   # -----------------------------------------------------------------------
   return data_out
#
# fiile2literal:
def file2literal(data_in) :
   data_out = data_in.replace('{xrst_file', '{xrst_literal')
   return data_out
#
# child2toc:
def child2toc(data_in) :
   data_out = data_in.replace('{xrst_children', '{xrst_toc_hidden')
   data_out = data_out.replace('{xrst_child_list', '{xrst_toc_list')
   data_out = data_out.replace('{xrst_child_table', '{xrst_toc_table')
   return data_out
#
# ref_section
def ref_section(data_in) :
   #
   # pattern
   pattern = dict()
   pattern['title']        = re.compile( r':ref:`([._a-z0-9]+)`' )
   pattern['section_name'] = re.compile( r':ref:`([._a-z0-9]+)<\1>`' )
   #
   # data_out
   data_out  = data_in
   data_out  = pattern['title'].sub( r':ref:`@\1`', data_out)
   data_out  = pattern['section_name'].sub( r':ref:`\1`', data_out)
   data_out  = data_out.replace(':ref:`genindex-0`', ':ref:`genindex`')
   return data_out
#
# dot2atsign
def dot2atsign(data_in) :
   # pattern
   pattern        = dict()
   pattern['ref'] = re.compile( r'(:ref:`[^`]*)\.' )
   #
   # data_out
   data_out = data_in
   #
   # m_ref
   m_ref    = pattern['ref'].search(data_out)
   while m_ref :
      # data_out
      data_out = pattern['ref'].sub(r'\1@', data_out)
      #
      # m_ref
      m_ref  = pattern['ref'].search(data_out, m_ref.start() )
   #
   return data_out
#
# xsrst2xrst
def xsrst2xrst(data_in) :
   data_out = data_in.replace('xsrst', 'xrst')
   return data_out
#
# main
def main() :
   if( len(sys.argv) != 4 ) :
      print(usage)
   #
   # operation_dict
   operation_dict = {
      'comment_ch'    :  comment_ch,
      'ref_section_2' :  ref_section_2,
      'literal_order' :  literal_order,
      'tab3space'     :  tab3space,
      'space4to3'     :  space4to3,
      'file2literal'  :  file2literal,
      'child2toc'     :  child2toc,
      'ref_section'   :  ref_section,
      'dot2atsign'    :  dot2atsign,
      'xsrst2xrst'    :  xsrst2xrst,
   }
   #
   # operation
   operation = sys.argv[1]
   if operation not in operation_dict :
      msg  = f'operation = {operation} is not a valid operation'
      abort(msg)
   #
   # file_in,
   file_in = sys.argv[2]
   if not os.path.isfile(file_in) :
      msg = f'file_in = {file_in} is not an existing file'
      abort(msg)
   #
   # file_out
   file_out = sys.argv[3]
   #
   # file_data
   file_obj   = open(file_in, 'r')
   file_data  = file_obj.read()
   file_obj.close()
   #
   # file_out
   file_data = operation_dict[operation](file_data)
   #
   # file_out
   file_obj = open(file_out, 'w')
   file_obj.write(file_data)
   file_obj.close()
#
main()
print('update_xrst.py: OK')
sys.exit(0)
