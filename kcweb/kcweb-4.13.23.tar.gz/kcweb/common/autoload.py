# -*- coding: utf-8 -*-
import time,hashlib,json,re,os,platform,sys,shutil,requests,importlib,traceback,pip,gzip,tarfile,zipfile,random,copy
import datetime as core_datetime
from kcweb import config
from kcweb.utill.dateutil.relativedelta import relativedelta as core_relativedelta
from kcweb.utill.db import mysql as kcwmysql
from kcweb.utill.db import mongodb as kcwmongodb
from kcweb.utill.db import sqlite as kcwsqlite
from kcweb.utill.cache import cache as kcwcache
from kcweb.utill.redis import redis as kcwredis
from kcweb.utill.http import Http
from kcweb.utill.queues import Queues
from kcweb.utill.db import model
from mako.template import Template as kcwTemplate
from mako.lookup import TemplateLookup
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from kcweb.utill import filetype
from . import globals

import asyncio,websockets,urllib,threading
class kcwebsocket:
    "websocket服务端"
    __clientlists=[] #所有客户端绑定的对象
    __lists=[] #所有客户端
    __group={} #组
    __uid={} #clientid绑定的uid
    async def bindUid(self,clientid,uid):
        """将clientid与uid绑定，以便通过sendToUid(uid)发送数据

        clientid 客户端id

        uid uid与client_id是一对多的关系，系统允许一个uid下有多个client_id
        """
        try:
            self.__uid[uid]
        except KeyError:
            self.__uid[uid]=[]
        self.__uid[uid].append(clientid)
    def unbindUid(self,clientid,uid):
        """将clientid与uid解绑 当clientid下线（连接断开）时会自动与uid解绑，开发者无需在onClose事件调用unbindUid
        
        clientid 客户端id

        uid 数字或者字符串
        """
        try:
            self.__uid[uid]
        except KeyError:
            pass
        else:
            try:
                self.__uid[uid].remove(clientid)
            except KeyError:
                pass
    async def sendToUid(self,uid,message):
        """向uid绑定的所有在线clientid发送数据

        uid uid可以是字符串、数字、或者包含uid的列表。如果为列表，则是给列表内所有uid发送数据

        message 要发送的数据（字符串类型）
        """
        if isinstance(uid,str):
            for clientid in self.__uid[uid]:
                await self.send_client(clientid,message)
        elif isinstance(uid,list):
            for k in uid:
                for clientid in self.__uid[k ]:
                    try:
                        await self.send_client(clientid,message)
                    except ValueError:
                        if config.app['app_debug']:
                            print("deluid",clientid)
                        self.__uid[uid].remove(clientid)
    async def joinGroup(self,clientid,group):
        """将clientid加入某个组
        
        clientid 客户端id

        Group 组名
        """
        try:
            self.__group[group]
        except KeyError:
            self.__group[group]=[]
        self.__group[group].append(clientid)
    async def leaveGroup(self,clientid,group):
        """将clientid从某个组中删除
        
        clientid 客户端id

        group 组名
        """
        try:
            self.__group[group]
        except KeyError:
            pass
        else:
            try:
                self.__group[group].remove(clientid)
            except KeyError:
                pass
    async def ungroup(self,group):
        """解散分组。 解散分组后所有属于这个分组的用户的连接将被移出分组，此分组将不再存在，除非再次调用 joinGroup

        group 组名
        """
        try:
            self.__group[group]
        except KeyError:
            pass
        else:
            del self.__group[group]
    async def sendToGroup(self,group,message,exclude_clientid=[]):
        """向某个分组的所有在线clientid发送数据。

        group 组名

        message 要发送的数据（字符串类型）

        exclude_clientid clientid组成的列表。exclude_clientid列表中指定的clientid将被排除在外，不会收到本次发的消息
        """
        try:
            self.__group[group]
        except KeyError:
            pass
        else:
            for client in self.__group[group]:
                if exclude_clientid:
                    for clientid in exclude_clientid:
                        if client!=clientid:
                            try:
                                await self.send_client(client,message)
                            except ValueError:
                                if config.app['app_debug']:
                                    print("delgroup",client)
                                self.__group[group].remove(client)
                else:
                    try:
                        await self.send_client(client,message)
                    except ValueError:
                        if config.app['app_debug']:
                            print("delgroup",client)
                        self.__group[group].remove(client)
    async def getClientIdCountByGroup(self,group):
        """获取某分组当前在线成连接数（多少clientid在线）
        
        group 组名

        return int 返回一个数字
        """
        try:
            self.__group[group]
        except KeyError:
            return 0
        else:
            return len(self.__group[group])
    def getAllClientIdCount(self):
        """获取当前在线连接总数（多少client_id在线）
        
        return int 返回一个数字
        """
        return len(self.__lists)
    async def send_all(self,message):
        "给所有人发送消息，包括自己"
        for l in self.__clientlists:
            try:
                await l['socket'].send(message)
            except:pass
    async def send_client(self,clientid,message):
        "给所指定客户端发送消息"
        xb=self.__lists.index(clientid)
        websockets=self.__clientlists[xb]['socket']
        try:
            await websockets.send(message)
        except:pass
    async def onConnect(self,clientid,params):
        "客户端发来连接时"
        if config.app['app_debug']:
            print("连接成功",clientid)
    async def onMessage(self,clientid,recv_text):
        "当客户端发来数据"
        await self.send_client(clientid,recv_text) #给当前用户发送消息
    async def onClose(self,clientid):
        "客户端与websocket的连接断开时触发"
        if config.app['app_debug']:
            print("onClose",clientid)
    async def __onClose(self,clientid):
        xb=self.__lists.index(clientid)
        del self.__lists[xb]
        del self.__clientlists[xb]
        if self.__uid:
            for uid in self.__uid.keys():
                try:
                    self.__uid[uid]
                except KeyError:
                    pass
                else:
                    try:
                        self.__uid[uid]['clientid']
                    except KeyError:
                        pass
                    else:
                        self.__uid[uid].remove(clientid)
    async def __main2(self,clientid,websocket,path):
        "服务器端主逻辑"
        async for message in websocket:
            await self.onMessage(clientid, message)
        await self.__onClose(clientid)
        await self.onClose(clientid)
    async def __main1(self,clientid,websocket,path):
        t = urllib.parse.parse_qs(urllib.parse.urlparse(path).query)
        params={}
        for key in t.keys():
            params[key]=t[key][0]
        await self.onConnect(clientid, params)
    async def __main(self,websocket,path):
        "服务器端主逻辑"
        clientid=md5(str(random.random()))
        self.__clientlists.append({"clientid":clientid,"socket":websocket})
        self.__lists.append(clientid)
        task1=asyncio.ensure_future(self.__main1(clientid,websocket,path))
        task2=asyncio.ensure_future(self.__main2(clientid,websocket,path))
        await task1
        await task2
    def start(self,ip='0.0.0.0',port='39020'):
        "启动websoeket服务"
        asyncio.set_event_loop(asyncio.new_event_loop()) # 防止出现RuntimeError
        asyncio.get_event_loop().run_until_complete(websockets.serve(self.__main,ip,port))
        asyncio.get_event_loop().run_forever()
