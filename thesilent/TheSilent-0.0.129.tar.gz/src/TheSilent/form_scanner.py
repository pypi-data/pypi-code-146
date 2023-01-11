from TheSilent.return_user_agent import *

import re
import requests

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

#scans for forms
def form_scanner(url, secure = True, parse = "forms"):
    if secure == True:
        my_secure = "https://"

    if secure == False:
        my_secure = "http://"

    url = my_secure + url

    try:
        result = web_session.get(url, verify = False, headers = user_agent, timeout = (5, 30)).text

        try:
            if parse == "forms":
                forms = re.findall("<form[\n\w\S\s]+?form>", result)
                return forms

            if parse == "input":
                input_form = re.findall("<input.+?>", result)
                return input_form

        except UnicodeDecodeError:
            return []

    except:
        return []
