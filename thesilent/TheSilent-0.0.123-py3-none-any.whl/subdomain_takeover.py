from TheSilent.subdomain_scanner import *
from TheSilent.return_user_agent import *

import requests

cyan = "\033[1;36m"

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

#scans for subdomain takeovers
def subdomain_takeover(url, secure = True, my_file = " "):
    result = subdomain_scanner(url, secure, my_file = my_file)

    clear()

    vuln_list = []

    if secure == True:
        my_secure = "https://"

    if secure == False:
        my_secure = "http://"
    
    for i in result:
        my_url = my_secure + str(i) + str(url)

        print(cyan + "checking: " + my_url)

        try:
            my_request = web_session.get(my_url, verify = False, headers = user_agent, timeout = (5, 30)).status_code

            if my_request == 404:
                print(True)
                vuln_list.append(my_url)

            else:
                print(cyan + "False")

        except:
            print(cyan + "False")

    clear()

    return vuln_list