# def start():
#     kwebsocket=kcwebsocket()
#     kwebsocket.start()


class DFAFilter():
    """DFA算法文字过滤器"""
    __sensitivelist=[]
    def __init__(self,sensitivelist):
        """
        sensitivelist 敏感字符串列表
        """
        self.keyword_chains = {}  # 关键词链表
        self.delimit = '\x00'  # 限定
        for keyword in sensitivelist:
            self.__add(str(keyword).strip())
    def __add(self, keyword):
        keyword = keyword.lower()  # 关键词英文变为小写
        chars = keyword.strip()  # 关键字去除首尾空格和换行
        if not chars:  # 如果关键词为空直接返回
            return
        level = self.keyword_chains
        # 遍历关键字的每个字
        for i in range(len(chars)):
            # 如果这个字已经存在字符链的key中就进入其子字典
            if chars[i] in level:
                level = level[chars[i]]
            else:
                if not isinstance(level, dict):
                    break
                for j in range(i, len(chars)):
                    level[chars[j]] = {}
                    last_level, last_char = level, chars[j]
                    level = level[chars[j]]
                last_level[last_char] = {self.delimit: 0}
                break
        if i == len(chars) - 1:
            level[self.delimit] = 0
    def filter(self, message, repl=""):
        """ 获取过滤后的字符串

        message 待处理的字符串

        repl 替换内容
        """
        message = message.lower()
        ret = []
        start = 0
        while start < len(message):
            level = self.keyword_chains
            step_ins = 0
            for char in message[start:]:
                if char in level:
                    step_ins += 1
                    if self.delimit not in level[char]:
                        level = level[char]
                    else:
                        ret.append(repl * step_ins)
                        start += step_ins - 1
                        break
                else:
                    ret.append(message[start])
                    break
            else:
                ret.append(message[start])
            start += 1
        return ''.join(ret)
    def sensitive(self,message):
        """ 判断字符串是否包含敏感

        message 待处理的字符串
        """
        if self.filter(message) == message:
            return True
        else:
            return False
redis=kcwredis()
def send_mail(user,text="邮件内容",theme="邮件主题",recNick="收件人昵称"):
    """发送邮件

    参数 user：接收邮件的邮箱地址

    参数 text：邮件内容

    参数 theme：邮件主题

    参数 recNick：收件人昵称

    return Boolean类型
    """
    ret=True
    if not theme:
        theme=config.email['theme']
    if not recNick:
        recNick=config.email['recNick']
    try:
        msg=MIMEText(text,'plain','utf-8')
        msg['From']=formataddr([config.email['sendNick'],config.email['sender']]) 
        msg['To']=formataddr([recNick,user]) 
        msg['Subject']=theme

        server=smtplib.SMTP_SSL("smtp.qq.com", 465) 
        server.login(config.email['sender'], config.email['pwd']) 
        server.sendmail(config.email['sender'],[user,],msg.as_string())
        server.quit()
    except Exception:
        ret=False
    return ret
get_sysinfodesffafew=None
def get_sysinfo():
    """获取系统信息

    return dict类型
    """
    global get_sysinfodesffafew
    if get_sysinfodesffafew:
        sysinfo=get_sysinfodesffafew
    else:
        sysinfo={}
        sysinfo['platform']=platform.platform()        #获取操作系统名称及版本号，'Linux-3.13.0-46-generic-i686-with-Deepin-2014.2-trusty'  
        sysinfo['version']=platform.version()         #获取操作系统版本号，'#76-Ubuntu SMP Thu Feb 26 18:52:49 UTC 2015'
        sysinfo['architecture']=platform.architecture()    #获取操作系统的位数，('32bit', 'ELF')
        sysinfo['machine']=platform.machine()         #计算机类型，'i686'
        sysinfo['node']=platform.node()            #计算机的网络名称，'XF654'
        sysinfo['processor']=platform.processor()       #计算机处理器信息，''i686'
        sysinfo['uname']=platform.uname()           #包含上面所有的信息汇总，('Linux', 'XF654', '3.13.0-46-generic', '#76-Ubuntu SMP Thu Feb 26 18:52:49 UTC 2015', 'i686', 'i686')
        sysinfo['start_time']=times()
        get_sysinfodesffafew=sysinfo
            # 还可以获得计算机中python的一些信息：
            # import platform
            # platform.python_build()
            # platform.python_compiler()
            # platform.python_branch()
            # platform.python_implementation()
            # platform.python_revision()
            # platform.python_version()
            # platform.python_version_tuple()
    return sysinfo
def Template(path,**context):
    "模板渲染引擎函数,使用配置的模板路径"
    return Templates(str(config.app['tpl_folder'])+str(path),**context)
def Templates(path,**context):
    "模板渲染引擎函数，需要完整的模板目录文件"
    lookup = TemplateLookup(directories=[''])
    # body=''
    # with open(path, 'r',encoding='utf-8') as f:
    #     contents=f.read()
    #     t=kcwTemplate(contents,lookup=lookup,module_directory=config.cache['path']+"/Template")
    #     body=t.render(**context)

    # t=kcwTemplate(filename=path,module_directory=config.cache['path']+"/Template",lookup=lookup)
    t=lookup.get_template(path)
    body=t.render(**context)
    return body
