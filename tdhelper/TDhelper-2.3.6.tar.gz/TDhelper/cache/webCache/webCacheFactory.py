from TDhelper.cache.webCache.mongo import mongo
class webCacheFactory:
    __conf__={
            "host":"",
            "collect":"",
            "user":"",
            "pwd":""
        }
    __cache__={}
    __cursor__=None
    __handle__=None
    def __init__(self,cls="memory",conf={}):
        if cls.lower()=="memory":
            pass
        elif cls.lower()=="mongo":
            self.__handle__= mongo(**conf)
        elif cls.lower()=="redis":
            pass
        else:
            raise Exception("cls must value: memory | mongo | redis.")
    
    def set(self,*args,**kwargs):
        self.__handle__.set(*args,**kwargs)
        
    def get(self,flag='single',*args,**kwargs):
        return self.__handle__.get(flag,*args,**kwargs)

    def collect(self,k):
        return self.__handle__.collect(k)
    
    def addCollect(self,k,v):
        self.__handle__.addCollect(k,v)
         
    def delCollect(self,k):
        self.__handle__.delCollect(k)
    
    def remove(self,*args,**kwargs):
        self.__handle__.remove(*args,**kwargs)
    
    def update(self,*args,**kwargs):
        self.__handle__.update(*args,**kwargs)