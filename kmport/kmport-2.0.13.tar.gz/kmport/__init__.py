#Kage Park
import os
import gc
import re
import sys
import ast
import json
import time
import shutil
import codecs
import socket
import struct
import pprint
import inspect
import getpass
import traceback
from threading import Thread
from importlib import import_module
#import pip
from datetime import datetime
from subprocess import check_call
from subprocess import PIPE as subprocess_PIPE
from subprocess import Popen as subprocess_Popen
from subprocess import TimeoutExpired as subprocess_TimeoutExpired
printf_log_base=None
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

__version__='2.0.15'

'''
Base Module
if you want requests then you need must pre-loaded below module when you use compiled binary file using pyinstaller

example)
from http.cookies import Morsel
Import('import requests')

Without build then import requests is ok. but if you build it then it need pre-loaded Morsel module for Import('import requests') command
'''
def Global():
    '''
    Method's global variables
    '''
    return dict(inspect.getmembers(inspect.stack()[-1][0]))["f_globals"]

def StdOut(msg):
    '''
    Standard Output Print without new line symbol
    '''
    try:
        if type(msg).__name__ == 'bytes':
            sys.stdout.buffer.write(msg)
        else:
            sys.stdout.write(msg)
        sys.stdout.flush()
    except:
        sys.stderr.write('Wrong output data format\n')
        sys.stderr.flush()

def StdErr(msg):
    '''
    Standard Error Print without new line symbol
    '''
    sys.stderr.write(msg)
    sys.stderr.flush()

def PyVer(main=None,miner=None,msym=None):
    '''
    python version check
    '''
    if isinstance(main,int):
        if main == sys.version_info[0]:
            if isinstance(miner,int):
                if msym:
                    if msym == '>=':
                        if sys.version_info[1] >= miner: return True
                    elif msym == '>':
                        if sys.version_info[1] > miner: return True
                    elif msym == '<=':
                        if sys.version_info[1] <= miner: return True
                    elif msym == '<':
                        if sys.version_info[1] < miner: return True
                if miner == sys.version_info[1]:return True
                return False
            return True
        return False
    else:
        return '{}.{}'.format(sys.version_info[0],sys.version_info[1])

def find_executable(executable,path=None):
    if not Type(executable,'str',data=True): return None
    if not Type(path,'str',data=True):
        path=os.environ['PATH']
    path_a=path.split(os.pathsep)
    if os.name == 'os2':
        (base,ext)=os.path.splitex(executable)
        if not ext:
            executable=executable+'.exe'
    elif sys.platform == 'win32':
        (base,ext)=os.path.splitex(executable)
        if not ext:
            executable=executable+'.exe'
    for p in path_a:
        f=os.path.join(p,executable)
        if os.path.isfile(f):
            return f
    return None

def ByteName(src):
    '''
    Get Byte type name
    '''
    if PyVer(3) and isinstance(src,bytes):
        if src.startswith(b'\xff\xfe\x00\x00') and src.endswith(b'\x00\x00\x00'):
            return True,'utf-32-le'
        elif src.startswith(b'\x00\x00\x00') and src.endswith(b'\xff\xfe\x00\x00'):
            return True,'utf-32-be'
        elif src.startswith(b'\xff\xfe') and src.endswith(b'\x00'):
            return True,'utf-16-le'
        elif src.startswith(b'\x00') and src.endswith(b'\xff\xfe'):
            return True,'utf-16-be'
        else:
            return True,'bytes'
    return False,None

def Bytes(src,**opts):
    '''
    Convert data to bytes data
    '''
    encode=opts.get('encode','utf-8')
    default=opts.get('default',{'org'})
    def _bytes_(src,encode,default):
        if type(src).__name__ == 'unicode': src=str(src)
        if isinstance(src,bytes): return src
        if isinstance(src,str):
            try:
                return bytes(src,encode)
            except:
                pass
        if default in ['org',{'org'}]: return src
        return default

    if isinstance(src,list):
        return [ _bytes_(x,encode,default) for x in src ]
    elif isinstance(src,tuple):
        return tuple([ _bytes_(x,encode,default) for x in src ])
    elif isinstance(src,dict):
        for ii in src:
            if isinstance(src[ii],(list,tuple,dict)):
                src[ii]=Bytes(src[ii],encode=encode,default=default)
            else:
                src[ii]=_bytes_(src[ii],encode,default)
        return src
    else:
        return _bytes_(src,encode,default)
def Int2Bytes(src,default='org'):
    try:
        #struct.pack('>I', src)[1:]
        #struct.pack('>L', src)[1:]
        return struct.pack('>BH', src >> 16, src & 0xFFFF)
    except:
        if default in ['org',{'org'}]: return src
        return default

def Bytes2Int(src,encode='utf-8',default='org'):
    if PyVer(3):
        bsrc=Bytes(src,encode=encode)
        if isinstance(bsrc,bytes):
            return int(bsrc.hex(),16)
        if default in ['org',{'org'}]: return src
        return default
    try:
        return int(src.encode('hex'),16)
    except:
        if default in ['org',{'org'}]: return src
        return default

def Str(src,**opts):
    '''
    Convert data to String data
    '''
    encode=opts.get('encode',None)
    default=opts.get('default','org')
    mode=opts.get('mode','auto')
    if not isinstance(encode,(str,list,tuple)): encode=['utf-8','latin1','windows-1252']
    def _byte2str_(src,encode):
        byte,bname=ByteName(src)
        if byte:
            if bname == 'bytes':
                if isinstance(encode,(list,tuple)):
                    for i in encode:
                        try:
                            return src.decode(i)
                        except:
                            pass
                else:
                    return src.decode(encode)
            else:
                return src.decode(bname)
        elif type(src).__name__=='unicode':
            if isinstance(encode,(list,tuple)):
                for i in encode:
                    try:
                        return src.encode(i)
                    except:
                        pass
            else:
                return src.encode(encode)
        return src
    tuple_data=False
    if isinstance(src,tuple):
        src=list(src)
        tuple_data=True
    if isinstance(src,list):
        for i in range(0,len(src)):
            if isinstance(src[i],list):
                src[i]=Str(src[i],encode=encode)
            elif isinstance(src[i],dict):
                for z in src[i]:
                    if isinstance(src[i][z],(dict,list)):
                        src[i][z]=Str(src[i][z],encode=encode)
                    else:
                        src[i][z]=_byte2str_(src[i][z],encode)
            else:
                src[i]=_byte2str_(src[i],encode)
    elif isinstance(src,dict):
        for i in src:
            if isinstance(src[i],(dict,list)):
                src[i]=Str(src[i],encode=encode)
            else:
                src[i]=_byte2str_(src[i],encode)
    else:
        src=_byte2str_(src,encode)

    # Force make all to string
    if mode in ['force','fix','fixed']:
        return '''{}'''.format(src)
    if tuple_data: return tuple(src)
    return src

def Default(a,b=None):
    if b in ['org',{'org'}]:
        return a
    return b

def Peel(i,mode=True,default='org',err=True,output_check=True):
    '''
    Peel list,tuple,dict to data, if not peelable then return original data
      - single data : just get data
      - multi data  : get first data
    if peeled data is None then return default
    default : 'org'(default) : return original data
    err     : True :(default) if not single data then return default, False: whatever it will return first data
    mode    : True :(default), peeling data, False: not peeling(return original)
    output_check: True:(default) If peeled data is list,tuple,dict then return default, False: just return peeled data
    '''
    if mode is False: return i
    elif mode == 'force':
        err=False
        output_check=False
    if isinstance(i,(list,tuple,dict)):
        #Error condition
        if len(i) == 0: return Default(i,default)
        if len(i) > 1:
            if err is True: return Default(i,default)
        rt=i[0] if isinstance(i,(list,tuple)) else i[Next(i)]
        if output_check is True:
            #Check output data format
            if isinstance(rt,(list,tuple,dict)):
                return Default(i,default)
        return rt
    else:
        #Not peelable
        return i

def Int(i,default='org',sym=None,err=False):
    '''
    Convert data to Int data when possible. if not then return default (original data)
    support data type: int,float,digit number,list,tuple
    default: (default org)
        org : fail then return or keeping the input data
        True,False,None: fail then return default value in single data or ignore the item in list
    sym     : split symbol when input is string
    err     : 
        False: replace data for possible positions
        True : if convert error in list/tuple then return default
    '''
    if isinstance(i,int): return i
    i_type=TypeName(i)
    if i_type in ('str','bytes'):
        if sym:
            sym=Bytes(sym) if i_type == 'bytes' else Str(sym)
            i=i.split(sym)
        else:
            try:
                return int(i)
            except:
                return Default(i,default)
    elif i_type in ('list','tuple'):
        tuple_out=True if i_type == 'tuple' else False
        rt=[]
        for a in i:
           try:
               rt.append(int(a))
           except:
               if err: return Default(i,default)
               rt.append(a)
        if tuple_out: return tuple(rt)
        return rt
    return Default(i,default)

def Join(*inps,symbol='_-_',byte=None,ignore_type=(dict,bool,None),ignore_data=(),append_front='',append_end=''):
    '''
    Similar as 'symbol'.join([list]) function
    '''
    def _ignore_(src,ignore_type,ignore_data):
        rt=[]
        for i in src:
            if type(i) in ignore_type: continue
            elif ignore_data and i in ignore_data: continue
            rt.append(i)
        return rt
    if ignore_type:
        if None in ignore_type:
            ignore_type=list(ignore_type)
            ignore_type[ignore_type.index(None)]=type(None)
    src=[]
    if len(inps) == 1 and isinstance(inps[0],(list,tuple)):
        src=src+_ignore_(inps[0],ignore_type,ignore_data)
    elif len(inps) == 2 and isinstance(inps[0],(list,tuple)) and symbol=='_-_':
        src=src+_ignore_(inps[0],ignore_type,ignore_data)
        symbol=inps[1]
    else:
        for ii in inps:
            if isinstance(ii,(list,tuple)):
                src=src+_ignore_(ii,ignore_type,ignore_data)
            elif type(ii) in ignore_type:
                continue
            elif ii in ignore_data:
                continue
            else:
                src.append(ii)
    if symbol=='_-_': symbol=''
    rt=''
    if isinstance(byte,bool):
        if byte:
            rt=b''
            symbol=Bytes(symbol)
            append_front=Bytes(append_front)
            append_end=Bytes(append_end)
        else:
            symbol=Str(symbol)
            append_front=Str(append_front)
            append_end=Str(append_end)
    else:
        byte=False
        if src and isinstance(src,(list,tuple)):
            if IsBytes(src[0]):
                rt=b''
                byte=True
                symbol=Bytes(symbol)
                append_front=Bytes(append_front)
                append_end=Bytes(append_end)
    init_none=None
    for i in src:
        if not isinstance(i,(str,bytes)):
            i='{}'.format(i)
        if byte:
            i=Bytes(i)
        else:
            i=Str(i)
        if init_none is None:
            rt=i
            init_none=1
        else:
            rt=rt+symbol+append_front+i+append_end
    return rt

def FixIndex(src,idx,default=False,err=False):
    '''
    Find Index number in the list,tuple,str,dict
    default   : if wrong or error then return default
    err : default False
        False: fixing index to correcting index without error
        True: if wrong index then return default value
    '''
    if isinstance(src,(list,tuple,str,dict)) and isinstance(idx,int):
        if idx < 0:
            if len(src) > abs(idx):
                idx=len(src)-abs(idx)
            else:
                if err: return default
                idx=0
        else:
            if len(src) <= idx:
                if err: return default
                idx=len(src)-1
        return idx
    return default


def Next(src,step=0,out=None,default='org'):
    '''
    Get Next data or first key of the dict 
    '''
    if isinstance(src,(list,tuple,dict)):
        step=FixIndex(src,step,default=0)
        iterator=iter(src)
        for i in range(-1,step):
            rt=next(iterator)
        return rt
    elif isinstance(src,str):
        step=FixIndex(src,step,default=0)
        if len(src) == 0:
            return ''
        elif len(src) >= 0 or len(src) <= step:
            return src[step]
    return Default(src,default)

def Copy(src):
    '''
    Copy data 
    '''
    if isinstance(src,(list,tuple)): return src[:]
    if isinstance(src,dict): return src.copy()
    if isinstance(src,str): return '{}'.format(src)
    if isinstance(src,int): return int('{}'.format(src))
    if isinstance(src,float): return float('{}'.format(src))
    if PyVer(2):
        if isinstance(src,long): return long('{}'.format(src))

def TypeName(obj):
    '''
    Get input's Type,Instance's name
    '''
    obj_dir=dir(obj)
    obj_name=type(obj).__name__
    if obj_name in ['function']: return obj_name
    if obj_name in ['str']:
        #try:
        #    obj_tmp=eval(obj)
        #    if type(obj_tmp).__name__ not in ['module','classobj','function','response','request']:
        #        obj_name=eval(obj).__name__
        #        if obj_name.lower() == obj.lower(): return obj.lower()
        #except:
        #    if obj.lower() in ['module','classobj','function','unknown','response','request']:
        #        return obj.lower()
        #    elif obj in ['kDict','kList','DICT']: # Special case name
        #        return obj
        return 'str'
    if '__dict__' in obj_dir:
        if obj_name == 'type': return 'classobj'
        if obj_name == 'Response': return 'response'
        if obj_name == 'Request': return 'request'
        return 'instance'
    try:
        if obj_name == 'type':
            return obj.__name__
        return obj_name.lower() # Object Name
    except:
        return 'unknown'

def Type(*inps,**opts):
    '''
    Similar as isinstance(A,())
    support : basic type and ('byte','bytes'),('obj','object'),('func','unboundmethod','function'),('classobj','class'),'generator','method','long',....
    '''
    def NameFix(i):
        if i == str: return 'str'
        if i in ['byte','bytes']: return 'bytes'
        if i in ['obj','object']: return 'object'
        if i in ['func','unboundmethod']: return 'function'
        if i in ['class','classobj']: return 'classobj'
        if i in ['yield','generator']: return 'generator'
        if i in ['builtinfunction','builtinmethod','builtin_function_or_method']: return 'builtin_function_or_method'
        # function: function and instance's function in Python3
        # method:  class's function in Python3
        # instancemethod: instance's and class's function in Python2
        if i in ['method','classfunction','instancemethod','unboundmethod']: return 'method'
        # Fix python version for long
        if i in ['long']:
            if PyVer('>',3): return 'int'
        return i
    inps_l=len(inps)
    if inps_l == 0:
        StdErr('minimum over 1 requirement')
        return
    obj_type=TypeName(inps[0])
    if inps_l == 1: return obj_type
    for check in inps[1:]:
        if isinstance(check,(tuple,list)):
            for i in check:
                #i=NameFix(i)
                check_type=TypeName(i)
                if check_type == 'str': check_type=NameFix(i)
                #check_type=i if a == 'str' else a
                if obj_type == check_type:
                    if opts.get('data'):
                        if IsNone(inps[0]):
                            return False
                    return True
        else:
            #check=NameFix(check)
            check_type=TypeName(check)
            if check_type == 'str':
                check_type=NameFix(check)
            if obj_type == check_type:
                if opts.get('data'):
                    if IsNone(inps[0]):
                        return False
                return True
    return False

class FIND:
    '''
    Searching regular expression form data and return the data
    '''
    def __init__(self,src=None,find=None,out='index',word=False):
        self.src=src
        if isinstance(find,str):
            find=find.replace('*','.+').replace('?','.')
            if word:
                self.find_re=re.compile(r'\b({0})\b'.format(find),flags=re.IGNORECASE)
            else:
                self.find_re=re.compile(find,flags=re.IGNORECASE)
        self.find=find
        self.out=out

    def From(self,data,symbol='\n'):
        rt=[]

        def Search(data,key,rt):
            found=self.find_re.findall(data)
            if found:
                if self.out in ['found']:
                    rt=rt+found
                elif self.out in ['index','idx','key']:
                    rt.append(key)
                elif self.out in ['all','*']:
                    rt.append((key,data))
                else:
                    rt.append(data)
            return rt

        if Type(data,str):
            data=data.split(symbol)
        if Type(data,list,tuple):
            for i in range(0,len(data)):
                if Type(data[i],(list,tuple,dict)):
                    sub=self.From(data[i],symbol=symbol)
                    if sub:
                        if self.out in ['key','index','idx']:
                            for z in sub:
                                rt.append('{}/{}'.format(i,z))
                        else:
                            rt=rt+sub
                elif Type(data[i],str):
                    rt=Search(data[i],i,rt)
        elif Type(data,dict):
            for i in data:
                if Type(data[i],(list,tuple,dict)):
                    sub=self.From(data[i],symbol=symbol)
                    if sub:
                        if self.out in ['key','index','idx']:
                            for z in sub:
                                rt.append('{}/{}'.format(i,z))
                        else:
                            rt=rt+sub
                elif Type(data[i],str):
                    rt=Search(data[i],i,rt)
        else:
             return 'Unknown format'
        return rt

    def Find(self,find,src='_#_',sym='\n',default=[],out=None,findall=True,word=False,mode='value',prs=None,line_num=False,peel=None,idx=None):
        if IsNone(src,chk_val=['_#_'],chk_only=True): src=self.src
        #if Type(src,'instance','classobj'):
        # if src is instance or classobj then search in description and made function name at key
        if isinstance(src,(list,tuple)):
            rt=[]
            for i in range(0,len(src)):
                a=self.Find(find,src[i],sym=sym,default=[],out='list',findall=findall,word=word,mode=mode,prs=prs,line_num=line_num,peel=peel,idx=idx)
                if a: rt=rt+a
            if len(rt):
                return rt
        elif isinstance(src,dict):
            path=[]
            for key in src:
                if mode in ['key','*','all']: # find in key only
                    if find == key:
                        path.append(key)
                found=src.get(key,None)
                if isinstance(found,dict):
                    if dep in found:
                         if mode in ['value','*','all'] and (find == found[dep] or (type(found[dep]) in [DICT,dict,list,tuple] and find in found[dep]) or (type(find) is str and type(found[dep]) is str and find in found[dep])): # find in 'find' only
                              # Value find
                              path.append(key)
                         elif isinstance(found[dep], dict): # recursing
                              path=path+self.Find(find,found[dep],proper=proper,mode=mode)
                    else:
                         if mode in ['value','*','all'] and find == found or (type(found) in [list,tuple] and find in found) or (type(find) is str and type(found) is str and find in found):
                             path.append(key)
                         else:
                             for kk in self.Find(find,src[key],proper=proper,mode=mode,out=dict,default={}): # recursing
                                 path.append(key+'/'+kk)
                else:
                    if mode in ['value','*','all'] and find == found or (type(found) in [list,tuple] and find in found) or (type(find) is str and type(found) is str and find in found):
                        path.append(key)
            return path
        elif isinstance(src,str):
            if findall:
                if prs == '$': idx=-1
                if prs == '^': idx=0
                if sym:
                    string_a=src.split(sym)
                else:
                    string_a=[src]
                if isinstance(find,dict):
                    found={}
                    for nn in range(0,len(string_a)):
                        for dd in find:
                            didx=None
                            if isinstance(find[dd],dict):
                                fmt=next(iter(find[dd]))
                                try:
                                    didx=int(find[dd][fmt].get('idx'))
                                except:
                                    didx=None
                            else:
                                fmt=find[dd]
