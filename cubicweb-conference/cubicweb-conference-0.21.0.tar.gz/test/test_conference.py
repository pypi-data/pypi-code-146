"""template automatic tests"""

from logilab.common.testlib import unittest_main

from cubicweb.devtools.testlib import AutomaticWebTest
from cubicweb.devtools.fill import ValueGenerator


class MyValueGenerator(ValueGenerator):
    def generate_Sponsor_url(self, entity, index):
        return "http://sponsor.example.com"


# necessary trick to avoid cw assertion error
class AutomaticWebTest(AutomaticWebTest):
    pass


if __name__ == "__main__":
    unittest_main()
