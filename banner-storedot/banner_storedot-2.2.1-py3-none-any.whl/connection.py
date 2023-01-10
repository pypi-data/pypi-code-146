
from typing import Union, Dict, Iterable
from abc import ABC, abstractmethod
from enum import Enum
from itertools import chain
from json import loads, dumps
from inspect import getfullargspec

from MySQLdb import connect as mysql_connect, MySQLError
from MySQLdb._exceptions import OperationalError
from MySQLdb.cursors import DictCursor

from psycopg2 import connect as postgres_sql_connect, Error as PostgresSQLError
from psycopg2.extras import RealDictCursor
from psycopg2.errors import DatabaseError as PostgresSQLDatabaseError
import redis
from redis.commands.json.path import Path
from pandas import DataFrame, concat

try:
    from pandas.core.computation.ops import UndefinedVariableError # pandas < 1.5.0
    
except ImportError:
    from pandas.errors import UndefinedVariableError 

from numpy import int64

from banner.utils.const import TTL_KWARG, NW_CACHE_COLUMNS
from banner.utils.misc import digested_key #Banner
from banner.utils.pandas import parse_mysql_to_pandas_query

class ConnectionType(Enum):
    mysql = 'mysql'
    redis = 'redis'
    postgres = 'postgres'

class ConnectionFactory(object):
    ''' Connection Factory'''
    def __new__(self, con_type: Union[ConnectionType, str] = ConnectionType.mysql, **kwargs):
        try:
            con_type = ConnectionType[con_type]

        except KeyError:
            pass
            
        if not isinstance(con_type, ConnectionType):
            raise TypeError('Unknown Connection Type')
        
        if con_type is ConnectionType.redis:
            return RedisConnection(**kwargs)
            
        return MySqlConnection(**kwargs)        

class Connection(ABC):
    @abstractmethod
    def retrieve(self):
        pass

    @abstractmethod
    def store(self):
        pass

class RelationalConnection(Connection):
    @abstractmethod
    def describe(self, table: str = ''):
        pass

class Storage(Connection):
    @abstractmethod
    def keys(self, query):
        pass

class PrintableConnection(Connection):
    @abstractmethod
    def name(self):
        pass
    
    @abstractmethod
    def __str__(self):
        pass

class RedisConnection(Storage, PrintableConnection):
    HOUR = 3600

    def __init__(self, host, port=6379, passwd=None, db=0, ssl_key=None, ssl_cert=None, ssl_ca_cert=None, name=None, ttl=HOUR):
        self.data = dict(
            host=host,
            port=port,
            password=passwd,
            db=db,
            ssl_keyfile=ssl_key,
            ssl_certfile=ssl_cert,
            ssl_ca_certs=ssl_ca_cert,
            ssl=any([ssl_key, ssl_cert, ssl_ca_cert])
        )

        self.__ttl = ttl or RedisConnection.HOUR
        self.__name = name

        # Redis manages opening/closing by itself, it is safe to init it here
        self.instance = redis.Redis(
            **self.data, 
            decode_responses=True
        )
    
    def keys(self, query: str):
        '''
            Retrieve Keys from Storage
        '''
        return self.instance.keys(pattern=f'{str(query)}')

    def retrieve(self, func: callable, *args, **kwargs):
        '''
            Retrieve Value from Storage
        '''
        controller = QUERY_TO_STORAGE_CONTROL.get(func.__name__, DefaultStorageController)

        return controller.retrieve(
            self.instance, func, *args, **kwargs
        )
        
    def store(self, value, func: callable, *args, ttl=None, nx=True, **kwargs):
        '''
            Set Value Into Storage
        '''
        ttl = ttl if ttl else self.__ttl

        controller = QUERY_TO_STORAGE_CONTROL.get(func.__name__, DefaultStorageController)
        
        return controller.store(
            self.instance, value, func, *args, ttl=ttl, nx=nx, **kwargs
        )

    def retrieve_by(self, key: str):
        return self.instance.get(
            str(key)
        )
        
    def store_by(self, key: str, value, ttl=None):
        ttl = ttl if ttl else self.__ttl

        resp = self.instance.set(
            key, value, ex=ttl, nx=True
        )

        if resp is True:
            return key

        raise KeyError(f'{key} Exists')
        
    @property
    def name(self):
        return self.__name or str(self.data)

    def __str__(self):
        return self.name
            
