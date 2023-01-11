#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/9/20 11:50
# @Author  : jia666666
# @FileName: test1.py

from __future__ import print_function #兼容python2的print
import re
import pyperclip
import json
from .colors import red,green,yellow,white,good,run
import execjs
import time
import urllib.parse




def decodeURIComponent(string):
    "url解码"
    try:
        js_code = "decodeURIComponent('{}')".format(string)
        ctx = execjs.compile(js_code)
        results = ctx.eval(js_code)
        return results
    except Exception as e:
        return urllib.parse.unquote(string)
def printWelcomeMessage():
    "打印欢迎语"
    WelcomeMessage="""
        __                   __                  ____                           __
       / /_  ___  ____ _____/ /__  __________   / __/___  _________ ___  ____ _/ /_
      / __ \/ _ \/ __ `/ __  / _ \/ ___/ ___/  / /_/ __ \/ ___/ __ `__ \/ __ `/ __/
     / / / /  __/ /_/ / /_/ /  __/ /  (__  )  / __/ /_/ / /  / / / / / / /_/ / /_
    /_/ /_/\___/\__,_/\__,_/\___/_/  /____/  /_/  \____/_/  /_/ /_/ /_/\__,_/\__/
    """
    print(f'''{red}{WelcomeMessage}''')

def url_params(url):
    """url处理"""
    url=decodeURIComponent(url)
    k = {}
    if '?' in url:
        s=url.split('?')
        ss = s[1]
        sss = ss.split('&')
        for info in sss:
            key, value = info.split('=', maxsplit=1)
            k.update({key: value})
        return s[0],k
    else:
        return url,k
def join_requests(method,url,headers,data):
    "拼接python3"
    url,params=url_params(url)

    if method=="GET":
        if params:
            res=f"""
params={params}
response = requests.get('{url}', headers=headers, params=params,verify=False)
            """
        else:
            res=f"""
response = requests.get('{url}', headers=headers,verify=False)
            """
    elif method=="POST":
        if data:
            try:
                data=json.loads(data)
                res=f"""
params={params}
data={data}
response = requests.post('{url}', headers=headers,params=params,json=data,verify=False)
                """
            except Exception as e:
                data=str(data)
                res=f"""
params={params}
data='{data}'
response = requests.post('{url}', headers=headers, params=params,data=data,verify=False)
                """
        else:
            res=f"""
params={params}
response = requests.post('{url}', headers=headers, params=params,verify=False)
            """
    else:
        assert False,f'{red}目前仅支持get,post方法，暂不支持{method}方法'
    timestamp = time.time()  # 当前时间戳
    strtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))

    pyhton3=f"""
#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : {strtime}
# @Author  : Fidder_to_python3

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


{headers}

{res}

print(response.content.decode(errors='ignore'))
    """
    pyperclip.copy(pyhton3)  # 复制到剪切板
    print(f'''{green}{pyhton3}''')
    print(f'{good}python3已经复制到剪切板')  # 控制台先输出，方便检视，与剪切板的内容一样
def headers_format():
    """headers格式化函数"""
    printWelcomeMessage() #打印欢迎语
    print(f'{run}请输入要格式化的headers，回车两次结束')
    string = ''
    for s in iter(input, ''):  # 空字符串是结束标记
        s = re.sub("(.*?):[\s]{0,1}(.*)", r"'\1': '\2',", s)  # 正则提取内容
        string += ('\t'+s + '\n')
    headers='headers = {\n' + string + '}'
    pyperclip.copy(headers)  # 复制到剪切板
    print(f'''{green}{headers}''')
    print(f'{good}已经复制到剪切板') # 控制台先输出，方便检视，与剪切板的内容一样
def fidder_to_python3():
    "fidder转python"
    printWelcomeMessage()  # 打印欢迎语
    print(f'{run}请输入要转python3的raw，回车两次结束')
    string = ''
    for index,s in enumerate(iter(input, '')):  # 空字符串是结束标记
        if index==0:
            method,url = re.findall("(.*?) [\s]{0,1}(.*) HTTP/.*?", s)[0]  # 正则提取内容
        else:
            s = re.sub("(.*?):[\s]{0,1}(.*)", r"'\1': '\2',", s)  # 正则提取内容
            string += ('\t' + s + '\n')
    headers = 'headers = {\n' + string + '}'
    data = input()
    if len(data):
        pass
    else:
        data=''
    sign= re.findall('^http', url) #验证url是否包含http,主要是兼容burp
    if not sign:
        host=re.findall("'Host': '(.*?)',",headers)
        if host:
            url="https://"+host[0]+url
    join_requests(method,url,headers,data)

if __name__ == '__main__':
    fidder_to_python3()
