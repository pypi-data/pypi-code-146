import requests
import json
from confapp import conf

class Get():
    def __init__(self,_apibase):
        self.apibase = _apibase

    def allprojects(self):
        result = requests.get(conf.ALYX_PLUGIN_ADDRESS+'/projects',headers= self.apibase.headers)
        if result.ok:
            result_data = result.json()
            for a in result_data:
                print(a)
    
    def project(self,_name):
        result = requests.get(conf.ALYX_PLUGIN_ADDRESS+'/projects/'+_name,headers= self.apibase.headers)
        if result.ok:
            print(result.json())

    def alldatasettypes(self):
        result = requests.get(conf.ALYX_PLUGIN_ADDRESS+'/dataset-types',headers= self.apibase.headers)
        if result.ok:
            result_data = result.json()
            for a in result_data:
                print(a)

    def datasettype(self, _name):
        result = requests.get(conf.ALYX_PLUGIN_ADDRESS+'/dataset-types/'+_name,headers= self.apibase.headers)
        if result.ok:
            print(result.json())

    
    def alldataformats(self):
        result = requests.get(conf.ALYX_PLUGIN_ADDRESS+'/data-formats',headers= self.apibase.headers)
        if result.ok:
            result_data = result.json()
            for a in result_data:
                print(a)

    def dataformat(self, _name):
        result = requests.get(conf.ALYX_PLUGIN_ADDRESS+'/data-formats/'+_name,headers= self.apibase.headers)
        if result.ok:
            print(result.json())

    def alldatasets(self):
        result = requests.get(conf.ALYX_PLUGIN_ADDRESS+'/datasets',headers= self.apibase.headers)
        if result.ok:
            result_data = result.json()
            for a in result_data:
                print(a)
    
    def dataset(self,_name):
        result = requests.get(conf.ALYX_PLUGIN_ADDRESS+'/datasets/'+_name,headers= self.apibase.headers)
        if result.ok:
            print(result.json())

    def allfiles(self):
        result = requests.get(conf.ALYX_PLUGIN_ADDRESS+'/files',headers= self.apibase.headers)
        if result.ok:
            result_data = result.json()
            for a in result_data:
                print(a)
    
    def files(self,_name):
        result = requests.get(conf.ALYX_PLUGIN_ADDRESS+'/files/'+_name,headers= self.apibase.headers)
        if result.ok:
            print(result.json())


    def alldatarepositorytypes(self):
        result = requests.get(conf.ALYX_PLUGIN_ADDRESS+'/data-repository-type',headers= self.apibase.headers)
        if result.ok:
            result_data = result.json()
            for a in result_data:
                print(a)

    def repositorytype(self, _name):
        result = requests.get(conf.ALYX_PLUGIN_ADDRESS+'/data-repository-type/'+_name,headers= self.apibase.headers)
        if result.ok:
            print(result.json())

    def alldatarepositories(self):
        result = requests.get(conf.ALYX_PLUGIN_ADDRESS+'/data-repository',headers= self.apibase.headers)
        if result.ok:
            result_data = result.json()
            for a in result_data:
                print(a)

    def datarepositoryty(self, _name):
        result = requests.get(conf.ALYX_PLUGIN_ADDRESS+'/data-repository/'+_name,headers= self.apibase.headers)
        if result.ok:
            print(result.json())