class MySqlConnection(RelationalConnection, PrintableConnection):
    def __init__(self, host, user, port=3306, passwd=None, db=None, ssl_key=None, ssl_cert=None, charset='utf8', use_unicode=True, name=None):
        self.data = dict(
            host=host,
            user=user,
            port=port,
            passwd=passwd,
            db=db,
            ssl=dict(key=ssl_key, cert=ssl_cert),
            charset=charset,
            use_unicode=use_unicode,
            cursorclass=DictCursor 
        )

        self.__name = name

    def retrieve(self, query: str):
        try:
            instance = self.__connect()
            
            cursor = instance.cursor()
            
            cursor.execute(query)

            records = cursor.fetchall()

            cursor.close()
        
            records = DataFrame(records).convert_dtypes()
            
        except MySQLError as e:
            raise e
        
        finally:
            self.__close(instance)        

        return records

    def store(self, statement: str, *args, unique_checks=True, foreign_key_checks=True):
        prefix, suffix = list(), list()

        if not unique_checks:
            prefix.append('SET unique_checks=0;')
            suffix.insert(0, 'SET unique_checks=1;')

        if not foreign_key_checks:
            prefix.append('SET foreign_key_checks=0;')
            suffix.insert(0, 'SET foreign_key_checks=1;')

        try:
            instance = self.__connect()
            
            cursor = instance.cursor()
            
            for q in prefix:
                cursor.execute(q)

            cursor.execute(statement, *args)
            
            for q in suffix:
                cursor.execute(q)
            
            instance.commit()
            
            cursor.close()
            
        except MySQLError as e:
            instance.rollback()
            raise e
        
        finally:
            self.__close(instance)
        
        return cursor.rowcount

    def describe(self, table: str = ''):
        _query = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{self.data.get('db')}'"

        if table:
            _query = f'DESCRIBE {table}'

        return self.retrieve(_query)

    def __connect(self):
        try:
            return mysql_connect(**self.data)

        except OperationalError:
            raise MySQLError(
                f'Connection to {self.name} Failed'
            )
      
    def __close(self, instance):
        try:
            instance.close() 
            
        except (AttributeError, MySQLError):
            pass
    
    @property
    def name(self):
        return self.__name or str(self.data)

    def __str__(self):
        return self.name

class PostgresSqlConnection(RelationalConnection, PrintableConnection):
    def __init__(self, host, user, port=5432, passwd=None, db=None, ssl_key=None, ssl_cert=None, charset='utf8', name=None):
        self.data = dict(
            host=host,
            port=port,
            user=user,
            password=passwd,
            dbname=db,
            sslkey=ssl_key,
            sslcert=ssl_cert
        )

        self.__name = name
        self.__charset = charset
        
    def retrieve(self, query: str):
        try:
            instance = self.__connect()
            
            cursor = instance.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute(query)
            
            records = cursor.fetchall()
            
            cursor.close()
        
            records = DataFrame(records).convert_dtypes()

        except PostgresSQLError as e:
            raise e
        
        finally:
            self.__close(instance)        

        return records

    def store(self, statement: str):
        try:
            instance = self.__connect()
            
            cursor = instance.cursor()
            
            cursor.execute(statement)

            instance.commit()
            
            cursor.close()
            
        except PostgresSQLDatabaseError as e:
            instance.rollback()
            raise e
        
        finally:
            self.__close(instance)

        return cursor.rowcount

    def describe(self, table: str = ''):
        _query = f"SELECT table_name FROM information_schema.tables"

        if table:
            _query = (
                'SELECT column_name as "Field", data_type as "Type", is_nullable as "Null", column_default as "Default"'
                f" FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{table}'"
            )
            
        return self.retrieve(_query)
    
    def __connect(self):
        try:
            instance = postgres_sql_connect(**self.data)
            instance.set_client_encoding(self.__charset)

            return instance

        except PostgresSQLError:
            raise PostgresSQLDatabaseError(
                f'Connection to {self.name} Failed'
            )
      
    def __close(self, instance):
        try:
            instance.close() 
            
        except (AttributeError, PostgresSQLError):
            pass

    @property
    def name(self):
        return self.__name or str(self.data)

    def __str__(self):
        return self.name

