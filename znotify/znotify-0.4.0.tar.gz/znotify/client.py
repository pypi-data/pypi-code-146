import requests

from znotify.static import ENDPOINT, Priority
from znotify.version import __version__


class Client:
    def __init__(self, user_id: str, endpoint: str):
        self.endpoint = endpoint if endpoint else ENDPOINT
        self.user_id = user_id
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": f"znotify-py-sdk/{__version__}",
        })

    @staticmethod
    def create(user_id: str, endpoint: str = None) -> "Client":
        client = Client(user_id, endpoint)
        client.check()
        return client

    def check(self):
        resp = self.session.get(f"{self.endpoint}/check", params={"user_secret": self.user_id})
        if not resp.json()["body"]:
            raise Exception("User ID not valid")

    def send(self, content: str, title: str = None, long: str = None, priority: Priority = None):
        if content is None or content == "":
            raise Exception("Content is required")

        if title is None:
            title = "Notification"
        if long is None:
            long = ""
        if priority is None:
            priority = Priority.NORMAL

        data = {
            "title": title,
            "content": content,
            "long": long,
            "priority": priority.value,
        }

        resp = self.session.post(f"{self.endpoint}/{self.user_id}/send", data=data)
        return resp.json()["body"]
