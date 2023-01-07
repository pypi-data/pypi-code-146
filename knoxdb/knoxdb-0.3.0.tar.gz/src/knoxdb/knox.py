import requests
import json
import urllib.parse
import psycopg2


def create(db_name):

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
    return get_from_id(id=id)


def get_from_id(id):

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


def connect(id):
    db = get_from_id(id=id)
    conn = psycopg2.connect(database=db["name"],
                            host=db["db"]["host"],
                            user=db["db"]["user"],
                            password=db["db"]["password"],
                            port="5432"
                            )
    return conn

def query(conn, command):
    cursor = conn.cursor()
    cursor.execute(command)
    response = cursor.fetchall()
    return response

def close_db_connection(conn):
    conn.close()