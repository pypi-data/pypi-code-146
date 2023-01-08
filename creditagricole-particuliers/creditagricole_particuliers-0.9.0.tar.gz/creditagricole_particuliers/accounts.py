
import requests
import json
from datetime import datetime, timedelta

from creditagricole_particuliers import operations
from creditagricole_particuliers import iban

FAMILLE_PRODUITS = [
     {"code": 1, "familleProduit": "COMPTES"}, 
     {"code": 3, "familleProduit": "EPARGNE_DISPONIBLE"}, 
     {"code": 7, "familleProduit": "EPARGNE_AUTRE"},
]

class Account:
    def __init__(self, session, account):
        """account class"""
        self.session = session
        self.account = account
        self.numeroCompte = account["numeroCompte"]
        self.compteIdx = account["index"]
        self.grandeFamilleCode = account["grandeFamilleProduitCode"]

    def __str__(self):
        """str"""
        return f"Compte[numero={self.numeroCompte}, produit={self.account['libelleProduit']}]"
 
    def get_iban(self):
        """get iban"""
        return iban.Iban(session=self.session, 
                         compteIdx=self.compteIdx,
                         grandeFamilleCode=self.grandeFamilleCode,
                         numeroCompte=self.numeroCompte)

    def get_operations(self, date_start=None, date_stop=None, count=100):
        """get operations"""
        if date_stop is None:
            current_date = datetime.today()
            previous_date = current_date - timedelta(days=30)
            date_stop = current_date.strftime('%Y-%m-%d')
            date_start = previous_date.strftime('%Y-%m-%d')
            
        return operations.Operations(session=self.session, 
                                     compteIdx=self.compteIdx,
                                     grandeFamilleCode=self.grandeFamilleCode,
                                     date_start=date_start,
                                     date_stop=date_stop, count=count)

    def as_json(self):
        """return as json"""
        return json.dumps(self.account)

    def get_solde(self):
        """get solde"""
        if "montantEpargne" in self.account:
            return self.account["montantEpargne"]
        return self.account["solde"]

class Accounts:
    def __init__(self, session):
        """operations class"""
        self.session = session
        self.accounts_list = []
        
        self.get_accounts_per_products()

    def __iter__(self):
        """iter"""
        self.n = 0
        return self
        
    def __next__(self):
        """next"""
        if self.n < len(self.accounts_list):
            op = self.accounts_list[self.n]
            self.n += 1
            return op
        else:
            raise StopIteration

    def search(self, num):
        """search account according to the num"""
        for acc in self.accounts_list:
            if acc.numeroCompte == num:
                return acc
        raise Exception( "[error] account not found" )

    def as_json(self):
        """as json"""
        _accs = []
        for acc in self.accounts_list:
            _accs.append(acc.descr)
        return json.dumps(_accs)

    def get_accounts_per_products(self):
        """get accounts per products"""
        for f in FAMILLE_PRODUITS:
            # call operations ressources
            url = "%s" % self.session.url
            url += "/%s/particulier/operations/" % self.session.regional_bank_url
            url += "synthese/jcr:content.produits-valorisation.json/%s" % f["code"]
            r = requests.get(url=url,
                            verify=self.session.ssl_verify,
                            cookies=self.session.cookies)
            if r.status_code != 200:
                raise Exception( "[error] get accounts: %s - %s" % (r.status_code, r.text) )

            for descr in json.loads(r.text):
                self.accounts_list.append( Account(self.session, descr) )

    def get_solde(self):
        """get global solde"""
        solde = 0
        for acc in self.accounts_list:
            solde += acc.get_solde()
        return round(solde, 2)

    def get_solde_per_products(self):
        """get solde per products"""
        ret_soldes = {}
        for f in FAMILLE_PRODUITS:
            ret_soldes[f["familleProduit"]] = 0.0

        for f in FAMILLE_PRODUITS:
            for acc in self.accounts_list:
                if int(acc.grandeFamilleCode) == f["code"]:
                    ret_soldes[f["familleProduit"]] += acc.get_solde()
            ret_soldes[f["familleProduit"]] = round(ret_soldes[f["familleProduit"]], 2)

        return ret_soldes
