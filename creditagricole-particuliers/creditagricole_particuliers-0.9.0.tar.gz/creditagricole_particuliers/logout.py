import requests

class Logout:
    def __init__(self, session):
        """logout class"""
        self.session = session
        self.logout()
        
    def logout(self):
        """logout from remote"""
        url += "%s" % self.session.url
        url += "/%s/particulier.npc.logout.html?resource=" % self.session.regional_bank_url
        url += "/content/ca/cr866/npc/fr/particulier.html"
        r = requests.get(url=url,
                         verify=self.session.ssl_verify,
                         cookies=self.session.cookies)
        if r.status_code != 200:
            raise Exception( "[error] logout: %s - %s" % (r.status_code, r.text) )