def getfunction(strs):
    """获取指定文件对象
    
    strs :app.index.common.autoload  获取app/index/common/目录下的autoload对象
    """
    return importlib.import_module(strs)
def mysql(table=None,configss=None):
    """mysql数据库操作实例
    
    参数 table：表名

    参数 configss 数据库配置  可以传数据库名字符串
    """
    dbs=kcwmysql.mysql()
    if table is None:
        return dbs
    elif configss:
        return dbs.connect(configss).table(table)
    else:
        return dbs.connect(config.database).table(table)
def sqlite(table=None,configss=None):
    """sqlite数据库操作实例
    
    参数 table：表名

    参数 configss 数据库配置  可以传数据库名字符串
    """
    dbs=kcwsqlite.sqlite()
    if table is None:
        return dbs
    elif configss:
        return dbs.connect(configss).table(table)
    else:
        return dbs.connect(config.sqlite).table(table)
def M(table=None,confi=None):
    """数据库操作实例
    
    参数 table：表名

    参数 confi 数据库配置  可以传数据库名字符串
    """
    if confi:
        if confi['type']=='sqlite':
            return sqlite(table,confi)
        else:
            return mysql(table,confi)
    else:
        if config.database['type']=='sqlite':
            return sqlite(table)
        else:
            return mysql(table)
def mongo(table=None,configss=None):
    """mongodb数据库操作实例
    
    参数 table：表名(mongodb数据库集合名)

    参数 configss mongodb数据库配置  可以传数据库名字符串
    """
    mObj=kcwmongodb.mongo()
    if table is None:
        return mObj
    elif configss:
        return mObj.connect(configss).table(table)
    else:
        return mObj.connect(config.mongo).table(table)
def is_index(params,index):
    """判断列表或字典里的索引是否存在

    params  列表或字典

    index   索引值

    return Boolean类型
    """
    try:
        params[index]
    except KeyError:
        return False
    except IndexError:
        return False
    else:
        return True
def set_cache(name,values,expire="no"):
    """设置缓存

    参数 name：缓存名

    参数 values：缓存值

    参数 expire：缓存有效期 0表示永久  单位 秒
    
    return Boolean类型
    """
    return kcwcache.cache().set_cache(name,values,expire)
def get_cache(name):
    """获取缓存

    参数 name：缓存名

    return 或者的值
    """
    return kcwcache.cache().get_cache(name)
def del_cache(name):
    """删除缓存

    参数 name：缓存名

    return Boolean类型
    """
    return kcwcache.cache().del_cache(name)
def md5(strs):
    """md5加密
    
    参数 strs：要加密的字符串

    return String类型
    """
    m = hashlib.md5()
    b = strs.encode(encoding='utf-8')
    m.update(b)
    return m.hexdigest()
def times():
    """生成时间戳整数 精确到秒(10位数字)
    
    return int类型
    """
    return int(time.time())
def json_decode(strs):
    """json字符串转python类型"""
    try:
        return json.loads(strs)
    except Exception:
        return []
def json_encode(strs):
    """python列表或字典转成字符串"""
    try:
        return json.dumps(strs,ensure_ascii=False)
    except Exception:
        return ""
def dateoperator(date,years=0,formats='%Y%m%d%H%M%S',months=0, days=0, hours=0, minutes=0,seconds=0,
                 leapdays=0, weeks=0, microseconds=0,
                 year=None, month=None, day=None, weekday=None,
                 yearday=None, nlyearday=None,
                 hour=None, minute=None, second=None, microsecond=None):
    """日期相加减计算
    date 2019-10-10
    formats 设置需要返回的时间格式 默认%Y%m%d%H%M%S
    
    years 大于0表示加年  反之减年
    months 大于0表示加月  反之减月
    days 大于0表示加日  反之减日

    return %Y%m%d%H%M%S
    """
    formatss='%Y%m%d%H%M%S'
    date=re.sub('[-年/月:：日 时分秒]','',date)
    if len(date) < 8:
        return None
    if len(date) < 14:
        s=14-len(date)
        i=0
        while i < s:
            date=date+"0"
            i=i+1
    d = core_datetime.datetime.strptime(date, formatss)
    strs=(d + core_relativedelta(years=years,months=months, days=days, hours=hours, minutes=minutes,seconds=seconds,
                 leapdays=leapdays, weeks=weeks, microseconds=microseconds,
                 year=year, month=month, day=day, weekday=weekday,
                 yearday=yearday, nlyearday=nlyearday,
                 hour=hour, minute=minute, second=second, microsecond=microsecond))
    strs=strs.strftime(formats)
    return strs
def get_folder():
    '获取当前框架目录'
    return os.path.split(os.path.realpath(__file__))[0][:-7] #当前框架目录
# aa=[]
def get_file(folder='./',is_folder=True,suffix="*",lists=[],append=False):
    """获取文件夹下所有文件夹和文件

    folder 要获取的文件夹路径

    is_folder  是否返回列表中包含文件夹

    suffix 获取指定后缀名的文件 默认全部
    """
    if not append:
        lists=[]
    lis=os.listdir(folder)
    for files in lis:
        if not os.path.isfile(folder+"/"+files):
            if is_folder:
                zd={"type":"folder","path":folder+"/"+files,'name':files}
                lists.append(zd)
            get_file(folder+"/"+files,is_folder,suffix,lists,append=True)
        else:
            if suffix=='*':
                zd={"type":"file","path":folder+"/"+files,'name':files}
                lists.append(zd)
            else:
                if files[-(len(suffix)+1):]=='.'+str(suffix):
                    zd={"type":"file","path":folder+"/"+files,'name':files}
                    lists.append(zd)
    return lists

def list_to_tree(data, pk = 'id', pid = 'pid', child = 'lowerlist', root=0,childstatus=True):
    """列表转换tree
    
    data 要转换的列表

    pk 关联节点字段

    pid 父节点字段

    lowerlist 子节点列表

    root 主节点值

    childstatus 当子节点列表为空时是否需要显示子节点字段
    """
    arr = []
    for v in data:
        if v[pid] == root:
            kkkk=list_to_tree(data,pk,pid,child,v[pk],childstatus)
            if childstatus:
                v[child]=kkkk
            else:
                if kkkk:
                    v[child]=kkkk
            arr.append(v)
    return arr

        
