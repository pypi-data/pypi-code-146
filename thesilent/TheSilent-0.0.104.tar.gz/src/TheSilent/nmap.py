from TheSilent.clear import *

import socket
import threading
import time

red = "\033[1;31m"

#global variables mainly used for multi-threading
host_up_list = []
nmap_list = []
open_port_list = []

def host_up(port, i, ii, iii, iv):
    global host_up_list

    my_socket = socket.socket()
    my_socket.settimeout(1)

    my_ip = str(i) + "." + str(ii) + "." + str(iii) + "." + str(iv)

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
def nmap():
    global host_up_list
    global nmap_list

    host_up_list = []
    nmap_list = []
    
    my_list = []

    clear()

    user_input = input("1 = 192 | 2 = 172 | 3 = 10\n")

    clear()

    print(red + "scanning")

    if user_input == "1":
        for i in range(192, 193):
            for ii in range(168, 169):
                for iii in range(0, 255):
                    for iv in range(0, 255):
                        my_thread = threading.Thread(target = host_up, args = (80, i, ii, iii, iv,))
                        my_thread.start()
                        time.sleep(0.001)

        print(str(len(host_up_list)) + " potential hosts up")
                            
        for my_ip in host_up_list:
            for port in range(1, 65537):
                my_thread = threading.Thread(target = nmap_thread, args = (my_ip, port,))
                my_thread.start()
                time.sleep(0.001)

    if user_input == "2":
        for i in range(172, 173):
            for ii in range(16, 32):
                for iii in range(0, 255):
                    for iv in range(0, 255):
                        my_thread = threading.Thread(target = host_up, args = (80, i, ii, iii, iv,))
                        my_thread.start()
                        time.sleep(0.001)

        print(str(len(host_up_list)) + " potential hosts up")
                        
        for my_ip in host_up_list:
            for port in range(1, 65537):
                my_thread = threading.Thread(target = nmap_thread, args = (my_ip, port,))
                my_thread.start()
                time.sleep(0.001)

    if user_input == "3":
        for i in range(10, 11):
            for ii in range(0, 255):
                for iii in range(0, 255):
                    for iv in range(0, 255):
                        my_thread = threading.Thread(target = host_up, args = (80, i, ii, iii, iv,))
                        my_thread.start()
                        time.sleep(0.001)

        print(str(len(host_up_list)) + " potential hosts up")
                        
        for my_ip in host_up_list:
            for port in range(1, 65537):
                my_thread = threading.Thread(target = nmap_thread, args = (my_ip, port,))
                my_thread.start()
                time.sleep(0.001)

    nmap_list = list(dict.fromkeys(nmap_list))
    nmap_list.sort()

    for i in nmap_list:
        print(i)
        
def nmap_thread(my_ip, port):
    my_socket = socket.socket()
    my_socket.settimeout(1)

    port_dict = {1:"tcpmux",2:"compressnet-management-utility",3:"compressnet-compression-process",5:"remote-job-entry",7:"echo",9:"discard",11:"active-users",13:"daytime",17:"qotd",18:"message-send",19:"chargen",20:"ftp-data",21:"ftp-command",22:"ssh",23:"telnet",25:"smtp",27:"nsw-user-system-fe",29:"msg-icp",31:"msg-auth",33:"dsp",37:"time",38:"rap/rlp",41:"graphics",42:"host-name-server",43:"whois",44:"mpm-flags",45:"mpm",46:"mpm-snd",48:"auditd",49:"tacacs",50:"re-mail-ck",52:"xns-time",53:"dns",54:"xns-name-server",55:"isi-graphics-language",56:"xns-authentication",58:"xns-mail",62:"acas",63:"whois++",64:"covia",65:"tacacs-ds",66:"sql-net",67:"dhcp",68:"dhcp",69:"tftp",70:"gopher",71:"netrjs",72:"netrjs",73:"netrjs",74:"netrjs",76:"deos",78:"vettcp",79:"finger",80:"http",82:"xfer",83:"mit-ml-dev",84:"common-trace-facility",85:"mit-ml-dev",86:"micro-focus-cobol",88:"kerberos",89:"su/mit-telnet-gateway",90:"dnsix",91:"mit-dov",92:"network-printing",93:"device-control",94:"objcall",95:"supdup-terminal-independent-remote-login",96:"dixie",97:"swift-rvf",98:"tacnews",99:"metagram",101:"nic",102:"tsap",104:"dicom",105:"ccso-nameserver",107:"rtelnet",108:"ibm-systems-network-architecture",109:"pop2",110:"pop3",111:"sun-rpc",113:"authentication-service/identification-protocol",115:"sftp",117:"uucp-mapping-project",118:"sql-services",119:"nntp",123:"ntp",137:"netbios-ns",443:"https",853:"dns-over-tls",3001:"nessus",8080:"http-proxy",8443:"https-proxy",9050:"tor",9051:"tor",19132:"minecraft-bedrock-server-ipv4",19133:"minecraft-bedrock-server-ipv6",62072:"iphone-sync",62078:"iphone-sync"}
    
    try:
        my_socket.connect((my_ip, port))

        try:
            nmap_list.append(my_ip + ": " + str(port) + " open " + port_dict[port])

        except:
            nmap_list.append(my_ip + ": " + str(port) + " open unknown" )

    except:
        pass
