# from unittest.case import TestCase
import json
from unittest.mock import Mock

from bs4 import BeautifulSoup
from django.test.testcases import TestCase

from tuitse.widget import KiamTsaNuaUi
from tuitse.constant import THAU_JI


class TsingHapTshiGiam(TestCase):

    def _mock_hamsik(self, tinliat):
        mock = Mock()
        mock.檢查 = json.dumps(tinliat)
        return KiamTsaNuaUi().檢查結果(mock)

    def test_nng_su(self):
        kiatko = self._mock_hamsik([
            ('好', 'hó', THAU_JI, True),
        ])
        soup = BeautifulSoup(kiatko, "html.parser")
        self.assertEqual(
            len(soup.find_all('rb')), 1
        )
