import copy
from datetime import datetime
from requests import post
from .credentials import Credentials
# from .types import AuthResponse

def verify_credentials(
  credentials: Credentials
  ):
  if is_authenticated(credentials):
    return credentials
  new_credentials = login(credentials)
  credentials.token = new_credentials.token
  credentials.token_expiration = new_credentials.token_expiration
  return credentials

def login(
  credentials: Credentials
  ) -> Credentials:
  if credentials.email is None or credentials.password is None:
    raise ValueError("Credentials not configured")

  response = post(
      f"{credentials.server}/auth/login",
      json={
          "email": credentials.email,
          "password": credentials.password,
      },
  )

  if not response.ok:
    raise ValueError("Invalid credentials")

  response_json = response.json()
  copied_credentials = copy.deepcopy(credentials)

  copied_credentials.token = response_json.get("token")
  copied_credentials.token_expiration = response_json.get("tokenPayload").get("expiresAt")

  return copied_credentials

def is_authenticated(credentials: Credentials) -> bool:
  if not credentials.token:
    return False

  now = datetime.utcnow()
  expirationDate = datetime.strptime(credentials.token_expiration, "%Y-%m-%dT%H:%M:%SZ")
  if now > expirationDate:
    return False

  # response = post(
  #     f"{credentials.server}/auth/authenticate",
  #     headers={"Authorization": f"Bearer {credentials.token}"},
  # )
  # return response.ok
  return True

# ---------------------------------------------------------------------------------

# def auth_login(
#   credentials: Credentials
#   ) -> AuthResponse:
#   response = post(
#     f"{credentials.server}/auth/login",
#     json={
#       "email": credentials.email,
#       "password": credentials.password
#       }
#   )
#   return response.json()

# def auth_refresh(
#   credentials: Credentials
#   ) -> AuthResponse:
#   response = post(
#     f"{credentials.server}/auth/refresh-token",
#     headers={"Authorization": f"Bearer {credentials.token}"},
#   )
#   return response.json()

# def auth_logout(
#   credentials: Credentials
#   ):
#   response = post(
#     f"{credentials.server}/auth/logout",
#     headers={"Authorization": f"Bearer {credentials.token}"},
#   )
#   return response.json()

# def auth_authenticate(
#   credentials: Credentials
#   ) -> AuthResponse:
#   response = post(
#     f"{credentials.server}/auth/authenticate",
#     headers={"Authorization": f"Bearer {credentials.token}"},
#   )
#   return response.json()