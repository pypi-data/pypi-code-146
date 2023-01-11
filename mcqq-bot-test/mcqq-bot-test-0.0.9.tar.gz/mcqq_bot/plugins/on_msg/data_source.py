import json

import aiomcrcon
import websockets
from nonebot import get_bot, logger
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot_plugin_guild_patch import GuildMessageEvent

from typing import Union
from ...utils import process_msg_for_ws, send_msg_to_qq, get_type_id, process_msg_for_rcon
from ...database.db import server_list

CLIENTS = []
"""客户端列表"""
RCON_CLIENTS = []
"""Rcon 连接列表"""


async def ws_client(websocket):
    """WebSocket"""
    msg = {}
    try:
        async for message in websocket:
            msg = json.loads(message)
            if msg['event_name'] == "ConnectEvent":
                CLIENTS.append({
                    "server_name": msg['server_name'],
                    "ws_client": websocket,
                })
                logger.success(f"[MC_QQ]丨[Server:{msg['server_name']}] 已连接至 WebSocket 服务器")
            # 发送消息到QQ
            else:
                await send_msg_to_qq(bot=get_bot(), json_msg=msg)
    except websockets.WebSocketException:
        # 移除当前客户端
        CLIENTS.remove({"server_name": msg['server_name'], "ws_client": websocket})
    if websocket.closed:
        logger.error(f"[MC_QQ]丨[Server:{msg['server_name']}] 的 WebSocket 连接已断开")


async def send_msg_to_mc(bot: Bot, event: Union[GroupMessageEvent, GuildMessageEvent]):
    """发送消息到 MC"""
    # 处理来自QQ的消息
    client, server = await get_ws_client(event=event)
    rcon, server = await get_rcon_connect(event=event)
    # 如果 服务器的rcon已连接 且 服务器切换为rcon发送消息
    if rcon["is_open"] and server["rcon_msg"] and rcon["rcon"]:
        text_msg, msgJson = await process_msg_for_rcon(bot=bot, event=event)
        try:
            await rcon["rcon"].send_cmd(msgJson)
            logger.success(f"[MC_QQ_Rcon]丨发送至 [server:{client['server_name']}] 的消息 \"{text_msg}\"")
        except aiomcrcon.ClientNotConnectedError:
            logger.error(f"[MC_QQ]丨[Server:{client['server_name']}] 的Rcon未连接")

    elif client['ws_client']:
        text_msg, msgJson = await process_msg_for_ws(bot=bot, event=event)
        try:
            await client['ws_client'].send(msgJson)
            logger.success(f"[MC_QQ]丨发送至 [server:{client['server_name']}] 的消息 \"{text_msg}\"")
        except websockets.WebSocketException:
            logger.error(f"[MC_QQ]丨发送至 [Server:{client['server_name']}] 的过程中出现了错误")
            CLIENTS.remove(client)


async def send_command_to_mc(bot: Bot, event: Union[GroupMessageEvent, GuildMessageEvent]):
    """发送命令到 Minecraft"""
    rcon, server = await get_rcon_connect(event=event)
    if rcon["is_open"] and server["rcon_cmd"] and rcon["rcon"]:
        try:
            await bot.send(event, message=str(
                (await rcon["rcon"].send_cmd(event.raw_message.strip("/mcc")))[0]))
            logger.success(
                f"[MC_QQ_Rcon]丨发送至 [server:{rcon['server_name']}] 的命令 \"{event.raw_message.strip('/mcc')}\""
            )
        except aiomcrcon.ClientNotConnectedError:
            logger.error(f"[MC_QQ_Rcon]丨发送至 [Server:{rcon['server_name']}] 的过程中出现了错误")
            # 连接关闭则移除客户端
            RCON_CLIENTS.remove(rcon)


async def get_ws_client(event: Union[GroupMessageEvent, GuildMessageEvent]):
    """获取 服务器名、ws客户端、rcon连接"""
    for per_client in CLIENTS:
        for per_server in server_list:
            # 如果 服务器名 == ws客户端中记录的服务器名，且ws客户端存在
            if per_client['ws_client'] and per_server['server_name'] == per_client['server_name']:
                for per_group in per_server['all_group_list']:
                    if await get_type_id(event) == per_group["type_id"]:
                        return per_client, per_server
    return None


async def get_rcon_connect(event: Union[GroupMessageEvent, GuildMessageEvent]):
    """获取 服务器名、ws客户端、rcon连接"""
    for per_rcon in RCON_CLIENTS:
        for per_server in server_list:
            # 如果 服务器名 == ws客户端中记录的服务器名，且ws客户端存在
            if per_rcon['rcon'] and per_server['server_name'] == per_rcon['server_name']:
                for per_group in per_server['all_group_list']:
                    if await get_type_id(event) == per_group["type_id"]:
                        return per_rcon, per_server
    return None


async def connect_rcon():
    """服务器启动时，连接启用rcon的服务器"""
    for server in server_list:
        if (server.rcon_msg | server.rcon_cmd) and server.rcon_password != "change_password":
            rcon_client = aiomcrcon.Client(server.rcon_ip, server.rcon_port, server.rcon_password)
            try:
                await rcon_client.connect()
                # 连接成功后装入rcon连接列表
                for client in CLIENTS:
                    if server.server_name == client["server_name"]:
                        client["rcon_connection"]["rcon"] = rcon_client
                        client["rcon_connection"]["is_open"] = True
                    logger.success(f"[MC_QQ]丨[Server:{client['server_name']}] 的Rcon连接成功")
            except aiomcrcon.RCONConnectionError:
                logger.error(f"[MC_QQ]丨[Server:{server.server_name}] 的Rcon连接失败")
            except aiomcrcon.IncorrectPasswordError:
                logger.error(f"[MC_QQ]丨[Server:{server.server_name}] 的Rcon密码错误")
