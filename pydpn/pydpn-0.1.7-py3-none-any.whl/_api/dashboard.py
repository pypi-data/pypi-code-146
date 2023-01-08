from dataclasses import dataclass
from pydpn._api.api_base import ApiBase
from pydpn._api.mode import DpnMode


@dataclass
class SystemInfo:
    pass


@dataclass
class RealtimeTraffic:
    pass


@dataclass
class WorldmapData:
    pass


class Dashboard(ApiBase):
    @property
    def dpnMode(self) -> int:
        """get the dpn mode

        Returns:
            DpnMode: dpn Mode
        """
        desc = {
            "serviceName": "dpnMode",
            "refUrl": self.refUrl,
            "apiRoute": "smartRoute/getDpnMode",
            "requestMethod": "GET",
            "responseType": dict,
            "responseContent": {"dpnMode": str, "tunnelCode": str},
            "responseAlias": {},
            "returnType": DpnMode,
        }

        return self.deeper._api_call(desc)

    @property
    def memory(self) -> int:
        """get memory used in %

        Returns:
            int: memory used
        """
        desc = {
            "serviceName": "memory",
            "refUrl": self.refUrl,
            "apiRoute": "liquid",
            "requestMethod": "GET",
            "responseType": dict,
            "responseContent": {"scale": int},
            "responseAlias": {"scale": "memory"},
            "returnType": int,
        }

        return self.deeper._api_call(desc)

    @property
    def cpu(self) -> int:
        """get cpu load in %

        Returns:
            int: cpu load
        """
        desc = {
            "serviceName": "cpu",
            "refUrl": self.refUrl,
            "apiRoute": "speedometer",
            "requestMethod": "GET",
            "responseType": dict,
            "responseContent": {"guage": int},
            "responseAlias": {"guage": "cpu"},
            "returnType": int,
        }

        return self.deeper._api_call(desc)

    @property
    def systemInfo(self) -> SystemInfo:
        """get system information

        Returns:
            SystemInfo:
                attrs:
                    - systemUpTime
                    - totalUploads
                    - totalDownloads

        """

        desc = {
            "serviceName": "systemInfo",
            "refUrl": self.refUrl,
            "apiRoute": "info",
            "requestMethod": "GET",
            "responseType": list,
            "responseContent": [
                ("systemUpTime", str),
                ("totalUploads", str),
                ("totalDownloads", str),
            ],
            "returnType": SystemInfo,
        }

        return self.deeper._api_call(desc)

    @property
    def realtimeTraffic(self) -> RealtimeTraffic:
        """get realtime traffic information

        Returns:
            RealtimeTraffic: _description_
        """
        desc = {
            "serviceName": "realtimeTraffic",
            "refUrl": self.refUrl,
            "apiRoute": "dynamic-data",
            "requestMethod": "GET",
            "responseType": dict,
            "responseContent": {
                "downLoadData": list,
                "upLoadData": list,
                "xData": list,
            },
            "returnType": RealtimeTraffic,
        }

        return self.deeper._api_call(desc)

    @property
    def worldmapData(self) -> WorldmapData:
        """get world map information

        Returns:
            WorldmapData: _description_
        """
        desc = {
            "serviceName": "worldmapData",
            "refUrl": self.refUrl,
            "apiRoute": "worldmap-data",
            "requestMethod": "GET",
            "responseType": dict,
            "responseContent": {
                "self": dict,
                "peerList": list,
            },
            "returnType": WorldmapData,
        }
        return self.deeper._api_call(desc)

    @property
    def inform(self) -> list:
        """get world map information

        Returns:
            WorldmapData: _description_
        """
        desc = {
            "serviceName": "inform",
            "refUrl": self.refUrl,
            "apiRoute": "inform",
            "requestMethod": "GET",
            "responseType": list,
            "responseContent": str,
            "returnType": list,
        }
        return self.deeper._api_call(desc)


# class SystemInfo:
#     def __init__(self, inList: list) -> None:

#         if isinstance(inList, list):
#             dlen = len(inList)
#             if dlen < 3:
#                 inList.extend([None] * dlen - 3)
#         else:
#             inList = [None, None, None]

#         self.systemUp = inList[0]
#         self.totalUploads = inList[1]
#         self.totalDownloads = inList[2]

#     def __dict__(self):
#         return {
#             "systemUp": self.systemUp,
#             "totalUploads": self.totalUploads,
#             "totalDownloads": self.totalDownloads,
#         }

#     def __repr__(self) -> str:
#         return json.dumps(self.__dict__())


# class Dashboard(OptionsBase):
#     def __init__(self, deeper) -> None:
#         self.deeper = deeper
#         self.apiRoutes = [
#             "info",
#             "inform",
#             "speedometer",
#             "liquid",
#             "smartRoute/getDpnMode",
#             "worldmap-data",
#             "dynamic-data",
#         ]

#         self._refUrl = self.deeper.hostIp

#         super().__init__()

#     def __repr__(self) -> str:

#         retDict = self.get_values()
#         for key in retDict.keys():
#             if hasattr(retDict[key], "__dict__"):
#                 retDict[key] = retDict[key].__dict__()

#         return json.dumps(retDict)

#     def get_values(self):
#         self.update()

#         _dpnMode = self._load_deeper_mode()
#         dpnMode = pick(_dpnMode, "dpnMode")
#         tunnelCode = pick(_dpnMode, "tunnelCode")

#         return {
#             "memoryUsed": self._load_memory_used(),
#             "cpuLoad": self._load_cpu_load(),
#             "dpnMode": dpnMode,
#             "tunnelCode": tunnelCode,
#             "systemInfo": self._load_system_info(),
#         }

#     def _load_memory_used(self):
#         self.update("liquid")
#         data = self.get_api_data("liquid")
#         if data:
#             if "scale" in data.keys():
#                 return int(data["scale"])

#     @property
#     def memoryUsed(self):
#         return self._load_memory_used()

#     def _load_cpu_load(self):
#         data = self.get_api_data("speedometer")
#         if data:
#             if "guage" in data.keys():
#                 return int(data["guage"])

#     @property
#     def cpuLoad(self):
#         return self._load_cpu_load()

#     def _load_deeper_mode(self, key: str = ""):
#         data = self.get_api_data("smartRoute/getDpnMode")
#         if data:
#             if key:
#                 if key in data.keys():
#                     return data[key]
#             else:
#                 return data

#     @property
#     def dpnMode(self):
#         return self._load_deeper_mode("dpnMode")

#     @property
#     def tunnelCode(self):
#         return self._load_deeper_mode("tunnelCode")

#     def _load_system_info(self) -> SystemInfo:
#         return SystemInfo(self.get_api_data("info"))

#     @property
#     def systemInfo(self):
#         return self._load_system_info(self)
