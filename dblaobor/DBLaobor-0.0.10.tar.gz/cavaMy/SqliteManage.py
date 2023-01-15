# -*- coding: utf-8 -*-
# @Time    : 2023/1/12 9:46
# @Author  :augwewe
# @FileName: SqliteManage.py
# @Software: PyCharm
import requests,re,os,json,sqlite3




BookInfo=sqlite3.connect("D:/afterschool/Gra/cava.db")



class SqliteOperation(object):
     def __init__(self,db_name:str,table_name:str):
          self.db=sqlite3.connect(db_name)
          self.table = sqlite3.connect(table_name)

     def query(self,query:str):
          query_sql=f"select * from {query}"
          return list(self.db.execute(query_sql))

     def delete(self,key,value):
          delete_sql="delete from {} where {} = {}".format(self.table,key,value)
          self.db.execute(delete_sql)
          self.db.commit()

     def update(self,update_sql):
          self.db.execute(update_sql)
          self.db.commit()

     def insert_many(self,insert_data:list):
          for data_sql in insert_data:
               self.db.execute(data_sql)
               self.db.commit()



