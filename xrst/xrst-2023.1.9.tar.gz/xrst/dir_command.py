# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Bradley M. Bell <bradbell@seanet.com>
# SPDX-FileContributor: 2020-22 Bradley M. Bell
# ----------------------------------------------------------------------------
"""
{xrst_begin dir_cmd user}
{xrst_spell
   dir
}

Converting Sphinx Command File Names
####################################

Syntax
******
``\{xrst_dir`` *file_name* ``}``

Purpose
*******
Sphinx commands that use file names must specify the file
relative to the :ref:`config_file@directory@rst_directory` .
The xrst dir command converts a file name relative to the
:ref:`config_file@directory@project_directory` to be relative to the
:ref:`config_file@directory@rst_directory` .

file_name
*********
Is a file name relative to the project directory.
The entire command gets replaced by a name for the same file
relative to the rst directory.
Leading and trailing white space in *file_name* is ignored.

Example
*******
:ref:`dir_example-name`

{xrst_end dir_cmd}
"""
# ----------------------------------------------------------------------------
import re
import os
import xrst
#
# {xrst_begin dir_cmd_dev dev}
# {xrst_spell
#     dir
# }
# {xrst_comment_ch #}
#
# Convert File Names to be Relative to the RST Directory
# ######################################################
#
# Arguments
# *********
#
# data_in
# =======
# is the data for this page.
#
# rst2project_dir
# ===============
# is a relative path from the :ref:`config_file@directory@rst_directory`
# to the :ref:`config_file@directory@project_directory` .
#
# Returns
# *******
#
# data_out
# ========
# The return data_out is a copy of data_in except that all the occurrences of
# {xrst_dir file_name} have been converted to the file name
# relative to the rst directory.
#
# {xrst_code py}
def dir_command(data_in, rst2project_dir) :
   assert type(data_in) == str
   assert type(rst2project_dir) == str
   # {xrst_code}
   # {xrst_literal
   #  BEGIN_RETURN
   #  END_RETURN
   # }
   # {xrst_end dir_cmd_dev}
   #
   # data_out
   data_out = data_in
   #
   # m_dir
   m_dir  = xrst.pattern['dir'].search(data_out)
   while m_dir != None :
      #
      # data_before, data_after
      data_before  = data_out[: m_dir.start()] + m_dir.group(1)
      data_after   = data_out[m_dir.end() :]
      #
      # data_left, data_out
      file_name    = m_dir.group(2).strip()
      file_name     = os.path.join(rst2project_dir, file_name)
      data_left    = data_before + file_name
      data_out     = data_left + data_after
      #
      # m_dir
      m_dir = xrst.pattern['dir'].search(data_out, len(data_left))
   #
   # BEGIN_RETURN
   assert type(data_out) == str
   return data_out
   # END_RETURN
