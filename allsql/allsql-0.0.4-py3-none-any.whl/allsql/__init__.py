import sqlite3
import cx_Oracle
import mysql.connector

class Sqlite:

    def __init__(self,database):
        self.database = database

    def main(self,database,type,command):
        try:
          cnx = self.connect(self.database)
          crs = cnx.cursor()
          result = []
          if type == 'DDL' or type == 'DML':
            crs.execute(command)
            cnx.commit()
          if type == 'DQL':
            rst = crs.execute(command)
            result.append(list(rst))
          cnx.close()
          return result[0]
        except Exception as err:
          return err

    def connect(self,database):
        try:
          cnx = sqlite3.connect(self.database)
          return cnx
        except Exception as err:
          return err

    def create_database(self,database):
        try:
          self.connect(self.database)
        except Exception as err:
          return err
  
    def create_table(self,table,columns):
        try:
          command = f'CREATE TABLE IF NOT EXISTS {table} ({columns});'
          self.main(self.database,'DDL',command)
        except Exception as err:
          return err

    def truncate_table(self,table):
        try:
          command = f'DELETE FROM {table};'
          self.main(self.database,'DML',command)
        except Exception as err:
          return err

    def drop_table(self,table):
        try:
          command = f'DROP TABLE {table};'
          self.main(self.database,'DDL',command)
        except Exception as err:
          return err

    def select(self,table,columns,where='',groupby='',orderby=''):
        try:
          vWhere = ''
          vGroupby = ''
          vOrderby = ''
          if len(where.strip()) > 0:
            vWhere = f'WHERE {where.replace(","," AND ")}'
          if len(groupby.strip()) > 0:
            vGroupby = f'GROUP BY {groupby}'
          if len(orderby.strip()) > 0:
            vOrderby = f'ORDER BY {orderby}'
          command = f'SELECT {columns} FROM {table} {vWhere} {vGroupby} {vOrderby};'
          result = self.main(self.database,'DQL',command)
          return result
        except Exception as err:
          return err

    def insert(self,table,columns,values):
        try:
          command = f'INSERT INTO {table} ({columns}) VALUES ({values});'
          self.main(self.database,'DML',command)
        except Exception as err:
          return err

    def update(self,table,set,where=''):
        try:
          vWhere = ''
          if len(where.strip()) > 0:
            vWhere = f'WHERE {where.replace(","," AND ")}'
          command = f'UPDATE {table} SET {set} {vWhere};'
          self.main(self.database,'DML',command)
        except Exception as err:
          return err

    def delete(self,table,where=''):
        try:
          vWhere = ''
          if len(where.strip()) > 0:
            vWhere = f'WHERE {where.replace(","," AND ")}'
          command = f'DELETE FROM {table} {vWhere};'
          self.main(self.database,'DML',command)
        except Exception as err:
          return err

    def sql(self,sql):
        try:
          command = sql.strip()
          result = self.main(self.database,'DQL',command)
          return result
        except Exception as err:
          return err

class Mysql:

    def __init__(self,usr,psw,hst,dba):
        self.usr = usr
        self.psw = psw
        self.hst = hst
        self.dba = dba

    def main(self,type,command):
        try:
          cnx = self.connect(self.usr,self.psw,self.hst,self.dba)
          crs = cnx.cursor()
          result = []
          if type == 'DDL' or type == 'DML':
            crs.execute(command)
            cnx.commit()
          if type == 'DQL':
            crs.execute(command)
            result.append(list(crs.fetchall()))
          cnx.close()
          return result[0]
        except Exception as err:
          return err

    def connect(self,usr,psw,hst,dba):
        try:
          cnx = mysql.connector.connect(user=usr,password=psw,host=hst,database=dba)
          return cnx
        except Exception as err:
          return err

    def connected(self):
        cnx = self.connect(self.usr,self.psw,self.hst,self.dba)
        return cnx.is_connected()

    def create_table(self,table,columns):
        try:
          command = f'CREATE TABLE {table} ({columns})'
          self.main('DDL',command)
        except Exception as err:
          return err
        
    def truncate_table(self,table):
        try:
          command = f'TRUNCATE TABLE {table}'
          self.main('DML',command)
        except Exception as err:
          return err

    def drop_table(self,table):
        try:
          command = f'DROP TABLE {table}'
          self.main('DDL',command)
        except Exception as err:
          return err

    def select(self,table,columns,where='',groupby='',orderby=''):
        try:
          vWhere = ''
          vGroupby = ''
          vOrderby = ''
          if len(where.strip()) > 0:
            vWhere = f'WHERE {where.replace(","," AND ")}'
          if len(groupby.strip()) > 0:
            vGroupby = f'GROUP BY {groupby}'
          if len(orderby.strip()) > 0:
            vOrderby = f'ORDER BY {orderby}'
          command = f'SELECT {columns} FROM {table} {vWhere} {vGroupby} {vOrderby}'
          result = self.main('DQL',command)
          return result
        except Exception as err:
          return err

    def insert(self,table,columns,values):
        try:
          command = f'INSERT INTO {table} ({columns}) VALUES ({values})'
          self.main('DML',command)
        except Exception as err:
          return err

    def update(self,table,set,where=''):
        try:
          vWhere = ''
          if len(where.strip()) > 0:
            vWhere = f'WHERE {where.replace(","," AND ")}'
          command = f'UPDATE {table} SET {set} {vWhere}'
          self.main('DML',command)
        except Exception as err:
          return err

    def delete(self,table,where=''):
        try:
          vWhere = ''
          if len(where.strip()) > 0:
            vWhere = f'WHERE {where.replace(","," AND ")}'
          command = f'DELETE FROM {table} {vWhere}'
          self.main('DML',command)
        except Exception as err:
          return err

    def sql(self,sql):
        try:
          command = sql.strip()
          result = self.main('DQL',command)
          return result
        except Exception as err:
          return err
