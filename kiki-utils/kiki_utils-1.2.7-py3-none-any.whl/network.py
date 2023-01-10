import re

from socket import gethostbyname
from urllib.parse import urlparse


# Network utils

def get_domain_ip(domain: str):
    return gethostbyname(domain)


def get_host(url: str):
    """Get the host of the input url."""

    if not re.match(r'https?:\/\/', url):
        return url

    return urlparse(url).hostname


def domains_is_ip(domains: list[str], ip: str):
    return all([get_domain_ip(domain) == ip for domain in domains])
