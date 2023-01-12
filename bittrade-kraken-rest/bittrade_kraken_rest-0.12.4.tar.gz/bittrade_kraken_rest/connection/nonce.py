from datetime import datetime


def get_nonce():
    return int(datetime.now().timestamp() * 1e3)
