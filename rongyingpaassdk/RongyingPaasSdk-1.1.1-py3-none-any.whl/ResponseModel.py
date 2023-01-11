import time
from typing import List


class BaseResponseModel:
    def __init__(self,
                 Flag: int = None,
                 Msg: str = None):
        self.Msg = Msg
        self.Flag = Flag

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Flag') is not None:
            self.Flag = m.get('Flag')
        if m.get('Msg') is not None:
            self.Msg = m.get('Msg')
        return self

class CreateApplicationsResponseModel(BaseResponseModel):
    def __init__(self, Flag: int = None, Msg: str = None,
                 AppToken: str = None,
                 AppId: str = None):
        super().__init__(Flag, Msg)
        self.AppToken = AppToken
        self.AppId = AppId

    # def to_map(self):
    #     result = dict()
    #     if self.Flag is not None:
    #         result['Flag'] = self.Flag
    #     if self.Msg is not None:
    #         result['Msg'] = self.Msg
    #     if self.AppToken is not None:
    #         result['AppToken'] = self.AppToken
    #     if self.AppId is not None:
    #         result['AppId'] = self.AppId
    #     return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Flag') is not None:
            self.Flag = m.get('Flag')
        if m.get('Msg') is not None:
            self.Msg = m.get('Msg')
        if m.get('AppToken') is not None:
            self.AppToken = m.get('AppToken')
        if m.get('Appid') is not None:
            self.AppId = m.get('Appid')
        return self

class AccountsAppIdDayDetail:
    def __init__(self,
                 CostTimeDay: time = None,
                 CostMoneySum: float = None):
        self.CostTimeDay = CostTimeDay
        self.CostMoneySum = CostMoneySum

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CostTimeDay') is not None:
            self.CostTimeDay = m.get('CostTimeDay')
        if m.get('CostMoneySum') is not None:
            self.CostMoneySum = m.get('CostMoneySum')
        return self

class AccountsAppIdDayResponseModel(BaseResponseModel):
    def __init__(self, Flag: int = None, Msg: str = None,
                 Total: int = None,
                 Data: List[AccountsAppIdDayDetail] = None):
        super().__init__(Flag, Msg)
        self.Data = Data
        self.Total = Total

    def from_map(self, m: dict = None):
        m = m or dict()
        self.Data = []
        if m.get('Data') is not None:
            for k in m.get('Data'):
                temp_model = AccountsAppIdDayDetail()
                self.Data.append(temp_model.from_map(k))
        if m.get('Total') is not None:
            self.Total = m.get('Total')
        if m.get('Flag') is not None:
            self.Flag = m.get('Flag')
        if m.get('Msg') is not None:
            self.Msg = m.get('Msg')
        return self

class AppIdInfoDetail:
    def __init__(self,
                 CompanyName: str = None,
                 OrderTime: time = None,
                 Banlance: float = None,
                 AmountFe: float = None,
                 AppId: str = None,
                 AppToken: str = None,
                 Fee: float = None,
                 MinConsumption: int = None,
                 AmountFee: float = None,
                 ClickType: str = None,
                 Status: int = None):
        self.CompanyName = CompanyName
        self.OrderTime = OrderTime
        self.Banlance = Banlance
        self.AmountFe = AmountFe
        self.AppId = AppId
        self.AppToken = AppToken
        self.Fee = Fee
        self.MinConsumption = MinConsumption
        self.AmountFee = AmountFee
        self.ClickType = ClickType
        self.Status = Status

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CompanyName') is not None:
            self.CompanyName = m.get('CompanyName')
        if m.get('OrderTime') is not None:
            self.OrderTime = m.get('OrderTime')
        if m.get('Banlance') is not None:
            self.Banlance = m.get('Banlance')
        if m.get('AmountFe') is not None:
            self.AmountFe = m.get('AmountFe')
        if m.get('AppId') is not None:
            self.AppId = m.get('AppId')
        if m.get('AppToken') is not None:
            self.AppToken = m.get('AppToken')
        if m.get('Fee') is not None:
            self.Fee = m.get('Fee')
        if m.get('MinConsumption') is not None:
            self.MinConsumption = m.get('MinConsumption')
        if m.get('AmountFee') is not None:
            self.AmountFee = m.get('AmountFee')
        if m.get('ClickType') is not None:
            self.ClickType = m.get('ClickType')
        if m.get('Status') is not None:
            self.Status = m.get('Status')
        return self

