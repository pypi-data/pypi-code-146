# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Bradley M. Bell <bradbell@seanet.com>
# SPDX-FileContributor: 2020-23 Bradley M. Bell
# ----------------------------------------------------------------------------
"""
{xrst_begin heading_links user}

Heading Cross Reference Links
#############################

Index
*****
For each word in a heading,
a link is included in the index from the word to the heading.
In addition, each word is added to the html keyword meta data
next to the page heading.

Labels
******
A cross reference label is defined for linking
from anywhere to a heading. The details of how to use
these labels are described below.

Level Zero
==========
Each :ref:`page<begin_cmd@page>` can have only one header at
the first level which is a title for the page.

page_name
---------
The input below will display the page name as the linking text:

  ``:ref:`` \` *page_name* ``-name`` \`

page_title
----------
The input below will display the page title as the linking text:

    ``:ref:`` \` *page_name* ``-title`` \`

Linking Text
------------
You can also explicitly choose the linking text using:

   ``:ref:`` \` *linking_text* ``<`` *page_name* ``-name>`` \`


Other Levels
============
The label for linking a heading that is not at level zero is the label
for the heading directly above it plus an at sign character :code:`@`,
plus the conversion for this heading.
These labels use the *page_name* for level zero,
without the ``-name`` or ``--title`` at the end.

Heading@To@Label
================
The conversion of a heading to a label
removes all backslashes ``\`` and changes at signs ``@``
to dashes ``-``.

For example, the label for the heading above is

   :ref:`heading_links@Labels@Heading-To-Label
   <heading_links@Labels@Heading-To-Label>`

The label corresponding to a header is used to reference the heading
using the ``:ref:`` role.

Label To Anchor
===============
There is a further conversion to create the
HTML anchor corresponding to a label.  To be specific:

1. The anchor is converted to lower case.
3. Characters that are not letters or decimal digits are converted to dashes.
4. Multiple dashes are converted to one dash.
5. The beginning of the anchor is trimmed until a letter is reached.
6. The end of the anchor is trimmed until a letter or digit is reached.

If for one page, these anchors are not unique, xrst reports an error.


Discussion
==========
#. Note that for level zero one uses the *page_name* and not the
   title; e.g., in the example above one uses ``heading_links``
   and not ``Heading Cross Reference Links`` .
#. The ``@`` and not ``.`` character is used to separate levels
   because the ``.`` character is often used in titles and
   page names; e.g. :ref:`auto_file@conf.py`.
#. The xrst automatically generated labels end in ``-name`` , ``-title`` ,
   or have a ``@`` character in them. Other labels, that you create using
   rst commands, should not satisfy this condition
   (and hence are easy to distinguish).
#. Including all the levels above a heading in its label may seem verbose,
   but it avoids ambiguity when the same heading appears twice in one page.
   For example, this link to the project name
   :ref:`config_file@project_name@Default`
   which is one of many Default headings on that page.
   This also helps keep the links up to date.
   If a heading changes, all the links to that heading, and all the
   headings below it,  will break.  This identifies the links that should be
   checked to make sure they are still valid.
#. It is an error for two headings have the same HTML anchor.
   This makes the html links to a heading valid as long as its label
   does not change. This is useful when posting the answer to a questions
   using a link to a particular heading.

Example
*******
:ref:`heading_example-name`

{xrst_end heading_links}
-------------------------------------------------------------------------------
"""
import re
import xrst
# -----------------------------------------------------------------------------
def check_anchor( label, line, file_name, page_name, previous_anchor) :
   assert type(label) == str
   assert type(line) == str
   assert type(file_name) == str
   assert type(previous_anchor) == dict
   #
   # anchor
   # convert to the following pattern: [a-z](-?[a-z0-9]+)*
   anchor = label.lower()
   anchor = re.sub( r'[^a-z0-9]', '-', anchor)
   anchor = re.sub( r'-+',        '-', anchor)
   anchor = re.sub( r'-$',        '',  anchor)
   anchor = re.sub( r'^[^a-z]*',  '',  anchor)
   if anchor == '' :
      msg  = 'The anchor correspnding to a header is empty.\n'
      msg += f'label = {label}'
      xrst.system_exit(
         msg, file_name = file_name, page_name = page_name, line = line,
      )
   #
   # check for duplicate anchor
   if anchor in previous_anchor :
      previous_line  = previous_anchor[anchor]['line']
      previous_label = previous_anchor[anchor]['label']
      msg  = 'A previous header has the same HTML anchor.\n'
      msg += f'label          = {label}\n'
      msg += f'previous_label = {previous_label}\n'
      msg += f'anchor         = {anchor}\n'
      msg += f'previous_line  = {previous_line}'
      xrst.system_exit(
         msg, file_name = file_name, page_name = page_name, line = line,
      )
      assert False, msg
   #
   # previous_anchor
   previous_anchor[anchor] = { 'line' : line, 'label' : label }
