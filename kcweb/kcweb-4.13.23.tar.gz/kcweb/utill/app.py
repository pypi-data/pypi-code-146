# -*- coding: utf-8 -*-
import re
def oauth(url,config):
    data=False
    requeststr=re.sub('/','',url)
    if config.oauth['status']:
        for k in config.oauth['need']:
            if k == '*':
                data=True
            kk=k.split("*")
            if(len(kk)>1):
                s=re.sub('/','',kk[0])
                if s==requeststr[0:len(s)]:
                    data=True
                    break
            else:
                routestr= re.sub('/','',k)
                if routestr==requeststr:
                    data=True
                    break
        for k in config.oauth['unwanted']:
            if k == '*':
                data=False
            kk=k.split("*")
            if(len(kk)>1):
                s=re.sub('/','',kk[0])
                if s==requeststr[0:len(s)]:
                    data=False
                    break
            else:
                routestr= re.sub('/','',k)
                if routestr==requeststr:
                    data=False
                    break
    return data