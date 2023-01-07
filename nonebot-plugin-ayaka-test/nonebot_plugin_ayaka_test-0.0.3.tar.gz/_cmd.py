'''拓展FakeCQ的终端命令'''
import asyncio
from pathlib import Path
from time import time
from .utils import load_data_from_file, safe_split
from .fake_cq import fake_cq
from .record import record


@fake_cq.on_cmd("d")
async def delay(text: str):
    '''<n> | 延时n秒，缺省为1秒'''
    try:
        n = float(text.strip())
    except:
        n = 1
    await asyncio.sleep(n)
    print()


@fake_cq.on_cmd("g")
async def send_group_msg(text: str):
    '''<group_id> <user_id> <text> | 发送群聊消息'''
    gid, uid, text = safe_split(text, 3)
    try:
        gid = int(gid)
        uid = int(uid)
    except:
        return

    name = f"测试{uid}号"
    data = {
        "post_type": "message",
        "message_type": "group",
        "time": int(time()),
        "self_id": fake_cq.self_id,
        "sub_type": "normal",
        "sender": {
            "age": 0,
            "area": "",
            "card": name,
            "level": "",
            "nickname": name,
            "role": "owner",
            "sex": "unknown",
            "title": "",
            "user_id": uid
        },
        "message_id": -1,
        "anonymous": None,
        "font": 0,
        "raw_message": text,
        "user_id": uid,
        "group_id": gid,
        "message": text,
        "message_seq": 0
    }

    # 回显
    fake_cq.print(f"群聊({gid}) <y>{name}</y>({uid}) 说：", colors=True)
    fake_cq.print(text)
    record(name, text)

    # 发送假cqhttp消息
    await fake_cq.send_json(data)


@fake_cq.on_cmd("p")
async def send_private_msg(text: str):
    '''<user_id> <text> | 发送私聊消息'''
    uid, text = safe_split(text, 2)
    try:
        uid = int(uid)
    except:
        return

    name = f"测试{uid}号"
    bot_id = fake_cq.self_id
    data = {
        "post_type": "message",
        "message_type": "private",
        "time": int(time()),
        "self_id": bot_id,
        "sub_type": "friend",
        "user_id": uid,
        "target_id": bot_id,
        "message": text,
        "raw_message": text,
        "font": 0,
        "sender": {
            "age": 0,
            "nickname": name,
            "sex": "unknown",
            "user_id": uid
        },
        "message_id": -1
    }

    # 回显
    fake_cq.print(f"私聊({uid}) <y>{name}</y> 说：", colors=True)
    fake_cq.print(text)
    record(name, text)

    # 发送假cqhttp消息
    await fake_cq.send_json(data)


@fake_cq.on_cmd("#")
async def do_nothing(text: str):
    '''注释'''
    return


@fake_cq.on_cmd("after")
async def set_after(line: str):
    '''<line> | 设置脚本每行代码执行完毕后，再执行的内容'''
    fake_cq.config.after = line


@fake_cq.on_cmd("s")
async def run_script(name: str):
    '''<name> | 执行 script/<name>.txt自动化脚本'''
    path = Path("script", name).with_suffix(".txt")
    if not path.is_file():
        fake_cq.print("脚本不存在")
        return

    lines: list[str] = load_data_from_file(path)

    for line in lines:
        print(f"{name}>", line)
        await fake_cq.terminal_deal(line)
        after = fake_cq.config.after
        await fake_cq.terminal_deal(after)


@fake_cq.on_cmd("r")
async def set_record(text: str):
    '''0/1 | 关闭/启动record，默认为关闭'''
    try:
        fake_cq.config.record = int(text) > 0
    except:
        return

    if fake_cq.config.record:
        fake_cq.print("已开启record")
    else:
        fake_cq.print("已关闭record")


@fake_cq.on_cmd("h")
async def _(text: str):
    '''帮助'''
    fake_cq.print_help()
