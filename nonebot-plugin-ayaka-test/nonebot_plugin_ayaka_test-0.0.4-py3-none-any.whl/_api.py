'''拓展FakeCQ的假cqhttp api'''
from .utils import base64_to_pic
from .fake_cq import fake_cq
from .record import record


def handle_message(message):
    '''message 可能是cqhttp格式的node数组'''
    if isinstance(message, list):
        def handle(node: dict):
            if node["type"] == "text":
                return node["data"]["text"]
            if node["type"] == "image":
                if "file" in node["data"]:
                    return base64_to_pic(node["data"]["file"])
            return str(node)
        return "".join(handle(m) for m in message)
    return str(message)


@fake_cq.on_api("send_msg")
async def _(echo: int, params: dict):
    message_type = params["message_type"]
    if message_type == "group":
        await group_msg(echo, params)
    else:
        await private_msg(echo, params)


@fake_cq.on_api("send_private_msg")
async def private_msg(echo: int, params: dict):
    uid = params["user_id"]
    text = handle_message(params["message"])
    fake_cq.print(
        f"<r>Ayaka Bot</r>({fake_cq.self_id}) 对私聊({uid}) 说：", colors=True)
    fake_cq.print(text)
    await fake_cq.send_echo(echo)


@fake_cq.on_api("send_group_msg")
async def group_msg(echo: int, params: dict):
    gid = params["group_id"]
    try:
        text = handle_message(params["message"])
    except:
        text = str(params["message"])
    fake_cq.print(
        f"群聊({gid}) <r>Ayaka Bot</r>({fake_cq.self_id}) 说：", colors=True)
    fake_cq.print(text)
    await fake_cq.send_echo(echo)


@fake_cq.on_api("send_group_forward_msg")
async def _(echo: int, params: dict):
    gid = params["group_id"]
    messages = params["messages"]
    items = []
    for m in messages:
        uid = m["data"]["user_id"]
        name = m["data"]["nickname"]
        text = m["data"]["content"]
        items.append(f"<y>{name}</y>({uid}) 说：\n{text}")
    fake_cq.print(f"群聊({gid}) 收到<y>合并转发</y>消息", colors=True)
    fake_cq.print("\n\n".join(items))
    await fake_cq.send_echo(echo)


@fake_cq.on_api("get_friend_list")
@fake_cq.on_api("get_group_member_list")
async def _(echo: int, params: dict):
    # 假装这个群有100个人，分别叫测试1-100号
    # 假装这个人有100个好友，分别叫测试1-100号
    data = [
        {
            "user_id": i,
            "card": f"测试{i}号",
            "nickname": f"测试{i}号"
        } for i in range(100)
    ]
    await fake_cq.send_echo(echo, data)


@fake_cq.on_api("get_msg")
async def get_msg(echo: int, params: dict):
    message = "https://m.weibo.cn/status/Md07njxZ7"
    message_id = params["message_id"]
    data = {
        "message": message,
        "message_id": message_id,
        "message_type": "group", "real_id": 1,
        "sender": {"nickname": "测试6号", "user_id": 6},
        "time": 1667308483
    }
    await fake_cq.send_echo(echo, data)


@fake_cq.on_api("delete_msg")
async def delete_msg(echo: int, params: dict):
    await fake_cq.send_echo(echo, params)
    fake_cq.print(f"<r>系统</r> 说：\n已撤回", colors=True)


@fake_cq.on_api("send_msg")
async def record_send_msg(echo: int, params: dict):
    message_type = params["message_type"]
    if message_type == "group":
        await record_group_msg(echo, params)
    else:
        await record_private_msg(echo, params)


@fake_cq.on_api("send_private_msg")
async def record_private_msg(echo: int, params: dict):
    text = handle_message(params["message"])
    record("Bot", text)


@fake_cq.on_api("send_group_msg")
async def record_group_msg(echo: int, params: dict):
    try:
        text = handle_message(params["message"])
    except:
        text = str(params["message"])
    record("Bot", text)


@fake_cq.on_api("send_group_forward_msg")
async def record_group_forward_msg(echo: int, params: dict):
    messages = params["messages"]
    for m in messages:
        name = m["data"]["nickname"]
        text = m["data"]["content"]
        record("Bot", text)
