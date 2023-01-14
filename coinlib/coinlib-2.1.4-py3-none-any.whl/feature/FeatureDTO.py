from typing import List

from coinlib.helper import Serializable


class FeatureData(Serializable):
    identifier: str
    title: str
    type: str
    description: str
    group: str
    groupDescription: str
    exchange: bool
    symbol: bool
    interval: int
    url: str
    icon: str

    @staticmethod
    def create(identifier, title, description=None, group=None, groupDescription=None, unit="", formatType=None, format=None, symbol=False, exchange=False, url=None, icon=None, interval=None):
        f = FeatureData()

        f.identifier = identifier
        f.title = title
        f.description = description
        f.icon = icon
        f.url = url
        f.exchange = exchange
        f.symbol = symbol
        f.unit = unit
        f.format = format
        f.formatType = formatType
        f.interval = interval
        f.group = group
        f.groupDescription = groupDescription


        return f

class FeatureTargetCollection(Serializable):
    chart_id: str
    workspace_id: str
    chart_prefix: str
    activity_id: str

class FeaturesInfo(Serializable):
    name: str
    group: str

class FeatureFetcherDTO(Serializable):
    start: str
    end: str
    features: List[FeaturesInfo]
    symbol: str
    exchange: str
    targetDatabase: FeatureTargetCollection

class RabbitInfo(Serializable):
    ip: str
    port: str
    prefix: str
    user: str
    pwd: str

    def __init__(self):
        self.ip = "78.47.96.243"
        self.port = "5672"
        self.user = "thoren"
        self.pwd = "thoren"



class FeatureDatabaseInfo(Serializable):
    server: str
    id: str

class FeatureLakeData(Serializable):
    pass

class FeatureInfos(Serializable):
    pass


class ProcessResponse(Serializable):
    pass