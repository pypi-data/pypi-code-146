# coding:utf-8
from tools_hjh import DBConn


def main():
    mdb = MemoryDB()
    rows = [('1', '1'), ('a', 'a'), ('1', 'a')]
    mdb.set('q1', ('c1', 'c2'), rows)
    mdb.append('q1', [('2', 'b')])
    rss = mdb.get('q1').get_rows()
    for rs in rss:
        print(rs)
    mdb.drop('q1')


class MemoryDB: 
    """ 维护一个:memory:方式打开的sqlite数据库连接 """

    def __init__(self):
        self.db_conn = DBConn(DBConn.SQLITE, db=':memory:')
        
    def set(self, table_name, cols, rows):
        """ 重建指定表，且插入rows数据 """
        sql1 = 'drop table if exists ' + table_name
        sql2 = 'create table ' + table_name + ' ('
        for col in cols:
            sql2 = sql2 + col + ' text, \n'
        sql2 = sql2.strip().strip(',') + ')'
        self.db_conn.run(sql1)
        self.db_conn.run(sql2)
        return self.db_conn.insert(table_name, rows)
    
    def drop(self, table_name):
        sql = 'drop table ' + table_name
        self.db_conn.run(sql)
    
    def append(self, table_name, rows):
        """ 往指定表插入rows数据 """
        return self.db_conn.insert(table_name, rows)
        
    def get(self, table_name):
        """ 得到指定表全部数据（col,rows） """
        sql = 'select * from ' + table_name
        return self.db_conn.run(sql)
        
    def close(self):
        self.db_conn.close()

    def __del__(self):
        self.close()
      

if __name__ == '__main__':
    main()
