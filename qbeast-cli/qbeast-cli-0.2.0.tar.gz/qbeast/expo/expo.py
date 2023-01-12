import typing as T
import re
from qbeast import predefs
from qbeast.utils import send_get, send_post

s3_regex = re.compile(predefs.s3_pattern)

""" GETTERS """


def get_share(share_name: str) -> (bool, T.Dict):
    success, reply = send_get(f'/shares/{share_name}')
    return success, reply


""" MODIFIERS """


# Send request to create a SHARE
def create_share_and_schema(share_name):
    path = '/shares'
    json_body = {"name": share_name,
                 "description": "Share created with qbeast CLI"}

    success, reply = send_post(path, json_body)
    real_share_name = reply["name"]
    if success:
        success, _ = create_schema(real_share_name)

    return success, reply


# Send request to create a SCHEMA
def create_schema(share_name, schema=predefs.default_schema_name):
    path = f"/shares/{share_name}/schemas"
    json_body = {"name": schema,
                 "description": "Schema created with qbeast CLI"}

    success, reply = send_post(path, json_body)
    return success, reply


# Send request to add TABLE to the schema
def add_table(share_name, name, location, account_id, description="", schema_name=predefs.default_schema_name):
    # Send request to add a SCHEMA to the share

    # Split path based on bucket or rel path
    matches = s3_regex.findall(location)
    if len(matches) != 2:
        raise RuntimeError()

    bucket, path = matches
    bucket_with_protocol = bucket if bucket.startswith("s3a") else "s3a" + bucket[1:]

    json_body = {
        "name": name,
        "storage": {
            "type": predefs.default_object_storage,
            "bucket": bucket_with_protocol,
            "path": path
        },
        "accountId": account_id,
        "format": {
            "type": predefs.default_format,
            "precision": predefs.default_precision
        },
        "presignedUrlValidityPeriod": predefs.default_url_validity_period,
        "description": description
    }

    success, reply = send_post(f"/shares/{share_name}/schemas/{schema_name}/tables", json_body)
    return success, reply


# Invite a user to a share
def create_invite(share_name, invitee_email, invitee_name):
    body_json = {"share": share_name,
                 "inviteeName": invitee_name,
                 "inviteeEmail": invitee_email}

    success, reply = send_post("/invitations", body_json)

    return success, reply
