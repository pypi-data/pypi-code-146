# coding:utf-8
from tools_hjh.ThreadPool import ThreadPool
from tools_hjh.Tools import remove_leading_space


class DBConn:
    """ 维护一个关系型数据库连接池，目前支持oracle，pgsql，mysql，sqlite；支持简单的sql执行 """
    
    ORACLE = 'oracle'
    PGSQL = 'pgsql'
    MYSQL = 'mysql'
    SQLITE = 'sqlite'

    def __init__(self, dbtype, host=None, port=None, db=None, username=None, password=None, poolsize=2, encoding='UTF-8', lib_dir=None):
        """ 初始化连接池
                如果是sqlite，db这个参数是要显示给入的
                如果是oracle，db给入的是sid或是servername都是可以的 """
                
        self.dbtype = dbtype
        self.host = host
        self.port = port
        self.db = db
        self.username = username
        self.password = password
        self.poolsize = poolsize
        self.encoding = encoding
        self.lib_dir = lib_dir
        
        self.runtp = ThreadPool(1, save_result=True)
        self.dbpool = None
        
        self.config = {
            'host':self.host,
            'port':self.port,
            'database':self.db,
            'user':self.username,
            'password':self.password,
            'maxconnections':self.poolsize,  # 最大连接数
            'blocking':True,  # 连接数达到最大时，新连接是否可阻塞
            'reset':False
        }
        
        if self.dbtype == 'pgsql' or self.dbtype == 'mysql':
            from dbutils.pooled_db import PooledDB
        if self.dbtype == "pgsql":
            import psycopg2
            self.dbpool = PooledDB(psycopg2, **self.config)
        elif self.dbtype == "mysql":
            import pymysql
            self.dbpool = PooledDB(pymysql, **self.config)
        elif self.dbtype == "sqlite": 
            import sqlite3
            from dbutils.persistent_db import PersistentDB
            self.dbpool = PersistentDB(sqlite3, database=db)
        elif self.dbtype == "oracle":
            import cx_Oracle
            if lib_dir is not None:
                cx_Oracle.init_oracle_client(lib_dir=lib_dir)
            try:
                dsn = cx_Oracle.makedsn(host, port, service_name=db)
                self.dbpool = cx_Oracle.SessionPool(user=username,
                                                    password=password,
                                                    dsn=dsn,
                                                    max=poolsize,
                                                    increment=1,
                                                    encoding=encoding)
            except:
                dsn = cx_Oracle.makedsn(host, port, sid=db)
                self.dbpool = cx_Oracle.SessionPool(user=username,
                                                    password=password,
                                                    dsn=dsn,
                                                    max=poolsize,
                                                    increment=1,
                                                    encoding=encoding)
    
    def __run(self, sql, param=None):
        sql = remove_leading_space(sql)
        # 替换占位符
        if self.dbtype == 'pgsql' or self.dbtype == 'mysql':
            sql = sql.replace('?', '%s')
        elif self.dbtype == 'oracle':
            sql = sql.replace('?', ':1')            
        else:
            pass
        
        # 获取连接
        if self.dbtype == "oracle":
            conn = self.dbpool.acquire()
        else:
            conn = self.dbpool.connection()
            
        cur = conn.cursor()
        
        '''
        # 执行SQL文件
        if type(param) == str and os.path.exists(param):
            file = open(param)
            sqlStr = file.read()
            file.close()
            if self.dbtype == 'pgsql':
                cur.execute(sqlStr)
            elif self.dbtype == 'sqlite':
                cur.executescript(sqlStr)
            elif self.dbtype == 'mysql' or self.dbtype == 'oracle':
                pass  # 暂不支持
            conn.commit()
            returnMess = self
        '''
        # 执行非SELECT语句
        if not sql.lower().strip().startswith("select"):
            sql = sql.strip()
            if type(param) == list:
                cur.executemany(sql, param)
            elif type(param) == tuple:
                cur.execute(sql, param)
            elif param is None:
                cur.execute(sql)
            conn.commit()
            rownum = cur.rowcount
            cur.close()
            conn.close()
            return rownum
    
        # 执行SELECT语句
        if sql.lower().strip().startswith("select"):
            sql = sql.strip()
            col = []
            if param is None:
                cur.execute(sql)
            elif type(param) == tuple:
                cur.execute(sql, param)
            for c in cur.description:
                col.append(c[0])
            rows = cur.fetchall()
            cur.close()
            conn.close()
            return QueryResults(tuple(col), rows)
        
    def run(self, sql, param=None, wait=False):
        """ 执行点什么
        sql中的占位符可以统一使用“?”
        wait为True则会等待当前正在执行的sql，有bug，暂不处理，自用规避"""
        if wait == True:
            tpnum = self.runtp.run(self.__run, (sql, param))
            self.runtp.wait()
            rs = self.runtp.result_map.pop(tpnum)
            return rs
        else:
            return self.__run(sql, param)
        
    def insert(self, table_name, rows, pks=[]):
        """ 往指定table_name中插入数据，rows是一个多个元组的列表，每个元组表示一组参数；或者是一个元组 """
        if type(rows) == list and len(rows) > 0:
            row = rows[0]
        elif type(rows) == tuple:
            row = rows
            
        sql2 = ''
        pk_num = 0
        if type(pks) == str:
            pk_num = 1
            sql2 = sql2 + pks + ' = ?'
        elif type(pks) == list or type(pks) == tuple:
            pk_num = len(pks)
            for pk in pks:
                sql2 = sql2 + pk + ' = ? and '
            sql2 = sql2.rstrip('and ')
            
        param_num = '?'
        for _ in range(len(row) - 1 - pk_num):
            param_num = param_num + ', ?'
            
        if self.dbtype == 'oracle':
            if len(pks) == 0:
                sql = 'insert into ' + table_name + ' select ' + param_num + ' from dual'
            else:
                sql = 'insert into ' + table_name + ' select ' + param_num + ' from dual where not exists(select 1 from ' + table_name + ' where ' + sql2 + ')'
        else:
            if len(pks) == 0:
                sql = 'insert into ' + table_name + ' select ' + param_num
            else:
                sql = 'insert into ' + table_name + ' select ' + param_num + ' where not exists(select 1 from ' + table_name + ' where ' + sql2 + ')'
        
        return self.run(sql, rows)
                
    def close(self):
        try:
            self.dbpool.close()
        except:
            pass
        finally:
            self.dbpool = None
    
    def __del__(self):
        self.close()
        

class QueryResults:

    def __init__(self, cols=(), rows=[]):
        self.cols = cols
        self.rows = rows

    def get_cols(self):
        return self.cols

    def get_rows(self):
        return self.rows
    
    def set_cols(self, cols):
        self.cols = cols
        
    def set_rows(self, rows):
        self.rows = rows
