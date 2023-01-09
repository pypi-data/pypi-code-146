# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Bradley M. Bell <bradbell@seanet.com>
# SPDX-FileContributor: 2020-23 Bradley M. Bell
# ----------------------------------------------------------------------------
'''
{xrst_begin get_spell_checker dev}
{xrst_spell
   pyspellchecker
}

Get A Spell Checker Object
##########################

Syntax
******

| *spell_checker* = xrst.get_spell_checker(*local_words*, *package*)
| *known*   = *spell_checker*.known ( *word* )
| *suggest* = *spell_checker*.suggest ( *word* )

local_words
***********
is a list of words
(each word is a non-empty str)
that get added to the dictionary for this spell checker.
No need to add single letter words because they are considered correct
by spell_command routine.
}

package
*******
is an str equal to 'pyspellchecker' or 'enchant' .

word
****
is a word the we are either checking to see if it is correct,
or looking for a suggested spelling for.

spell_checker
*************
is the spell checking object.

known
*****
is True (False) if *word* is (is not) a correctly spelled word.

suggest
*******
if *word* is correctly spelled, *suggest* is equal to *word* .
Otherwise if *suggest* is not None, it is a suggestion
for correcting the spelling.
If *suggest* is None, the spell checker does not have a suggestion
for correcting the spelling of *word*. .


{xrst_end get_spell_checker}
'''
# -----------------------------------------------------------------------------
# remove_from_dictionary
# list of words that, if they are in the dictionary, are removed
remove_from_dictionary = [
   # BEGIN_SORT_THIS_LINE_PLUS_1
   'af',
   'anl',
   'ap',
   'av',
   'bnd',
   'bv',
   'cg',
   'conf',
   'cpp',
   'dep',
   'dir',
   'dv',
   'exp',
   'gcc',
   'hes',
   'hess',
   'ind',
   'jac',
   'len',
   'mcs',
   'meas',
   'nc',
   'nd',
   'nr',
   'op',
   'prt',
   'ptr',
   'rc',
   'rel',
   'sim',
   'std',
   'tbl',
   'thier',
   'var',
   'vec',
   'xp',
   'yi',
   # END_SORT_THIS_LINE_MINUS_1
]
# -----------------------------------------------------------------------------
# add_to_dictionary
# list of
add_to_dictionary = [
   # BEGIN_SORT_THIS_LINE_PLUS_1
   'aborts',
   'asymptotic',
   'configurable',
   'covariate',
   'covariates',
   'debug',
   'deprecated',
   'destructor',
   'exponentiation',
   'hessians',
   'html',
   'identifiability',
   'indenting',
   'initialization',
   'initialize',
   'initialized',
   'integrand',
   'integrands',
   'invertible',
   'jacobian',
   'jacobians',
   'likelihoods',
   'messaging',
   'modeled',
   'modeling',
   'multipliers',
   'optimizes',
   'partials',
   'tex',
   'piecewise',
   'subdirectory',
   'unary',
   'unicode',
   'verbose',
   'wiki',
   'wikipedia',
   'xrst',
   # END_SORT_THIS_LINE_MINUS_1
]
# -----------------------------------------------------------------------------
class py_spell_checker :
   #
   # self
   def __init__(self, local_words) :
      assert type(local_words) == list
      for word in local_words :
         assert type(word) == str
      #
      # spellchecker
      import spellchecker
      #
      # checker
      checker = spellchecker.SpellChecker(distance=1)
      #
      # checker
      remove_list = checker.known( remove_from_dictionary )
      checker.word_frequency.remove_words(remove_list)
      #
      # checker
      checker.word_frequency.load_words(add_to_dictionary)
      checker.word_frequency.load_words(local_words)
      #
      self.checker = checker
   #
   # ok
   def known(self, word) :
      assert type(word) == str
      #
      return len( self.checker.unknown( [word] ) ) == 0
   #
   # suggest
   def suggest(self, word) :
      assert type(word) == str
      #
      return self.checker.correction(word)
# -----------------------------------------------------------------------------
class enchant_spell_checker :
   #
   # self
   def __init__(self, local_words) :
      assert type(local_words) == list
      for word in local_words :
         assert type(word) == str
      #
      # enchant
      import enchant
      #
      # checker
      checker =  enchant.Dict("en_US")
      #
      # checker
      for word in remove_from_dictionary :
         checker.remove(word)
      #
      # checker
      for word in add_to_dictionary + local_words :
         checker.add(word)
      #
      self.checker = checker
   #
   # ok
   def known(self, word) :
      assert type(word) == str
      #
      return self.checker.check(word)
   #
   # suggest
   def suggest(self, word) :
      assert type(word) == str
      #
      suggest_list =  self.checker.suggest(word)
      if len(suggest_list) == 0 :
         return None
      return suggest_list[0]
# -----------------------------------------------------------------------------
def get_spell_checker(local_words, package) :
   if package == 'pyspellchecker' :
      return py_spell_checker(local_words)
   else :
      assert package == 'pyenchant'
      return enchant_spell_checker(local_words)
