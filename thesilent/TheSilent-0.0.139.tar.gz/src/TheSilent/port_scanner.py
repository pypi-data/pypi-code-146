from TheSilent.clear import *

import socket
import threading
import time

cyan = "\033[1;36m"

#scans for open ports on a server
def port_scanner(url):
    clear()

    global open_port_list
    open_port_list = []
    
    print(cyan + "scanning")
    
    for i in range(1, 65537):
        my_thread = threading.Thread(target = port_scanner_thread, args = (url, i,))
        my_thread.start()
        time.sleep(0.001)

    open_port_list = list(dict.fromkeys(open_port_list))
    open_port_list.sort()

    clear()
    
    return open_port_list

def port_scanner_thread(url, port):
    global my_port_list

    my_socket = socket.socket()
    my_socket.settimeout(1)

    my_list = []
    
    try:
        my_socket.connect((url, port))
        open_port_list.append(port)
        my_socket.close()

    except:
        my_socket.close()
