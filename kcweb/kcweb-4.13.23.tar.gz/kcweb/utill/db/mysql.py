# -*- coding: utf-8 -*-
from .pymysql import connect,escape_string
# import config.conf as config
import kcweb.config as config
import time,traceback,decimal,random,copy,hashlib
from kcweb.utill.cache import cache as kcwcache
mycache=copy.deepcopy(config.cache)
mycache['type']='Python'

dbconfig=config.database
def md5(strs):
    """md5加密"""
    if not strs:
        return strs
    m = hashlib.md5()
    b = strs.encode(encoding='utf-8')
    m.update(b)
    return m.hexdigest()
class mysql:
    """数据库实例"""
    __config=dbconfig
    __conn={} #数据库链接对象
    __connlists=[] #短连接列表  用于关闭
    __cursor=None #游标对象
    __errorcount=dbconfig['break'] #允许最大链接错误次数
    __errorcounts=0 #默认链接错误次数 
    __dbObjcount=dbconfig['dbObjcount'] #数据库链接实例数量
    __sql=''
    __sqls=''
    __masteridentifier='' # 主服务器标识
    __slaveidentifier='' # 从服务器标识
    def __del__(self):
        pass
    def close(self):
        "关闭连接,web一下模式下该方法无需理会，框架自动完成"
        if not self.__config['pattern'] and mysql.__conn:
            if self.__connlists:
                for k in self.__connlists:
                    try:
                        mysql.__conn[k].close()
                    except Exception as e:
                        if self.__config['debug']:
                            print("mysql短连接关闭失败",str(e),k)
                    else:
                        if self.__config['debug']:
                            print("mysql短连接关闭成功",k)
                mysql.__connlists=[]
                mysql.__conn={}
            elif isinstance(mysql.__conn,dict):
                i=0
                for thost in self.__config['host']:
                    identifier=thost+str(self.__config['port'][i])+self.__config['user'][i]+self.__config['password'][i]+self.__config['db'][i]
                    # print(mysql.__conn)
                    for k in mysql.__conn[identifier]:
                        try:
                            k['obj'].close()
                            if self.__config['debug']:
                                print("mysql短连接已关闭",k)
                        except Exception as e:
                            if self.__config['debug']:
                                print("mysql短连接关闭失败",str(e),k)
                    i+=1
                mysql.__conn={}
                self.__connlists=[]
            elif isinstance(mysql.__conn,object):
                mysql.__conn[self.__masteridentifier].close()
                mysql.__conn={}
                if self.__config['debug']:
                    print("mysql短连接已关闭",mysql.__conn)
        mysql.__config=copy.deepcopy(dbconfig)
    __dbcount=1
    def __setdbcount(self):
        "设置数据库配置总数量"
        if isinstance(self.__config['host'],str):
            self.__config['host']=[self.__config['host']]
        if isinstance(self.__config['port'],str):
            self.__config['port']=[self.__config['port']]
        if isinstance(self.__config['user'],str):
            self.__config['user']=[self.__config['user']]
        if isinstance(self.__config['password'],str):
            self.__config['password']=[self.__config['password']]
        if isinstance(self.__config['db'],str):
            self.__config['db']=[self.__config['db']]
        host=len(self.__config['host'])
        port=len(self.__config['port'])
        user=len(self.__config['user'])
        password=len(self.__config['password'])
        db=len(self.__config['db'])
        lists=[host,port,user,password,db]
        lists.sort()
        self.__dbcount=lists[0]
    def __closeconn(self,identifier):
        "长链接模式下，关闭链接池的链接"
        if self.__config['pattern']:
            if identifier in mysql.__conn:
                for k in mysql.__conn[identifier]:
                    try:
                        k['obj'].close()
                        if self.__config['debug']:
                            print("mysql长连接关闭成功",k)
                    except Exception as e:
                        if self.__config['debug']:
                            print(k,"mysql长连接关闭失败",str(e))
                mysql.__conn[identifier]=[]
    __dbobjident=None #集中式(单一服务器)并且长连接模式下随机服务器链接标识  和 分布式(主从服务器)模式下随机服务器链接标识
    def __connects(self,typess="DQL"):
        """设置数据库链接
        
        参数 typess ：数据查询语言DQL，数据操纵语言DML，数据定义语言DDL，数据控制语言DCL
        """
        try:
            if self.__config['deploy']==0: # 集中式(单一服务器)
                if self.__config['pattern']: # 长连接情况下
                    self.__masteridentifier=self.__config['host'][0]+str(self.__config['port'][0])+self.__config['user'][0]+self.__config['password'][0]+self.__config['db'][0] # 服务器标识
                    if self.__masteridentifier not in mysql.__conn or len(mysql.__conn[self.__masteridentifier])<1:
                        i=0
                        masterlistsdb=[]
                        while i<self.__dbObjcount: #创建self.__dbObjcount个数据库链接实例
                            obj=connect(host=self.__config['host'][0], port=self.__config['port'][0], user=self.__config['user'][0], password=self.__config['password'][0], db=self.__config['db'][0], charset=self.__config['charset'])
                            objar={"obj":obj,"error":0}
                            masterlistsdb.append(objar)
                            i=i+1
                        mysql.__conn[self.__masteridentifier]=masterlistsdb
                        if self.__config['debug']:
                            print("第%s次创建数据库链接对象，长连接模式" % (self.__errorcounts+1))
                else:
                    self.__masteridentifier=self.__config['host'][0]+str(self.__config['port'][0])+self.__config['user'][0]+self.__config['password'][0]+self.__config['db'][0] # 服务器标识
                    try:
                        mysql.__conn[self.__masteridentifier]
                    except KeyError: # 铺获未知异常
                        mysql.__conn[self.__masteridentifier]=connect(host=self.__config['host'][0], port=self.__config['port'][0], user=self.__config['user'][0], password=self.__config['password'][0], db=self.__config['db'][0], charset=self.__config['charset'])
                        self.__connlists.append(self.__masteridentifier)
                        if self.__config['debug']:
                            print("mysql短连接已创建",self.__masteridentifier,mysql.__conn[self.__masteridentifier])
            elif self.__config['deploy']==1: # 分布式(主从服务器)
                if self.__config['pattern']: # 长连接情况下
                    j=0
                    self.__masteridentifier=''
                    while j < self.__config['master_num']:
                        self.__masteridentifier=self.__masteridentifier+self.__config['host'][j]+str(self.__config['port'][j])+self.__config['user'][j]+self.__config['password'][j]+self.__config['db'][j] # 主服务器标识
                        j=j+1
                    j=self.__config['master_num']
                    self.__slaveidentifier=''
                    while j < self.__dbcount:
                        self.__slaveidentifier=self.__slaveidentifier+self.__config['host'][j]+str(self.__config['port'][j])+self.__config['user'][j]+self.__config['password'][j]+self.__config['db'][j] # 从服务器标识
                        j=j+1
                    if self.__masteridentifier not in mysql.__conn or len(mysql.__conn[self.__masteridentifier])<self.__config['master_num']:
                        j=0
                        masterlistsdb=[] #主服务器实例
                        while j < self.__config['master_num']: #主服务器数量
                            i=0
                            while i<self.__dbObjcount: #创建self.__dbObjcount个数据库链接实例
                                obj=connect(host=self.__config['host'][j], port=self.__config['port'][j], user=self.__config['user'][j], password=self.__config['password'][j], db=self.__config['db'][j], charset=self.__config['charset'])
                                objar={"obj":obj,"error":0}
                                masterlistsdb.append(objar)
                                i=i+1
                            j=j+1
                        mysql.__conn[self.__masteridentifier]=masterlistsdb
                        if self.__config['debug']:
                            print("%d次创建数据库链接对象，长连接模式（主）" % (self.__errorcounts+1))
                    if self.__slaveidentifier not in mysql.__conn or len(mysql.__conn[self.__slaveidentifier])<self.__dbcount-self.__config['master_num']:
                        
                        j=self.__config['master_num']
                        slaveerlistsdb=[] #从服务器实例
                        while j < self.__dbcount: #从服务器数量
                            i=0
                            while i<self.__dbObjcount: #创建self.__dbObjcount个数据库链接实例
                                obj=connect(host=self.__config['host'][j], port=self.__config['port'][j], user=self.__config['user'][j], password=self.__config['password'][j], db=self.__config['db'][j], charset=self.__config['charset'])
                                objar={"obj":obj,"error":0}
                                slaveerlistsdb.append(objar)
                                i=i+1
                            j=j+1
                        mysql.__conn[self.__slaveidentifier]=slaveerlistsdb
                        if self.__config['debug']:
                            print("%d创建数据库链接对象，长连接模式（从）" % (self.__errorcounts+1))
                else:
                    if typess == "DQL": #数据查询语言DQL
                        if self.__config['master_dql']: #所有服务器随机
                            self.__dbobjident=random.randint(0,self.__dbcount-1)
                            self.__masteridentifier=self.__config['host'][self.__dbobjident]+str(self.__config['port'][self.__dbobjident])+self.__config['user'][self.__dbobjident]+self.__config['password'][self.__dbobjident]+self.__config['db'][self.__dbobjident] # 服务器标识
                            try:
                                mysql.__conn[self.__masteridentifier]
                            except KeyError:
                                mysql.__conn[self.__masteridentifier]=connect(host=self.__config['host'][self.__dbobjident], 
                                    port=self.__config['port'][self.__dbobjident], 
                                    user=self.__config['user'][self.__dbobjident], 
                                    password=self.__config['password'][self.__dbobjident], 
                                    db=self.__config['db'][self.__dbobjident], 
                                    charset=self.__config['charset']
                                )
                                self.__connlists.append(self.__masteridentifier)
                                if self.__config['debug']:
                                    print("创建所有数据库链接对象",(self.__errorcounts+1),self.__config['host'][self.__dbobjident])
                        else: #从服务器随机
                            self.__dbobjident=random.randint(self.__config['master_num'],self.__dbcount-1)
                            self.__masteridentifier=self.__config['host'][self.__dbobjident]+str(self.__config['port'][self.__dbobjident])+self.__config['user'][self.__dbobjident]+self.__config['password'][self.__dbobjident]+self.__config['db'][self.__dbobjident] # 服务器标识
                            try:
                                mysql.__conn[self.__masteridentifier]
                            except KeyError:
                                mysql.__conn[self.__masteridentifier]=connect(host=self.__config['host'][self.__dbobjident], 
                                    port=self.__config['port'][self.__dbobjident], 
                                    user=self.__config['user'][self.__dbobjident], 
                                    password=self.__config['password'][self.__dbobjident], 
                                    db=self.__config['db'][self.__dbobjident], 
                                    charset=self.__config['charset']
                                )
                                self.__connlists.append(self.__masteridentifier)
                                if self.__config['debug']:
                                    print("创建从数据库链接对象",str(self.__errorcounts+1),self.__config['host'][self.__dbobjident],str(self.__config['db'][self.__dbobjident]))
                    else:
                         #从服务器随机
                        self.__dbobjident=random.randint(self.__config['master_num'],self.__dbcount-1)
                        self.__masteridentifier=self.__config['host'][self.__dbobjident]+str(self.__config['port'][self.__dbobjident])+self.__config['user'][self.__dbobjident]+self.__config['password'][self.__dbobjident]+self.__config['db'][self.__dbobjident] # 服务器标识
                        try:
                            mysql.__conn[self.__masteridentifier]
                        except KeyError: 
                            mysql.__conn[self.__masteridentifier]=connect(host=self.__config['host'][self.__dbobjident], 
                                port=self.__config['port'][self.__dbobjident], 
                                user=self.__config['user'][self.__dbobjident], 
                                password=self.__config['password'][self.__dbobjident], 
                                db=self.__config['db'][self.__dbobjident], 
                                charset=self.__config['charset']
                            )
                            self.__connlists.append(self.__masteridentifier)
                            if self.__config['debug']:
                                print("创建从数据库链接对象" , (self.__errorcounts+1),self.__config['host'][self.__dbobjident],str(self.__config['db'][self.__dbobjident]))
                    
        except Exception as e: # 铺获未知异常
            try:
                errcome=tuple(eval(str(e)))[0]
            except Exception as e: # 铺获未知异常
                raise Exception(e)
            if errcome == 2003: #如果数据库链接失败
                # self.__closeconn(self.__masteridentifier)
                # self.__closeconn(self.__slaveidentifier)
                if self.__config['cli']:
                    time.sleep(10)
                    self.__errorcounts=self.__errorcounts+1
                    if self.__errorcounts<self.__errorcount*300:
                        if self.__config['debug']:
                            print("无法链接到数据库服务器，准备第%d次重新链接:%s" % (self.__errorcounts,e))
                        self.__connects(typess)
                    else:
                        # self.__config=copy.deepcopy(dbconfig)
                        self.__errorcounts=0
                        raise Exception(e)
                else:
                    self.__errorcounts=self.__errorcounts+1
                    if self.__errorcounts<self.__errorcount:
                        if self.__config['debug']:
                            print("无法链接到数据库服务器，开始重新链接")
                        self.__connects(typess)
                    else:
                        # self.__config=copy.deepcopy(dbconfig)
                        self.__errorcounts=0
                        raise Exception(e)
            else:
                raise Exception(e)
        else:
            self.__errorcounts=0

    def connect(self,config):
        """设置数据库链接信息 

        参数 config 参考配置信息格式  可以设置数据库名（以字符串形式）

        返回 mysql对象
        """ 
        if config:
            if isinstance(config,dict):
                if "type" in config:
                    self.__config['type']=config['type']
                if "host" in config:
                    self.__config['host']=config['host']
                if "port" in config:
                    self.__config['port']=config['port']
                if "user" in config:
                    self.__config['user']=config['user']
                if "password" in config:
                    self.__config['password']=config['password']
                if "db" in config:
                    self.__config['db']=config['db']
                if "charset" in config:
                    self.__config['charset']=config['charset']
                if "pattern" in config:
                    self.__config['pattern']=config['pattern']
                if "cli" in config:
                    self.__config['cli']=config['cli']
                if "dbObjcount" in config:
                    self.__config['dbObjcount']=config['dbObjcount']
                if "deploy" in config:
                    self.__config['deploy']=config['deploy']
                if "master_num" in config:
                    self.__config['master_num']=config['master_num']
                if "master_dql" in config:
                    self.__config['master_dql']=config['master_dql']
                if "break" in config:
                    self.__config['break']=config['break']
            elif isinstance(config,str):
                self.__config['db']=[]
                i=0
                if not self.__dbcount:
                    self.__dbcount=len(self.__config['host'])
                while i<self.__dbcount:
                    self.__config['db'].append(config)
                    i=i+1
            else:
                print("config类型错误，设置连接不生效")
        return self
    __table=""
    def table(self,table):
        """设置表名

        参数 table：str 表名
        """
        self.__table=table
        return self
    __patternerrorcount=0 # 长连接情况下 错误次数
    def __setcursor(self,typess='DQL'):
        """设置游标

        参数 type ：数据查询语言DQL，数据操纵语言DML，数据定义语言DDL，数据控制语言DCL
        """
        self.__setdbcount()
        # self.__DBsingle=self.__config['pattern']
        self.__dbObjcount=self.__config['dbObjcount']
        self.__errorcount=self.__config['break']
        self.__connects()
        bs=''
        try:
            if self.__config['deploy']==0: # 集中式(单一服务器)
                if self.__config['pattern']: # 长连接情况下
                    bs=self.__masteridentifier
                    # types='master'
                    self.__dbobjident=random.randint(0, self.__dbObjcount-1)
                    self.__cursor=self.__conn[self.__masteridentifier][self.__dbobjident]['obj'].cursor() #获取随机数据库链接实例
                else:
                    self.__cursor=self.__conn[self.__masteridentifier].cursor() #获取随机数据库链接实例
            elif self.__config['deploy']==1: # 分布式(主从服务器)
                if self.__config['pattern']: # 长连接情况下
                    bs=self.__masteridentifier
                    slavecount=self.__dbcount-self.__config['master_num'] #从服务器数量
                    # types='master'
                    if typess=='DQL': #数据查询语言DQL
                        if self.__config['master_dql']:  #主服务器可以执行DQL
                            if slavecount:
                                if random.randint(0,1):
                                    bs=self.__masteridentifier
                                    # types='master'
                                    self.__dbobjident=random.randint(0,self.__dbObjcount*self.__config['master_num']-1)
                                    self.__cursor=self.__conn[self.__masteridentifier][self.__dbobjident]['obj'].cursor() #获取随机数据库链接实例 主服务器
                                else:
                                    bs=self.__slaveidentifier
                                    # types='slave'
                                    self.__dbobjident=random.randint(0,self.__dbObjcount*slavecount-1)
                                    self.__cursor=self.__conn[self.__slaveidentifier][self.__dbobjident]['obj'].cursor() #获取随机数据库链接实例 从服务器
                            else:
                                bs=self.__masteridentifier
                                # types='master'
                                self.__dbobjident=random.randint(0,self.__dbObjcount*self.__config['master_num']-1)
                                self.__cursor=self.__conn[self.__masteridentifier][self.__dbobjident]['obj'].cursor() #获取随机数据库链接实例 主服务器
                        else:
                            bs=self.__slaveidentifier
                            # types='slave'
                            self.__dbobjident=random.randint(0,self.__dbObjcount*slavecount-1)
                            self.__cursor=self.__conn[self.__slaveidentifier][self.__dbobjident]['obj'].cursor() #获取随机数据库链接实例 从服务器
                    else: #数据操纵语言DML，数据定义语言DDL，数据控制语言DCL
                        bs=self.__masteridentifier
                        # types='master'
                        self.__dbobjident=random.randint(0,self.__dbObjcount*self.__config['master_num']-1)
                        self.__cursor=self.__conn[self.__masteridentifier][self.__dbobjident]['obj'].cursor() #获取随机数据库链接实例 主服务器
                    self.__conn[bs][self.__dbobjident]['error']=0
                else:
                    self.__cursor=self.__conn[self.__masteridentifier].cursor()
        except Exception as e: # 铺获未知异常
            raise Exception(e)
        else:
            self.__patternerrorcount=0
            return self.__cursor
    
    def get_exec_cursor(self):
        """获取执行游标（不推荐使用）
        
        参数 type ：数据查询语言DQL，数据操纵语言DML，数据定义语言DDL，数据控制语言DCL
        """
        cursor=self.__setcursor("DML")
        return cursor
    def get_query_cursor(self):
        """获取查询游标（不推荐使用）
        
        参数 type ：数据查询语言DQL，数据操纵语言DML，数据定义语言DDL，数据控制语言DCL
        """
        cursor=self.__setcursor("DQL")
        return cursor
    def __execute(self,typess='DQL'):
        """执行sql语句
        
        参数 type ：数据查询语言DQL，数据操纵语言DML，数据定义语言DDL，数据控制语言DCL
        """
        self.__setdbcount()
        # self.__DBsingle=self.__config['pattern']
        self.__dbObjcount=self.__config['dbObjcount']
        self.__errorcount=self.__config['break']
        self.__connects()
        try:
            if self.__config['deploy']==0: # 集中式(单一服务器)
                if self.__config['pattern']: # 长连接情况下
                    bs=self.__masteridentifier
                    types='master'
                    self.__dbobjident=random.randint(0, self.__dbObjcount-1)
                    self.__cursor=self.__conn[self.__masteridentifier][self.__dbobjident]['obj'].cursor() #获取随机数据库链接实例
                    res=self.__cursor.execute(self.__sql)
                else:
                    self.__cursor=self.__conn[self.__masteridentifier].cursor() #获取随机数据库链接实例
                    res=self.__cursor.execute(self.__sql)
            elif self.__config['deploy']==1: # 分布式(主从服务器)
                if self.__config['pattern']: # 长连接情况下
                    bs=self.__masteridentifier
                    slavecount=self.__dbcount-self.__config['master_num'] #从服务器数量
                    types='master'
                    if typess=='DQL': #数据查询语言DQL
                        if self.__config['master_dql']:  #主服务器可以执行DQL
                            if slavecount:
                                if random.randint(0,1):
                                    bs=self.__masteridentifier
                                    types='master'
                                    self.__dbobjident=random.randint(0,self.__dbObjcount*self.__config['master_num']-1)
                                    self.__cursor=self.__conn[self.__masteridentifier][self.__dbobjident]['obj'].cursor() #获取随机数据库链接实例 主服务器
                                else:
                                    bs=self.__slaveidentifier
                                    types='slave'
                                    self.__dbobjident=random.randint(0,self.__dbObjcount*slavecount-1)
                                    self.__cursor=self.__conn[self.__slaveidentifier][self.__dbobjident]['obj'].cursor() #获取随机数据库链接实例 从服务器
                            else:
                                bs=self.__masteridentifier
                                types='master'
                                self.__dbobjident=random.randint(0,self.__dbObjcount*self.__config['master_num']-1)
                                self.__cursor=self.__conn[self.__masteridentifier][self.__dbobjident]['obj'].cursor() #获取随机数据库链接实例 主服务器
                        else:
                            bs=self.__slaveidentifier
                            types='slave'
                            self.__dbobjident=random.randint(0,self.__dbObjcount*slavecount-1)
                            self.__cursor=self.__conn[self.__slaveidentifier][self.__dbobjident]['obj'].cursor() #获取随机数据库链接实例 从服务器
                    else: #数据操纵语言DML，数据定义语言DDL，数据控制语言DCL
                        bs=self.__masteridentifier
                        types='master'
                        self.__dbobjident=random.randint(0,self.__dbObjcount*self.__config['master_num']-1)
                        self.__cursor=self.__conn[self.__masteridentifier][self.__dbobjident]['obj'].cursor() #获取随机数据库链接实例 主服务器
                    res=self.__cursor.execute(self.__sql)
                    self.__conn[bs][self.__dbobjident]['error']=0
                else:
                    self.__cursor=self.__conn[self.__masteridentifier].cursor()
                    res=self.__cursor.execute(self.__sql)
        except Exception as e: # 铺获未知异常
            try:
                errorcodes=tuple(eval(str(e)))[0]
            except:
                errorcodes=0
            if errorcodes == 2013 or errorcodes == 2006 or errorcodes == 2003 or errorcodes == 1053 or errorcodes == 0:  #2013连接丢失、2003数据库无法连接时、1053连接正在被关闭时、2006服务器丢失
                if self.__config['pattern']: # 长连接情况下
                    if self.__config['cli']==True:
                        if self.__config['debug']:
                            print("等待连接数据库")
                        if self.__patternerrorcount>self.__config['dbObjcount'] * self.__dbcount: #长连接情况下如果错误次数超过数据实例数量 关闭使用连接进行重连接
                            self.__patternerrorcount=0
                            if self.__config['deploy'] == 1: #分布式(主从服务器) 情况下
                                if self.__config['debug']:
                                    print("数据库连接失效，关闭主从连接池后重新连接")
                                self.__closeconn(self.__masteridentifier)
                                self.__closeconn(self.__slaveidentifier)
                                time.sleep(10)
                                self.__connects(typess)
                                self.__execute(typess)
                            else:
                                if self.__config['debug']:
                                    print("数据库连接失效，关闭主连接池后重新连接")
                                self.__closeconn(self.__masteridentifier)
                                time.sleep(10)
                                self.__connects(typess)
                                self.__execute(typess)
                        else:
                            self.__patternerrorcount=self.__patternerrorcount+1
                            self.__execute(typess)
                    else:
                        self.__conn[bs][self.__dbobjident]['error']=self.__conn[bs][self.__dbobjident]['error']+1 #当前数据库连接实例异常错误数量
                        if self.__conn[bs][self.__dbobjident]['error'] > 0:
                            try:
                                # mysql.__conn[bs][self.__dbobjident]['obj'].close() #关闭当前实例
                                self.__closeconn(bs)
                            except Exception as e:
                                if self.__config['debug']:
                                    print("关闭异常",e)
                            else:
                                self.__connects(typess)
                                self.__execute(typess)
                else: # 短连接情况下
                    if self.__config['debug']:
                        print("服务器正在被关闭，关闭当前连接后重试")
                    try:
                        del mysql.__conn[self.__masteridentifier]
                        mysql.__conn[self.__masteridentifier].close() #关闭当前实例
                    except Exception as e:
                        if self.__config['debug']:
                            print("关闭异常",e)
                    self.__connects(typess)
                    self.__execute(typess)
            else:
                raise Exception(e)
        else:
            self.__patternerrorcount=0
            return res

    def query(self,sql):
        """执行sql语句 注：只支持单一服务器模式

        参数 sql 字符串

        返回 列表  或  数字
        """
        self.__sql=sql
        res=self.__execute('DQL')
        description=self.__cursor.description #获取字段
        result = self.__cursor.fetchall() #获取查询结果
        self.__cursor.close()
        self.__None()
        if description is None:
            return res
        else:
            lists=[]
            data_dict=[]
            for field in description:#获取字段
                data_dict.append(field[0])
            for k in result:
                i=0
                dicts={}
                for j in k:
                    dicts[data_dict[i]]=j
                    i=i+1
                lists.append(dicts)
            return lists
    def execute(self,sql):
        """执行sql语句 注：只支持单一服务器模式

        参数 sql 字符串

        返回 列表  或  数字
        """
        self.__sql=sql
        res=self.__execute('DML')
        description=self.__cursor.description #获取字段
        result = self.__cursor.fetchall() #获取查询结果
        self.__cursor.close()
        self.__None()
        if description is None:
            return res
        else:
            lists=[]
            data_dict=[]
            for field in description:#获取字段
                data_dict.append(field[0])
            for k in result:
                i=0
                dicts={}
                for j in k:
                    dicts[data_dict[i]]=j
                    i=i+1
                lists.append(dicts)
            return lists
    def select(self,id=None):
        """select查询 

        返回 list(列表)
        """
        if id :
            self.__where="id=%d" % id
        self.__setsql()
        if self.__buildSql:
            self.__sqls="("+self.__sql+")"
            self.__None()
            return self.__sqls
        if self.__cache and self.__cache[0]:
            cou=kcwcache.cache().set_config(mycache).get_cache(md5(self.__sql+str(self.__config['db'][0])+str(self.__config['host'][0])))
            if cou:
                self.__None()
                return cou
        self.__execute()
        description=self.__cursor.description #获取字段
        result = self.__cursor.fetchall() #获取查询结果
        self.__cursor.close()
        # self.__None()
        lists=[]
        keys =[]
        for field in description:#获取字段
            keys.append(field[0])
        key_number = len(keys)
        for row in result:
            item = dict()
            for q in range(key_number):
                k=row[q]
                if type(row[q])==decimal.Decimal:
                    k=float(row[q])
                item[keys[q]] = k
            lists.append(item)
        if lists and self.__cache and self.__cache[0]:
            kcwcache.cache().set_config(mycache).set_cache(md5(self.__sql+str(self.__config['db'][0])+str(self.__config['host'][0])),lists,self.__cache[1])
        self.__None()
        return lists
    def find(self,id=None):
        """查询一条记录
        
        返回 字典
        """
        if id :
            self.__where="id=%s" % id
        self.limit(1)
        self.__setsql()
        if self.__buildSql:
            self.__sqls="("+self.__sql+")"
            self.__None()
            return self.__sqls
        if self.__cache and self.__cache[0]:
            item=kcwcache.cache().set_config(mycache).get_cache(md5(self.__sql+str(self.__config['db'][0])+str(self.__config['host'][0])))
            if item:
                self.__None()
                return item
        self.__execute()
        description=self.__cursor.description #获取字段
        result = self.__cursor.fetchall() #获取查询结果
        self.__cursor.close()
        # self.__None()
        item = dict()
        keys =[]
        for field in description:#获取字段
            keys.append(field[0])
        key_number = len(keys)
        for row in result:
            for q in range(key_number):
                k=row[q]
                if type(row[q])==decimal.Decimal:
                    k=float(row[q])
                item[keys[q]] = k
        if item and self.__cache and self.__cache[0]:
            kcwcache.cache().set_config(mycache).set_cache(md5(self.__sql+str(self.__config['db'][0])+str(self.__config['host'][0])),item,self.__cache[1])
        self.__None()
        return item
    def value(self,field):
        """查询指定字段值
        
        返回 一个字段
        """
        self.__field=field
        self.limit(1)
        self.__setsql()
        if self.__buildSql:
            self.__sqls="("+self.__sql+")"
            self.__None()
            return self.__sqls
        if self.__cache and self.__cache[0]:
            cou=kcwcache.cache().set_config(mycache).get_cache(md5(self.__sql+str(self.__config['db'][0])+str(self.__config['host'][0])))
            if cou:
                self.__None()
                return cou
        self.__execute()
        result = self.__cursor.fetchall() #获取查询结果
        self.__cursor.close()
        # self.__None()
        strs=''
        if result:
            strs=result[0][0]
        if strs and self.__cache and self.__cache[0]:
            kcwcache.cache().set_config(mycache).set_cache(md5(self.__sql+str(self.__config['db'][0])+str(self.__config['host'][0])),strs,self.__cache[1])
        self.__None()
        return strs
    def count(self,field="*"):
        """查询数量
        
        返回 int 数字
        """
        self.__field=field
        self.__setsql('count')
        if self.__buildSql:
            self.__sqls="("+self.__sql+")"
            self.__None()
            return self.__sql
        if self.__cache and self.__cache[0]:
            cou=kcwcache.cache().set_config(mycache).get_cache(md5(self.__sql+str(self.__config['db'][0])+str(self.__config['host'][0])))
            if cou:
                self.__None()
                return cou
        self.__execute()
        result = self.__cursor.fetchall() #获取查询结果
        self.__cursor.close()
        if self.__group:
            cou=len(result)
        else:
            try:
                cou=int(result[0][0])
            except IndexError:
                cou=0
        # self.__None()
        if cou and self.__cache and self.__cache[0]:
            kcwcache.cache().set_config(mycache).set_cache(md5(self.__sql+str(self.__config['db'][0])+str(self.__config['host'][0])),cou,self.__cache[1])
        self.__None()
        return cou
    def max(self,field):
        """查询某字段的最大值
        
        返回 int 数字
        """
        self.__field=field
        self.__setsql('max')
        if self.__buildSql:
            self.__sqls="("+self.__sql+")"
            self.__None()
            return self.__sql
        if self.__cache and self.__cache[0]:
            cou=kcwcache.cache().set_config(mycache).get_cache(md5(self.__sql+str(self.__config['db'][0])+str(self.__config['host'][0])))
            if cou:
                self.__None()
                return cou
        self.__execute()
        result = self.__cursor.fetchall() #获取查询结果
        self.__cursor.close()
        cou=int(result[0][0])
        # self.__None()
        if cou and self.__cache and self.__cache[0]:
            kcwcache.cache().set_config(mycache).set_cache(md5(self.__sql+str(self.__config['db'][0])+str(self.__config['host'][0])),cou,self.__cache[1])
        self.__None()
        return cou
    def min(self,field):
        """查询某字段的最小值
        
        返回 int 数字
        """
        self.__field=field
        self.__setsql('min')
        if self.__buildSql:
            self.__sqls="("+self.__sql+")"
            self.__None()
            return self.__sql
        if self.__cache and self.__cache[0]:
            cou=kcwcache.cache().set_config(mycache).get_cache(md5(self.__sql+str(self.__config['db'][0])+str(self.__config['host'][0])))
            if cou:
                self.__None()
                return cou
        self.__execute()
        result = self.__cursor.fetchall() #获取查询结果
        self.__cursor.close()
        # self.__None()
        cou=int(result[0][0])
        if cou and self.__cache and self.__cache[0]:
            kcwcache.cache().set_config(mycache).set_cache(md5(self.__sql+str(self.__config['db'][0])+str(self.__config['host'][0])),cou,self.__cache[1])
        self.__None()
        return cou
    def avg(self,field):
        """查询某字段的平均值
        
        返回 int 数字
        """
        self.__field=field
        self.__setsql('avg')
        if self.__buildSql:
            self.__sqls="("+self.__sql+")"
            self.__None()
            return self.__sql
        if self.__cache and self.__cache[0]:
            cou=kcwcache.cache().set_config(mycache).get_cache(md5(self.__sql+str(self.__config['db'][0])+str(self.__config['host'][0])))
            if cou:
                self.__None()
                return cou
        self.__execute()
        result = self.__cursor.fetchall() #获取查询结果
        self.__cursor.close()
        # self.__None()
        cou=int(result[0][0])
        if cou and self.__cache and self.__cache[0]:
            kcwcache.cache().set_config(mycache).set_cache(md5(self.__sql+str(self.__config['db'][0])+str(self.__config['host'][0])),cou,self.__cache[1])
        self.__None()
        return cou
    def sum(self,field):
        """查询某字段之和
        
        返回 int 数字
        """
        self.__field=field
        self.__setsql('sum')
        if self.__buildSql:
            self.__sqls="("+self.__sql+")"
            self.__None()
            return self.__sql
        if self.__cache and self.__cache[0]:
            cou=kcwcache.cache().set_config(mycache).get_cache(md5(self.__sql+str(self.__config['db'][0])+str(self.__config['host'][0])))
            if cou:
                self.__None()
                return cou
        self.__execute()
        result = self.__cursor.fetchall() #获取查询结果
        self.__cursor.close()
        # self.__None()
        cou=result[0][0]
        if not cou:
            cou=0
        else:
            if self.__cache and self.__cache[0]:
                kcwcache.cache().set_config(mycache).set_cache(md5(self.__sql+str(self.__config['db'][0])+str(self.__config['host'][0])),cou,self.__cache[1])
        self.__None()
        return cou

    def setinc(self,field,key=1,affair=False):
        """更新字段增加
         
        参数 field 要更新的字段

        参数 key 字段需要加多少

        参数 affair 是否开启事务 True表示手动提交事务  False表示自动提交事务
        """
        data={"field":field,"key":key}
        self.__setsql('setinc',data)
        res=self.__execute('DML')
        if affair==False and self.__startTrans==False:
            if not self.__config['pattern']:
                self.__conn[self.__masteridentifier].commit()
            else:
                self.__conn[self.__masteridentifier][self.__dbobjident]['obj'].commit()
        self.__cursor.close()
        self.__None()
        return res
    def update(self,data,affair=False):
        """数据表更新
         
        参数 data 要更新的内容  格式：{"name":"测试","age":20}

        参数 affair 是否开启事务 True表示手动提交事务  False表示自动提交事务
        """
        self.__setsql('update',data)
        res=self.__execute('DML')
        if affair==False and self.__startTrans==False:
            if not self.__config['pattern']:
                self.__conn[self.__masteridentifier].commit()
            else:
                self.__conn[self.__masteridentifier][self.__dbobjident]['obj'].commit()
        self.__cursor.close()
        self.__None()
        return res
    def delete(self,affair=False):
        """数据表删除

        参数 affair 是否开启事务 True表示手动提交事务  False表示自动提交事务
        """
        self.__setsql('delete')
        if self.__where:
            res=self.__execute('DML')
        else:
            return 0
        if affair==False and self.__startTrans==False:
            if not self.__config['pattern']:
                self.__conn[self.__masteridentifier].commit()
            else:
                self.__conn[self.__masteridentifier][self.__dbobjident]['obj'].commit()
        self.__cursor.close()
        self.__None()
        return res
    def insert(self,dicts,affair=False):
        """插入数据库 单条插入或多条插入

        参数 dicts 要插入的内容 单条格式：{"name":"测试","age":20}  。     多条格式：[{"name":"测试","age":20},{"name":"测试","age":20}]
        
        参数 affair 是否开启事务 True表示手动提交事务  False表示自动提交事务

        返回插入的数量
        """
        self.__setsql('insert',dicts)
        res=self.__execute('DML')
        if affair==False and self.__startTrans==False:
            if not self.__config['pattern']:
                self.__conn[self.__masteridentifier].commit()
            else:
                self.__conn[self.__masteridentifier][self.__dbobjident]['obj'].commit()
        self.__cursor.close()
        self.__None()
        return res

    __startTrans=False
    def startTrans(self):
        "开启事务,仅对 update方法、delete方法、install方法有效"
        self.__startTrans=True
    def commit(self):
        """事务提交

        增删改后的任务进行提交
        """
        if self.__masteridentifier:
            if not self.__config['pattern']:
                self.__conn[self.__masteridentifier].commit()
            else:
                self.__conn[self.__masteridentifier][self.__dbobjident]['obj'].commit()

    def rollback(self):
        """事务回滚

        增删改后的任务进行撤销
        """
        if self.__masteridentifier:
            if not self.__config['pattern']:
                self.__conn[self.__masteridentifier].rollback()
            else:
                self.__conn[self.__masteridentifier][self.__dbobjident]['obj'].rollback()
    def getsql(self):
        """得到生成的sql语句"""
        return self.__sql
    __buildSql=None
    def buildSql(self):
        """构造子查询"""
        self.__buildSql=True
        return self
    def __None(self):
        "清除所有赋值条件"
        self.__lock=None
        self.__distinct=None
        self.__join=None
        self.__joinstr=''
        self.__alias=None
        self.__having=None
        self.__group=None
        self.__group1=None
        self.__order=None
        self.__order1=None
        self.__limit=None
        self.__field="*"
        self.__where=None
        self.__wheres=()
        self.__table=None
        self.__buildSql=None
        self.__table=None
        self.__cache=None
    
    __where=None
    __wheres=()
    def where(self,where = None,*wheres):
        """设置过滤条件

        传入方式:
        "id",2 表示id='2'

        "id","in",2,3,4,5,6,...表示 id in (2,3,4,5,6,...)

        "id","in",[2,3,4,5,6,...]表示 id in (2,3,4,5,6,...)


        [("id","gt",6000),"and",("name","like","%超")] 表示 ( id > "6000" and name LIKE "%超" )

        "id","eq",1 表示 id = '1'

        eq 等于
            neq 不等于
            gt 大于
            egt 大于等于
            lt 小于
            elt 小于等于
            like LIKE
        """
        self.__where=where
        self.__wheres=wheres
        return self
    __field='*'
    def field(self,field = "*"):
        """设置过滤显示条件

        参数 field：str 字符串
        """
        self.__field=field
        return self
    __limit=[]
    def limit(self,offset=1, length = None):
        """设置查询数量

        参数 offset：int 起始位置

        参数 length：int 查询数量
        """
        if not offset:
            offset=1
        offset=int(offset)
        if length:
            length=int(length)
        self.__limit=[offset,length]
        return self
    def page(self,pagenow=1, length = 20):
        """设置分页查询

        参数 pagenow：int 页码

        参数 length：int 查询数量
        """
        if not pagenow:
            pagenow=1
        if not length:
            length=20
        pagenow=int(pagenow)
        length=int(length)
        offset=(pagenow-1)*length
        self.__limit=[offset,length]
        return self
    __order=None
    __order1=None
    def order(self,strs=None,*strs1):
        """设置排序查询

        传入方式:

        "id desc"

        "id",'name','appkey','asc'

        "id",'name','appkey'   不包含asc或desc的情况下 默认是desc

        ['id','taskid',{"task_id":"desc"}]
        """
        self.__order=strs
        self.__order1=strs1
        return self
    __group=None
    __group1=None
    def group(self,strs=None,*strs1):
        """设置分组查询

        传入方式:

        "id,name"

        "id","name"
        """
        self.__group=strs
        self.__group1=strs1
        return self
    __having=None
    def having(self,strs=None):
        """用于配合group方法完成从分组的结果中筛选（通常是聚合条件）数据

        参数 strs：string 如："count(time)>3"
        """
        self.__having=strs
        return self
    __alias=None
    def alias(self,strs=None):
        """用于设置当前数据表的别名，便于使用其他的连贯操作例如join方法等。

        参数 strs：string 默认当前表作为别名
        """
        if strs:
            self.__alias=strs
        else:
            self.__alias=self.__table
        return self
    __join=None
    __joinstr=''
    def join(self,strs,on=None,types='INNER'):
        """用于根据两个或多个表中的列之间的关系，从这些表中查询数据

        参数 strs  string 如："test t1"   test表设置别名t1

        参数 on  string 如："t1.id=t2.pid"   设置连接条件

        参数 types  支持INNER、LEFT、RIGHT、FULL  默认INNER

        """
        joinstr=''
        if strs and on:
            joinstr=joinstr+types+" JOIN "+strs+" ON "+on+" "
        if joinstr:
            self.__joinstr=self.__joinstr+joinstr
        return self
    __distinct=None
    def distinct(self,bools=None):
        "用于返回唯一不同的值,配合field方法使用生效,来消除所有重复的记录，并只获取唯一一次记录。"
        self.__distinct=bools
        return self
    __lock=None
    def lock(self,strs=None):
        """用于数据库的锁机制，在查询或者执行操作的时候使用

        排他锁 (FOR UPDATE)

        共享锁 (lock in share mode)
        
        参数 strs  如：True表示自动在生成的SQL语句最后加上FOR UPDATE，

        
        """
        self.__lock=strs
        return self
   
    __cache=[]
    def cache(self,status=None,endtime=86400):
        """设置查询缓存
        status  缓存开关

        参数 endtime：int 缓存时间  0永久
        """
        self.__cache=[status,endtime]
        return self
    def __setsql(self,types=None,data = {}):
        """生成sql语句"""
        if types==None:
            self.__sql="SELECT"
            if self.__distinct and self.__field:
                self.__sql=self.__sql+" DISTINCT"
            if self.__alias:
                self.__sql=self.__sql+" %s FROM %s %s" % (self.__field,self.__table,self.__alias)
            else:
                self.__sql=self.__sql+" %s FROM %s" % (self.__field,self.__table)
        elif types=='count':
            self.__sql="SELECT COUNT(%s) FROM %s" % (self.__field,self.__table)
        elif types=='max':
            self.__sql="SELECT MAX(%s) FROM %s" % (self.__field,self.__table)
        elif types=='min':
            self.__sql="SELECT MIN(%s) FROM %s" % (self.__field,self.__table)
        elif types=='avg':
            self.__sql="SELECT AVG(%s) FROM %s" % (self.__field,self.__table)
        elif types=='sum':
            self.__sql="SELECT SUM(%s) FROM %s" % (self.__field,self.__table)
        elif types=='setinc':
            self.__sql="update %s set %s=%s+%s" % (self.__table,data['field'],data['field'],data['key'])
        elif types=='update':
            strs=''
            for k in data:
                if isinstance(data[k],str):
                    strs=strs+" %s = '%s' ," % (k,escape_string(data[k]))
                else:
                    strs=strs+" %s = %s ," % (k,data[k])
            strs=strs[:-1]
            self.__sql="UPDATE %s SET %s" % (self.__table,strs)
        elif types=='delete':
            self.__sql="DELETE FROM %s" % self.__table
        elif types=='insert':
            if isinstance(data,dict):
                strs=''
                val=''
                for k in data:
                    strs=strs+"%s," % k
                    if isinstance(data[k],str):
                        val=val+"'%s'," % escape_string(data[k])
                    else:
                        val=val+"%s," % data[k]
                strs=strs[:-1]
                val=val[:-1]
                self.__sql="INSERT INTO %s (%s) VALUES (%s)" % (self.__table,strs,val)
            elif isinstance(data,list):
                strs=''
                val='('
                for k in data[0]:
                    strs=strs+" , "+k
                for k in data:
                    for j in k:
                        if isinstance(k[j],str):
                            val=val+"'"+str(k[j])+"',"
                        else:
                            val=val+str(k[j])+","
                    val=val[:-1]
                    val=val+"),("
                val=val[:-2]
                self.__sql="INSERT INTO "+self.__table+" ("+strs[3:]+") VALUES "+val
        if self.__joinstr:
            self.__sql=self.__sql+" "+self.__joinstr
        if self.__where:
            if isinstance(self.__where,str):
                if self.__wheres:
                    if len(self.__wheres) == 2:
                        if isinstance(self.__wheres[1],list):
                            self.__sql=self.__sql + " WHERE %s %s (" % (self.__where,self.__operator(self.__wheres[0]))
                            for k in self.__wheres[1]:
                                self.__sql=self.__sql+str(k)+","
                            self.__sql=self.__sql[:-1]+")"
                        else:
                            self.__sql=self.__sql + " WHERE  %s %s '%s'" % (self.__where,self.__operator(self.__wheres[0]),self.__wheres[1])
                    elif len(self.__wheres) > 2:
                        if self.__wheres[0]=='in':
                            strs=str(self.__wheres[1])
                            i=0
                            for k in self.__wheres:
                                if i > 1:
                                    strs=strs+","+str(k)
                                i=i+1
                            self.__sql=self.__sql + " WHERE  %s in (%s)" % (self.__where,strs)
                    else:
                        self.__sql=self.__sql + " WHERE  %s = '%s'" % (self.__where,self.__wheres[0])
                else:
                    self.__sql=self.__sql + " WHERE  %s" % self.__where
            elif isinstance(self.__where,list):
                self.__sql=self.__sql + " WHERE  %s" % self.__listTrans()
            else:
                print("参数where类型错误")
        if self.__group:
            s=self.__group
            if self.__group1:
                for key in self.__group1:
                    s=s+","+key
            self.__sql=self.__sql+" GROUP BY "+s
        if self.__order:
            s=''
            if isinstance(self.__order,list):
                for strs in self.__order:
                    if isinstance(strs,str):
                        s=s+strs+","
                    else:
                        pass
                        for key in strs:
                            s=s+key+" "+strs[key]
                        s=s+","
                s=s[:-1]
            if isinstance(self.__order,str):
                if self.__order1:
                    if len(self.__order1) > 1:
                        if self.__order1[len(self.__order1)-1] == 'desc' or self.__order1[len(self.__order1)-1] == 'asc':
                            i=0
                            while i<len(self.__order1)-1:
                                s=s+self.__order1[i]+","
                                i=i+1
                            s=s[:-1]+" "+self.__order1[len(self.__order1)-1]
                        else:
                            for key in self.__order1:
                                s=s+key+","
                            s=s[:-1]
                            s=s+" asc"
                        s=self.__order+","+s
                    else:
                        s=s[:-1]+self.__order1[0]
                        s=self.__order+" "+s
                else:
                    s=self.__order
            self.__sql=self.__sql+" ORDER BY "+s
        if self.__having:
            self.__sql=self.__sql+" HAVING "+self.__having
        if self.__limit:
            if self.__limit[1]:
                self.__sql=self.__sql+" LIMIT %d,%d" % (self.__limit[0],self.__limit[1])
            else:
                self.__sql=self.__sql+" LIMIT %d" % self.__limit[0]
        if self.__lock:
            if isinstance(self.__lock,str):
                self.__sql=self.__sql+" "+self.__lock
            else:
                self.__sql=self.__sql+' FOR UPDATE'
    def __listTrans(self):
        """列表转换sql表达式
        返回 字符串
        """
        strs=''
        #[('id', 'eq', '1'), 'or', ('id', 'eq', '2')]
        for k in self.__where:
            if isinstance(k,tuple):
                t=0
                for j in k:
                    if t==0:
                        strs=strs+' '+str(j)+' '
                    elif t==1:
                        strs=strs+self.__operator(j)
                    if t==2:
                        strs=strs+' "'+str(j)+'" '
                    t=t+1
            elif isinstance(k,str):
                strs=strs+k
        return "("+strs+")"
    def __operator(self,strs):
        """运算符转换
        参数 strs 待转的字符串
        返回 已转换的运算符

        符号定义
            eq 等于
            neq 不等于
            gt 大于
            egt 大于等于
            lt 小于
            elt 小于等于
            like LIKE
        """
        strss=strs.upper()
        if strss == 'EQ':
            k='='
        elif strss == 'NEQ':
            k='<>'
        elif strss == 'GT':
            k='>'
        elif strss == 'EGT':
            k='>='
        elif strss == 'LT':
            k='<'
        elif strss == 'ELT':
            k='<='
        elif strss == 'LIKE':
            k='LIKE'
        else:
            k=strss
        return k