class StorageController(ABC):
    '''
        Handles Store&Retrieve from Data Storage
    '''
    @abstractmethod
    def store(): # Return Command to fetch the data
        pass

    @abstractmethod
    def retrieve(): # Return Command to fetch the data
        pass

class DefaultStorageController(StorageController):
    '''
        Default Storage Controller
    '''
    NUM_OF_KEYS = 10
    MAX_ROWS = 100000

    @staticmethod
    def __table_index(func: callable, *args, **kwargs):
        try:
            table_index = getfullargspec(func).args.index('table')
            
        except (IndexError, KeyError, ValueError):
            table_index = -1
        
        return table_index

    @staticmethod
    def __keys(func: callable, *args, **kwargs):
        key = digested_key(func, *args, **kwargs)

        keys = [f'{key}#{i}' for i in range(DefaultStorageController.NUM_OF_KEYS)]

        return keys

    @staticmethod
    def store(
        storage: redis.client.Redis, value: DataFrame, 
        func: callable, *args, 
        ttl=None, nx=True, **kwargs
    ):  
        keys = DefaultStorageController.__keys(func, *args, **kwargs)
        values = value.split(size=DefaultStorageController.MAX_ROWS) # This is a banner function
        
        for key, val in zip(keys, values):
            resp = storage.set(
                key, val.to_json(orient='records'), ex=ttl, nx=nx
            )

            if not resp:
                raise redis.ResponseError
            
        return True

    @staticmethod
    def retrieve(
        storage: redis.client.Redis, func: callable, *args, **kwargs
    ):
        keys = DefaultStorageController.__keys(func, *args, **kwargs)
        values = list(filter(None, storage.mget(keys)))

        table_index = DefaultStorageController.__table_index(func) # Is it a table query?

        df = DataFrame.from_dict(
            chain(*[loads(value) for value in values]), orient='columns'
        ).convert_dtypes()
        
        if table_index >= 0: # Should set df._tables
            table = kwargs.get('table') # Check if table kwarg exists

            if not table: # Else use arg
                table = args[table_index] # Will raise Index Error if missing
            
            df._tables = [table] # Set table metadata

        return df

