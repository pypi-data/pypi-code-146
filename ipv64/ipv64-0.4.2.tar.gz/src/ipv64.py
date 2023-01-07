import dns.resolver
import requests
from datetime import datetime as dt
import argparse
import time
import socket

# version
version = "0.3.5"
# gloabl variables
global headers
headers = {
    'User-Agent': 'ipv64-updater/' + str(version),
}

# get the current IP of the host
def get_ip(only_ipv4, only_ipv6):

    if only_ipv4 == False and only_ipv6 == False:
        only_ipv6 = True
        only_ipv4 = True

    # Get the current IPv4 of the host
    if only_ipv4 == True:
        try:
            ipv4 = requests.get('https://ipv4.ipapi.de', headers=headers).text
            print(str(dt.now()) + ": IPv4 found: " + str(ipv4))
        except:
            print(str(dt.now()) + ": IPv4 resolution failed")
            ipv4 = False
            if only_ipv6 == False:
                exit()
    else:
        ipv4 = False
    
    # get the current IPv6 of the host
    if only_ipv6 == True:
        try:
            ipv6 = requests.get('https://ipv6.ipapi.de', headers=headers).text
            print(str(dt.now()) + ": IPv6 found: " + str(ipv6))
        except:
            print(str(dt.now()) + ": IPv6 resolution failed")
            ipv6 = False
            if ipv4 == False:
                exit()
    else:
        ipv6 = False
    
    return ipv4, ipv6

# Get the current ip of the domain
def nslookup(prefix, domain, ipv4, ipv6, only_ipv4, only_ipv6):
    resolver = dns.resolver.Resolver()
    dns.resolver.Cache(1)
    dns.resolver.Timeout(10)
    
    # IPv4
    try:
        ns1_ip4 = socket.getaddrinfo("ns1.ipv64.net", None, socket.AF_INET)[0][4][0]
    except:
        ns1_ip4 = False
    try:
        ns2_ip4 = socket.getaddrinfo("ns2.ipv64.net", None, socket.AF_INET)[0][4][0]
    except:
        ns2_ip4 = False

    # IPv6
    try:
        ns1_ip6 = socket.getaddrinfo("ns1.ipv64.net", None, socket.AF_INET6)[0][4][0]
    except:
        ns1_ip6 = False
    try:
        ns2_ip6 = socket.getaddrinfo("ns2.ipv64.net", None, socket.AF_INET6)[0][4][0]
    except:
        ns2_ip6 = False
    
    if ns1_ip4 != False and ns1_ip6 == False:
        resolver.nameservers = [ns1_ip4]
    elif ns2_ip4 != False and ns2_ip6 == False:
        resolver.nameservers = [ns2_ip4]
    elif ns1_ip6 != False and ns1_ip4 == False:
        resolver.nameservers = [ns1_ip6]
    elif ns2_ip6 != False and ns2_ip4 == False:
        resolver.nameservers = [ns2_ip6]
    elif ns1_ip4 != False and ns1_ip6 != False:
        resolver.nameservers = [ns1_ip4, ns1_ip6]
    elif ns2_ip4 != False and ns2_ip6 != False:
        resolver.nameservers = [ns2_ip4, ns2_ip6]
    else:
        print("Nameserver Error")
        exit()
    

    if only_ipv4 == False and only_ipv6 == False:
        only_ipv6 = True
        only_ipv4 = True

    if prefix != "":
        domain = str(prefix) + "." + str(domain)
    else:
        domain = str(domain)
    
    # check for A records
    if only_ipv4 == True and ipv4 != False:
        try:
            ipv4_ns = resolver.resolve(domain, 'A')
            # if there is more than one IP
            for ip in ipv4_ns:
                ipv4_ns = ip.to_text()
                print(str(dt.now()) + ": A record found: (" + str(domain) + " - " + str(ip) + ")")
                
        except:
            print(str(dt.now()) + ": A nslookup failed")
            ipv4_ns = False
    else:
        ipv4_ns = False

    # check for AAAA records
    if only_ipv6 == True and ipv6 != False:
        try:
            ipv6_ns = resolver.resolve(domain, 'AAAA')
            # if there is more than one IP
            for ip in ipv6_ns:
                ipv6_ns = ip.to_text()
                print(str(dt.now()) + ": AAAA record found: (" + str(domain) + " - " + str(ipv6_ns) + ")")
            
        except:
            print(str(dt.now()) + ": AAAA nslookup failed")
            ipv6_ns = False
    else:
        ipv6_ns = False

    return ipv4_ns, ipv6_ns


