from CxAdmin.api.cxEnvironment import CxEnvironment
from CxAdmin.api.cxFlows import CxFlows
from CxAdmin.api.cxItem import CxItem
from CxAdmin.api.cxLists import CxLists
from CxAdmin.api.cxQueues import CxQueues
from CxAdmin.api.cxStatistics import CxStatistics
from CxAdmin.objects.cx import Cx
from CxAdmin.objects.cxList import CxList
from CxAdmin.objects.cxQueue import CxQueue


class API:
    Environment = CxEnvironment
    Flows = CxFlows
    Item = CxItem
    Lists = CxLists
    Queues = CxQueues
    Statistics = CxStatistics


class Objects:
    Cx = Cx
    CxList = CxList
    CxQueue = CxQueue
