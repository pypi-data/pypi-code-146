import enum
import requests
from investaholic_common.representation.ticker_representation import TickerRepresentation
from investaholic_common.representation.user_representation import UserRepresentation


class EntitySet(enum.Enum):
    TICKERS = enum.auto()
    USERS = enum.auto()


class Statistics:
    _URL = 'http://127.0.0.1:5000'

    @staticmethod
    def get_all_users():
        response = requests.get(f'{Statistics._URL}/users')
        if isinstance(response.json(), list):
            users = []
            for user in response.json():
                users.append(UserRepresentation.as_object(user))
            return users
        return UserRepresentation.as_object(response.json())

    @staticmethod
    def get_all_tickers_symbols():
        tickers = Statistics._get_all_entities(entity_set=EntitySet.TICKERS)
        if isinstance(tickers, list):
            return [x.symbol for x in tickers]
        return tickers.symbol

    @staticmethod
    def _get_all_entities(entity_set: EntitySet):
        response = requests.get(f'{Statistics._URL}/{entity_set.name.lower()}')
        if response.status_code != 200:
            raise ConnectionError(f'GET tickers returned {response.status_code}:{response.text}')

        match entity_set:
            case EntitySet.TICKERS:
                repr_class = TickerRepresentation
            case EntitySet.USERS:
                repr_class = UserRepresentation
            case _:
                raise ValueError('Entity set not managed in statistics')

        if isinstance(response.json(), list):
            entities = []
            for entity in response.json():
                entities.append(repr_class.as_object(entity))
            return entities
        return repr_class.as_object(response.json())