#                            aa=re.compile(fmt).findall(string_a[nn])
                            if word:
                                aa=re.compile(r'\b({0})\b'.format(fmt),flags=re.IGNORECASE).findall(string_a[nn])
                            else:
                                aa=re.compile(fmt,flags=re.IGNORECASE).findall(string_a[nn])
                            if aa:
                                for mm in aa:
                                    if isinstance(mm,(tuple,list)) and isinstance(didx,int):
                                        if line_num:
                                            found.update({dd:{'data':mm[didx],'line':nn,'src':string_a[nn]}})
                                        else:
                                            found.update({dd:mm[didx]})
                                    else:
                                        if line_num:
                                            found.update({dd:{'data':mm,'line':nn,'src':string_a[nn]}})
                                        else:
                                            found.update({dd:mm})
                    #if found: return OutFormat(found,out=out,peel=peel)
                    return OutFormat(found,out=out,peel=peel,org=src,default=default)
                else:
                    found=[]
                    for nn in range(0,len(string_a)):
                        if isinstance(find,(list,tuple)):
                            find=list(find)
                        else:
                            find=[find]
                        for ff in find:
                            #aa=re.compile(ff).findall(string_a[nn])
                            if word:
                                aa=re.compile(r'\b({0})\b'.format(ff),flags=re.IGNORECASE).findall(string_a[nn])
                            else:
                                aa=re.compile(ff,flags=re.IGNORECASE).findall(string_a[nn])
                            for mm in aa:
                                if isinstance(idx,int):
                                    if isinstance(mm,(tuple,list)):
                                        if line_num:
                                            found.append((mm[idx],nn,string_a[nn]))
                                        else:
                                            found.append(mm[idx])
                                else:
                                    if line_num:
                                        found.append((mm,nn,string_a[nn]))
                                    else:
                                        found.append(mm)
                    #if found:return OutFormat(found,out=out,peel=peel)
                    return OutFormat(found,out=out,peel=peel,org=src,default=default)
#                match=find_re.findall(src)
#                if match: return OutFormat(match,out=out)
            elif isinstance(find,str):
                if word:
                    find_re=re.compile(r'\b({0})\b'.format(find),flags=re.IGNORECASE)
                else:
                    find_re=re.compile(find,flags=re.IGNORECASE)
                match=find_re.search(src)
                if match: return OutFormat([match.group()],out=out,peel=peel)
        #return OutFormat(default,out=out,peel=peel)
        return OutFormat([],out=out,peel=peel,org=src,default=default)
def Found(data,find,digitstring=False,word=False,white_space=True,sense=True,location=False):
    '''
    if found <find> in <data> then return True, not then False
    If find "[All]" then you can type "\[All\]" at the <find> location
    if not then "[]" will be work with re expression
    <find> rule:
       re.compile regular expression
       any keep characters  : *
       any single character : ?
       ^                    : start
       $                    : end
    <option>
       sense                : True:(default) sensetive, False: lower and upper is same
       white_space          : True:(default) keep white_space, False: ignore white_space
       word                 : True: <find> is correct word, False:(default) <find> in insde string
       digitstring          : True: string and intiger is same, False:(default) different
       location             : True: return found location ex:(3,10), False:(default) return True/False
    '''
    def _Found_(data,find,word,sense,location):
        data_type=type(data).__name__
        if data_type == 'bytes':
            find=Bytes(find)
        elif data_type == 'str':
            find=Str(find)
        if data == find: #Same Data
            if location: return [(0,len(data))]
            return True 
        if data_type == 'bytes':
            find=find.replace(b'*',b'.+').replace(b'?',b'.') # Fix * or ? case
            if word and find: find=Bytes(r'\b(')+find+Bytes(')\b')
        elif data_type == 'str':
            find=find.replace('*','.+').replace('?','.') # Fix * or ? case
            if word and find: find=r'\b({0})\b'.format(find)
        if not find: return False
        try:
            if sense:
                mm=re.compile(find)
            else:
                mm=re.compile(find,flags=re.IGNORECASE)
        except:
            return False
        #if word:
        #    ff=re.match(mm,data) # Find First Matched(word type) location
        #else:
        #    #ff=mm.findall(data) # Find All Data
        ff=mm.finditer(data)
        if bool(ff):
            rt=[]
            for i in list(ff): # when change list(ff) then lost data
                rt.append(i.span())
            if location: return rt
            return True if rt else False
        return False

    data=WhiteStrip(data,BoolOperation(white_space,mode='oppisit'))
    type_data=type(data).__name__
    type_find=type(find).__name__
    if digitstring:
        if type_data in ['int','float']:
            data='{}'.format(data)
            type_data='str'
        if type_find in ['int','float']:
            find='{}'.format(find)
            type_find='str'
    if type_data in ['str','bytes'] and type_find in ['str','bytes']:
        return _Found_(data,find,word,sense,location)
    return data == find

def IsSame(src,dest,sense=False,order=False,_type_=False,digitstring=True,white_space=False):
    '''
    return True/False
    Check same data or not between src and dest datas
    <dest> rule:
       re.compile format
       any keep characters  : *
       any single character : ?
       ^                    : start
       $                    : end
    <option>
       order                : True: if list,tuple then check ordering too, False:(default) just check data is same or not
       Type                 : True: check Type only, False:(default) check data
       sense                : True: sensetive, False:(default) lower and upper is same
       white_space          : True: keep white space, False:(default) ignore white_space
       digitstring          : True:(default) string and intiger is same, False: different
    '''
#    src_type=TypeName(src)
#    dest_type=TypeName(dest)
    if _type_ is True: # If check type only
        return Type(src,dest)
#        if src_type == 'unknown' and dest_type == 'unknown':
#            return type(src) == type(dest)
#        return src_type == dest_type
#    if src_type in ['str','bytes'] and dest_type in ['str','bytes']:# and dest:
    if Type(src,('str','bytes')) and Type(dest,('str','bytes')):# and dest:
#        tobyte=True if dest_type == 'bytes' or src_type == 'bytes' else False
#        if tobyte:
        if Type(dest,'bytes') or Type(src,'bytes'):
            src=Bytes(src)
            dest=Bytes(dest)
            if src == dest: return True
            if dest:
                if dest[0] != b'^': dest=b'^'+dest
                if dest[-1] != b'$': dest=dest+b'$'
#            src_type='bytes'
#            dest_type='bytes'
        else:
            src=Str(src)
            dest=Str(dest)
            if src == dest: return True
            if dest:
                if dest[0] != '^': dest='^'+dest
                if dest[-1] != '$': dest=dest+'$'
#            src_type='str'
#            dest_type='str'
    if isinstance(src,(list,tuple)) and isinstance(dest,(list,tuple)):
        if sense and order: return src == dest
        if len(src) != len(dest): return False
        if order:
            for j in range(0,len(src)):
                if not Found(src[j],dest[j],digitstring=digitstring,white_space=white_space,sense=sense): return False
            return True
        else:
            a=list(src[:])
            b=list(dest[:])
            for j in range(0,len(src)):
                for i in range(0,len(dest)):
                    if (isinstance(src[j],dict) and isinstance(dest[j],dict)) or (isinstance(src[j],(list,tuple)) and isinstance(dest[j],(list,tuple))):
                        if IsSame(src[j],dest[i],sense,order,_type_,digitstring,white_space):
                            a[j]=None
                            b[i]=None
                    elif Found(src[j],dest[i],digitstring=digitstring,white_space=white_space,sense=sense):
                        a[j]=None
                        b[i]=None
            if a.count(None) == len(a) and b.count(None) == len(b): return True
            return False
    elif isinstance(src,dict) and isinstance(dest,dict):
        if sense: return src == dest
        if len(src) != len(dest): return False
        for j in src:
            if j in dest:
                if (isinstance(src[j],dict) and isinstance(dest[j],dict)) or (isinstance(src[j],(list,tuple)) and isinstance(dest[j],(list,tuple))):
                    if not IsSame(src[j],dest[i],sense,order,_type_,digitstring,white_space): return False
                else:
                    if not Found(src[j],dest[j],digitstring=digitstring,white_space=white_space,sense=sense): return False
        return True
    else:
        return Found(src,dest,digitstring=digitstring,white_space=white_space,sense=sense)

def IsIn(find,dest,idx=False,default=False,sense=False,startswith=True,endswith=True,digitstring=True,word=True,white_space=False,order=False,**opts):
    '''
    Check key or value in the dict, list or tuple then True, not then False
    '''
    _type_=opts.get('Type',opts.get('_type_',False))
    #dest_type=TypeName(dest)
    #if dest_type in ['list','tuple','str','bytes']:
    if Type(dest,('list','tuple','str','bytes')):
        #if TypeName(idx) == 'int':
        if Type(idx,'int'):
            idx=FixIndex(dest,idx,default=False,err=True)
            if idx is False: return default
            #if dest_type in ['str','bytes']:
            if Type(dest,('str','bytes')):
                if Found(dest[idx:],find,digitstring,word,white_space,sense): return True
            else:
                if Found(dest[idx],find,digitstring,word,white_space,sense): return True
        else:
            for i in dest:
                if IsSame(i,find,sense,order,_type_,digitstring,white_space): return True
    elif isinstance(dest, dict):
        if idx in [None,'',False]:
            for i in dest:
                if IsSame(i,find,sense,order,_type_,digitstring,white_space): return True
        else:
            if Found(dest.get(idx),find,digitstring,word,white_space,sense): return True
    return default

def BoolOperation(a,mode=bool):
    if type(a).__name__ == 'bool':
        if mode is bool: return a
        if mode in ['opposition','opposit']:
            return not a

def WhiteStrip(src,mode=True):
    '''
    remove multi space to single space, remove first and end space
    others return original
    '''
    if mode is True and type(src).__name__ in ('str','bytes'): return src.strip()
    return src

def IsNone(src,**opts):
    '''
    Check the SRC is similar None type data('',None) or not
    -check_type=<type> : include above and if different type then the return True
    -list_none :
      - False: check index item in the source (default)
      - True : check all list of source
    -index   : if source is list then just want check index item
    -space   :
      - True : aprove space to data in source
      - False: ignore space data in source
    '''
    value=opts.get('value',opts.get('chk_val',['',None]))
    space=opts.get('space',True)
    chk_only=opts.get('chk_only',opts.get('check_only',False))
    index=opts.get('index',opts.get('idx'))
    list_none=opts.get('LIST',False)

    #check type
    CheckType=opts.get('check_type',None)
    _type_=False
    if CheckType is not None:
        value=value+[CheckType]
        _type_=True
    def _IsIn_(src,value,sense=False):
        if isinstance(value,(list,tuple)):
            for i in value:
                if not sense and  type(i).__name__ in ['str','bytes'] and type(src).__name__ in ['str','bytes']:
                    if Str(i).lower() == Str(src).lower(): return True
                else:
                    if i == src: return True
        else:
            if not sense and type(value).__name__ in ['str','bytes'] and type(src).__name__ in ['str','bytes']:
                if Str(value).lower() == Str(src).lower(): return True
            else:
                if value == src: return True
        return False
        
    src=WhiteStrip(src,BoolOperation(space,mode='opposit'))
    if _IsIn_(src,value,sense=False): return True
    if src:
        if isinstance(src,(list,tuple)):
            if list_none:
                for i in src:
                    if not _IsIn_(WhiteStrip(i,BoolOperation(space,mode='opposit')),value,sense=False): return False
                return True
            elif isinstance(index,int) and len(src) > abs(index):
                if _IsIn_(WhiteStrip(src[index],BoolOperation(space,mode='opposit')),value,sense=False): return True
        elif isinstance(src,dict):
            if index in src:
                if _IsIn_(WhiteStrip(src[index],BoolOperation(space,mode='opposit')),value,sense=False): return True
    if chk_only:
        # i want check Type then different type then return True
        if _type_:
            #if TypeName(src) != TypeName(CheckType): return True
            return False if Type(src,CheckType) else True
        return False
    if not isinstance(src,(bool,int)):
        if not src: return True
    # i want check Type then different type then return True
    if _type_:
        #if TypeName(src) != TypeName(CheckType): return True
        return False if Type(src,CheckType) else True
    return False

def IsVar(src,obj=None,default=False,mode='all',parent=0):
    '''
    Check the input(src) is Variable name or not (in OBJ or in my function)
    '''
    oo=Variable(src,obj=obj,parent=1+parent,history=False,default='_#_',mode=mode)
    if oo == '_#_': return default
    return True

def IsFunction(src,find='_#_'):
    '''
    Check the find is Function in src object
    '''
    if IsNone(src):
        if isinstance(find,str) and find != '_#_':
            find=Global().get(find)
        return inspect.isfunction(find)
    else:
        if type(src).__name__ == 'function': return True # src is function then
    # find function in object
    aa=[]
    if type(find).__name__ == 'function': find=find.__name__
    if not isinstance(find,str): return False
    if isinstance(src,str): src=sys.modules.get(src)
    if inspect.ismodule(src) or inspect.isclass(src):
        for name,fobj in inspect.getmembers(src):
            if inspect.isfunction(fobj): # inspect.ismodule(obj) check the obj is module or not
                aa.append(name)
    else:
        for name,fobj in inspect.getmembers(src):
            if inspect.ismethod(fobj): # inspect.ismodule(obj) check the obj is module or not
                aa.append(name)
    if find in aa: return True
    return False

def IsBytes(src):
    '''
    Check data is Bytes or not
    '''
    if PyVer(3):
        if isinstance(src,bytes):
            return True
    return False

def IsInt(src,mode='all'):
    '''
    Check data is Int or not
    - mode : int => check only int
             str => int type string only
             all => Int and int type string
    '''
    def _int_(data):
        try:
            int(data)
            return True
        except:
            return False

    if not isinstance(src,bool):
        if mode in [int,'int']:
            if isinstance(src,int):
                return True
        elif mode in [str,'str','text','string']:
            if Type(src,('str','bytes')):
                return _int_(src)
        else:
            return _int_(src)
    return False

def Dict(*inp,**opt):
    '''
    Dictionary
    - Define
    - marge
    - Update
    - Append
    support : Dict, list or tuple with 2 data, dict_items, Django request.data, request data, like path type list([('/a/b',2),('/a/c',3),...]), kDict
    '''
    src={}
    if len(inp) >= 1:
        src=inp[0]
    src_type=TypeName(src)
    if isinstance(src,dict):
        if src_type == 'QueryDict': # Update data at request.data of Django
            try:
                src._mutable=True
            except:
                StdErr("src(QueryDict) not support _mutable=True parameter\n")
        for dest in inp[1:]:
            if not isinstance(dest,dict): continue
            for i in dest:
                if i in src and isinstance(src[i],dict) and isinstance(dest[i],dict):
                    src[i]=Dict(src[i],dest[i])
                else:
                    src[i]=dest[i]
    elif src_type in ['dict_items']:
        src=dict(src)
    elif src_type in ['kDict']:
        src=src.Get()
    elif src_type in ['list','tuple']:
        tmp={}
        for ii in src:
            if isinstance(ii,tuple) and len(ii) == 2:
                if ii[0][0] == '/':
                    src_a=ii[0].split('/')[1:]
                    tt=tmp
                    for kk in src_a[:-1]:
                        if kk not in tt: tt[kk]={}
                        tt=tt[kk]
                    tt[src_a[-1]]=ii[1]
                else:
                    tmp[ii[0]]=ii[1]
        src=tmp
    elif src_type in ['ImmutableMultiDict']:
        if len(src) > 0:
            tmp={}
            for ii in src:
                tmp[ii]=src[ii]
            src=tmp
    else:
        src={}
    #Update Extra inputs
    for ext in inp[1:]:
        extra=Dict(ext)
        if Type(extra,dict):
            src.update(extra)
    #Update Extra option data
    if opt:
        for i in opt:
            if i in src and isinstance(src[i],dict) and isinstance(opt[i],dict):
                src[i]=Dict(src[i],opt[i])
            else:
                src[i]=opt[i]
    return src

