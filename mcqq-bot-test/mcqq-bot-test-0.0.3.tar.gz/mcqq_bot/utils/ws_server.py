import aiomcrcon
import websockets
from nonebot import logger

from ..database.models import Server
from ..plugins.on_msg.data_source import ws_client, RCON_CLIENTS
from ..plugins.rcon import change_rcon_status
from ..utils import config
from ..database.db import server_list


async def start_ws_server():
    """启动 WebSocket 服务器"""
    global ws
    ws = await websockets.serve(ws_client, config.get_mc_qq_ws_ip(), config.get_mc_qq_ws_port())
    logger.success("[MC_QQ]丨WebSocket 服务器已开启")


async def stop_ws_server():
    """关闭 WebSocket 服务器"""
    global ws
    ws.close()
    logger.success("[MC_QQ]丨WebSocket 服务器已关闭")


async def start_rcon_connect():
    servers = Server.all()
    async for server in servers:
        if server.rcon_msg | server.rcon_cmd:
            rcon_client = aiomcrcon.Client(server.rcon_ip, server.rcon_port, server.rcon_password)

            try:
                await rcon_client.connect()
                rcon_client_status = True
                RCON_CLIENTS.append({
                    "server_name": server.server_name,
                    "rcon": rcon_client,
                    "is_open": rcon_client_status
                })
                logger.success(f"[MC_QQ]丨[Server:{server.server_name}] 的Rcon连接成功")
            except aiomcrcon.RCONConnectionError:
                logger.error(f"[MC_QQ]丨[Server:{server.server_name}] 的Rcon连接失败")
            except aiomcrcon.IncorrectPasswordError:
                logger.error(f"[MC_QQ]丨[Server:{server.server_name}] 的Rcon密码错误")
