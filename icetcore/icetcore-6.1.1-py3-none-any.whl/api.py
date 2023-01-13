from abc import abstractmethod
import sys
import win32event
import pythoncom
from icetcore.quote import QuoteClass,QuoteEventMeta
from icetcore.trade import TradeClass,TradeEventMeta
from icetcore.constant import BarType,GreeksType,OrderStruct
from datetime import datetime,timedelta
import time
from concurrent.futures import ThreadPoolExecutor
import psutil
import win32com
import json
class QuoteEvent(QuoteEventMeta):
    def __init__(self) -> None:
        super().__init__()
    @abstractmethod
    def onconnected(self,apitype:str):
        pass
    @abstractmethod
    def ondisconnected(self,apitype:str):
        pass
    @abstractmethod
    def onbar(self,datatype,interval,symbol,data:list,isreal:bool):
        pass
    def ongreeksreal(self,datatype,symbol,data:dict):
        pass
    def ongreeksline(self,datatype,interval,symbol,data,isreal):
        pass
    def onquote(self,data):
        pass
    def onATM(self,datatype,symbol,data:dict):
        pass
    def onservertime(self, serverdt):
        pass

class TradeEvent(TradeEventMeta):
    def __init__(self) -> None:
        super().__init__()
    @abstractmethod
    def onconnected(self, strapi):
        pass
    @abstractmethod
    def ondisconnected(self, strapi):
        pass
    def onaccountlist(self,data,count):
        pass
    def onordereportreal(self,data):
        pass
    def onfilledreportreal(self,data):
        pass
    def onorderreportreset(self):
        pass
    def onpositionmoniter(self,data):
        pass
