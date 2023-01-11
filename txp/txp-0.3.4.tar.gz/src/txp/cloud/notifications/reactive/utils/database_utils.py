import json
from typing import List

from google.oauth2 import service_account
from google.cloud import firestore
from txp.common.utils.firestore_utils import get_all_tenants_from_firestore
from txp.common.utils.firestore_utils import (
    get_authenticated_client as get_firestore_authenticated_client,
)


CREDENTIALS_PATH = "credentials/pub_sub_to_bigquery_credentials.json"


def get_gcloud_credentials_from_file(
    credentials_path: str,
) -> service_account.Credentials:
    """Loads a credentials file.

    Args:
        credentials_path: Path to credentials file.
    """
    with open(credentials_path, "r") as file:
        credentials_str = file.read().replace("\n", "")
    json_dict_service_account = json.loads(credentials_str, strict=False)
    gcloud_credentials = service_account.Credentials.from_service_account_info(
        json_dict_service_account
    )
    return gcloud_credentials


def get_tenants_from_phone_number(
    tenants_data: List[dict], phone_number: str
) -> List[str]:
    """Returns a list with the tenants' IDs related to a user's phone number.

    Args:
        tenants_data: Tenant's data from database.
        phone_number: Phone number (WhatsApp) of the tenant's user.
    """
    tenants = list()
    no_prefix_phone = phone_number.split("+")[1]
    try:
        for t in tenants_data:
            if any(
                d["phone_number"] == no_prefix_phone for d in t["notification_users"]
            ):
                tenants.append(t["tenant_id"])
        if tenants:
            return tenants
        else:
            return [None]

    except Exception as e:
        print(e)


def build_tenants_json(filename: str, firestore_client: firestore.Client):
    """Download tenants data using a Firestore client.

    Args:
        filename: Name and path of the JSON file in which the downloaded data will be saved.
        firestore_client: A firestore.Client object authenticated with the provided credentials.
    """
    tenants_from_firestore = get_all_tenants_from_firestore(firestore_client)
    with open(filename, "w") as json_file:
        json.dump(tenants_from_firestore, json_file)


def read_tenants_json(filename: str) -> dict:
    """Loads JSON file with the tenants' data.

    Args:
        filename: Name and path of the JSON file wich contains tenants' data.
    """
    try:
        with open(filename, "r") as json_file:
            return json.load(json_file)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    credentials = get_gcloud_credentials_from_file(
        "credentials/pub_sub_to_bigquery_credentials.json"
    )
    client = get_firestore_authenticated_client(credentials)
    build_tenants_json("tenants_data.json", client)
    client.close()
