# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Bradley M. Bell <bradbell@seanet.com>
# SPDX-FileContributor: 2020-23 Bradley M. Bell
# ----------------------------------------------------------------------------
import re
import xrst
#
# pattern_toc
pattern_toc = re.compile(
   r'\n{xrst_TOC_(hidden|list|table)}\n'
)
#
# patttern_rst_extension
pattern_rst_extension = re.compile( r'\.rst$' )
# ----------------------------------------------------------------------------
# {xrst_begin process_children dev}
# {xrst_spell
#     len
#     toc
#     toctree
# }
# {xrst_comment_ch #}
#
# Add child information to a page
# ###############################
#
# Arguments
# *********
#
# data_in
# =======
# is the data for this page after the toc_command function has processed
# the toc commands.
#
# list_children
# =============
# is a list of the page names for the children of this page.
# If this list is empty, data_out is equal to data_in.
#
# Returns
# *******
#
# data_out
# ========
# The return value data_out has the child information added.
#
#  #. A hidden table of contents (toctree) for the children is added at the
#     end of data_out.
#  #. If the TOC command in data_in is {xrst_TOC_list} or {xrst_TOC_table},
#     the corresponding links will replace the command.
#  #. If the child command is {xrst_TOC_hidden}, the command is removed
#     and no table of links is added.
#  #. If there is no TOC command and list_children is non-empty,
#     the toc_table style is used for the links to the children which are
#     placed at the end of the data_out (before the toctree).
#
# {xrst_code py}
def process_children(
   page_name,
   data_in,
   list_children,
) :
   assert type(page_name) == str
   assert type(data_in) == str
   assert type(list_children) == list
   if len(list_children) > 0 :
      assert type(list_children[0]) == str
   # {xrst_code}
   # {xrst_literal
   #  BEGIN_return
   #  END_return
   # }
   # {xrst_end process_children}
   #
   if len(list_children) == 0 :
      m_child = pattern_toc.search(data_in)
      assert m_child is None
      return data_in
   #
   # data_out
   data_out = data_in
   #
   # m_child
   m_child = pattern_toc.search(data_out)
   #
   # page_has_child_command
   page_has_child_command =  m_child != None
   if page_has_child_command :
      #
      # type of toc command
      toc_type = m_child.group(1)
      #
      # There chould be at most one toc command per page created by
      # the xrst.child_command routine
      m_tmp = pattern_toc.search(data_in, m_child.end())
      assert m_tmp == None
      #
      # cmd
      if toc_type ==  'list' :
         cmd = '\n\n'
         for child in list_children :
            cmd += '-  :ref:`' + child + '-title`\n'
         cmd += '\n\n'
      elif toc_type == 'table' :
         cmd  = '\n\n'
         cmd += '.. csv-table::\n'
         cmd += '   :header:  "Name", "Title"\n'
         cmd += '   :widths: auto\n\n'
         for child in list_children :
            cmd += '   "' + child + '"'
            cmd += ', :ref:`' + child + '-title`\n'
      else :
         assert toc_type == 'hidden'
         cmd = '\n'
      #
      # data_out
      data_tmp = data_out[: m_child.start()]
      data_tmp += cmd
      data_tmp += data_out[m_child.end() :]
      data_out  = data_tmp
   #
   # -----------------------------------------------------------------------
   if data_out[-1] != '\n' :
      data_out += '\n'
   #
   # data_out
   # If there is no toc command in this page, automatically generate
   # links to the child pages at the end of the page.
   if not page_has_child_command :
      data_out += '.. csv-table::\n'
      data_out += '   :header: "Child", "Title"\n'
      data_out += '   :widths: 20, 80\n\n'
      for child in list_children :
         data_out += '   "' + child + '"'
         data_out += ', :ref:`' + child + '-title`\n'
      data_out += '\n'
   #
   # data_out
   # put hidden toctree at end of page
   toctree  = '\n.. toctree::\n'
   toctree += '   :maxdepth: 1\n'
   toctree += '   :hidden:\n\n'
   for child in list_children :
      entry    = pattern_rst_extension.sub('', child)
      toctree += '   ' + entry + '\n'
   data_out = data_out + toctree
   #
   # BEGIN_return
   assert type(data_out) == str
   #
   return data_out
   # END_return