def CompVersion(*inp,**opts):
    '''
    input: source, compare_symbol(>x,<x,==,!xx), destination
      return BOOL
    input: source, destination, compare_symbol='>x,<x,==,!xx'
      return BOOL
    input: source, destination
      - without compare_symbol
      - out=sym      : return symbol (>, ==, <)  (default)
      - out=int      : return 1(>), 0(==), -1(<)
      - out=str      : return bigger(>), same(==), lower(<)
    input: source
      - out=str      : return '3.0.1' (default)
      - out=tuple    : return to tuple type (3,0,1)
      - out=list     : return to list type [3,0,1]
    version_symbol or symbol : default '.'

    sort list
    <list>.sort(key=CompVersion)  or sorted(<list>,key=CompVersion)
    '''
    version_symbol=opts.get('version_symbol',opts.get('symbol','.'))
    compare_symbol=opts.get('compare_symbol',opts.get('compare'))
    if compare_symbol == 'is': compare_symbol='=='
    elif compare_symbol == 'is not': compare_symbol='!='
    out=opts.get('out',opts.get('output',str))
    def _clean_(a):
        for i in range(0,len(a)):
            if a[i] == '': a[i]=0
        for i in range(len(a)-1,0,-1):
            if i > 1 and a[i] == 0 and a[i-1]==0:
                a.pop(i)
        return a
    def Comp(src,dest):
        len_src=len(src)
        len_dest=len(dest)
        bigger=len_dest if len_dest > len_src else len_src
        for i in range(0,bigger):
            if i < len_src and i < len_dest:
                ss=src[i]
                dd=dest[i]
                if type(ss) != type(dd):
                    ss=Str(src[i])
                    ss=Str(dest[i])
                if ss > dd:
                    return 1
                elif ss < dd:
                    return -1
            elif i < len_src:
                return 1
            elif i < len_dest:
                return -1
        return 0
    def MkVerList(src,version_symbol):
        if isinstance(src,dict): src=src.get('version',src.get('__version__'))
        if Type(src,('str','bytes')):
            src=Str(src).split(version_symbol)
        elif Type(src,('int','float')):
            src=[src]
        elif isinstance(src, tuple):
            src=list(src)
        if isinstance(src,list):
            return tuple(_clean_([ Int(i) for i in src ]))
    src=[]
    dest=[]
    if len(inp) == 1:
        ver_tuple=MkVerList(inp[0],version_symbol)
        if out in [str,'str']:
            return '.'.join([Str(i) for i in ver_tuple])
        elif out in [list,'list']:
            return list(ver_tuple)
        return ver_tuple
    elif len(inp) == 2:
        src=MkVerList(inp[0],version_symbol)
        dest=MkVerList(inp[1],version_symbol)
    elif len(inp) == 3:
        src=MkVerList(inp[0],version_symbol)
        compare_symbol=inp[1]
        dest=MkVerList(inp[2],version_symbol)
    if src and dest:
        cc=Comp(src,dest)
        if isinstance(compare_symbol,str) and compare_symbol:
            rev=False
            if '!' in compare_symbol: rev=True
            if cc == 0:
                if '=' in compare_symbol:
                    return False if rev else True
            elif cc == 1:
                if '>' in compare_symbol:
                    return False if rev else True
                if rev: return True
            elif cc == -1:
                if '<' in compare_symbol:
                    return False if rev else True
            return True if rev else False
        else:
            if out in [int,'int','integer','num']: return cc
            if cc > 0:
                if out in [str,'str','string']: return 'bigger(>)'
                return '>'
            elif cc < 0:
                if out in [str,'str','string']: return 'lower(<)'
                return '<'
            if out in [str,'str','string']: return 'same(=)'
            return '=='


def ModVersion(mod):
    '''
    Find Module Version
    '''
    if PyVer(3,8,'<'): 
        import pkg_resources
        try:
            return pkg_resources.get_distribution(mod).version
        except:
            return None
    else:
        from importlib.metadata import version
        try:
            return version(mod)
        except:
            return None

# Python 2 has built in reload
if PyVer(3,4,'<='): 
    from imp import reload # Python 3.0 - 3.4 
elif PyVer(3,4,'>'): 
    from importlib import reload # Python 3.5+

def GlobalEnv(): # Get my parent's globals()
    '''
    Get Global Environment of the python code
    '''
    return dict(inspect.getmembers(inspect.stack()[1][0]))["f_globals"]

def Install(module,install_account='',mode=None,upgrade=False,version=None,force=False,pkg_map=None,err=False):
    '''
    Install python module file
    module name
    install_accout='' : default None,  --user : install on account's directory
    upgrade :
      False : default
      True  : Install or Upgrade the module
    version :
      None  : default
      <version>: Check the version
                 == <version> : if not Same version then install at the same version
                 >= <version> : if not bigger the version then install or upgrade
                 <= <version> : if not lower the version then install at the version
    force  : default False
      True : if installed then force re-install, not then install
    pkg_map: mapping package name and real package name
      format => { <pkg name>: <real install pkg name> }
    err    : default False
      True : if installing got any isseu then crashing
      False: if installing got any issue then return False
    '''
    # version 
    #  - same : ==1.0.0
    #  - big  : >1.0.0
    #  - or   : >=1.3.0,<1.4.0
    # pip module)
    #pip_main=None
    #if hasattr(pip,'main'):
    #    pip_main=pip.main
    #elif hasattr(pip,'_internal'):
    #    pip_main=pip._internal.main
    if pkg_map is None:
        pkg_map={
           'magic':'python-magic',
           'bdist_wheel':'wheel',
        }

    pip_main=check_call
    if not pip_main:
        print('!! PIP module not found')
        return False

    pkg_name=module.split('.')[0]
    install_name=pkg_map.get(pkg_name,pkg_name)
    # Check installed package
    # pip module)
    #install_cmd=['install']
    if os.path.basename(sys.executable).startswith('python'):
        install_cmd=[sys.executable,'-m','pip','install']
    else:
        install_cmd=['python3','-m','pip','install']
    ipkgs=working_set
    pkn=ipkgs.__dict__.get('by_key',{}).get(install_name)
    if pkn:
        if version:
            for i in range(len(version)-1,0,-1):
                if version[i] in ['>','<','=']: break
            ver_str=version[i+1:]
            compare_symbol=version[:i+1]
            if not CompVersion(pkn.version,compare_symbol,ver_str):
                upgrade=True
                install_cmd.append(install_name+version)
            else:
                return True
        else:
            install_cmd.append(install_name)
        if force: install_cmd.append('--force-reinstall')
        if install_account: install_cmd.append(install_account)
        if not force and upgrade: install_cmd.append('--upgrade')
        if pip_main and force or upgrade:
            if err:
                if pip_main(install_cmd) == 0: return True
                return False
            else:
                try:
                    if pip_main(install_cmd) == 0: return True
                    return False
                except:
                    return False
        return True

#    if mode == 'git':
#        git.Repo.clone_from(module,'/tmp/.git.tmp',branch='master')
#        build the source and install
#        return True

    if version:
        install_cmd.append(install_name+version)
    else:
        install_cmd.append(install_name)
    if force: install_cmd.append('--force-reinstall')
    if install_account: install_cmd.append(install_account)

    if err:
        if pip_main(install_cmd) == 0: return True
    else:
        try:
            if pip_main(install_cmd) == 0: return True
        except:
            pass
    return False


def ModName(src):
    '''
    Analysis Module name from input string
    '''
    rt=True
    class_name=None
    module_name=None
    alias_name=None
    version=None
    symbol=None
    if isinstance(src,str):
        src_a=src.split()
        #remove from , import tag
        if src_a[0] in ['from','import']:
            del src_a[0]
        module_name=src_a[0]
        #remove version information
        src_a_len=len(src_a)
        for i in range(src_a_len-1,0,-1):
            if src_a[i] in ['==','=','>','>=','<','<=']:
                if i < src_a_len:
                    symbol=src_a[i]
                    version=src_a[i+1]
                break
        if 'import' in src_a:
            import_idx=src_a.index('import')
            if src_a_len > import_idx+1:
                class_name=src_a[import_idx+1]
            else:
                rt=False
        if 'as' in src_a:
            alias_idx=src_a.index('as')
            if src_a_len > alias_idx+1:
                alias_name=src_a[alias_idx+1]
            else:
                rt=False
        if alias_name is None:
            alias_name=module_name
    return rt,module_name,alias_name,class_name,version,symbol

#def ModLoad(inp,force=False,globalenv=dict(inspect.getmembers(inspect.stack()[1][0]))["f_globals"],unload=False,re_load=False):
def ModLoad(inp,force=False,globalenv=Global(),unload=False,re_load=False):
    '''
    Load python module
    '''
    def Reload(name):
        if isinstance(name,str):
            globalenv[name]=reload(globalenv[name])
        else:
            name=reload(name)
        return True

    def Unload(name):
        if isinstance(name,str):
            del globalenv[name]
        elif isinstance(name,type(inspect)):
            try:
                nname = name.__spec__.name
            except AttributeError:
                nname = name.__name__
            if nname in globalenv: del globalenv[nname]

    if not inp: return 0,''
#    inp_a=inp.split()
    wildcard=None
    class_name=None
#    if inp_a[0] in ['from','import']:
#        del inp_a[0]
#    name=inp_a[-1]
#    module=inp_a[0]
    ok,module,name,class_name,version,symbol=ModName(inp)
    if ok is False:
            print('*** Wrong information')
            return 0,module
    if unload:
        #if '*' not in inp and name in globalenv: # already loaded
        if class_name != '*' and name in globalenv: # already loaded
            Unload(name) #Unload
        return 2,module #Not loaded

#    import inspect,sys
#    print(inspect.stack())
#    dep=len(inspect.stack())-1
#    fname=sys._getframe(dep).f_code.co_name
#    if fname == '_bootstrap_inner' or name == '_run_code':
#        fname=sys._getframe(2).f_code.co_name
#    print('>>',fname,':::',name,class_name,module)
    #if '*' not in inp and name in globalenv: # already loaded
    if class_name != '*' and name in globalenv: # already loaded
        if re_load:
            Reload(name) # if force then reload
            return 0,module
        elif force:
            Unload(name) #if force then unload and load again
#    if 'import' in inp_a:
#        import_idx=inp_a.index('import')
#        if len(inp_a) > import_idx+1:
#            class_name=inp_a[import_idx+1]
#        else:
#            print('*** Wrong information')
#            return 0,module
    try:
        if class_name:
            if class_name == '*':
                wildcard=import_module(module)
            else:
                try:
                    globalenv[name]=getattr(import_module(module),class_name)
                except:
                    globalenv[name]=import_module('{}.{}'.format(module,class_name))
        else:
            globalenv[name]=import_module(module)
        return wildcard,module # Loaded. So return wildcard information
    except AttributeError: # Try Loading looped Module/Class then ignore  or Wrong define
        return 0,module
    except ImportError: # Import error then try install
        return 1,module

def Import(*inps,**opts):
    '''
    basic function of import
    if not found the module then automaticall install
    version check and upgrade, reinstall according to the version
    support requirement files

    inps has "require <require file>" then install the all require files in <require file>
    Import('<module name>  >= <version>') : Check version and lower then automaticall upgrade 
    Import('<module name>  == <version>') : Check version and different then automaticall reinstall with the version
    Import('<module name>',path='AAA,BBB,CCCC') : import <module name> from default and extra AAA and BBB and CCC.
    -path=       : searching and the module in the extra path (seperate with ',' or ':' )
    -force=True  : unload and load again when already loaded (default: False)
    -reload=True : run reload when already loaded (default: False)
    -unload=True : unload module (default : False)
    -err=True    : show install or loading error (default: False)
    -dbg=True    : show comment (default : False)
    -install_account=: '--user','user','myaccount','account',myself then install at my local account
                 default: Install by System default setting

    '''
    globalenv=opts.get('globalenv',dict(inspect.getmembers(inspect.stack()[1][0]))["f_globals"]) # Get my parent's globals()
    force=opts.get('force',None) # unload and load again when already loaded (force=True)
    re_load=opts.get('reload',None) #  run reload when already loaded
    unload=opts.get('unload',False) # unload module when True
    err=opts.get('err',False) # show install or loading error when True
    default=opts.get('default',False)
    dbg=opts.get('dbg',False) # show comment when True
    #install_account=opts.get('install_account','--user')
    install_account=opts.get('install_account','') # '--user','user','myaccount','account',myself then install at my local account

    #Append Module Path
    base_lib_path=['/usr/lib/python3.6/site-packages','/usr/lib64/python3.6/site-packages','/usr/local/python3.6/site-packages','/usr/local/lib/python3.6/site-packages','/usr/local/lib64/python3.6/site-packages']
    path=opts.get('path') # if the module file in a special path then define path
    if not IsNone(path,check_type=str):
        if ',' in path:
            base_lib_path=base_lib_path+path.split(',')
        elif ':' in path:
            base_lib_path=base_lib_path+path.split(':')
        else:
            base_lib_path=base_lib_path+[path]
    elif isinstance(path,(list,tuple)):
        base_lib_path=base_lib_path+list(path)
    home=Path('~')
    if isinstance(home,str):
        base_lib_path.append('{}/.local/lib/python3.6/site-packages'.format(home))
    for ii in base_lib_path:
        if os.path.isdir(ii) and not ii in sys.path:
            sys.path.append(ii)

    if install_account in ['user','--user','personal','myaccount','account','myself']:
        install_account='--user'
    else:
        install_account=''

    def CheckObj(obj):
        obj_dir=dir(obj)
        obj_name=type(obj).__name__
        if obj_name in ['function']: return obj_name
        if '__dict__' in obj_dir:
            if obj_name == 'type': return 'classobj'
            return 'instance'
        return obj_name.lower()

    ninps=[]
    for inp in inps:
        ninps=ninps+inp.split(',')
    for inp in ninps:
        # if inp is File then automatically get the Path and file name
        # and automatically adding Path to path and import the File Name
        if os.path.isfile(inp):
            ipath=os.path.dirname(inp)
            ifile=os.path.basename(inp)
            ifile_a=ifile.split('.')
            if len(ifile_a) > 2:
                if dbg:
                    print('*** Not support {} filename'.format(inp))
                continue
            inp=ifile_a[0]
            if ipath not in sys.path:
                sys.path=[ipath]+sys.path

        inp_a=inp.split()
        version=None
        ver_compare=None
        if len(inp_a) ==2 and inp_a[0] in ['require','requirement']:
            if os.path.isfile(inp_a[1]):
                rq=[]
                with open(inp_a[1]) as f:
                    rq=f.read().split('\n')
                for ii in rq:
                    if not ii: continue
                    ii_l=ii.split()
                    version=None
                    if len(ii_l) in [2,3]:
                        if '=' in ii_l[1] or '>' in ii_l[1] or '<' in ii_l[1]:
                            if len(ii_l) == 3:
                                version=ii_l[1]+ii_l[2]
                            else:
                                version=ii_l[1]
                    ii_a=ii_l[0].split(':')
                    if len(ii_a) == 2:
                        ic=Install(ii_a[1],install_account,version=version)
                    else:
                        ic=Install(ii_a[0],install_account,version=version)
                    if ic:
                        loaded,module=ModLoad(ii_a[0],force=force,globalenv=globalenv,re_load=re_load)
            continue
        else:
            ok,module,name,class_name,version,symbol=ModName(inp)
            if ok and version and symbol:
                cur_version=ModVersion(module)
                #Mismatched version or not installed then install
                if cur_version is None or (cur_version and not CompVersion(cur_version,symbol,version)):
                    if symbol in ['>','>=']:
                        Install(module,install_account=install_account,upgrade=True)
                    elif symbol in ['==']:
                        Install(module,install_account=install_account,upgrade=True,version='== {}'.format(version))
                    elif symbol in ['<','<=']:
                        Install(module,install_account=install_account,upgrade=True,version='{} {}'.format(symbol,version))

        #Load module
        loaded,module=ModLoad(inp,force=force,globalenv=globalenv,unload=unload,re_load=re_load)
        if loaded == 2: #unloaded
            continue
        if loaded == 1: #not installed
            if Install(module,install_account):
                loaded,module=ModLoad(inp,force=force,globalenv=globalenv,re_load=re_load)
            else:
                if dbg:
                    print('*** Import Error or Need install with SUDO or ROOT or --user permission')
                continue
        if loaded not in [None,0,1]: # import wildcard
            for ii in loaded.__dict__.keys():
                if ii not in ['__name__','__doc__','__package__','__loader__','__spec__','__file__','__cached__','__builtins__']:
                    if ii in globalenv:
                        # swap Same Name between module(my module of the wild card) and class(wild card import class name)
                        if ii in loaded.__dict__.keys():
                            if CheckObj(globalenv[ii]) == 'module' and CheckObj(loaded.__dict__[ii]) == 'classobj':
#                                TMP=globalenv[ii] # move to local temporay 
                                globalenv[ii]=loaded.__dict__[ii]
                                continue
                        if not force: continue # Not force then ignore same name
                    globalenv[ii]=loaded.__dict__[ii]

def MethodInClass(class_name):
    '''
    Get Method list in Class
    '''
    ret=dir(class_name)
    if hasattr(class_name,'__bases__'):
        for base in class_name.__bases__:
            ret=ret+MethodInClass(base)
    return ret

def ObjInfo(obj):
    '''
    Get object information : type, name, method list, path, module_name, module_version, module
    '''
    rt={}
    rt['type']=type(obj).__name__
    rt['name']=obj.__name__
    rt['methods']=MethodInClass(obj)
    if rt['type'] in ['module']:
        rt['path']=obj.__path__
        rt['version']=ModVersion(rt['name'])
        rt['module_name']=obj.__name__
        rt['module']=obj
    elif rt['type'] in ['function']:
        rt['path']=os.path.abspath(inspect.getfile(obj))
        rt['module']=inspect.getmodule(obj)
        rt['module_name']=rt['module'].__name__
        rt['module_version']=ModVersion(rt['module_name'])
#        rt['methods']=[rt['module_name']]
    elif rt['type'] in ['class']:
        rt['module_name']=obj.__module__
        rt['path']=os.path.abspath(sys.modules[rt['module_name']].__file__)
        rt['module']=sys.modules[rt['module_name']]
        rt['module_version']=ModVersion(rt['module_name'])
    return rt

def MyModule(default=False,parent=-1):
    '''
    Get current module 
    - parent
      -1 : my current python page's module
      0  : my function's module
      1  : my parent's module
    '''
    if parent >= 0:
        loc=1+parent
    else:
        loc=parent
    try:
        #frame=inspect.stack()[-1]
        frame=inspect.stack()
        if len(frame) <= loc:
            loc=-1
        return inspect.getmodule(frame[loc][0])
    except:
        return default

def CallerName(default=False,detail=False):
    '''
    Get the caller name of my group function
    detail=True: return (func name, line number, filename)
    default    : If not found caller name then return default

    def A():               #Group A()
        CallerName()       -> Called by module's A() => A
        B()
    def B():               #Group B()
        CallerName()       -> Called my group by A() function => A
        def C():
            CallerName()   -> Called my group by A() function => A
        C()
    A()                    -> Calling def A() in python script(module)
    '''
    try:
        dep=len(inspect.stack())-2
        name=sys._getframe(dep).f_code.co_name
        if name == '_bootstrap_inner' or name == '_run_code':
            dep=3
        if detail:
            return sys._getframe(dep).f_code.co_name,sys._getframe(dep).f_lineno,sys._getframe(dep).f_code.co_filename
        return sys._getframe(dep).f_code.co_name
    except:
        return default

