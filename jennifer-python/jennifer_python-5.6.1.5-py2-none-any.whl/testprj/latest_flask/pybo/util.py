import os


def get_mysql_ip():

    if os.getenv("DEMO_CONTAINER"):
        return "192.168.0.8"

    wsl_name = os.getenv("WSL_DISTRO_NAME")

    if os.getenv("WSL_DISTRO_NAME") == "Ubuntu-20.04":
        return "192.168.0.8"

    return get_wsl_ip()


def get_wsl_ip():
    try:
        with open('/etc/resolv.conf') as f:
            for line in f.readlines():
                item = line.split(' ')
                if item[0] == 'nameserver':
                    return item[1].strip()
    except:
        pass
