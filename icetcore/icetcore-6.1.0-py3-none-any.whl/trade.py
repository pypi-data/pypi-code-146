import json
import os
import uuid
from win32com import client
import pythoncom
from abc import ABCMeta,abstractmethod
from datetime import datetime,timedelta
import pytz
from icetcore.constant import OrderStruct
import win32event

Git=pythoncom.CoCreateInstance(
        pythoncom.CLSID_StdGlobalInterfaceTable,
        None,
        pythoncom.CLSCTX_INPROC,
        pythoncom.IID_IGlobalInterfaceTable,
    )
def iff(itemvalue,tcsize=1):
    if itemvalue!=-9223372036854775808 and itemvalue!="":
        return int(itemvalue)/tcsize
    elif itemvalue=="":
        return 0
    else:
        return None

class TradeEventMeta(metaclass=ABCMeta):
    def __init__(self) -> None:
        self._tcoreapi=None
    @abstractmethod
    def onconnected(self, strapi):
        pass
    @abstractmethod
    def ondisconnected(self, strapi):
        pass
    @abstractmethod
    def onaccountlist(self,data,count):
        pass
    @abstractmethod
    def onordereportreal(self,data):
        pass
    @abstractmethod
    def onfilledreportreal(self,data):
        pass
    @abstractmethod
    def onorderreportreset(self):
        pass
    @abstractmethod
    def onpositionmoniter(self,data):
        pass

class BaseEvents(metaclass=ABCMeta):
    def __init__(self):
        self.tz = pytz.timezone('Etc/GMT+8')
        self.tradeapi=None
        self.extendevent=None

        self.cmsgevent=win32event.CreateEvent(None, 0, 0, None)
        self.symbollistready=False
        self.hotmonthready=False
        self.symblookready=False
        self.symbinfoready=False

        self.accountcout=0
        self.positioncout={}
        self.combpositioncout={}
        self.margincout={}
        self.combordercout={}
        self.orderinfo={}

    def onconnected(self, strapi):
        if self.extendevent:
            self.extendevent.onconnected(strapi)

    def ondisconnected(self, strapi):
        if self.extendevent:
            self.extendevent.ondisconnected(strapi)

    def onaccountlist(self,accoutlist,count):
        if self.extendevent:
            self.extendevent.onaccountlist(accoutlist,count)
    def onordereportreal(self,data):
        self.orderinfo[data["UserKey1"]]=data
        if self.extendevent:
            self.extendevent.onordereportreal(data)

    def onfilledreportreal(self,data):
        if self.extendevent:
            self.extendevent.onfilledreportreal(data)

    def onorderreportreset(self):
        if self.extendevent:
            self.extendevent.onorderreportreset()

    def onpositionmoniter(self,data):
        if self.extendevent:
            self.extendevent.onpositionmoniter(data)

    def OnCommandMsg(self, MsgType, MsgCode, MsgString):
        if int(MsgType)==2 and int(MsgCode)==1:
            win32event.SetEvent(self.cmsgevent)
            self.onconnected("trade")
        if int(MsgType)==1 and int(MsgCode)==1:
            self.ondisconnected("trade")
        if int(MsgType)==2 and int(MsgCode)==5:
            print("SYMBOLCLEAR. Symbol=",MsgType, MsgCode, MsgString)

    def OnAccountUpdate(self, nType, AcctMask, nCount):
        if(nCount == -100 or nCount == -200):
            return
        if nType==1:
            self.accountcout= nCount
            accoutlist=[]
            for i in range(nCount):
                acc=self.tradeapi.getaccoutlist(i)
                accoutlist.append(acc)
            self.onaccountlist(accoutlist,nCount)
        elif nType==7:
            self.positioncout[AcctMask]=nCount
            #print("OnAccountUpdate",nType, AcctMask, nCount)
            # win32event.SetEvent(self.event)
            # print("OnAccountUpdate",self.event)
            # for i in range(nCount):
            #     pos=self.tradeapi.getposition(i,AcctMask)
            #     print(pos["Symbol"])
        elif nType==8:
            self.combpositioncout[AcctMask]=nCount
            # for i in range(nCount):
            #     combpos=self.tradeapi.getcombposition(i,AcctMask)
            #     #if "^" in combpos.Symbol:
            #     if combpos:
            #         print(combpos)#["Symbol"],"  ",combpos["SymbolA"],"  ",combpos["SymbolB"])
        elif nType==9:
            self.margincout[AcctMask]=nCount
        #     #for i in range(nCount):
        #     margin=self.tradeapi.getaccmargin(AcctMask)
        #     print(margin)
        elif nType==32:
            self.combordercout[AcctMask]=nCount
            # for i in range(nCount):
            #     combord=self.tradeapi.getcombinationorder(i,AcctMask)
            #     print(combord)
        # elif nType==100:
        #     print("ADT_ACCOUNT_DATA_READY")
        # print("OnAccountUpdate",nType, AcctMask, nCount,datetime.strftime(datetime.now(),"%Y%m%d %H:%M:%S"))
        
    def OnExecutionReport(self, strReportID):
        self.onordereportreal(self.tradeapi.getreportbyid(strReportID))
    def OnFilledReport(self, strReportID):
        realFilled=self.tradeapi.getfilledreportbyid(strReportID)
        realFilled['ReportID']=strReportID.split("-")[0]
        self.onfilledreportreal(realFilled)
    # def OnExecTCReport(self, ReportID):
    #     print("$$$$$$$$$$$$$$$$$$$$$",ReportID)
    #     self.onordereport(self.tradeapi.getreportbyid(ReportID))
    def OnPositionTracker(self):
        self.onpositionmoniter(self.tradeapi.getpositionmoniter())
    def OnReportReset(self):
        self.onorderreportreset()
    def OnSetTopic(self, strTopic, lParam, strParam, pvParam):
        if os.path.exists(pvParam):
            with open(pvParam.replace('\\','/'),'rb+') as symblist:
                sym=json.load(symblist,encoding="utf-8")
                #self.onsymbolhistory(strParam,lParam,sym)  
        else:
            print("无法获取到历史合约，请确认账户是否有dogs权限")
        self.tradeapi.topicunsub("ICECREAM.RETURN")

    def OnSymbolClassificationsUpdate(self):
        self.symbollistready=True
    def OnHotMonthUpdate(self):
        self.hotmonthready=True
    def OnSymbolLookupUpdate(self):
        self.symblookready=True
    def OnInstrumentInfoUpdate(self):
        self.symbinfoready=True
    # def OnExtendReport(self, nType, strReportData):
    #     print("OnExtendReport",nType, strReportData)
    # def OnCancelReplaceError(self, strReportID):
    #     print("OnCancelReplaceError",strReportID)
    # def OnSpreadReport(self, bstrSpdReportID):
    #     print("OnSpreadReport",bstrSpdReportID)
    # def OnSpreadPosition(self, bstrSpdSymbol):
    #     print("OnSpreadPosition",bstrSpdSymbol)
   
