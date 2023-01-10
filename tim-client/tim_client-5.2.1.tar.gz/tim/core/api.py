import json
import requests
from typing import Any, TypeVar, Optional
from .credentials import Credentials
from .authentication import verify_credentials

T = TypeVar('T')

def execute_request(
    credentials: Credentials,
    method: str,
    path: str,
    body: Optional[Any] = None,
    params: Optional[Any] = None,
    file: Optional[str] = None,
) -> Any:
  verified_credentials = verify_credentials(credentials)
  headers = {
      "Authorization": f"Bearer {verified_credentials.token}",
      "X-Tim-Client": verified_credentials.client_name,
  }

  upload_file = lambda: requests.request(
      method=method,
      url=f"{verified_credentials.server}{path}",
      headers=headers,
      files={
          "configuration": json.dumps(body),
          "file": file,
      },
  )

  handle_request = lambda: requests.request(
      method=method,
      url=f"{verified_credentials.server}{path}",
      json=body,
      params=params,
      headers=headers,
  )

  response = upload_file() if file else handle_request()

  if not response.ok:
    if response.status_code == 500:
      raise ValueError("Internal error. Please contact support.")

    raise ValueError(json.loads(response.text)["message"])

  if response.headers.get('content-type') == 'application/json':
    return response.json()

  return response.text