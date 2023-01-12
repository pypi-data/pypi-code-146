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
    def error(self):
        return self._error

    
    @error.setter
    def error(self, errorString):
        self._error.append(errorString)


    @property
    def data(self):
        return self._data


    @data.setter
    def data(self, dataInput: dict or list):

        if type(dataInput) is dict:
            data = [dataInput]
        else:
            data = dataInput

        #dataList: list = [*dataDict]
        fieldList = [*data[0],]
        self.queryParts["field"] = Validation.fieldExists(self, fieldList)
        
        self.queryParts['data'] = []

        for row in data:
            dataDict, error = Validation.check(self, row)
        
            if error:
                self.error = error
                continue

            temp = {}
            rowData = {}
            for field in self.queryParts["field"]:
                #self._data[field] = dataDict[field]
                #self.queryParts['data'][field] = dataDict[field]
                rowData[field] = dataDict[field]
                temp[field] = dataDict[field]

            self.queryParts['data'].append(temp)
            
            self._data.append(rowData)


    def __init__(self, schemaFile, connectionInfo: dict):
        Console.info('Datasource instance.................')
        super().__init__(schemaFile)
        
        database_type = self.database_spec['type']

        self.db = import_module(f'.module.connection.{database_type}', package='ivyorm').Connection(connectionInfo)
        self._data = []
        self._error = []
        self.id: any
        self.count: int = 0


        self.field(self.field_spec.keys())
        self.database(self.database_spec['name'])
        self.table(self.table_spec['name'])
        self.pk(self.table_spec['pk'])
        

    def select(self):
        self.queryParts['action'] = 'select'

        if not self.error:
            success, result, meta = self.db.query(self.queryParts)

            if result:
                self._data = result
            
            return success

        return False


    def insert(self, dataInput: dict or list = None):
        self.queryParts['action'] = 'insert'
        h = dataInput

        if dataInput:
            if type(dataInput) is list:
                self.data = dataInput
            
            if type(dataInput) is dict:
                self.data = dataInput

        if not self.error:
            #self.queryParts['data'] = self.data

            success, result, meta  = self.db.query(self.queryParts)
            self.id = result[0][self.queryParts['pk'][0]]
            #self.data[0][ self.queryParts['pk'][0] ] = self.id
            
            return success

        return False


    def update(self, dataInput: dict or list = None):
        self.queryParts['action'] = 'update'

        if dataInput:
            self.data = dataInput

        data = self._data[0]
        pkList = self.queryParts['pk']
        
        counter = 0
        no_of_pk = len(pkList)
        
        where = {}
        for pk in pkList:

            for field in data.keys():

                if field == pk:
                    counter = counter + 1
                    where[field] = self.data[0][field]


        '''
        all of the pk requirements have not been met and we have no where
        '''
        if no_of_pk != counter and self.queryParts['where'] is None:
            self.error = 'No PK passed in'
            return None

        if no_of_pk == counter:
            for field, value in where.items():
                items = [field, value, '=']
                self.where(items)

        success, result, meta  = self.db.query(self.queryParts)

        return success


    def delete(self):
        self.queryParts['action'] = 'delete'
        
        if not self.queryParts['where']:
            self.error = 'arguments are a requirement for a DELETE statement'

        success, result, meta = self.db.query(self.queryParts)

        return success


    def field(self, fields: list):
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
        '''
        fieldArr is a list, these sub lists will at minimum contain 2 values, up to 4 values
        we access the 3rd and 4th value with *args, but need to test for them and assign defaults if
        they don't exist
        '''
        field, value, *args = fieldArr

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

    

    '''
    Resets the queryParts dict to blank all the keys
    '''
    def reset(self):
        for key in self.queryParts:
            if type(self.queryParts[key]) in [list, tuple, dict]:
                self.queryParts[key].clear()