class AppIdInfoResponseModel(BaseResponseModel):
    def __init__(self,
                 Flag: int = None,
                 Msg: str = None,
                 Total: int = None,
                 Data: List[AppIdInfoDetail] = None):
        super().__init__(Flag, Msg)
        self.Data = Data
        self.Total = Total

    def from_map(self, m: dict = None):
        m = m or dict()
        self.Data = []
        if m.get('Data') is not None:
            for k in m.get('Data'):
                temp_model = AppIdInfoDetail()
                self.Data.append(temp_model.from_map(k))
        if m.get('Total') is not None:
            self.Total = m.get('Total')
        if m.get('Flag') is not None:
            self.Flag = m.get('Flag')
        if m.get('Msg') is not None:
            self.Msg = m.get('Msg')
        return self

class RechargeRecoveryRecordDetail:
    def __init__(self,
                 Banlance: float = None,
                 Type: int = None,
                 Date: time = None):
        self.Banlance = Banlance
        self.Type = Type
        self.Date = Date

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Banlance') is not None:
            self.Banlance = m.get('Banlance')
        if m.get('Type') is not None:
            self.Type = m.get('Type')
        if m.get('Date') is not None:
            self.Date = m.get('Date')
        return self

class RechargeRecoveryRecordResponseModel(BaseResponseModel):
    def __init__(self,
                 Flag: int = None,
                 Msg: str = None,
                 Total: int = None,
                 Data: List[RechargeRecoveryRecordDetail] = None):
        super().__init__(Flag, Msg)
        self.Data = Data
        self.Total = Total

    def from_map(self, m: dict = None):
        m = m or dict()
        self.Data = []
        if m.get('Data') is not None:
            for k in m.get('Data'):
                temp_model = RechargeRecoveryRecordDetail()
                self.Data.append(temp_model.from_map(k))
        if m.get('Flag') is not None:
            self.Flag = m.get('Flag')
        if m.get('Msg') is not None:
            self.Msg = m.get('Msg')
        if m.get('Total') is not None:
            self.Total = m.get('Total')
        return self

class AppIdNumberDetail:
    def __init__(self,
                 Number: str = None):
        self.Number = Number

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Number') is not None:
            self.Number = m.get('Number')
        return self

class AppIdNumberResponseModel(BaseResponseModel):
    def __init__(self,
                 Flag: int = None,
                 Msg: str = None,
                 Total: int = None,
                 Data: List[AppIdNumberDetail] = None):
        super().__init__(Flag, Msg)
        self.Data = Data
        self.Total = Total

    def from_map(self, m: dict = None):
        m = m or dict()
        self.Data = []
        if m.get('Data') is not None:
            for k in m.get('Data'):
                temp_model = AppIdNumberDetail()
                self.Data.append(temp_model.from_map(k))

        if m.get('Total') is not None:
            self.Total = m.get('Total')
        if m.get('Flag') is not None:
            self.Flag = m.get('Flag')
        if m.get('Msg') is not None:
            self.Msg = m.get('Msg')
        return self

class AppMontyPackageDetail:
    def __init__(self,
                 Name: str = None,
                 Date: time = None,
                 Money: float = None,
                 Count: int = None):
        self.Name = Name
        self.Date = Date
        self.Money = Money
        self.Count = Count

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Name') is not None:
            self.Name = m.get('Name')
        if m.get('Date') is not None:
            self.Date = m.get('Date')
        if m.get('Money') is not None:
            self.Money = m.get('Money')
        if m.get('Count') is not None:
            self.Count = m.get('Count')
        return self

class AppMontyPackageResponseModel(BaseResponseModel):
    def __init__(self,
                 Flag: int = None,
                 Msg: str = None,
                 Total: int = None,
                 Data: List[AppMontyPackageDetail] = None):
        super().__init__(Flag, Msg)
        self.Data = Data
        self.Total = Total

    def from_map(self, m: dict = None):
        m = m or dict()
        self.Data = []
        if m.get('Data') is not None:
            for k in m.get('Data'):
                temp_model = AppMontyPackageDetail()
                self.Data.append(temp_model.from_map(k))

        if m.get('Total') is not None:
            self.Total = m.get('Total')
        if m.get('Flag') is not None:
            self.Flag = m.get('Flag')
        if m.get('Msg') is not None:
            self.Msg = m.get('Msg')
        return self

