from ..util import Console
from ..interface.IConnection import Base

import psycopg2
import psycopg2.extras

class Connection(Base,object):

    _instances = {}

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            print('Creating the object...')
            cls.instance = super(Connection, cls).__new__(cls)
        return cls.instance


    def __init__(self):
        self.connection = self.connect()
        self.query_parts_og = {}
        self.query_parts = {}


    def connect(self):
        Console.info('Running connect in connector....')
        conn = psycopg2.connect(database="test",
                                host="localhost",
                                user="root",
                                password="root",
                                port="5432")

        conn.autocommit = True

        return conn


    def query(self, queryDict):
        
        self.query_parts_og = queryDict
        result = {}
        
        
        #self._reset()
        '''
        We loops through the query parts to call various functions to perform the translation so it works with this datasource
        '''
        for key in queryDict:
            if key == 'action': 
                continue
            do = f"_{key}"
            
            if hasattr(self, do) and callable(func := getattr(self, do)):
                self.query_parts[key] = func(self.query_parts_og[key])

        self.query_parts['action'] = self._action(self.query_parts_og['action'])

        do = f"_action_{self.query_parts_og['action']}"

        command = ''
        if hasattr(self, do) and callable(func := getattr(self, do)):
            command = func()

        Console.log(self.query_parts)
        Console.log(f'{command}')
        success, data = self._run(command)
        Console.db(data)
        return success, data

        

    def _run(self, queryStr):
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)#NamedTupleCursor)#DictCursor)
        result = {}
        success: bool
        
        try:
            cursor.execute(queryStr, self.query_parts['data'])
            success = True
        except Exception as err:
            Console.error(f'{err}')
            Console.error(f'{type(err)}')
            success = False

        try:
            columns: list = [col.name for col in cursor.description]
            res = cursor.fetchall()

            count = cursor.rowcount
            data: list = []
            for row in res:
                row_data: dict = {}
                for field in columns:
                    row_data[field] = row[field]
                data.append(row_data)


            result = data
            #result[0][ self.query_parts['pk'][0] ] = id

        except:
            pass

        cursor.close()

        
        return success, result        
        

    def _process_field(self):
        pass


    def _action(self, value):
        match value:
            case 'select':
                return 'SELECT'
            case 'update':
                return 'UPDATE'
            case 'insert':
                return 'INSERT INTO'
            case 'delete':
                return 'DELETE'
            case 'create':
                return 'CREATE TABLE'
            case 'drop':
                return 'DROP TABLE'
            case 'alter':
                return 'ALTER TABLE'


    def _field(self, fieldArr):
        string = ','.join(fieldArr)
        return string


    def _order(self, value: list):
        if not value:
            return ''

        orderArr: list = []
        for field, direction in value:
            orderArr.append(f'{field} {direction}')
        
        return 'ORDER BY ' + ','.join(orderArr)


    def _pagination(self, value):
        limit = value["limit"]

        return(f'LIMIT {limit}')


    def _table(self, value):
        return(f'{value}')


    def _where(self, whereList: list):
        if not whereList:
            return ''
        
        whereArr: list = []
        length = len(whereList)
        counter = 0

        self.query_parts_og['data'] = {}#.append({})
        for field, value, operation, group_operation in whereList:

            ## exclude the final group_operation so it doesn't interfere with the remainder of our query after the WHERE clause
            if counter < length-1:
                group_operation = self._translate(group_operation)
            else:
                group_operation = ''

            whereArr.append(f'({field} {self._translate(operation)} %({field}{counter})s) {group_operation}')
            data_field_name = f'{field}{counter}'
            self.query_parts_og['data'][f'{field}{counter}'] = value

            counter = counter + 1
        return 'WHERE ' + ' '.join(whereArr)



    def _database(self, value):
        return(f'{value}')


    def _data(self, value):
        return value


    def _pk(self, value):
        return value
        return ','.join(value)


    def _action_create(self):
        arr = []
        for field, schema in self.query_parts_og['field'].items():

            # build up each column with various attributes like, auto, pk, not null etc
            line = [field]

            if 'auto' in schema.keys():
                line.append('SERIAL PRIMARY KEY')
            else:
                line.append(f'{schema["type"].upper()}')

            if schema['type'] not in 'int,number':
                line.append(f'({str(schema["size"])})')
       
            if 'required' in schema.keys():
                line.append('NOT NULL')
            line.append(',')
            
            arr.append(' '.join(line))
        
        result = ''.join(arr)[:-1]
        self.query_parts['field'] = '(' + result + ')'
        
        return self.query_parts['action'] + ' ' + self.query_parts['table'] + ' ' + self.query_parts['field'] + ' '
        

    def _action_drop(self):
        return self.query_parts['action'] + ' ' + self.query_parts['table']


    def _action_select(self):
        return self.query_parts['action'] + ' ' + self.query_parts['field'] + ' FROM ' + self.query_parts['table'] + ' ' + self.query_parts['where'] + ' ' + self.query_parts['order'] + ' ' + self.query_parts['pagination']


    def _action_insert(self):
        valueArr = []
        for field, value in self.query_parts['data'].items():
            valueArr.append(f'%({str(field)})s')

        return self.query_parts['action'] + ' ' + self.query_parts['table'] + ' (' + self.query_parts['field'] + ') VALUES (' + ','.join(valueArr) + ') RETURNING ' + ','.join(self.query_parts['pk'])


    def _reset(self):
        self.query_parts = self.query_parts_og

    '''
    converts keywords to this database specific keywords
    '''
    def _translate(self, value):

        return value