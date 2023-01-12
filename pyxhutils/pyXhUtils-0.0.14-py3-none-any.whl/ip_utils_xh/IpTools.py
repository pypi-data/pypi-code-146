import re


class Ip:
    def __init__(self, ip_seg: [int]):
        self.valid(ip_seg)
        self.ip_seg = ip_seg

    def binary_notation(self):
        Ip.valid(self.ip_seg)
        ipStr = "".join(["{:08b}".format(seg) for seg in self.ip_seg[:-1]])
        if self.ip_seg[4] > -1:
            s = ""
            for k, i in enumerate(ipStr):
                if k > self.ip_seg[4]:
                    s += "X"
                else:
                    s += f"{i}"
            return s
        else:
            return ipStr

    @staticmethod
    def from_regular_form(ip_str: str) -> 'Ip':
        pattern = "(\d+)\.(\d+)\.(\d+)\.(\d+)(/\d+){0,1}"
        m = re.match(pattern, ip_str)
        return Ip([int(m[1]), int(m[2]), int(m[3]), int(m[4]), int(m[5][1:]) if m[5] else -1])

    @staticmethod
    def valid(ip_seg: [int]):
        for key, seg in enumerate(ip_seg):
            if key < 4:
                if seg > 255 or seg < 0:
                    raise f"IP{ip_seg} not valid for value: {seg}"
            else:
                if seg > 32 or seg < -1:
                    raise f"IP[{ip_seg}] CIDR not valid for value: {seg}"

    @staticmethod
    def regular_form(ip: [int]):
        s = ""
        return ".".join([f"{seg}" for key, seg in ip[:-1]]) + f"/{ip[-1]}" if ip[-1] > -1 else ""


if __name__ == "__main__":
    ip = Ip.from_regular_form("192.168.8.1/16")
    print(ip.binary_notation())
    ipResults = [
        print(f"{ipStr}[{pow(2, 32 - ip.ip_seg[4])}] {ip.binary_notation()}")
        for ipStr in
        "10.91.132.0/22\n10.91.136.0/21\n10.91.144.0/20\n10.91.160.0/19\n10.91.196.0/22\n10.91.200.0/21\n10.91.208.0/20\n10.91.224.0/19".split("\n")
        for ip in [Ip.from_regular_form(ipStr)]
    ]
