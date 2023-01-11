import aiomcrcon
from nonebot import logger

from . import change_ip, change_port, change_password
from ..on_msg.data_source import RCON_CLIENTS
from ...database import DB as db


async def change_rcon_status(server_name):
    """更新Rcon状态"""
    for rcon in RCON_CLIENTS:
        # 如果服务器名匹配
        if rcon["server_name"] == server_name:
            # 获取该服务器的信息
            server = await db.get_server(server_name=server_name)
            # 如果两者都为关
            if not rcon["is_open"]:
                rcon["rcon"] = aiomcrcon.Client(
                    server.rcon_ip,
                    server.rcon_port,
                    server.rcon_password
                )
                try:
                    await rcon["rcon"].connect()
                    rcon["is_open"] = True
                    logger.success(f"[MC_QQ]丨[Server:{server.server_name}] 的Rcon连接成功")
                except aiomcrcon.RCONConnectionError:
                    logger.error(f"[MC_QQ]丨[Server:{server.server_name}] 的Rcon连接失败")
                except aiomcrcon.IncorrectPasswordError:
                    logger.error(f"[MC_QQ]丨[Server:{server.server_name}] 的Rcon密码错误")

            # 开关为否
            if not server.rcon_msg and not server.rcon_cmd and rcon["is_open"]:
                await rcon["rcon"].close()
                rcon["is_open"] = False
                logger.success(f"[MC_QQ]丨[Server:{server.server_name}] 的Rcon已关闭")
