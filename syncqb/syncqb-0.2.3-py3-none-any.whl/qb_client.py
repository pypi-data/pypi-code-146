import time
from . import json_quickbase, xml_quickbase
from typing import Union, Dict
import os
import getpass
from dotenv import find_dotenv, load_dotenv

def get_client(json_sdk: bool = None, creds: Dict=None) -> Union[json_quickbase.Client, xml_quickbase.Client]:
    """
    Function to initialize a Client object. 
    :param json_sdk: Boolean to determine which SDK is used. True for the JSON SDK, otherwise the XML SDK.
    :param creds: dictionary containing the realm credentials. If omitted, defaults to environmental variables.
    """
    load_dotenv(find_dotenv())
    if creds:
        url = creds.get('QB_URL')
        user_token = creds.get('QB_USERTOKEN')
        username = creds.get('QB_USERNAME')
        password = creds.get('QB_PASSWORD')
    else:
        url = os.environ.get('QB_URL')
        user_token = os.environ.get('QB_USER_TOKEN')
        username = os.environ.get('QB_USERNAME')
        password = os.environ.get('QB_PASSWORD')

    realmhost = url.split('https://')[1]

    if json_sdk:
        new_qb_client = json_quickbase.Client(
            realmhost=realmhost, base_url=url, user_token=user_token)
        return new_qb_client
    else:
        if time_update_qb_client is None or time.time() - time_update_qb_client > 24 * 60 * 60:

            qb_client = xml_quickbase.Client(
                username, password, base_url=url, hours=25)
            time_update_qb_client = time.time()
        return qb_client


def set_qb_info():
    """
    Function to set the default Quickbase information to initialize client objects. Writes each input into a .env file to create environmental variables.
    WARNING: The .env file is created in your CWD. If your project is shared on github, be sure to add .env to your .gitignore!
    """
    QB_URL = input('Quickbase URL (include https): ')
    QB_USER_TOKEN = input('User Token: ')
    QB_USERNAME = input('Username: ')
    QB_PASSWORD = getpass.getpass()
    with open(".env", "w") as env:
        env.write(f'QB_URL={QB_URL}\n')
        env.write(f'QB_USER_TOKEN={QB_USER_TOKEN}\n')
        env.write(f'QB_USERNAME={QB_USERNAME}\n')
        env.write(f'QB_PASSWORD={QB_PASSWORD}')