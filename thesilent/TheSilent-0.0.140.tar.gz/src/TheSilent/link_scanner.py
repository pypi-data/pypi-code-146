from TheSilent.clear import *
from TheSilent.return_user_agent import *

import re
import requests

cyan = "\033[1;36m"
red = "\033[1;31m"

tor_proxy = {"https": "socks5h://localhost:9050", "http": "socks5h://localhost:9050"}

#create html sessions object
web_session = requests.Session()

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

#crawls a website looking for links
def link_scanner(url, secure = True, tor = False, my_file = " "):
    if secure == True:
        my_secure = "https://"

    if secure == False:
        my_secure = "http://"

    my_url = my_secure + url
    tracker = 0

    website_list = []
    website_list.append(my_url)

    clear()

    while True:
        length_count = 0

        website_list = list(dict.fromkeys(website_list))
        
        try:
            my_filter = re.findall("(https://|http://)(.+?/)", website_list[tracker])
            find_my = re.search(url, str(my_filter))

            if find_my or website_list[tracker] == my_url:
                if tor == True:
                    stream_boolean = web_session.get(website_list[tracker], verify = False, headers = user_agent, proxies = tor_proxy, timeout = (5, 30), stream = True)

                else:
                    stream_boolean = web_session.get(website_list[tracker], verify = False, headers = user_agent, timeout = (5, 30), stream = True)

                for i in stream_boolean.iter_lines():
                    length_count += len(i)

                if length_count > 100000000:
                    print(red + "too long" + ": " + str(website_list[tracker]))
                    website_list.pop(tracker)

                if length_count <= 100000000:
                    if tor == True:
                        status = web_session.get(website_list[tracker], verify = False, headers = user_agent, proxies = tor_proxy, timeout = (5, 30)).status_code

                    if tor == False:
                        status = web_session.get(website_list[tracker], verify = False, headers = user_agent, timeout = (5, 30)).status_code

                    if status == 200:
                        print(cyan + website_list[tracker])

                        if tor == True:
                            my_request = web_session.get(website_list[tracker], verify = False, headers = user_agent, proxies = tor_proxy, timeout = (5, 30)).text

                        if tor == False:
                            my_request = web_session.get(website_list[tracker], verify = False, headers = user_agent, timeout = (5, 30)).text

                        if len(my_request) <= 100000000:
                            tracker += 1

                            #urls
                            website = re.findall("http://|https://\S+", my_request)
                            website = list(dict.fromkeys(website))

                            for i in website:
                                try:
                                    result = re.split("[%\(\)<>\[\],\{\};�|]", i)
                                    result = result[0]
                                    result = re.sub("[\"\']", "", result)

                                except:
                                    result = i
                                    
                                if url in i:
                                    website_list.append(re.sub("[\\\"\']", "", result))

                            #href
                            href = re.sub(" ", "", my_request)
                            href = re.findall("href\s*=\s*[\"\']\S+?[\'\"]", href)
                            href = list(dict.fromkeys(href))
                            for i in href:
                                try:
                                    i = i.clean(" ", "")
                                    result = re.split("[%\(\)<>\[\],\{\};�|]", i)
                                    result = result[0]

                                except:
                                    result = i
                                
                                result = re.sub("[\\\"\';=\s]|href", "", i)

                                if result.startswith("http"):
                                    if url in result:
                                        website_list.append(result)

                                if result.startswith("http") == False and result[0] != "/":
                                    result = re.sub(url, "", result)
                                    result = re.sub("www", "", result)
                                    website_list.append(my_url + "/" + result)

                                if result.startswith("http") == False and result[0] == "/":
                                    result = re.sub(url, "", result)
                                    result = re.sub("www", "", result)
                                    website_list.append(my_url + result)

                            #action
                            action = re.sub(" ", "", my_request)
                            action = re.findall("action\s*=\s*[\"\']\S+?[\'\"]", action)
                            action = list(dict.fromkeys(action))
                            
                            for i in action:
                                try:
                                    i = i.clean(" ", "")
                                    result = re.split("[%\(\)<>\[\],\{\};�|]", i)
                                    result = result[0]

                                except:
                                    result = i
                                    
                                result = re.sub("[\\\"\';=\s]|action", "", i)

                                if result.startswith("http"):
                                    if url in result:
                                        website_list.append(result)

                                if result.startswith("http") == False and result[0] != "/":
                                    result = re.sub(url, "", result)
                                    result = re.sub("www", "", result)
                                    website_list.append(my_url + "/" + result)

                                if result.startswith("http") == False and result[0] == "/":
                                    result = re.sub(url, "", result)
                                    result = re.sub("www", "", result)
                                    website_list.append(my_url + result)

                            #src
                            src = re.sub(" ", "", my_request)
                            src = re.findall("src\s*=\s*[\"\']\S+?[\'\"]", src)
                            src = list(dict.fromkeys(src))

                            for i in src:
                                try:
                                    i = i.clean(" ", "")
                                    result = re.split("[%\(\)<>\[\],\{\};�|]", i)
                                    result = result[0]

                                except:
                                    result = i
                                    
                                result = re.sub("[\\\"\';=\s]|src", "", i)
                                
                                if result.startswith("http"):
                                    if url in result:
                                        website_list.append(result)

                                if result.startswith("http") == False and result[0] != "/":
                                    result = re.sub(url, "", result)
                                    result = re.sub("www", "", result)
                                    website_list.append(my_url + "/" + result)

                                if result.startswith("http") == False and result[0] == "/":
                                    result = re.sub(url, "", result)
                                    result = re.sub("www", "", result)
                                    website_list.append(my_url + result)

                            #slash
                            slash = re.findall("[\'|\"]/\S+[\"|\']", my_request)

                            for i in slash:
                                my_search = re.search("http|\.com|\.edu|\.net|\.org|\.tv|www|http", i)

                                if not my_search:
                                    result = re.sub("[\"\']", "", i)
                                    result = re.split("[%\(\)<>\[\],\{\};�|]", result)
                                    result = result[0]
                                    website_list.append(my_url + result)

                    else:
                        print(red + str(status) + ": " + str(website_list[tracker]))
                        website_list.pop(tracker)

            if not find_my:
                website_list.pop(tracker)

        except IndexError:
            break

        except:
            print(red + "ERROR: " + str(website_list[tracker]))
            website_list.pop(tracker)


    website_list = list(dict.fromkeys(website_list))
    website_list.sort()

    clear()

    if my_file != " ":
        with open(my_file, "a") as file:
            for i in website_list:
                file.write(i + "\n")

    return website_list
