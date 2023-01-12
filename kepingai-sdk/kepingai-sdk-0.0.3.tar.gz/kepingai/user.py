from kepingai.api import KepingApi


class User:
    def __init__(self, api: KepingApi):
        self.api = api

    def get_balance(self, wallet_id: str = ''):
        params = {"wallet_id": wallet_id}
        return self.api.get(params=params, tag="user/balance")

    def get_bot_data(self, bot_id: str = ''):
        params = {"bot_id": bot_id}
        return self.api.get(params=params, tag="user/bot")
