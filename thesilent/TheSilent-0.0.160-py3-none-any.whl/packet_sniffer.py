from TheSilent.clear import *

import socket

#capture packets like wireshark (requires linux)
def packet_sniffer(protocol = " ", data = False, parse = " ", hex_dump = False, ip = " "):
    clear()

    red = "\033[1;31m"
    cyan = "\033[1;36m"
    green = "\033[0;32m"

    my_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))

    while True:
        try:
            packet = my_socket.recvfrom(65537)

            #data
            data_hex = binascii.hexlify(packet[0])
            data_hex = str(data_hex).replace("b'", "")
            data_hex = data_hex.replace("'", "")

            data_ascii = codecs.decode(packet[0], errors = "replace")
            
            #mac stuff
            mac_destination = struct.unpack("!6s", packet[0][0:6])
            super_mac_destination = binascii.hexlify(mac_destination[0])
            super_mac_destination = str(super_mac_destination).replace("b'", "")
            super_mac_destination = super_mac_destination.replace("'", "")

            mac_source = struct.unpack("!6s", packet[0][6:12])
            super_mac_source = binascii.hexlify(mac_source[0])
            super_mac_source = str(super_mac_source).replace("b'", "")
            super_mac_source = super_mac_source.replace("'", "")

            #protocol
            my_protocol = struct.unpack("!1s", packet[0][23:24])
            super_protocol = binascii.hexlify(my_protocol[0])
            super_protocol = str(super_protocol).replace("b'", "")
            super_protocol = super_protocol.replace("'", "")

            proto = super_protocol

            if super_protocol == "00":
                proto = "HOPOPT"

            if super_protocol == "01":
                proto = "ICMP"

            if super_protocol == "02":
                proto = "IGMP"

            if super_protocol == "03":
                proto = "GGP"

            if super_protocol == "04":
                proto = "IP-in-IP"

            if super_protocol == "05":
                proto = "ST"
            
            if super_protocol == "06":
                proto = "TCP"

            if super_protocol == "07":
                proto = "CBT"

            if super_protocol == "08":
                proto = "EGP"

            if super_protocol == "09":
                proto = "IGP"

            if super_protocol == "0a":
                proto = "BBN-RCC-MON"

            if super_protocol == "0b":
                proto = "NVP-II"

            if super_protocol == "0c":
                proto = "PUP"

            if super_protocol == "0d":
                proto = "ARGUS"

            if super_protocol == "0e":
                proto = "EMCON"

            if super_protocol == "0f":
                proto = "XNET"

            if super_protocol == "10":
                proto = "CHAOS"

            if super_protocol == "11":
                proto = "UDP"

            if super_protocol == "12":
                proto = "MUX"

            if super_protocol == "13":
                proto = "DCN-MEAS"

            if super_protocol == "14":
                proto = "HMP"

            if super_protocol == "15":
                proto = "PRM"

            if super_protocol == "16":
                proto = "XNS-IDP"

            if super_protocol == "17":
                proto = "TRUNK-1"

            if super_protocol == "18":
                proto = "TRUNK-2"

            if super_protocol == "19":
                proto = "LEAF-1"

            if super_protocol == "1a":
                proto = "LEAF-2"

            if super_protocol == "1b":
                proto = "RDP"

            if super_protocol == "1c":
                proto = "IRTP"

            if super_protocol == "1d":
                proto = "ISO-TP4"

            if super_protocol == "1e":
                proto = "NETBLT"

            if super_protocol == "1f":
                proto = "MFE-NSP"

            if super_protocol == "20":
                proto = "MERIT-INP"

            if super_protocol == "21":
                proto = "DCCP"

            if super_protocol == "22":
                proto = "3PC"

            if super_protocol == "23":
                proto = "IDPR"

            if super_protocol == "24":
                proto = "XTP"

            if super_protocol == "25":
                proto = "DDP"

            if super_protocol == "26":
                proto = "IDPR-CMTP"

            if super_protocol == "27":
                proto = "TP++"

            if super_protocol == "28":
                proto = "IL"

            if super_protocol == "29":
                proto = "IPv6"

            if super_protocol == "2a":
                proto = "SDRP"

            if super_protocol == "2b":
                proto = "IPv6-Route"

            if super_protocol == "2c":
                proto = "IPv6-Frag"

            if super_protocol == "2d":
                proto = "IDRP"

            if super_protocol == "2e":
                proto = "RSVP"

            if super_protocol == "2f":
                proto = "GRE"

            if super_protocol == "30":
                proto = "DSR"

            if super_protocol == "31":
                proto = "BNA"

            if super_protocol == "32":
                proto = "ESP"

            if super_protocol == "33":
                proto = "AH"

            if super_protocol == "34":
                proto = "I-NLSP"

            if super_protocol == "35":
                proto = "SwIPe"

            if super_protocol == "36":
                proto = "NARP"

            if super_protocol == "37":
                proto = "MOBILE"

            if super_protocol == "38":
                proto = "TLSP"

            if super_protocol == "39":
                proto = "SKIP"

            if super_protocol == "3a":
                proto = "IPv6-ICMP"

            if super_protocol == "3b":
                proto = "IPv6-NoNxt"

            if super_protocol == "3c":
                proto = "IPv6-Opts"

            if super_protocol == "3d":
                proto = "3d"

            if super_protocol == "3e":
                proto = "CFTP"

            if super_protocol == "3f":
                proto = "3f"

            if super_protocol == "40":
                proto = "SAT-EXPAK"

            if super_protocol == "41":
                proto = "KRYPTOLAN"

            if super_protocol == "42":
                proto = "RVD"

            if super_protocol == "43":
                proto = "IPPC"

            if super_protocol == "44":
                proto = "44"

            if super_protocol == "45":
                proto = "SAT-MON"

            if super_protocol == "46":
                proto = "VISA"

            if super_protocol == "47":
                proto = "IPCU"

            if super_protocol == "48":
                proto = "CPNX"

            if super_protocol == "49":
                proto = "CPHB"

            if super_protocol == "4a":
                proto = "WSN"

            if super_protocol == "4b":
                proto = "PVP"

            if super_protocol == "4c":
                proto = "BR-SAT-MON"

            if super_protocol == "4d":
                proto = "SUN-ND"

            if super_protocol == "4e":
                proto = "WB-MON"

            if super_protocol == "4f":
                proto = "WB-EXPAK"

            if super_protocol == "50":
                proto = "ISO-IP"

            if super_protocol == "51":
                proto = "VMTP"

            if super_protocol == "52":
                proto = "SECURE-VMTP"

            if super_protocol == "53":
                proto = "VINES"

            if super_protocol == "54":
                proto = "TTP"

            if super_protocol == "55":
                proto = "NSFNET-IGP"

            if super_protocol == "56":
                proto = "DGP"

            if super_protocol == "57":
                proto = "TCF"

            if super_protocol == "58":
                proto = "EIGRP"

            if super_protocol == "59":
                proto = "OSPF"

            if super_protocol == "5a":
                proto = "Sprite-RPC"

            if super_protocol == "5b":
                proto = "LARP"

            if super_protocol == "5c":
                proto = "MTP"

            if super_protocol == "5d":
                proto = "AX.25"

            if super_protocol == "5e":
                proto = "OS"

            if super_protocol == "5f":
                proto = "MICP"

            if super_protocol == "61":
                proto = "ETHERIP"

            if super_protocol == "62":
                proto = "ENCAP"

            #ip stuff
            ip_header = packet[0][26:34]
            super_ip_header = struct.unpack("!4s4s", ip_header)

            #formatting
            destination = socket.inet_ntoa(super_ip_header[1])
            source = socket.inet_ntoa(super_ip_header[0])

            #checksum
            checksum = packet[0][24:26]
            checksum = struct.unpack("!2s", checksum)
            checksum = binascii.hexlify(checksum[0])
            checksum = str(checksum).replace("b'", "")
            checksum = checksum.replace("'", "")

            #protocol header
            source_port = packet[0][34:36]
            source_port = struct.unpack("!2s", source_port)
            source_port = binascii.hexlify(source_port[0])
            source_port = int(source_port, 16)

            destination_port = packet[0][36:38]
            destination_port = struct.unpack("!2s", destination_port)
            destination_port = binascii.hexlify(destination_port[0])
            destination_port = int(destination_port, 16)
            
            if proto == "UDP":
                checksum_protocol_udp = packet[0][40:42]
                checksum_protocol_udp = struct.unpack("!2s", checksum_protocol_udp)
                checksum_protocol_udp = binascii.hexlify(checksum_protocol_udp[0])
                checksum_protocol_udp = str(checksum_protocol_udp).replace("b'", "")
                checksum_protocol_udp = checksum_protocol_udp.replace("'", "")

            if proto == "TCP":
                try:
                    checksum_protocol_tcp = packet[0][42:44]
                    checksum_protocol_tcp = struct.unpack("!2s", checksum_protocol_tcp)
                    checksum_protocol_tcp = binascii.hexlify(checksum_protocol_tcp[0])
                    checksum_protocol_tcp = str(checksum_protocol_tcp).replace("b'", "")
                    checksum_protocol_tcp = checksum_protocol_tcp.replace("'", "")

                except:
                    pass
                
            #other protocols
            if destination_port == 20 or source_port == 20 or destination_port == 21 or source_port == 21:
                proto = "FTP"

            if destination_port == 22 or source_port == 22:
                proto = "SSH"

            if destination_port == 23 or source_port == 23:
                proto = "TELNET"

            if destination_port == 25 or source_port == 25:
                proto = "SMTP"

            if destination_port == 53 or source_port == 53:
                proto = "DNS"

            if destination_port == 67 or source_port == 67 or destination_port == 68 or source_port == 68:
                proto = "DHCP"
                
            if destination_port == 80 or source_port == 80:
                proto = "HTTP"

            if destination_port == 443 or source_port == 443:
                proto = "HTTPS"

            arp_check = struct.unpack("!2s", packet[0][12:14])
            arp_check = binascii.hexlify(arp_check[0])
            arp_check = str(arp_check).replace("b'", "")
            arp_check = arp_check.replace("'", "")

            if arp_check == "0806":
                proto = "ARP"
            
            #display
            if protocol == " ":
                if source == ip or destination == ip:
                    print(red + "source ip: " + str(source) + " | source mac: " + str(super_mac_source) + " | source port: " + str(source_port))
                    print(red + "destination ip: " + str(destination) + " | destination mac: " + str(super_mac_destination) + " | destination port: " + str(destination_port))
                    print(red + "protocol: " + proto)

                    if proto == "UDP":
                        print(red + "checksum (ip): " + checksum + " | checksum (protocol): " + str(checksum_protocol_udp))

                    if proto == "TCP":
                        print(red + "checksum (ip): " + checksum + " | checksum (protocol): " + str(checksum_protocol_tcp))
                    
                    if data == True:
                        print(cyan + "hex data: " + str(data_hex))
                        print(green + "utf-8 data: " + str(data_ascii))

                    if hex_dump == True:
                        with open("hex dump.txt", "a") as file:
                            file.write(data_hex + "\n")

                    print("")
                    
                if ip  == " ":
                    print(red + "source ip: " + str(source) + " | source mac: " + str(super_mac_source) + " | source port: " + str(source_port))
                    print(red + "destination ip: " + str(destination) + " | destination mac: " + str(super_mac_destination) + " | destination port: " + str(destination_port))
                    print(red + "protocol: " + proto)

                    if proto == "UDP":
                        print(red + "checksum (ip): " + checksum + " | checksum (protocol): " + str(checksum_protocol_udp))

                    if proto == "TCP":
                        print(red + "checksum (ip): " + checksum + " | checksum (protocol): " + str(checksum_protocol_tcp))

                    if data == True:
                        print(cyan + "hex data: " + str(data_hex))
                        print(green + "utf-8 data: " + str(data_ascii))

                    if hex_dump == True:
                        with open("hex dump.txt", "a") as file:
                            file.write(data_hex + "\n")

                    print("")

            if protocol == proto and protocol != "CLEAR":
                if source == ip or destination == ip:
                    print(red + "source ip: " + str(source) + " | source mac: " + str(super_mac_source) + " | source port: " + str(source_port))
                    print(red + "destination ip: " + str(destination) + " | destination mac: " + str(super_mac_destination) + " | destination port: " + str(destination_port))
                    print(red + "protocol: " + proto)

                    if proto == "UDP":
                        print(red + "checksum (ip): " + checksum + " | checksum (protocol): " + str(checksum_protocol_udp))

                    if proto == "TCP":
                        print(red + "checksum (ip): " + checksum + " | checksum (protocol): " + str(checksum_protocol_tcp))
                    
                    if data == True:
                        print(cyan + "hex data: " + str(data_hex))
                        print(green + "utf-8 data: " + str(data_ascii))

                    if hex_dump == True:
                        with open("hex dump.txt", "a") as file:
                            file.write(data_hex + "\n")

                    print("")

                if ip == " ":
                    print(red + "source ip: " + str(source) + " | source mac: " + str(super_mac_source) + " | source port: " + str(source_port))
                    print(red + "destination ip: " + str(destination) + " | destination mac: " + str(super_mac_destination) + " | destination port: " + str(destination_port))
                    print(red + "protocol: " + proto)

                    if proto == "UDP":
                        print(red + "checksum (ip): " + checksum + " | checksum (protocol): " + str(checksum_protocol_udp))

                    if proto == "TCP":
                        print(red + "checksum (ip): " + checksum + " | checksum (protocol): " + str(checksum_protocol_tcp))
                            
                    if data == True:
                        print(cyan + "hex data: " + str(data_hex))
                        print(green + "utf-8 data: " + str(data_ascii))

                    if hex_dump == True:
                        with open("hex dump.txt", "a") as file:
                            file.write(data_hex + "\n")
                            
                    print("")

            if protocol == "CLEAR":
                if destination_port == 20 or source_port == 20 or destination_port == 21 or source_port == 21 or destination_port == 23 or source_port == 23 or destination_port == 25 or source_port == 25 or destination_port == 53 or source_port == 53 or destination_port == 67 or source_port == 67 or destination_port == 68 or source_port == 68 or destination_port == 80 or source_port == 80 or destination_port == 443 or source_port == 443:
                    if source == ip or destination == ip:
                        print(red + "source ip: " + str(source) + " | source mac: " + str(super_mac_source) + " | source port: " + str(source_port))
                        print(red + "destination ip: " + str(destination) + " | destination mac: " + str(super_mac_destination) + " | destination port: " + str(destination_port))
                        print(red + "protocol: " + proto)

                        if proto == "UDP":
                            print(red + "checksum (ip): " + checksum + " | checksum (protocol): " + str(checksum_protocol_udp))

                        if proto == "TCP":
                            print(red + "checksum (ip): " + checksum + " | checksum (protocol): " + str(checksum_protocol_tcp))
                        
                        if data == True:
                            print(cyan + "hex data: " + str(data_hex))
                            print(green + "utf-8 data: " + str(data_ascii))

                        if hex_dump == True:
                            with open("hex dump.txt", "a") as file:
                                file.write(data_hex + "\n")

                        print("")

                    if ip == " ":
                        print(red + "source ip: " + str(source) + " | source mac: " + str(super_mac_source) + " | source port: " + str(source_port))
                        print(red + "destination ip: " + str(destination) + " | destination mac: " + str(super_mac_destination) + " | destination port: " + str(destination_port))
                        print(red + "protocol: " + proto)

                        if proto == "UDP":
                            print(red + "checksum (ip): " + checksum + " | checksum (protocol): " + str(checksum_protocol_udp))

                        if proto == "TCP":
                            print(red + "checksum (ip): " + checksum + " | checksum (protocol): " + str(checksum_protocol_tcp))
                                
                        if data == True:
                            print(cyan + "hex data: " + str(data_hex))
                            print(green + "utf-8 data: " + str(data_ascii))

                        if hex_dump == True:
                            with open("hex dump.txt", "a") as file:
                                file.write(data_hex + "\n")
                                
                        print("")

        except:
            print(red + "ERROR!")
            continue
