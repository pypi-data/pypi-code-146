from .brokerage import rest, iex
from .brokerage import vars


class Portal:
    def __apca_config_exist(self):
        config = all(
            [
                vars.BROKER_KEY,
                vars.BROKER_SECRET,
                vars.BROKER_API_URL,
                vars.MARKET_API_URL,
                vars.IEX_API_URL,
                vars.IEX_TOKEN,
            ]
        )
        if not config:
            raise NotImplementedError("ALPACA env Config not set")

    def __iex_config_exist(self):
        config = all(
            [
                vars.IEX_API_URL,
                vars.IEX_TOKEN,
            ]
        )
        if not config:
            raise NotImplementedError("IEX env Config not set")

    def get_broker_client(self) -> rest.Broker:
        self.__apca_config_exist()
        return rest.Broker()

    def get_market_client(self) -> rest.MarketData:
        self.__apca_config_exist()

        return rest.MarketData()

    def get_event_client(self) -> rest.BrokerEvents:
        self.__apca_config_exist()
        return rest.BrokerEvents()

    def get_iex_client(self) -> iex.PriceData:
        self.__iex_config_exist()
        return iex.PriceData()
