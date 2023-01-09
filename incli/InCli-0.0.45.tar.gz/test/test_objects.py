import unittest
from InCli.SFAPI import restClient,query


class Test_Objects(unittest.TestCase):
    def test_limits(self):
        restClient.init('DEVNOSCAT2')
        action = '/services/data/v51.0/limits'
        res = restClient.callAPI(action)

        print()


    def test_id(self):
        restClient.init('DEVNOSCAT2')
        action = '/services/data/v51.0'
        res = restClient.callAPI(action)

        print()

    def test_id(self):
        restClient.init('DEVNOSCAT2')
        action = '/services/data/v51.0'
        res = restClient.callAPI(action)
        for key in res.keys():
            print()
            action = res[key]
            res1 = restClient.callAPI(action)
            print(action)
            print(res1)

        print()