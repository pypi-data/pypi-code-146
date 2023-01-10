# -*- coding: utf-8 -*-
# 应用配置
import sys
app={}
app['app_debug']=True  #是否开启调试模式
app['tpl_folder']='./tpl'  #设置模板文件目录名 注意：不能配置目录路径
app['before_request']=''  #设置请求前执行的函数
app['after_request']=''    #设置请求后执行的函数  
app['staticpath']='static'
app['http_server']='wsgiref' #使用的开发服务器 支持 wsgiref、kcweb、kcweb_server
try:
    if sys.argv[2]=='--cli':
        app['cli']=True
    else:
        app['cli']=False
except:
    app['cli']=False
# redis配置
redis={}
redis['host']='127.0.0.1' #服务器地址
redis['port']=6379 #端口
redis['password']=''  #密码
redis['db']=0 #Redis数据库    注：Redis用0或1或2等表示
redis['pattern']=True # True连接池链接 False非连接池链接
redis['ex']=0  #过期时间 （秒）

#缓存配置
cache={}
cache['type']='File' #驱动方式 支持 File Redis Python
cache['path']='runtime/cachepath' #缓存保存目录 
cache['expire']=120 #缓存有效期 0表示永久缓存
cache['host']=redis['host'] #Redis服务器地址
cache['port']=redis['port'] #Redis 端口
cache['password']=redis['password'] #Redis登录密码
cache['db']=1 #Redis数据库    注：Redis用1或2或3等表示
cachevalue={}

# session配置
session={}
session['type']='File' #session 存储类型  支持 file、Redis、Python
session['path']='runtime/session' #session缓存目录
session['expire']=86400 #session默认有效期 该时间是指session在服务的保留时间，通常情况下浏览器上会保留该值的10倍
session['prefix']="KCW" # SESSION 前缀
session['host']=redis['host'] #Redis服务器地址
session['port']=redis['port'] #Redis 端口
session['password']=redis['password'] #Redis登录密码
session['db']=2 #Redis数据库    注：Redis用1或2或3等表示


# 默认数据库配置
database={}
database['type']='mysql' # 数据库类型  目前支持mysql和sqlite
database['debug']=False  #是否开启数据库调试描述
database['host']=['127.0.0.1']#服务器地址 [地址1,地址2,地址3...] 多个地址分布式(主从服务器)下有效
database['port']=[3306] #端口 [端口1,端口2,端口3...]
database['user']=['root']  #用户名 [用户名1,用户名2,用户名3...]
database['password']=['root']  #密码 [密码1,密码2,密码3...]
database['db']=['test']  #数据库名 [数据库名1,数据库名2,数据库名3...]
database['charset']='utf8mb4'   #数据库编码默认采用utf8mb4
database['pattern']=False # True数据库长连接模式 False数据库短连接模式  注：建议web应用有效，cli应用方式下，如果长时间运行建议使用mysql().close()关闭
database['cli']=app['cli'] # 是否以cli方式运行
database['dbObjcount']=1 # 连接池数量（单个数据库地址链接数量），数据库链接实例数量 mysql长链接模式下有效
database['deploy']=0 # 数据库部署方式:0 集中式(单一服务器),1 分布式(主从服务器)  mysql数据库有效
database['master_num']=1 #主服务器数量 不能超过host服务器数量  （等于服务器数量表示读写不分离：主主复制。  小于服务器表示读写分离：主从复制。） mysql数据库有效
database['master_dql']=False #主服务器是否可以执行dql语句 是否可以执行select语句  主服务器数量大于等于host服务器数量时必须设置True
database['break']=0 #断线重连次数，0表示不重连。 注：cli模式下 10秒进行一次重连并且连接次数是当前配置的300倍

#sqlite配置
sqlite={}
sqlite['db']='kcwdb'  # 数据库文件存放地址

#mongodb配置
mongo={}
mongo['host']='127.0.0.1'
mongo['port']='27017'
mongo['user']=''
mongo['password']=''
mongo['db']='test'
mongo['retryWrites']=False #是否支持重新写入



#路由配置
route={}
route['default']=True #是否开启默认路由  默认路由开启后面不影响以下配置的路由，模块名/版本名/控制器文件名/方法名 作为路由地址   如：http://www.kcw.com/modular/plug/index/index/
route['modular']='' #指定访问配置固定模块 （如果配置了该值，将无法通过改变url访问不同模块）
route['plug']='' #指定访问固定插件 （如果配置了该值，将无法通过改变url访问不同插件）
route['defmodular']='index' #默认模块 当url不包括模块名时
route['defplug']='index' #默认插件 当url不包括插件名时
route['files']='index' #默认路由文件（控制器） 当url不包括控制器名时
route['funct']='index'  #默认路由函数 (操作方法) 当url不包括操作方法名时
route['methods']=['POST','GET'] #默认请求方式
route['children']=[]
#email配置
email={}
email['sender']='' #发件人邮箱账号
email['pwd']='' #发件人邮箱密码(如申请的smtp给的口令)
email['sendNick']='' #发件人昵称
email['theme']='' #默认主题
email['recNick']='' #默认收件人昵称

kcweb={}
kcweb['name']='kcweb'                             #项目的名称
kcweb['version']='4.13.23'							#项目版本
kcweb['description']=''       #项目的简单描述
kcweb['long_description']=''     #项目详细描述
kcweb['license']='MIT'                    #开源协议   mit开源
kcweb['url']=''
kcweb['author']='禄可集团-坤坤'  					 #名字
kcweb['author_email']='fk1402936534@qq.com' 	     #邮件地址
kcweb['maintainer']='坤坤' 						 #维护人员的名字
kcweb['maintainer_email']='fk1402936534@qq.com'    #维护人员的邮件地址
kcweb['username']=''
kcweb['password']=''

domain={}
domain['kcwebfile']="https://file.kwebapp.cn"
domain['kcwebstatic']="https://static.kwebapp.cn"
domain['kcwebimg']="https://img.kwebapp.cn"
# domain['kcwebapi']="//kcweb.kwebapp.cn"
domain['kcwebapi']="https://kcweb.kwebapp.cn"

#其他配置
other={}

