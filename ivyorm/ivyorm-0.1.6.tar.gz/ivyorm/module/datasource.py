from .util import Console
from .validation import Validation

from importlib import import_module

from dictionary import Dictionary

class Datasource(Dictionary, Validation):

    queryParts:dict = {
        'field':{},
        'pagination':{},
        'where':{},
        'order':{},
        'action':'',
        'table': '',
        'database': '',
        'pk':{},
        'data':{}
    }
    
    @property
    def data(self):
        return self._data


    @data.setter
    def data(self, dataDict):
        dataList: list = [*dataDict]
        self.queryParts["field"] = Validation.fieldExists(self, dataList)
        
        dataDict, error = Validation.check(self, dataDict)

        
        self.error = error

        for field in self.queryParts["field"]:
            self._data[field] = dataDict[field]
            self.queryParts['data'][field] = dataDict[field]


    def __init__(self, schemaFile):
        Console.info('Datasource instance.................')
        super().__init__(schemaFile)
        
        database_type = self.database_spec['type']

        self.db = import_module(f'module.connection.{database_type}').Connection()
        self._data = {}
        self.error = {}
        self.id: any

        self.database(self.database_spec['name'])
        self.table(self.table_spec['name'])
        self.pk(self.table_spec['pk'])
        

    def select(self):
        self.queryParts['action'] = 'select'

        if not self.error:

            success, result = self.db.query(self.queryParts)
            self._data = result
            return success
            

        return False


    def insert(self, data: dict = None):
        self.queryParts['action'] = 'insert'

        if data:
            self.data = data

        if not self.error:
            success, result = self.db.query(self.queryParts)
            self.id = result[0][self.queryParts['pk'][0].lower()]
            self.data[ self.queryParts['pk'][0] ] = self.id
            return success

        return False


    def field(self, fields: list):
        Console.info('field')
        self.queryParts["field"] = Validation.fieldExists(self, fields)
        return self
    

    def order(self, fields):
        Console.info('order')
        return self


    def where(self, fields):
        Console.info('where')
        return self


    def limit(self, fields):
        Console.info('limit')
        return self    


    def database(self, database: str):
        self.queryParts["database"] = database


    def table(self, table: str):
        self.queryParts["table"] = table


    def pk(self, pkList: list):
        self.queryParts['pk'] = pkList


    def object(self, object):
        self.table(object)


    def create(self):
        self.queryParts["action"] = 'create'

        fields = {}
        for field in self.field_spec:
            fields[field] = self.field_spec[field]['back']

        self.queryParts["field"] = fields
        self.db.query(self.queryParts)


    def drop(self):
        self.queryParts["action"] = 'drop'
        self.db.query(self.queryParts)