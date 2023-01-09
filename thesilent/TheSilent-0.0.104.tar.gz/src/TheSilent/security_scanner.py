from TheSilent.clear import *
from TheSilent.subdomain_takeover import *
from TheSilent.sql_injection_scanner import *
from TheSilent.xss_scanner import *

red = "\033[1;31m"

#scans for all security flaws    
def security_scanner(url, secure = True, my_file = " "):
    clear()

    my_subdomain_takeover = subdomain_takeover(url, secure, my_file)
    my_sql_injection_scanner = sql_injection_scanner(url, secure, my_file)
    my_xss_scanner = xss_scanner(url, secure, my_file)

    clear()
    
    print(red + "sql injection:")

    for i in my_sql_injection_scanner:
        print(red + i)

    print("")
    print(red + "subdomain takeover:")

    for i in my_subdomain_takeover:
        print(red + i)

    print("")
    print(red + "xss:")

    for i in my_xss_scanner:
        print(red + i)
