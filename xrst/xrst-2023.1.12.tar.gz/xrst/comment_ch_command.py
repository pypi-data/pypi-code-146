# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Bradley M. Bell <bradbell@seanet.com>
# SPDX-FileContributor: 2020-23 Bradley M. Bell
# ----------------------------------------------------------------------------
"""
{xrst_begin comment_ch_cmd user}

Comment Character Command
#########################

Syntax
******
``\{xrst_comment_ch`` *ch* ``}``

Purpose
*******
Some languages have a special character that
indicates the rest of the line is a comment.
If you embed sphinx documentation in this type of comment,
you need to inform xrst of the special character so it does
not end up in your ``.rst`` output file.

ch
**
The value of *ch* must be one non white space character.
There must be at least one white space character
between ``xrst_comment_ch`` and *ch*.
Leading and trailing white space around *ch* is ignored.

Input Stream
************
Spaces and tabs before the special character,
the special character,
and one space directory after the special character (if present),
are removed from the input stream before any xrst processing.
For example, if :code:`#` is the special character,
the following input has the heading Factorial
and the ``def`` token indented the same amount:

.. code-block:: py

   # Factorial
   # ---------
   def factorial(n) :
      if n == 1 :
         return 1
      return n * factorial(n-1)

Indent
******
The :ref:`indent-name` is calculated before removing the special character
and its white space.

Example
*******
:ref:`comment_ch_example-name`

{xrst_end comment_ch_cmd}
"""
# ----------------------------------------------------------------------------
import re
import xrst
#
# pattern
pattern = dict()
# need \{xrst_comment_ch so it does not match comment_ch command
pattern['error']      = re.compile( r'[^\\]\{xrst_comment_ch[^a-z]' )
pattern['comment_ch'] = xrst.pattern['comment_ch']
#
# Returns the beginning of line comment character for a file.
#
# Comment Character:
# The comment character is specified by \{xrst_comment_ch ch} where ch
# is a single character after leading and trailing white space is removed.
#
# data_in:
# is the data for this page.
#
# data_out:
# is a copy of data_in with the comment command removed.
#
# file_name:
# is the name of this file (used for error reporting).
#
# page_name:
# is the page name (used for error reporting)
#
# comment_ch:
# is a the comment character for this file. It is None when the
# is no comment character command for the file.
#
# data_out, comment_ch =
def comment_ch_command(data_in, file_name, page_name) :
   assert type(data_in) == str
   assert type(file_name) == str
   assert type(page_name) == str
   #
   # m_obj
   m_obj   = pattern['comment_ch'].search(data_in)
   if not m_obj :
      m_error = pattern['error'].search(data_in)
      if m_error :
         msg  = f'syntax_error in xrst comment_ch command'
         line = data_in[: m_error.start() + 1].count('\n') + 1
         xrst.system_exit(
            msg,
            file_name = file_name,
            page_name = page_name,
            m_obj     = m_error,
            data      = data_in,
         )
      #
      # data_out
      data_out = data_in
      #
      # comment_ch
      comment_ch = None
   else :
      #
      # comment_ch
      comment_ch = m_obj.group(2)
      line       = data_in[: m_obj.start() ].count('\n') + 1
      if len( comment_ch ) != 1 :
         msg = 'Expected a single character argument to comment_ch command'
         xrst.system_exit(
            msg,
            file_name = file_name,
            page_name = page_name,
            m_obj     = m_obj,
            data      = data_in,
         )
      if comment_ch in '.:]' :
         msg  = f'Cannot use {comment_ch} as character in comment_ch command\n'
         xrst.system_exit(msg, file_name=file_name, line=line)
      #
      # m_rest
      data_rest  = data_in[ m_obj.end() : ]
      m_rest     = pattern['error'].search(data_rest)
      if m_rest :
         line = data_in[: m_obj.end() + m_rest.start() ].count('\n') + 1
         msg = 'There are multiple comment_ch commands in this file'
         xrst.system_exit(
            msg,
            file_name = file_name,
            page_name = page_name,
            m_obj     = m_rest,
            data      = data_in,
         )
      #
      # data_out
      data_out= data_in[: m_obj.start()] + data_in[ m_obj.end() :]
      #
   #
   # check_syntax_error
   xrst.check_syntax_error(
      command_name  = 'comment_ch',
      data          = data_out,
      file_name     = file_name,
      page_name     = page_name,
   )
   #
   return data_out, comment_ch