def Frame2Function(obj,default=False):
    '''
    Get Function Object from frame or frame info
    '''
    obj_type=TypeName(obj)
    if obj_type == 'function': return obj
    if obj_type == 'frameinfo':
        return gc.get_referrers(obj.frame.f_code)[0]
    elif obj_type == 'frame':
        return gc.get_referrers(obj.f_code)[0]
    return default

def FunctionName(parent=0,default=False,history=0,tree=False,args=False,line_number=False,filename=False,obj=False,show=False):
    '''
    Get function name
     - parent
       0            : my name (default)
       1            : my parent function
       ...          : going top parent function
     - history      : Getting history (return list)
     - tree         : tree  (return list)
       - show       : show tree on screen
     - args         : show arguments
     - line_number  : show line number
     - filename     : show filename
     - obj          : Get OBJ (return list)
    '''
    if parent >= 0:
        loc=1+parent
    else:
        loc=parent
    try:
        my_history=inspect.stack()
    except:
        return default
    if history:
        rt=[]
        space=''
        for i in range(len(my_history)-1,0,-1):
            if tree:
                if space:
                    pp='{} -> {}'.format(space,my_history[i].function)
                else:
                    pp=my_history[i].function
                if pp == '<module>':
                    if show:
                        print(pp)
                    else:
                        rt.append(pp)
                else:
                    if args:
                        arg=FunctionArgs(Frame2Function(my_history[i].frame),mode='string',default='')
                        if arg: pp=pp+'{}'.format(arg)
                        else: pp=pp+'()'
                    if line_number: pp=pp+' at {}'.format(my_history[i].lineno)
                    if filename: pp=pp+' in {}'.format(my_history[i].filename)
                    if show:
                        print(pp)
                    else:
                        rt.append(pp)
                space=space+'  '
            else:
                if obj:
                    rt.append((my_history[i].function,Frame2Function(my_history[i].frame),my_history[i].lineno,my_history[i].filename))
                else:
                    rt.append((my_history[i].function,my_history[i].lineno,my_history[i].filename))
        return rt
    else: # single function
        if len(my_history) <= loc: #out of range
            loc=-1
        if obj:
            # return name and object
            return (my_history[loc].function,Frame2Function(my_history[loc].frame))
        else:
            rt=my_history[loc].function
            if args:
                arg=FunctionArgs(Frame2Function(my_history[loc].frame),mode='string',default='')
                if arg: rt=rt+'{}'.format(arg)
                else: rt=rt+'()'
            if line_number: rt=rt+' at {}'.format(my_history[loc].lineno)
            if filename: rt=rt+' in {}'.format(my_history[loc].filename)
            return rt

def FunctionList(obj=None):
    '''
    Get function list in this object
    '''
    aa={}
    if isinstance(obj,str):
       obj=sys.modules.get(obj)
    elif IsNone(obj):
       obj=MyModule(default=None)
    if Type(obj,('classobj','module','instance')):
        if Type(obj,'instance'): obj=obj.__class__ # move CLASS() to CLASS
        for name,fobj in inspect.getmembers(obj):
            if inspect.isfunction(fobj):
                aa.update({name:fobj})
    return aa

def GetClass(obj,default=None):
    '''
    Get Class object from instance,method,function
    '''
    obj_type=TypeName(obj)
    if obj_type in ['instance']:
        obj=obj.__class__ # Convert instance to classobj
        obj_type=TypeName(obj)
    if obj_type in ['classobj']: return obj
    if obj_type in ['method']:
        obj_name = obj.__name__
        if obj.__self__:
            classes = [obj.__self__.__class__]
        else:
            #unbound method
            classes = [obj.im_class]
        while classes:
            c = classes.pop()
            if obj_name in c.__dict__:
                return c
            else:
                classes = list(c.__bases__) + classes
    elif obj_type in ['function']:
        if PyVer(3):
            #caller_module_name=inspect.currentframe().f_back.f_globals['__name__']
            #caller_module=sys.modules[caller_module_name]
            caller_module=inspect.getmodule(inspect.currentframe().f_back)
            return getattr(caller_module_name,'.'.join(obj.__qualname__.split('.')[:-1]))
    return default

def FunctionArgs(func,**opts):
    '''
    Get function's input Arguments
    - mode
      - defaults : get default (V=?,...)
      - args     : get args  (V,V2,...)
      - varargs  : get varargs (*V)
      - keywords : get keywords (**V)
      - string   : return arguments to string format
      - list,tuple: return arguments to list format
      default output : dictioniary format
    - default : if nothing then return default value (default None)
    '''
    mode=opts.get('mode',opts.get('field','defaults'))
    default=opts.get('default',None)
    if not Type(func,'function'):
        return default
    rt={}
    #Not support *v parameter with getargspec()
    #args, varargs, keywords, defaults = inspect.getargspec(func)
    #if not IsNone(defaults):
    #    defaults=dict(zip(args[-len(defaults):], defaults))
    #    del args[-len(defaults):]
    #    rt['defaults']=defaults
    # inspect.getcallargs(<function>,datas....) : automatically matching and put to <functions>'s inputs : Check it later
    arg = inspect.getfullargspec(func)
    args=arg.args
    varargs=arg.varargs
    keywords=arg.varkw
    defaults=arg.kwonlydefaults
    if not IsNone(arg.defaults):
        if defaults is None:
            defaults=dict(zip(args[-len(arg.defaults):],arg.defaults))
        else:
            defaults.update(dict(zip(args[-len(arg.defaults):],arg.defaults)))
        del args[-len(arg.defaults):]

    if not IsNone(defaults): rt['defaults']=defaults
    if args: rt['args']=args
    if varargs: rt['varargs']=varargs
    if keywords: rt['keywords']=keywords
    if Type(mode,(list,tuple)):
        rts=[]
        for ii in rt:
            rts.append(rt.get(ii,default))
        return rts
    else:
        if mode in ['str','string','format']:
            return str(inspect.signature(func))
            #arg_str=''
            #if rt:
            #    for z in rt.get('args',[]):
            #         if arg_str:
            #             arg_str=arg_str+',{}'.format(z)
            #         else:
            #             arg_str='{}'.format(z)
            #    if 'varargs' in rt:
            #         if arg_str:
            #             arg_str=arg_str+',*{}'.format(rt['varargs'])
            #         else:
            #             arg_str='*{}'.format(rt['varargs'])
            #    if 'defaults' in rt:
            #        for z in rt['defaults']:
            #             if arg_str:
            #                 arg_str=arg_str+',{}='.format(z)
            #             else:
            #                 arg_str='{}='.format(z)
            #             if Type(rt['defaults'][z],str):
            #                 arg_str=arg_str+"'{}'".format(rt['defaults'][z])
            #             else:
            #                 arg_str=arg_str+"{}".format(rt['defaults'][z])
            #    if 'keywords' in rt:
            #        if arg_str:
            #             arg_str=arg_str+',**{}'.format(rt['keywords'])
            #        else:
            #             arg_str='**{}'.format(rt['keywords'])
            #return arg_str
        if mode in rt:
            return rt[mode]
        return rt

def Args(src,field='all',default={}):
    '''
    Get Class, instance's global arguments
    Get Function input parameters
    '''
    rt={}
    if Type(src,('classobj,instance')):
        try:
            src=getattr(src,'__init__')
        except:
            return src.__dict__
    elif not Type(src,'function'):
        return default
    return FunctionArgs(src,mode=field,default=default)

def Variable(src=None,obj=None,parent=0,history=False,default=False,mode='local',VarType=None,alltype=True):
    '''
    Get available variable data
     - src: 
       if None: return whole environment (dict)
       if string then find the string variable in the environment
       if variable then return that
     - parent 
       0 : my function (default)
       1 : my parents function
       ...
     - history: from me to my top of the functions
     - mode  : variable area
       local : function's local(inside) variable
       global: function's global variable
    '''
    src_type=TypeName(src)
    obj_type=TypeName(obj)
    parent=Int(parent)
    if not isinstance(parent,int): parent=0
    if parent >= 0:
        loc=1+parent
    else:
        loc=parent
    inspst=inspect.stack()
    #inspect.stack()[depth][0] : frame 
    #inspect.getmembers(frame) : environments
    if len(inspst) <= loc: #out of range
        loc=-1
    rt={}
    if obj_type in ['module','classobj','instance']:
        rt.update(obj.__dict__)
    else: # global and locals variables from me to top
        if history:
            for i in range(len(inspst)-1,0,-1):
                if mode in ['global','all']:
                    rt.update(dict(inspect.getmembers(inspst[i][0]))["f_globals"])
                if mode in ['local','all']:
                    rt.update(dict(inspect.getmembers(inspst[i][0]))["f_locals"])
        else:
            if mode in ['global','all']:
                rt.update(dict(inspect.getmembers(inspst[loc][0]))["f_globals"])
            if mode in ['local','all']:
                rt.update(dict(inspect.getmembers(inspst[loc][0]))["f_locals"])
    if src_type=='nonetype':
        if alltype:
            return rt
        o={}
        for i in rt:
            if i in ('__builtins__','__cached__','modules','mod_path') or TypeName(rt[i]) in ('function','module','classobj','instance','builtin_function_or_method','method'): 
                continue
            o[i]=rt[i]
        return o
    elif src_type == 'str':
        out=rt.get(src,default)
        if VarType: # if put expected type then
            if Type(out,VarType): return out # if getting data is expected type then 
            return default # if not expected then return default
        return out # just return gotten data
        #if obj_type in ['module']:
        #    # getattr(<class>,'name') : Get data
        #    # hasattr(<class>,'name') : check name
        #    # setattr(<class>,'name') : update to name
        #    # delattr(<class>,'name') : remove name
        #    if hasattr(obj,src): return getattr(obj,src)
        #elif obj_type in ['class']:
        #    obj=obj()
        #    if hasattr(obj,src): return getattr(obj,src)
        #else: #No object
        #    out=rt.get(src,default)
        #    if VarType: # if put expected type then
        #        if Type(out,VarType): return out # if getting data is expected type then 
        #        return default # if not expected then return default
        #    return out # just return gotten data
    return default

def Uniq(src,default='org',sort=False,strip=False,cstrip=False):
    '''
    make to uniq data
    default='org': return original data
    sort=False   : sort data
    strip=False  : remove white space and make to uniq
    cstrip=False : check without white space, but remain first similar data
    '''
    if isinstance(src,(list,tuple)):
        rt=[]
        if cstrip:
            nsrc=[i.strip() if isinstance(i,(str,bytes)) else i for i in src]
            c=[]
            for i,d in enumerate(nsrc):
                if d not in c:
                    c.append(d)
                    rt.append(src[i])
        else:
            if strip:
                src=[i.strip() if isinstance(i,(str,bytes)) else i for i in src]
            for i in src:
                if i not in rt: rt.append(i)
        if sort: rt=Sort(rt)
        return tuple(rt) if isinstance(src,tuple) else rt
    return Default(src,default)

def Split(src,sym,default=None,sym_spliter='|'):
    '''
    multipul split then 'a|b|...'
    without "|" then same as string split function
    '''
    #SYMBOL Split
    if len(sym) > 1:
        if Type(sym,(str,bytes)) and sym_spliter:
            if Type(sym,bytes): sym_spliter=Bytes(sym_spliter)
            else: sym_spliter=Str(sym_spliter)
            sym=Uniq(sym.split(sym_spliter))
        try:
            msym='|'.join(map(re.escape,tuple(sym)))
            if Type(src,'bytes'): msym=Bytes(msym)
            else: msym=Str(msym)
            return re.split(msym,src) # splited by '|' or expression
        except:
            pass
    else:
        # Normal split
        try:
            if Type(src,'bytes'): sym=Bytes(sym)
            else : sym=Str(sym)
            return src.split(sym)
        except:
            pass
    if default in ['org',{'org'}]:
        return src
    return default

def FormData(src,default=None,want_type=None):
    '''
    convert string data to format
    '1' => 1
    json string to json format
    "{'a':1}" => {'a':1}
    "[1,2,3]" => [1,2,3]
    ....
    '''
    form_src=None
    if isinstance(src,str):
        if Type(want_type,'str'): return src
        try:
            form_src=ast.literal_eval(src)
        except:
            try:
                form_src=json.loads(src)
            except:
                try:
                    form_src=eval(src)
                except:
                    return Default(src,default)
    else:
        form_src=src
    if IsNone(want_type):
        return form_src
    else:
        if Type(form_src,want_type): return form_src
        return Default(src,default)

def IndexForm(idx,idx_only=False,symbol=None):
    '''
    return : <True/False>, Index Data
     - False: not found Index form from input idx 
     - True : found Index
    Index Data
     - tuple(A,B) : Range Index (A~B)
     - list [A,B] : OR Index or keys A or B
     - Single     : int: Index, others: key
    - idx_only    : only return integer index
    - symbol   : default None, if idx is string and want split with symbol
    '''
    if IsNone(idx):
        return False,None
    elif isinstance(idx,str):
        for s in [':','-','~']: # Range Index
            if s in idx:
                idx_a=idx.split(s)
                if len(idx_a) == 2:
                    if IsInt(idx_a[0]) and IsInt(idx_a[1]):
                        return True,(Int(idx_a[0]),Int(idx_a[1]))
                return False,None
        if '|' in idx: # OR Index
            idx_a=idx.split('|')
            if idx_only:
                rt=[]
                for i in idx_a:
                    if IsInt(i): rt.append(Int(i))
                return True,rt
            return True,idx.split('|')
        elif '/' in idx: # Path index
            idx_a=idx.split('/')
            if idx_a[0] == '':
                return None,idx_a[1:]
            return None,idx_a
        else:
            if idx_only:
                if symbol:
                    idxs=idx.split(symbol)
                    rt=[]
                    for i in idxs:
                        if IsInt(i): rt.append(Int(i))
                    if rt: return True,rt
                    return False,None
                if IsInt(idx):
                    return True,Int(idx)
                return False,None
    elif isinstance(idx,list):
        return True,idx
    elif isinstance(idx,tuple) and len(idx) == 2:
        return True,idx
    return True,idx # Return original

