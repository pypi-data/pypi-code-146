## $Id: test_textlinechoice.py 7811 2012-03-08 19:00:51Z uli $
##
## Copyright (C) 2011 Uli Fouquet & Henrik Bettermann
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##
"""Test TextLineChoice
"""
import unittest
from zope.interface import implements, directlyProvides
from zope.schema import vocabulary
from zope.schema.interfaces import (
    InvalidValue, ValidationError,
    IVocabulary, ISource, IContextSourceBinder,)
from zope.schema.tests.test_strfield import TextLineTest
from waeup.kofa.schema import TextLineChoice

# Define some helper functions, classes, vars for tests
class DummyRegistry(vocabulary.VocabularyRegistry):
    def get(self, object, name):
        v = SampleVocabulary()
        v.object = object
        v.name = name
        return v

class SampleTerm(object):
    pass

SAMPLE_VALUES = [u'a', u'b', u'c', u'd']
class SampleVocabulary(object):
    implements(IVocabulary)

    def __iter__(self):
        return iter([self.getTerm(x) for x in SAMPLE_VALUES])

    def __contains__(self, value):
        return value in SAMPLE_VALUES
        return 0 <= value < 10

    def __len__(self):
        return len(SAMPLE_VALUES)

    def getTerm(self, value):
        if value in self:
            t = SampleTerm()
            t.value = value
            t.upper = value.upper() #2 * value
            return t
        raise LookupError("no such value: %r" % value)

class LetterASource(object):
    # A source that contains all strings with letter 'a'
    implements(ISource)
    required_letter = 'a'
    def __contains__(self, value):
        return self.required_letter in value
letter_a_source = LetterASource()

def letter_source_binder(context):
    source = LetterASource()
    source.required_letter = context.req_letter
    return source
directlyProvides(letter_source_binder, IContextSourceBinder)

class SampleContext(object):
    req_letter = 'b'



class TextLineChoiceAsTextLineTest(TextLineTest):
    # Tests to guarantee TextLine like behaviour of TextLineChoice
    # i.e. make sure that a TextLineChoice can everything a TextLine can
    _Field_Factory = TextLineChoice

class TextLineChoice_Values_Tests(unittest.TestCase):
    # Tests to guarantee values support
    def test_create_vocabulary(self):
        choice = TextLineChoice(values=[1, 3])
        self.assertEqual([term.value for term in choice.vocabulary], [1, 3])

    def test_validate_string(self):
        choice = TextLineChoice(values=[u'a', u'c'])
        choice.validate(u'a')
        #choice.validate('c')
        choice.validate(u'c')
        self.assertRaises(InvalidValue, choice.validate, u'd')

    def test_validate_strings(self):
        choice = TextLineChoice(values=[u'foo', u'bar'])
        choice.validate(u'foo')
        choice.validate(u'bar')
        choice.validate(u'bar')
        self.assertRaises(InvalidValue, choice.validate, u'baz')

class TextLineChoice_Vocabulary_Tests(unittest.TestCase):
    # Tests of the TextLineChoice Field using vocabularies.
    # Most tests were copied (slightly modified) from zope.schema.tests.

    def setUp(self):
        vocabulary._clear()

    def tearDown(self):
        vocabulary._clear()

    def check_preconstructed(self, cls, okval, badval):
        v = SampleVocabulary()
        field = cls(vocabulary=v)
        self.assert_(field.vocabulary is v)
        self.assert_(field.vocabularyName is None)
        bound = field.bind(None)
        self.assert_(bound.vocabulary is v)
        self.assert_(bound.vocabularyName is None)
        bound.default = okval
        self.assertEqual(bound.default, okval)
        self.assertRaises(ValidationError, setattr, bound, "default", badval)

    def test_preconstructed_vocabulary(self):
        self.check_preconstructed(TextLineChoice, u'a', u'z')

    def check_constructed(self, cls, okval, badval):
        vocabulary.setVocabularyRegistry(DummyRegistry())
        field = cls(vocabulary="vocab")
        self.assert_(field.vocabulary is None)
        self.assertEqual(field.vocabularyName, "vocab")
        o = object()
        bound = field.bind(o)
        self.assert_(isinstance(bound.vocabulary, SampleVocabulary))
        bound.default = okval
        self.assertEqual(bound.default, okval)
        self.assertRaises(ValidationError, setattr, bound, "default", badval)

    def test_constructed_vocabulary(self):
        self.check_constructed(TextLineChoice, u'a', u'z')

    def test_create_vocabulary(self):
        vocabulary.setVocabularyRegistry(DummyRegistry())
        field = TextLineChoice(vocabulary="vocab")
        o = object()
        bound = field.bind(o)
        self.assertEqual([term.value for term in bound.vocabulary],
                         SAMPLE_VALUES)

    def test_undefined_vocabulary(self):
        choice = TextLineChoice(vocabulary="unknown")
        self.assertRaises(ValueError, choice.validate, u"value")

class TextLineChoice_Source_Tests(unittest.TestCase):
    # Tests of the TextLineChoice Field using sources.

    def test_simple_source(self):
        choice = TextLineChoice(__name__='astring', source=letter_a_source)
        bound = choice.bind(object())
        self.assertEqual(bound.vocabulary, letter_a_source)
        return

    def test_validate_simple_source(self):
        choice = TextLineChoice(__name__='astring', source=letter_a_source)
        bound = choice.bind(object())
        bound.validate(u'string_with_letter_a')
        self.assertRaises(
            InvalidValue, bound.validate, u'other_string')
        return

    def test_contextual_source(self):
        # make sure we can pass contextual sources
        choice = TextLineChoice(__name__='astring', source=letter_source_binder)
        bound = choice.bind(SampleContext()) # requires 'b' instead of 'a'
        self.assertTrue(isinstance(bound.vocabulary, LetterASource))
        self.assertTrue(bound.vocabulary is not letter_a_source)
        return

    def test_validate_contextual_source(self):
        # make sure the values from context are considered
        choice = TextLineChoice(__name__='astring', source=letter_source_binder)
        bound = choice.bind(SampleContext()) # requires 'b' instead of 'a'
        bound.validate(u'string_with_letter_b')
        self.assertRaises(
            InvalidValue, bound.validate, u'other_string') # no 'b'
        return

def test_suite():
    # We must define a test suite as we do not want the imported
    # TextLineTest to be collected by testrunner.
    return unittest.TestSuite((
        unittest.makeSuite(TextLineChoiceAsTextLineTest),
        unittest.makeSuite(TextLineChoice_Values_Tests),
        unittest.makeSuite(TextLineChoice_Vocabulary_Tests),
        unittest.makeSuite(TextLineChoice_Source_Tests),
        ))
