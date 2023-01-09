import datetime
import json

from PaasSdk.CreateRequestClient import CreateRequestClient as Client
from PaasSdk.Config import Config as Config
from PaasSdk import RequestModel as models
from PaasSdk import ResponseModel as responseModels

request = models.CreateApplicationsRequestModel(AppName="python测试")

config = Config(AppId="d5007cb3e2554d28996be7c8bc97afdd",
                AppIdToken="5f3739ac98da4f308e802806920006ad",
                AccountSid="00000000521547df5j41k45f8629801f",
                AccountToken="201181216269332252a816unz3h8la01")
client = Client(config)
dayRequest = models.AccountsAppIdDayRequestModel(Type=1,
                                                 StartTime="2022-12-01",
                                                 EndTime="2022-12-29")


def AppRechargeRecovery():
    rechargeRecoveryRequestModel = models.RechargeRecoveryRequestModel(Banlance=3,
                                                                       Type=1)
    info = client.AppRechargeRecovery(rechargeRecoveryRequestModel)
    print(info.Msg)
    print(info.Flag)


def QueryAccountAppInfo() -> object:
    info = client.QueryAccountAppInfo()
    print(info.Msg)
    print(info.Flag)
    print(info.Total)
    for k in info.Data:
        print(k.CompanyName + "   " + str(k.Banlance))


def QueryAppIdInfo() -> object:
    info = client.QueryAppIdInfo()
    print(info.Msg)
    print(info.Flag)
    print(info.Total)
    for k in info.Data:
        print(k.CompanyName + "   " + str(k.Banlance))

def QueryCallRecordDetail() -> object:
    infoData = models.CallRecordDetailModel(SessionId='00JZM1374093651485Z0105141418')
    requestModel = models.CallRecordDetailRequestModel(CallDetail=infoData)
    info = client.QueryCallRecordDetail(requestModel)
    # print(requestModel.to_map())
    print(info.Msg)
    print(info.Flag)
    if len(info.Data) > 0:
        for k in info.Data:
            callOutTime = datetime.datetime.strptime(k.callOutStartTime, "%Y-%m-%d %H:%M:%S")
            # print(callOutTime)
            callOutDateTime = (callOutTime + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
            print(k.calleeNum + ";被叫号码：" + k.fwdDstNum + "；呼出时间："
                  + callOutDateTime)
    else:
        print('无话单记录')

def QueryCallRecordBatch() -> object:
    billList = models.CallRecordBatchModel(
                                           StartTime='2023-01-05 01:10:53',
                                           EndTime='2023-01-06 10:10:53',
                                           )
    requestModel = models.CallRecordBatchRequestModel(BillList=billList)
    # print(requestModel.to_map())
    info = client.QueryCallRecordBatch(requestModel)
    print(info.Msg)
    print(info.Flag)
    if len(info.Data) > 0:
        for k in info.Data:
            callOutTime = datetime.datetime.strptime(k.callOutStartTime, "%Y-%m-%d %H:%M:%S")
            print(callOutTime)
            callOutDateTime = (callOutTime + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
            print(k.calleeNum + ";被叫号码：" + k.fwdDstNum + "；呼出时间："
                  + callOutDateTime)

def QueryAccountDetails() -> object:
    info = client.QueryAccountDetails()
    print(info.Msg)
    print(info.Flag)
    if info.Flag == 200:
        data = info .Data
        print(data.CompanyName)
        print(data.SeatCount)
        print(data.Cell)

def QueryAccountBanlance() -> object:
    info = client.QueryAccountBanlance()
    print(info.Msg)
    print(info.Flag)
    if info.Flag == 200 and len(info.Data) > 0:
        for k in info.Data:
            print(k.Company)
            print(k.Banlance)
            print(k.ZBanlance)
            print(k.Fee)

def BlacklistDetection() -> object:
    config = Config(AppIdToken='e02a12b24ca34aaf8efc6dcda0d2033c',
                    AppId='1592e8a4140b411c8905294feb723dbc',
                    AccountSid='00000000521547df5j41k45f8629801f')
    client = Client(config)
    request = models.BlacklistDetectionRequestModel(Mobile='18516190242')
    info = client.BlacklistDetection(request)
    print(info.Msg)
    print(info.Flag)
    print(info.Data)


# AppRechargeRecovery()
# QueryAccountAppInfo()
# QueryAppIdInfo()
# QueryCallRecordDetail()
# QueryCallRecordBatch()
# QueryAccountDetails()
# QueryAccountBanlance()
BlacklistDetection()
# if info["Flag"] == 200:
#     print(info["Data"])
# else:
#     print(info["Msg"])
