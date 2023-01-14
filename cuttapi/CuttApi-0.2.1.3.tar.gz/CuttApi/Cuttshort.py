import requests
import urllib.parse as urlparse
from urllib.parse import urlencode
import urllib
import pyperclip

class yurl():
    def __init__(self, link):
        if link.startswith("http"):
            link = link
        else:
            link = "http://" + link
        

        try:
            
            status = requests.get(link).status_code
            #print(status)
            
            if status==200 or (status>=500 and status<=1000):
                
                status1 = requests.head(link).status_code
                #print(status1)
                secpro, url = link.split("://")

                if status1 == 200 or (status1>=500 and status1<=1000) or status1==405:
                    
                    if "/?" in url:
                        try:
                            u1, u2 = url.split("/?", 1)
                            
                            link2 = "https://www." + u1 + "/?" + u2
                            if u2=="":
                                link2 = "https://www." + u1 + "/"
                            status3 = requests.get(link2).status_code
                            status4 = requests.head(link2).status_code
                            if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                link = link2
                            else:
                                
                                link2 = "http://www." + u1 + "/?" + u2
                                if u2=="":
                                    link2 = "http://www." + u1 + "/"
                                status3 = requests.get(link2).status_code
                                status4 = requests.head(link2).status_code
                                if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                    link = link2
                                else:
                                    
                                    link2 = "https://www." + u1 + "?" + u2
                                    if u2=="":
                                        link2 = "https://www." + u1
                                    status3 = requests.get(link2).status_code
                                    status4 = requests.head(link2).status_code
                                    if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                        link = link2
                                    else:
                                        
                                        link2 = "http://www." + u1 + "?" + u2
                                        if u2=="":
                                            link2 = "http://www." + u1
                                        status3 = requests.get(link2).status_code
                                        status4 = requests.head(link2).status_code
                                        if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                            link = link2
                                        else:
                                            
                                            link2 = "https://" + u1 + "/?" + u2
                                            if u2=="":
                                                link2 = "http://" + u1 + "/"
                                            status3 = requests.get(link2).status_code
                                            status4 = requests.head(link2).status_code
                                            if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                                link = link2
                                            else:
                                                
                                                link2 = "http://" + u1 + "/?" + u2
                                                if u2=="":
                                                    link2 = "http://" + u1 + "/"
                                                status3 = requests.get(link2).status_code
                                                status4 = requests.head(link2).status_code
                                                if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                                    link = link2
                                                else:
                                                    
                                                    link2 = "https://" + u1 + "?" + u2
                                                    if u2=="":
                                                        link2 = "https://" + u1
                                                    status3 = requests.get(link2).status_code
                                                    status4 = requests.head(link2).status_code
                                                    if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                                        link = link2
                                                    else:
                                                        
                                                        link2 = "http://" + u1 + "?" + u2
                                                        if u2=="":
                                                            link2 = "http://" + u1
                                                        status3 = requests.get(link2).status_code
                                                        status4 = requests.head(link2).status_code
                                                        if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                                            link = link2
                        except requests.ConnectionError as exception:
                            
                            link2 = "https://" + u1 + "/?" + u2
                            if u2=="":
                                link2 = "https://" + u1 + "/"
                            status3 = requests.get(link2).status_code
                            status4 = requests.head(link2).status_code
                            if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                link = link2
                            else:
                                
                                link2 = "http://" + u1 + "/?" + u2
                                if u2=="":
                                    link2 = "http://" + u1 + "/"
                                status3 = requests.get(link2).status_code
                                status4 = requests.head(link2).status_code
                                if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                    link = link2
                                else:
                                    
                                    link2 = "https://" + u1 + "?" + u2
                                    if u2=="":
                                        link2 = "https://" + u1
                                    status3 = requests.get(link2).status_code
                                    status4 = requests.head(link2).status_code
                                    if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                        link = link2
                                    else:
                                        
                                        link2 = "http://" + u1 + "?" + u2
                                        if u2=="":
                                            link2 = "http://" + u1
                                        status3 = requests.get(link2).status_code
                                        status4 = requests.head(link2).status_code
                                        if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                            link = link2
                    elif "?" in url:
                        print("ok")
                        try:
                            u1, u2 = url.split("?", 1)
                            
                            link2 = "https://www." + u1 + "/?" + u2
                            if u2=="":
                                link2 = "https://www." + u1 + "/"
                            status3 = requests.get(link2).status_code
                            status4 = requests.head(link2).status_code
                            if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                link = link2
                            else:
                                
                                link2 = "http://www." + u1 + "/?" + u2
                                if u2=="":
                                    link2 = "http://www." + u1 + "/"
                                status3 = requests.get(link2).status_code
                                status4 = requests.head(link2).status_code
                                if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                    link = link2
                                else:
                                    
                                    link2 = "https://www." + u1 + "?" + u2
                                    if u2=="":
                                        link2 = "https://www." + u1
                                    status3 = requests.get(link2).status_code
                                    status4 = requests.head(link2).status_code
                                    if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                        link = link2
                                    else:
                                        
                                        link2 = "http://www." + u1 + "?" + u2
                                        if u2=="":
                                            link2 = "http://www." + u1
                                        status3 = requests.get(link2).status_code
                                        status4 = requests.head(link2).status_code
                                        if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                            link = link2
                                        else:
                                            
                                            link2 = "https://" + u1 + "/?" + u2
                                            if u2=="":
                                                link2 = "http://" + u1 + "/"
                                            status3 = requests.get(link2).status_code
                                            status4 = requests.head(link2).status_code
                                            if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                                link = link2
                                            else:
                                                
                                                link2 = "http://" + u1 + "/?" + u2
                                                if u2=="":
                                                    link2 = "http://" + u1 + "/"
                                                status3 = requests.get(link2).status_code
                                                status4 = requests.head(link2).status_code
                                                if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                                    link = link2
                                                else:
                                                    
                                                    link2 = "https://" + u1 + "?" + u2
                                                    if u2=="":
                                                        link2 = "https://" + u1
                                                    status3 = requests.get(link2).status_code
                                                    status4 = requests.head(link2).status_code
                                                    if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                                        link = link2
                                                    else:
                                                        
                                                        link2 = "http://" + u1 + "?" + u2
                                                        if u2=="":
                                                            link2 = "http://" + u1
                                                        status3 = requests.get(link2).status_code
                                                        status4 = requests.head(link2).status_code
                                                        if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                                            link = link2
                        except requests.ConnectionError as exception:
                            
                            link2 = "https://" + u1 + "/?" + u2
                            if u2=="":
                                link2 = "https://" + u1 + "/"
                            status3 = requests.get(link2).status_code
                            status4 = requests.head(link2).status_code
                            if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                link = link2
                            else:
                                
                                link2 = "http://" + u1 + "/?" + u2
                                if u2=="":
                                    link2 = "http://" + u1 + "/"
                                status3 = requests.get(link2).status_code
                                status4 = requests.head(link2).status_code
                                if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                    link = link2
                                else:
                                    
                                    link2 = "https://" + u1 + "?" + u2
                                    if u2=="":
                                        link2 = "https://" + u1
                                    status3 = requests.get(link2).status_code
                                    status4 = requests.head(link2).status_code
                                    if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                        link = link2
                                    else:
                                        
                                        link2 = "http://" + u1 + "?" + u2
                                        if u2=="":
                                            link2 = "http://" + u1
                                        status3 = requests.get(link2).status_code
                                        status4 = requests.head(link2).status_code
                                        if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                            link = link2
                    elif "/?" not in link or"?" not in link:
                        try:
                            if url.endswith("/"):
                                
                                url1 = url.rstrip("/")
                                url = url1
                            
                            link2 = "https://www." + url + "/"
                            status3 = requests.get(link2).status_code
                            status4 = requests.head(link2).status_code
                            if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                link = link2
                            else:
                                
                                link2 = "http://www." + url + "/"
                                status3 = requests.get(link2).status_code
                                status4 = requests.head(link2).status_code
                                if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                    link = link2
                                else:
                                    
                                    link2 = "https://www." + url
                                    status3 = requests.get(link2).status_code
                                    status4 = requests.head(link2).status_code
                                    if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                        link = link2
                                    else:
                                        
                                        link2 = "http://" + url
                                        status3 = requests.get(link2).status_code
                                        status4 = requests.head(link2).status_code
                                        if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                            link = link2
                                        else:
                                            
                                            link2 = "https://" + url + "/"
                                            status3 = requests.get(link2).status_code
                                            status4 = requests.head(link2).status_code
                                            if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                                link = link2
                                            else:
                                                
                                                link2 = "http://" + url + "/"
                                                status3 = requests.get(link2).status_code
                                                status4 = requests.head(link2).status_code
                                                if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                                    link = link2
                                                else:
                                                    
                                                    link2 = "https://" + url
                                                    status3 = requests.get(link2).status_code
                                                    status4 = requests.head(link2).status_code
                                                    if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                                        link = link2
                                                    else:
                                                        
                                                        link2 = "https://" + url + "/"
                                                        status3 = requests.get(link2).status_code
                                                        status4 = requests.head(link2).status_code
                                                        if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                                            link = link2
                        except requests.ConnectionError as exception:
                            
                            link2 = "https://" + url + "/"
                            status3 = requests.get(link2).status_code
                            status4 = requests.head(link2).status_code
                            if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                link = link2
                            else:
                                
                                link2 = "http://" + url + "/"
                                status3 = requests.get(link2).status_code
                                status4 = requests.head(link2).status_code
                                if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                    link = link2
                                else:
                                    
                                    link2 = "https://" + url
                                    status3 = requests.get(link2).status_code
                                    status4 = requests.head(link2).status_code
                                    if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                        link = link2
                                    else:
                                        
                                        link2 = "http://" + url + "/"
                                        status3 = requests.get(link2).status_code
                                        status4 = requests.head(link2).status_code
                                        if (status3==200 and status4==200) or (status3==999 and status4==999) or (status3==200 and status4==405):
                                            link = link2
                    self.link = link
                elif status1 >= 301 and status1 <= 399:
                    
                    if "/?" in link:
                        secpro, url = link.split("://")
                        url1, url2 = url.split("/?", 1)

                        if "www" in url1:
                            
                            url3, url4 = url1.split("www.", 1)
                            link1 = "https://www." + url4 + "/?" + url2
                            if url2=="":
                                link1 = "https://www." + url4 + "/"
                            status2 = requests.head(link1).status_code
                            status3 = requests.get(link1).status_code
                            if status2 == 200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                self.link = link1
                            else:
                                
                                link1 = "http://www." + url4 + "/?" + url2
                                if url2=="":
                                    link1 = "http://www." + url4 + "/"
                                status2 = requests.head(link1).status_code
                                status3 = requests.get(link1).status_code
                                if status2 == 200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                    self.link = link1
                                else:
                                    
                                    link1 = "https://www." + url4 + "?" + url2
                                    if url2=="":
                                        link1 = "https://www." + url4
                                    status2 = requests.head(link1).status_code
                                    status3 = requests.get(link1).status_code
                                    if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                        self.link = link1
                                    else:
                                        
                                        link1 = "http://www." + url4 + "?" + url2
                                        if url2=="":
                                            link1 = "http://www." + url4
                                        status2 = requests.head(link1).status_code
                                        status3 = requests.get(link1).status_code
                                        if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                            self.link = link1
                                        else:
                                            
                                            link1 = "https://" + url4 + "/?" + url2
                                            if url2=="":
                                                link1 = "https://" + url4 + "/"
                                            status2 = requests.head(link1).status_code
                                            status3 = requests.get(link1).status_code
                                            if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                self.link = link1
                                            else:
                                                
                                                link1 = "http://" + url4 + "/?" + url2
                                                if url2=="":
                                                    link1 = "http://" + url4 + "/"
                                                status2 = requests.head(link1).status_code
                                                status3 = requests.get(link1).status_code
                                                if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                    self.link = link1
                                                else:
                                                    
                                                    link1 = "https://" + url4 + "?" + url2
                                                    if url2=="":
                                                        link1 = "https://" + url4
                                                    status2 = requests.head(link1).status_code
                                                    status3 = requests.get(link1).status_code
                                                    if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                        self.link = link1
                                                    else:
                                                        
                                                        link1 = "http://" + url4 + "?" + url2
                                                        if url2=="":
                                                            link1 = "http://" + url4
                                                        status2 = requests.head(link1).status_code
                                                        status3 = requests.get(link1).status_code
                                                        if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                            self.link = link1
                                                        else:
                                                            self.link = "The entered URL is already shortened!"

                        elif "www" not in url1:
                            try:
                                
                                link1 = "https://www." + url1 + "/?" + url2
                                if url2=="":
                                    link1 = "https://www." + url1 + "/"
                                status2 = requests.head(link1).status_code
                                status3 = requests.get(link1).status_code
                                if status2 == 200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                    self.link = link1
                                else:
                                    
                                    link1 = "http://www." + url1 + "/?" + url2
                                    if url2=="":
                                        link1 = "http://www." + url1 + "/"
                                    status2 = requests.head(link1).status_code
                                    status3 = requests.get(link1).status_code
                                    if status2 == 200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                        self.link = link1
                                    else:
                                        
                                        link1 = "https://www." + url1 + "?" + url2
                                        if url2=="":
                                            link1 = "https://www." + url1
                                        status2 = requests.head(link1).status_code
                                        status3 = requests.get(link1).status_code
                                        if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                            print("\nCompleted")
                                        else:
                                            
                                            link1 = "http://www." + url1 + "?" + url2
                                            if url2=="":
                                                link1 = "http://www." + url1
                                            status2 = requests.head(link1).status_code
                                            status3 = requests.get(link1).status_code
                                            if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                print("\nCompleted")
                                            else:
                                                
                                                link1 = "https://" + url1 + "/?" + url2
                                                if url2=="":
                                                    link1 = "https://" + url1 + "/"
                                                status2 = requests.head(link1).status_code
                                                status3 = requests.get(link1).status_code
                                                if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                    self.link = link1
                                                else:
                                                    
                                                    link1 = "http://" + url1 + "/?" + url2
                                                    if url2=="":
                                                        link1 = "http://" + url1 + "/"
                                                    status2 = requests.head(link1).status_code
                                                    status3 = requests.get(link1).status_code
                                                    if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                        self.link = link1
                                                    else:
                                                        
                                                        link1 = "https://" + url1 + "?" + url2
                                                        if url2=="":
                                                            link1 = "https://" + url1
                                                        status2 = requests.head(link1).status_code
                                                        status3 = requests.get(link1).status_code
                                                        if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                            self.link = link1
                                                        else:
                                                            
                                                            link1 = "http://" + url1 + "?" + url2
                                                            if url2=="":
                                                                link1 = "http://" + url1
                                                            status2 = requests.head(link1).status_code
                                                            status3 = requests.get(link1).status_code
                                                            if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                                self.link = link1
                                                            else:
                                                                self.link = "The entered URL is already shortened!"
                            except requests.ConnectionError as exception:
                                                
                                                link1 = "https://" + url1 + "/?" + url2
                                                if url2=="":
                                                    link1 = "https://" + url1 + "/"
                                                status2 = requests.head(link1).status_code
                                                status3 = requests.get(link1).status_code
                                                if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                    self.link = link1
                                                else:
                                                    
                                                    link1 = "http://" + url1 + "/?" + url2
                                                    if url2=="":
                                                        link1 = "http://" + url1 + "/"
                                                    status2 = requests.head(link1).status_code
                                                    status3 = requests.get(link1).status_code
                                                    if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                        self.link = link1
                                                    else:
                                                        
                                                        link1 = "https://" + url1 + "?" + url2
                                                        if url2=="":
                                                            link1 = "https://" + url1
                                                        status2 = requests.head(link1).status_code
                                                        status3 = requests.get(link1).status_code
                                                        if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                            self.link = link1
                                                        else:
                                                            
                                                            link1 = "http://" + url1 + "?" + url2
                                                            if url2=="":
                                                                link1 = "http://" + url1
                                                            status2 = requests.head(link1).status_code
                                                            status3 = requests.get(link1).status_code
                                                            if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                                self.link = link1
                                                            else:
                                                                self.link = "The entered URL is already shortened!"
                    elif "?" in link:
                        
                        secpro, url = link.split("://")
                        url1, url2 = url.split("?", 1)
                        #print(url1)

                        if "www" in url1:
                            
                            url3, url4 = url1.split("www.", 1)
                            link1 = "https://www." + url4 + "/?" + url2
                            if url2=="":
                                link1 = "https://www." + url4 + "/"
                            status2 = requests.head(link1).status_code
                            status3 = requests.get(link1).status_code
                            if status2 == 200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                self.link = link1
                            else:
                                
                                link1 = "http://www." + url4 + "/?" + url2
                                if url2=="":
                                    link1 = "http://www." + url4 + "/"
                                status2 = requests.head(link1).status_code
                                status3 = requests.get(link1).status_code
                                if status2 == 200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                    self.link = link1
                                else:
                                    
                                    link1 = "https://www." + url4 + "?" + url2
                                    if url2=="":
                                        link1 = "https://www." + url4
                                    status2 = requests.head(link1).status_code
                                    status3 = requests.get(link1).status_code
                                    if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                        print("\nCompleted")
                                    else:
                                        
                                        link1 = "http://www." + url4 + "?" + url2
                                        if url2=="":
                                            link1 = "http://www." + url4
                                        status2 = requests.head(link1).status_code
                                        status3 = requests.get(link1).status_code
                                        if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                            print("\nCompleted")
                                        else:
                                            
                                            link1 = "https://" + url4 + "/?" + url2
                                            if url2=="":
                                                link1 = "https://" + url4 + "/"
                                            status2 = requests.head(link1).status_code
                                            status3 = requests.get(link1).status_code
                                            if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                self.link = link1
                                            else:
                                                
                                                link1 = "http://" + url4 + "/?" + url2
                                                if url2=="":
                                                    link1 = "http://" + url4 + "/"
                                                status2 = requests.head(link1).status_code
                                                status3 = requests.get(link1).status_code
                                                if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                    self.link = link1
                                                else:
                                                    
                                                    link1 = "https://" + url4 + "?" + url2
                                                    if url2=="":
                                                        link1 = "https://" + url4
                                                    status2 = requests.head(link1).status_code
                                                    status3 = requests.get(link1).status_code
                                                    if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                        self.link = link1
                                                    else:
                                                        
                                                        link1 = "http://" + url4 + "?" + url2
                                                        if url2=="":
                                                            link1 = "http://" + url4
                                                        status2 = requests.head(link1).status_code
                                                        status3 = requests.get(link1).status_code
                                                        if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                            self.link = link1
                                                        else:
                                                            self.link = "The entered URL is already shortened!"

                        elif "www" not in url1:
                            #url3, url4 = url1.split("www.")
                            try:
                                
                                link1 = "https://www." + url1 + "/?" + url2
                                if url2=="":
                                    link1 = "https://www." + url1 + "/"
                                status2 = requests.head(link1).status_code
                                status3 = requests.get(link1).status_code
                                if status2 == 200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                    self.link = link1
                                else:
                                    
                                    link1 = "http://www." + url1 + "/?" + url2
                                    if url2=="":
                                        link1 = "http://www." + url1 + "/"
                                    status2 = requests.head(link1).status_code
                                    status3 = requests.get(link1).status_code
                                    if status2 == 200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                        self.link = link1
                                    else:
                                        
                                        link1 = "https://www." + url1 + "?" + url2
                                        if url2=="":
                                            link1 = "https://www." + url1
                                        status2 = requests.head(link1).status_code
                                        status3 = requests.get(link1).status_code
                                        if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                            self.link = link1
                                        else:
                                            
                                            link1 = "http://www." + url1 + "?" + url2
                                            if url2=="":
                                                link1 = "http://www." + url1
                                            status2 = requests.head(link1).status_code
                                            status3 = requests.get(link1).status_code
                                            if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                print("\nCompleted")
                                            else:
                                                
                                                link1 = "https://" + url1 + "/?" + url2
                                                if url2=="":
                                                    link1 = "https://" + url1 + "/"
                                                status2 = requests.head(link1).status_code
                                                status3 = requests.get(link1).status_code
                                                if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                    self.link = link1
                                                else:
                                                    
                                                    link1 = "http://" + url1 + "/?" + url2
                                                    if url2=="":
                                                        link1 = "http://" + url1 + "/"
                                                    status2 = requests.head(link1).status_code
                                                    status3 = requests.get(link1).status_code
                                                    if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                        self.link = link1
                                                    else:
                                                        
                                                        link1 = "https://" + url1 + "?" + url2
                                                        if url2=="":
                                                            link1 = "https://" + url1
                                                        status2 = requests.head(link1).status_code
                                                        status3 = requests.get(link1).status_code
                                                        if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                            self.link = link1
                                                        else:
                                                            
                                                            link1 = "http://" + url1 + "?" + url2
                                                            if url2=="":
                                                                link1 = "http://" + url1
                                                            status2 = requests.head(link1).status_code
                                                            status3 = requests.get(link1).status_code
                                                            if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                                self.link = link1
                                                            else:
                                                                self.link = "The entered URL is already shortened!"
                            except requests.ConnectionError as exception:
                                                
                                                link1 = "https://" + url1 + "/?" + url2
                                                if url2=="":
                                                    link1 = "https://" + url1 + "/"
                                                status2 = requests.head(link1).status_code
                                                status3 = requests.get(link1).status_code
                                                if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                    self.link = link1
                                                else:
                                                    
                                                    link1 = "http://" + url1 + "/?" + url2
                                                    if url2=="":
                                                        link1 = "http://" + url1 + "/"
                                                    status2 = requests.head(link1).status_code
                                                    status3 = requests.get(link1).status_code
                                                    if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                        self.link = link1
                                                    else:
                                                        
                                                        link1 = "https://" + url1 + "?" + url2
                                                        if url2=="":
                                                            link1 = "https://" + url1
                                                        status2 = requests.head(link1).status_code
                                                        status3 = requests.get(link1).status_code
                                                        if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                            self.link = link1
                                                        else:
                                                            
                                                            link1 = "http://" + url1 + "?" + url2
                                                            if url2=="":
                                                                link1 = "http://" + url1
                                                            status2 = requests.head(link1).status_code
                                                            status3 = requests.get(link1).status_code
                                                            if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                                self.link = link1
                                                            else:
                                                                self.link = "The entered URL is already shortened!"
                    elif "/?" not in link or "?" not in link:
                        
                        if link.endswith("/"):
                            link1 = link.rstrip("/")
                            link = link1
                        secpro, url = link.split("://")

                        if "www" in url:
                            
                            url3, url4 = url.split("www.", 1)
                            link1 = "https://www." + url4 + "/"
                            status2 = requests.head(link1).status_code
                            status3 = requests.get(link1).status_code
                            if status2 == 200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                self.link = link1
                            else:
                                
                                link1 = "http://www." + url4 + "/"
                                status2 = requests.head(link1).status_code
                                status3 = requests.get(link1).status_code
                                if status2 == 200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                    self.link = link1
                                else:
                                    
                                    link1 = "https://www." + url4
                                    status2 = requests.head(link1).status_code
                                    status3 = requests.get(link1).status_code
                                    if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                        self.link = link1
                                    else:
                                        
                                        link1 = "http://www." + url4
                                        status2 = requests.head(link1).status_code
                                        status3 = requests.get(link1).status_code
                                        if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                            print("\nCompleted")
                                        else:
                                            
                                            link1 = "https://" + url4 + "/"
                                            status2 = requests.head(link1).status_code
                                            status3 = requests.get(link1).status_code
                                            if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                self.link = link1
                                            else:
                                                
                                                link1 = "http://" + url4 + "/"
                                                status2 = requests.head(link1).status_code
                                                status3 = requests.get(link1).status_code
                                                if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                    self.link = link1
                                                else:
                                                    
                                                    link1 = "https://" + url4
                                                    status2 = requests.head(link1).status_code
                                                    status3 = requests.get(link1).status_code
                                                    if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                        self.link = link1
                                                    else:
                                                        
                                                        link1 = "http://" + url4
                                                        status2 = requests.head(link1).status_code
                                                        status3 = requests.get(link1).status_code
                                                        if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                            self.link = link1
                                                        else:
                                                            self.link = "The entered URL is already shortened!"

                        elif "www" not in url:
                            #url3, url4 = url1.split("www.")
                            try:
                                
                                link1 = "https://www." + url + "/"
                                status2 = requests.head(link1).status_code
                                status3 = requests.get(link1).status_code
                                if status2 == 200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                    self.link = link1
                                else:
                                    
                                    link1 = "http://www." + url + "/"
                                    status2 = requests.head(link1).status_code
                                    status3 = requests.get(link1).status_code
                                    if status2 == 200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                        self.link = link1
                                    else:
                                        
                                        link1 = "https://www." + url
                                        status2 = requests.head(link1).status_code
                                        status3 = requests.get(link1).status_code
                                        if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                            self.link = link1
                                        else:
                                            
                                            link1 = "http://www." + url
                                            status2 = requests.head(link1).status_code
                                            status3 = requests.get(link1).status_code
                                            if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                print("\nCompleted")
                                            else:
                                                
                                                link1 = "https://" + url + "/"
                                                status2 = requests.head(link1).status_code
                                                status3 = requests.get(link1).status_code
                                                if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                    self.link = link1
                                                else:
                                                    
                                                    link1 = "http://" + url + "/"
                                                    status2 = requests.head(link1).status_code
                                                    status3 = requests.get(link1).status_code
                                                    if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                        self.link = link1
                                                    else:
                                                        
                                                        link1 = "https://" + url
                                                        status2 = requests.head(link1).status_code
                                                        status3 = requests.get(link1).status_code
                                                        if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                            self.link = link1
                                                        else:
                                                            
                                                            link1 = "http://" + url
                                                            status2 = requests.head(link1).status_code
                                                            status3 = requests.get(link1).status_code
                                                            if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                                self.link = link1
                                                            else:
                                                                self.link = "The entered URL is already shortened!"
                            except requests.ConnectionError as exception:
                                                
                                                link1 = "https://" + url + "/"
                                                status2 = requests.head(link1).status_code
                                                status3 = requests.get(link1).status_code
                                                if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                    self.link = link1
                                                else:
                                                    
                                                    link1 = "http://" + url + "/"
                                                    status2 = requests.head(link1).status_code
                                                    status3 = requests.get(link1).status_code
                                                    if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                        self.link = link1
                                                    else:
                                                        
                                                        link1 = "https://" + url
                                                        status2 = requests.head(link1).status_code
                                                        status3 = requests.get(link1).status_code
                                                        if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                            self.link = link1
                                                        else:
                                                            
                                                            link1 = "http://" + url
                                                            status2 = requests.head(link1).status_code
                                                            status3 = requests.get(link1).status_code
                                                            if status2==200 or (status2==405 and status3 == 200) or ((status2>=302 and status2<=307) and status3 == 200):
                                                                self.link = link1
                                                            else:
                                                                self.link = "The entered URL is already shortened!"
                link = self.link
            else:
                self.link = "The entered URL does not exist on the Internet"
                link = self.link
        except requests.ConnectionError as exception:
            self.link = "The entered URL does not exist on the Internet"
            link = self.link

