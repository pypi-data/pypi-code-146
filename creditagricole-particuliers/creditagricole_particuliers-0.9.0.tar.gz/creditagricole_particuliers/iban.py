import json
import requests

class Iban:
    def __init__(self, session, compteIdx, grandeFamilleCode, numeroCompte):
        """class init"""
        self.session = session
        self.compteIdx = compteIdx
        self.numeroCompte = numeroCompte
        self.grandeFamilleCode = grandeFamilleCode
        self.iban = {}
        self.ibanCode = "-"

        self.get_iban_data()

    def __str__(self):
        """stre representation"""
        return f"Iban[compte={self.numeroCompte}, code={self.ibanCode}]"

    def get_iban_data(self):
        """get iban"""
        url = "%s" % self.session.url
        url += "/%s/particulier/operations/" % self.session.regional_bank_url
        url += "operations-courantes/editer-rib/"
        url += "jcr:content.ibaninformation.json?compteIdx=%s&grandeFamilleCode=%s" % (self.compteIdx,self.grandeFamilleCode)

        r = requests.get(url=url,
                        verify=self.session.ssl_verify,
                        cookies=self.session.cookies)
        if r.status_code != 200:
            raise Exception( "[error] get accounts: %s - %s" % (r.status_code, r.text) )

        self.iban = json.loads(r.text)
        self.ibanCode = self.iban["ibanData"]["ibanData"]["ibanCode"]

    def as_json(self):
        """return as json"""
        return json.dumps(self.iban)