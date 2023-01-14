# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 18:59:17 2023

@author: Administrator
"""
import ntplib,datetime
def ct(url):
    c = ntplib.NTPClient()
    
    hosts = ['edu.ntp.org.cn', 'tw.ntp.org.cn', 'us.ntp.org.cn', 'cn.pool.ntp.org', 'jp.ntp.org.cn']
    # hosts=url
    for host in hosts:
    
        try:
    
            response = c.request(host)
    
            if response:
    
                break
    
        except Exception as e:
    
            print(e)
    
    current_time = response.tx_time
    
    _date, _time = str(datetime.datetime.fromtimestamp(current_time))[:22].split(' ')
    
    print("系统当前时间", str(datetime.datetime.now())[:22])
    
    print("北京标准时间", _date, _time)
    
    a, b, c = _time.split(':')
    
    c = float(c) + 0.5
    
    _time = "%s:%s:%s" % (a, b, c)
    
    eval(r"os.system('date %s && time %s' % (_date, _time))")
    print("同步后时间:", str(datetime.datetime.now())[:22])