from TheSilent.clear import *

import socket
import threading
import time

cyan = "\033[1;36m"

my_socket = socket.socket()
my_socket.settimeout(1)

#scans for open ports on a server
def port_scanner(url):
    clear()

    global open_port_list
    open_port_list = []
    
    print(cyan + "scanning")
    
    for i in range(1, 1025):
        my_thread = threading.Thread(target = port_scanner_thread, args = (url, i,))
        my_thread.start()

    open_port_list = list(dict.fromkeys(open_port_list))
    open_port_list.sort()

    clear()

    my_socket.close()
    
    return open_port_list

def port_scanner_thread(url, port):
    global my_port_list

    my_list = []
    
    try:
        my_socket.connect((url, port))
        open_port_list.append(port)

    except:
        pass
