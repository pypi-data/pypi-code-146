from urllib import parse
import requests
import json

class RegionalBanks:
    def __init__(self):
        """regional banks"""
        self.url = "https://www.credit-agricole.fr"
        self.ssl_verify = True

    def by_departement(self, department):
        url = "%s/particulier/acces-cr.get-cr-by-department.json" % (self.url)
        headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        payload = {'department': "%s" % department}
        r = requests.post(url=url, 
                          data=parse.urlencode(payload),
                          headers=headers,
                          verify=self.ssl_verify)
        if r.status_code != 200:
            raise Exception( "[error] get regional bank by departement: %s - %s" % (r.status_code, r.text) )

        regionalBanks = json.loads(r.text)
        if not len(regionalBanks):
            raise Exception( "[error] get regional bank by departement code not found"  )

        return regionalBanks[0]