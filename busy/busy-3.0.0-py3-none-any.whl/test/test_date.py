
from unittest import TestCase
from tempfile import TemporaryDirectory
from pathlib import Path
from unittest import mock
from io import StringIO
from datetime import date as Date
import unittest

import busy.dateparser

class TestDate(TestCase):

    @mock.patch('busy.dateparser.today', lambda : Date(2019,2,11))
    def test_today(self):
        t = busy.dateparser.relative_date('today')
        self.assertEqual(t, Date(2019, 2, 11))

