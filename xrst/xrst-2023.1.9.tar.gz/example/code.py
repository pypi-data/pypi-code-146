# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Bradley M. Bell <bradbell@seanet.com>
# SPDX-FileContributor: 2020-22 Bradley M. Bell
# ----------------------------------------------------------------------------
"""
{xrst_begin code_example}

Code Command Example
####################

Factorial
*********
{xrst_code py}"""
def factorial(n) :
   if n == 1 :
      return 1
   return n * factorial(n-1)
"""{xrst_code}

Git Hash
********
{xrst_spell_off}
{xrst_code py}"""
git_hash='7c35a3ce607a14953f070f0f83b5d74c2296ef93'
"""{xrst_code}
{xrst_spell_on}

xrst_code
*********
The file below demonstrates the use of ``xrst_code`` .

xrst_spell_off, xrst_spell_on
*****************************
The file below demonstrates the use of ``xrst_spell_off``
and ``xrst_spell_on`` .

This Example File
*****************
{xrst_literal}

{xrst_end code_example}
"""
