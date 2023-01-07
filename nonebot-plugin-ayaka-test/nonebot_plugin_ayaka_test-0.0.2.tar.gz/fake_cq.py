'''FakeCQ'''
import asyncio
import json
from typing import Awaitable, Callable
from websockets.legacy.client import Connect
from .utils import run_in_startup, get_driver, logger

driver = get_driver()
logger.level("AYAKA", no=27, icon="⚡", color="<blue>")
FAKE_BOT_ID = 123456


class FakeCQ:
    def __init__(self) -> None:
        self.cmd_func_dict = {}
        self.api_func_dict = {}
        self._helps = []
        self.self_id = FAKE_BOT_ID
        self._data = {}

    def print(self, *args, colors=False, max_length: int = 3000):
        '''AYAKA日志输出'''
        info = " ".join(str(arg) for arg in args)
        info = info[:max_length]
        logger.opt(colors=colors).log("AYAKA", info)

    async def _connect(self):
        '''反相ws连接nb'''
        addr = f"ws://127.0.0.1:{driver.config.port}/onebot/v11/ws"
        self.conn = Connect(addr, extra_headers={"x-self-id": self.self_id})
        self.ws = await self.conn.__aenter__()

    async def connect(self):
        '''反相ws连接nb，最多重试3次'''
        retry_cnt = 0
        while retry_cnt <= 3:
            try:
                await self._connect()
                break
            except:
                retry_cnt += 1
                self.print(f"FakeCQ连接失败，正在重试 retry_cnt {retry_cnt}/3")
        else:
            self.print("FakeCQ连接失败，已超最大重试次数")
            return

        # 启动收发循环
        asyncio.create_task(self.terminal_loop())
        asyncio.create_task(self.fake_cq_loop())

        # 发送帮助
        self.print("<g>AYAKA_TEST</g> 已启动", colors=True)
        self.print(f"BOT_ID: {self.self_id}")
        self.print_help()

    def print_help(self):
        '''打印帮助'''
        for h in self._helps:
            self.print(h, colors=True)

    async def unknown_terminal_cmd(self, *args, **kwargs):
        self.print("未定义的终端命令")

    async def terminal_deal(self, line: str):
        '''处理来自终端的输入'''
        line = line.strip()
        if not line:
            return
        for cmd in self.cmd_func_dict:
            if line.startswith(cmd):
                func = self.cmd_func_dict[cmd]
                text = line[len(cmd):].strip()
                break
        else:
            func = self.unknown_terminal_cmd
            text = ""

        await func(text)

    async def terminal_loop(self):
        '''通过终端向nonebot发消息'''
        loop = asyncio.get_event_loop()
        while True:
            line = await loop.run_in_executor(None, input)
            await self.terminal_deal(line)

    async def unknown_fake_cq_api(self, *args, **kwargs):
        self.print("未定义的假cqhttp api")

    async def fake_cq_loop(self):
        '''作为虚假的cq，回复nb发出的请求'''
        while True:
            text = await self.ws.recv()
            data = json.loads(text)
            action = data["action"]
            self.print(f"<y>{action}</y>", colors=True)
            func = self.api_func_dict.get(action, self.unknown_fake_cq_api)
            await func(data["echo"], data["params"])

    def on_cmd(self, cmd):
        '''注册终端命令回调'''
        def decorator(func: Callable[[str], Awaitable]):
            doc = func.__doc__ if func.__doc__ else func.__name__
            doc = doc.replace("<", "\<")
            self._helps.append(f"<y>{cmd}</y> {doc}")
            self.cmd_func_dict[cmd] = func
            return func
        return decorator

    def on_api(self, api):
        '''注册假cqhttp api回调'''
        def decorator(func: Callable[[int, dict], Awaitable]):
            self.api_func_dict[api] = func
            return func
        return decorator

    async def send_json(self, data: dict):
        await self.ws.send(json.dumps(data))

    async def send_echo(self, echo: int, response_data={}):
        '''向nonebot发送假应答消息'''
        data = {
            'data': response_data,
            'echo': echo,
            'retcode': 0,
            'status': 'ok'
        }
        await self.send_json(data)


fake_cq = FakeCQ()


@run_in_startup
async def startup():
    asyncio.create_task(fake_cq.connect())
