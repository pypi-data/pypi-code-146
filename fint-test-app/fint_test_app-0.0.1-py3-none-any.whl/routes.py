#  Copyright (c) 2023 actfint
#  Licensed under the BSD 3-Clause License
#  Created by @Wh1isper 2023/1/8

import random

from fastapi import APIRouter, Depends, WebSocket

from fps.hooks import register_router

from fint_test_app.auth import current_user, websocket_auth

r = APIRouter()


@r.get("/test")
async def reqeust_test(
    user=Depends(current_user)
):
    return user.dict()


@r.websocket("/test-ws")
async def websocket_test(
    websocket_permission=Depends(websocket_auth)
):
    if not websocket_permission:
        return

    websocket, user = websocket_permission
    websocket: WebSocket
    await websocket.accept()
    await websocket.send_json(user.dict())


router = register_router(r)
