# -*- coding: utf-8 -*-
from kcweb.config import session as kcwsession
from kcweb.common import globals as kcwglobals
import time,random,hashlib
from kcweb.utill.cache import cache as kcwcache
from datetime import datetime
def __md5(strs):
    m = hashlib.md5()
    m.update(strs.encode())
    return m.hexdigest()
def set(name,value,expire=None):
    "设置session"
    if not expire:
        expire=kcwsession['expire']
    HTTP_COOKIE=kcwglobals.HEADER.HTTP_COOKIE
    SESSIONID="SESSIONID"+__md5(str(name)+str(kcwsession['prefix']))[0:8]  #######
    try: 
        HTTP_COOKIE=HTTP_COOKIE.split(";")
    except:
        token=None
    else:
        token=None
        for k in HTTP_COOKIE:
            if SESSIONID in k:
                token=k.split("=")[1]
    if not token:
        strs="kcw"+str(time.time())+str(random.randint(0,9))
        token=__md5(strs)
    kcwglobals.set_cookie=SESSIONID+"="+token+";expires="+datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')+"; Max-Age=%d;Path=/" % (int(expire)*10)
    return kcwcache.cache().set_config(kcwsession).set_cache(token,value,expire)
def get(name):
    "获取session"
    HTTP_COOKIE=kcwglobals.HEADER.HTTP_COOKIE
    try:
        HTTP_COOKIE=HTTP_COOKIE.split(";")
    except:
        return None
    SESSIONID="SESSIONID"+__md5(str(name)+str(kcwsession['prefix']))[0:8]  #########
    token=''
    for k in HTTP_COOKIE:
        if SESSIONID in k:
            token=k.split("=")[1]
    v=kcwcache.cache().set_config(kcwsession).get_cache(token)
    return v
def rm(name):
    "删除session"
    HTTP_COOKIE=kcwglobals.HEADER.HTTP_COOKIE
    try:
        HTTP_COOKIE=HTTP_COOKIE.split(";")
    except:
        return None
    SESSIONID="SESSIONID"+__md5(str(name)+str(kcwsession['prefix']))[0:8]  #######
    token=''
    for k in HTTP_COOKIE:
        if SESSIONID in k:
            token=k.split("=")[1]
    kcwcache.cache().set_config(kcwsession).del_cache(token)
    kcwglobals.set_cookie=SESSIONID+"="+token+";expires="+datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')+"; Max-Age=2"
    return True

