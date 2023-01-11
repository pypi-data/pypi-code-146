## $Id: test_vocabularies.py 16812 2022-02-16 15:50:47Z henrik $
##
## Copyright (C) 2012 Uli Fouquet & Henrik Bettermann
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
import unittest
from waeup.kofa.students.vocabularies import (
    StudyLevelSource, levels_from_range,
    )
from waeup.kofa.university.certificate import Certificate

class HelperTests(unittest.TestCase):

    def test_levels_from_range(self):
        # default
        self.assertEqual(
            levels_from_range(),
            [10,
             100, 110, 120, 200, 210, 220, 300, 310, 320, 400, 410, 420,
             500, 510, 520, 600, 610, 620, 700, 710, 720, 800, 810, 820,
             900, 910, 920, 999, 1000,])
        # edge-case: level 10
        self.assertEqual(
            levels_from_range(10, 10), [10])
        # edge-case: level 999
        self.assertEqual(
            levels_from_range(999, 10), [999])
        self.assertEqual(
            levels_from_range(10, 999), [999])
        self.assertEqual(
            levels_from_range(10, 200),
            [10, 100, 110, 120, 200, 210, 220, 300, 310, 320])
        self.assertEqual(
            levels_from_range(100, 300),
            [100, 110, 120, 200, 210, 220, 300, 310, 320, 400, 410, 420])
        self.assertEqual(
            levels_from_range(800, 900),
            [800, 810, 820, 900, 910, 920])
        return

class FakeStudyCourse(object):

    def __init__(self):
        cert = Certificate(code="CERT1")
        cert.start_level = 100
        cert.end_level = 500
        self.certificate = cert

class VocabularyTests(unittest.TestCase):

    def test_studylevelsource(self):
        studycourse = FakeStudyCourse()
        studylevelsource = StudyLevelSource().factory
        values = studylevelsource.getValues(studycourse)
        self.assertEqual(values, [0, 100, 110, 120, 200, 210, 220, 300, 310, 320,
            400, 410, 420, 500, 510, 520, 600, 610, 620])
        # All titles do exist
        titles = [studylevelsource.getTitle(studycourse, value)
            for value in values]
        self.assertEqual(len(titles), 19)
        # Unfortunately, unittests don't know about internationalization
        self.assertEqual(studylevelsource.getTitle(studycourse, None),
            'Error: level id ${value} out of range')
        self.assertEqual(studylevelsource.getTitle(studycourse, 0),
            'Level Zero')
        self.assertEqual(studylevelsource.getTitle(studycourse, 1),
            'Error: level id ${value} out of range')
        self.assertEqual(studylevelsource.getTitle(studycourse, 10),
            'Error: level id ${value} out of range')
        self.assertEqual(studylevelsource.getTitle(studycourse, 100),
            '100 (Year 1)')
        self.assertEqual(studylevelsource.getTitle(studycourse, 110),
            '${title} on 1st probation')
        self.assertEqual(studylevelsource.getTitle(studycourse, 120),
            '${title} on 2nd probation')
        self.assertEqual(studylevelsource.getTitle(studycourse, 500),
            '500 (Year 5)')
        self.assertEqual(studylevelsource.getTitle(studycourse, 600),
            '${title} 1st spillover')
        self.assertEqual(studylevelsource.getTitle(studycourse, 610),
            '${title} 2nd spillover')
        self.assertEqual(studylevelsource.getTitle(studycourse, 620),
            '${title} 3rd spillover')
        self.assertEqual(studylevelsource.getTitle(studycourse, 630),
            'Error: level id ${value} out of range')
        self.assertEqual(studylevelsource.getTitle(studycourse, 700),
            'Error: level id ${value} out of range')
        # Now we modify the certificates to be a pure pre-studies
        # course
        studycourse.certificate.start_level = 10
        studycourse.certificate.end_level = 10
        values = studylevelsource.getValues(studycourse)
        self.assertEqual(values, [0, 10])
        titles = [studylevelsource.getTitle(studycourse, value)
            for value in values]
        self.assertEqual(len(titles), 2)
        self.assertEqual(studylevelsource.getTitle(studycourse, 10),
            'Pre-Studies')
        self.assertEqual(studylevelsource.getTitle(studycourse, 100),
            'Error: level id ${value} out of range')
        self.assertEqual(studylevelsource.getTitle(studycourse, 200),
            'Error: level id ${value} out of range')
        # Finally we modify the certificate to be a mixed course,
        # starting with pre-studies.
        studycourse.certificate.end_level = 200
        values = studylevelsource.getValues(studycourse)
        self.assertEqual(values, [0, 10, 100, 110, 120,
            200, 210, 220, 300, 310, 320])
        titles = [studylevelsource.getTitle(studycourse, value)
            for value in values]
        self.assertEqual(len(titles), 11)