class Cuttshort:
    def __init__(self, api_key):
        while True:
            try:
                ak = api_key
                #if api_key.upper() == "UD":
                    #ak = "b9fbdde0736d2ca0ad6b910bd6e60dea"
                #else:
                    #ak = api_key
                api_url = 'http://cutt.ly/api/api.php?key={}'.format(ak)
                data = requests.get(api_url).json()
                if data["auth"]==True:
                    while True:
                        try:
                            link = input("Enter the link to be shortened: ")
                            params = {'utm_source':'apidevthe'}
                            a = yurl(link).link
                            url_parts = list(urlparse.urlparse(a))
                            query = dict(urlparse.parse_qsl(url_parts[4]))
                            query.update(params)

                            url_parts[4] = urlencode(query)
                            url1 = urlparse.urlunparse(url_parts)
                            url = urllib.parse.quote(url1)
                            if a != "The entered URL does not exist on the Internet" and a != "The entered URL is already shortened":
                                while True:
                                        name = input("Would you like to give a name? : ")
                                        if name.upper()=="YES":
                                            while True:
                                                name1 = input("Enter name: ")
                                                api_url1 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url, name1)
                                                data1 = requests.get(api_url1).json()["url"]
                                                if data1["status"] == 7:
                                                    shortened_url1 = data1["shortLink"]
                                                    print("Shortened URL: ", shortened_url1)
                                                    pyperclip.copy(shortened_url1)
                                                    break
                                                elif data1["status"] == 5:
                                                    print("Please re-enter the name as the name contains invalid characters!")
                                                else:
                                                    print("Please re-enter the name as the entered name already exists!")
                                                    continue
                                            break
                                        elif name.upper()=="NO":
                                            api_url2 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url)
                                            data2 = requests.get(api_url2).json()["url"]
                                            if data2["status"] == 7:
                                                shortened_url2 = data2["shortLink"]
                                                print("Shortened URL: ", shortened_url2)
                                                pyperclip.copy(shortened_url2)
                                                break
                                        else:
                                            print("Please enter either Yes/No!")
                            else:
                                print(a)
                        except requests.ConnectionError as exception:
                            
                            print("URL does not exist on the Internet")
                            break
                else:
                    print("The entered API key does not exist. Please retry!")
                    break
            except requests.JSONDecodeError as exception:
                print("There is an issue with the API. Please try after a few seconds")
                break


if __name__ == "__main__":
    import stdiomask
    api_key = stdiomask.getpass("Enter your Cuttly api key: ")
    short = Cuttshort(api_key)