def Get(*inps,**opts):
    '''
    Get (Any) something
    Get('whoami')  : return my function name
    Get('funclist'): return my module's function list
     - parent=1    : my parent's function list
    Get(<list|string|dict|int|...>,<index|key|keypath>): Get data at the <index|key|keypath>
     - keypath : '/a/b/c' => {'a':{'b':{'c':1,'d'}}} => return c's 1
     - key     :
       Range Format from 1 to 5: tuple format (1,5), String format '1-5' or '1:5' or '1~5'
       OR data 1,3,5           : list format  [1,3,5], String format '1|3|5'
         - if found any data then getting that data only
         - if use fill_up option then if error of a key then fill to <fill_up> value at the error location.
     - index   : integer       : single data
    Get('_this_',<key>): my functions's <key>
    Get('<var name>')  : return variable data
    Get('_this_','args')  : return my functions Arguments
    Get(<function>,'args')  : return the functions Arguments
    <option>
      fill_up : If error of the key's value then fill up <fill_up> to right position when the <key> is list
      default : None, any issue
      err     : False, if any error then ignore the data
      idx_only: if input data is dictionary then convert dictionary's keys to input data. So, int idx can get keys(list) name
      _type_  : define to input data's data format (ex: (list,tuple))
      method  : if input is request then can define method('GET','POST',...)
      strip   : default: False, it can strip white space
      peel    : 
          force: just take first data in the list,tuple (if data format has any form also OK, just return the data)
          True : single data(list,tuple,dict) then peel to data (if data format is list,tuple,dict... then return default)
          False: return founded data (any format)
      out     : define to output data (list-> output will list, ...), if wrong format then return default
    '''
    default=opts.get('default')
    err=opts.get('err',opts.get('error',False))
    fill_up=opts.get('fill_up','_fAlsE_')
    idx_only=opts.get('idx_only',opts.get('index_only',False))
    _type=opts.get('_type_',opts.get('type'))
    out=opts.get('out',opts.get('out_form','raw'))
    peel=opts.get('peel')
    strip=opts.get('strip',False)

    if len(inps) == 0:
        return Default(inps,default)
    if len(inps) == 1:
        if inps[0] in ['whoami','myname','funcname','functionname','FunctionName']:
            return FunctionName(parent=opts.get('parent',1)) # my parent's function name
        elif isinstance(inps[0],str):
            if inps[0].lower() in ['func','function','functions','funclist','func_list','list']:
                return FunctionList(parent=opts.get('parent',-1)) # default: my page's function list
            return Variable(inps[0],parent=opts.get('parent',1)) # my parent's variable
    inps=list(inps)
    obj=inps[0]
    if IsNone(obj):
        return Default(obj,default)
    del inps[0]
    if len(inps) == 1:
        idx=inps[0]
    elif len(inps) > 1:
        idx=inps[:]
    else:
        idx=None
    #When check type
    if _type is not None:
        if not Type(obj,_type):
            return Default(obj,default)
    ok,nidx=IndexForm(idx,idx_only=idx_only)
    idx_type=type(nidx).__name__
    if obj == '_this_':
        obj_type='function'
    else:
        obj_type=TypeName(obj)
    def _max_(obj,idx,err=True):
        obj_len=len(obj)
        if obj_len == 0: return None
        if type(idx).__name__ != 'int':
            if err is True: return False
            return obj_len-1
        if idx >= 0:
            if obj_len <= idx:
                if err is True: return False
                return obj_len-1
            else:
                return idx
        else:
            if obj_len < abs(idx):
                if err is True: return False
                return 0
            return idx
        
    if ok and obj_type in ('list','tuple','str','bytes'):
        if idx_type == 'tuple':
            ss=_max_(obj,Int(nidx[0]),err)
            ee=_max_(obj,Int(nidx[1]),err)
            if Type(ss,int) and Type(ee,int):
                return obj[ss:ee+1]
        elif idx_type == 'list':
            rt=[]
            for i in nidx:
                #if not IsInt(i):
                #    if fill_up == '_fAlsE_':
                #        continue
                #    else:
                #        rt.append(fill_up)
                ix=_max_(obj,Int(i,default=False,err=True),err)
                if Type(ix,int):
                    rt.append(obj[ix])
                elif fill_up != '_fAlsE_':
                    rt.append(fill_up)
            return OutFormat(rt,out=out,default=default,org=obj,peel=peel,strip=strip)
        elif idx_type == 'int':
            ix=_max_(obj,nidx,err)
            if Type(ix,int): return obj[ix]
        return Default(obj,default)
    elif obj_type in ('dict'):
        if ok is True:
            obj_items=list(obj.items())
            if idx_type == 'tuple': #Range Index
                ss=_max_(obj_items,Int(nidx[0]),err)
                ee=_max_(obj_items,Int(nidx[1]),err)
                if Type(ss,int) and Type(ee,int):
                    return dict(obj_items[ss:ee+1])
            elif idx_type == 'list': #OR Index
                rt=[]
                for i in nidx:
                    if idx_only:
                        ix=_max_(obj_items,Int(i,default=False,err=True),err)
                        if Type(ix,int):
                            rt.append(obj_items[ix])
                        elif fill_up != '_fAlsE_':
                            rt.append(fill_up)
                    else:
                        t=obj.get(i)
                        if t is not None: rt.append(t)
                return OutFormat(rt,out=out,default=default,org=obj,peel=peel,strip=strip)
            else:
                if idx_only:
                    ix=_max_(obj_items,Int(idx),err)
                    if Type(ix,int): return obj_items[ix]
                return obj.get(idx,Default(obj,default))
        elif ok is None: #Path Index
            for i in nidx:
                if i not in obj: return Default(obj,default)
                obj=obj[i]
            return obj
        return Default(obj,default)
    elif obj_type in ('function'): #???
        if ok:
            if idx_type == 'str':
                if nidx.lower() in ['args','arguments']:
                    if obj == '_this_':
                        obj=inspect.getmembers(MyModule()).get(CallerName())
                    return FunctionArgs(obj)
                else:
                    if obj == '_this_':
                        return Variable(nidx,parent=1)
                    return Varable(nidx,obj)
            elif idx_type == 'list':
                rt=[]
                for i in nidx:
                    if Type(i,str) and i.lower() in ['args','arguments']:
                        if obj == '_this_':
                            obj2=inspect.getmembers(MyModule()).get(CallerName())
                            rt.append(FunctionArgs(obj2))
                        else:
                            rt.append(FunctionArgs(obj))
                    else:
                        if obj == '_this_':
                            rt.append(Variable(nidx,parent=1))
                        else:
                            rt.append(Variable(nidx,obj))
                return OutFormat(rt,out=out,default=default,org=obj,peel=peel,strip=strip)
    elif obj_type in ('instance','classobj','module'):
        if Type(idx,str) and idx.lower() in ['func','function','functions','funclist','func_list','list']:
            return FunctionList(obj)
        elif idx_type in ['list','tuple']: #OR Index
            rt=[]
            # get function object of finding string name in the class/instance
            for ff in nidx:
                if isinstance(ff,str):
                    if ff in ['__name__','method_name','__method__']: #Get Method name list in class
                        if obj_type in ('classobj'): obj=obj() # move from CLASS to CLASS()
                        if Type(obj,'instance'):
                            rt=rt+MethodInClass(obj)
                    else:
                        rt.append(getattr(obj,ff,default))
            return OutFormat(rt,out=out,default=default,org=obj,peel=peel,strip=strip)
        elif idx_type == 'str':
            if obj_type == 'classobj': obj=obj() # move CLASS to CLASS()
            return getattr(obj,nidx,Default(obj,default))
        else:
            if Type(obj,'classobj'): obj=obj() # move from CLASS to CLASS()
            if ok is False:
                return obj.__dict__
            else:
                return Get(obj.__dict__,idx,default,err) # converted obj with original idx
    elif obj_type in ('response'): # Web Data
        if ok:
            def _web_(obj,nidx):
                if nidx in ['rc','status','code','state','status_code']:
                    return obj.status_code
                elif nidx in ['data','value','json']:
                    try:
                        return FormData(obj.text)
                    except:
                        if err is True: return Default(obj,default)
                        return obj.text
                elif nidx in ['text','str','string']:
                    return obj.text
                else:
                    return obj
            if idx_type=='str':
                return _web_(obj,nidx)
            elif idx_type == 'list':
                rt=[]
                for ikey in nidx:
                    rt.append(_web_(obj,ikey))
                return OutFormat(rt,out=out,default=default,org=obj,peel=peel,strip=strip)
    elif obj_type in ('request'): # Web Data2
        rt=[]
        method=opts.get('method',None)
        if IsNone(method): method=obj.method.upper()
        elif isinstance(method,str): method=method.upper()

        if ok:
            def _web_data(obj,nkey,method,default):
                if nkey.lower() == 'method':
                    return method
                if method=='GET':
                    rt=obj.GET.get(nkey)
                    if not IsNone(rt): return rt
                    return Default(obj,default)
                elif method=='FILE':
                    rt=obj.FILES.getlist(nkey,default)
                    if not IsNone(rt):
                        return OutFormat(rt,out='raw',peel=peel,strip=strip,default=default)
                    #if not IsNone(rt): return rt
                    #rt=obj.FILES.get(nkey,default)
                    #if not IsNone(rt): return rt
                    return Default(obj,default)
                elif method=='POST':
                    rt=obj.FILES.getlist(nkey)
                    #rt2=obj.FILES.get(nkey)
                    if not IsNone(rt):
                        return OutFormat(rt,out='raw',peel=peel,strip=strip,default=default)
                    rt=obj.POST.getlist(nkey)
                    #rt=obj.POST.get(nkey)
                    if not IsNone(rt):
                        return OutFormat(rt,out='raw',peel=peel,strip=strip,default=default)
                    return Default(obj,default)
            if idx_type == 'str':
                return _web_data(obj,nidx,method,default)
            elif idx_type == 'list':
                rt=[]
                for i in nidx:
                    rt.append(_web_data(obj,i,method,default))
                return OutFormat(rt,out=out,default=default,org=obj,peel=peel,strip=strip)
    elif obj_type in ('ImmutableMultiDict'): # Flask Web Data
        tmp={}
        if obj:
            for ii in obj:
                tmp[ii]=obj[ii]
        return Get(tmp,idx,default,err) 
    elif obj_type in ('kDict','kList','DICT'): 
        return Get(obj.Get(),idx,default,err) 
    return OutFormat([],out=out,default=default,org=obj,peel=peel,strip=strip)


def TryCode(code,default=False,_return_=True):
    '''
    Run string code
    default :False
    _return_: True: return output, False: print on screen
    '''
    if Type(code,str):
        err=None
        if _return_:
            # create file-like string to capture output
            codeOut = StringIO()
            codeErr = StringIO()
            sys.stdout.flush()
            sys.stderr.flush()
            sys.stdout=codeOut # Standard Out from application
            sys.stderr=codeErr # Standard Error from application
        try:
            exec(code)
        except:
            #Code Error message
            err=ExceptMessage()
        finally:
            if _return_:
                sys.stdout.flush()
                sys.stderr.flush()
                #recover/restore stdout and stderr
                sys.stdout=sys.__stdout__
                sys.stderr=sys.__stderr__
                #Get value 
                rt=codeOut.getvalue()
                er=codeErr.getvalue()
                #Close IO
                codeOut.close()
                codeErr.close()
            if err: #Code Error
                if _return_:
                    return False,err
                else:
                    StdErr(err)
            if _return_:
                # Standard Out and Error
                return rt,er
    if _return_:
        return False,None  #Not a string code

def ExceptMessage(msg='',default=None):
    '''
    Try:
       AAA
    Except:
       err=ExceptMessage() => If excepting then taken error or traceback code and return it
    '''
    e=sys.exc_info()[0]
    er=traceback.format_exc()
    if e or er != 'NoneType: None\n':
        if msg:
            msg='{}\n\n{}\n\n{}'.format(msg,e,er)
        else:
            msg='\n\n{}\n\n{}'.format(e,er)
        return msg
    return default

def IpV4(ip,out='str',default=False,port=None,bmc=False,used=False,pool=None):
    '''
    check/convert IP
    ip : int, str, ...
    out:
      str : default : convert to xxx.xxx.xxx.xxx format
      int : convert to int format
      hex : convert to hex format
    port: if you want check the IP with port then type
    bmc : default False, True: check BMC port (623,664,443)
    return : IP, if fail then return default value
    used:
      * required port option, but check with single port
      False: default (not check)
      True: Check IP already used the port(return True) or still available(return False)
    pool: if give IP Pool(tuple) then check the IP is in the POOL or not.
    '''
    def IsOpenPort(ip,port):
        '''
        It connectionable port(?) like as ssh, ftp, telnet, web, ...
        '''
        tcp_sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_sk.settimeout(1)
        rt=[]
        for pt in port:
            try:
                tcp_sk.connect((ip,pt))
                tcp_sk.close()
                rt.append(pt)
            except:
                pass
        return rt
    def IsUsedPort(ip,port):
        '''
        The IP already used the port, it just checkup available port or alread used
        '''
        if IsNone(ip,chk_val=[None,'','localhost','local']):
            ip='127.0.0.1'
        soc=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rt=[]
        for pt in port:
            try:
                location=(ip,pt)
                rt=soc.connect_ex(location)
                soc.close()
                #rt==0 then already used
                if rt == 0: rt.append(pt)
            except:
                pass
        return rt
    if bmc: # Update BMC Port
        default_bmc_port=[623,664,443]
        if not IsNone(port):
            port=Int(port,default=False)
            if isinstance(port,(list,tuple)):
                for i in port:
                    if i not in default_bmc_port: default_bmc_port.append(i)
            elif isinstance(port,int):
                if port not in default_bmc_port:
                    default_bmc_port.append(port)
        port=tuple(default_bmc_port)
    if port:
        port=Int(port,default=False)
        if port is False: return default
        if Type(port,int): port=[port]
    ip_int=None
    if isinstance(ip,str):
        ipstr=ip.strip()
        if '0x' in ipstr:
            ip_int=int(ipstr,16)
        elif ipstr.isdigit():
            ip_int=int(ipstr)
        elif '.' in ipstr:
            try:
                ip_int=struct.unpack("!I", socket.inet_aton(ipstr))[0] # convert Int IP
                #struct.unpack("!L", socket.inet_aton(ip))[0]
            except:
                return default
    elif isinstance(ip,int):
        try:
            socket.inet_ntoa(struct.pack("!I", ip)) # check int is IP or not
            ip_int=ip
        except:
            return default
    elif isinstance(ip,type(hex)):
        ip_int=int(ip,16)

    if not IsNone(ip_int):
        try:
            if out in ['int',int]:
                return ip_int
            elif out in ['hex',hex]:
                return hex(ip_int)
            elif isinstance(pool,(list,tuple)) and len(pool) == 2:
                return IpV4(pool[0],out=int) <= ip_int <= IpV4(pool[1],out=int)
            else: #default to str
                ip_str=socket.inet_ntoa(struct.pack("!I", ip_int))
                if port: # If bing Port then check the port
                    if used:
                        rt=IsUsedPort(ip_str,port)
                        if rt: return rt
                    else:
                        rt=IsOpenPort(ip_str,port)
                        if rt: return rt
                else:
                    return ip_str
        except:
            pass
    return default

def ping(host,**opts):
    '''
    same as ping command
    '''
    count=opts.get('count',0)
    interval=opts.get('interval',1)
    keep_good=opts.get('keep_good',0)
    timeout=opts.get('timeout',opts.get('timeout_sec',0))
    lost_mon=opts.get('lost_mon',False)
    log=opts.get('log',None)
    stop_func=opts.get('stop_func',None)
    log_format=opts.get('log_format','.')
    alive_port=opts.get('alive_port')
    cancel_func=opts.get('cancel_func',None)

    ICMP_ECHO_REQUEST = 8 # Seems to be the same on Solaris. From /usr/include/linux/icmp.h;
    ICMP_CODE = socket.getprotobyname('icmp')
    ERROR_DESCR = {
        1: ' - Note that ICMP messages can only be '
           'sent from processes running as root.',
        10013: ' - Note that ICMP messages can only be sent by'
               ' users or processes with administrator rights.'
        }

    def checksum(msg):
        sum = 0
        size = (len(msg) // 2) * 2
        for c in range(0,size, 2):
            sum = (sum + ord(msg[c + 1])*256+ord(msg[c])) & 0xffffffff
        if size < len(msg):
            sum = (sum+ord(msg[len(msg) - 1])) & 0xffffffff
        ra = ~((sum >> 16) + (sum & 0xffff) + (sum >> 16)) & 0xffff
        ra = ra >> 8 | (ra << 8 & 0xff00)
        return ra

    def mk_packet(size):
        """Make a new echo request packet according to size"""
        # Header is type (8), code (8), checksum (16), id (16), sequence (16)
        header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, 0, size, 1)
        #data = struct.calcsize('bbHHh') * 'Q'
        data = size * 'Q'
        my_checksum = checksum(Str(header) + data)
        header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0,
                             socket.htons(my_checksum), size, 1)
        return header + Bytes(data)

    def receive(my_socket, ssize, stime, timeout):
        while True:
            if timeout <= 0:
                return
            ready = select.select([my_socket], [], [], timeout)
            if ready[0] == []: # Timeout
                return
            received_time = time.time()
            packet, addr = my_socket.recvfrom(1024)
            type, code, checksum, gsize, seq = struct.unpack('bbHHh', packet[20:28]) # Get Header
            if gsize == ssize:
                return received_time - stime
            timeout -= received_time - stime

    def pinging(ip,timeout=1,size=64):
        try:
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP_CODE)
        except socket.error as e:
            if e.errno in ERROR_DESCR:
                raise socket.error(''.join((e.args[1], ERROR_DESCR[e.errno])))
                #raise socket.error(Join((e.args[1], ERROR_DESCR[e.errno]),symbol=''))
            raise
        if size in ['rnd','random']:
            # Maximum size for an unsigned short int c object(65535)
            size = int((id(timeout) * random.random()) % 65535)
        packet = mk_packet(size)
        while packet:
            sent = my_socket.sendto(packet, (ip, 1)) # ICMP have no port, So just put dummy port 1
            packet = packet[sent:]
        delay = receive(my_socket, size, TIME().Time(), timeout)
        my_socket.close()
        if delay:
            return delay,size

    def do_ping(ip,timeout=1,size=64,count=None,interval=0.7,log_format='ping',cancel_func=False):
        ok=1
        i=1
        ping_cmd=find_executable('ping')
        while True:
            if IsCancel(cancel_func):
                return -1,'canceled'
            if ping_cmd:
                ping_s=size-8 if size >= 8 else 0
                rc=rshell("ping -s {} -c 1 {}".format(ping_s,host))
                delay=[]
                if rc[0] == 0:
                    delay=[]
                    tt=rc[1].split('\n')[1].split()
                    delay=[float(tt[6].split('=')[1])/1000,tt[0]]
            else:
               delay=pinging(ip,timeout,size)
            if delay:
                ok=0
                if log_format == '.':
                    StdOut('.')
                elif log_format == 'ping':
                    StdOut('{} bytes from {}: icmp_seq={} ttl={} time={} ms\n'.format(delay[1],ip,i,size,round(delay[0]*1000.0,4)))
            else:
                ok=1
                if log_format == '.':
                    StdOut('x')
                elif log_format == 'ping':
                    StdOut('{} icmp_seq={} timeout ({} second)\n'.format(ip,i,timeout))
            if count:
                count-=1
                if count < 1:
                    return ok,'{} is alive'.format(ip)
            i+=1
            time.sleep(interval)

    if log_format=='ping':
        if not count: count=1
        do_ping(host,timeout=timeout,size=64,count=count,log_format='ping',cancel_func=cancel_func)
    else:
        if alive_port:
            return True if IpV4(host,port=alive_port) else False
        Time=TIME()
        init_sec=0
        infinit=False
        if not count and not timeout:
            count=1
            infinit=True
        if not infinit and not count:
            init_sec=Time.Init()
            if keep_good and keep_good > timeout:
                timeout=keep_good + timeout
            count=timeout
            ocount=timeout
        chk_sec=Time.Init()
        log_type=type(log).__name__
        found_lost=False
        good=False
        while count > 0:
           if IsCancel(cancel_func) or IsCancel(stop_func):
               log(' - Canceled/Stopped ping')
               return False
           rc=do_ping(host,timeout=1,size=64,count=1,log_format=None)
           if rc[0] == 0:
              good=True
              if keep_good:
                  if good and keep_good and TIME().Now(int) - chk_sec >= keep_good:
                      return True
              else:
                  return True
              if log_type == 'function':
                  log('.',direct=True,log_level=1)
              else:
                  StdOut('.')
           else:
              good=False
              chk_sec=TIME().Now(int)
              if log_type == 'function':
                  log('x',direct=True,log_level=1)
              elif log_format == '.':
                  StdOut('x')
           if init_sec:
               count=ocount-(TIME().Now(int)-init_sec)
           elif not infinit:
               count-=1
           TIME().Sleep(interval)
        return good

