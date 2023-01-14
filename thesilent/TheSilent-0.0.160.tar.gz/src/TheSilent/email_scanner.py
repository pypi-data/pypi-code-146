from TheSilent.clear import *
from TheSilent.return_user_agent import *

import re
import requests

cyan = "\033[1;36m"
red = "\033[1;31m"

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

#scans for emails on a website
def email_scanner(url, secure = True):
    if secure == True:
        my_secure = "https://"

    if secure == False:
        my_secure = "http://"

    my_url = my_secure + url

    tracker = 0

    email_list = []
    website_list = []
    website_list.append(my_url)

    clear()

    while True:
        length_count = 0

        website_list = list(dict.fromkeys(website_list))
            
        try:
            stream_boolean = web_session.get(website_list[tracker], verify = False, headers = user_agent, timeout = (5, 30), stream = True)

            for i in stream_boolean.iter_lines():
                length_count += len(i)

            if length_count > 25000000:
                print(red + "too long" + ": " + str(website_list[tracker]))
                website_list.pop(tracker)

            if length_count <= 25000000 :
                status = web_session.get(website_list[tracker], verify = False, headers = user_agent, timeout = (5, 30)).status_code

                if status == 200:
                    print(cyan + website_list[tracker])
                    my_request = web_session.get(website_list[tracker], verify = False, headers = user_agent, timeout = (5, 30)).text

                    if len(my_request) <= 25000000:
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
                        href = re.findall("href=[\"\']\S+?[\'\"]", href)
                        href = list(dict.fromkeys(href))
                        for i in href:
                            try:
                                result = re.split("[%\(\)<>\[\],\{\};�|]", i)
                                result = result[0]

                            except:
                                result = i
                            
                            result = re.sub("[\\\"\';]|href=", "", i)

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
                        action = re.findall("action=[\"\']\S+?[\'\"]", action)
                        action = list(dict.fromkeys(action))
                        
                        for i in action:
                            try:
                                result = re.split("[%\(\)<>\[\],\{\};�|]", i)
                                result = result[0]

                            except:
                                result = i
                                
                            result = re.sub("[\\\"\';]|action=", "", i)

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
                        src = re.findall("src=[\"\']\S+?[\'\"]", src)
                        src = list(dict.fromkeys(src))

                        for i in src:
                            try:
                                result = re.split("[%\(\)<>\[\],\{\};�|]", i)
                                result = result[0]

                            except:
                                result = i
                                
                            result = re.sub("[\\\"\';]|src=", "", i)
                            
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

        except IndexError:
            break

        except:
            print(red + "ERROR: " + str(website_list[tracker]))
            website_list.pop(tracker)

        email = re.findall("[a-z0-9]+@[a-z0-9]+[.][a-z]+", my_request)

        for emails in email:
            email_list.append(emails)

    clear()



    email_list = list(dict.fromkeys(email_list))
    email_list.sort()

    return email_list