class kcwebzip:
    def packzip(src,dst):
        "压缩"
        filelist = []
        if os.path.isfile(src):
            filelist.append(src)
        for root, dirs, files in os.walk(src):
            for name in files:
                filelist.append(os.path.join(root, name))
        zf = zipfile.ZipFile(dst, "w", zipfile.zlib.DEFLATED)
        for tar in filelist:
            arcname = tar[len(src):]
            zf.write(tar,arcname)
        zf.close()
    def unzip_file(dst, src):
        "解压"
        zf = zipfile.ZipFile(dst)
        zf.extractall(src)
        zf.close()
class kcwtar:
    def targz(src,dst):
        """
        打包目录为tar.gz
        :param src: 需要打包的目录
        :param dst: 压缩文件名
        :return: bool
        """
        with tarfile.open(dst, "w:gz") as tar:
            tar.add(src, arcname=os.path.basename(src))
        return True
    def untar(dst, src):
        """
        解压tar.gz文件
        :param dst: 压缩文件名
        :param src: 解压后的存放路径
        :return: bool
        """
        try:
            t = tarfile.open(dst)
            t.extractall(path = src)
            return True
        except Exception as e:
            return False

class response:
    tpldata={} #公共模板变量
    def tpl(path=None,status='200 ok',response_cache=False,ETag=None,header={"Content-Type":"text/html; charset=utf-8"},**context):
        """返回模板内容
        
        path 文件地址

        status 响应状态码

        response_cache 是否启用浏览器缓存  响应状态码200 ok时有效

        ETag 缓存标识  响应状态码200 ok时有效

        header 响应头
        """
        for k in dir(response):
            if k not in ['download','json','pic','redirect','tpl','tpldata','video'] and k[-2:]!='__':
                try:
                    context[k]=response.__dict__[k]
                except KeyError:
                    pass
        context['config']=config
        headers=copy.deepcopy(header)
        getroutecomponent=globals.VAR.component
        if path:
            if path[:1]=="/":
                Temppath=path
            else:
                Temppath="/"+getroutecomponent[1]+"/controller/"+getroutecomponent[2]+"/tpl/"+path+".html"
        else:
            Temppath="/"+getroutecomponent[1]+"/controller/"+getroutecomponent[2]+"/tpl/"+getroutecomponent[3]+"/"+getroutecomponent[4]+".html"
        if status=='200 ok' and response_cache:
            if not ETag:
                ttt=''
                for k in context.keys():
                    ttt+=k+str(context[k])
                ETag=md5(Temppath+ttt+globals.HEADER.URL)
            try:
                HTTP_IF_NONE_MATCH=globals.HEADER.GET['HTTP_IF_NONE_MATCH']
            except:
                HTTP_IF_NONE_MATCH=None
            if HTTP_IF_NONE_MATCH and HTTP_IF_NONE_MATCH==ETag:
                status="304 Not Modified"
                body=''
            else:
                # if isinstance(response_cache,int) and response_cache>1:
                #     headers['response_cache']=str(response_cache)+" s"
                #     set_cache(ETag,1,response_cache)
                # else:
                #     headers['response_cache']="default"
                #     set_cache(ETag,1)
                body=Template(Temppath,**context)
            dateArray = core_datetime.datetime.utcfromtimestamp(times()-86400)
            otherStyleTime = dateArray.strftime('%a, %d %b %Y %H:%M:%S GMT')
            headers['Last-Modified']=otherStyleTime
            headers['ETag']=ETag
            return body,status,headers
        elif status:
            return Template(Temppath,tpldata=response.tpldata,**context),status,headers
        else:
            return Template(Temppath,tpldata=response.tpldata,**context),'200 ok',headers
    def json(res=[],status='200 ok',response_cache=False,ETag=None,header={"Content-Type":"application/json; charset=utf-8","Access-Control-Allow-Origin":"*"}):
        """响应json内容

        res  body内容

        status 响应状态码

        response_cache 是否启用浏览器缓存  响应状态码200 ok时有效

        ETag 缓存标识  响应状态码200 ok时有效

        header 响应头
        """
        headers=copy.deepcopy(header)
        if status=='200 ok' and response_cache:
            if not ETag:
                ETag=md5(globals.HEADER.URL)
            try:
                HTTP_IF_NONE_MATCH=globals.HEADER.GET['HTTP_IF_NONE_MATCH']
            except:
                HTTP_IF_NONE_MATCH=None
            if(HTTP_IF_NONE_MATCH and get_cache(ETag)):
                status="304 Not Modified"
                body=''
            else:
                if isinstance(response_cache,int) and response_cache>1:
                    set_cache(ETag,1,response_cache)
                    headers['response_cache']=str(response_cache)+" s"
                else:
                    set_cache(ETag,1)
                    headers['response_cache']="default"
                body=json_encode(res)
            dateArray = core_datetime.datetime.utcfromtimestamp(times()-86400)
            otherStyleTime = dateArray.strftime('%a, %d %b %Y %H:%M:%S GMT')
            headers['Last-Modified']=otherStyleTime
            headers['ETag']=ETag
            
        else:
            body=json_encode(res)
        return body,status,headers
    def pic(body,response_cache=True,ETag=None):
        """输出图片
        
        body 图片二进制内容或图片路径 建议使用图片路径

        response_cache 是否启用浏览器缓存  body使用图片路径时有效

        ETag 缓存标识
        """
        status='200 ok'
        header={"Cache-Control":"public, max-age=2592000"}
        if isinstance(body,str):
            if response_cache:
                if not ETag:
                    ETag=md5(body+globals.HEADER.URL)
                try:
                    HTTP_IF_NONE_MATCH=globals.HEADER.GET['HTTP_IF_NONE_MATCH']
                except:
                    HTTP_IF_NONE_MATCH=None
                if(HTTP_IF_NONE_MATCH and get_cache(ETag)):
                    status="304 Not Modified"
                    body=''
                else:
                    if isinstance(response_cache,int) and response_cache>1:
                        set_cache(ETag,1,response_cache)
                    else:
                        set_cache(ETag,1)
                    filename=body
                    f=open(filename,"rb")
                    body=f.read()
                    f.close()
                    kind = filetype.guess(filename)
                    try:
                        header['Content-Type']=kind.mime
                    except:
                        header['Content-Type']="image/png"
            else:
                filename=body
                f=open(filename,"rb")
                body=f.read()
                f.close()
                kind = filetype.guess(filename)
                try:
                    header['Content-Type']=kind.mime
                except:
                    header['Content-Type']="image/png"
            dateArray = core_datetime.datetime.utcfromtimestamp(times()-86400)
            otherStyleTime = dateArray.strftime('%a, %d %b %Y %H:%M:%S GMT')
            header['Last-Modified']=otherStyleTime
            header['ETag']=ETag
        else:
            header['Content-Type']="image/png"
        return body,status,header
    def video(body):
        """输出音频
        
        body 音频二进制内容或音频路径
        """
        status='200 ok'
        header={"Cache-Control":"public, max-age=2592000"}
        if isinstance(body,str):
            ETag=md5(body)
            try:
                HTTP_IF_NONE_MATCH=globals.HEADER.GET['HTTP_IF_NONE_MATCH']
            except:
                HTTP_IF_NONE_MATCH=None
            if(HTTP_IF_NONE_MATCH and get_cache(ETag)):
                status="304 Not Modified"
                body=''
            else:
                set_cache(ETag,1,2592000)
                filename=body
                f=open(filename,"rb")
                body=f.read()
                f.close()
                kind = filetype.guess(filename)
                try:
                    header['Content-Type']=kind.mime
                except:
                    header['Content-Type']="video/mp4"
            dateArray = core_datetime.datetime.utcfromtimestamp(times()-86400)
            otherStyleTime = dateArray.strftime('%a, %d %b %Y %H:%M:%S GMT')
            header['Last-Modified']=otherStyleTime
            header['ETag']=ETag
        else:
            header['Content-Type']="video/mp4"
        return body,status,header
    # def video(body):
    #     """输出音频
        
    #     body 音频二进制内容或音频路径
    #     """
    #     if isinstance(body,str):
    #         filename=body
    #         f=open(filename,"rb")
    #         body=f.read()
    #         f.close()
    #         kind = filetype.guess(filename)
    #         try:
    #             ContentType=kind.mime
    #         except:
    #            ContentType="video/mp4" 
    #     else:
    #         ContentType="video/mp4"
    #     return body,'200 ok',{"Content-Type":ContentType,"Cache-Control":"public, max-age=600"}
    def download(pathname):
        """下载文件
        
        pathname 文件路径
        """
        if os.path.isfile(pathname):
            f=open(pathname,"rb")
            body=f.read()
            f.close()
            kind = filetype.guess(pathname)
            try:
                return body,"200 ok",{"Content-Type":"application/"+kind.mime,"Accept-Ranges":"bytes"}
            except:
                return body,"200 ok",{"Content-Type":"application/text","Accept-Ranges":"bytes"}
        else:
            return Templates('E:\doc\python\kcwebplus\kcweb/tpl/err.html',title="文件不存在",content="文件不存在",imgsrc=config.domain['kcwebimg']+"/icon/error.png",config=config)
    def redirect(url,status="302 Found",html='',header={"Content-Type":"application/html; charset=utf-8"}):
        """重定向

        参数 url 重定向地址 必须

        参数 status 响应码  可选

        参数 html body响应内容 可选

        参数 header 响应头  可选
        """
        header['Location']=url
        return html,status,header