class TradeClass:
    def __init__(self,eventclass:type):
        #pythoncom.CoInitialize()
        pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
        obj = client.Dispatch("{5C434E24-11B1-451A-BF66-E5F42E8B8E75}")#clsctx=pythoncom.CLSCTX_ALL
        self.eventobj=client.WithEvents(obj,BaseEvents)
        self.eventobj.extendevent=eventclass
        self.eventobj.tradeapi=self
        self.cookie = Git.RegisterInterfaceInGlobal(obj, pythoncom.IID_IDispatch)
        self.tz = pytz.timezone('Etc/GMT+8')
        self.ordererr={"-10":"unknow error",
                        "-11":"买卖别错误",
                        "-12":"复式单商品代码解晰错误",
                        "-13":"下单账号, 不可下此交易所商品",
                        "-14":"下单错误, 不支持的价格 或 OrderType 或 TimeInForce ",
                        "-15":"不支援证券下单",
                        "-20":"联机未建立",
                        "-22":"价格的 TickSize 错误",
                        "-23":"下单数量超过该商品的上下限",
                        "-24":"下单数量错误",
                        "-25":"价格不能小于和等于 0 (市价类型不会去检查)"}
    def connect(self,appid:str,servicekey:str):
        try:
            pythoncom.CoInitialize()
            disp = Git.GetInterfaceFromGlobal(self.cookie, pythoncom.IID_IDispatch)
            interp = client.Dispatch(disp)
            re=interp.Connect(".", appid, servicekey, 1)
            print(re)
            self.setaccountsubscriptionlevel(3)
            return 
        except pythoncom.com_error as e:
            print("连接错误:",e)

    def disconnect(self):
        try:
            pythoncom.CoInitialize()
            disp = Git.GetInterfaceFromGlobal(self.cookie, pythoncom.IID_IDispatch)
            interp = client.Dispatch(disp)
            interp.Disconnect()
        except pythoncom.com_error as e:
            print("连接错误:",e)

    def getexpirationdate(self, symbol:str):
        try:
            pythoncom.CoInitialize()
            disp = Git.GetInterfaceFromGlobal(self.cookie, pythoncom.IID_IDispatch)
            interp = client.Dispatch(disp)
            return interp.GetExpirationDate(symbol)
        except pythoncom.com_error as e:
            print("getexpirationDate错误:",e)

    #获取剩余交易日
    def gettradeingdays(self, strSymbol):
        try:
            lEndDate=self.getexpirationdate(strSymbol)
            pythoncom.CoInitialize()
            disp = Git.GetInterfaceFromGlobal(self.cookie, pythoncom.IID_IDispatch)
            interp = client.Dispatch(disp)
            return interp.GetTradeingDays(strSymbol, lEndDate)
        except pythoncom.com_error as e:
            print("gettradeingdays错误:",e)

    def gethotmonth(self, symbol:str, strdate="", strtime=""):
        try:
            temp={}
            pythoncom.CoInitialize()
            disp = Git.GetInterfaceFromGlobal(self.cookie, pythoncom.IID_IDispatch)
            interp = client.Dispatch(disp)
            if strdate and strtime:
                strhot=interp.GetHotMonthByDateTime(symbol, strdate, strtime)
                hot=strhot.split("~")[0].split(":")
                temp[datetime.strptime(str(hot[1]),'%Y%m%d%H%M%S').replace(tzinfo=self.tz)+timedelta(hours=8)]=hot[0]
                return temp
            else:
                
                interp.GetHotMonthByDateTime(symbol, strdate, strtime)
                with open("C:\\ProgramData\\TCore\\HotChange\\"+symbol+".txt",'r+') as symblist:
                    for count,line in enumerate(symblist):
                        if count!=0:
                            linedata=line.split("->")
                            temp[datetime.strptime(linedata[0]+" "+self.getsymbol_session(symbol).split(";")[-1].split("~")[-1],'%Y%m%d %H:%M').replace(tzinfo=self.tz)+timedelta(hours=8)+timedelta(seconds=1)]=symbol.replace("HOT",str(linedata[1].strip("\n")))
                return temp
        except pythoncom.com_error as e:
            print("gethotmonth错误:",e)
    def subsymbolhistory(self,symboltype,dt):
        self.topicsub("ICECREAM.RETURN")
        self.topicpublish ("ICECREAM.RECOVER",dt, symboltype,None)#20221203, "OPT"
    def getsymbol_ticksize(self,symbol:str):
        return self.__getsymbolInfo("2",symbol)
    def getsymbol_session(self,symbol:str):
        return self.__getsymbolInfo("3",symbol)
    def getsymbolvolume_multiple(self,symbol:str):
        return self.__getsymbolInfo("6",symbol)
    def getsymbol_id(self,symbol:str):
        return self.__getsymbolInfo("Instrument",symbol)
    def getsymbol_allinfo(self,symbol:str):
        return self.__getsymbolInfo("ALL",symbol)

    def __getsymbolInfo(self,strType:str, symbol:str):
        try:
            pythoncom.CoInitialize()
            disp = Git.GetInterfaceFromGlobal(self.cookie, pythoncom.IID_IDispatch)
            interp = client.Dispatch(disp)
            return interp.GetInstrumentInfo(strType, symbol)
        except pythoncom.com_error as e:
            print("getsymbolInfo错误:",e)

    def getallsymbol(self,symboltype="",exchange=""):
        symbolist=[]
        if symboltype=="" or symboltype in "FUTURES":
            ex=self.__getsymbollist("FUT", "", "", "", "")
            for y1 in [x1.split(",")[0] for x1 in ex.split("|")]:
                if exchange=="" or exchange in y1:
                    ex1=self.__getsymbollist("FUT",y1, "", "", "")
                    for y2 in [x2.split(",")[0] for x2 in ex1.split("|")]:
                        if y2!="HOT" and y2!="FutIndex00":
                            ex2=self.__getsymbollist("FUT",y1,y2, "", "")
                            symbolist=symbolist+[x3.split(",")[0] for x3 in ex2.split("|")]
        if symboltype=="" or symboltype in "OPTIONS":
            ex=self.__getsymbollist("OPT", "", "", "", "")
            for y1 in [x1.split(",")[0] for x1 in ex.split("|")]:
                if exchange=="" or exchange in y1:
                    ex1=self.__getsymbollist("OPT",y1, "", "", "")
                    for y2 in [x2.split(",")[0] for x2 in ex1.split("|")]:
                        ex2=self.__getsymbollist("OPT",y1,y2, "", "")
                        for y3 in [x3.split(",")[0] for x3 in ex2.split("|")]:
                            if "HOT" not in y3:
                                ex3=self.__getsymbollist("OPT",y1,y2,y3, "Call")
                                symbolist=symbolist+[x4.split(",")[0] for x4 in ex3.split("|")]
                                ex4=self.__getsymbollist("OPT",y1,y2,y3, "Put")
                                symbolist=symbolist+[x5.split(",")[0] for x5 in ex4.split("|")]
        if symboltype=="" or symboltype in "STKSTOCKS":
            ex=self.__getsymbollist("STK","", "", "", "")
            for y1 in [x.split(",")[0] for x in ex.split("|")][0:2]:
                if exchange=="" or exchange in y1:
                    ex1=self.__getsymbollist("STK", y1, "", "", "")
                    for y2 in [x1.split(",")[0] for x1 in ex1.split("|")]:
                            ex2=self.__getsymbollist("STK",y1, y2, "", "")
                            symbolist=symbolist+[x2.split(",")[0] for x2 in ex2.split("|")]
        return symbolist 

    def getsynu_futuresymbol(self):
        symbolist=[]
        ex=self.__getsymbollist("SYMSELECT", "", "", "", "")
        for y1 in [x1.split(",")[0] for x1 in ex.split("|")]:
            ex1=self.__getsymbollist("SYMSELECT",y1, "SynU", "", "")
            for y2 in [x2.split(",")[0] for x2 in ex1.split("|")]:
                ex2=self.__getsymbollist("SYMSELECT",y1,"SynU",y2, "")
                symbolist=symbolist+[x3.split(",")[0] for x3 in ex2.split("|")]
                #symbolist=symbolist+[{"symbol":x3.split(",")[0],"name":x3.split(",")[1]} for x3 in ex2.split("|")]
        return symbolist

    def __getsymbollist(self, Classify, Exchange, Symbol, Month, CallPut):
        try:
            pythoncom.CoInitialize()
            disp = Git.GetInterfaceFromGlobal(self.cookie, pythoncom.IID_IDispatch)
            interp = client.Dispatch(disp)
            return interp.GetSymbolClassifications(Classify, Exchange, Symbol, Month, CallPut)
        except pythoncom.com_error as e:
            print("getsymbol错误:",e)

    def cancelorder(self, ReportID, Key):
        try:
            pythoncom.CoInitialize()
            disp = Git.GetInterfaceFromGlobal(self.cookie, pythoncom.IID_IDispatch)
            interp = client.Dispatch(disp)
            return interp.CancelOrder(ReportID, Key)
        except pythoncom.com_error as e:
            print("CancelOrder错误:",e)

    def cancelspreadorder(self, bstrReportID):
        try:
            pythoncom.CoInitialize()
            disp = Git.GetInterfaceFromGlobal(self.cookie, pythoncom.IID_IDispatch)
            interp = client.Dispatch(disp)
            return interp.CancelSpreadOrder(bstrReportID)
        except pythoncom.com_error as e:
            print("CancelOrder错误:",e) 

    def changeorderaction(self, bstrReportID, lAction):
        try:
            pythoncom.CoInitialize()
            disp = Git.GetInterfaceFromGlobal(self.cookie, pythoncom.IID_IDispatch)
            interp = client.Dispatch(disp)
            return interp.ChangeOrderAction( bstrReportID, lAction)
        except pythoncom.com_error as e:
            print("CancelOrder错误:",e) 

    def optcomb(self,strAcctMask,SymbolA,SymbolB,Volume:int,CombinationType:int,CombID=""):
        strParam="SYMBOLA="+SymbolA+"&SYMBOLB="+SymbolB+"&VOLUME="+str(Volume)+"&ACTIONTYPE=1"+"&OPTCOMB_CODE="+str(CombinationType)+"&OPTCOMB_ID="+CombID
        return self._generalquery(1, "OPTCOMB",strParam, 1, strAcctMask)

    def optcombsplit(self,strAcctMask,Symbol:str,Volume:int,CombinationType:int,CombID=""):#strParam &SIDEA=2&SIDEB=2
        if "&" in Symbol:
            symlist=Symbol.split("&")[0].split(".")
        else:
            print("合约代码格式错误，组合合约才可拆分")
            return
        temp=symlist[0]+"."+symlist[1]+"."+symlist[2]+"."
        Symbol=Symbol.replace(temp,"")
        Symbol=Symbol.replace("&","^")
        Symbol=symlist[0]+"."+symlist[1]+"2."+symlist[2]+"."+Symbol
        strParam="SYMBOL="+Symbol+"&VOLUME="+str(Volume)+"&ACTIONTYPE=2"+"&OPTCOMB_CODE="+str(CombinationType)+"&OPTCOMB_ID="+CombID
        return self._generalquery(1, "OPTCOMB",strParam, 1, strAcctMask)

    def _generalquery(self, lIndex, strQueryName, strQueryParam, lContentEncodeType, strAcctMask):
        try:
            pythoncom.CoInitialize()
            disp = Git.GetInterfaceFromGlobal(self.cookie, pythoncom.IID_IDispatch)
            interp = client.Dispatch(disp)
            return interp.GeneralQuery(lIndex, strQueryName, strQueryParam, lContentEncodeType, strAcctMask)
        except pythoncom.com_error as e:
            print("CancelOrder错误:",e)

    def getaccoutlist(self,index):
        accitem= client.Dispatch('{758B63D4-D8C9-492B-AB2B-A1014AAC1FA3}')
        self._getaccountdata(1,index,"",accitem)
        return {"AccMask":accitem.BrokerID+"-"+accitem.Account,
        "Account":accitem.Account,
		"AccountName":accitem.AccountName,
		"AccountType":accitem.AccountType,
		"BrokerID":accitem.BrokerID,
		"BrokerName":accitem.BrokerName,
		"ItemType":accitem.ItemType,
		"LoginID":accitem.LoginID,
		"OrderExchange":accitem.OrderExchange,
		"Status":accitem.Status,
		"UserAddGroup":accitem.UserAddGroup,
		"UserName":accitem.UserName}

    def getaccmargin(self,accmast):
        try:
            marginitem= client.Dispatch('{000F4D92-9D84-4B59-AFEF-8EBCDE144D36}')
            self._getaccountdata(9,0,accmast,marginitem)
            marginmuil=1000000
            return {"BrokerID":marginitem.BrokerID,
                    "LoginID":marginitem.LoginID,
                    "UserName":marginitem.UserName,
                    "BrokerName":marginitem.BrokerName,
                    "Account":marginitem.Account,
                    "AccountName":marginitem.AccountName,
                    "TransactDate":marginitem.TransactDate,
                    "TransactTime":marginitem.TransactTime+80000,
                    "BeginningBalance":iff(marginitem.BeginningBalance,marginmuil),
                    "Commissions":iff(marginitem.Commissions,marginmuil),
                    "FrozenCommission":iff(marginitem.FrozenCommission,marginmuil),
                    "ExchangeClearinigFee":iff(marginitem.ExchangeClearinigFee,marginmuil),
                    "BrokerageFee":iff(marginitem.BrokerageFee,marginmuil),
                    "GrossPL":iff(marginitem.GrossPL,marginmuil),
                    "OptionPremium":iff(marginitem.OptionPremium,marginmuil),
                    "CashIn":iff(marginitem.CashIn,marginmuil),
                    "NetPL":iff(marginitem.NetPL,marginmuil),
                    "Deposit":iff(marginitem.Deposit,marginmuil),
                    "Withdraw":iff(marginitem.Withdraw,marginmuil),
                    "CashActivity":iff(marginitem.CashActivity,marginmuil),
                    "ExcessEquity":iff(marginitem.ExcessEquity,marginmuil),
                    "WithdrawQuota":iff(marginitem.WithdrawQuota,marginmuil),
                    "EndingBalance":iff(marginitem.EndingBalance,marginmuil),
                    "OpenTradeEquity":iff(marginitem.OpenTradeEquity,marginmuil),
                    "TotalEquity":iff(marginitem.TotalEquity,marginmuil),
                    "OptionNetMarketValue":iff(marginitem.OptionNetMarketValue,marginmuil),
                    "AccountValueAtMarket":iff(marginitem.AccountValueAtMarket,marginmuil),
                    "InitialMarginRequirement":iff(marginitem.InitialMarginRequirement,marginmuil),
                    "MaintenanceMarginRequirement":iff(marginitem.MaintenanceMarginRequirement,marginmuil),
                    "CurrMargin":iff(marginitem.CurrMargin,marginmuil),
                    "ExchangeMargin":iff(marginitem.ExchangeMargin,marginmuil),
                    "MarginDeficit":iff(marginitem.MarginDeficit,marginmuil),
                    "FrozenMargin":iff(marginitem.FrozenMargin,marginmuil),
                    "FrozenCash":iff(marginitem.FrozenCash,marginmuil),
                    "ReserveBalance":iff(marginitem.ReserveBalance,marginmuil),
                    "Credit":iff(marginitem.Credit,marginmuil),
                    "Mortgage":iff(marginitem.Mortgage,marginmuil),
                    "PreMortgage":iff(marginitem.PreMortgage,marginmuil),
                    "PreCredit":iff(marginitem.PreCredit,marginmuil),
                    "PreDeposit":iff(marginitem.PreDeposit,marginmuil),
                    "PreMargin":iff(marginitem.PreMargin,marginmuil),
                    "DeliveryMargin":iff(marginitem.DeliveryMargin,marginmuil),
                    "ExchangeDeliveryMargin":iff(marginitem.ExchangeDeliveryMargin,marginmuil),
                    "CurrencyToSystem":marginitem.CurrencyToSystem,
                    "CurrencyConversionRate":iff(marginitem.CurrencyConversionRate,marginmuil),
                    "CurrencyToClient":marginitem.CurrencyToClient,
                    "ConvertedAccountValueAtMkt":iff(marginitem.ConvertedAccountValueAtMkt,marginmuil),
                    "ExerciseIncome":iff(marginitem.ExerciseIncome,marginmuil),
                    "IncomeBalance":iff(marginitem.IncomeBalance,marginmuil),
                    "InterestBase":iff(marginitem.InterestBase,marginmuil),
                    "Interest":iff(marginitem.Interest,marginmuil),
                    "MarginLevel":iff(marginitem.GetItemData("MarginLevel"),marginmuil),
                    "UPLForOptions":iff(marginitem.GetItemData("UPLForOptions"),marginmuil),
                    "LongOptionNetMarketValue":iff(marginitem.GetItemData("LongOptionNetMarketValue"),marginmuil),
                    "ShortOptionNetMarketValue":iff(marginitem.GetItemData("ShortOptionNetMarketValue"),marginmuil),
                    "FrozenpPremium":iff(marginitem.GetItemData("FrozenpPremium"),marginmuil),
                    "MarginExcess":iff(marginitem.GetItemData("MarginExcess"),marginmuil),
                    "AdjustedEquity":iff(marginitem.GetItemData("AdjustedEquity"),marginmuil),
                    "PreFundMortgageIn":iff(marginitem.GetItemData("PreFundMortgageIn"),marginmuil),
                    "PreFundMortgageOut":iff(marginitem.GetItemData("PreFundMortgageOut"),marginmuil),
                    "FundMortgageIn":iff(marginitem.GetItemData("FundMortgageIn"),marginmuil),
                    "FundMortgageOut":iff(marginitem.GetItemData("FundMortgageOut"),marginmuil),
                    "FundMortgageAvailable":iff(marginitem.GetItemData("FundMortgageAvailable"),marginmuil),
                    "MortgageableFund":iff(marginitem.GetItemData("MortgageableFund"),marginmuil),
                    "SpecProductMargin":iff(marginitem.GetItemData("SpecProductMargin"),marginmuil),
                    "SpecProductFrozenMargin":iff(marginitem.GetItemData("SpecProductFrozenMargin"),marginmuil),
                    "SpecProductCommission":iff(marginitem.GetItemData("SpecProductCommission"),marginmuil),
                    "SpecProductFrozenCommission":iff(marginitem.GetItemData("SpecProductFrozenCommission"),marginmuil),
                    "SpecProductPositionProfit":iff(marginitem.GetItemData("SpecProductPositionProfit"),marginmuil),
                    "SpecProductCloseProfit":iff(marginitem.GetItemData("SpecProductCloseProfit"),marginmuil),
                    "SpecProductPositionProfitByAlg":iff(marginitem.GetItemData("SpecProductPositionProfitByAlg"),marginmuil),
                    "SpecProductExchangeMargin":iff(marginitem.GetItemData("SpecProductExchangeMargin"),marginmuil),
                    "FloatProfitByDate":iff(marginitem.GetItemData("FloatProfitByDate"),marginmuil),
                    "FloatProfitByTrade":iff(marginitem.GetItemData("FloatProfitByTrade"),marginmuil),
                    "FutureProfitByDay":iff(marginitem.GetItemData("FutureProfitByDay"),marginmuil),
                    "ReferenceRiskRate":iff(marginitem.GetItemData("ReferenceRiskRate"),marginmuil),
                    "TryExcessEquity":iff(marginitem.GetItemData("TryExcessEquity"),marginmuil),
                    "DynamicEquity":iff(marginitem.GetItemData("DynamicEquity"),marginmuil),
                    "MarketPremium":iff(marginitem.GetItemData("MarketPremium"),marginmuil),
                    "OptionPremiumCoin":iff(marginitem.GetItemData("OptionPremiumCoin"),marginmuil),
                    "StockReferenceMarket":iff(marginitem.GetItemData("StockReferenceMarket"),marginmuil),
                    "RiskRate":iff(marginitem.GetItemData("RiskRate"),marginmuil),
                    "StockMarketValue":iff(marginitem.GetItemData("StockMarketValue"),marginmuil),
                    "TheoMktVal":iff(marginitem.GetItemData("TheoMktVal"),marginmuil),
                    "TheoMktValEquity":iff(marginitem.GetItemData("TheoMktValEquity"),marginmuil),
                    "DoUpdate":iff(marginitem.GetItemData("DoUpdate"),1)}
        
        except pythoncom.com_error as e:
            print("gettradeingdays错误:",e)

    def getposition(self,index,acc):
        try:
            #win32event.WaitForSingleObject(self.ev.event, 1)
            pythoncom.CoInitialize()
            positem= client.Dispatch('{D5F1627F-0150-45C4-86EB-6FAAC952775C}')
            self._getaccountdata(6,index,acc,positem)
            return {"AbandonFrozen":positem.AbandonFrozen,
                    "Account":positem.Account,
                    "AccountName":positem.AccountName,
                    "AvgPrice":iff(positem.AvgPrice,10000000000),
                    "BrokerID":positem.BrokerID,
                    "BrokerName":positem.BrokerName,
                    "CallPut":positem.CallPut,
                    "CallPut2":positem.CallPut2,
                    "CashIn":positem.CashIn,
                    "CloseAmount":positem.CloseAmount,
                    "CloseProfit":positem.CloseProfit,
                    "CloseProfitByDate":positem.CloseProfitByDate,
                    "CloseProfitByTrade":positem.CloseProfitByTrade,
                    "CloseVolume":positem.CloseVolume,
                    "CombLongFrozen":positem.CombLongFrozen,
                    "CombPosition":positem.CombPosition,
                    "CombShortFrozen":positem.CombShortFrozen,
                    "Commission":positem.Commission,
                    "Covered":positem.Covered,
                    "CurrencyToSystem":positem.CurrencyToSystem,
                    "Exchange":positem.Exchange,
                    "FrozenCash":positem.FrozenCash,
                    "FrozenMargin":positem.FrozenMargin,
                    "ItemType":positem.ItemType,
                    "Lock_ExecFrozen":positem.Lock_ExecFrozen,
                    "LoginID":positem.LoginID,
                    "LongAvailable":positem.LongAvailable,
                    "LongAvgPrice":iff(positem.LongAvgPrice,10000000000),
                    "LongFrozen":positem.LongFrozen,
                    "LongFrozenAmount":positem.LongFrozenAmount,
                    "MarginRateByMoney":positem.MarginRateByMoney,
                    "MarginRateByVolume":positem.MarginRateByVolume,
                    "MatchedPrice1":iff(positem.MatchedPrice1,10000000000),
                    "MatchedPrice2":iff(positem.MatchedPrice2,10000000000),
                    "Month":positem.Month,
                    "Month2":positem.Month2,
                    "OpenAmount":positem.OpenAmount,
                    "OpenCost":positem.OpenCost,
                    "OpenDate":positem.OpenDate,
                    "OpenPrice":iff(positem.OpenPrice,10000000000),
                    "OpenVolume":positem.OpenVolume,
                    "OrderID":positem.OrderID,
                    "PositionCost":positem.PositionCost,
                    "PositionProfitByDate":positem.PositionProfitByDate,
                    "PositionProfitByTrade":positem.PositionProfitByTrade,
                    "PreMargin":positem.PreMargin,
                    "PrevSettlementPrice":iff(positem.PrevSettlementPrice,10000000000),
                    "Quantity":positem.Quantity,
                    "Security":positem.Security,
                    "Security2":positem.Security2,
                    "SecurityType":positem.SecurityType,
                    "SettlementPrice":positem.SettlementPrice,
                    "ShortAvailable":positem.ShortAvailable,
                    "ShortAvgPrice":iff(positem.ShortAvgPrice,10000000000),
                    "ShortFrozen":positem.ShortFrozen,
                    "ShortFrozenAmount":positem.ShortFrozenAmount,
                    "Side":positem.Side,
                    "Side1":positem.Side1,
                    "Side2":positem.Side2,
                    "StrikeFrozen":positem.StrikeFrozen,
                    "StrikeFrozenAmount":positem.StrikeFrozenAmount,
                    "StrikePrice":iff(positem.StrikePrice,10000000000),
                    "StrikePrice2":iff(positem.StrikePrice2,10000000000),
                    "SumLongQty":positem.SumLongQty,
                    "SumShortQty":positem.SumShortQty,
                    "Symbol":positem.Symbol,
                    "SymbolA":positem.SymbolA,
                    "SymbolB":positem.SymbolB,
                    "TdBuyQty":positem.TdBuyQty,
                    "TdSellQty":positem.TdSellQty,
                    "TdTotalQty":positem.TdTotalQty,
                    "TodayLongQty":positem.TodayLongQty,
                    "TodayShortQty":positem.TodayShortQty,
                    "TransactDate":positem.TransactDate,
                    "TransactTime":positem.TransactTime+80000,
                    "UnrealizedPL":positem.UnrealizedPL,
                    "UsedMargin":positem.UsedMargin,
                    "UserName":positem.UserName,
                    "WorkingLong":positem.WorkingLong,
                    "WorkingShort":positem.WorkingShort,
                    "YdLongQty":positem.YdLongQty,
                    "YdShortQty":positem.YdShortQty}
        except pythoncom.com_error as e:
            print("getposition错误:",e)

    def getcombposition(self,index,acc):
        try:
            combpositem= client.Dispatch('{D5F1627F-0150-45C4-86EB-6FAAC952775C}')
            self._getaccountdata(8,index,acc,combpositem)
            if "^" in combpositem.Symbol:
                return {'LoginID':combpositem.LoginID,
                        'UserName':combpositem.UserName,
                        'BrokerID':combpositem.BrokerID, 
                        'BrokerName':combpositem.BrokerName,
                        'Account':combpositem.Account, 
                        'AccountName':combpositem.AccountName,
                        'SecurityType':combpositem.SecurityType, 
                        'Symbol':combpositem.SymbolA+"&"+combpositem.SymbolB, #combpositem.Symbol,
                        'SymbolA':combpositem.SymbolA, 
                        'SymbolB':combpositem.SymbolB,
                        'CurrencyToSystem':combpositem.CurrencyToSystem,
                        'CombinationType':combpositem.GetItemData("OptCombCode"), 
                        'TransactDate':combpositem.TransactDate, 
                        'TransactTime':combpositem.TransactTime, 
                        'SpreadType':combpositem.GetItemData("SpreadType"),
                        'Side':combpositem.Side, 
                        'Side1':combpositem.Side1, 
                        'Side2':combpositem.Side2, 
                        'Quantity':combpositem.Quantity,
                        'OptCombID':combpositem.GetItemData("OptCombID"),
                        'CombLongPosition':combpositem.GetItemData("CombLongPosition"), 
                        'CombShortPosition':combpositem.GetItemData("CombShortPosition"), 
                        'UsedMargin':combpositem.UsedMargin}
        except pythoncom.com_error as e:
            print("getcombposition错误:",e)

    def getcombinationorder(self,index,acc):
        try:
            comborder= client.Dispatch('{461286A0-EC62-47C9-B93D-9CBED37194ED}')
            self._getaccountdata(32,index,acc,comborder)
            return {'Account':comborder.GetItemData("Account"),
                    'BrokerID':comborder.GetItemData("BrokerID"),
                    'OrderID':comborder.GetItemData("OrderID"),
                    'FilledID':comborder.GetItemData("FilledID"),
                    'Symbol':comborder.GetItemData("SymbolA")+"&"+comborder.GetItemData("SymbolB"),
                    'Quantity':comborder.GetItemData("Quantity"),
                    'OptCombCode':comborder.GetItemData("OptCombCode"),
                    'Side':comborder.GetItemData("Side"),
                    'CombSide':comborder.GetItemData("CombSide"),
                    'ExecType':comborder.GetItemData("ExecType")}
        except pythoncom.com_error as e:
            print("getcombinationorder错误:",e)

    def _getaccountdata(self, nType, nIndex, AcctMask,idispatch):
        try:
            pythoncom.CoInitialize()
            disp = Git.GetInterfaceFromGlobal(self.cookie, pythoncom.IID_IDispatch)
            interp = client.Dispatch(disp)
            interp.GetAccountData(nType, nIndex, AcctMask, idispatch)
        except pythoncom.com_error as e:
            print("_getaccountdata错误:",e)
    
    def getpositionmoniter(self):
        try:
            pythoncom.CoInitialize()
            disp = Git.GetInterfaceFromGlobal(self.cookie, pythoncom.IID_IDispatch)
            interp = client.Dispatch(disp)
            outitem= client.Dispatch('{6E586DA2-9AA7-48DA-83EB-510F61E3CBB9}')
            interp.GetPositionTracker(outitem)
            result=[]
            for itemkey in outitem.GetItemKeys().strip(";").split(";"):
                for subkey in outitem.GetSubKeys(itemkey).strip(";").split(";"):
                    temp={}
                    if ":" in itemkey:
                        itk=itemkey.split(":")
                        temp["Symbol"]= itk[1]
                        idx=itk[0].find("-")
                        if idx>0:
                            temp["BrokerID"]=itk[0][0:idx]
                            temp["Account"]=itk[0][idx+1:]
                        else:
                            temp["BrokerID"]=""
                            temp["Account"]=itk[0]
                    else:
                        temp["BrokerID"]=""
                        temp["Account"]=""
                        temp["Symbol"]= itemkey
                    temp["SubKey"]= subkey
                    temp["$Delta"]= iff(outitem.GetSubItemValue(itemkey,subkey,"$Delta"),10000000000)
                    temp["Td$Delta"]=iff(outitem.GetSubItemValue(itemkey,subkey,"Td$Delta"),10000000000)
                    temp["$Gamma"]= iff(outitem.GetSubItemValue(itemkey,subkey,"$Gamma"),10000000000)
                    temp["Td$Gamma"]=iff(outitem.GetSubItemValue(itemkey,subkey,"Td$Gamma"),10000000000)
                    temp["Yd$Gamma"]=iff(outitem.GetSubItemValue(itemkey,subkey,"Yd$Gamma"),10000000000)
                    temp["$Theta"]= iff(outitem.GetSubItemValue(itemkey,subkey,"$Theta"),10000000000)
                    temp["Td$Theta"]=iff(outitem.GetSubItemValue(itemkey,subkey,"Td$Theta"),10000000000)
                    temp["Yd$Theta"]=iff(outitem.GetSubItemValue(itemkey,subkey,"Yd$Theta"),10000000000)
                    temp["$Vega"]= iff(outitem.GetSubItemValue(itemkey,subkey,"$Vega"),10000000000)
                    temp["Td$Vega"]=iff(outitem.GetSubItemValue(itemkey,subkey,"Td$Vega"),10000000000)
                    temp["Yd$Vega"]=iff(outitem.GetSubItemValue(itemkey,subkey,"Yd$Vega"),10000000000)
                    temp["$Rho"]=iff(outitem.GetSubItemValue(itemkey,subkey,"$Rho"),10000000000)
                    temp["Td$Rho"]= iff(outitem.GetSubItemValue(itemkey,subkey,"Td$Rho"),10000000000)
                    temp["Yd$Rho"]= iff(outitem.GetSubItemValue(itemkey,subkey,"Yd$Rho"),10000000000)
                    temp["$Charm"]=iff(outitem.GetSubItemValue(itemkey,subkey,"$Charm"),10000000000)
                    temp["Td$Charm"]=iff(outitem.GetSubItemValue(itemkey,subkey,"Td$Charm"),10000000000)
                    temp["$Vanna"]= iff(outitem.GetSubItemValue(itemkey,subkey,"$Vanna"),10000000000)
                    temp["Td$Vanna"]= iff(outitem.GetSubItemValue(itemkey,subkey,"Td$Vanna"),10000000000)
                    temp["$Vomma"]= iff(outitem.GetSubItemValue(itemkey,subkey,"$Vomma"),10000000000)
                    temp["Td$Vomma"]= iff(outitem.GetSubItemValue(itemkey,subkey,"Td$Vomma"),10000000000)
                    temp["$Speed"]= iff(outitem.GetSubItemValue(itemkey,subkey,"$Speed"),10000000000) 
                    temp["Td$Speed"]= iff(outitem.GetSubItemValue(itemkey,subkey,"Td$Speed"),10000000000)
                    temp["$Zomma"]= iff(outitem.GetSubItemValue(itemkey,subkey,"$Zomma"),10000000000) 
                    temp["Td$Zomma"]= iff(outitem.GetSubItemValue(itemkey,subkey,"Td$Zomma"),10000000000)
                    temp["TimeValue"]= iff(outitem.GetSubItemValue(itemkey,subkey,"TimeValue"),10000000000)
                    temp["TdTimeValue"]=iff(outitem.GetSubItemValue(itemkey,subkey,"TdTimeValue"),10000000000)
                    temp["YdTimeValue"]=iff(outitem.GetSubItemValue(itemkey,subkey,"YdTimeValue"),10000000000)
                    temp["PnL"]= iff(outitem.GetSubItemValue(itemkey,subkey,"PnL"),10000000000)
                    temp["TdPnL"]= iff(outitem.GetSubItemValue(itemkey,subkey,"TdPnL"),10000000000)
                    temp["YdPnL"]= iff(outitem.GetSubItemValue(itemkey,subkey,"YdPnL"),10000000000)
                    temp["TheoPnL"]= iff(outitem.GetSubItemValue(itemkey,subkey,"TheoPnL"),10000000000)
                    temp["TdTheoPnL"]=iff(outitem.GetSubItemValue(itemkey,subkey,"TdTheoPnL"),10000000000)
                    temp["YdTheoPnl"]= iff(outitem.GetSubItemValue(itemkey,subkey,"YdTheoPnl"),10000000000)
                    temp["FloatPnL"]= iff(outitem.GetSubItemValue(itemkey,subkey,"FloatPnL"),10000000000)
                    temp["ClosePnL"]= iff(outitem.GetSubItemValue(itemkey,subkey,"ClosePnL"),10000000000)
                    temp["CallOI"]= outitem.GetSubItemValue(itemkey,subkey,"CallOI")
                    temp["TdCallOI"]=outitem.GetSubItemValue(itemkey,subkey,"TdCallOI")
                    temp["YdCallOI"]=outitem.GetSubItemValue(itemkey,subkey,"YdCallOI")
                    temp["PutOI"]=outitem.GetSubItemValue(itemkey,subkey,"PutOI")
                    temp["TdPutOI"]= outitem.GetSubItemValue(itemkey,subkey,"TdPutOI")
                    temp["YdPutOI"]= outitem.GetSubItemValue(itemkey,subkey,"YdPutOI")
                    temp["LongOI"]= outitem.GetSubItemValue(itemkey,subkey,"LongOI")
                    temp["ShortOI"]= outitem.GetSubItemValue(itemkey,subkey,"ShortOI")
                    temp["TdOpenQty"]=outitem.GetSubItemValue(itemkey,subkey,"TdOpenQty")
                    temp["TdCloseQty"]=outitem.GetSubItemValue(itemkey,subkey,"TdCloseQty")
                    temp["NetFill"]= iff(outitem.GetSubItemValue(itemkey,subkey,"BSFill"))
                    temp["PosFillRatio"]= iff(outitem.GetSubItemValue(itemkey,subkey,"PosFillRatio"),10000000000)
                    temp["1%$Gamma"]= iff(outitem.GetSubItemValue(itemkey,subkey,"1Pct$Gamma"),10000000000)
                    temp["1%Td$Gamma"]= iff(outitem.GetSubItemValue(itemkey,subkey,"1PctTd$Gamma"),10000000000)
                    temp["1%Yd$Gamma"]=iff(outitem.GetSubItemValue(itemkey,subkey,"1PctYd$Gamma"),10000000000)
                    temp["1%$Vanna"]= iff(outitem.GetSubItemValue(itemkey,subkey,"1Pct$Vanna"),10000000000)
                    temp["1%Td$Vanna"]= iff(outitem.GetSubItemValue(itemkey,subkey,"1PctTd$Vanna"),10000000000)
                    temp["TotalFill"]=iff(outitem.GetSubItemValue(itemkey,subkey,"BuyFill"))+iff(outitem.GetSubItemValue(itemkey,subkey,"SellFill"))
                    temp["TotalPosition"]=iff(outitem.GetSubItemValue(itemkey,subkey,"LongOI"))+iff(outitem.GetSubItemValue(itemkey,subkey,"ShortOI"))
                    temp["NetPosition"]=iff(outitem.GetSubItemValue(itemkey,subkey,"LongOI"))-iff(outitem.GetSubItemValue(itemkey,subkey,"ShortOI"))
                    temp["YdNetPosition"]=iff(outitem.GetSubItemValue(itemkey,subkey,"YdCallOI"))+iff(outitem.GetSubItemValue(itemkey,subkey,"YdPutOI"))
                    temp["1%$Delta"]=iff(outitem.GetSubItemValue(itemkey,subkey,"$Delta"),1000000000000)
                    temp["1%Td$Delta"]=iff(outitem.GetSubItemValue(itemkey,subkey,"Td$Delta"),1000000000000)
                    temp["1%Yd$Delta"]=iff(outitem.GetSubItemValue(itemkey,subkey,"Yd$Delta"),1000000000000)
                    temp["OrderNumbers"]=outitem.GetSubItemValue(itemkey,subkey,"OrderNumbers")
                    temp["DealNumbers"]=outitem.GetSubItemValue(itemkey,subkey,"DealNumbers")
                    temp["DeleteNumbers"]=outitem.GetSubItemValue(itemkey,subkey,"DeleteNumbers")
                    result.append(temp)
            return result#outitem.GetItemKeys()
        except pythoncom.com_error as e:
            print("getpositiontracker错误:",e) 

    def getproductcurrency(self, SymbolID):
    # Result is a Unicode object
        try:
            pythoncom.CoInitialize()
            disp = Git.GetInterfaceFromGlobal(self.cookie, pythoncom.IID_IDispatch)
            interp = client.Dispatch(disp)
            return interp.GetProductCurrency(SymbolID)
        except pythoncom.com_error as e:
            print("getproductcurrency错误:",e)

    def getactiveorder(self):
        try:
            pythoncom.CoInitialize()
            activeorder=[]
            ReportItems= client.Dispatch('{597B9AE7-55D3-48B4-92F0-12840541C8C7}')
            self.__getreportdata(1,"",ReportItems)
            for i in range(ReportItems.Count):
                activeorderdict=self.getreportbyid(ReportItems.GetReportID(i))
                activeorder.append(activeorderdict)
            return activeorder
        except pythoncom.com_error as e:
            print("getactiveorder错误:",e)

    def getorderreport(self):
        try:
            pythoncom.CoInitialize()
            report=[]
            ReportItems= client.Dispatch('{597B9AE7-55D3-48B4-92F0-12840541C8C7}')
            self.__getreportdata(3,"",ReportItems)
            for i in range(ReportItems.Count):
                reportdict=self.getreportbyid(ReportItems.GetReportID(i))
                report.append(reportdict)
            return report
        except pythoncom.com_error as e:
            print("getallorderreport错误:",e)

    def getdetailfilledreport(self):
        try:
            pythoncom.CoInitialize()
            fillreport=[]
            ReportItems= client.Dispatch('{597B9AE7-55D3-48B4-92F0-12840541C8C7}')
            self.__getreportdata(2,"",ReportItems)
            for i in range(ReportItems.Count):
                strReportID = ReportItems.GetReportID(i)
                ExecutionReportItem=client.Dispatch('{C4D0CDB7-8F21-4752-AF97-025ADC7B7FD9}')
                self. __getreportdata(0,strReportID,ExecutionReportItem)
                for j in range(ExecutionReportItem.FilledOrdersCount):
                    fillreportdict=self.getfilledreportbyid(ExecutionReportItem.GetFilledOrderReportID(j))
                    fillreportdict["ReportID"]=strReportID
                    fillreport.append(fillreportdict)
            return fillreport
        except pythoncom.com_error as e:
            print("getfilledreport错误:",e) 

    def getfilledreport(self):
        try:
            pythoncom.CoInitialize()
            fillreport=[]
            ReportItems= client.Dispatch('{597B9AE7-55D3-48B4-92F0-12840541C8C7}')
            self.__getreportdata(2,"",ReportItems)
            for i in range(ReportItems.Count):
                reportdict=self.getreportbyid(ReportItems.GetReportID(i))
                fillreport.append(reportdict)
            return fillreport
        except pythoncom.com_error as e:
            print("getfilledreport错误:",e) 
    def getfilledreportbyid(self,ReportID):
        try:
            pythoncom.CoInitialize()
            FilledOrderItem=client.Dispatch('{61B1724C-72CA-46DF-85E9-D3EF72F7705F}')
            self. __getreportdata(0,ReportID,FilledOrderItem)
            return {"Account":FilledOrderItem.Account,
                    "BrokerID":FilledOrderItem.BrokerID,
                    "CallPut":FilledOrderItem.CallPut,
                    "CallPut2":FilledOrderItem.CallPut2,
                    "Exchange":FilledOrderItem.Exchange,
                    "MatchedPrice":iff(FilledOrderItem.MatchedPrice,10000000000),
                    "MatchedPrice1":iff(FilledOrderItem.MatchedPrice1,10000000000),
                    "MatchedPrice2":iff(FilledOrderItem.MatchedPrice2,10000000000),
                    "MatchedQty":FilledOrderItem.MatchedQty,
                    "Month":FilledOrderItem.Month,
                    "Month2":FilledOrderItem.Month2,
                    "OrderID":FilledOrderItem.OrderID,
                    "PositionEffect":FilledOrderItem.PositionEffect,
                    "DetailReportID":FilledOrderItem.ReportID,
                    "Security":FilledOrderItem.Security,
                    "Security2":FilledOrderItem.Security2,
                    "SecurityType":FilledOrderItem.SecurityType,
                    "Side":FilledOrderItem.Side,
                    "Side1":FilledOrderItem.Side1,
                    "Side2":FilledOrderItem.Side2,
                    "Strategy":FilledOrderItem.Strategy,
                    "StrikePrice":iff(FilledOrderItem.StrikePrice,10000000000),
                    "StrikePrice2":iff(FilledOrderItem.StrikePrice2,10000000000),
                    "Symbol":FilledOrderItem.Symbol,
                    "SymbolA":FilledOrderItem.SymbolA,
                    "SymbolB":FilledOrderItem.SymbolB,
                    "TradeType":FilledOrderItem.TradeType,
                    "TransactDate":FilledOrderItem.TransactDate,
                    "TransactTime":FilledOrderItem.TransactTime,
                    "UserKey1":FilledOrderItem.UserKey1,
                    "UserKey2":FilledOrderItem.UserKey2,
                    "UserKey3":FilledOrderItem.UserKey3}
        except pythoncom.com_error as e:
            print("getreportbyid错误:",e) 

    def getreportbyid(self,ReportID):
        try:
            pythoncom.CoInitialize()
            ExecutionReportItem=client.Dispatch('{C4D0CDB7-8F21-4752-AF97-025ADC7B7FD9}')
            self. __getreportdata(0,ReportID,ExecutionReportItem)
            return {"Account":ExecutionReportItem.Account,
            "AvgPrice":iff(ExecutionReportItem.AvgPrice,10000000000),
            "BrokerID":ExecutionReportItem.BrokerID,
            "CallPut":ExecutionReportItem.CallPut,
            "CallPut2":ExecutionReportItem.CallPut2,
            "CumQty":ExecutionReportItem.CumQty,
            "DayTrade":ExecutionReportItem.DayTrade,
            "ErrorCode":ExecutionReportItem.ErrorCode,
            "ExCode":ExecutionReportItem.ExCode,
            "Exchange":ExecutionReportItem.Exchange,
            "ExecHis":ExecutionReportItem.ExecHis,
            "ExecType":ExecutionReportItem.ExecType,
            "ExecTypeText":ExecutionReportItem.ExecTypeText,
            "ExtraFields":ExecutionReportItem.ExtraFields,
            "Group":ExecutionReportItem.Group,
            "IsRestoreData":ExecutionReportItem.IsRestoreData,
            "ItemType":ExecutionReportItem.ItemType,
            "LeavesQty":ExecutionReportItem.LeavesQty,
            "Month":ExecutionReportItem.Month,
            "Month2":ExecutionReportItem.Month2,
            "OrderID":ExecutionReportItem.OrderID,
            "OrderQty":ExecutionReportItem.OrderQty,
            "OrderResult":ExecutionReportItem.OrderResult,
            "OrderStatusCount":ExecutionReportItem.OrderStatusCount,
            "OrderType":ExecutionReportItem.OrderType,
            "OrgSource":ExecutionReportItem.OrgSource,
            "OriginalQty":ExecutionReportItem.OriginalQty,
            "PositionEffect":ExecutionReportItem.PositionEffect,
            "Price":iff(ExecutionReportItem.Price,10000000000),
            "ReportID":ExecutionReportItem.ReportID,
            "Security":ExecutionReportItem.Security,
            "Security2":ExecutionReportItem.Security2,
            "SecurityType":ExecutionReportItem.SecurityType,
            "Side":ExecutionReportItem.Side,
            "Side1":ExecutionReportItem.Side1,
            "Side2":ExecutionReportItem.Side2,
            "StopPrice":iff(ExecutionReportItem.StopPrice,10000000000),
            "Strategy":ExecutionReportItem.Strategy,
            "StrikePrice":iff(ExecutionReportItem.StrikePrice,10000000000),
            "StrikePrice2":iff(ExecutionReportItem.StrikePrice2,10000000000),
            "SubOrdersCount":ExecutionReportItem.SubOrdersCount,
            "Symbol":ExecutionReportItem.Symbol,
            "SymbolA":ExecutionReportItem.SymbolA,
            "SymbolB":ExecutionReportItem.SymbolB,
            "TimeInForce":ExecutionReportItem.TimeInForce,
            "TouchCondition":ExecutionReportItem.TouchCondition,
            "TradeDate":ExecutionReportItem.TradeDate,
            "TradeType":ExecutionReportItem.TradeType,
            "TrailingAmount":ExecutionReportItem.TrailingAmount,
            "TransactDate":ExecutionReportItem.TransactDate,
            "TransactTime":ExecutionReportItem.TransactTime+80000,
            "TriggeredPrice":iff(ExecutionReportItem.TriggeredPrice,10000000000),
            "UserKey1":ExecutionReportItem.UserKey1,
            "UserKey2":ExecutionReportItem.UserKey2,
            "UserKey3":ExecutionReportItem.UserKey3}
        except pythoncom.com_error as e:
            print("getreportbyid错误:",e) 

    def __getreportdata(self, ReportType,ReportID,ReportItems):
        try:
            pythoncom.CoInitialize()
            disp = Git.GetInterfaceFromGlobal(self.cookie, pythoncom.IID_IDispatch)
            interp = client.Dispatch(disp)
            interp.GetReportData(ReportType, ReportID, ReportItems)
        except pythoncom.com_error as e:
            print("__getreportdata错误:",e) 
    def neworder(self,ordarg:OrderStruct):
        if "TC.S" in ordarg.Symbol:
            ordkey,msg=self.newstockorder(ordarg) 
        else:
            ordkey,msg=self.newfutoptorder(ordarg)
        return ordkey,msg
        #获取委托单信息
    def getorderinfo(self, ordkey):
        if ordkey in self.eventobj.orderinfo.keys():
            return self.eventobj.orderinfo[ordkey]
        else:
            return
    def newstockorder(self,stkordarg:OrderStruct):
        stkorditem=client.Dispatch("{26A9FCF9-93E2-486F-8139-A3D2772957B9}")
        ordid=str(uuid.uuid1())
        stkorditem.Account=stkordarg.Account
        stkorditem.BrokerID=stkordarg.BrokerID
        stkorditem.Symbol=stkordarg.Symbol
        stkorditem.ChasePrice=stkordarg.ChasePrice
        stkorditem.ContingentSymbol=stkordarg.ContingentSymbol
        stkorditem.DiscloseQty=stkordarg.DiscloseQty
        stkorditem.GroupID=stkordarg.GroupID
        stkorditem.GroupType=stkordarg.GroupType
        stkorditem.Interval=stkordarg.Interval
        stkorditem.LeftoverAction=stkordarg.LeftoverAction
        stkorditem.OrderQty=stkordarg.OrderQty
        stkorditem.OrderType=stkordarg.OrderType
        stkorditem.Price=stkordarg.Price*10000000000
        stkorditem.Side=stkordarg.Side
        stkorditem.SlicedType=stkordarg.SlicedType
        stkorditem.StopPrice=stkordarg.StopPrice*10000000000
        stkorditem.Strategy=stkordarg.Strategy
        stkorditem.Synthetic=stkordarg.Synthetic
        stkorditem.TimeInForce=stkordarg.TimeInForce
        stkorditem.TouchCondition=stkordarg.TouchCondition
        stkorditem.TouchField=stkordarg.TouchField
        stkorditem.TouchPrice=stkordarg.TouchPrice*10000000000
        stkorditem.TrailingAmount=stkordarg.TrailingAmount
        stkorditem.TrailingField=stkordarg.TrailingField
        stkorditem.TrailingType=stkordarg.TrailingType
        stkorditem.UserKey1=ordid
        stkorditem.UserKey2=stkordarg.UserKey2
        #stkorditem.UserKey3="tcoreapi.py"
        stkorditem.Variance=stkordarg.Variance
        stkorditem.ExtCommands=stkordarg.ExtCommands+",SelfTradePrevention="+str(stkordarg.SelfTradePrevention)
        stkorditem.ExCode=stkordarg.ExCode
        stkorditem.Exchange=stkordarg.Exchange
        stkorditem.TradeType=stkordarg.TradeType
        ordresult=self._neworder(8,stkorditem)
        if ordresult>=1:
            return ordid,"委托成功"
        else:
            print(self.ordererr[str(ordresult)])
            return None,self.ordererr[str(ordresult)]

    def newfutoptorder(self,ordargs:OrderStruct):
        futoptorditem=client.Dispatch("{FD1350F3-7D1B-4DAF-840F-B7BF6DE06607}")
        ordid=str(uuid.uuid1())
        futoptorditem.Account=ordargs.Account
        futoptorditem.BrokerID=ordargs.BrokerID
        futoptorditem.Symbol=ordargs.Symbol
        futoptorditem.SymbolA=ordargs.SymbolA
        futoptorditem.SymbolB=ordargs.SymbolB
        futoptorditem.Price=ordargs.Price*10000000000
        futoptorditem.StopPrice=ordargs.StopPrice*10000000000
        futoptorditem.Side=ordargs.Side
        futoptorditem.Side1=ordargs.Side1
        futoptorditem.Side2=ordargs.Side2
        futoptorditem.OrderQty=ordargs.OrderQty
        futoptorditem.OrderType=ordargs.OrderType
        futoptorditem.TimeInForce=ordargs.TimeInForce
        futoptorditem.PositionEffect=ordargs.PositionEffect
        futoptorditem.ContingentSymbol=ordargs.ContingentSymbol
        futoptorditem.TrailingAmount=ordargs.TrailingAmount
        futoptorditem.TrailingField=ordargs.TrailingField
        futoptorditem.TrailingType=ordargs.TrailingType
        futoptorditem.TouchCondition=ordargs.TouchCondition
        futoptorditem.TouchField=ordargs.TouchField
        futoptorditem.TouchPrice=ordargs.TouchPrice*10000000000
        futoptorditem.Synthetic=ordargs.Synthetic
        futoptorditem.GroupID=ordargs.GroupID
        futoptorditem.GroupType=ordargs.GroupType
        futoptorditem.GrpAcctOrdType=ordargs.GrpAcctOrdType
        futoptorditem.ChasePrice=ordargs.ChasePrice
        futoptorditem.Strategy=ordargs.Strategy
        futoptorditem.UserKey1=ordid
        futoptorditem.UserKey2=ordargs.UserKey2
        #futoptorditem.UserKey3="tcoreapi.py"
        futoptorditem.SlicedPriceField=ordargs.SlicedPriceField
        futoptorditem.SlicedTicks=ordargs.SlicedTicks
        futoptorditem.SlicedType=ordargs.SlicedType
        futoptorditem.DiscloseQty=ordargs.DiscloseQty
        futoptorditem.Variance=ordargs.Variance
        futoptorditem.Interval=ordargs.Interval
        futoptorditem.LeftoverAction=ordargs.LeftoverAction
        futoptorditem.ExtCommands=ordargs.ExtCommands+",SelfTradePrevention="+str(ordargs.SelfTradePrevention)
        ordresult=self._neworder(9,futoptorditem)
        if ordresult>=1:
            #print("委托单产生成功")
            return ordid,"委托成功"
        else:
            print(self.ordererr[str(ordresult)])
            return None,self.ordererr[str(ordresult)]
    def _neworder(self, SecurityType, NewOrderParameters):
        try:
            pythoncom.CoInitialize()
            disp = Git.GetInterfaceFromGlobal(self.cookie, pythoncom.IID_IDispatch)
            interp = client.Dispatch(disp)
            return interp.NewOrder2(SecurityType, NewOrderParameters)
        except pythoncom.com_error as e:
            print("neworder错误:",e) 

    def newstrategyorder(self,strategyorder:dict):
        try:
            pythoncom.CoInitialize()
            disp = Git.GetInterfaceFromGlobal(self.cookie, pythoncom.IID_IDispatch)
            interp = client.Dispatch(disp)
            strategyorder["UserKey3"]="8076c9867a372d2a9a814ae710c256e2|Python"
            strategyorder["ProcessID"]=os.getpid()
            args=str(strategyorder)
            return interp.NewStrategyOrder(args.replace("'","\""))
        except pythoncom.com_error as e:
            print("neworder错误:",e) 

    def replaceorder(self, reportid,orderqty,price,stopprice):
        try:
            pythoncom.CoInitialize()
            disp = Git.GetInterfaceFromGlobal(self.cookie, pythoncom.IID_IDispatch)
            interp = client.Dispatch(disp)
            ReplaceOrderParameters= client.Dispatch("{0F9B6537-B2A4-4888-A2CD-70914309773F}")
            ReplaceOrderParameters.ReportID=reportid
            if orderqty and not price and not stopprice:
                ReplaceOrderParameters.OrderQty= orderqty
                ReplaceOrderParameters.ReplaceExecType=1
            if not orderqty and (price or stopprice):
                ReplaceOrderParameters.ReplaceExecType=0
            if orderqty and (price or stopprice):
                ReplaceOrderParameters.OrderQty= orderqty
                ReplaceOrderParameters.ReplaceExecType=2
            if price:
                ReplaceOrderParameters.Price=int(price*10000000000)
            if stopprice:
                ReplaceOrderParameters.StopPrice=int(stopprice*10000000000)
            return interp.ReplaceOrder(ReplaceOrderParameters)
        except pythoncom.com_error as e:
            print("replaceorder错误:",e) 

    def setaccountsubscriptionlevel(self, Level):
        try:
            pythoncom.CoInitialize()
            disp = Git.GetInterfaceFromGlobal(self.cookie, pythoncom.IID_IDispatch)
            interp = client.Dispatch(disp)
            return interp.SetAccountSubscriptionLevel(Level)
        except pythoncom.com_error as e:
            print("CancelOrder错误:",e) 

    def topicpublish(self, strTopic, lParam, strParam, pvParam):
        try:
            pythoncom.CoInitialize()
            disp = Git.GetInterfaceFromGlobal(self.cookie, pythoncom.IID_IDispatch)
            interp = client.Dispatch(disp)
            return interp.TopicPublish(strTopic, lParam, strParam, pvParam)
        except pythoncom.com_error as e:
            print("gettradeingdays错误:",e)
    def topicsub(self, strTopic):
        try:
            pythoncom.CoInitialize()
            disp = Git.GetInterfaceFromGlobal(self.cookie, pythoncom.IID_IDispatch)
            interp = client.Dispatch(disp)
            return interp.TopicSub(strTopic)
        except pythoncom.com_error as e:
            print("gettradeingdays错误:",e)

    def topicunsub(self, strTopic):
        try:
            pythoncom.CoInitialize()
            disp = Git.GetInterfaceFromGlobal(self.cookie, pythoncom.IID_IDispatch)
            interp = client.Dispatch(disp)
            return interp.TopicUnsub(strTopic)
        except pythoncom.com_error as e:
            print("gettradeingdays错误:",e)

    def getgeneralservice(self, Key):
        try:
            pythoncom.CoInitialize()
            disp = Git.GetInterfaceFromGlobal(self.cookie, pythoncom.IID_IDispatch)
            interp = client.Dispatch(disp)
            return interp.GetGeneralService(Key)
        except pythoncom.com_error as e:
            print("gettradeingdays错误:",e)

    # def join(self):
    #     pythoncom.PumpMessages()

