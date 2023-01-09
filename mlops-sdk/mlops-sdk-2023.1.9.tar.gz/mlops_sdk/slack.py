from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import hvac


def get_secrets(mount_point, path, parse_data=True):
    vault_client = hvac.Client()
    data = vault_client.secrets.kv.v2.read_secret_version(mount_point=mount_point, path=path)
    if parse_data:
        data = data["data"]["data"]
    return data


"""
Slack연동과 관련된 function list입니다.
"""
token = get_secrets(mount_point="datafabric", path="mlops/access/slack")["token"]
username = "jerryjung@emart.com"
channel = "#emart_dt_report"
icon_emoji = ":large_blue_circle:"


def send(
    text="This is default text",
    blocks=None,
    channel=None,
    dataframe=False,
):

    """
    Report channel에 Slack message를 보냅니다.
    ## Args
     text="This is default text",
     channel="#channel_name",
     dataframe=True|False,
    ## Returns
        None
    ## Example
    ```python
        slack.send(text=text)
    ```
    """
    import requests

    if dataframe:
        from tabulate import tabulate

        text = "```" + tabulate(text, tablefmt="simple", headers="keys") + "```"
    headers = {
        "Content-Type": "application/json;charset=utf-8",
        "Authorization": f"Bearer {token}",
    }
    json_body = {
        "username": username,
        "channel": channel,
        "text": text,
        "blocks": blocks,
        "icon_emoji": icon_emoji,
    }

    r = requests.post(
        "https://www.slack.com/api/chat.postMessage",
        headers=headers,
        json=json_body,
    )
    r.raise_for_status()
    if not r.json()["ok"]:
        raise Exception(r.json())


def send_file(file_name=None, channel=None):
    """
    Report channel에 file로 slack message를 보냅니다.
    ## Args
     file_name="./test.txt"
     channel="#channel_name"
    ## Returns
        None
    ## Example
    ```python
        data = slack.send_file(file_name="./text.txt"])
    ```
    """
    client = WebClient(token=token)
    try:
        filepath = file_name
        response = client.files_upload(channels=channel, file=filepath)
        assert response["file"]  # the uploaded file
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")
