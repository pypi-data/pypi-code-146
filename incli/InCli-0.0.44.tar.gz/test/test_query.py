import unittest
from InCli.SFAPI import restClient,query


class Test_Query(unittest.TestCase):
    def test_query1(self):
        restClient.init('DEVNOSCAT2')
        res = query.query("select fields(all) from order limit 1")

        self.assertTrue(res['totalSize']>=0)

        print()