class WEB:
    '''
    GetIP: get server or client IP
    Request: request()
    str2url: convert string to URL format
    form2dict: convert form data to dictionary format
    '''
    def __init__(self,request=None):
        Import('import requests')
        if request:
            self.requests=request
        else:
            self.requests=requests

    def Session(self):
        return self.requests.session._get_or_create_session_key()

    def GetIP(self,mode='server'):
        ''' 
        mode:
          server : get server IP (default)
          client : get client IP
        '''
        if mode == 'server':
            return self.requests.get_host().split(':')
        else:
            x_forwarded_for = self.requests.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                return x_forwarded_for.split(',')[0]
            else:
                return self.requests.META.get('REMOTE_ADDR')

    def Method(self,method_name=None,mode='lower'):
        method_n=self.requests.method
        if method_name:
            return method_name.lower() == method_n.lower()
        else:
            if mode == 'upper':
                return method_n.upper()
            else:
                return method_n.lower()

    def Request(self,host_url,**opts):
        '''
        user & password: string format
        auth: tuple format
        data: dictionary format
        json: dictionary / JSON format
        files: dictionary format
           ex) files = { '<file parameter name>': (<filename>, open(<filename>,'rb'))}
        headers: string or dictionary format
           - string example
             headers='json'
             required data or json 
           - dictionary example
             headers = { "Content-Type": "application/json"}
        dbg : True: show debuging log(default), False ignore debugging log
        ping: True: Check dest IP with ping, False: not check dest IP (default)
        max_try: default 3, retry max number when failed
        mode: default get, (get,post,patch)
        ip: dest IP
        port: default 80 or 443, arrcording to http or https, if you want special port then type
        bmc: default False, True then automaticall check BMC port
        timeout: request timeout (seconds), default None
        '''
        # remove SSL waring error message (test)
        self.requests.packages.urllib3.disable_warnings()

        ip=opts.get('ip',None)
        port=opts.get('port',None)
        bmc=opts.get('bmc',False)
        mode=opts.get('mode',opts.get('method','get'))
        max_try=opts.get('max_try',3) # Retry max number
        auth=opts.get('auth',None)
        user=opts.get('user',None)
        passwd=opts.get('passwd',None)
        data=opts.get('data',None) # dictionary format
        json_data=opts.get('json',None) # dictionary format
        files=opts.get('files',None) # dictionary format
        request_url=opts.get('request_url',None)
        dbg=opts.get('dbg',True)  # show debugging log
        ping=opts.get('ping',False) # check ping to IP
        timeout=opts.get('timeout',None) # request timeout
        req_data={}
        chk_dest=None
        if isinstance(timeout,int): req_data['timeout']=timeout
        if opts.get('https'): req_data['verify']=False
        if Type(auth,'tuple',data=True):
            req_data['auth']=opts.get('auth')
        elif Type(user,'str',data=True) and Type(passwd,'str',data=True):
            req_data['auth']=(user,passwd)
        if Type(data,'dict',data=True): req_data['data']=opts.get('data')
        if Type(json_data,'dict',data=True): req_data['json']=json_data
            
        if Type(files,'dict',data=True): req_data['files']=opts.get('files')
        headers=opts.get('headers') # dictionary format
        if Type(headers,'str',data=True):
            if headers == 'json':
                headers={ "Content-Type": "application/json"}
                if data:
                    data=json.dumps(data)
                    req_data['data']=data
                elif json_data:
                    data=json.dumps(json_data)
                    if 'json' in req_data: req_data.pop('json')
                    req_data['data']=data
        elif Type(headers,'dict',data=True):
            req_data['headers']=headers
        if not IsNone(ip):
            ip=IpV4(ip,out=str)
            chk_dest='{}'.format(ip)
            if req_data.get('verify',True):
                host_url='http://{}'.format(ip)
            else:
                host_url='https://{}'.format(ip)
            if not IsNone(port): host_url='{}:{}'.format(host_url,port)
            if not IsNone(request_url): host_url='{}/{}'.format(host_url,request_url)
        elif Type(host_url,'str',data=True) and host_url.startswith('http'):
            chk_dest=re.compile('(http|https)://([a-zA-Z0-9.]*)[:/]').findall(host_url)
            if len(chk_dest)==0:
                chk_dest=re.compile('(http|https)://([a-zA-Z0-9.]*)').findall(host_url)
            if len(chk_dest):
                chk_dest=chk_dest[0][1]
                if host_url.find('https://') == 0:
                    req_data['verify']=False
        if IsNone(chk_dest):
            return False,'host_url or ip not found'
        if bmc:
            if IpV4(chk_dest,bmc=True) is False:
                return False,'The IP({}) is not BMC IP'.format(chk_dest)
        if ping and chk_dest:
            if not ping(chk_dest,timeout_sec=3):
                return False,'Can not access to destination({})'.format(chk_dest)
        ss = self.requests.Session()
        for j in range(0,max_try):
            try:
                if IsSame(mode,'post'):
                    r =ss.post(host_url,**req_data)
                elif IsSame(mode,'patch'):
                    r =ss.patch(host_url,**req_data)
                else:
                    r =ss.get(host_url,**req_data)
                return True,r
            except:
                pass
            #except requests.exceptions.RequestException as e:
            if dbg: StdErr("Server({}) has no response (wait {}/{} (10s))".format(chk_dest,j,max_try))
            time.sleep(10)
        return False,'TimeOut'

    def str2url(self,string):
        if IsNone(string): return ''
        if isinstance(string,str):
            return string.replace('+','%2B').replace('?','%3F').replace('/','%2F').replace(':','%3A').replace('=','%3D').replace(' ','+')
        return string

    def form2dict(self,src=None):
        if IsNone(src): src=self.requests.form
        return Dict(src)

class TIME:
    def __init__(self,src=None):
        self.init_sec=int(datetime.now().strftime('%s'))
        self.src=src

    def Reset(self):
        self.init_sec=int(datetime.now().strftime('%s'))
    def Sleep(self,try_wait=None,default=1):
        if isinstance(try_wait,(int,str)): try_wait=(try_wait,)
        if isinstance(try_wait,(list,tuple)) and len(try_wait):
            if len(try_wait) == 2:
                try:
                    time.sleep(random.randint(int(try_wait[0]),int(try_wait[1])))
                except:
                    pass
            else:
                try:
                    time.sleep(int(try_wait[0]))
                except:
                    pass
        else:
            time.sleep(default)
    def Rand(self,try_wait=None,default=1):
        if isinstance(try_wait,(int,str)): try_wait=(try_wait,)
        if isinstance(try_wait,(list,tuple)) and len(try_wait):
            if len(try_wait) == 2:
                try:
                    return random.randint(int(try_wait[0]),int(try_wait[1]))
                except:
                    pass
            else:
                try:
                    return int(try_wait[0])
                except:
                    pass
        return default

    def Int(self):
        return int(datetime.now().strftime('%s'))

    def Now(self,mode=None):
        if mode in [int,'int','INT','sec']:return self.Int()
        return datetime.now()

    def Out(self,timeout_sec,default=(24*3600)):
        try:
            timeout_sec=int(timeout_sec)
        except:
            timeout_sec=default
        if timeout_sec == 0:
            return False
        if self.Int() - self.init_sec >  timeout_sec:
            return True
        return False
    def Format(self,tformat='%s',read_format='%S',time='_#_'):
        if IsNone(time,chk_val=['_#_'],chk_only=True): time=self.src
        if IsNone(time,chk_val=[None,'',0,'0']):
            return datetime.now().strftime(tformat)

        elif read_format == '%S':
            if isinstance(time,int) or (isinstance(time,str) and time.isdigit()):
                return datetime.fromtimestamp(int(time)).strftime(tformat)
        elif isinstance(time,str):
            return datetime.strptime(time,read_format).strftime(tformat)
        elif type(time).__name__ == 'datetime':
            return time.strftime(tformat)

    def Init(self):
        return self.init_sec

    def Time(self):
        return time.time()

    def Datetime(self):
        return datetime()

def rshell(cmd,timeout=None,ansi=True,path=None,progress=False,progress_pre_new_line=False,progress_post_new_line=False,log=None,progress_interval=5,cd=False,default_timeout=3600):
    def Pprog(stop,progress_pre_new_line=False,progress_post_new_line=False,log=None,progress_interval=5):
        time.sleep(progress_interval)
        if stop():
            return
        if progress_pre_new_line:
            if log:
                log('\n',direct=True,log_level=1)
            else:
                StdOut('\n')
        post_chk=False
        while True:
            if stop(): break
            if log:
                log('>',direct=True,log_level=1)
            else:
                StdOut('>')
            post_chk=True
            time.sleep(progress_interval)
        if post_chk and progress_post_new_line:
            if log:
                log('\n',direct=True,log_level=1)
            else:
                StdOut('\n')

    start_time=TIME()
    if not Type(cmd,'str',data=True):
        return -1,'wrong command information :{0}'.format(cmd),'',start_time.Init(),start_time.Init(),start_time.Now(int),cmd,path
    Popen=subprocess_Popen
    PIPE=subprocess_PIPE
    cmd_env=''
    cmd_a=cmd.split()
    cmd_file=cmd_a[0]
    if cmd_a[0] == 'sudo': cmd_file=cmd_a[1]
    if path and isinstance(path,str):
        if os.path.isfile(os.path.join(path,cmd_file)):
            if cd:
                cmd_env=cmd_env+'''cd %s && ./'''%(path)
            else:
                cmd_env=cmd_env+'''%s/'''%(path)
        else:
            cmd_env='''export PATH=%s:${PATH}; '''%(path)
    elif cmd_file[0] != '/' and cmd_file == os.path.basename(cmd_file) and os.path.isfile(cmd_file):
        cmd_env='./'
    p = Popen(cmd_env+cmd , shell=True, stdout=PIPE, stderr=PIPE)
    out=None
    err=None
    if progress:
        stop_threads=False
        ppth=Thread(target=Pprog,args=(lambda:stop_threads,progress_pre_new_line,progress_post_new_line,log,progress_interval))
        ppth.start()
    if timeout is not None:
        try:
            timeout=int(WhiteStrip(timeout))
        except:
            timeout=default_timeout
        if timeout < 3:
            timeout=3
    if PyVer(3):
        try:
            out, err = p.communicate(timeout=timeout)
        except subprocess_TimeoutExpired:
            p.kill()
            if progress:
                stop_threads=True
                ppth.join()
            return -2, 'Kill process after timeout ({0} sec)'.format(timeout), 'Error: Kill process after Timeout {0}'.format(timeout),start_time.Init(),start_time.Now(int),cmd,path
    else:
        if isinstance(timeout,int):
            countdown=int('{}'.format(timeout))
            while p.poll() is None and countdown > 0:
                time.sleep(2)
                countdown -= 2
            if countdown < 1:
                p.kill()
                if progress:
                    stop_threads=True
                    ppth.join()
                return -2, 'Kill process after timeout ({0} sec)'.format(timeout), 'Error: Kill process after Timeout {0}'.format(timeout),start_time.Init(),start_time.Now(int),cmd,path
        out, err = p.communicate()

    if progress:
        stop_threads=True
        ppth.join()
    if PyVer(3):
        out=out.decode("ISO-8859-1")
        err=err.decode("ISO-8859-1")
    if ansi:
        return p.returncode, out.rstrip(), err.rstrip(),start_time.Init(),start_time.Now(int),cmd,path
    else:
        return p.returncode, ansi_escape.sub('',out).rstrip(), ansi_escape.sub('',err).rstrip(),start_time.Init(),start_time.Now(int),cmd,path

def IsCancel(func):
    if Type(func,('function','instancemethod','method')):
        if func(): return True
    elif Type(func,('bool','str')) and func in [True,'cancel','revoke']:
        return True
    return False

def sprintf(string,*inps,**opts):
    '''
    """ipmitool -H %(ipmi_ip)s -U %(ipmi_user)s -P '%(ipmi_pass)s' """%(**opts)
    """{app} -H {ipmi_ip} -U {ipmi_user} -P '{ipmi_pass}' """.format(**opts)
    """{} -H {} -U {} -P '{}' """.format(*inps)
    """{0} -H {1} -U {2} -P '{3}' """.format(*inps)
    '''
    if not isinstance(string,str): return False,string
    ffall=[re.compile('\{(\d*)\}').findall(string),re.compile('\{(\w*)\}').findall(string),re.compile('\%\((\w*)\)s').findall(string),re.compile('\{\}').findall(string)]
    i=0
    for tmp in ffall:
        if i in [0,1]: tmp=[ j  for j in tmp if len(j) ]
        if tmp:
            if i == 0:
                mx=0
                for z in tmp:
                    if int(z) > mx: mx=int(z)
                if inps:
                    if len(inps) > mx: return string.format(*inps)
                elif opts:
                    if len(opts) > mx: return string.format(*opts.values())
                return False,"Need more input (tuple/list) parameters(require {})".format(mx)
            elif 0< i < 2:
                new_str=''
                string_a=string.split()
                oidx=0
                for ii in tmp:
                    idx=None
                    if '{%s}'%(ii) in string_a:
                        idx=string_a.index('{%s}'%(ii))
                    elif "'{%s}'"%(ii) in string_a:
                        idx=string_a.index("'{%s}'"%(ii))
                    if isinstance(idx,int):
                        if ii in opts:
                            string_a[idx]=string_a[idx].format(**opts)
                    elif ii in opts:
                        for jj in range(0,len(string_a)):
                           if '{%s}'%(ii) in string_a[jj]:
                               string_a[jj]=string_a[jj].format(**opts)
                return True,Join(string_a,symbol=' ')
            elif i == 2:
                new_str=''
                string_a=string.split()
                oidx=0
                for ii in tmp:
                    idx=None
                    if '%({})s'.format(ii) in string_a:
                        idx=string_a.index('%({})s'.format(ii))
                    elif "'%({})'".format(ii) in string_a:
                        idx=string_a.index("'%({})s'".format(ii))
                    if isinstance(idx,int):
                        if ii in opts:
                            string_a[idx]=string_a[idx]%(opts)
                    elif ii in opts:
                        for jj in range(0,len(string_a)):
                           if '%({})s'.format(ii) in string_a[jj]:
                               string_a[jj]=string_a[jj]%(opts)
                return True,Join(string_a,symbol=' ')
            elif i == 3:
                if inps:
                    if len(tmp) == len(inps): return string.format(*inps)
                    return False,"Mismatched input (tuple/list) number (require:{}, input:{})".format(len(tmp),len(inps))
                elif opts:
                    if len(tmp) == len(opts): return string.format(*opts.values())
                    return False,"Mismatched input (tuple/list) number (require:{}, input:{})".format(len(tmp),len(opts))
        i+=1
    return True,string

def Sort(src,reverse=False,func=None,order=None,field=None,base='key',sym=None):
    if isinstance(src,str) and not IsNone(sym): src=src.split(sym)
    if isinstance(src,dict) and base in ['data','value']:
        field=1
    def _clen_(e):
        try:
            if isinstance(field,int):
                if isinstance(e,(list,tuple)) and len(e) > field:
                    return len('{}'.format(Str(e[field])))
                else:
                    return 9999999
            return len('{}'.format(Str(e)))
        except:
            return e
    def _cint_(e):
        try:
            if isinstance(field,int):
                if isinstance(e,(list,tuple)) and len(e) > field:
                    return int(e[field])
                else:
                    return 9999999
            return int(e)
        except:
            return e
    def _cstr_(e):
        if isinstance(field,int):
            if isinstance(e,(list,tuple)) and len(e) > field:
                return '''{}'''.format(e[field])
            else:
                return 'zzzzzzzzz'
        return '''{}'''.format(e)
    if isinstance(src,(list,tuple)):
        src=list(src)
        if order in [int,'int','digit','number']:
            src.sort(reverse=reverse,key=_cint_)
        elif order in ['len','length']:
            src.sort(reverse=reverse,key=_clen_)
        elif order in [str,'str']:
            src.sort(reverse=reverse,key=_cstr_)
        else:
            if isinstance(field,int):
                src.sort(reverse=reverse,key=_cint_)
            else:
                src.sort(reverse=reverse,key=func)
        return src
    elif isinstance(src,dict):
        lst=list(src.items())
        if base == 'key':
            field=0
            if order in [int,'int','digit','number']:
                lst.sort(reverse=reverse,key=_cint_)
            elif order in ['len','length']:
                lst.sort(reverse=reverse,key=_clen_)
            elif order in [str,'str']:
                lst.sort(reverse=reverse,key=_cstr_)
            else:
                lst.sort(reverse=reverse,func=func)
        else: # value / data case
            field=1
            if order in [int,'int','digit','number']:
                lst.sort(reverse=reverse,key=_cint_)
            elif order in ['len','length']:
                return lst.sort(reverse=reverse,key=_clen_)
            elif order in [str,'str']:
                lst.sort(reverse=reverse,key=_cstr_)
            else:
                lst.sort(reverse=reverse,func=func)
        return lst
        #return [i[0] for i in lst]


def MacV4(src,**opts):
    '''
    Check Mac address format and convert
    Hex to Int
    Hex to Mac string
    Mac string to Int
    symbol : default ':' mac address spliter symbol
    out :
      str : default : XX:XX:XX:XX:XX format
      int : integer format
    default : False
    case : 
      upper : upper case output
      lower : lower case output
    '''
    symbol=opts.get('symbol',opts.get('sym',':'))
    default=opts.get('default',False)
    out=opts.get('out','str')
    case=opts.get('case','lower')
    def int2str(src,sym):
        return ':'.join(['{}{}'.format(a, b) for a, b in zip(*[iter('{:012x}'.format(src))]*2)])
    def str2int(src):
        return int(src.lower().replace('-','').replace(':',''), 16)
    if Type(src,'bytes'): 
        if len(src) == 6: # format b'\x00\xde4\xef.\xf4'
            src=codecs.encode(src,'hex')  # format b'00de34ef2ef4'
        src=Str(src)
    if isinstance(src,str):
        src=src.strip()
        # make sure the format
        if 12 <= len(src) <= 17:
            for i in [':','-']:
                src=src.replace(i,'')
            src=Join([src[i:i+2] for i in range(0,12,2)],symbol=':')
        # Check the normal mac format
        octets = src.split(':')
        if len(octets) != 6: return default
        for i in octets:
            try:
               if len(i) != 2 or int(i, 16) > 255:
                   return default
            except:
               return default
        if out in [int,'int','number']: return str2int(src)
        if symbol != ':': src=src.replace(':',symbol)
        if case == 'upper': return src.upper()
        return src.lower()
    elif isinstance(src,int):
        if out in [int,'int','number']: return src
        src=int2str(src,symbol)
        if case == 'upper': return src.upper()
        return src.lower()
    return default

