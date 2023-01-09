from TheSilent.link_scanner import *

import re

red = "\033[1;31m"

#create html sessions object
web_session = requests.Session()

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

#scans for subdomains
def subdomain_scanner(url, secure = True, my_file = " "):
    domain_list = []

    website = []

    if my_file == " ":
        website = link_scanner(url, secure)

    if my_file != " ":
        with open(my_file, "r", errors = "ignore") as file:
            for i in file:
                clean = i.replace("\n", "")
                website.append(clean)

    clear()

    for i in website:
        domain = re.findall("(https://?|http://?)(\S+)" + "." + url, i)

        try:
            result = domain[0][1]
            domain_list.append(result)

        except:
            continue
        
    domain_list = list(dict.fromkeys(domain_list))
    domain_list.sort()

    return domain_list
