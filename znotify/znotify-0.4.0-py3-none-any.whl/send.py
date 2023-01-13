from znotify import Client


def send(user_id, content, title=None, long=None):
    client = Client.create(user_id)
    return client.send(content, title, long)