class NewareCacheController(DefaultStorageController):
    '''
        Neware Cache Data(DataFrame) Storage Controller
    '''
    PRIMARY_KEY = ['ip', 'dev_uid', 'unit_id', 'chl_id', 'test_id']

    @staticmethod
    def __keys(func: callable, *args, **kwargs):
        _keys_index = NewareCacheController.__keys_index(func, *args, **kwargs)
        
        try:
            assert(_keys_index >= 0)
            
            if (all(isinstance(item, Iterable) for item in args[_keys_index])):
                _keys = [tuple(key) for key in args[_keys_index]] # Make sure each key(collection) is a tuple
            
            else:
                _keys = [tuple(args[_keys_index])] # Single entry was given
            
            return [
                f'{ip}-{device}-{unit}-{channel}-{test}' for ip, device, unit, channel, test in _keys
            ]
                
        except (AssertionError, TypeError):
            return digested_key(func, *args, **kwargs)
    
    @staticmethod
    def __keys_index(func: callable, *args, **kwargs):
        try:
            keys_index = getfullargspec(func).args.index('keys')

        except (IndexError, KeyError, ValueError):
            keys_index = -1

        return keys_index

    @staticmethod
    def __dump(df: DataFrame):
        df_without_pk = df[df.columns.difference(NewareCacheController.PRIMARY_KEY)]

        return {
            str(key): loads(value.to_json(orient='values')) for key, value in df_without_pk.items()
        }

    @staticmethod
    def __load(key: str, value: dict):
        df = DataFrame.from_dict(value)
        
        for pk, val in zip(reversed(NewareCacheController.PRIMARY_KEY), reversed(key.split('-'))):
            df.insert(0, pk, val)
        
        return df

    @staticmethod
    def __should_cache(condition: str, columns: list):
        try: # More cases may appear, this can include all
            if condition and condition.lower() not in ['true', 1]: # Make sure condition doesnt create a partial result
                raise ValueError
            
            if set(columns) != NW_CACHE_COLUMNS: # Make sure we have all cache columns!
                raise ValueError

        except Exception as e:
            return False

        return True

    @staticmethod
    def store(
        storage: redis.client.Redis, value: DataFrame, 
        func: callable, *args, 
        ttl=None, nx=True, **kwargs
    ):
        condition = kwargs.get('condition', False)
        columns = kwargs.get('columns')

        if not columns or columns == '*':
            columns = value.columns

        if not NewareCacheController.__should_cache(condition, columns): # Partial value is given #TODO, should still be cached
            return DefaultStorageController.store(storage, value, func, *args, ttl=ttl, nx=nx, **kwargs)

        try: 
            data = value.groupby(NewareCacheController.PRIMARY_KEY).apply(NewareCacheController.__dump)
            
            for key, val in data.items():
                _key = '-'.join(map(str, key))
                
                resp = storage.json().set(
                    _key, Path.root_path(), val, nx=nx
                )
                
                if resp:
                    storage.expire(_key, ttl)
                
            return True

        except (TypeError, KeyError, redis.ResponseError):
            raise
        
    @staticmethod
    def retrieve(
        storage: redis.client.Redis, func: callable, *args, **kwargs
    ):  
        condition = kwargs.get('condition', False)
        columns = kwargs.get('columns') # Requested columns

        if not columns or columns == '*':
            columns = NW_CACHE_COLUMNS

        
        if not NewareCacheController.__should_cache(condition, columns): # Partial value is given #TODO, value should be retrieved and completed!
            return DefaultStorageController.retrieve(storage, func, *args, **kwargs)
        
        keys = NewareCacheController.__keys(func, *args, **kwargs) # Expected Keys
        
        try:
            values = storage.json().mget(keys, Path.root_path())
            values = list(filter(None, values)) # Remove Empty entries
            
            assert(len(values) == len(keys))
            
            df = concat(
                [NewareCacheController.__load(key, value) for key, value in zip(keys, values)],
                ignore_index=True
            )
            
            for column in df[NewareCacheController.PRIMARY_KEY].columns:
                df[column] = df[column].astype(int64)

            for column in df.filter(like='time').columns:
                df[column] = df[column].astype('datetime64[ms]')
            
            return df[list(columns)].convert_dtypes()

        except (AssertionError, redis.ResponseError):
            return DataFrame()

