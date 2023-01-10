
def get_public_ip():

    import urllib.request
    import ssl

    ssl._create_default_https_context = ssl._create_unverified_context

    return urllib.request.urlopen("https://ifconfig.me/ip").read().decode()
