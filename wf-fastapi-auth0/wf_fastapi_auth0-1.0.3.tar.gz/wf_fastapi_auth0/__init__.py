import os

from auth0.v3.management.users import Users
from auth0.v3.management.clients import Clients
from auth0.v3.authentication import GetToken
from fastapi import Depends, HTTPException, Request
from fastapi.security.http import HTTPBearer

from cachetools.func import ttl_cache
from jose import jwt
import requests


AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
API_AUDIENCE = os.environ.get("API_AUDIENCE")
ALGORITHMS = ["RS256"]
CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")

TOKEN_EMAIL_DOMAIN = os.environ.get("TOKEN_EMAIL_DOMAIN", "wildflower-tech.org")
TOKEN_DOMAIN = os.environ.get("TOKEN_DOMAIN", "wildflowerschools.org")


@ttl_cache(ttl=60 * 60 * 4)
def admin_token(audience=None):
    get_token = GetToken(AUTH0_DOMAIN, timeout=10)
    token = get_token.client_credentials(
        CLIENT_ID, CLIENT_SECRET, audience if audience is not None else f"https://{AUTH0_DOMAIN}/api/v2/"
    )
    api_token = token["access_token"]
    return api_token


async def verify_token(authorization=Depends(HTTPBearer())):
    if hasattr(authorization, "credentials"):
        token = authorization.credentials
    else:
        token = authorization
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = load_rsa_key(unverified_header["kid"])
    try:
        payload = jwt.decode(
            token, rsa_key, algorithms=ALGORITHMS, audience=API_AUDIENCE, issuer=f"https://{AUTH0_DOMAIN}/"
        )
        return payload
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(status_code=401, detail="token_expired") from e
    except jwt.JWTClaimsError as e:
        raise HTTPException(status_code=401, detail="invalid_claims") from e
    except Exception as e:
        raise HTTPException(status_code=401, detail="invalid_header") from e


async def get_profile(authorization: str = Depends(HTTPBearer())):
    authentication = await verify_token(authorization)
    if "gty" not in authentication:
        user_id = authentication["sub"]
        u = Users(AUTH0_DOMAIN, admin_token())
        return u.get(user_id)  # , ["email", "app_metadata"])
    gty = authentication["gty"]
    if gty == "client-credentials":
        clients = Clients(AUTH0_DOMAIN, admin_token())
        client_id = authentication["sub"].split("@")[0]
        return clients.get(client_id)
    raise HTTPException(status_code=401, detail="user_or_client_token_required")


async def get_subject_domain(authorization: str = Depends(HTTPBearer())):
    profile = await get_profile(authorization=authorization)
    primary_email = None
    domain = None
    if "primaryEmail" in profile:
        primary_email = profile["primaryEmail"]
        domain = primary_email.split("@")[1]

    if primary_email is None and "identities" in profile:
        for identity in profile["identities"]:
            if identity["provider"] == "google-apps":
                primary_email = identity["profileData"]["primaryEmail"]
                domain = primary_email.split("@")[1]

    if primary_email is None and "client_id" in profile:
        primary_email = f"{profile['name']}@{TOKEN_EMAIL_DOMAIN}"
        domain = TOKEN_DOMAIN

    if primary_email is None and "email" in profile and "email_verified" in profile:
        if profile["email_verified"]:
            primary_email = profile["email"]
            domain = primary_email.split("@")[1]

    if primary_email is None:
        raise HTTPException(status_code=401, detail="unable_to_verify_user_profile")

    return (primary_email, domain)


@ttl_cache(ttl=60 * 60)
def load_certs():
    return requests.get(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json", timeout=10).json()


@ttl_cache(ttl=60 * 60)
def load_rsa_key(kid):
    rsa_key = None
    jwks = load_certs()
    for key in jwks["keys"]:
        if key["kid"] == kid:
            rsa_key = {"kty": key["kty"], "kid": key["kid"], "use": key["use"], "n": key["n"], "e": key["e"]}
    return rsa_key
