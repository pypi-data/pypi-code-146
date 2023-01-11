from nonebot import get_driver
from nonebot.plugin.manager import PluginLoader

from .utils.ws_server import start_ws_server, stop_ws_server, start_rcon_connect
from . import plugins

driver = None
if isinstance(globals()["__loader__"], PluginLoader):
    driver = get_driver()


# Bot 连接时
@driver.on_bot_connect
async def on_start():
    # 启动 WebSocket 服务器
    await start_ws_server()
    await start_rcon_connect()


# Bot 断开时
@driver.on_bot_disconnect
async def on_close():
    # 关闭 WebSocket 服务器
    await stop_ws_server()