class NewareTestController(NewareCacheController):
    '''
        Neware Test(DataFrame) Storage Controller
    '''
    VALUE_GROUP_KEY = 'cycle' # All df is a single test, is simply cycle
    
    @staticmethod
    def __dump(df: DataFrame):
        df_without_pk = df.drop(NewareTestController.VALUE_GROUP_KEY, axis=1)
        
        return {
            str(key): loads(value.to_json(orient='values')) for key, value in df_without_pk.items()
        }

    @staticmethod
    def __load(key: str, value: dict):
        df = DataFrame.from_dict(value)
        
        try:
            location = df.columns.get_loc("seq_id") + 1

        except KeyError:
            location = 0
    
        df.insert(location, NewareTestController.VALUE_GROUP_KEY, key)
        
        return df

    @staticmethod
    def __should_cache(cache_data: DataFrame, condition: str, raw: bool):
        try:
            assert(isinstance(cache_data, DataFrame)) # Must have cache df
            
            if not raw and condition and condition.lower() not in ['true', 1]:
                # Assumption!! If the given condition filters cache it will not contain partial cycle data, and is safe to use!
                # Any exception raised here means query is meant for value and should not be cached!
                
                # if len(cache_data.query(condition).index) == len(cache_data.index): 
                #     raise ValueError
                
                if not isinstance(cache_data.query(condition), DataFrame):
                    raise ValueError

        except Exception as e:
            return False

        return True

    @staticmethod
    def store(
        storage: redis.client.Redis, value: DataFrame, 
        func: callable, *args, 
        ttl=None, nx=True, **kwargs
    ):  
        cache_data, condition = kwargs.get('cache_data'), parse_mysql_to_pandas_query(kwargs.get('condition', ''))
        raw = kwargs.get('raw', False)
        
        if not NewareTestController.__should_cache(cache_data, condition, raw):
            return DefaultStorageController.store(storage, value, func, *args, ttl=43200, nx=nx, **kwargs)
        
        try: 
            partial_key = list(cache_data[NewareTestController.PRIMARY_KEY].iloc[-1]) # A single test so grab any(last) row
            
            data = value.groupby(NewareTestController.VALUE_GROUP_KEY).apply(NewareTestController.__dump) 
            
            for cycle, cycle_data in data.items(): 
                _key = f"{'-'.join(map(str, partial_key))}-{int(cycle)}"
                
                resp = storage.json().set(_key, Path.root_path(), {},  nx=nx) # Make sure Key exists

                if resp:
                    storage.expire(_key, ttl)
                
                for column, column_data in cycle_data.items(): # TODO with a single command (currently not implemented by redis)
                    if column in NW_CACHE_COLUMNS: # Case column belong to NW_CACHE_COLUMNS
                        column_data = column_data[0] # Only first value since neware_cache values are per cycle!
                        
                    resp = storage.json().set(
                        _key, Path(column), column_data, nx=nx
                    )
                        
            return True

        except (TypeError, KeyError, IndexError, UndefinedVariableError, redis.ResponseError):
            raise

    @staticmethod
    def retrieve(
        storage: redis.client.Redis, func: callable, *args, **kwargs
    ):  
        cache_data, condition = kwargs.get('cache_data'), parse_mysql_to_pandas_query(kwargs.get('condition', ''))
        raw = kwargs.get('raw', False)
        
        if not NewareTestController.__should_cache(cache_data, condition, raw):
            return DefaultStorageController.retrieve(storage, func, *args, **kwargs)
        
        try:
            if condition and condition.lower() not in ['true', 1]:
                cache_data = cache_data.query(condition) # Only supports query on cache
            
            cycles = set(cache_data[NewareTestController.VALUE_GROUP_KEY]) # Ordered by default
            
            partial_key = list(cache_data[NewareTestController.PRIMARY_KEY].iloc[-1]) # A single test so grab any(last) row
            
            keys = [f"{'-'.join(map(str, partial_key))}-{cycle}" for cycle in cycles]
            
            values = storage.json().mget(keys, Path.root_path())
            
            values = list(filter(None, values)) # Remove Empty entries
            
            assert(len(values) == len(keys)) # TODO - HANDLE PARTIAL RESULT! (ONLY certain cycles in cache)
            
            df = concat(
                [NewareTestController.__load(cycle, value) for cycle, value in zip(cycles, values)],
                ignore_index=True
            )
            
            columns = kwargs.get('columns')
            
            if isinstance(columns, list):
                df = df[columns]
            
            for column in df.filter(like='test_atime').columns:
                df[column] = df[column].astype('datetime64[ms]')
            
            return df.convert_dtypes()
            
        except (AssertionError, KeyError, IndexError, UndefinedVariableError, redis.ResponseError):
            return DataFrame()

QUERY_TO_STORAGE_CONTROL = dict(
    _neware_cache_query=NewareCacheController,
    neware_query=NewareTestController
) 