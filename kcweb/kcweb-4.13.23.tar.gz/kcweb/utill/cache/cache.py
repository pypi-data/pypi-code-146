# -*- coding: utf-8 -*-
import os,sys,time,hashlib,json
from kcweb import config
from kcweb.utill import rediss as red
# from kcweb.utill.db.mysql import mysql

import time,hashlib
def md5(strs):
    """md5加密"""
    if not strs:
        return strs
    m = hashlib.md5()
    b = strs.encode(encoding='utf-8')
    m.update(b)
    return m.hexdigest()
def times():
    """时间戳 精确到秒"""
    return int(time.time())
def json_decode(jsonstr):
    """json字符串转python类型"""
    try:
        return eval(jsonstr)
    except Exception:
        return {}
# def json_decode(strs):
#     """json字符串转python类型"""
#     try:
#         return json.loads(strs)
#     except Exception:
#         return {}
class cache:
    "开发完善中..."
    __name=None
    __values=None
    __cachepath='' #os.path.split(os.path.realpath(__file__))[0]+'/../../../'
    __config=config.cache
    __redisobj=None
    __mysqlobj=None
    # def __setmysqlonj(self):
    #     conf=config.database
    #     if 'host' in self.__config and self.__config['host']:
    #         conf['host']=[self.__config['host']]
    #     if 'port' in self.__config and self.__config['port']:
    #         conf['port']=[self.__config['port']]
    #     if 'user' in self.__config and self.__config['user']:
    #         conf['user']=[self.__config['user']]
    #     if 'password' in self.__config and self.__config['password']:
    #         conf['password']=[self.__config['password']]
    #     if 'db' in self.__config and self.__config['db']:
    #         conf['db']=[self.__config['db']]
    #     db=mysql()
    #     self.__mysqlobj=db.connect(conf)
    def __setredisobj(self):
        "设置redis链接实例"
        conf=config.redis
        if 'host' in self.__config and self.__config['host']:
            conf['host']=self.__config['host']
        if 'port' in self.__config and self.__config['port']:
            conf['port']=self.__config['port']
        if 'password' in self.__config and self.__config['password']:
            conf['password']=self.__config['password']
        if 'db' in self.__config and self.__config['db']:
            conf['db']=self.__config['db']
        if conf['pattern']:
            if conf['password']:
                redis_pool=red.ConnectionPool(host=conf['host'],password=conf['password'],port=conf['port'],db=conf['db'])
            else:
                redis_pool=red.ConnectionPool(host=conf['host'],port=conf['port'],db=conf['db'])
            self.__redisobj=red.Redis(connection_pool=redis_pool)
        else:
            if conf['password']:
                self.__redisobj=red.Redis(host=conf['host'],password=conf['password'],port=conf['port'],db=conf['db'])
            else:
                self.__redisobj=red.Redis(host=conf['host'],port=conf['port'],db=conf['db'])
    def set_cache(self,name,values,expire = 'no'):
        """设置缓存

        参数 name：缓存名

        参数 values：缓存值

        参数 expire：缓存有效期 0表示永久  单位 秒
        
        return Boolean类型
        """
        # print(name)
        # exit()
        self.__name=name
        self.__values=values
        if expire != 'no':
            self.__config['expire']=int(expire)
        return self.__seltype('set')
    def get_cache(self,name):
        """获取缓存

        return 或者的值
        """
        self.__name=name
        return self.__seltype('get')
    def del_cache(self,name):
        """删除缓存

        return Boolean类型
        """
        self.__name=name
        return self.__seltype('del')
    def set_config(self,congig):
        """设置缓存配置
        """
        self.__config=congig
        return self

    
    def __seltype(self,types):
        """选择缓存"""
        # m = hashlib.md5()
        # b = self.__name.encode(encoding='utf-8')
        # m.update(b)
        self.__name=md5(self.__name)
        if self.__config['type'] == 'File':
            if types == 'set':
                return self.__setfilecache()
            elif types=='get':
                return self.__getfilecache()
            elif types=='del':
                return self.__delfilecache()
        elif self.__config['type'] == 'Redis':
            self.__setredisobj()
            if types == 'set':
                return self.__setrediscache()
            elif types=='get':
                return self.__getrediscache()
            elif types=='del':
                return self.__delrediscache()
        # elif self.__config['type'] == 'MySql':
        #     self.__setmysqlonj()
        #     if types == 'set':
        #         return self.__setmysqlcache()
        #     elif types == 'get':
        #         return self.__getmysqlcache()
        #     elif types == 'del':
        #         return self.__delmysqlcache()
        elif self.__config['type'] == 'Python':
            if types == 'set':
                return self.__setpythoncache()
            elif types == 'get':
                return self.__getpythoncache()
            elif types == 'del':
                return self.__delpythoncache()
        else:
            raise Exception("缓存类型错误")
    def __setpythoncache(self):
        """设置python缓存
        
        return Boolean类型
        """
        data={
            'expire':self.__config['expire'],
            'time':times(),
            'values':self.__values
        }
        config.cachevalue[self.__name]=data
        return True
    def __getpythoncache(self):
        """获取python缓存
        
        return 缓存的值
        """
        try:
            ar=config.cachevalue[self.__name]
        except KeyError:
            return ""
        else:
            if ar['expire'] > 0:
                if (times()-ar['time']) > ar['expire']:
                    self.__delpythoncache()
                    return ""
                else:
                    return ar['values']
            else:
                return ar['values']
    def __delpythoncache(self):
        """删除python缓存
        
        return Boolean类型
        """
        try:
            del config.cachevalue[self.__name]
        except KeyError:
            pass
        return True
    # def __setmysqlcache(self): ########################################################################################
    #     """设置mysql缓存
        
    #     return Boolean类型
    #     """
    #     data=[str(self.__values)]
    #     strs="["
    #     for k in data:
    #         strs=strs+k
    #     strs=strs+"]"
    #     k=self.__mysqlobj.table('fanshukeji_core_cache').where("name",self.__name).count('id')
    #     self.__setmysqlonj()
    #     if k:
    #         return self.__mysqlobj.table('fanshukeji_core_cache').where("name",self.__name).update({"val":strs,"expire":self.__config['expire'],"time":times()})
    #     else:
    #         return self.__mysqlobj.table('fanshukeji_core_cache').insert({"name":self.__name,"val":strs,"expire":self.__config['expire'],"time":times()})
    # def __getmysqlcache(self):
    #     """获取mysql缓存
        
    #     return 缓存的值
    #     """
    #     data=self.__mysqlobj.table('fanshukeji_core_cache').where("name",self.__name).find()
    #     if data :
    #         if data['expire']>0 and times()-data['time']>data['expire']:
    #             self.__setmysqlonj()
    #             self.__mysqlobj.table('fanshukeji_core_cache').where("name",self.__name).delete()
    #             return False
    #         else:
    #             return eval(data['val'])[0]
    #     else:
    #         return False
    # def __delmysqlcache(self):
    #     """删除mysql缓存
        
    #     return Boolean类型
    #     """
    #     return self.__mysqlobj.table('fanshukeji_core_cache').where("name",self.__name).delete()
    def __setrediscache(self):
        """设置redis缓存
        
        return Boolean类型
        """
        # print(self.__redisobj)
        data=[self.__values]
        try:
            if self.__config['expire']:
                self.__redisobj.set(self.__name,str(data),self.__config['expire'])
            else:
                self.__redisobj.set(self.__name,str(data))
        except:
            return False
        return True
    def __getrediscache(self):
        """获取redis缓存
        
        return 缓存的值
        """
        lists=self.__redisobj.get(self.__name)
        if lists:
            data=eval(lists)
            return data[0]
        else:
            return False
    def __delrediscache(self):
        """删除redis缓存
        
        return int类型
        """
        return self.__redisobj.delete(self.__name)
    def __setfilecache(self):
        """设置文件缓存
        
        return Boolean类型
        """
        data={
            'expire':self.__config['expire'],
            'time':times(),
            'values':self.__values
        }
        if not os.path.exists(self.__config['path']):
            os.makedirs(self.__config['path']) #多层创建目录
        f=open(self.__config['path']+"/"+self.__name,"w")
        f.write(str(data))
        f.close()
        return True
    def __getfilecache(self):
        """获取文件缓存
        
        return 缓存的值
        """
        try:
            f=open(self.__config['path']+"/"+self.__name,"r")
        except Exception:
            return ""
        json_str=f.read()
        f.close()
        ar=json_decode(json_str)
        
        if ar['expire'] > 0:
            if (times()-ar['time']) > ar['expire']:
                
                self.__delfilecache()
                return ""
            else:
                return ar['values']
        else:
            return ar['values']
    def __delfilecache(self):
        """删除文件缓存
        
        return Boolean类型
        """
        if not os.path.exists(self.__config['path']+"/"+self.__name):
            return True
        try:
            os.remove(self.__config['path']+"/"+self.__name)
        except:
            return False
        return True