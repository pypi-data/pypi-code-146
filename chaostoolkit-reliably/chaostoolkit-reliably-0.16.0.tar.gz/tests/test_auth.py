from chaosreliably import get_auth_info


def test_using_secret_only() -> None:
    auth_info = get_auth_info(None, {"token": "78890", "host": "reliably.dev"})
    assert auth_info["token"] == "78890"
    assert auth_info["host"] == "reliably.dev"


def test_missing_host_from_secrets() -> None:
    auth_info = get_auth_info(
        {},
        {"token": "78890", "org": "an-org"},
    )
    assert auth_info["token"] == "78890"
    assert auth_info["host"] == "app.reliably.com"
