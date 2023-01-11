import subprocess
import ipaddress
import qrcode 


class wireguard(object):
 
    def __init__(
        self, 
        server_name = 'wg0', 
        server_addres = 'wireguard.example.org', 
        server_ip = '10.10.10.1',
        server_private_key = '',
        server_port = 51820, 
        peer_ip_mask = 32, 
        peer_allowedIPs = '0.0.0.0/0', 
        dns = ''
        ):

        self.server_name = server_name
        self.server_addres = server_addres
        self.server_private_key = server_private_key
        self.server_ip = server_ip
        self.server_port = server_port
        self.peer_ip_mask = peer_ip_mask
        self.peer_allowedIPs = peer_allowedIPs
        self.dns = dns
        

    @property
    def get_private_key(self):
        cmd = f"wg genkey"
        private_key = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].decode('utf-8').rstrip()
        return private_key

    def get_pub_key(self, private_key):
        cmd = f"/bin/echo '{private_key}' | wg pubkey"
        pub_key = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].decode('utf-8').rstrip()
        return private_key
    
    @property
    def keys(self):
        private_key = self.get_private_key
        pub_key = self.get_pub_key(private_key)
        return {'private_key':private_key, 'pub_key': pub_key}
    

    def add(self, public_key='', ip=''):
        ip = str(ip) + '/' + str(self.peer_ip_mask)
        cmd = f"""wg set  '{self.server_name}' peer '{public_key}' allowed-ips '{ip}'"""
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return True
        

    def delete(self, public_key, server_name=''):
        cmd = f"wg set {server_name} peer  {public_key} remove"
        # print(cmd)
        res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # print(res.communicate()[0].decode('utf-8'))
        return True


    def info(self, who):
        ip_addresses = []
        peers = []
        cmd = f"wg show '{self.server_name}' allowed-ip_addresses"
        result_wg_info = \
            subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].decode(
                'utf-8').split('\n')
        for l in result_wg_info:
            if l:
                ip_addresses.append(l.split('\t')[1].split('/32')[0])
                peers.append(l.split('\t')[0])
        if who == 'ip_addresses':
            return ip_addresses
        if who == 'peers':
            return peers
    

    @property
    def status(self):
        cmd = f"wg show '{self.server_name}'"
        result_wg_info = \
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].decode('utf-8')
        peers_online = {}
        for peer in result_wg_info.split('\n\n'):
            peer_data = peer.split('\n')
            peer = ''
            server_addres = ''
            handshake = ''
            allowed_ip_addresses = ''
            for data in peer_data:
                peer_dict = {}
                if 'peer:' in data:
                    peer = data.split('peer: ')[1]
                if 'server_addres: ' in data:
                    server_addres = data.split('server_addres: ')[1].split(':')[0]
                if 'latest handshake: ' in data:
                    handshake = str(data.split('latest handshake: ')[1].split(':')[0].split('\n')).strip('[]').replace(
                        ' ', '_').replace('\'', '')
                    # print(handshake)
                if 'allowed ip_addresses:' in data:
                    allowed_ip_addresses = data.split('allowed ip_addresses: ')[1].split(':')[0]

                if peer:
                    peer_dict['server_addres'] = server_addres
                    peer_dict['handshake'] = handshake
                    peer_dict['allowed_ip_addresses'] = allowed_ip_addresses
                    peers_online[peer] = peer_dict
        if peers_online:
            return peers_online
        return False


    def get_config_client(self, peer_private_key, peer_ip, allowedIPs=''):
        dns_addr = ''
        if self.dns: dns_addr = f'DNS = {self.dns}{chr(10)}'
        if not allowedIPs: allowedIPs = self.peer_allowedIPs

        server_pub_key = self.get_pub_key(self.server_private_key)

        config_client = (
            f'[Interface]{chr(10)}'
            f'Address = {peer_ip}{chr(10)}'
            f'PrivateKey =  {peer_private_key}{chr(10)}'
            f'{dns_addr}{chr(10)}'

            f'[Peer]{chr(10)}'
            f'PublicKey = {server_pub_key}{chr(10)}'
            f'# PresharedKey ={chr(10)}'
            f'AllowedIPs = {allowedIPs}{chr(10)}'
            f'server_addres = {self.server_addres}')
        return config_client


    def get_config_server(self):
        keys = self.keys
        config_server = (
            f'[Interface]{chr(10)}'
            f'PrivateKey = {keys["private_key"]}{chr(10)}'
            f'Address = {self.server_ip}{chr(10)}'
            f'ListenPort = {self.server_port}'
        )
        return config_server, keys["pub_key"]


    # Ищет новый IP адрес сортируя имеющиеся, добавляет IP в промежутках
    def new_ip(self):
        ip_addresses = self.info(who='ip_addresses')
        ip_addresses_tmp = []
        for ip in ip_addresses:
            ip_addresses_tmp.append(ip)
            try:
                ipaddress.ip_address(ip)
            except Exception as error:
                ip_addresses_tmp.remove(ip)

        ip_addresses = ip_addresses_tmp
        ip_addresses = sorted([ipaddress.ip_address(addr) for addr in ip_addresses])
        tmp_ip = ip_addresses[0]
        for ip in ip_addresses:
            if ip == tmp_ip:
                tmp_ip += 1
            else:
                return tmp_ip
        return ip + 1
    

    def get_qr(self, peer_private_key, peer_ip, allowedIPs=''):
        config_peer = self.get_config_client(peer_private_key, peer_ip, allowedIPs='')
        qr = qrcode.QRCode()
        qr.add_data(config_peer)
        qr.make()
        img = qr.make_image()
        return img.convert('RGB')


