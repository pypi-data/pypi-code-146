import cloudscraper, websocket, json, time
from .authorization import Authorization
from .websockets import Websocket
from .utils.errors import errors

scraper = cloudscraper.create_scraper()

class Player:
    def __init__(self, dict: dict) -> None:
        self.thumbnail = dict["avatar"]
        self.betamount = dict["betAmount"]
        self.id = dict["_id"]
        self.username = dict["username"]

class Game:
    def __init__(self, info: dict):
        self.value = sum([player["betAmount"] for player in info["players"]])
        self.time = info["timeLeft"]
        self.status = info["status"]
        self.winner = info["winner"]
        self.winningColor = info["winningColor"]
        self.id = info["_id"]
        self.players = map(Player, info["players"])


class Jackpot:
    def __init__(self, auth: str) -> None:
        self.auth = auth

    class _Websocket:
        def __init__(self, auth: str) -> None:
            self.auth = auth
            self._connection = None

        def connect(self, headers: dict = None) -> websocket.WebSocket:
            """Connects to websocket and returns websocket object

            Parameters:
            headers (dict): Headers to be used to connect to websocket (Optional)

            Returns:
            websocket.WebSocket: A websocket connection connected and already logged in
            """

            self._connection = Websocket(headers) if headers else (Websocket())

            ws = self._connection
            ws.send("40/jackpot,")
            ws.send(f'42/jackpot,["auth","{self.auth}"]')

            return self._connection

        @property
        def connection(self) -> websocket.WebSocket:
            return self._connection

        def join(self, betamount: float, multiplier: float) -> None:
            """Joins Crash game with the betamount as well as multiplier"""

            json = str(
                {
                    "betAmount": betamount
                }
            ).replace("'", '"').replace(" ", "")
            self._connection.send(f'42/jackpot,["join-game",{str(json)}]')

    def Websocket(self):
        return self._Websocket(self.auth)

    @staticmethod
    def sniper(snipe_at: int = 0.05, interval: float = 0.01, on_game_start: type(print) = None) -> float:
        """Indefinitely yields the pot's value N seconds before wheel spins

        Parameters:
        amount (int): Amount of games to return each time
        interval (float): Time to wait in between each api request

        Returns:
        list: Recent games

        """

        if snipe_at > 29:
            raise errors.InvalidParameter("'snipe_at' cannot be above greater than 29")

        elif not callable(on_game_start) and on_game_start:
            raise errors.InvalidParameter("'on_game_start' must be a callable object.")

        while True:
            try:
                current = scraper.get("https://api.bloxflip.com/games/jackpot").json()["current"]
            except Exception as e:
                pass

            if len(current["players"]) == 2:
                time.sleep(30 - snipe_at)

                current = scraper.get("https://api.bloxflip.com/games/jackpot").json()["current"]

                pot_value = sum([player["betAmount"] for player in current["players"]])

                if on_game_start: on_game_start(pot_value)

                yield Game(current)

            time.sleep(interval)

    @property
    def current(self) -> float:
        """Returns the current game's pot value

        Returns:
        int: Current game's value
        """

        try:
            current = scraper.get("https://api.bloxflip.com/games/jackpot").json()["current"]
        except json.decoder.JSONDecodeError:
            raise errors.NetworkError("A Network Error has occurred")

        return Game(current)
