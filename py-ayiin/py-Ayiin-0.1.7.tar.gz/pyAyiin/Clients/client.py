from fipper import Client

from ..config import Var as Variable

Var = Variable()


hndlr = f"{Var.HNDLR[0]} {Var.HNDLR[1]} {Var.HNDLR[2]} {Var.HNDLR[3]} {Var.HNDLR[4]} {Var.HNDLR[5]}"

'''
try:
    import pytgcalls
except ImportError:
    print("'pytgcalls' not found")
    pytgcalls = None
'''


tgbot = (
    Client(
        name="tgbot",
        api_id=Var.API_ID,
        api_hash=Var.API_HASH,
        bot_token=Var.BOT_TOKEN,
    )
)

# For Publik Repository
AYIIN1 = (
    Client(
        name="AYIIN1",
        api_id=Var.API_ID,
        api_hash=Var.API_HASH,
        session_string=Var.STRING_1,
        in_memory=True,
    )
    if Var.STRING_1
    else None
)


AYIIN2 = (
    Client(
        name="AYIIN2",
        api_id=Var.API_ID,
        api_hash=Var.API_HASH,
        session_string=Var.STRING_2,
        in_memory=True,
    )
    if Var.STRING_2
    else None
)
        
AYIIN3 = (
    Client(
        name="AYIIN3",
        api_id=Var.API_ID,
        api_hash=Var.API_HASH,
        session_string=Var.STRING_3,
        in_memory=True,
    )
    if Var.STRING_3
    else None
)

AYIIN4 = (
    Client(
        name="AYIIN4",
        api_id=Var.API_ID,
        api_hash=Var.API_HASH,
        session_string=Var.STRING_4,
        in_memory=True,
    )
    if Var.STRING_4
    else None
)

AYIIN5 = (
    Client(
        name="AYIIN5",
        api_id=Var.API_ID,
        api_hash=Var.API_HASH,
        session_string=Var.STRING_5,
        in_memory=True,
    )
    if Var.STRING_5
    else None
)

AYIIN6 = (
    Client(
        name="AYIIN6",
        api_id=Var.API_ID,
        api_hash=Var.API_HASH,
        session_string=Var.STRING_6,
        in_memory=True,
    )
    if Var.STRING_6
    else None
)


AYIIN7 = (
    Client(
        name="AYIIN7",
        api_id=Var.API_ID,
        api_hash=Var.API_HASH,
        session_string=Var.STRING_7,
        in_memory=True,
    )
    if Var.STRING_7
    else None
)
        
AYIIN8 = (
    Client(
        name="AYIIN8",
        api_id=Var.API_ID,
        api_hash=Var.API_HASH,
        session_string=Var.STRING_8,
        in_memory=True,
    )
    if Var.STRING_8
    else None
)


AYIIN9 = (
    Client(
        name="AYIIN9",
        api_id=Var.API_ID,
        api_hash=Var.API_HASH,
        session_string=Var.STRING_9,
        in_memory=True,
    )
    if Var.STRING_9
    else None
)
AYIIN10 = (
    Client(
        name="AYIIN10",
        api_id=Var.API_ID,
        api_hash=Var.API_HASH,
        session_string=Var.STRING_10,
        in_memory=True,
    )
    if Var.STRING_10
    else None
)


Bots = [
    bot for bot in [
        AYIIN1, 
        AYIIN2, 
        AYIIN3, 
        AYIIN4, 
        AYIIN5, 
        AYIIN6, 
        AYIIN7, 
        AYIIN8,
        AYIIN9,
        AYIIN10,
    ] if bot
]

'''
if pytgcalls is not None:
    for bot in Bots:
        if not hasattr(bot, "group_call"):
            try:
                setattr(bot, "group_call", pytgcalls.GroupCallFactory(bot).get_group_call())
            except AttributeError:
                pass
'''
