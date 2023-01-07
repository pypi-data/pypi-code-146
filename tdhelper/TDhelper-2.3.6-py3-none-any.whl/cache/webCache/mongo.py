from TDhelper.cache.webCache.interface import cacheInterface
from TDhelper.db.mongodb.setting import db_cfg
from TDhelper.db.mongodb.base import mongodbclient
from TDhelper.db.mongodb.dbhelper import dbhelper
from TDhelper.db.mongodb.objectId import objectId

class mongo(cacheInterface):
    
    def __init__(self) -> None:
        super(mongo,self).__init__()
    
    def collect(self,k):
        if k in self.__cache__:
            self.__cursor__= self.__cache__[k]
        return self
    
    def addCollect(self,k,v):
        if k in self.__cache__:
            raise Exception("'%s' has already in cache."% k)
        else:
            self.__cache__[k]=v
            return self
            
    def delCollect(self,k):
        if k in self.__cache__:
            del self.__cache__[k]
            return self
        else:
            raise Exception("'%s' not found in cache."%k)
    
    def set(self,*args,**kwargs):
        if self.__cursor__:
            self.__cursor__.save(kwargs)
            self.__cursor__=None
        else:
            raise Exception('not found collect.')
    
    def get(self,flag="single",*args,**kwargs)-> object:
        if self.__cursor__:
            result= None
            if flag.lower()=="single":
                result= self.__cursor__.findOne(kwargs)
            else:
                result= self.__cursor__.find(**kwargs)
            self.__cursor__= None
            return result
        else:
            raise Exception("not found collect.")
    
    def remove(self,*args,**kwargs):
        if self.__cursor__:
            result= self.__cursor__.remove(kwargs)
            self.__cursor__= None
            return result
        else:
            raise Exception('not found collect.')
    
    def update(self,*args,**kwargs):
        if self.__cursor__:
            result= self.__cursor__.update(kwargs['query'],kwargs['args'])
            self.__cursor__= None
            return result
        else:
            raise Exception('not found collect.')