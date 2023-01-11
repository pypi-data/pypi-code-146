from TheSilent.clear import *
from ipaddress import *

import socket
import threading
import time

cyan = "\033[1;36m"

#global variables mainly used for multi-threading
host_up_list = []
nmap_list = []
open_port_list = []

my_socket = socket.socket()
my_socket.settimeout(1)

def host_up(port, my_ip):
    global host_up_list

    my_socket = socket.socket()
    my_socket.settimeout(1)

    try:
        my_socket.connect((my_ip, port))
        host_up_list.append(my_ip)

    except ConnectionRefusedError:
        host_up_list.append(my_ip)
        
    except OSError:
        pass

    except TimeoutError:
        host_up_list.append(my_ip)

#scan entire network
def nmap(ip, subnet):
    global host_up_list
    global nmap_list

    host_up_list = []
    nmap_list = []
    
    my_list = []

    clear()

    ip_list = list(ip_network(str(ip) + "/" + str(subnet)).hosts())

    thread_list = []

    for i in ip_list:
        print(cyan + "scanning: " + str(i))

        my_thread = threading.Thread(target = host_up, args = (80, str(i),))
        my_thread.start()

    for i in thread_list:
        i.join()
            
    clear()

    print(str(len(host_up_list)) + " potential hosts up")

    for my_ip in host_up_list:
        print(cyan + "scanning: " + str(my_ip))

        thread_list = []

        for port in range(1024):
            my_thread = threading.Thread(target = nmap_thread, args = (str(my_ip), port,))
            my_thread.start()

        for i in thread_list:
            i.join()

    nmap_list = list(dict.fromkeys(nmap_list))
    nmap_list.sort()

    clear()

    return nmap_list
        
def nmap_thread(my_ip, port):
    global nmap_list

    try:
        my_socket.connect((my_ip, port))
        nmap_list.append(my_ip + ": " + str(port))

    except:
        pass
