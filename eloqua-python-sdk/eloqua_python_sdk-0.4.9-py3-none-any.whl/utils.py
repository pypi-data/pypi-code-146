from base64 import b64encode


def b64auth(username, password):
    return b64encode(bytes('{username}:{password}'.format(
        username=username, password=password)))
