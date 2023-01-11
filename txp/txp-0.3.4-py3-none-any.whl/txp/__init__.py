from txp.common.config import settings


def hello_txp() -> str:
    """Basic function to test Github actions CI"""
    return settings.testing.hello_world_message