def Path(*inp,**opts):
    '''
    Get Path of input
    inputs)
       ~       : home path
       ~<user> : user's home path
       None    : current path
       __file__: current python script file path
       __mod__ : This python script file path
       file    : the file's path
       [list]  : convert to path rule 
       obj     : support function, module, class, instance

    remove_dot : 
      True : (default) /a/b/./../c => /a/c
      False: /a/b/./../c => /a/b/./../c
    error : 
      False: default, if path issue then return error
      True : if path issue then ignore
    out :
     str : default: return path string
     list: return list format
       - force_root : default False, True: ['','a','b'] or ['a','b'] => '/a/b'

     '/a/b/c' => ['','a','b','c'] (out=list)
     'a/b/c'  => ['a','b','c']    (out=list)
     ['','a','b','c']  => '/a/b/c'(out=str)
     ['a','b','c']     => 'a/b/c' (out=str)
    '''
    sym=opts.get('sym','/')
    out=opts.get('out','str')
    exist=opts.get('exist',False)
    default=opts.get('default',False)
    remove_dot=opts.get('remove_dot',True)
    err=opts.get('err',opts.get('error',False))
    default=opts.get('default',False)
    base_dir=None
    if not inp:
        base_dir=os.environ['PWD']
    elif inp:
        if isinstance(inp[0],str):
            if os.path.isfile(inp[0]):
                base_dir=os.path.dirname(os.path.abspath(inp[0]))
            elif inp[0] == '__mod__':
                #This module path
                base_dir=os.path.dirname(os.path.abspath(__file__)) # Not input then get current path
            elif inp[0] == '__file__':
                #Get Caller function's Filename
                my_file=inspect.getfile(FunctionName(parent=1,obj=True)[1]) 
                base_dir=os.path.dirname(os.path.abspath(my_file)) # Get filename path
            else:
                base_dir=inp[0]
        elif Type(inp[0],('function','module','classobj','instance')):
            my_file=inspect.getfile(inp[0]) # Get obj's filename
            base_dir=os.path.dirname(os.path.abspath(my_file))  
    full_path=[]
    if isinstance(base_dir,str):
        full_path=base_dir.split(sym)
    elif isinstance(inp[0],(list,tuple)):
        full_path=list(inp[0])
    if full_path:
        if full_path[0] == '~' or (full_path[0] and full_path[0][0] == '~'):      # ~ or ~<user> style
            #full_path=os.environ['HOME'].split(sym)+full_path[1:]
            full_path=os.path.expanduser(full_path[0]).split(sym)+full_path[1:]
#        elif full_path[0] and full_path[0][0] == '~': # ~<user> style
#            full_path=os.path.expanduser(full_path[0]).split(sym)+full_path[1:]
    if remove_dot:
        nfp=[]
        for i in full_path:
            if i == '..': #remove '..'
                if nfp:
                    #keep root path ('/')
                    if len(nfp)==1:
                        if nfp[0]:
                            del nfp[-1]
                        elif err:
                            return default
                    else:
                        del nfp[-1]
                elif err:
                    return default
            else:
                if i != '.': #remove '.'
                    nfp.append(i)
        full_path=nfp
    for ii in inp[1:]: # add extra input
        if isinstance(ii,str):
            for zz in ii.split(sym):
                if remove_dot:
                    if zz == '.' or not Type(zz,'str',data=True): continue
                    if zz == '..':
                        if full_path:
                            #keep root path ('/')
                            if len(full_path)==1:
                                if full_path[0]:
                                    del full_path[-1]
                                elif err:
                                    return default
                            else:
                                del full_path[-1]
                            continue
                        elif err:
                            return default
                full_path.append(zz)
    if out in [str,'str']:
        if not full_path: return ''
        rt=Join(full_path,symbol=sym)
        if opts.get('force_root',opts.get('root',False)):
            if rt[0] != '/': return '/'+rt
        return rt
    else:
        return full_path

def Cut(src,head_len=None,body_len=None,new_line='\n',out=str):
    '''
    Cut string
    head_len : int : first line length (default None)
               if body_len is None then everything cut same length with head_len
    body_len : int : line length after head_len (default None)
    new_line : default linux new line
    out=
        str  : output to string with new_line (default)
        list : output to list instead new_line
    '''
    if not isinstance(src,str): return False
    source=src.split(new_line)
    if len(source) == 1 and not head_len or head_len >= len(src):
       if src and out in ['str',str]: return Join(src,symbol=new_line)
       return [src]
    rt=[]
    for src_idx in range(0,len(source)):
        str_len=len(source[src_idx])

        if not body_len:
            rt=rt+[source[src_idx][i:i + head_len] for i in range(0, str_len, head_len)]
        else:
            if src_idx == 0:
                rt.append(source[src_idx][0:head_len]) # Take head
                if str_len > head_len:
                    rt=rt+[source[src_idx][head_len:][i:i + body_len] for i in range(0, str_len-head_len, body_len)]
            else:
                rt=rt+[source[src_idx][i:i + body_len] for i in range(0, str_len, body_len)]
    if rt and out in ['str',str]: return Join(rt,symbol=new_line)
    return rt

def Space(num=4,fill=None,mode='space',tap=''):
    '''
    make a charactor(space, tap) group
    num: default 4, how many fill out <fill>
    mode:
      space : default: ' '
      tap   : \\t
    fill:
      None : default: following mode information
      <special charactor> : fill out the charactor
    tap:
      ''   : default
      <spcial inital chractor>: pre-fillout with this chractor
    '''
    mode=mode.lower()
    if mode =='tap':
        fill='\t'
    elif mode == 'space' or fill is None:
        fill=' '
    for i in range(0,num):
        tap=tap+fill
    return tap

def WrapString(string,fspace=0,nspace=0,new_line='\n',flength=0,nlength=0,ntap=0,NFLT=False,mode='space',default='',out='str'):
    if IsNone(string): return default
    if not Type(string,'str'):string='''{}'''.format(string)
    rc_str=[]
    string_a=string.split(new_line)
    #First line design
    if NFLT: fspace=0
    rc_str.append(Space(fspace,mode=mode)+Join(Cut(string_a[0],head_len=flength,body_len=nlength,new_line=new_line,out=list),'\n',append_front=Space(nspace,mode=mode)))
    #Body line design
    for ii in string_a[1:]:
        rc_str.append(Space(nspace,mode=mode)+Join(Cut(ii,head_len=nlength,new_line=new_line,out=list),'\n',append_front=Space(nspace,mode=mode)))
    #return new_line.join(rc_str)
    if out in [list,'list']: return rc_str
    elif out in [tuple,'tuple']: return tuple(rc_str)
    return Join(rc_str,new_line)

def GetKey(src,find=None,default=None,mode='first',root=None):
    '''
    Get key from dict,list,tuple,str
    find : if matched value then return the key/index of the data
    mode :
      first : default: return first find
      all   : return found all
    default : return when not found
    '''
    rt=[]
    if isinstance(src,dict):
        if IsNone(find):
            return list(src.keys())
        else:
            for key,val in src.items():
                if isinstance(val,dict):
                    a=GetKey(val,find,default,mode,key)
                    if a:
                        if isinstance(a,str):
                            if root is None:
                                return '/{}/{}'.format(key,a)
                            else:
                                return '{}/{}'.format(key,a)
                        elif isinstance(a,list):
                            for i in a:
                                if root is None:
                                    rt.append('/{}/{}'.format(key,i))
                                else:
                                    rt.append('{}/{}'.format(key,i))
                elif val == find:
                    if mode == 'first': return key
                    rt.append(key)
            if rt: return rt
    elif isinstance(src,(list,tuple,str)):
        if IsNone(find):
            return len(src)
        else:
            for i in range(0,len(src)):
                if find == src[i]:
                    if mode == 'first': return i
                    rt.append(i)
        if rt: return rt
    return default

def rm(*args,**opts):
    '''
    delete local file with option like as CLI
       [<opt>] <files>/<directory>
       -f    : don't ask delete
       -r    : <directory> or recurring delete
    delete local file with option like as Function
       <files>/<directory>,...
       force=True    : don't ask delete, default False
       recurring=True: <directory> or recurring delete
    delete list/tuple
       <list,tuple>,<del items>,...
       option)
         data
           True : delete data like as <del items>
           False: (default) delete index (<del items> are int)
    delete dict
       <dict>,<del items>,...
       option)
         data
           True : delete data like as <del items>
           False: (default) delete key like as <del items>
         recurring 
           False: searching data in first level
           True : keep searching inside dictionary 
    '''
    if len(args) <= 0: return opts.get('default')
    #List/Tuple
    if Type(args[0],(list,tuple)):
        rt=list(args[0])
        del_data=opts.get('value',opts.get('data',False))
        if del_data:
            for i in args[1:]:
                if i in rt: rt.remove(i)
            if Type(args[0],'tuple'): return tuple(rt)
            return rt
        else:
            tmp=[]
            for i in range(0,len(rt)):
                if i in args[1:]: continue
                tmp.append(rt[i])
            if Type(args[0],'tuple'): return tuple(tmp)
            return tmp
    #Dict
    elif Type(args[0],dict):
        rt=args[0]
        del_data=opts.get('value',opts.get('data',False))
        # Del Data
        if del_data: 
            tmp=[]
            rt_items=list(rt.items())
            for i in range(0,len(rt_items)):
                #Recurring check
                if opts.get('recurring',False) and Type(rt_items[i][1],dict):
                    a=list(rt_items[i])
                    a[1]=rm(rt_items[i][1],*args[1:],data=del_data)
                    tmp.append(tuple(a))
                elif rt_items[i][1] not in args[1:]:
                    tmp.append(rt_items[i])
            return dict(tmp)
        # Del key
        else:
            # Recurring checking
            if opts.get('recurring',False):
                tmp=[]
                rt_items=list(rt.items())
                for i in range(0,len(rt_items)):
                    if rt_items[i][0] not in args[1:]:
                        if Type(rt_items[i][1],dict):
                            a=list(rt_items[i])
                            a[1]=rm(rt_items[i][1],*args[1:],data=del_data)
                            tmp.append(tuple(a))
                        else:
                            tmp.append(rt_items[i])
                return dict(tmp)
            else:
                for i in args[1:]:
                    #Path key
                    if '/' in i and i[0] == '/':
                        i_a=i.split('/')
                        tmp=rt
                        brk=False
                        for z in i_a[1:-1]:
                            if z in tmp:
                                tmp=tmp[z]
                            else:
                                brk=True
                                break
                        if not brk and i_a[-1] in tmp: tmp.pop(i_a[-1])
                        continue
                    elif i in rt:
                        rt.pop(i)
        return rt
    else:
            #File/Directory
            sub_dir=opts.get('recurring',False)
            force=opts.get('force',False)
            if find_executable('rm'):
                sub_opt=''
                if sub_dir: sub_opt='-r'
                if force:
                    if sub_opt: sub_opt=sub_opt+'f'
                    else: sub_opt='-f'
                rshell('rm -i {}'.format(sub_opt)+Join(args,' '),interactive=True)
            else:
                for arg in args:
                    if arg[0] == '-':
                       if 'r' in arg:
                          sub_dir=True
                       if 'f' in arg:
                          force=True
                    else:
                        if os.isfile(arg):
                            if not force:
                                yn=cli_input('Delete {} (Y/N)?')
                                if not isinstance(yn,str) or yn.lower() not in ['y','yes']: continue
                            #os.remove(arg)
                            os.unlink(arg)
                        elif os.isdir(arg):
                            if sub_dir:
                                if not force:
                                    yn=cli_input('Delete {} (Y/N)?')
                                    if not isinstance(yn,str) or yn.lower() not in ['y','yes']: continue
                                shutil.rmtree(arg)
                            else:
                                print('''can't delete directory:{}'''.format(arg))
                        else:
                            print('''can't delete {}'''.format(arg))
    return opts.get('default')

def List(*inps,**opts):
    '''
    tuple2list: 
        True : convert tuple data to list data
        False: append tuple into list
    <dict input>
     items : <dict>.items()
     data  : <dict>.value()
     path  : convert <dict> to path like list ([('/a/b',1),('/a/c',2),...])
     (default): <dict>.keys()
    <option>
     idx=<int>    : get <idx> data
     del=<int>    : delete <idx>
     first=<data> : move <data> to first
     end=<data>   : move <data> to end
     find=<data>  : get Index list
     uniq=False   : Uniq data
     strip=False  : remove white space
     default      : False
     mode 
        auto      : auto fixing index
        err       : not found then return default(False)
        ignore    : not found then ignore the data
    '''
    def DD(s):
        rt=[]
        for i in s:
            if Type(s[i],dict):
                for z in DD(s[i]):
                    rt.append((i+'/'+z[0],z[1]))
            else:
                rt.append((i,s[i]))
        return rt

    tuple2list=opts.get('tuple2list',True)
    mode=opts.get('mode','auto')
    rt=[]
    if len(inps) == 0 : return rt
    if Type(inps[0],list):
        rt=inps[0]
    elif Type(inps[0],tuple):
        if tuple2list:
            rt=list(inps[0])
        else:
            rt.append(inps[0])
    elif Type(inps[0],dict):
        if opts.get('data'):
            rt=list(inps[0].values())
        elif opts.get('all',opts.get('whole',opts.get('items'))):
            rt=list(inps[0].items())
        elif opts.get('path'):
            tmp=[]
            for k in inps[0]:
                if Type(inps[0][k],dict):
                    for d in DD(inps[0][k]):
                        tmp.append(('/'+k+'/'+d[0],d[1]))
                else:
                    tmp.append(('/'+k,inps[0][k]))
            rt=rt+tmp
        else:
            rt=list(inps[0])
    for i in inps[1:]:
        if Type(i,list):
            rt=rt+i
        else:
            if Type(i,tuple):
                if tuple2list:
                    rt=rt+list(i)
                    continue
            elif Type(i,dict):
                rt=rt+List(rt,i,**opts)
                continue
            rt.append(i)
    if opts.get('strip'):
        rt=[i.strip() if isinstance(i,(str,bytes)) else i for i in rt]
    if opts.get('uniq'):
        return Uniq(rt)
    idx=opts.get('idx')
    if not IsNone(idx):
        ok,idx=IndexForm(idx,idx_only=True,symbol=',')
        if ok is False: return opts.get('default',False)
        if isinstance(idx,tuple) and len(idx) == 2:
            idx=range(idx[0],idx[1]+1)
        if not Type(idx,(list,tuple,'range')): idx=[idx]
        tt=[]
        for i in idx:
            if mode == 'auto':
                i=FixIndex(rt,i,default=False,err=False)
            elif mode in ['err','ignore']:
                i=FixIndex(rt,i,default=False,err=True)
            if i is False:
                if mode == 'err': return opts.get('default',False)
            else:
                tt.append(rt[i])
        return tt
    if not IsNone(opts.get('rm')):
        return rm(rt,*opts.get('rm') if Type(opts.get('rm'),(list,tuple)) else opts.get('rm'))
    first=opts.get('first')
    if not IsNone(first) and first in rt:
        return [first]+[i for i in rt if i != first]
    end=opts.get('end')
    if not IsNone(end) and end in rt:
        return [i for i in rt if i != end]+[end]
    find=opts.get('find')
    if not IsNone(find):
        if not Type(find,(list,tuple)): find=[find]
        tt=[]
        for i in find:
            for z in range(0,len(rt)):
                j=i.replace('*','.+').replace('?','.')
                mm=re.compile(j)
                if bool(re.match(mm,rt[z])):
                    tt.append(z)
                #if rt[z] == i: tt.append(z)
        return tt
    return rt

def Replace(src,replace_what,replace_to,default=None,newline='\n'):
    '''
    replace string (src, from, to)
    if not string then return default
    default: return defined value when not string
      'org': return src
      ...  : return defined default
    '''
    def _S_(src,p):
        if isinstance(p,list):
            t=[]
            m=len(p)-1
            for i in range(0,m+1):
                if i == 0:
                    t.append(src[:p[i][0]])
                    if i==m:
                        t.append(src[p[i][1]:])
                elif i < m:
                    t.append(src[p[i-1][1]:p[i][0]])
                elif i == m:
                    t.append(src[p[i-1][1]:p[i][0]])
                    t.append(src[p[i][1]:])
            return t

    if not Type(src,('str','bytes')):
        return Default(src,default)
    if Type(src,'bytes'):
        replace_what=Bytes(replace_what)
        replace_to=Bytes(replace_to)
        newline=Bytes(newline)
    else:
        replace_what=Str(replace_what)
        replace_to=Str(replace_to)
        newline=Str(newline)
    tmp=[]
    for ii in src.split(newline):
        tt=_S_(ii,Found(ii,replace_what,location=True))
        tmp.append(Join(tt,replace_to) if tt else ii)
    return Join(tmp,newline)

def krc(rt,chk='_',rtd={'GOOD':[True,'True','Good','Ok','Pass','Sure',{'OK'},0],'FAIL':[False,'False','Fail',{'FAL'}],'NONE':[None,'None','Nothing','Empty','Null','N/A',{'NA'}],'IGNO':['IGNO','Ignore',{'IGN'}],'ERRO':['ERR','Erro','Error',{'ERR'},1,126,128,130,255],'WARN':['Warn','Warning',{'WAR'}],'UNKN':['Unknown','UNKN',"Don't know",'Not sure',{'UNK'}],'JUMP':['Jump',{'JUMP'}],'TOUT':['TimeOut','Time Out','TMOUT','TOUT',{'TOUT'}],'REVD':['Cancel','Canceled','REV','REVD','Revoked','Revoke',{'REVD'}],'LOST':['Lost','Connection Lost','Lost Connection',{'LOST'}],'NFND':['File not found','Not Found','Can not found',{'NFND'},127]},default=False,mode=None):
    '''
    Shell exit code:
      1   - Catchall for general errors
      2   - Misuse of shell builtins (according to Bash documentation)
    126   - Command invoked cannot execute
    127   - “command not found”
    128   - Invalid argument to exit
    128+n - Fatal error signal “n”
    130   - Script terminated by Control-C
    255\* - Exit status out of range
    '''
    if mode == 'get':
        return rtd
    elif mode == 'keys':
        if isinstance(rtd,dict):
            return rtd.keys()
    def trans(irt):
        type_irt=type(irt)
        for ii in rtd:
            for jj in rtd[ii]:
                if type(jj) == type_irt and ((type_irt is str and jj.lower() == irt.lower()) or jj == irt):
                    return ii
        return 'UNKN'
    rtc=Get(rt,'0|rc',err=True,default='org',type=(bool,int,list,tuple,dict))
    nrtc=trans(Peel(rtc,err=False,default='unknown')) #If Get() got multi data then use first data
    if chk != '_':
        if not isinstance(chk,list): chk=[chk]
        for cc in chk:
            if trans(cc) == nrtc:
                return True
            if nrtc == 'UNKN' and default == 'org':
                return rtc
        return Default(rt,default)
    return nrtc