class CreateSeatAccountResponseModel(BaseResponseModel):
    def __init__(self,
                 Flag: int = None,
                 Msg: str = None,
                 SeatAccount: str = None):
        super().__init__(Flag, Msg)
        self.SeatAccount = SeatAccount

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SeatAccount') is not None:
            self.SeatAccount = m.get('SeatAccount')
        if m.get('Flag') is not None:
            self.Flag = m.get('Flag')
        if m.get('Msg') is not None:
            self.Msg = m.get('Msg')
        return self

class SeatDetailInfoModel:
    def __init__(self,
                 SeatName: str = None,
                 Passwd: str = None,
                 SeatAccount: str = None,
                 State: int = None,
                 Mobile: str = None,
                 IsVail: int = None):
        self.SeatAccount = SeatAccount
        self.Passwd = Passwd
        self.SeatName = SeatName
        self.State = State
        self.Mobile = Mobile
        self.IsVail = IsVail

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SeatAccount') is not None:
            self.SeatAccount = m.get('SeatAccount')
        if m.get('Passwd') is not None:
            self.Passwd = m.get('Passwd')
        if m.get('SeatName') is not None:
            self.SeatName = m.get('SeatName')
        if m.get('State') is not None:
            self.State = m.get('State')
        if m.get('Mobile') is not None:
            self.Mobile = m.get('Mobile')
        if m.get('IsVail') is not None:
            self.IsVail = m.get('IsVail')
        return self

class SeatDetailResponseModel(BaseResponseModel):
    def __init__(self,
                 Flag: int = None,
                 Msg: str = None,
                 Total: int = None,
                 Data: List[SeatDetailInfoModel] = None):
        super().__init__(Flag, Msg)
        self.Data = Data
        self.Total = Total

    def from_map(self, m: dict = None):
        m = m or dict()
        self.Data = []
        if m.get('Data') is not None:
            for k in m.get('Data'):
                temp_model = SeatDetailInfoModel()
                self.Data.append(temp_model.from_map(k))
        if m.get('Total') is not None:
            self.Total = m.get('Total')
        if m.get('Flag') is not None:
            self.Flag = m.get('Flag')
        if m.get('Msg') is not None:
            self.Msg = m.get('Msg')
        return self

class SeatTransferResponseModel(BaseResponseModel):
    def __init__(self,
                 Flag: int = None,
                 Msg: str = None,
                 Appid: str = None,
                 Caller: str = None,
                 AmountfeDiff: float = None):
        super().__init__(Flag, Msg)
        self.Caller = Caller
        self.Appid = Appid
        self.AmountfeDiff = AmountfeDiff

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Caller') is not None:
            self.Caller = m.get('Caller')
        if m.get('Appid') is not None:
            self.Appid = m.get('Appid')
        if m.get('Flag') is not None:
            self.Flag = m.get('Flag')
        if m.get('Msg') is not None:
            self.Msg = m.get('Msg')
        if m.get('AmountfeDiff') is not None:
            self.AmountfeDiff = m.get('AmountfeDiff')
        return self

class SeatAddPackageRecordDetail:
    def __init__(self,
                 Name: str = None,
                 Date: time = None,
                 Money: float = None,
                 VoipAccount: str = None,
                 IsDelete: int = None):
        self.Name = Name
        self.Date = Date
        self.Money = Money
        self.VoipAccount = VoipAccount
        self.IsDelete = IsDelete

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Name') is not None:
            self.Name = m.get('Name')
        if m.get('Date') is not None:
            self.Date = m.get('Date')
        if m.get('Money') is not None:
            self.Money = m.get('Money')
        if m.get('VoipAccount') is not None:
            self.VoipAccount = m.get('VoipAccount')
        if m.get('IsDelete') is not None:
            self.IsDelete = m.get('IsDelete')
        return self

class SeatAddPackageRecordResponseModel(BaseResponseModel):
    def __init__(self,
                 Flag: int = None,
                 Msg: str = None,
                 Total: int = None,
                 Data: List[SeatAddPackageRecordDetail] = None):
        super().__init__(Flag, Msg)
        self.Data = Data
        self.Total = Total

    def from_map(self, m: dict = None):
        m = m or dict()
        self.Data = []
        if m.get('Data') is not None:
            for k in m.get('Data'):
                temp_model = SeatAddPackageRecordDetail()
                self.Data.append(temp_model.from_map(k))
        if m.get('Total') is not None:
            self.Total = m.get('Total')
        if m.get('Flag') is not None:
            self.Flag = m.get('Flag')
        if m.get('Msg') is not None:
            self.Msg = m.get('Msg')
        return self

