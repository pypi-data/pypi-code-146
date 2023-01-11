from typing import Optional


def _login_request_info(username: str, password: str, scope: Optional[str] = None) -> dict:
    data = {
        "client_id": "algora-api",
        "grant_type": "password",
        "username": username,
        "password": password
    }
    if scope is not None:
        data.update({'scope': scope})

    return {
        "url": f"https://auth.algoralabs.com/auth/realms/production/protocol/openid-connect/token",
        "data": data
    }


def _refresh_token_request_info(refresh_token: Optional[str] = None) -> dict:
    return {
        "url": f"https://auth.algoralabs.com/auth/realms/production/protocol/openid-connect/token",
        "data": {
            "client_id": "algora-api",
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
    }


def _token_exchange_request_info(requested_subject: str, subject_token: str) -> dict:
    data = {
        "client_id": "algora-api",
        "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
        "requested_subject": requested_subject,
        "subject_token": subject_token,
        "scope": "offline_access"
    }

    return {
        "url": f"https://auth.algoralabs.com/auth/realms/production/protocol/openid-connect/token",
        "data": data
    }
