import requests
import json
from confapp import conf

ENDPOINT = conf.ALYX_PLUGIN_ADDRESS+'/subjects'

class Post():

    def __init__(self,_apibase):
        self.apibase = _apibase     

    
    def newsubject(self, _nickname, _responsible_user, _birth_date = None, _death_date = None, _species = None, _sex = None, _litter = None, _strain = None, _line = None, _description = None, _genotype = None):
        _data = dict(nickname = _nickname,
                    responsible_user = _responsible_user,
                    birth_date = _birth_date,
                    death_date = _death_date,
                    species = _species,
                    sex = _sex,
                    litter = _litter,
                    strain = _strain,
                    line = _line,
                    description = _description,
                    genotype = _genotype)

        print(_data)

        #requests.post(ENDPOINT,headers = self.apibase.headers, data= _data)

    def updatesubject(self, _nickname, _responsible_user, _birth_date = None, _death_date = None, _species = None, _sex = None, _litter = None, _strain = None, _line = None, _description = None, _genotype = None):
        _data = dict(nickname = _nickname,
                    responsible_user = _responsible_user,
                    birth_date = _birth_date,
                    death_date = _death_date,
                    species = _species,
                    sex = _sex,
                    litter = _litter,
                    strain = _strain,
                    line = _line,
                    description = _description,
                    genotype = _genotype)

        print(_data)

        #requests.patch(ENDPOINT+'/'+_nickname,headers = self.apibase.headers, data= _data)
