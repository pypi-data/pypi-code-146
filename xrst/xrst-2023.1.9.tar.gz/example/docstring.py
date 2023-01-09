# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Bradley M. Bell <bradbell@seanet.com>
# SPDX-FileContributor: 2020-22 Bradley M. Bell
# ----------------------------------------------------------------------------
def factorial(n) :
   """
{xrst_begin docstring_example}
{xrst_spell
   docstring
}

Docstring Example
#################

Discussion
**********
This example demonstrates using a python docstring to document a function.
see :ref:`indent_example@Python Docstring`
for an example of an indented docstring.

This Example File
*****************
{xrst_literal}

{xrst_end docstring_example}
   """
   if n == 1 :
      return 1
   return n * factorial(n-1)