def OutFormat(data,out=None,strip=False,peel=None,org=None,default=None):
    '''
    Output Format maker
    <option>
      out
        None: Not convert
        str,int,list,dict : convert data to want format
        raw : Peeled data when single data(['a'],('a'),{'a':'abc'}) others then return orignal
      peel
        None : automatically working according to out
        True : Peeling data
        False: Not Peeling
      strip 
        False: not remove white space
        True : remove white space
    '''
    out_data=None
    if out in [tuple,'tuple',list,'list']:
        if not isinstance(data,(tuple,list)):
            out_data=[data]
        else:
            out_data=list(data)
        if out in [tuple,'tuple']:
            if out_data:
                return tuple(out_data)
            elif isinstance(default,tuple):
                return default
            else:
                return (Default(org,default))
        if out_data:
            return out_data
        elif isinstance(default,list):
            return default
        else:
            return [Default(org,default)]
    elif out in [dict,'dict']:
        if data:
            return Dict(data)
        elif isinstance(default,dict):
            return default
        else:
            return Default(org,default)
    elif out in ['str',str]:
        out_data=WhiteStrip(Peel(data,peel),strip)
    elif out in ['int',int]:
        out_data=Int(WhiteStrip(Peel(data,peel),strip))
    if out_data is False: #if str or int got False then 
        return Default(org,default)
    if out == 'raw' or IsNone(out):
        if IsNone(peel): peel=True
    out_data=WhiteStrip(Peel(data,peel),strip)
    if out_data: return out_data
    return Default(org,default)

def FeedFunc(obj,*inps,**opts):
    '''
    Automatically Feed matched variables to function
    FeedFunc(<func>,<function's arguments>,<function's variables>)
    if something wrong then return False
    if correct then return output of ran the Function with inputs
    '''
    if Type(obj,'str') and not inspect.isclass(obj): # for str class
        mymod=MyModule(default=False,parent=1)
        if mymod is False:
            mymod=MyModule(default=False,parent=0)
        if mymod is False:
            mymod=MyModule(default=False,parent=-1)
        if Type(mymod,'module'):
            try:
                obj=getattr(mymod,obj,None)
            except:
                StdErr('Function name "{}" not found in the module\n'.format(obj))
                return False
    if Type(obj,('function','builtin_function_or_method','type','int','str','list','dict')):
        fcargs=FunctionArgs(obj,mode='detail',default={})
        ninps=[]
        nopts={}
        #Special case int,str,list,dict
        if Type(obj, ('int','str','list','dict')):
            if inps: ninps.append(inps[0])
            if 'base' in opts: #int()
                nopts['base']=opts['base']
            if 'encoding' in opts: # str()
                nopts['encoding']=opts['encoding']
            elif Type(obj,'str') and ninps and Type(ninps[0],'bytes') and 'encoding' not in opts: # str()
                nopts['encoding']='ascii'
        idx=0
        if 'args' in fcargs:
            for i in fcargs['args']:
                if len(inps) > idx:
                    ninps.append(inps[idx])
                    idx+=1
                else:
                    if i in opts:
                        ninps.append(opts.pop(i))
                    else:
                        StdErr('input parameter "{}" not found\n'.format(i))
                        return False
        if 'varargs' in fcargs:
            ninps=ninps+list(inps[idx:])
        if 'defaults' in fcargs:
            for i in fcargs['defaults']:
                if i in opts:
                    nopts[i]=opts.pop(i) #make with input value
                else:
                    nopts[i]=fcargs['defaults'][i] # make with default value
        if 'keywords' in fcargs:
            nopts.update(opts)
        #Run function with found arguments
        if ninps and nopts:
            if Type(obj,('int','str')):
                return obj(ninps[0],**nopts)
            else:
                return obj(*ninps,**nopts)
        elif ninps:
            if Type(obj,('int','str','list','dict')):
                return obj(ninps[0])
            else:
                return obj(*ninps)
        elif nopts:
            return obj(**nopts)
        else:
            try:
                return obj()
            except:
                e=ExceptMsg()
                StdErr(e)
    return False

def printf(*msg,**opts):
    date_format=opts.get('date_format','%m/%d/%Y %H:%M:%S' if opts.get('date') else None)
    direct=opts.get('direct',False)
    dsp=opts.get('dsp','a')
    log=opts.get('log',None)
    log_level=opts.get('log_level',8)
    caller=opts.get('caller','detail' if opts.get('caller_detail') else None)
    caller_tree=opts.get('caller_tree',opts.get('caller_history'))
    syslogd=opts.get('syslogd',None)
    new_line=opts.get('new_line',opts.get('newline','' if direct else '\n'))
    form=opts.get('form')
    intro=opts.get('intro',None)
    logfile=opts.get('logfile',[])

    #Logfile
    if isinstance(logfile,str):
        logfile=logfile.split(',')
    for ii in msg:
        if isinstance(ii,str) and ':' in ii:
            logfile_list=ii.split(':')
            if logfile_list[0] in ['log_file','logfile']:
                if len(logfile_list) > 2:
                    for jj in logfile_list[1:]:
                        logfile.append(jj)
                else:
                    logfile=logfile+logfile_list[1].split(',')
                msg.remove(ii)
    # save msg(removed log_file information) to syslogd 
    if syslogd:
        if syslogd in ['INFO','info']:
            syslog.syslog(syslog.LOG_INFO,msg)
        elif syslogd in ['KERN','kern']:
            syslog.syslog(syslog.LOG_KERN,msg)
        elif syslogd in ['ERR','err']:
            syslog.syslog(syslog.LOG_ERR,msg)
        elif syslogd in ['CRIT','crit']:
            syslog.syslog(syslog.LOG_CRIT,msg)
        elif syslogd in ['WARN','warn']:
            syslog.syslog(syslog.LOG_WARNING,msg)
        elif syslogd in ['DBG','DEBUG','dbg','debug']:
            syslog.syslog(syslog.LOG_DEBUG,msg)
        else:
            syslog.syslog(msg)
    # Make a Intro
    intro_msg=''
    if date_format and not syslogd:
        intro_msg='{0} '.format(TIME().Now().strftime(date_format))
    intro_len=len(intro_msg)
    if caller:
        arg={'parent':1,'args':True}
        if caller == 'detail':
            arg.update({'line_number':True,'filename':True})
        if caller_tree is True:
            arg.update({'history':True,'tree':True})
        call_name=FunctionName(**arg)
        if call_name:
            intro_msg=intro_msg+WrapString(Join(call_name,'\n'),fspace=0, nspace=len(intro_msg),mode='space')+': '
            intro_len=intro_len+len(call_name[-1])+2
    if Type(intro,'str') and intro:
        intro_msg=intro_msg+intro+': '
        intro_len=intro_len+len(intro)

    # Make a msg
    msg_str=''
    for ii in msg:
        if form:
            msg_str=msg_str if msg_str else intro_msg + ColorStr(WrapString(Str(pprint.pformat(ii),default='org'),fspace=intro_len if msg_str else 0, nspace=intro_len,mode='space'),**opts)
        else:
            msg_str=msg_str if msg_str else intro_msg + ColorStr(WrapString(Str(ii,default='org'),fspace=intro_len if msg_str else 0, nspace=intro_len,mode='space'),**opts)

    log_p=False
    #Log function
    if Type(log,'function'):
        log_p=True
        FeedFunc(log,msg_str,**opts)
    if isinstance(printf_log_base,int) and not isinstance(printf_log_base,bool):
        if printf_log_base < log_level:
            return
    # Save msg to file
    if 'f' in dsp or 'a' in dsp:
        for ii in logfile:
            if ii and os.path.isdir(os.path.dirname(ii)):
                log_p=True
                with open(ii,'a+') as f:
                    f.write(msg_str+new_line)
    # print msg to screen
    if (log_p is False and 'a' in dsp) or 's' in dsp or 'e' in dsp:
         if 'e' in dsp:
             StdErr(msg_str+new_line)
         else:
             StdOut(msg_str+new_line)
    # return msg
    if 'r' in dsp:
         return msg_str

def ColorStr(msg,**opts):
    color=opts.get('color',None)
    color_db=opts.get('color_db',{'blue': 34, 'grey': 30, 'yellow': 33, 'green': 32, 'cyan': 36, 'magenta': 35, 'white': 37, 'red': 31})
    bg_color=opts.get('bg_color',None)
    bg_color_db=opts.get('bg_color_db',{'cyan': 46, 'white': 47, 'grey': 40, 'yellow': 43, 'blue': 44, 'magenta': 45, 'red': 41, 'green': 42})
    attr=opts.get('attr',None)
    attr_db=opts.get('attr_db',{'reverse': 7, 'blink': 5,'concealed': 8, 'underline': 4, 'bold': 1})
    if IsNone(os.getenv('ANSI_COLORS_DISABLED')) and (color or bg_color or attr):
        reset='''\033[0m'''
        fmt_msg='''\033[%dm%s'''
        if color and color in color_db:
            msg=fmt_msg % (color_db[color],msg)
        if bg_color and bg_color in bg_color_db:
            msg=fmt_msg % (color_db[bg_color],msg)
        if attr and attr in attr_db:
            msg=fmt_msg % (attr_db[attr],msg)
        return msg+reset #Support Color
    return msg #Not support color

def CleanAnsi(data):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    if Type(data,('str','bytes')):
        return ansi_escape.sub('',Str(data))
    elif isinstance(data,(list,tuple)):
        return [CleanAnsi(ii) for ii in data]
    elif isinstance(data,dict):
        for i in data:
            data[i]=CleanAnsi(data[i])
    return data

def cli_input(msg,**opts):
    '''
    CLI Input command
    '''
    hidden=opts.get('hidden',opts.get('passwd',opts.get('password',False)))
    if hidden:
        if sys.stdin.isatty():
            p = getpass.getpass(msg)
        else:
            printf(msg,end_line='')
            p = sys.stdin.readline().rstrip()
    else:
        if PyVer(2):
            p=raw_input(msg)
        else:
            p=input(msg)
    return p

def TypeData(src,want_type=None,default='org',spliter=None):
    '''Convert (input)data to want type (ex: str -> list, int, ...), can not convert to type then return False'''
    if Type(want_type,'str'):
        if isinstance(src,(list,tuple)):
            if not isinstance(spliter,str): spliter=' '
            return Join(Str(src),Str(spliter))
        else:
            return Str(src,mode='force')
    elif Type(want_type,'bytes'):
        if isinstance(src,(list,tuple)):
            if not isinstance(spliter,str): spliter=b' '
            return Join(Bytes(src),Bytes(spliter))
        else:
            return Bytes(src)
    elif Type(want_type,'int'):
        return Int(src,err=True)
    elif Type(want_type,('list','tuple')) and isinstance(src,str) and isinstance(spliter,str):
        if Type(want_type,'tuple'):
            return tuple(Split(src,spliter))
        return Split(src,spliter)
    elif Type(want_type,'tuple') and isinstance(src,(list,dict)):
        if isinstance(src,dict):
            if spliter == 'key':
                return tuple(src.keys())
            elif spliter == 'value':
                return tuple(src.values())
            else:
                return tuple(src.items())
        return tuple(src)
    elif Type(want_type,'list') and isinstance(src,(tuple,dict)):
        if isinstance(src,dict):
            if spliter == 'key':
                return list(src.keys())
            elif spliter == 'value':
                return list(src.values())
            else:
                return list(src.items())
        return list(src)
    elif Type(src,want_type):
        return src
    if Type(src,('str','bytes')):
        return FormData(src,default='org')
    return Default(src,default)

def MoveData(src,data=None,to=None,from_idx=None,force=False,default='org'):
    '''
    support src type is list,str,(tuple)
    moving format : data(data) or from_idx(int)
      - data : if src has many same data then just keep single data at moved
    moving dest   : to(int)
    move data or index(from_idx) to want index(to)
      force=True: even tuple to move
    if not support then return default
    default : org
    '''
    _tuple=False
    src_type=TypeName(src)
    if src_type == 'tuple':
        if not force: return Default(src,default)
        _tuple=True
        src_type='list'
    if src_type in ['list','str'] and src:
        src=list(src)
        if to == 'last': to=-1
        elif to == 'first': to=0
        if isinstance(from_idx,int) and isinstance(to,int):
            if len(src) > abs(from_idx):
                to=FixIndex(src,to)
                if from_idx!=to:
                    if to == -1:
                        src.append(src[from_idx])
                    elif to == 0:
                        src=[src[from_idx]]+src
                    else:
                        src=src[:to]+[src[from_idx]]+src[to:]
                    src[to]=src[from_idx]
                    del src[from_idx]
        elif not IsNone(data) and isinstance(to,int):
            to=FixIndex(src,to)
            src=[i for i in src if i!=data]
            if to == -1:
                src.append(data)
            elif to == 0:
                src=[data]+src
            else:
                src=src[:to]+[data]+src[to:]
        if _tuple: return tuple(src)
        elif src_type == 'str': return Join(src,'')
        return src
    return Default(src,default)


#if __name__ == "__main__":
#    # Integer
#    print("Get(12345):",Get(12345))
#    print("Get(12345,1):",Get(12345,1))
#    # String
#    print("Get('12345'):",Get('12345'))
#    print("Get('12345',0):",Get('12345',0))
#    print("Get('12345',1):",Get('12345',1))
#    print("Get('12345',4):",Get('12345',4))
#    print("Get('12345',5):",Get('12345',5))
#    print("Get('12345',-1):",Get('12345',-1))
#    print("Get('12345',-5):",Get('12345',-5))
#    print("Get('12345',-7):",Get('12345',-7))
#    # List
#    print("Get([1,2,3,4,5]):",Get([1,2,3,4,5]))
#    print("Get([1,2,3,4,5],1):",Get([1,2,3,4,5],1))
#    print("Get([1,2,3,4,5],(1,3)):",Get([1,2,3,4,5],(1,3)))
#    print("Get([1,2,3,4,5],'1-3')):",Get([1,2,3,4,5],'1-3'))
#    print("Get([1,2,3,4,5],-1)):",Get([1,2,3,4,5],-1))
#    print("Get([1,2,3,4,5],-5)):",Get([1,2,3,4,5],-5))
#    print("Get([1,2,3,4,5],-6)):",Get([1,2,3,4,5],-6))
#    print("Get([1,2,3,4,5],5)):",Get([1,2,3,4,5],5))
#    print("Get([1,2,3,4,5],'1|2')):",Get([1,2,3,4,5],'1|2'))
#    print("Get([1,2,3,4,5],'1|2',idx_only=True)):",Get([1,2,3,4,5],'1|2',idx_only=True))
#    # Dict
#    print("Get({'a':{'b':{'c':1,'d':2},'e':3},'f':4}):",Get({'a':{'b':{'c':1,'d':2},'e':3},'f':4}))
#    print("Get({'a':{'b':{'c':1,'d':2},'e':3},'f':4},'/a/b/c'):",Get({'a':{'b':{'c':1,'d':2},'e':3},'f':4},'/a/b/c'))
#    print("Get({'a':{'b':{'c':1,'d':2},'e':3},'f':4},'a/b/d'):",Get({'a':{'b':{'c':1,'d':2},'e':3},'f':4},'a/b/d'))
#    print("Get({'a':{'b':{'c':1,'d':2},'e':3},'f':4},'f'):",Get({'a':{'b':{'c':1,'d':2},'e':3},'f':4},'f'))
#    print("Get({'a':{'b':{'c':1,'d':2},'e':3},'f':4},'a'):",Get({'a':{'b':{'c':1,'d':2},'e':3},'f':4},'a'))
#    print("Get({'a':{'b':{'c':1,'d':2},'e':3},'f':4},-1):",Get({'a':{'b':{'c':1,'d':2},'e':3},'f':4},-1))
#    print("Get({'a':{'b':{'c':1,'d':2},'e':3},'f':4},-1,idx_only=True):",Get({'a':{'b':{'c':1,'d':2},'e':3},'f':4},-1,idx_only=True))
#    print("Get({'a':{'b':{'c':1,'d':2},'e':3},'f':4,'g':5},(1,2)):",Get({'a':{'b':{'c':1,'d':2},'e':3},'f':4,'g':5},(1,2)))
#    # Module
#    me=MyModule()
#    #print("Get(me):",Get(me))
#    print("Get(me,'Get'):",Get(me,'Get'))
#    print("Get(me,'Get','Import'):",Get(me,'Get','Import'))
#    print("Get(me,'func_list'):",Get(me,'func_list'))
#    
#    print('1 : ',TypeName(1))
#    print('ping : ',TypeName('ping'))
#    print('function ping : ',TypeName(ping))
#    print('int : ',TypeName(int))
#    print('str : ',TypeName(str))
#    print('function : ',TypeName('function'))
#    print('classobj : ',TypeName('classobj'))
#    print('3.14 : ',TypeName(3.14))
#    print('WEB : ',TypeName('WEB'))
#    print('class WEB : ',TypeName(WEB))
#    print('bool : ',TypeName(bool))
#    print('False : ',TypeName(False))
#    print('True : ',TypeName(True))
#    print('None : ',TypeName(None))
    # Function
#    def KLog(inps,log_level=3,**opts):
#        print("KLog:",':',inps,'log_level=',log_level)
# 
#    print('Klog1:',FeedFunc('KLog',inps='1111',log_level=9))
#    print('Klog2:',FeedFunc('KLog','akd','uuuuuu',log_level=8,abc=33))
#    print('Klog3:',FeedFunc('KLog',log_level=8,abc=33))
#    print('int:',FeedFunc(int,'33',base=10))
#    print('str:',FeedFunc(str,33))
#    print('str:',FeedFunc(str,b'33'))
#    print('list:',FeedFunc(list,'33'))
#    print('list:',FeedFunc(list))
#    print('dict:',FeedFunc(dict,[('aa','33')]))
#    print('dict:',FeedFunc(dict))
