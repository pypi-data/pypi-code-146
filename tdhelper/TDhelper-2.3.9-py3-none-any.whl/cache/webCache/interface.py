import abc
import six

@six.add_metaclass(abc.ABCMeta)
class cacheInterface:
    __cache__={}
    __cursor__=None
    @abc.abstractclassmethod
    def __init__(self):
        pass
    
    @abc.abstractclassmethod
    def set(self,*args,**kwargs):
        pass
        
    @abc.abstractclassmethod
    def get(self,flag='single',*args,**kwargs):
        pass
    
    @abc.abstractclassmethod
    def exist(self,*args,**kwargs):
        pass
    
    @abc.abstractclassmethod
    def collect(self,*args,**kwargs):
        pass
    
    @abc.abstractclassmethod
    def addCollect(self,k,v):
        pass
    
    @abc.abstractclassmethod        
    def delCollect(self,k):
        pass
    
    @abc.abstractclassmethod   
    def remove(self,*args,**kwargs):
        pass
    
    @abc.abstractclassmethod   
    def update(self,*args,**kwargs):
        pass