class TCoreAPI():
    def __init__(self,eventclass=None) -> None:
        if eventclass:
            self.eventcls=eventclass()
        else:
            self.eventcls=None
        self.connpool=ThreadPoolExecutor(max_workers=5)
        self.tradeobj=None
        self.quoteobj=None
    #连线
    def connect(self,appid="",servicekey="8076c9867a372d2a9a814ae710c256e2"):#AlgoMaster2  8076c9867a372d2a9a814ae710c256e2
        if appid=="":
            path=""
            apppath=""
            pids=psutil.pids()
            for pid in pids:
                p=psutil.Process(pid)
                if "TCore" in p.name():
                    apppath=p.exe()
                    break
            if not apppath:
                wmi=win32com.client.GetObject('winmgmts:')
                for p in wmi.InstancesOf('win32_process'):
                    if "TCore" in p.Name:
                        apppath=p.Properties_('ExecutablePath').Value
                        break
            if not apppath:
                sys.exit("请先启动客户端，否则python接口无法正常使用！")
            ap=apppath.split("\\")
            path=ap[0]+"\\"+ap[1]+"\\"+ap[2]+"\\"+ap[3]+"\\ComShared\\SystemSettings.ini"
            with open(path,encoding="utf-8") as file:
                for line in file.readlines():
                    if "SystemName=" in line:
                        appid=line.replace("SystemName=","").strip()
                        break        
                
        tradere= self.connpool.submit(TradeClass, self.eventcls)
        quotere= self.connpool.submit(QuoteClass, self.eventcls)
        self.tradeobj=tradere.result()
        self.quoteobj=quotere.result()
        self.tradeobj.connect(appid,servicekey)
        self.quoteobj.connect(appid,servicekey)
        time.sleep(1)
        if self.eventcls:
            self.eventcls._tcoreapi=self
        tre=win32event.WaitForSingleObject(self.tradeobj.eventobj.cmsgevent, 1000)
        qre=win32event.WaitForSingleObject(self.quoteobj.eventobj.cmsgevent, 1000)
        if win32event.WAIT_OBJECT_0==tre and win32event.WAIT_OBJECT_0==qre:
            return 1
        else:
            sys.exit("连线失败")
            return -1
    #断开连线
    def disconnect(self):
        self.tradeobj.disconnect()
        self.quoteobj.disconnect()

    #下单
    def neworder(self,ordarg:OrderStruct):
        ordkey,msg=self.tradeobj.neworder(ordarg)
        return ordkey,msg
    #获取新增委托单最新信息和状态
    def getorderinfo(self,ordkey:str):
        return self.tradeobj.getorderinfo(ordkey)
    #改单
    def replaceorder(self,reportid:str,orderqty=None,price=None,stopprice=None):
        return self.tradeobj.replaceorder(reportid,orderqty,price,stopprice)
    #取消委托单
    def cancelorder(self, reportid:str,strkey=""):
        return self.tradeobj.cancelorder(self, reportid,strkey)
    #取消价差单
    def cancelspreadorder(self,  reportid:str):
        return self.tradeobj.cancelspreadorder(self, reportid)
    #修改委托单状态
    def changeorderaction(self,  reportid:str, laction):
        return self.tradeobj.changeorderaction( reportid, laction)
    #新增Vanna策略委托
    def newstrategyorder(self,newstrategyorder:dict):
        return self.tradeobj.newstrategyorder(newstrategyorder)
    #期权持仓组合
    def optcomb(self,strAcctMask,SymbolA,SymbolB,Volume:int,CombinationType:int,CombID=""):#strParam &SIDEA=2&SIDEB=2
        return self.tradeobj.optcomb(strAcctMask,SymbolA,SymbolB,Volume,CombinationType,CombID)
    #期权组合持仓拆分
    def optcombsplit(self,strAcctMask,Symbol:str,Volume:int,CombinationType:int,CombID=""):#strParam &SIDEA=2&SIDEB=2
        return self.tradeobj.optcombsplit(strAcctMask,Symbol,Volume,CombinationType,CombID)
    #获取已登入账户列表
    def getaccountlist(self):
        temp=[]
        for i in range(self.tradeobj.eventobj.accountcout):
            temp.append(self.tradeobj.getaccoutlist(i))
        return temp
    #获取指定账户的资金信息
    def getaccmargin(self,accmask:str):
        return self.tradeobj.getaccmargin(accmask)
    #获取指定子账户的持仓信息
    def getposition(self,accmask:str):
        temp=[]
        if accmask in self.tradeobj.eventobj.positioncout:
            for i in range(self.tradeobj.eventobj.positioncout[accmask]):
                temp.append(self.tradeobj.getposition(i,accmask))
        return temp
    #获取指定账户的组合持仓
    def getcombposition(self,accmask:str):
        temp=[]
        if accmask in self.tradeobj.eventobj.combpositioncout:
            for i in range(self.tradeobj.eventobj.combpositioncout[accmask]):
                combp=self.tradeobj.getcombposition(i,accmask)
                if combp:
                    temp.append(combp)
        return temp
    #获取指定账户的组合报单记录
    def getcombinationorder(self,accmask:str):
        temp=[]
        if accmask in self.tradeobj.eventobj.combordercout:
            for i in range(self.tradeobj.eventobj.combordercout[accmask]):
                self.tradeobj.getcombinationorder(i,accmask)
        return temp

    #获取当前未成交委托
    def getactiveorder(self):
        return self.tradeobj.getactiveorder()
    #获取当日所有委托单
    def getorderreport(self):
        return self.tradeobj.getorderreport()
    #获取当日所有成交委托
    def getfilledreport(self):
        return self.tradeobj.getfilledreport()
    #获取当日所有成交委托明细
    def getdetailfilledreport(self):
        return self.tradeobj.getdetailfilledreport()
    #根据内部报单编号获取对应的委托单信息
    def getreportbyid(self,reportid:str):
        return self.tradeobj.getreportbyid(reportid)
    #订阅动态K线数据
    def subbar(self,btype:BarType,interval:int,symbol:str,starttime:str,endtime=datetime.strftime(datetime.now()-timedelta(hours=7),'%Y%m%d%H')):
        try:
            datetime.strptime(starttime,'%Y%m%d%H')
            datetime.strptime(endtime,'%Y%m%d%H')
        except:
            print("日期时间格式错误，请输入格式为‘yyyyMMddHH’")
        self.quoteobj.eventobj.bardata[symbol+"-"+str(btype)+"-"+str(interval)]=[]
        #if symbol+"-"+str(btype) not in self.quoteobj.eventobj.barinterval.keys():
        self.quoteobj.subquote(1,symbol,0,0)
        re=self.quoteobj.subquote(btype,symbol,int(starttime),int(endtime))
        if symbol+"-"+str(btype) in self.quoteobj.eventobj.barinterval.keys():
            self.quoteobj.eventobj.barinterval[symbol+"-"+str(btype)].append(interval)
        else:
            self.quoteobj.eventobj.barinterval[symbol+"-"+str(btype)]=[interval]
        return re

    #解订K线数据
    def unsubbar(self,btype:BarType,symbol:str):
        del self.quoteobj.eventobj.bardata[symbol+"-"+str(btype)]
        self.quoteobj.unsubquote(1,symbol,0,0)
    #订阅实时行情
    def subquote(self,symbol:str):
        return self.quoteobj.subquote(1,symbol,0,0)
    #解订实时行情
    def unsubquote(self,symbol:str):
        return self.quoteobj.unsubquote(1,symbol,0,0)
    #获取历史行情数据    
    def getquotehistory(self,btype:BarType,interval:int,symbol:str,starttime:str,endtime=datetime.strftime(datetime.now()-timedelta(hours=7),'%Y%m%d%H')):
        try:
            datetime.strptime(starttime,'%Y%m%d%H')
            datetime.strptime(endtime,'%Y%m%d%H')
        except:
            print("日期时间格式错误，请输入格式为‘yyyyMMddHH’")
        if symbol+"-"+str(btype) in self.quoteobj.eventobj.barinterval.keys():
            self.quoteobj.eventobj.barinterval[symbol+"-"+str(btype)].append(interval)
        else:
            self.quoteobj.eventobj.barinterval[symbol+"-"+str(btype)]=[interval]
        self.quoteobj.eventobj.quotehistory[symbol+"-"+str(btype)+str(interval)+":"+starttime+"~"+str(endtime)]=[]
        self.quoteobj.subquote(btype,symbol,int(starttime),int(endtime))
        qre=win32event.WaitForSingleObject(self.quoteobj.eventobj.quotehistoryevent, 50000)
        quotehistory=self.quoteobj.eventobj.quotehistory[symbol+"-"+str(btype)+str(interval)+":"+starttime+"~"+str(endtime)]
        self.quoteobj.eventobj.barinterval[symbol+"-"+str(btype)].remove(interval)
        del self.quoteobj.eventobj.quotehistory[symbol+"-"+str(btype)+str(interval)+":"+starttime+"~"+str(endtime)]
        if win32event.WAIT_OBJECT_0==qre and quotehistory:
            return quotehistory
        else:
            return

    #订阅动态greekline数据
    def subgreeksline(self,linetype:GreeksType,interval:int,symbol:str,starttime:str,endtime=datetime.strftime(datetime.now()-timedelta(hours=7),'%Y%m%d%H')):
        try:
            datetime.strptime(starttime,'%Y%m%d%H')
        except:
            print("日期时间格式错误，请输入格式为‘yyyyMMddHH’")
        endtime=datetime.strftime(datetime.now()-timedelta(hours=7),'%Y%m%d%H')
        
        self.quoteobj.eventobj.linedata[symbol+"-"+str(linetype)+"-"+str(interval)]=[]
        #if symbol+"-"+str(btype) not in self.quoteobj.eventobj.barinterval.keys():
        if "TC.O" in symbol:
            arrsymb=symbol.split(".")
            if "SSE" in symbol or "SZSE" in symbol:
                usymbol="TC.S."+arrsymb[2]+"."+arrsymb[3]
                ufsymbol="TC.F.U_"+arrsymb[2]+"."+arrsymb[3]+"."+arrsymb[4] 
            else:
                usymbol="TC.F."+arrsymb[2]+"."+arrsymb[3]+"."+arrsymb[4]
                ufsymbol="TC.F.U_"+arrsymb[2]+"."+arrsymb[3]+"."+arrsymb[4]
            re1=self.quoteobj.subquote(1,usymbol,0,0)
            re2=self.quoteobj.subquote(1,ufsymbol,0,0)
        self.quoteobj.subquote(1,symbol,0,0)
        self.quoteobj.subquote(6,symbol,0,0)
        re=self.quoteobj.subquote(linetype,symbol,int(starttime),int(endtime))
        if symbol+"-"+str(linetype) in self.quoteobj.eventobj.lineinterval.keys():
            self.quoteobj.eventobj.lineinterval[symbol+"-"+str(linetype)].append(interval)
        else:
            self.quoteobj.eventobj.lineinterval[symbol+"-"+str(linetype)]=[interval]
        return re
    #订阅实时greek
    def subgreeksreal(self,symbol:str):
        return self.quoteobj.subquote(6,symbol,0,0)
    #解订实时greek
    def unsubgreeksreal(self,symbol:str):
        return self.quoteobj.unsubquote(6,symbol,0,0)
    #获取历史greeks数据
    def getgreekshistory(self,datatype:GreeksType,interval:int,symbol:str,starttime:str,endtime=datetime.strftime(datetime.now()-timedelta(hours=7),'%Y%m%d%H')):
        try:
            datetime.strptime(starttime,'%Y%m%d%H')
            datetime.strptime(endtime,'%Y%m%d%H')
        except:
            print("日期时间格式错误，请输入格式为‘yyyyMMddHH’")
        if symbol+"-"+str(datatype) in self.quoteobj.eventobj.lineinterval.keys():
            self.quoteobj.eventobj.lineinterval[symbol+"-"+str(datatype)].append(interval)
        else:
            self.quoteobj.eventobj.lineinterval[symbol+"-"+str(datatype)]=[interval]
        self.quoteobj.eventobj.greekshistory[symbol+"-"+str(datatype)+str(interval)+":"+str(starttime)+"~"+str(endtime)]=[]
        self.quoteobj.subquote(datatype,symbol,int(starttime),int(endtime))
        qre=win32event.WaitForSingleObject(self.quoteobj.eventobj.greekshistoryevent, 20000)

        greekshistory=self.quoteobj.eventobj.greekshistory[symbol+"-"+str(datatype)+str(interval)+":"+str(starttime)+"~"+str(endtime)]
        del self.quoteobj.eventobj.greekshistory[symbol+"-"+str(datatype)+str(interval)+":"+str(starttime)+"~"+str(endtime)]
        if win32event.WAIT_OBJECT_0==qre and greekshistory:
            return greekshistory
        else:
            return None
    #订阅ATM合约
    def subATM(self,symbol:str):
        #TC.O.SSE.510050.202211.GET.ATM
        if "TC.O" in symbol:
            _symbl=symbol.split(".")
            self.quoteobj.subquote(1,"TC.O."+_symbl[2]+"."+ _symbl[3]+"."+ _symbl[4]+".GET.ATM",0,0)
        else:
            print("合约代码格式错误:必须是TC.O.交易所.合约.月份，例如：TC.O.SSE.510050.202211")

    #解订ATM合约
    def unsubATM(self,symbol:str):
        if "TC.O" in symbol:
            _symbl=symbol.split(".")
            self.quoteobj.unsubquote(1,"TC.O."+_symbl[2]+"."+ _symbl[3]+"."+ _symbl[4]+".GET.ATM",0,0)
        else:
            print("合约代码格式错误，‘TC.O.’开头的期权合约可用")
    #获取ATM
        # -2:实值两档期权合约
        # -1:实值一档期权合约
        #  0:平值期权合约
        #  1:虚值期权合约        
    def getATM(self,symbol:str,atmindex:int):
        if "TC.O" in symbol:
            _symbl=symbol.split(".")
        else:
            print("合约代码格式错误:必须是TC.O.交易所.合约.月份，例如：TC.O.SSE.510050.202211")
        atmsymbol="TC.O."+_symbl[2]+"."+ _symbl[3]+"."+ _symbl[4]+".GET.ATM"
        self.quoteobj.eventobj.atm[atmsymbol]=None
        self.quoteobj.subquote(1,atmsymbol,0,0)
        qre=win32event.WaitForSingleObject(self.quoteobj.eventobj.atmevent, 2000)
        atmdata=self.quoteobj.eventobj.atm[atmsymbol]
        if win32event.WAIT_OBJECT_0==qre and atmdata:
            del self.quoteobj.eventobj.atm[atmsymbol]
            self.quoteobj.unsubquote(1,atmsymbol,0,0)
            result=None
            atmsymbol=None
            _callsymbol=atmdata["OPTLIST"]
            _putsymbol=[i.replace(".C.",".P.") for i in atmdata["OPTLIST"]]

            cidx=_callsymbol.index(atmdata["OTM-1C"])
            pidx=_putsymbol.index(atmdata["OTM-1P"])
            if atmindex==0:
                atmsymbol=atmdata["OTM-1C"] if atmdata["ATM"] in atmdata["OTM-1C"] else ["OTM-1P"]
                if ".P" in symbol and ".P" not in atmsymbol:
                    result=atmsymbol.replace(".C.",".P.")
            else:
                if ".P" in symbol:
                    result=_putsymbol[pidx-atmindex+1]
                else:
                    result=_callsymbol[cidx+atmindex-1]
            
            return result
        else:
            del self.quoteobj.eventobj.atm[atmsymbol]
            self.quoteobj.unsubquote(1,atmsymbol,0,0)
            return
       
    #获取合约的到期日
    def getexpirationdate(self, symbol:str):
        return self.quoteobj.getexpirationdate(symbol)
    #获取合约的剩余交易日
    def gettradeingdays(self,symbol:str):
        return self.quoteobj.gettradeingdays(symbol)
    #获取热门月换月信息
    def gethotmonth(self, symbol:str, strdate="", strtime=""):
        if self.quoteobj.eventobj.hotmonthready:
            return self.quoteobj.gethotmonth(symbol, strdate, strtime)
    #获取合约最小跳动
    def getsymbol_ticksize(self,symbol:str):
        if self.quoteobj.eventobj.symbinfoready:
            return self.quoteobj.getsymbol_ticksize(symbol)
    #获取合约交易时段
    def getsymbol_session(self,symbol:str):
        if self.quoteobj.eventobj.symbinfoready:
            return self.quoteobj.getsymbol_session(symbol)
    #获取合约乘数
    def getsymbolvolume_multiple(self,symbol:str):
        if self.quoteobj.eventobj.symbinfoready:
            return self.quoteobj.getsymbolvolume_multiple(symbol)
    #获取合约的交易编码
    def getsymbol_id(self,symbol:str):
        return self.quoteobj.getsymbol_id(symbol)
    #获取合约所有信息
    def getsymbol_allinfo(self,symbol:str):
        if self.quoteobj.eventobj.symbinfoready:
            return json.loads(self.quoteobj.getsymbol_allinfo(symbol))
    #获取合约名称描述
    def getsymbolname(self,symbol:str):
        return self.quoteobj.getsymbolname(symbol)
    #获取当前最新所有合约，只包含合约，不包含合约信息
    ##当symboltype和exchange均不带入参数默认为空时，获取所有合约
    ##symboltype 指定合约类型:OPT/FUT/STK
    ##exchange   指定交易所
    def getallsymbol(self,symboltype="",exchange=""):
        if self.quoteobj.eventobj.symbollistready:
            return self.quoteobj.getallsymbol(symboltype,exchange)
    #获取合成期货合约列表
    def get_u_futuresymbol(self):
        if self.quoteobj.eventobj.symbollistready:
            return self.quoteobj.getsynu_futuresymbol()
    #获取历史合约和信息
    def getsymbolhistory(self,symboltype:str,dt:str):
        self.quoteobj.eventobj.symbolhistory[symboltype+"-"+dt]=None
        self.quoteobj.subsymbolhistory(symboltype,dt)
        qre=win32event.WaitForSingleObject(self.quoteobj.eventobj.symbolhistoryevent, 2000)
        symbolhistory=self.quoteobj.eventobj.symbolhistory[symboltype+"-"+dt]
        del self.quoteobj.eventobj.symbolhistory[symboltype+"-"+dt]
        if win32event.WAIT_OBJECT_0==qre:
            return symbolhistory
        else:
            return
    #模糊查找合约
    def symbollookup(self, findkey:str,symboltype=""):
        if self.quoteobj.eventobj.symblookready:
            symtype=0
            if symboltype=="":
                symtype=0
            elif symboltype=="STK":
                symtype=1
            elif symboltype=="FUT":
                symtype=2
            elif symboltype=="OPT":
                symtype=3
            strre=self.quoteobj.symbollookup(symtype, findkey)
            if strre:
                if "|" in strre:
                    return [{symb.split(",")[0]:symb.split(",")[1]} for symb in strre.split("|")]
                elif "|" not in strre and "," in strre:
                    return [{strre.split(",")[0]:strre.split(",")[1]}]
            else:
                return None

    #指定时间，对应合约是否为假日
    def isholiday(self, bstrDate, symbol:str):
        return self.quoteobj.isholiday(bstrDate,symbol)
    #指定合约是否为标的合约
    def isunderlying(self, symbol:str):
        return self.quoteobj.isunderlying(symbol)

    def join(self):
        pythoncom.PumpMessages()  
        #self.tradeobj.join()