class SeatTrafficStatisticsTotalDetail:
    def __init__(self,
                 SeatAccount: str = None,
                 CallCount:  int = None,
                 SuccessCount: int = None,
                 SuccessRate: float = None,
                 TotalBillSec: int = None,
                 AvgTime: float = None,
                 CallMin: int = None,
                 SumCallMin: int = None,
                 CostMoney: float = None,
                 IsDelete: int = None):
        self.SeatAccount = SeatAccount
        self.CallCount = CallCount
        self.SuccessCount = SuccessCount
        self.SuccessRate = SuccessRate
        self.TotalBillSec = TotalBillSec
        self.AvgTime = AvgTime
        self.CallMin = CallMin
        self.SumCallMin = SumCallMin
        self.CostMoney = CostMoney
        self.IsDelete = IsDelete

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SeatAccount') is not None:
            self.SeatAccount = m.get('SeatAccount')
        if m.get('CallCount') is not None:
            self.CallCount = m.get('CallCount')
        if m.get('SuccessCount') is not None:
            self.SuccessCount = m.get('SuccessCount')
        if m.get('SuccessRate') is not None:
            self.SuccessRate = m.get('SuccessRate')
        if m.get('TotalBillSec') is not None:
            self.TotalBillSec = m.get('TotalBillSec')
        if m.get('AvgTime') is not None:
            self.AvgTime = m.get('AvgTime')
        if m.get('CallMin') is not None:
            self.CallMin = m.get('CallMin')
        if m.get('SumCallMin') is not None:
            self.SumCallMin = m.get('SumCallMin')
        if m.get('CostMoney') is not None:
            self.TotalBillSec = m.get('CostMoney')
        if m.get('IsDelete') is not None:
            self.TotalBillSec = m.get('IsDelete')
        return self


class SeatTrafficStatisticsDetail:
    def __init__(self,
                 SeatAccount: str = None,
                 CallCount:  int = None,
                 SuccessCount: int = None,
                 SuccessRate: float = None,
                 TotalBillSec: int = None,
                 AvgTime: float = None,
                 CallMin: int = None,
                 SumCallMin: int = None,
                 CostMoney: float = None,
                 IsDelete: int = None,
                 CallDate: time = None):
        self.SeatAccount = SeatAccount
        self.CallCount = CallCount
        self.SuccessCount = SuccessCount
        self.SuccessRate = SuccessRate
        self.TotalBillSec = TotalBillSec
        self.AvgTime = AvgTime
        self.CallMin = CallMin
        self.SumCallMin = SumCallMin
        self.CostMoney = CostMoney
        self.IsDelete = IsDelete
        self.CallDate = CallDate

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SeatAccount') is not None:
            self.SeatAccount = m.get('SeatAccount')
        if m.get('CallCount') is not None:
            self.CallCount = m.get('CallCount')
        if m.get('SuccessCount') is not None:
            self.SuccessCount = m.get('SuccessCount')
        if m.get('SuccessRate') is not None:
            self.SuccessRate = m.get('SuccessRate')
        if m.get('TotalBillSec') is not None:
            self.TotalBillSec = m.get('TotalBillSec')
        if m.get('AvgTime') is not None:
            self.AvgTime = m.get('AvgTime')
        if m.get('CallMin') is not None:
            self.CallMin = m.get('CallMin')
        if m.get('SumCallMin') is not None:
            self.SumCallMin = m.get('SumCallMin')
        if m.get('CostMoney') is not None:
            self.TotalBillSec = m.get('CostMoney')
        if m.get('IsDelete') is not None:
            self.TotalBillSec = m.get('IsDelete')
        if m.get('CallDate') is not None:
            self.CallDate = m.get('CallDate')
        return self
class SeatTrafficStatisticsResponseModel(BaseResponseModel):
    def __init__(self,
                 Flag: int = None,
                 Msg: str = None,
                 Total: int = None,
                 Data: List[SeatTrafficStatisticsDetail] = None):
        super().__init__(Flag, Msg)
        self.Data = Data
        self.Total = Total

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Total') is not None:
            self.Total = m.get('Total')
        if m.get('Flag') is not None:
            self.Flag = m.get('Flag')
        if m.get('Msg') is not None:
            self.Msg = m.get('Msg')
        self.Data = []
        if m.get('Data') is not None:
            for k in m.get('Data'):
                temp_model = SeatTrafficStatisticsDetail()
                self.Data.append(temp_model.from_map(k))
        return self

