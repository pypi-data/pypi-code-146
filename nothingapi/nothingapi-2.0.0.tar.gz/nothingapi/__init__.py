import requests
import json


def get_user(user_id: int):
    user = requests.get(f"https://nothingness.crypticcode.org/api/users/{user_id}")
    user = json.loads(user.text)
    return user

def get_guild(guild_id: int):
    guild = requests.get(f"https://nothingness.crypticcode.org/api/guilds/{guild_id}")
    guild = json.loads(guild.text)
    return guild