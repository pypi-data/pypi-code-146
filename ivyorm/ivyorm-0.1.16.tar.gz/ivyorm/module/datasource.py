from .util import Console
from .validation import Validation

from importlib import import_module

from .dictionary import Dictionary

class Datasource(Dictionary, Validation):

    queryParts:dict = {
        'field':{},
        'pagination':{},
        'where':[],
        'order':[],
        'action':'',
        'table': '',
        'database': '',
        'pk':{},
        'data':[]
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

        self.db = import_module(f'.module.connection.{database_type}', package='ivyorm').Connection()
        self._data = {}
        self.error = {}
        self.id: any

        self.field(self.field_spec.keys())
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
    
    '''
    Expects a list of lists
    '''
    def order(self, fieldArr: list):
        for field, direction in fieldArr:
            
            if not Validation.fieldExists(self, field):
                continue

            if direction not in ['DESC','desc','DSC','dsc','ASC','asc']:
                continue

            stuff_to_add = [field, direction]
            self.queryParts["order"].append(stuff_to_add)

        return self


    def where(self, fieldArr: list):
        Console.info('where')

        '''
        fieldArr is a list of lists, these sub lists will at minimum contain 2 values, up to 4 values
        we access the 3rd and 4th value with *args, but need to test for them and assign defaults if
        they don't exist
        '''
        for field, value, *args in fieldArr:
            operation = '='
            group_operation = 'AND'
            if args:
                if len(args) == 1:
                    tmp = super().translate(args[0])
                    if tmp:
                        operation = tmp
                    else:
                        Console.warn(f'Operation symbol {args[0]} not found. Defaulting to {operation}')

                if len(args) == 2:
                    tmp = super().translate(args[1])
                    if tmp:
                        group_operation = tmp
                    else:
                        Console.warn(f'Group operation symbol {args[1]} not found. Defaulting to {group_operation}')

            stuff_to_add = [field, value, operation, group_operation]
            self.queryParts["where"].append(stuff_to_add)

        return self


    def limit(self, value):
        Console.info('limit')
        self.queryParts["pagination"]["limit"] = value
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