import cloudscraper, json
from .utils.errors import errors

scraper = cloudscraper.create_scraper()

class Account:
    """An object for a user's account info"""

    def __init__(self, info: dict) -> None:
        self.games_played = info["gamesPlayed"]
        self.games_won = info["gamesWon"]
        self.account_verified = info["hasVerifiedAccount"]
        self.total_deposited = info["totalDeposited"]
        self.total_withdrawn = info["totalWithdrawn"]
        self.total_wagered = info["wager"]
        self.username = info["user"]["robloxUsername"]
        self.id = info["user"]["robloxId"]
        self.rank = info["user"]["rank"]
        self.balance = info["user"]["wallet"]

class User:
    """A class for the lookup info on somebodies account"""

    def __init__(self, info: dict, user_id: str, bet_amount: int) -> None:
        self.rank = info["rank"]
        self.username = info["username"]
        self.wagered = info["wager"]
        self.games_played = info["gamesPlayed"]
        self.rain_winnings = info["rainWinnings"]
        self.trivia_winnings = info["triviaWinnings"]
        if bet_amount: self.bet_amount = bet_amount
        self.id = user_id


class Authorization:
    def __init__(self) -> None:
        pass

    @staticmethod
    def generate(cookie: str, affiliate: str = "BFSB") -> str:
        """Generate a Bloxflip Auth Token from a Roblox Cookie"""

        request = scraper.post("https://api.bloxflip.com/user/login", json={
            "affiliateCode": affiliate,
            "cookie": cookie
        }).json()

        if "jwt" in list(request):
            return request["jwt"]

        raise errors.GeneralError("Either cookie is invalid or cookie is ip locked.")

    @staticmethod
    def validate(auth: str) -> bool:
        """Validates that the Authorization Token works"""

        request = scraper.get("https://api.bloxflip.com/user", headers={
            "x-auth-token": auth
        }).json()

        if request["success"]:
            return True

        return False

    @staticmethod
    def get_info(auth: str) -> User:
        """Gets user's info then returns in a class"""

        try:
            request = scraper.get("https://api.bloxflip.com/user", headers={
                "x-auth-token": auth
            }).json()
        except json.decoder.JSONDecodeError:
            raise errors.NetworkError("Network Error.")

        try:
            return Account(request)
        except KeyError:
            raise errors.InvalidAuthorization("Invalid Authorization provided")

    @staticmethod
    def lookup(user_id: str, bet_amount: int = None) -> User:
        try:
            request = scraper.get(f"https://api.bloxflip.com/user/lookup/{user_id}").json()
        except json.decoder.JSONDecodeError:
            raise errors.NetworkError("Network Error.")

        if not request["success"]:
            raise errors.InvalidParameter("Invalid UserID")

        try:
            return User(request, str(user_id), bet_amount)
        except KeyError:
            raise errors.InvalidAuthorization("Invalid Authorization provided")