class create:
    appname=None
    modular=None
    path=get_folder() #当前框架目录
    def __init__(self,appname="app",modular="api"):
        self.appname=str(appname)
        self.modular=str(modular)
    def uninstallplug(self,plug):
        """卸载插件

        plug 插件名
        """
        f=open(self.appname+"/"+self.modular+"/controller/__init__.py","r",encoding='utf-8')
        text=f.read()
        f.close()
        text=re.sub("\nfrom . import "+plug,"",text)
        text=re.sub("from . import "+plug,"",text)
        f=open(self.appname+"/"+self.modular+"/controller/__init__.py","w",encoding='utf-8')
        f.write(text)
        f.close()
        shutil.rmtree(self.appname+"/"+self.modular+"/controller/"+plug)
        return True,"成功"
    def packplug(self,plug):
        """打包插件
        
        plug 插件名
        """
        """打包模块"""
        if os.path.exists(self.appname+"/"+self.modular+"/controller/"+plug):
            kcwebzip.packzip(self.appname+"/"+self.modular+"/controller/"+plug,self.appname+"/"+self.modular+"/controller/"+plug+".zip")
            return True,"成功"
        else:
            return False,"失败"
    def uploadplug(self,plug,username='',password='',cli=False):
        "上传一个插件"
        if not os.path.isfile(self.appname+"/"+self.modular+"/controller/"+plug+".zip"):
            self.packplug(plug=plug)
        i=0
        http=Http()
        http.set_timeout=300
        while True:
            timestamp=times()
            sign=md5(str(username)+str(timestamp)+md5(md5(password)))
            # http.set_header['username']=username
            # http.set_header['timestamp']=str(timestamp)
            # http.set_header['sign']=sign
            http.openurl(config.domain['kcwebapi']+"/user/userinfo/?username="+username+"&timestamp="+str(timestamp)+"&sign="+sign)
            arr=json_decode(http.get_text)
            if not arr:
                os.remove(self.appname+"/"+self.modular+"/controller/"+plug+".zip")
                if config.app['app_debug']:
                    print(http.get_text)
                return False,"用户身份验证失败，服务器暂时无法处理"
            if (arr['code']==-1 or arr['code']==2) and cli:
                if i >= 3:
                    os.remove(self.appname+"/"+self.modular+"/controller/"+plug+".zip")
                    return False,"用户名或密码错误"
                elif i:
                    print("用户名或密码错误，请重新输入")
                    username = input("请输入用户名（手机号）\n")
                    password = input("请输入密码\n")
                else:
                    username = input("请输入用户名（手机号）\n")
                    password = input("请输入密码\n")
                i+=1
            elif arr['code']==0:
                break
            else:
                os.remove(self.appname+"/"+self.modular+"/controller/"+plug+".zip")
                return False,arr['msg']
        http.openurl(config.domain['kcwebapi']+"/user/uploadplug/?username="+username+"&timestamp="+str(timestamp)+"&sign="+sign,'POST',
        data={'name':str(plug),'describes':'','modular':self.modular},
        files={'file':open(self.appname+"/"+self.modular+"/controller/"+plug+".zip", 'rb')})
        arr=json_decode(http.get_text)
        if not arr:
            os.remove(self.appname+"/"+self.modular+"/controller/"+plug+".zip")
            if config.app['app_debug']:
                print(http.get_text)
            return False,"上传失败，服务器暂时无法处理上传"
        elif arr['code']==-1 or arr['code']==2:
            os.remove(self.appname+"/"+self.modular+"/controller/"+plug+".zip")
            return False,"用户名或密码错误"
        elif arr['code']==0:
            os.remove(self.appname+"/"+self.modular+"/controller/"+plug+".zip")
            return True,arr['msg']
        elif arr['code']==0:
            os.remove(self.appname+"/"+self.modular+"/controller/"+plug+".zip")
            return False,arr['msg']
        else:
            os.remove(self.appname+"/"+self.modular+"/controller/"+plug+".zip")
            return False,arr['msg']
    def installplug(self,plug,edition='',token='',cli=False,mandatory=False):
        """创建一个插件，如果您的模块目录下没有插件包，则创建默认插件文件
        
        plug 插件名
        """
        plug=str(plug)
        if os.path.exists(self.appname+"/"+self.modular+"/controller/"+plug) and not mandatory:
            return False,"该插件已存在"
        else:
            http=Http()
            i=0
            j=0
            tplug=plug
            modular=self.modular
            while True:
                http.openurl(config.domain['kcwebapi']+"/pub/plug","GET",params={"modular":modular,"name":str(tplug),"edition":str(edition),"token":token})
                arr=json_decode(http.get_text)
                if arr:
                    if arr['code']==-1 and cli:
                        if i >= 3:
                            return False,plug+"插件授权码错误"
                        elif i:
                            token = input("授权码错误，请重新输入授权码，从而获得该插件\n")
                        else:
                            token = input("请输入授权码，从而获得该插件\n")
                        i+=1
                    elif arr['code']==-1:
                        return False,plug+"插件授权码错误"
                    elif not arr['data']:
                        modular="api"
                        tplug="index" #默认插件
                    elif arr['code']==0 and arr['data']:
                        i=0
                        j+=1
                        arr=arr['data']
                        r=requests.get(arr['dowurl'],verify=False)
                        f = open(self.appname+"/"+self.modular+"/controller/"+plug+".zip", "wb")
                        for chunk in r.iter_content(chunk_size=512):
                            if chunk:
                                f.write(chunk)
                        f.close()
                        if zipfile.is_zipfile(self.appname+"/"+self.modular+"/controller/"+plug+".zip") and os.path.isfile(self.appname+"/"+self.modular+"/controller/"+plug+".zip"):
                            break
                        if j >= 10:
                            return False,str(plug)+"插件下载失败"
                        time.sleep(0.1)
                    else:
                        return False,str(plug)+"插件搜索失败"
                else:
                    return False,self.modular+"模块下找不到"+str(plug)+"插件"
            if os.path.isfile(self.appname+"/"+self.modular+"/controller/"+plug+".zip"):#安装打包好的插件
                kcwebzip.unzip_file(self.appname+"/"+self.modular+"/controller/"+plug+".zip",self.appname+"/"+self.modular+"/controller/"+plug+"/")
                os.remove(self.appname+"/"+self.modular+"/controller/"+plug+".zip")
                if os.path.isfile(self.appname+"/"+self.modular+"/controller/"+plug+"/install.txt"): #安装依赖包
                    install_requires=[]
                    try:
                        f=open(self.appname+"/"+self.modular+"/controller/"+plug+"/install.txt")
                        while True:
                            line = f.readline()
                            if not line:
                                break
                            elif len(line) > 2:
                                install_requires.append(line)
                        f.close()
                    except:
                        shutil.rmtree(self.appname+"."+self.modular+"/controller/"+plug)
                        return False,"error"
                    if len(install_requires):
                        try:
                            install_requires.insert(0,"install")
                            if 0 != pip.main(install_requires):
                                shutil.rmtree(self.appname+"/"+self.modular+"/controller/"+plug)
                                return False,"error"
                        except AttributeError as e:
                            shutil.rmtree(self.appname+"/"+self.modular+"/controller/"+plug)
                            if config.app['app_debug']:
                                print("建议更新您的pip版本。参考命令：Python -m pip install --user --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/")
                            return False,str(e)
                if os.path.isfile(self.appname+"."+self.modular+"/controller/"+plug+"/install.py"):
                    try:
                        m=importlib.import_module(self.appname+"."+self.modular+"/controller/"+plug+".install")
                    except:
                        shutil.rmtree(self.appname+"."+self.modular+"/controller/"+plug)
                        print(traceback.format_exc())
                        return False,"插件依赖包文件不存在或依赖包文件格式错误"
                    else:
                        try:
                            a=m.install()
                        except:
                            shutil.rmtree(self.appname+"."+self.modular+"/controller/"+plug)
                            return False,"插件依赖包install函数被破坏"
                        # if not a[0]:
                        #     shutil.rmtree(self.appname+"."+self.modular+"/controller/"+plug)
                        #     return False,str(a[1])

                f=open(self.appname+"/"+self.modular+"/controller/__init__.py","r",encoding='utf-8')
                text=f.read()
                f.close()
                text=re.sub("\nfrom . import "+plug,"",text)
                text=re.sub("from . import "+plug,"",text)
                f=open(self.appname+"/"+self.modular+"/controller/__init__.py","w",encoding='utf-8')
                text+="\nfrom . import "+plug
                f.write(text)
                f.close()

                f=open(self.appname+"/"+self.modular+"/controller/"+plug+"/common/autoload.py","r",encoding='utf-8')
                text=f.read()
                f.close()
                text=re.sub("app.api",self.appname+"."+self.modular,text)
                f=open(self.appname+"/"+self.modular+"/controller/"+plug+"/common/autoload.py","w",encoding='utf-8')
                f.write(text)
                f.close()

                
                return True,"插件安装成功，"+plug+"=="+str(arr['edition'])
            else:
                return False,str(plug)+"插件获取失败"
    def uninstallmodular(self):
        "卸载模块"
        f=open(self.appname+"/__init__.py","r")
        text=f.read()
        f.close()
        text=re.sub("\nfrom . import "+self.modular,"",text)
        text=re.sub("from . import "+self.modular,"",text)
        f=open(self.appname+"/__init__.py","w")
        f.write(text)
        f.close()
        shutil.rmtree(self.appname+"/"+self.modular)
        return True,"成功"
    def packmodular(self):
        """打包模块"""
        if os.path.exists(self.appname+"/"+self.modular):
            kcwebzip.packzip(self.appname+"/"+self.modular,self.appname+"/"+self.modular+".zip")
            return True,"成功"
        else:
            return False,"失败"
    def uploadmodular(self,username='',password='',cli=False):
        "上传模块"
        if not os.path.isfile(self.appname+"/"+self.modular+".zip"):
            self.packmodular()
        i=0
        http=Http()
        http.set_timeout=300
        while True:
            timestamp=times()
            sign=md5(str(username)+str(timestamp)+md5(md5(password)))
            # http.set_header['username']=username
            # http.set_header['timestamp']=str(timestamp)
            # http.set_header['sign']=sign
            http.openurl(config.domain['kcwebapi']+"/user/uploadmodular/?username="+username+"&timestamp="+str(timestamp)+"&sign="+sign,'POST',
            data={'name':str(self.modular),'describes':''},
            files={'file':open(self.appname+"/"+self.modular+".zip", 'rb')})
            arr=json_decode(http.get_text)
            if not arr:
                os.remove(self.appname+"/"+self.modular+".zip")
                if config.app['app_debug']:
                    print(http.get_text)
                return False,"用户身份验证失败，服务器暂时无法处理"
            if (arr['code']==-1 or arr['code']==2) and cli:
                if i >= 3:
                    os.remove(self.appname+"/"+self.modular+".zip")
                    return False,"用户名或密码错误"
                elif i:
                    print("用户名或密码错误，请重新输入")
                    username = input("请输入用户名（手机号）\n")
                    password = input("请输入密码\n")
                else:
                    username = input("请输入用户名（手机号）\n")
                    password = input("请输入密码\n")
                i+=1
            elif arr['code']==0:
                break
            elif arr['code']==-1:
                os.remove(self.appname+"/"+self.modular+".zip")
                return False,"用户名或密码错误"
            else:
                os.remove(self.appname+"/"+self.modular+".zip")
                return False,arr['msg']
        
        http.openurl(config.domain['kcwebapi']+"/user/uploadmodular/?username="+username+"&timestamp="+str(timestamp)+"&sign="+sign,'POST',
        data={'name':str(self.modular),'describes':''},
        files={'file':open(self.appname+"/"+self.modular+".zip", 'rb')})
        arr=json_decode(http.get_text)
        if not arr:
            os.remove(self.appname+"/"+self.modular+".zip")
            if config.app['app_debug']:
                print(http.get_text)
            return False,"上传失败，服务器暂时无法处理上传"
        elif arr['code']==-1 or arr['code']==2:
            os.remove(self.appname+"/"+self.modular+".zip")
            return False,"用户名或密码错误"
        elif arr['code']==0:
            os.remove(self.appname+"/"+self.modular+".zip")
            return True,arr['msg']
        else:
            os.remove(self.appname+"/"+self.modular+".zip")
            return False,arr['msg']
    def installmodular(self,token='',cli=False):
        "创建模块，如果应用不存，则创建默认应用，如果在您的应用目录下没有模块包，则创建默认模块文件"
        if not os.path.exists(self.appname):
            # os.makedirs(self.appname)
            r=requests.get(config.domain['kcwebfile']+"/kcweb/app.zip")
            f = open("./app.zip", "wb")
            for chunk in r.iter_content(chunk_size=512):
                if chunk:
                    f.write(chunk)
            f.close()
            kcwebzip.unzip_file("./app.zip","./"+self.appname)
            os.remove("./app.zip")
            if not os.path.isfile("./server.py"):
                if "Windows" in platform.platform():
                    pythonname="python"
                else:
                    pythonname="python3"
                servertext=('# -*- coding: utf-8 -*-\n #gunicorn -b 0.0.0.0:39010 '+self.appname+':app\n'+
                        'from kcweb import web\n'+
                        'import '+self.appname+' as application\n'+
                        'app=web(__name__,application)\n'+
                        'if __name__ == "__main__":\n'+
                        '    #host监听ip port端口 name python解释器名字 (windows一般是python  linux一般是python3)\n'+
                        '    app.run(host="0.0.0.0",port="39001",name="'+pythonname+'")')
                f=open("./server.py","w+",encoding='utf-8')
                f.write(servertext)
                f.close()
            f=open(self.appname+"/common/autoload.py","w",encoding='utf-8')
            f.write("from kcweb.common import *\n"+
                    "from "+self.appname+" import config\n"+
                    "G=globals.G")
            f.close()

            content=''
            f=open(self.appname+"/"+self.modular+"/common/autoload.py","r",encoding='utf-8')
            while True:
                line = f.readline()
                if not line:
                    break
                elif 'from' not in line and 'import' not in line:
                    content+=line
            f.close()
            f=open(self.appname+"/"+self.modular+"/common/autoload.py","w",encoding='utf-8')
            f.write("from "+self.appname+".common import *\n"+content)
            f.close()

            content=''
            f=open(self.appname+"/"+self.modular+"/controller/index/common/autoload.py","r",encoding='utf-8')
            while True:
                line = f.readline()
                if not line:
                    break
                elif 'from' not in line and 'import' not in line:
                    content+=line
            f.close()
            f=open(self.appname+"/"+self.modular+"/controller/index/common/autoload.py","w",encoding='utf-8')
            f.write("from "+self.appname+"."+self.modular+".common import *\n"+content)
            f.close()
            return True,"应用创建成功"
        else:
            if not os.path.isfile(self.appname+"/__init__.py") or not os.path.exists(self.appname+"/common"):
                return False,self.appname+"不是kcweb应用"
        if os.path.exists(self.appname+"/"+self.modular):
            return False,self.appname+"/"+self.modular+"已存在"
        else:
            http=Http()
            i=0
            modular=self.modular
            while True:
                http.openurl(config.domain['kcwebapi']+"/pub/modular","POST",params={"name":modular,"token":token})
                arr=json_decode(http.get_text)
                if arr:
                    if arr['code']==-1 and cli:
                        if i >= 3:
                            return False,self.modular+"模块授权码错误"
                        elif i:
                            token = input("授权码错误，请重新输入授权码，从而获得该模块\n")
                        else:
                            token = input("请输入授权码，从而获得该模块\n")
                        i+=1
                    elif arr['code']==-1:
                        return False,self.modular+"模块授权码错误"
                    elif not arr['data']:
                        modular="api"
                    elif arr['code']==0 and arr['data']:
                        arr=arr['data']
                        #循环下载模块
                        i=0
                        while i < 5:
                            r=requests.get(arr['dowurl'])
                            f = open(self.appname+"/"+self.modular+".zip", "wb")
                            for chunk in r.iter_content(chunk_size=1024*100):
                                if chunk:
                                    f.write(chunk)
                            f.close()
                            time.sleep(0.3)
                            if os.path.isfile(self.appname+"/"+self.modular+".zip"):
                                break
                            i+=1
                        if os.path.isfile(self.appname+"/"+self.modular+".zip"):#安装打包好的模块
                            kcwebzip.unzip_file(self.appname+"/"+self.modular+".zip",self.appname+"/"+self.modular+"/")
                            os.remove(self.appname+"/"+self.modular+".zip")

                            if os.path.isfile(self.appname+"/"+self.modular+"/install.txt"): #安装依赖包
                                install_requires=[]
                                try:
                                    f=open(self.appname+"/"+self.modular+"/install.txt")
                                    while True:
                                        line = f.readline()
                                        if not line:
                                            break
                                        elif len(line) > 3:
                                            install_requires.append(line)
                                    f.close()
                                except:
                                    shutil.rmtree(self.appname+"/"+self.modular)
                                    return False,"error"
                                if len(install_requires):
                                    try:
                                        install_requires.insert(0,"install")
                                        if 0 != pip.main(install_requires):
                                            shutil.rmtree(self.appname+"/"+self.modular)
                                            return False,"error"
                                    except AttributeError as e:
                                        shutil.rmtree(self.appname+"/"+self.modular)
                                        if config.app['app_debug']:
                                            print("建议更新您的pip版本。参考命令：Python -m pip install --user --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/")
                                        return False,str(e)
                            if os.path.isfile(self.appname+"/"+self.modular+"/install.py"):#如果存在依赖文件
                                try:
                                    m=importlib.import_module(self.appname+'.'+self.modular+'.install')
                                except:
                                    shutil.rmtree(self.appname+"/"+self.modular)
                                    print(traceback.format_exc())
                                    return False,"模块依赖包文件不存在或依赖包文件格式错误"
                                else:
                                    try:
                                        a=m.install()
                                    except:
                                        shutil.rmtree(self.appname+"/"+self.modular)
                                        return False,"模块依赖包install方法被破坏"
                                    # if not a[0]:
                                    #     shutil.rmtree(self.appname+"/"+self.modular)
                                    #     return False,str(a[1])
                            content="\nfrom . import "+self.modular
                            f=open(self.appname+"/__init__.py","a",encoding='utf-8')
                            f.write(content)
                            f.close()

                            content=''
                            f=open(self.appname+"/"+self.modular+"/common/autoload.py","r",encoding='utf-8')
                            while True:
                                line = f.readline()
                                if not line:
                                    break
                                elif 'from' not in line and 'import' not in line:
                                    content+=line
                            f.close()
                            f=open(self.appname+"/"+self.modular+"/common/autoload.py","w",encoding='utf-8')
                            f.write("from "+self.appname+".common import *\n"+content)
                            f.close()

                            content=''
                            f=open(self.appname+"/"+self.modular+"/controller/index/common/autoload.py","r",encoding='utf-8')
                            while True:
                                line = f.readline()
                                if not line:
                                    break
                                elif 'from' not in line and 'import' not in line:
                                    content+=line
                            f.close()
                            f=open(self.appname+"/"+self.modular+"/controller/index/common/autoload.py","w",encoding='utf-8')
                            f.write("from "+self.appname+"."+self.modular+".common import *\n"+content)
                            f.close()
                        else:
                            return False,self.modular+"模块下载失败"
                        if not os.path.isfile("./server.py"):
                            if "Windows" in platform.platform():
                                pythonname="python"
                            else:
                                pythonname="python3"
                            # sys.argv[0]=re.sub('.py','',sys.argv[0])
                            servertext=('# -*- coding: utf-8 -*-\n#gunicorn -b 0.0.0.0:39010 '+self.appname+':app\n'+
                                    'from kcweb import web\n'+
                                    'import '+self.appname+' as application\n'+
                                    'app=web(__name__,application)\n'+
                                    'if __name__ == "__main__":\n'+
                                    '    #host监听ip port端口 name python解释器名字 (windows一般是python  linux一般是python3)\n'+
                                    '    app.run(host="0.0.0.0",port="39001",name="'+pythonname+'")')
                            f=open("./server.py","w+",encoding='utf-8')
                            f.write(servertext)
                            f.close()
                        return True,"安装成功"
                    else:

                        return False,"模块下载失败"
                else:
                    return False,"找不到"+self.modular+"模块"
    # def __zxmodular(self,sourcep): 
    #     "处理模块文件"
    #     path1=self.path+"/application/api"+sourcep
    #     path2=self.appname+"/"+self.modular+sourcep
    #     lists=os.listdir(path1)
    #     for files in lists:
    #         if os.path.isfile(path1+"/"+files):
    #             if ".py" in files:
    #                 content=Templates(path1+"/"+files,appname=self.appname,modular=self.modular)
    #                 f=open(path2+"/"+files,"w+",encoding='utf-8')
    #                 f.write(content)
    #                 f.close()
    #             else:
    #                 f=open(path1+"/"+files,"r",encoding='utf-8')
    #                 content=f.read()
    #                 f.close()
    #                 f=open(path2+"/"+files,"w+",encoding='utf-8')
    #                 f.write(content)
    #                 f.close()
    #         elif files != '__pycache__':
    #             if not os.path.exists(path2+"/"+files):
    #                 os.makedirs(path2+"/"+files)
    #             self.__zxmodular(sourcep+"/"+files)