# Update the DNS records of the domain with the current IP of the host at ipv64.net
def set_ip(prefix, domain, update_key, ipv4, ipv6, only_ipv4, only_ipv6):

    #wenn kein -4 oder -6 parameter, dann beide Einträge versuchen zu aktualisieren
    if only_ipv4 == False and only_ipv6 == False:
        only_ipv6 = True
        only_ipv4 = True

    # update A record
    if ipv4 != False and only_ipv4 == True:
        print(str(dt.now()) + ": Updating A record")
        url = "https://ipv64.net/update.php?key=" + update_key + "&domain=" + str(domain) + "&ip=" + str(ipv4) + "&praefix=" + str(prefix)

        try:
            r = requests.get(url, headers=headers)
            status_a = r.status_code
        except:
            print(str(dt.now()) + ": A record update failed")
            status_a = False
    else:
        print(str(dt.now()) + ": A record update skipped")
        status_a = False
    
    # timeout 1 seconds to prevent rate limit
    time.sleep(1)

    # update AAAA record
    if ipv6 != False and only_ipv6 == True:
        print(str(dt.now()) + ": Updating AAAA record")
        url = "https://ipv64.net/update.php?key=" + update_key + "&domain=" + str(domain) + "&ip6=" + str(ipv6) + "&praefix=" + str(prefix)
        try:
            r = requests.get(url, headers=headers)
            status_aaaa = r.status_code
        except:
            print(str(dt.now()) + ": AAAA record update failed")
            status_aaaa = False
    else:
        print(str(dt.now()) + ": AAAA record update skipped")
        status_aaaa = False

    return status_a, status_aaaa

# Send a message to discord
def discord_msg(msg=False, webhook=False):
    if webhook != False or "":
        # Send a message to a discord channel
        try:
            requests.post(webhook, json={"content": msg, "username": "IPV64 Updater"})
        except:
            print(str(dt.now()) + ": Discord message failed")

def gotify_msg(msg=False, gotifyurl=False, gotifytoken=False):
    if gotifyurl != False and gotifytoken != False:
        resp = requests.post(str(gotifyurl) + '/message?token=' + str(gotifytoken), json={
        "message": msg,
        "priority": 5,
        "title": "ipv64 status update"
        })

