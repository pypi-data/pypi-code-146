import requests # type: ignore

def is_dwh_consumer_alive(name: str):
    """returns true if dwh-consumer isalive endpoint returns OK"""
    # pylint: disable=no-member
    return requests.get("https://" + name + ".nais.adeo.no/isalive", timeout=10).status_code == requests.codes.ok
