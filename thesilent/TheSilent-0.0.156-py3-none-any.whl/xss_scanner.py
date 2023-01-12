from TheSilent.clear import *
from TheSilent.form_scanner import *
from TheSilent.link_scanner import *
from TheSilent.return_user_agent import *

import hashlib
import requests

cyan = "\033[1;36m"
red = "\033[1;31m"

#create html sessions object
web_session = requests.Session()

tor_proxy = {"https": "socks5h://localhost:9050", "http": "socks5h://localhost:9050"}

#fake user agent
user_agent = {"User-Agent" : return_user_agent()}

#increased security
requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"

#increased security
try:
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"

except AttributeError:
    pass

def return_mal_payloads():
    #malicious script
    mal_payloads = []

    my_random = random.randint(0, 1000000000)
    md5 = hashlib.md5(str(my_random).encode("utf8")).hexdigest()
    mal_payloads.append("toString(" + str(md5) + ")")

    my_random = random.randint(0, 1000000000)
    md5 = hashlib.md5(str(my_random).encode("utf8")).hexdigest()
    mal_payloads.append('<scipt>alert("' + str(md5) + '")</script>')

    my_random = random.randint(0, 1000000000)
    md5_1 = hashlib.md5(str(my_random).encode("utf8")).hexdigest()
    md5_2 = hashlib.md5(str(my_random).encode("utf8")).hexdigest()
    mal_payloads.append(str(md5_1) + "=" + str(md5_2))

    my_random = random.randint(0, 1000000000)
    md5 = hashlib.md5(str(my_random).encode("utf8")).hexdigest()
    mal_payloads.append("getElementById(" + str(md5) + ")")

    my_random = random.randint(0, 1000000000)
    md5 = hashlib.md5(str(my_random).encode("utf8")).hexdigest()
    mal_payloads.append("innerHTML=" + str(md5))

    my_random = random.randint(0, 1000000000)
    md5 = hashlib.md5(str(my_random).encode("utf8")).hexdigest()
    mal_payloads.append("src=" + str(md5))

    my_random = random.randint(0, 1000000000)
    md5 = hashlib.md5(str(my_random).encode("utf8")).hexdigest()
    mal_payloads.append("console.log(" + str(md5) + ")")

    my_random = random.randint(0, 1000000000)
    md5 = hashlib.md5(str(my_random).encode("utf8")).hexdigest()
    mal_payloads.append("document.write(" + str(md5) + ")")

    my_random = random.randint(0, 1000000000)
    md5 = hashlib.md5(str(my_random).encode("utf8")).hexdigest()
    mal_payloads.append("appendChild(" + str(md5) + ")")

    my_random = random.randint(0, 1000000000)
    md5 = hashlib.md5(str(my_random).encode("utf8")).hexdigest()
    mal_payloads.append("document.createTextNode(" + str(md5) + ")")

    return mal_payloads

#scans for xss
def xss_scanner(url, secure = True, tor = False, my_file = " ",):
    if secure == True:
        my_secure = "https://"

    if secure == False:
        my_secure = "http://"
        
    my_list = []
    
    clear()

    mal_payloads = return_mal_payloads()

    links = my_secure + url

    #crawl
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
        mal_payloads = return_mal_payloads()
        
        try:
            for mal_script in mal_payloads:
                if links.endswith("/"):
                    my_url = links + mal_script

                if not links.endswith("/"):
                    my_url = links + "/" + mal_script

                print(cyan + "checking: " + str(my_url)) 

                if tor == True:
                    result = web_session.get(my_url, verify = False, headers = user_agent, proxies = tor_proxy, timeout = (5, 30))
                    
                if tor == False:
                    result = web_session.get(my_url, verify = False, headers = user_agent, timeout = (5, 30))

                if result.status_code == 401 or result.status_code == 403 or result.status_code == 405:
                    print(red + "firewall detected")

                if result.status_code >= 200 and result.status_code < 300:
                    if mal_script in result.text and "404" not in result.text:
                        print(cyan + "true: " + my_url)
                        my_list.append(my_url)

        except:
            continue
        
        print(cyan + "checking: " + str(links) + " (user agent)")  

        try:
            for mal_script in mal_payloads:
                user_agent_moded = {"User-Agent" : return_user_agent(), mal_script: mal_script}

                if tor == True:
                    result = web_session.get(links, verify = False, headers = user_agent_moded, proxies = tor_proxy, timeout = (5, 30))

                if tor == False:
                    result = web_session.get(links, verify = False, headers = user_agent_moded, timeout = (5, 30))
                
                if result.status_code == 401 or result.status_code == 403 or result.status_code == 405:
                    print(red + "firewall detected")

                if result.status_code >= 200 and result.status_code < 300:
                    if mal_script in result.text and "404" not in result.text:
                        print(cyan + "true: " + links + " (user agent) " + mal_script)
                        my_list.append(links + " (user agent) " + mal_script)

        except:
            continue

        

        print(cyan + "checking: " + str(links) + " (cookie)")  

        try:
            for mal_script in mal_payloads:
                mal_cookie = {mal_script: mal_script}

                if tor == True:
                    result = web_session.get(links, verify = False, headers = user_agent, cookies = mal_cookie, proxies = tor_proxy, timeout = (5, 30))

                if tor == False:
                    result = web_session.get(links, verify = False, headers = user_agent, cookies = mal_cookie, timeout = (5, 30))
                
                if result.status_code == 401 or result.status_code == 403 or result.status_code == 405:
                    print(red + "firewall detected")

                if result.status_code >= 200 and result.status_code < 300:
                    if mal_script in result.text and "404" not in result.text:
                        print(cyan + "true: " + links + " (cookie) " + mal_script)
                        my_list.append(links + " (cookie) " + mal_script)

        except:
            continue

        try:
            print(cyan + "checking for forms on: " + links)
            clean = links.replace("http://", "")
            clean = clean.replace("https://", "")
            form_input = form_scanner(clean, secure, parse = "input")

            for i in form_input:
                for mal_script in mal_payloads:
                    name = str(re.findall("name.+\".+\"", i)).split("\"")
                    mal_dict = {name[1] : mal_script}

                    print(cyan + "checking: " + str(links) + " " + str(mal_dict))

                    if tor == True:
                        get = web_session.get(links, params = mal_dict, verify = False, headers = user_agent, proxies = tor_proxy, timeout = (5, 30))
                        post = web_session.post(links, data = mal_dict, verify = False, headers = user_agent, proxies = tor_proxy, timeout = (5, 30))

                    if tor == False:
                        get = web_session.get(links, params = mal_dict, verify = False, headers = user_agent, timeout = (5, 30))
                        post = web_session.post(links, data = mal_dict, verify = False, headers = user_agent, timeout = (5, 30))

                    if get.status_code == 401 or get.status_code == 403 or get.status_code == 405:
                        print(red + "firewall detected")

                    if get.status_code >= 200 and get.status_code < 300:
                        if mal_script in get.text and "404" not in get.text:
                            print(cyan + "true: " + str(links) + " " + str(mal_dict))
                            my_list.append(str(links) + " " + str(mal_dict))

                    if post.status_code == 401 or post.status_code == 403 or post.status_code == 405:
                        print(red + "firewall detected")

                    if post.status_code >= 200 and post.status_code < 300:
                        if mal_script in post.text and "404" not in post.text:
                            print(cyan + "true: " + str(links) + " " + str(mal_dict))
                            my_list.append(str(links) + " " + str(mal_dict))

        except:
            continue

    clear()

    my_list = list(dict.fromkeys(my_list))
    my_list.sort()

    return my_list
