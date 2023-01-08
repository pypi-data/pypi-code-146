import os
from dotenv import load_dotenv
import requests
import click
import sys
import json

load_dotenv()

vams_backend = os.getenv("VAMS_BACKEND")

class LoginParamsError(Exception):
    """Exception raised for errors in the input salary.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Input params error"):
        self.message = message
        super().__init__(self.message)

#add outside repo for vams server and dependensy injection
def hello():
    print("Hello vams")

def authenticate(username, password):
    try:        
        credentials = read_credentials()

        username = username
        password = password

        is_valid = validate_params(username, password)
        headers={'tokens': json.dumps(credentials)}

        if(is_valid):
            res = requests.post(f"{vams_backend}/login", data={"username":username, "password":password}, headers=headers)
            if("userStatus" in res.json() and res.json()["userStatus"] == "FORCE_CHANGE_PASSWORD"):
                change_password(username)
                return 

            json_object = json.dumps(res.json(), indent=4)
 
            write_credentials(json_object)

            print('You have successfully logged in')
            return 
    except Exception as e:
        print('Fail')
        print("Error ", e)
        return e


def validate_params(username, password):
    if(username == None or len(username.strip()) == 0):
        raise LoginParamsError("Username is empty")
    
    if(password == None or len(password.strip()) == 0):
        raise LoginParamsError("Password is empty")

    if(len(username) < 4):
        raise LoginParamsError("Username is too short")
    
    if(len(password) < 8):
        raise LoginParamsError("Password is too short")

    return True

def change_password(username):
    print("You need change password. Please, enter new password")
    new_password = sys.stdin.readline().strip()
    username = username
    res = requests.post(f"{vams_backend}/change_password", data={"username": username, "new_password":new_password})

    if(res.json()['result'] == 'ok'):
        print('Now you can login with new password')
    
    return

def read_credentials():
    try: 
        with open('.credentials', 'r') as openfile:
            credentials = json.load(openfile)    
            return credentials
    except Exception as e:
        print("Error ", e)


def write_credentials(credentials):
    try:
        with open(".credentials", "w") as outfile:
            outfile.write(credentials)
    except Exception as e:
        print("Error ", e)


@click.group(help="VAMS CLI")
def main():
    """vams cli"""

@main.command('ping', help='service health check')
def ping():
    res = requests.get(f"{vams_backend}/health-check")
    print(res.json())

@main.command('login', help='login to vams')
@click.option('-u', '--user', default="", help='Username')
@click.option('-p', '--password', default="", help='Password')
def login(user, password):
    authenticate(user, password)