# -----------------------------------------------------------------------------
# {xrst_begin process_headings dev}
# {xrst_spell
#     bool
#     fullmatch
#     overline
#     toc
# }
# {xrst_comment_ch #}
#
# Add labels and index entries for headings
# #########################################
#
# Arguments
# *********
#
# local_toc
# =========
# is the xrst command line local_toc setting.
#
# data_in
# =======
# contains the data for a page before the headings are processed.
#
# file_name
# =========
# name of the file that contains the input data for this page.
# This is only used for error reporting.
#
# page_name
# =========
# is the name of this page.
#
# not_in_index_list
# =================
# is a list of compiled regular expressions. If pattern is in this list,
# *word* is a lower case version of a word in the heading text, and
# pattern.fullmatch( *word* ) returns a match, an index entry is not
# generated for word.
#
# Returns
# *******
#
# data_out
# ========
# is a copy of data_in with the following extra command added:
#
#  #. The index entries, and meta keyword entries (same as index),
#     and the :ref:`heading_links@Labels` for this page.
#  #. The command \\n{xrst_before_title} is placed directly before the
#     first heading for this page; i.e. its title.
#     This is makes it easy to add the page number to the heading text.
#
# page_title
# ==========
# This is the heading text in the first heading for this page.
# There can only be one heading at this level.
#
# pseudo_heading
# ==============
# This is an automatically generated heading for this page. It is intended
# to come before the page_title heading.
# It has three lines each terminated by a newline:
#
#  1. an overline line
#  2. heading text line for this page title
#  3. an underline line
#
# {xrst_code py}
def process_headings(
      local_toc, data_in, file_name, page_name, not_in_index_list
) :
   assert type(local_toc) == bool
   assert type(data_in) == str
   assert type(file_name) == str
   assert type(page_name) == str
   assert type(not_in_index_list) == list
   # {xrst_code}
   # {xrst_literal
   #  BEGIN_return
   #  END_return
   # }
   # {xrst_end process_headings}
   #
   # pattern_colon_in_label
   pattern_colon_space = re.compile( r':(\s)' )
   #
   # previous_anchor
   previous_anchor = dict()
   #
   # external_line, internal_line
   external_line, internal_line = xrst.sphinx_label(
      data_in, file_name, page_name
   )
   #
   # previous_anchor
   for label in internal_line :
      line = internal_line[label]
      check_anchor(
         label, line, file_name, page_name, previous_anchor, exteranl_line
      )
   #
   # data_out
   data_out = data_in
   #
   # punctuation
   punctuation      = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
   assert len(punctuation) == 34 - 2 # two escape sequences
   #
   # overline_used
   overline_used = set()
   #
   # found_level_one_heading
   found_level_one_heading = False
   #
   # heading_list, heading_index, heading_text, underline_text
   heading_list     = list()
   data_index       = 0
   heading_index, heading_text, underline_text = \
      xrst.next_heading(data_out, data_index, file_name, page_name)
   #
   while 0 <= heading_index :
      if 0 < heading_index :
         assert data_out[heading_index-1] == '\n'
      #
      # m_line
      m_line = xrst.pattern['line'].search(data_out, heading_index)
      #
      # overline
      index = m_line.start()
      overline = underline_text == data_out[heading_index : index]
      #
      # character
      character = underline_text[0]
      #
      # heading
      heading   = {
         'overline' : overline,
         'character': character,
         'text':      heading_text
      }
      #
      # underline_end
      underline_end = data_out.find('\n', heading_index)
      underline_end = data_out.find('\n', underline_end+1)
      if overline :
         underline_end = data_out.find('\n', underline_end+1)
      assert data_out[underline_end] == '\n'
      #
      # overline_used
      if overline :
         overline_used.add(character)
      #
      # heading_list
      if len( heading_list ) == 0 :
         # first heading in this page
         heading_list.append( heading )
      else :
         # level_zero
         level_zero = overline == heading_list[0]['overline']
         if level_zero :
            level_zero = character == heading_list[0]['character']
         if level_zero :
            msg = 'There are multiple titles for this page'
            xrst.system_exit(
               msg,
               file_name = file_name,
               page_name = page_name,
               line      = m_line.group(1),
            )
         #
         # found_level
         found_level = False
         level       = 1
         while level < len(heading_list) and not found_level :
            found_level = overline == heading_list[level]['overline']
            if found_level :
               found_level = character == heading_list[level]['character']
            if found_level :
               #
               # heading_list
               heading_list = heading_list[: level ]
               heading_list.append(heading)
            else :
               level += 1
         #
         # heading_list
         if not found_level :
            # this heading at a higher level
            heading_list.append( heading )
      #
      # label
      label = None
      for level in range( len(heading_list) ) :
         if level == 0 :
            assert page_name == page_name.replace('\\', '').replace('@', '_')
            #
            # label
            if len(heading_list) == 1 :
               label = page_name + '-title'
            else :
               label = page_name
         else :
            conversion  = heading_list[level]['text']
            conversion  = conversion.replace('\\', '')
            conversion  = conversion.replace('@',  '-')
            conversion  = pattern_colon_space.sub( '\\:\\1', conversion)
            label      += '@' + conversion
      #
      # label
      if label.endswith(':') :
         label = label[:-1] + '\\:'
      if label.startswith('_') :
         label = '\\' + label
      #
      # check external labels
      if label.lower() in external_line :
         other_line = external_line[ label.lower() ]
         msg  = 'This label has same lower case representation as anotheer\n'
         msg += 'other line = {other_line}'
         xrst.system_exit(msg, file_name = file_name, page_name = page_name)
      #
      # check_anchor
      line = m_line.group(1)
      check_anchor(label, line, file_name, page_name, previous_anchor)
      #
      # index_entries
      if len(heading_list) == 1 :
         index_entries = page_name
      else :
         index_entries = ''
      for word in heading_list[-1]['text'].lower().split() :
         skip = False
         for pattern in not_in_index_list :
            m_obj = pattern.fullmatch(word)
            if m_obj :
               skip = True
         if not skip :
            if index_entries == '' :
               index_entries = word
            else :
               index_entries += ', ' + word
      #
      # data_tmp
      # data that comes before this heading
      data_tmp   = data_out[: heading_index]
      #
      # data_tmp
      # If first level one heading and sphinx_rtd_theme,
      # put jump table command before heading
      if len(heading_list) == 2 and not found_level_one_heading :
         found_level_one_heading = True
         if local_toc :
            data_tmp += '\n.. contents::\n'
            data_tmp += 3 * ' ' + ':local:\n\n'
      #
      # data_tmp
      # add sphnix keyword, index, and label commnds
      cmd  = ''
      if index_entries != '' :
            cmd += '.. meta::\n'
            cmd += 3 * ' ' + ':keywords: ' + index_entries + '\n\n'
            cmd += '.. index:: '           + index_entries + '\n\n'
      cmd += '.. _' + label + ':\n\n'
      data_tmp  += cmd
      #
      # data_tmp
      # If level zero, put page number command just before heading
      if len(heading_list) == 1 :
         data_tmp += '{xrst_before_title}\n'
      #
      # data_tmp
      # add data from stat to end of heading
      assert data_out[underline_end] == '\n'
      data_tmp  += data_out[heading_index : underline_end]
      #
      # data_out
      data_right = data_out[underline_end : ]
      data_out   = data_tmp + data_right
      #
      # next heading
      data_index = len(data_tmp) + 1
      heading_index, heading_text, underline_text = \
         xrst.next_heading(data_out, data_index, file_name, page_name)
   #
   if len(heading_list) == 0 :
      msg = 'There are no headings in this page'
      xrst.system_exit(msg, file_name=file_name, page_name=page_name)
   #
   # pseudo_heading
   i = 0
   while punctuation[i] in overline_used :
      i += 1
      if i == len(punctuation) :
         msg  = 'more than ' + len(punctuation) - 1
         msg += ' overlined heading levels'
         xrst.system_exit(
            msg, file_name=file_name, page_name=page_name
         )
   line           = len(page_name) * punctuation[i] + '\n'
   pseudo_heading = line + page_name + '\n' + line + '\n'
   #
   # page_title
   page_title = heading_list[0]['text']
   #
   # BEGIN_return
   assert type(data_out) == str
   assert type(page_title) == str
   assert type(pseudo_heading) == str
   #
   return data_out, page_title, pseudo_heading
   # END_return
