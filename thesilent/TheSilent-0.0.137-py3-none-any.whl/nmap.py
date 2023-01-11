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

def host_up(port, my_ip):
    global host_up_list

    my_socket = socket.socket()
    my_socket.settimeout(1)

    try:
        my_socket.connect((my_ip, port))
        host_up_list.append(my_ip)
        my_socket.close()

    except ConnectionRefusedError:
        host_up_list.append(my_ip)
        my_socket.close()
        
    except OSError:
        my_socket.close()

    except TimeoutError:
        host_up_list.append(my_ip)
        my_socket.close()

#scan entire network
def nmap(ip, subnet):
    global host_up_list
    global nmap_list

    host_up_list = []
    nmap_list = []
    
    my_list = []

    clear()

    ip_list = list(ip_network(str(ip) + "/" + str(subnet)).hosts())

    for i in ip_list:
        print(cyan + "scanning: " + str(i))

        my_thread = threading.Thread(target = host_up, args = (80, str(i),))
        my_thread.start()

    my_thread.join()

    clear()

    print(str(len(host_up_list)) + " potential hosts up")
    
    for my_ip in host_up_list:
        print(cyan + "scanning: " + str(my_ip))

        for port in range(1, 1025):
            my_thread = threading.Thread(target = nmap_thread, args = (str(my_ip), port,))
            my_thread.start()

        my_thread.join()

    nmap_list = list(dict.fromkeys(nmap_list))
    nmap_list.sort()

    clear()

    return nmap_list
        
def nmap_thread(my_ip, port):
    my_socket = socket.socket()
    my_socket.settimeout(1)

    try:
        my_socket.connect((my_ip, port))
        nmap_list.append(my_ip + ": " + str(port))
        my_socket.close()

    except:
        my_socket.close()
