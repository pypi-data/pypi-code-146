# -*- coding: utf-8 -*-
# @Time    : 2023/1/12 11:21
# @Author  :augwewe
# @FileName: MongoDB.py
# @Software: PyCharm
import pymongo

class MongoDB(object):
    def __init__(self,database,_set,host="localhost",port=27017):
        self.client=pymongo.MongoClient(host=host,port=port)
        self.db=self.client[database]
        self.collection=self.db[_set]

    def insert(self,data:dict):
        result = self.collection.insert_one(data)
        return result

    def inserts(self,datas:list):
        result=self.collection.insert_many(datas)
        return result

    def query(self,query:dict):
        result=self.collection.find_one(query)
        return result

    def find_all(self,find_dict):
        result=self.collection.find(find_dict)
        return result

    def update(self,data:dict,key,value):
        query_result=self.query(data)
        query_result[key]=value
        result=self.collection.update(data,query_result)
        return result

    def delete_one(self,data:dict):
        result=self.collection.delete_one(data)
        print(f"本次删除了：{result.deleted_count}")
        return result

    def delete_many(self,data:dict):
        result=self.collection.delete_many(data)
        print(f"本次删除了：{result.deleted_count}")
        return  result




