import json
import os

from fastapi import Header, HTTPException, Request


async def verify_auth_token(request: Request, x_hub_rdv_auth_token: str = Header(None)):
    if os.environ.get("ALLOW_ORIGINS"):
        origin_url = dict(request.scope["headers"]).get(b"origin", b"").decode()
        if origin_url in os.environ.get("ALLOW_ORIGINS"):
            return
    if x_hub_rdv_auth_token not in json.loads(os.environ.get("AUTH_TOKENS")):
        raise HTTPException(
            status_code=401, detail="X-HUB-RDV-AUTH-TOKEN header invalid"
        )