class SeatTrafficStatisticsTotalResponseModel(BaseResponseModel):
    def __init__(self,
                 Flag: int = None,
                 Msg: str = None,
                 Total: int = None,
                 Data: List[SeatTrafficStatisticsTotalDetail] = None):
        super().__init__(Flag, Msg)
        self.Data = Data
        self.Total = Total

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Total') is not None:
            self.Total = m.get('Total')
        if m.get('Flag') is not None:
            self.Flag = m.get('Flag')
        if m.get('Msg') is not None:
            self.Msg = m.get('Msg')
        self.Data = []
        if m.get('Data') is not None:
            for k in m.get('Data'):
                temp_model = SeatTrafficStatisticsTotalDetail()
                self.Data.append(temp_model.from_map(k))
        return self

class SeatClickCallResponseModel(BaseResponseModel):
    def __init__(self,
                 Flag: int = None,
                 Msg: str = None,
                 VirtualNumber: str = None,
                 SessionId: str = None):
        super().__init__(Flag, Msg)
        self.SessionId = SessionId
        self.VirtualNumber = VirtualNumber

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('VirtualNumber') is not None:
            self.VirtualNumber = m.get('VirtualNumber')
        if m.get('Flag') is not None:
            self.Flag = m.get('Flag')
        if m.get('Msg') is not None:
            self.Msg = m.get('Msg')
        if m.get('SessionId') is not None:
            self.SessionId = m.get('SessionId')
        return self

class CallRecordDetailModel:
    def __init__(self,
                 maxid: int = None,
                 sessionId: str = None,
                 bindNum: str = None,
                 calleeNum: str = None,
                 fwdDstNum: str = None,
                 fwdDisplayNum: str = None,
                 fwdStartTime: time = None,
                 fwdAlertingTime: time = None,
                 fwdAnswerTime: time = None,
                 callEndTime: time = None,
                 failTime: time = None,
                 callOutStartTime: time = None,
                 callOutAlertingTime: time = None,
                 callOutAnswerTime: time = None,
                 billsec: int = None,
                 recordFlag: int = None,
                 recordStartTime: time = None,
                 recordFileDownloadUrl: str = None,
                 fwdUnaswRsn: str = None,
                 ulFailReason: str = None,
                 direction: str = None,
                 ):
        self.maxid = maxid
        self.sessionId = sessionId
        self.bindNum = bindNum
        self.calleeNum = calleeNum
        self.fwdDstNum = fwdDstNum
        self.fwdDisplayNum = fwdDisplayNum
        self.fwdStartTime = fwdStartTime
        self.fwdAlertingTime = fwdAlertingTime
        self.fwdAnswerTime = fwdAnswerTime
        self.callEndTime = callEndTime
        self.failTime = failTime
        self.callOutStartTime = callOutStartTime
        self.callOutAlertingTime = callOutAlertingTime
        self.callOutAnswerTime = callOutAnswerTime
        self.billsec = billsec
        self.recordFlag = recordFlag
        self.recordStartTime = recordStartTime
        self.recordFileDownloadUrl = recordFileDownloadUrl
        self.fwdUnaswRsn = fwdUnaswRsn
        self.ulFailReason = ulFailReason
        self.direction = direction

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('maxid') is not None:
            self.maxid = m.get('maxid')
        if m.get('sessionId') is not None:
            self.sessionId = m.get('sessionId')
        if m.get('bindNum') is not None:
            self.bindNum = m.get('bindNum')
        if m.get('calleeNum') is not None:
            self.calleeNum = m.get('calleeNum')
        if m.get('fwdDstNum') is not None:
            self.fwdDstNum = m.get('fwdDstNum')
        if m.get('fwdDisplayNum') is not None:
            self.fwdDisplayNum = m.get('fwdDisplayNum')
        if m.get('fwdStartTime') is not None:
            self.fwdStartTime = m.get('fwdStartTime')
        if m.get('fwdAlertingTime') is not None:
            self.fwdAlertingTime = m.get('fwdAlertingTime')
        if m.get('fwdAnswerTime') is not None:
            self.fwdAnswerTime = m.get('fwdAnswerTime')
        if m.get('callEndTime') is not None:
            self.callEndTime = m.get('callEndTime')
        if m.get('failTime') is not None:
            self.failTime = m.get('failTime')
        if m.get('callOutStartTime') is not None:
            self.callOutStartTime = m.get('callOutStartTime')
        if m.get('callOutAlertingTime') is not None:
            self.callOutAlertingTime = m.get('callOutAlertingTime')
        if m.get('callOutAnswerTime') is not None:
            self.callOutAnswerTime = m.get('callOutAnswerTime')
        if m.get('billsec') is not None:
            self.billsec = m.get('billsec')
        if m.get('recordFlag') is not None:
            self.recordFlag = m.get('recordFlag')
        if m.get('recordStartTime') is not None:
            self.recordStartTime = m.get('recordStartTime')
        if m.get('recordFileDownloadUrl') is not None:
            self.recordFileDownloadUrl = m.get('recordFileDownloadUrl')
        if m.get('fwdUnaswRsn') is not None:
            self.fwdUnaswRsn = m.get('fwdUnaswRsn')
        if m.get('ulFailReason') is not None:
            self.ulFailReason = m.get('ulFailReason')
        if m.get('direction') is not None:
            self.direction = m.get('direction')
        return self

