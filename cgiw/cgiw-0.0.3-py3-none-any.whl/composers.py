from typing import Any

from .schemas import HeadersType

def compose_response(status: str, headers: HeadersType, body: Any) -> str:
    formatted_headers = '\n'.join([f"{k}: {v}" for k, v in headers.items()])
    return f"Status: {status}\n{formatted_headers}\n\n{body}"