def do_update(prefix, domain, update_key, webhook, only_ipv4, only_ipv6, gotifyurl, gotifytoken):
    # Get the current IP of the host
    ipv4, ipv6 = get_ip(only_ipv4, only_ipv6)

    # Get the current IP of the domain
    ipv4_ns, ipv6_ns = nslookup(prefix, domain, ipv4, ipv6, only_ipv4, only_ipv6)

    # Check if the IP of the host and the domain are the same
    if ipv4 == ipv4_ns and ipv6 == ipv6_ns:
        print(str(dt.now()) + ": A and AAAA is up to date")
        status_a, status_aaaa = False, False
    else:
        if ipv4 != False and ipv4 != ipv4_ns and ipv6 != False and ipv6 != ipv6_ns:
            print(str(dt.now()) + ": A and AAAA is not up to date")
            status_a, status_aaaa = set_ip(prefix, domain, update_key, ipv4, ipv6, only_ipv4, only_ipv6)
        
        elif ipv6 != False and ipv6 != ipv6_ns:
            print(str(dt.now()) + ": AAAA is not up to date")
            status_a, status_aaaa = set_ip(prefix, domain, update_key, False, ipv6, only_ipv4, only_ipv6)

        elif ipv4 != False and ipv4 != ipv4_ns:
            print(str(dt.now()) + ": A is not up to date")
            status_a, status_aaaa = set_ip(prefix, domain, update_key, ipv4, False, only_ipv4, only_ipv6)


        # print(str(dt.now()) + ": IP is not up to date")
        # discord_msg("IP is not up to date", webhook)
        # # Update the DNS records of the domain with the current IP of the host
        # status_a, status_aaaa = set_ip(prefix, domain, update_key, ipv4, ipv6, only_ipv4, only_ipv6)

    # IPv4
    if status_a == 200:
        msg_a = f"🟩 Success Updated A record for {prefix}.{domain} to {ipv4}, ipv64.net Response: OK"
    elif status_a == 400:
        msg_a = f"🟥 Error updating A record for {prefix}.{domain}, ipv64.net Response: Bad Request"
    elif status_a == 401:
        msg_a = f"🟥 Error updating A record for {prefix}.{domain}, ipv64.net Response: Unauthorized"
    elif status_a == 429:
        msg_a = f"🟥 Error updating A record for {prefix}.{domain}, ipv64.net Response: Too Many Requests"

    if gotifyurl != False and gotifytoken != False and status_a != False:
        gotify_msg(msg_a, gotifyurl, gotifytoken)
    
    if webhook != False and status_a != False:
        discord_msg(msg_a, webhook)
    
    # IPv6
    if status_aaaa == 200:
        msg_aaaa = f"🟩 Success Updated AAAA record for {prefix}.{domain} to {ipv6}, ipv64.net Response: OK"
    elif status_aaaa == 400:
        msg_aaaa = f"🟥 Error updating AAAA record for {prefix}.{domain}, ipv64.net Response: Bad Request"
    elif status_aaaa == 401:
        msg_aaaa = f"🟥 Error updating AAAA record for {prefix}.{domain}, ipv64.net Response: Unauthorized"
    elif status_aaaa == 429:
        msg_aaaa = f"🟥 Error updating AAAA record for {prefix}.{domain}, ipv64.net Response: Too Many Requests"

    if gotifyurl != False and gotifytoken != False and status_aaaa != False:
        gotify_msg(msg_aaaa, gotifyurl, gotifytoken)
    
    if webhook != False and status_aaaa != False:
        discord_msg(msg_aaaa, webhook)
        
        
    exit()

 # ==================== ARGPARSE ====================
# ask for argprase inputs
# if no inputs are given, show help
parser = argparse.ArgumentParser(description='Update the IP for a domain on ipv64.net')
# ipv64 Arguments
parser.add_argument('-d', '--domain', help='The domain to update', required=True)
parser.add_argument('-uh', '--hash', help='Your ipv64 Account Update Token', required=True)
parser.add_argument('-p', '--prefix', help='The prefix for the domain', default="", required=False)
# Discord
parser.add_argument('-w', '--webhook', help='The webhook url for discord notifications', required=False, default=False)
# Gotify
parser.add_argument('-gu', '--gotifyurl', help='Your Gotify URL', required=False, default=False)
parser.add_argument('-gt', '--gotifytoken', help='Your Gotify Token', required=False, default=False)

# check if only ipv4 or ipv6 should be updated
parser.add_argument("-4", "--ipv4", help="Update only the A record", required=False, action='store_true')
parser.add_argument("-6", "--ipv6", help="Update only the AAAA record", required=False, action='store_true')

args = parser.parse_args()


# ======================== START ========================
#run_update(str(args.domain), str(args.hash), args.webhook, args.ipv4, args.ipv6)

#nslookup(args.prefix, args.domain, args.ipv4, args.ipv6)
#get_ip(args.ipv4, args.ipv6)

do_update(args.prefix, args.domain, args.hash, args.webhook, args.ipv4, args.ipv6, args.gotifyurl, args.gotifytoken)