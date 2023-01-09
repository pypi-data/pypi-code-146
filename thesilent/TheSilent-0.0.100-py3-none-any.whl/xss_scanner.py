from TheSilent.clear import *
from TheSilent.link_scanner import *

import requests

red = "\033[1;31m"

#create html sessions object
web_session = requests.Session()

tor_proxy = {"https": "socks5h://localhost:9050", "http": "socks5h://localhost:9050"}

#fake user agent
user_agent = {"User-Agent" : "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}

#increased security
requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"

#increased security
try:
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"

except AttributeError:
    pass

#scans for xss
def xss_scanner(url, secure = True, tor = False, my_file = " ",):
    if secure == True:
        my_secure = "https://"

    if secure == False:
        my_secure = "http://"

    cyan = "\033[1;36m"
        
    my_list = []
    
    #malicious script
    mal_payloads = ['<scipt>alert("TheSilent")</script>', 'toString(TheSilent)', 'TheSilent=TheSilent', 'getElementById(TheSilent)', "innerHTML=TheSilent", "src=TheSilent", 'console.log("TheSilent")', "document.write(TheSilent)", "window.print()", "appendChild(TheSilent)", "document.createTextNode(TheSilent)"]
    
    clear()

    my_result = []

    if my_file == " ":
        my_result = link_scanner(url, secure, tor)

    if my_file != " ":
        with open(my_file, "r", errors = "ignore") as file:
            for i in file:
                clean = i.replace("\n", "")
                my_result.append(clean)

    clear()

    for links in my_result:
        try:
            for mal_script in mal_payloads:
                if links.endswith("/"):
                    my_url = links + mal_script

                if not links.endswith("/"):
                    my_url = links + "/" + mal_script

                print(red + "checking: " + str(my_url)) 

                if tor == True:
                    result = web_session.get(my_url, verify = False, headers = user_agent, proxies = tor_proxy, timeout = (5, 30))
                    
                else:
                    result = web_session.get(my_url, verify = False, headers = user_agent, timeout = (5, 30))

                if result.status_code == 401 or result.status_code == 403 or result.status_code == 405:
                    print(cyan + "firewall detected")

                if result.status_code >= 200 and result.status_code < 300:
                    if mal_script in result.text and "404" not in result.text:
                        print(red + "true: " + my_url)
                        my_list.append(my_url)

        except:
            continue
        
        print(red + "checking: " + str(links) + " (user agent)")  

        try:
            for mal_script in mal_payloads:
                user_agent_moded = {"User-Agent" : "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36", mal_script: mal_script}

                if tor == True:
                    result = web_session.get(links, verify = False, headers = user_agent_moded, proxies = tor_proxy, timeout = (5, 30))

                else:
                    result = web_session.get(links, verify = False, headers = user_agent_moded, timeout = (5, 30))
                
                if result.status_code == 401 or result.status_code == 403 or result.status_code == 405:
                    print(cyan + "firewall detected")

                if result.status_code >= 200 and result.status_code < 300:
                    if mal_script in result.text and "404" not in result.text:
                        print(red + "true: " + links + " (user agent) " + mal_script)
                        my_list.append(links + " (user agent) " + mal_script)

        except:
            continue

        

        print(red + "checking: " + str(links) + " (cookie)")  

        try:
            for mal_script in mal_payloads:
                mal_cookie = {mal_script: mal_script}

                if tor == True:
                    result = web_session.get(links, verify = False, headers = user_agent, cookies = mal_cookie, proxies = tor_proxy, timeout = (5, 30))

                else:
                    result = web_session.get(links, verify = False, headers = user_agent, cookies = mal_cookie, timeout = (5, 30))
                
                if result.status_code == 401 or result.status_code == 403 or result.status_code == 405:
                    print(cyan + "firewall detected")

                if result.status_code >= 200 and result.status_code < 300:
                    if mal_script in result.text and "404" not in result.text:
                        print(red + "true: " + links + " (cookie) " + mal_script)
                        my_list.append(links + " (cookie) " + mal_script)

        except:
            continue

        try:
            print("checking for forms on: " + links)
            clean = links.replace("http://", "")
            clean = clean.replace("https://", "")
            form_input = form_scanner(clean, secure, parse = "input")

            for i in form_input:
                for mal_script in mal_payloads:
                    name = str(re.findall("name.+\".+\"", i)).split("\"")
                    mal_dict = {name[1] : mal_script}

                    print(red + "checking: " + str(links) + " " + str(mal_dict))

                    if tor == True:
                        get = web_session.get(links, params = mal_dict, verify = False, headers = user_agent, proxies = tor_proxy, timeout = (5, 30))
                        post = web_session.post(links, data = mal_dict, verify = False, headers = user_agent, proxies = tor_proxy, timeout = (5, 30))

                    else:
                        get = web_session.get(links, params = mal_dict, verify = False, headers = user_agent, timeout = (5, 30))
                        post = web_session.post(links, data = mal_dict, verify = False, headers = user_agent, timeout = (5, 30))

                    if get.status_code == 401 or get.status_code == 403 or get.status_code == 405:
                        print(cyan + "firewall detected")

                    if get.status_code >= 200 and get.status_code < 300:
                        if mal_script in get.text and "404" not in get.text:
                            print(red + "true: " + str(links) + " " + str(mal_dict))
                            my_list.append(str(links) + " " + str(mal_dict))

                    if post.status_code == 401 or post.status_code == 403 or post.status_code == 405:
                        print(cyan + "firewall detected")

                    if post.status_code >= 200 and post.status_code < 300:
                        if mal_script in post.text and "404" not in post.text:
                            print(red + "true: " + str(links) + " " + str(mal_dict))
                            my_list.append(str(links) + " " + str(mal_dict))

        except:
            continue

    my_list = list(dict.fromkeys(my_list))
    my_list.sort()

    clear()

    my_list = list(dict.fromkeys(my_list))
    my_list.sort()

    return my_list
