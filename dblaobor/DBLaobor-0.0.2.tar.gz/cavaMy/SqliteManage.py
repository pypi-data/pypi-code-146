# -*- coding: utf-8 -*-
# @Time    : 2023/1/12 9:46
# @Author  :augwewe
# @FileName: SqliteManage.py
# @Software: PyCharm
import requests,re,os,json,sqlite3
from pprint import pprint

from sqlalchemy import create_engine
from sqlalchemy import Table, Column
from sqlalchemy import String, Boolean, Integer, MetaData, DateTime
from datetime import datetime
from sqlalchemy import  insert
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import  declarative_base


BookInfo=sqlite3.connect("D:/afterschool/Gra/cava.db")



class SqliteOperation(object):
     def __init__(self,db_name:str,table_name:str):
          self.db=sqlite3.connect(db_name)
          self.table = sqlite3.connect(table_name)

     def query(self,query:str):
          query_sql=f"select * from {query}"
          return list(self.db.execute(query_sql))

     def delete(self,key:str,value):
          delete_sql=f"delete from {self.table} where {key} = {value}"
          self.db.execute(delete_sql)
          self.db.commit()

     def update(self):
          update_sql="update {self.table} set {} = '史铁生' where id = 2 "
          self.db.execute(update_sql)
          self.db.commit()

     def insert_many(self,insert_data:list):
          for data_sql in insert_data:
               self.db.execute(data_sql)
               self.db.commit()



