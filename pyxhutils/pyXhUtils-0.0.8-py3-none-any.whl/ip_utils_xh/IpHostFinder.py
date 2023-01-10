from socket import socket


class IpHostFinder:
    map = {}

    def find(self, ip_str: str):
        if ip_str in self.map:
            return self.map[ip_str]
        else:
            try:
                domain, s = socket.getnameinfo((ip_str, 0), 0)
                self.map.update({ip_str: domain})
                return domain
            except:
                self.map.update({ip_str: "Unknown"})
                return "Unknown"
