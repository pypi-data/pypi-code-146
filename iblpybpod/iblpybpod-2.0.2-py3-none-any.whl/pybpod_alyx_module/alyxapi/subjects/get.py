import requests
import json
from confapp import conf

#self.apibase.addr + '/subjects' = conf.ALYX_PLUGIN_ADDRESS+'/subjects'

class Get():

    def __init__(self,_apibase):
        self.apibase = _apibase
        

    def allsubjects(self):
        result = requests.get(self.apibase.addr + '/subjects',headers=self.apibase.headers)
        if result.ok:
            result_data = result.json()
            return result_data
            
        return None

    
    def usersubjects(self, username):
        result = requests.get(self.apibase.addr + '/subjects?responsible_user=' + username, headers=self.apibase.headers)
        if result.ok:
            result_data = result.json()
            return result_data
            
        return None


    def bynickname(self, name):
        result = requests.get(self.apibase.addr + '/subjects'+'/'+name, headers=self.apibase.headers)
        if result.ok:
            result_data = result.json()
            return result_data

    def alive(self, _alive):
        _data = dict(alive= _alive)
        result = requests.get(self.apibase.addr + '/subjects',headers= self.apibase.headers,data = _data)
        if result.ok:
            
            print(result.json())

    def stock(self, _stock):
        _data = dict(stock= _stock)
        result = requests.get(self.apibase.addr + '/subjects',headers= self.apibase.headers,data = _data)
        if result.ok:
            
            print(result.json())
    
    def water_restircted(self, _water_restircted):
        _data = dict(water_restircted= _water_restircted)
        result = requests.get(self.apibase.addr + '/subjects',headers= self.apibase.headers,data = _data)
        if result.ok:
            
            print(result.json())

    def responsible_user(self, _responsible_user):
        _data = dict(responsible_user= _responsible_user)
        result = requests.get(self.apibase.addr + '/subjects',headers= self.apibase.headers,data = _data)
        rdata = []
        if result.ok:
            rd = result.json()
            for r in rd:
                if r['responsible_user'] == _responsible_user:
                    rdata.append(r)
        print(rdata)
        print(rd)
