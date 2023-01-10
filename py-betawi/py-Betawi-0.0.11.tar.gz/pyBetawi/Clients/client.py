from geezlibs import Client

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
GEEZ1 = (
    Client(
        name="GEEZ1",
        api_id=Var.API_ID,
        api_hash=Var.API_HASH,
        session_string=Var.STRING_1,
        in_memory=True,
    )
    if Var.STRING_1
    else None
)


GEEZ2 = (
    Client(
        name="GEEZ2",
        api_id=Var.API_ID,
        api_hash=Var.API_HASH,
        session_string=Var.STRING_2,
        in_memory=True,
    )
    if Var.STRING_2
    else None
)
        
GEEZ3 = (
    Client(
        name="GEEZ3",
        api_id=Var.API_ID,
        api_hash=Var.API_HASH,
        session_string=Var.STRING_3,
        in_memory=True,
    )
    if Var.STRING_3
    else None
)

GEEZ4 = (
    Client(
        name="GEEZ4",
        api_id=Var.API_ID,
        api_hash=Var.API_HASH,
        session_string=Var.STRING_4,
        in_memory=True,
    )
    if Var.STRING_4
    else None
)

GEEZ5 = (
    Client(
        name="GEEZ5",
        api_id=Var.API_ID,
        api_hash=Var.API_HASH,
        session_string=Var.STRING_5,
        in_memory=True,
    )
    if Var.STRING_5
    else None
)

GEEZ6 = (
    Client(
        name="GEEZ6",
        api_id=Var.API_ID,
        api_hash=Var.API_HASH,
        session_string=Var.STRING_6,
        in_memory=True,
    )
    if Var.STRING_6
    else None
)


GEEZ7 = (
    Client(
        name="GEEZ7",
        api_id=Var.API_ID,
        api_hash=Var.API_HASH,
        session_string=Var.STRING_7,
        in_memory=True,
    )
    if Var.STRING_7
    else None
)
        
GEEZ8 = (
    Client(
        name="GEEZ8",
        api_id=Var.API_ID,
        api_hash=Var.API_HASH,
        session_string=Var.STRING_8,
        in_memory=True,
    )
    if Var.STRING_8
    else None
)


GEEZ9 = (
    Client(
        name="GEEZ9",
        api_id=Var.API_ID,
        api_hash=Var.API_HASH,
        session_string=Var.STRING_9,
        in_memory=True,
    )
    if Var.STRING_9
    else None
)
GEEZ10 = (
    Client(
        name="GEEZ10",
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
        GEEZ1, 
        GEEZ2, 
        GEEZ3, 
        GEEZ4, 
        GEEZ5, 
        GEEZ6, 
        GEEZ7, 
        GEEZ8,
        GEEZ9,
        GEEZ10,
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