class CallRecordDetailResponseModel(BaseResponseModel):
    def __init__(self,
                 Flag: int = None,
                 Msg: str = None,
                 Total: int = None,
                 Data: List[CallRecordDetailModel] = None):
        super().__init__(Flag, Msg)
        self.Data = Data
        self.Total = Total

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Total') is not None:
            self.Total = m.get('Total')
        if m.get('Flag') is not None:
            self.Flag = m.get('Flag')
        if m.get('Msg') is not None:
            self.Msg = m.get('Msg')
        self.Data = []
        if m.get('Data') is not None:
            for k in m.get('Data'):
                temp_model = CallRecordDetailModel()
                self.Data.append(temp_model.from_map(k))
        return self

class AccountDetailsModel:
    def __init__(self,
                 CompanyName: str = None,
                 Cell: str = None,
                 SeatCount: int = None):
        self.CompanyName = CompanyName
        self.Cell = Cell
        self.SeatCount = SeatCount

    def from_mop(self, m: dict = None):
        m = m or dict()
        if m.get('CompanyName') is not None:
            self.CompanyName = m.get('CompanyName')
        if m.get('Cell') is not None:
            self.Cell = m.get('Cell')
        if m.get('SeatCount') is not None:
            self.SeatCount = m.get('SeatCount')
        return self

class AccountDetailsResponseModel(BaseResponseModel):
    def __init__(self,
                 Flag: int = None,
                 Msg: str = None,
                 Total: int = None,
                 Data: AccountDetailsModel = None):
        super().__init__(Flag, Msg)
        self.Data = Data
        self.Total = Total

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Total') is not None:
            self.Total = m.get('Total')
        if m.get('Flag') is not None:
            self.Flag = m.get('Flag')
        if m.get('Msg') is not None:
            self.Msg = m.get('Msg')
        self.Data = []
        if m.get('Data') is not None:
            temp_model = AccountDetailsModel()
            self.Data = temp_model.from_mop(m.get('Data'))
        return self

class AccountBalanceDetail:
    def __init__(self,
                 Company: str = None,
                 ZBanlance: float = None,
                 Banlance: float = None,
                 Fee: float = None):
        self.Company = Company
        self.ZBanlance = ZBanlance
        self.Banlance = Banlance
        self.Fee = Fee

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Company') is not None:
            self.Company = m.get('Company')
        if m.get('ZBanlance') is not None:
            self.ZBanlance = m.get('ZBanlance')
        if m.get('Banlance') is not None:
            self.Banlance = m.get('Banlance')
        if m.get('Fee') is not None:
            self.Fee = m.get('Fee')
        return self

class AccountBalanceResponseModel(BaseResponseModel):
    def __init__(self,
                 Flag: int = None,
                 Msg: str = None,
                 Total: int = None,
                 Data: List[AccountBalanceDetail] = None):
        super().__init__(Flag, Msg)
        self.Data = Data
        self.Total = Total

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Total') is not None:
            self.Total = m.get('Total')
        if m.get('Flag') is not None:
            self.Flag = m.get('Flag')
        if m.get('Msg') is not None:
            self.Msg = m.get('Msg')
        self.Data = []
        if m.get('Data') is not None:
            for k in m.get('Data'):
                temp_model = AccountBalanceDetail()
                self.Data.append(temp_model.from_map(k))
        return self

class BlacklistResponseModel(BaseResponseModel):
    def __init__(self,
                 Flag: int = None,
                 Msg: str = None,
                 Data: int = None):
        super().__init__(Flag, Msg)
        self.Data = Data

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Flag') is not None:
            self.Flag = m.get('Flag')
        if m.get('Msg') is not None:
            self.Msg = m.get('Msg')
        if m.get('Data') is not None:
            self.Data = m.get('Data')
        return self
