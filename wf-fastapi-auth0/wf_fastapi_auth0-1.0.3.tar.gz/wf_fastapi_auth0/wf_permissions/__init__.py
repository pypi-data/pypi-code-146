import os
from typing import List

from fastapi import Depends, Request, HTTPException
from pydantic import BaseModel
import requests

from wf_fastapi_auth0 import get_subject_domain, admin_token


PERMS_API_URI = os.environ.get("PERMS_API_URI", "https://permissions.api.wildflower-tech.org")
PERMS_API_AUD = os.environ.get("PERMS_API_AUD", "wildflower-tech.org")


class Predicate(BaseModel):
    obj: str
    act: str


class AuthRequest(BaseModel):
    sub: str
    dom: str
    obj: str
    act: str


def access_patterns(predicates: List[Predicate]):
    async def wrapped(perm_info: tuple = Depends(get_subject_domain)):
        (sub, domain) = perm_info
        reqs = []
        for predicate in predicates:
            reqs.append(AuthRequest(sub=sub, dom=domain, obj=predicate.obj, act=predicate.act))
        return await check_requests(reqs)

    return wrapped


async def check_requests(reqs: List[AuthRequest]):
    payload = {"data": [r.dict() for r in reqs]}
    try:
        resp = requests.post(
            f"{PERMS_API_URI}/authz",
            json=payload,
            headers={"Authorization": f"bearer {admin_token(PERMS_API_AUD)}"},
            timeout=10,
        ).json()
        return resp["data"]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="permissions_not_verified") from e


def include_path_params(pattern: str):
    async def wrapped(request: Request):
        return pattern.format(**request.path_params)

    return wrapped
