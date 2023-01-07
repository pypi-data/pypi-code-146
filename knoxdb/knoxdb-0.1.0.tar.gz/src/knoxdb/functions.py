import requests
import json
import urllib.parse

def create_db(db_name):

    url = "https://customer.elephantsql.com/api/instances"

    payload = json.dumps({
        "name": db_name,
        "plan": "turtle",
        "region": "amazon-web-services::us-east-1"
    })
    headers = {
        'Authorization': 'Basic OmYyYTVkYWNiLTg5MDAtNDViNC05MjNhLThkYWFjMjkzYjJkMA==',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    res = response.json()
    id = res["id"]
    return get_db_from_id(id=id)


def get_db_from_id(id):

    url = "https://customer.elephantsql.com/api/instances/{0}".format(id)

    payload = ""
    headers = {
        'Authorization': 'Basic OmYyYTVkYWNiLTg5MDAtNDViNC05MjNhLThkYWFjMjkzYjJkMA==',
        'Cookie': 'rack.session=BAh7CEkiD3Nlc3Npb25faWQGOgZFVG86HVJhY2s6OlNlc3Npb246OlNlc3Npb25JZAY6D0BwdWJsaWNfaWRJIkU2ODk3MjRkOWQ3ZjczYmI0NDljOTEwZThmNzdlYzBiMWQxMTNjYzQ4MTBlMjViZGM1MjdiZGQ0MTQyZmYwOWE3BjsARkkiDV9fcmVxY250BjsARmkISSIJdXNlcgY7AEZ7AA%3D%3D--2e03016849d7e82d6f4ce1dc2ec815dd3d93129c'
    }

    response = requests.request("GET", url, headers=headers, data=payload)


    # Parse the URL
    res = response.json()
    url = res["url"]
    parsed_url = urllib.parse.urlparse(url)

    # Extract the host, user, password, and database
    host = parsed_url.hostname
    user = parsed_url.username
    password = parsed_url.password
    database = parsed_url.path[1:]

    dbjson = {
        "id": res["id"],
        "type": "PostgresSQL",
        "name": res["name"],
        "url": res["url"],
        "db": {
            "host": host,
            "user": user,
            "password": password,
            "database": database
        },
        "ready": res["ready"]
    }

    return dbjson