#from win32com.client import DispatchBaseClass
import json
from icetcore.constant import BarType
from datetime import datetime,timedelta
from win32com import client
import pythoncom
import os
from abc import ABCMeta,abstractmethod
import win32event
import pytz

Git=pythoncom.CoCreateInstance(
        pythoncom.CLSID_StdGlobalInterfaceTable,
        None,
        pythoncom.CLSCTX_INPROC,
        pythoncom.IID_IGlobalInterfaceTable,
    )
def iff(itemvalue,tcsize=1):
    if itemvalue!=-9223372036854775808:
        return itemvalue/tcsize
    else:
        return None


class QuoteEventMeta(metaclass=ABCMeta):
    def __init__(self) -> None:
        self._tcoreapi=None
    @abstractmethod
    def onconnected(self,apitype:str):
        pass
    @abstractmethod
    def ondisconnected(self,apitype:str):
        pass
    @abstractmethod
    def onATM(self,datatype,symbol,data:dict):
        pass
    @abstractmethod
    def ongreeksline(datatype,interval,symbol,data,isreal):
        pass
    @abstractmethod
    def ongreeksreal(self,datatype,symbol,data:dict):
        pass
    @abstractmethod
    def onquote(self,data):
        pass
    @abstractmethod
    def onbar(self,datatype,interval,symbol,data:list,isreal:bool):
        pass
    @abstractmethod
    def onservertime(self, serverdt):
        pass

class BaseEvents():
    def __init__(self):
        self.tz = pytz.timezone('Etc/GMT+8')
        self.quoteapi=None
        self.extendevent=None
        #self.connstatue=0

        self.barinterval={}
        self.bardata={}
        self.lineinterval={}
        self.linedata={}
        self.linetemp={}
        self.underlyingprice={}

        self.temp={}
        self.voltemp=0
        self.cmsgevent=win32event.CreateEvent(None, 0, 0, None)
        self.symbolhistoryevent=win32event.CreateEvent(None, 0, 0, None)
        self.symbolhistory={}
        self.quotehistoryevent=win32event.CreateEvent(None, 0, 0, None)
        self.quotehistory={}
        self.greekshistoryevent=win32event.CreateEvent(None, 0, 0, None)
        self.greekshistory={}
        self.atmevent=win32event.CreateEvent(None, 0, 0, None)
        self.atm={}
        self.symbollistready=False
        self.hotmonthready=False
        self.symblookready=False
        self.symbinfoready=False

    #@abstractmethod
    def onconnected(self,strapi):
        if self.extendevent:
            self.extendevent.onconnected(strapi)
    #@abstractmethod
    def ondisconnected(self,strapi):
        if self.extendevent:
            self.extendevent.ondisconnected(strapi)
    #@abstractmethod
    def onquote(self,data):
        if self.extendevent:
            self.extendevent.onquote(data)
    #@abstractmethod
    def onbar(self,datatype,interval,symbol,data:list,isreal:bool):
        if self.extendevent:
            self.extendevent.onbar(datatype,interval,symbol,data,isreal)
    #@abstractmethod
    def onATM(self,datatype,symbol,data:dict):
        if self.extendevent:
            self.extendevent.onATM(datatype,symbol,data)
        self.atm[symbol]=data
        win32event.SetEvent(self.atmevent)
    #@abstractmethod
    def ongreeksline(self,datatype,interval,symbol,data:list,isreal:bool):
        if self.extendevent:
            self.extendevent.ongreeksline(datatype,interval,symbol,data,isreal)

    #@abstractmethod
    def onsymbolhistory(self,symboltype,symboldate,sym):
        self.symbolhistory[symboltype+"-"+str(symboldate)]=sym
        win32event.SetEvent(self.symbolhistoryevent)
        #self.extendevent.onsymbolhistory(symboltype,symboldate,sym)
    #@abstractmethod
    def ontimediff(self, TimeDiff):
        if self.extendevent:
            self.extendevent.onservertime(datetime.now().replace(tzinfo=self.tz)+timedelta(seconds=TimeDiff))


    def OnCommandMsg(self, MsgType, MsgCode, MsgString):
        #print(" OnCommandMsgQuote",MsgType, MsgCode, MsgString)
        if int(MsgType)==2 and int(MsgCode)==1:
            win32event.SetEvent(self.cmsgevent)
            self.onconnected("quote")
        if int(MsgType)==1 and int(MsgCode)==1:
            self.ondisconnected("quote")

    def dtfilter(self,symbol,dt):
        sess=[i.split("~")  for i in self.quoteapi.getsymbol_session(symbol).split(";")]
        for i in sess:
            sessopen = datetime.strptime(str(dt.date()) + i[0], '%Y-%m-%d%H:%M').replace(tzinfo=self.tz)+timedelta(hours=8)
            sessclose = datetime.strptime(str(dt.date()) + i[1], '%Y-%m-%d%H:%M').replace(tzinfo=self.tz)+timedelta(hours=8)
            # dt=datetime.strptime(str(dt.date()) + str(dt.hour)+":"+str(dt.minute) ,'%Y-%m-%d%H:%M').replace(tzinfo=self.tz)
            if "SSE" in symbol or "SZSE" in symbol:
                if (sessopen-timedelta(minutes=15))<=dt <sessopen:
                    return datetime.strptime(str(dt.date()) + i[0]+":00", '%Y-%m-%d%H:%M:%S').replace(tzinfo=self.tz)+timedelta(hours=8)
                if sessclose<=dt <(sessclose+timedelta(minutes=1)):
                    return datetime.strptime(str(dt.date()) + i[1]+":59", '%Y-%m-%d%H:%M:%S').replace(tzinfo=self.tz)+timedelta(hours=8)-timedelta(minutes=1)
            else:
                if (sessopen-timedelta(minutes=1))<=dt <sessopen:
                    return datetime.strptime(str(dt.date()) + i[0]+":00", '%Y-%m-%d%H:%M:%S').replace(tzinfo=self.tz)+timedelta(hours=8)
                if sessclose<=dt <(sessclose+timedelta(minutes=1)):
                    return datetime.strptime(str(dt.date()) + i[1]+":59", '%Y-%m-%d%H:%M:%S').replace(tzinfo=self.tz)+timedelta(hours=8)-timedelta(minutes=1)
        return dt

    def isduringdt(self,symbol,dt):
        sess=[i.split("~")  for i in self.quoteapi.getsymbol_session(symbol).split(";")]
        for i in sess:
            start_time = datetime.strptime(str(dt.date()) + i[0], '%Y-%m-%d%H:%M').replace(tzinfo=self.tz)+timedelta(hours=8)
            end_time = datetime.strptime(str(dt.date()) + i[1], '%Y-%m-%d%H:%M').replace(tzinfo=self.tz)+timedelta(hours=8)
            dt=datetime.strptime(str(dt.date()) + str(dt.hour)+":"+str(dt.minute) ,'%Y-%m-%d%H:%M').replace(tzinfo=self.tz)
            if start_time <= dt <= end_time:
                return True,start_time
        return False,None

    def onbarupdate(self,datatype,interval,symbol,data:list,isreal:bool):
        if isreal:
            bararr=[i for i in self.bardata.keys() if symbol in i]
            isbarcout=0
            for barkey in bararr:
                if self.bardata[barkey]:
                    isbarcout=isbarcout+1
            if isbarcout==len(bararr):
                for barkey in bararr:
                    bar=self.bardata[barkey]
                    bartypeinte=barkey.split("-")
                    bartype=int(bartypeinte[1])
                    interval=int(bartypeinte[2])
                    if symbol in self.temp.keys():
                        if self.temp[symbol] :
                            for te in self.temp[symbol]:
                                if bartype==BarType.DK:
                                    if te["DateTime"].date()<=bar[-1]['DateTime'].date():
                                        if te["Close"]>bar[-1]['Close']:
                                            bar[-1]["UpTick"]=bar[-1]['UpTick']+1
                                            bar[-1]["UpVolume"]=bar[-1]['UpVolume']+te["Quantity"]
                                        else:
                                            bar[-1]["DownTick"]=bar[-1]['DownTick']+1
                                            bar[-1]["DownVolume"]=bar[-1]['DownVolume']+te["Quantity"]
                                        if te["High"]>bar[-1]['High']:
                                            bar[-1]["High"]=te["High"]
                                        if te["Low"]<bar[-1]['Low']:
                                            bar[-1]['Low']=te["Low"]
                                        bar[-1]["Close"]=te["Close"]
                                        bar[-1]["Volume"]=te["Volume"]
                                        bar[-1]["OpenInterest"]=te["OpenInterest"]
                                    else:
                                        ktemp={}
                                        # if bartype==4:
                                        #     ktemp["DateTime"]=datetime.strptime(str(te["DateTime"].date())+str(te["DateTime"].hour)+":"+str(te["DateTime"].minute)+":00",'%Y-%m-%d%H:%M:%S').replace(tzinfo=self.tz)+timedelta(minutes=interval-1)
                                        # if bartype==5:
                                        ktemp["DateTime"]=datetime.strptime(str(te["DateTime"].date())+str(te["DateTime"].hour)+":"+str(te["DateTime"].minute)+":00",'%Y-%m-%d%H:%M:%S').replace(tzinfo=self.tz)+timedelta(days=interval-1)
                                        ktemp["Symbol"]=symbol
                                        ktemp["Open"]=te['Open']
                                        ktemp["High"]=te["High"]
                                        ktemp["Low"]=te["Low"]
                                        ktemp["Close"]=te["Close"]
                                        ktemp["Volume"]=te["Volume"]
                                        ktemp["OpenInterest"]=te["OpenInterest"]
                                        if te["Close"]>bar[-1]['Close']:
                                            ktemp["DownTick"]=0
                                            ktemp["DownVolume"]=0
                                            ktemp["UnchVolume"]=0
                                            ktemp["UpTick"]=1
                                            ktemp["UpVolume"]=te["Quantity"]
                                        else:
                                            ktemp["DownTick"]=1
                                            ktemp["DownVolume"]=te["Quantity"]
                                            ktemp["UnchVolume"]=0
                                            ktemp["UpTick"]=0
                                            ktemp["UpVolume"]=0
                                        bar.append(ktemp)
                                elif bartype==BarType.MINUTE:
                                    if te["DateTime"]<=bar[-1]['DateTime']:
                                        if te["Close"]>bar[-1]['Close']:
                                            bar[-1]["UpTick"]=bar[-1]['UpTick']+1
                                            bar[-1]["UpVolume"]=bar[-1]['UpVolume']+te["Quantity"]
                                        else:
                                            bar[-1]["DownTick"]=bar[-1]['DownTick']+1
                                            bar[-1]["DownVolume"]=bar[-1]['DownVolume']+te["Quantity"]
                                        if te["Close"]>bar[-1]['High']:
                                            bar[-1]["High"]=te["Close"]
                                        if te["Close"]<bar[-1]['Low']:
                                            bar[-1]["Low"]=te["Close"]
                                        bar[-1]["Close"]=te["Close"]
                                        bar[-1]["Volume"]=bar[-1]["Volume"]+te["Quantity"]
                                        bar[-1]["OpenInterest"]=te["OpenInterest"]
                                    else:
                                        ktemp={}
                                        # if bartype==4:
                                        ktemp["DateTime"]=datetime.strptime(str(te["DateTime"].date())+str(te["DateTime"].hour)+":"+str(te["DateTime"].minute)+":00",'%Y-%m-%d%H:%M:%S').replace(tzinfo=self.tz)+timedelta(minutes=interval-1)
                                        # if bartype==5:
                                        #     ktemp["DateTime"]=datetime.strptime(str(te["DateTime"].date())+str(te["DateTime"].hour)+":"+str(te["DateTime"].minute)+":00",'%Y-%m-%d%H:%M:%S').replace(tzinfo=self.tz)+timedelta(days=interval-1)
                                        ktemp["Symbol"]=symbol
                                        ktemp["Open"]=te["Close"]
                                        ktemp["High"]=te["Close"]
                                        ktemp["Low"]=te["Close"]
                                        ktemp["Close"]=te["Close"]
                                        ktemp["Volume"]=te["Quantity"]
                                        ktemp["OpenInterest"]=te["OpenInterest"]
                                        if te["Close"]>bar[-1]['Close']:
                                            ktemp["DownTick"]=0
                                            ktemp["DownVolume"]=0
                                            ktemp["UnchVolume"]=0
                                            ktemp["UpTick"]=1
                                            ktemp["UpVolume"]=te["Quantity"]
                                        else:
                                            ktemp["DownTick"]=1
                                            ktemp["DownVolume"]=te["Quantity"]
                                            ktemp["UnchVolume"]=0
                                            ktemp["UpTick"]=0
                                            ktemp["UpVolume"]=0
                                        bar.append(ktemp)
                                elif bartype==BarType.TICK:
                                    if interval==1:
                                        if te["DateTime"]>=bar[-1]["DateTime"] and te["Volume"]>bar[-1]['Volume']:
                                            bar.append({"DateTime":te["DateTime"],
                                            "Symbol":symbol,
                                            "Ask":te["Ask"],
                                            "Bid":te["Bid"],
                                            "Last":te["Close"],
                                            "Quantity":te["Quantity"],
                                            "Volume":te["Volume"],
                                            "OpenInterest":te["OpenInterest"]})
                                    else:
                                        if te["DateTime"]<=bar[-1]['DateTime']:
                                            if te["Close"]>bar[-1]['Close']:
                                                bar[-1]["UpTick"]=bar[-1]['UpTick']+1
                                                bar[-1]["UpVolume"]=bar[-1]['UpVolume']+te["Quantity"]
                                            else:
                                                bar[-1]["DownTick"]=bar[-1]['DownTick']+1
                                                bar[-1]["DownVolume"]=bar[-1]['DownVolume']+te["Quantity"]
                                            if te["Close"]>bar[-1]['High']:
                                                bar[-1]["High"]=te["Close"]
                                            if te["Close"]<bar[-1]['Low']:
                                                bar[-1]["Low"]=te["Close"]
                                            bar[-1]["Close"]=te["Close"]
                                            bar[-1]["Volume"]=bar[-1]["Volume"]+te["Quantity"]
                                            bar[-1]["OpenInterest"]=te["OpenInterest"]
                                        else:
                                            ktemp={}
                                            ktemp["DateTime"]=te["DateTime"]+timedelta(seconds=interval-1)
                                            if ktemp["DateTime"].second%5!=0:
                                                print(ktemp["DateTime"])
                                            ktemp["Symbol"]=symbol
                                            ktemp["Open"]=te["Close"]
                                            ktemp["High"]=te["Close"]
                                            ktemp["Low"]=te["Close"]
                                            ktemp["Close"]=te["Close"]
                                            ktemp["Volume"]=te["Quantity"]
                                            ktemp["OpenInterest"]=te["OpenInterest"]
                                            if te["Close"]>bar[-1]['Close']:
                                                ktemp["DownTick"]=0
                                                ktemp["DownVolume"]=0
                                                ktemp["UnchVolume"]=0
                                                ktemp["UpTick"]=1
                                                ktemp["UpVolume"]=te["Quantity"]
                                            else:
                                                ktemp["DownTick"]=1
                                                ktemp["DownVolume"]=te["Quantity"]
                                                ktemp["UnchVolume"]=0
                                                ktemp["UpTick"]=0
                                                ktemp["UpVolume"]=0
                                            bar.append(ktemp)
                            self.onbar(bartype,interval,symbol,bar,False)
                            del self.temp[symbol]
                    else:
                        te=data[0]
                        if bartype==BarType.DK:
                            if te["DateTime"].date()<=bar[-1]['DateTime'].date():
                                if te["Close"]>bar[-1]['Close']:
                                    bar[-1]["UpTick"]=bar[-1]['UpTick']+1
                                    bar[-1]["UpVolume"]=bar[-1]['UpVolume']+te["Quantity"]
                                else:
                                    bar[-1]["DownTick"]=bar[-1]['DownTick']+1
                                    bar[-1]["DownVolume"]=bar[-1]['DownVolume']+te["Quantity"]
                                if te["High"]>bar[-1]['High']:
                                    bar[-1]["High"]=te["High"]
                                if te["Low"]<bar[-1]['Low']:
                                    bar[-1]['Low']=te["Low"]
                                bar[-1]["Close"]=te["Close"]
                                bar[-1]["Volume"]= bar[-1]["Volume"]+te["Quantity"]
                                bar[-1]["OpenInterest"]=te["OpenInterest"]
                            else:
                                ktemp={}
                                if bartype==4:
                                    ktemp["DateTime"]=datetime.strptime(str(te["DateTime"].date())+str(te["DateTime"].hour)+":"+str(te["DateTime"].minute)+":00",'%Y-%m-%d%H:%M:%S').replace(tzinfo=self.tz)+timedelta(minutes=interval)
                                if bartype==5:
                                    ktemp["DateTime"]=datetime.strptime(str(te["DateTime"].date())+str(te["DateTime"].hour)+":"+str(te["DateTime"].minute)+":00",'%Y-%m-%d%H:%M:%S').replace(tzinfo=self.tz)+timedelta(days=interval)
                                ktemp["Symbol"]=symbol
                                ktemp["Open"]=te['Open']
                                ktemp["High"]=te["High"]
                                ktemp["Low"]=te["Low"]
                                ktemp["Close"]=te["Close"]
                                ktemp["Volume"]=te["Volume"]
                                ktemp["OpenInterest"]=te["OpenInterest"]
                                if te["Close"]>bar[-1]['Close']:
                                    ktemp["DownTick"]=0
                                    ktemp["DownVolume"]=0
                                    ktemp["UnchVolume"]=0
                                    ktemp["UpTick"]=1
                                    ktemp["UpVolume"]=te["Quantity"]
                                else:
                                    ktemp["DownTick"]=1
                                    ktemp["DownVolume"]=te["Quantity"]
                                    ktemp["UnchVolume"]=0
                                    ktemp["UpTick"]=0
                                    ktemp["UpVolume"]=0
                                bar.append(ktemp)
                        elif bartype==BarType.MINUTE:
                            if te["DateTime"]<=bar[-1]['DateTime']:
                                if te["Close"]>bar[-1]['Close']:
                                    bar[-1]["UpTick"]=bar[-1]['UpTick']+1
                                    bar[-1]["UpVolume"]=bar[-1]['UpVolume']+te["Quantity"]
                                else:
                                    bar[-1]["DownTick"]=bar[-1]['DownTick']+1
                                    bar[-1]["DownVolume"]=bar[-1]['DownVolume']+te["Quantity"]
                                if te["Close"]>bar[-1]['High']:
                                    bar[-1]["High"]=te["Close"]
                                if te["Close"]<bar[-1]['Low']:
                                    bar[-1]["Low"]=te["Close"]
                                bar[-1]["Close"]=te["Close"]
                                bar[-1]["Volume"]=bar[-1]["Volume"]+te["Quantity"]
                                bar[-1]["OpenInterest"]=te["OpenInterest"]
                            else:
                                ktemp={}
                                if bartype==4:
                                    ktemp["DateTime"]=datetime.strptime(str(te["DateTime"].date())+str(te["DateTime"].hour)+":"+str(te["DateTime"].minute)+":00",'%Y-%m-%d%H:%M:%S').replace(tzinfo=self.tz)+timedelta(minutes=interval)
                                if bartype==5:
                                    ktemp["DateTime"]=datetime.strptime(str(te["DateTime"].date())+str(te["DateTime"].hour)+":"+str(te["DateTime"].minute)+":00",'%Y-%m-%d%H:%M:%S').replace(tzinfo=self.tz)+timedelta(days=interval)
                                ktemp["Symbol"]=symbol
                                ktemp["Open"]=te["Close"]
                                ktemp["High"]=te["Close"]
                                ktemp["Low"]=te["Close"]
                                ktemp["Close"]=te["Close"]
                                ktemp["Volume"]=te["Quantity"]
                                ktemp["OpenInterest"]=te["OpenInterest"]
                                if te["Close"]>bar[-1]['Close']:
                                    ktemp["DownTick"]=0
                                    ktemp["DownVolume"]=0
                                    ktemp["UnchVolume"]=0
                                    ktemp["UpTick"]=1
                                    ktemp["UpVolume"]=te["Quantity"]
                                else:
                                    ktemp["DownTick"]=1
                                    ktemp["DownVolume"]=te["Quantity"]
                                    ktemp["UnchVolume"]=0
                                    ktemp["UpTick"]=0
                                    ktemp["UpVolume"]=0
                                bar.append(ktemp)
                        elif bartype==BarType.TICK:
                            if interval==1:
                                if te["DateTime"]>=bar[-1]["DateTime"] and te["Volume"]>bar[-1]['Volume']:
                                        bar.append({"DateTime":te["DateTime"],
                                        "Symbol":symbol,
                                        "Ask":te["Ask"],
                                        "Bid":te["Bid"],
                                        "Last":te["Close"],
                                        "Quantity":te["Quantity"],
                                        "Volume":te["Volume"],
                                        "OpenInterest":te["OpenInterest"]})
                            else:
                                if te["DateTime"]<=bar[-1]['DateTime']:
                                    if te["Close"]>bar[-1]['Close']:
                                        bar[-1]["UpTick"]=bar[-1]['UpTick']+1
                                        bar[-1]["UpVolume"]=bar[-1]['UpVolume']+te["Quantity"]
                                    else:
                                        bar[-1]["DownTick"]=bar[-1]['DownTick']+1
                                        bar[-1]["DownVolume"]=bar[-1]['DownVolume']+te["Quantity"]
                                    if te["Close"]>bar[-1]['High']:
                                        bar[-1]["High"]=te["Close"]
                                    if te["Close"]<bar[-1]['Low']:
                                        bar[-1]["Low"]=te["Close"]
                                    bar[-1]["Close"]=te["Close"]
                                    bar[-1]["Volume"]=bar[-1]["Volume"]+te["Quantity"]
                                    bar[-1]["OpenInterest"]=te["OpenInterest"]
                                else:
                                    ktemp={}
                                    ktemp["DateTime"]=te["DateTime"]+timedelta(seconds=interval-1)
                                    if ktemp["DateTime"].second%5!=0:
                                        print(ktemp["DateTime"])
                                    ktemp["Symbol"]=symbol
                                    ktemp["Open"]=te["Close"]
                                    ktemp["High"]=te["Close"]
                                    ktemp["Low"]=te["Close"]
                                    ktemp["Close"]=te["Close"]
                                    ktemp["Volume"]=te["Quantity"]
                                    ktemp["OpenInterest"]=te["OpenInterest"]
                                    if te["Close"]>bar[-1]['Close']:
                                        ktemp["DownTick"]=0
                                        ktemp["DownVolume"]=0
                                        ktemp["UnchVolume"]=0
                                        ktemp["UpTick"]=1
                                        ktemp["UpVolume"]=te["Quantity"]
                                    else:
                                        ktemp["DownTick"]=1
                                        ktemp["DownVolume"]=te["Quantity"]
                                        ktemp["UnchVolume"]=0
                                        ktemp["UpTick"]=0
                                        ktemp["UpVolume"]=0
                                    bar.append(ktemp)
                        self.onbar(bartype,interval,symbol,bar,True)
            else:
                if symbol in self.temp.keys():
                    self.temp[symbol].append(data[0])
                else:
                    self.temp[symbol]=data
        else:
            self.bardata[symbol+"-"+str(datatype)+"-"+str(interval)]=data
            self.onbar(datatype,interval,symbol,data,False)

    def onquotehistory(self,datatype,symbol,starttime,endtime,data:list):
        #if symbol+"-"+str(datatype) in self.bardata.keys():
        for interval in self.barinterval[symbol+"-"+str(datatype)]:
            if interval==1:
                if symbol+"-"+str(datatype)+"-"+str(interval) in self.bardata.keys():
                    self.onbarupdate(datatype,interval,symbol,data,False)
                if symbol+"-"+str(datatype)+str(interval)+":"+str(starttime)+"~"+str(endtime) in self.quotehistory.keys():
                    self.quotehistory[symbol+"-"+str(datatype)+str(interval)+":"+str(starttime)+"~"+str(endtime)]=data
                    win32event.SetEvent(self.quotehistoryevent)
            else:
                datatemp=[]
                for basedata in data:
                    basedata["DateTime"]=self.dtfilter(symbol,basedata["DateTime"])
                    if datatemp:
                        if basedata['DateTime']<=datatemp[-1]['DateTime']:
                            if datatype==2:
                                if basedata["Last"]>datatemp[-1]['Close']:
                                    datatemp[-1]["UpTick"]=datatemp[-1]['UpTick']+1
                                    datatemp[-1]["UpVolume"]=datatemp[-1]['UpVolume']+basedata["Quantity"]
                                else:
                                    datatemp[-1]["DownTick"]=datatemp[-1]['DownTick']+1
                                    datatemp[-1]["DownVolume"]=datatemp[-1]['DownVolume']+basedata["Quantity"]
                                if basedata["Last"]>datatemp[-1]['High']:
                                    datatemp[-1]["High"]=basedata["Last"]
                                if basedata["Last"]<datatemp[-1]['Low']:
                                    datatemp[-1]["Low"]=basedata["Last"]
                                datatemp[-1]["Close"]=basedata["Last"]
                                datatemp[-1]["Volume"]=datatemp[-1]["Volume"]+basedata["Quantity"]
                                datatemp[-1]["OpenInterest"]=basedata["OpenInterest"]
                            else:
                                if basedata["Close"]>datatemp[-1]['Close']:
                                    datatemp[-1]["UpTick"]=datatemp[-1]['UpTick']+1
                                    datatemp[-1]["UpVolume"]=datatemp[-1]['UpVolume']+basedata["Volume"]
                                else:
                                    datatemp[-1]["DownTick"]=datatemp[-1]['DownTick']+1
                                    datatemp[-1]["DownVolume"]=datatemp[-1]['DownVolume']+basedata["Volume"]
                                if basedata["Close"]>datatemp[-1]['High']:
                                    datatemp[-1]["High"]=basedata["Close"]
                                if basedata["Close"]<datatemp[-1]['Low']:
                                    datatemp[-1]["Low"]=basedata["Close"]
                                datatemp[-1]["Close"]=basedata["Close"]
                                datatemp[-1]["Volume"]=datatemp[-1]["Volume"]+basedata["Volume"]
                                datatemp[-1]["OpenInterest"]=basedata["OpenInterest"]
                        else:
                            ktemp={}
                            if datatype==2:
                                ktemp["DateTime"]=basedata["DateTime"]+timedelta(seconds=interval-1)
                                ktemp["Symbol"]=symbol
                                ktemp["Open"]=basedata["Last"]
                                ktemp["High"]=basedata["Last"]
                                ktemp["Low"]=basedata["Last"]
                                ktemp["Close"]=basedata["Last"]
                                ktemp["Volume"]=basedata["Quantity"]
                                ktemp["OpenInterest"]=basedata["OpenInterest"]
                                if basedata["Last"]>datatemp[-1]['Close']:
                                    ktemp["DownTick"]=0
                                    ktemp["DownVolume"]=0
                                    ktemp["UnchVolume"]=0
                                    ktemp["UpTick"]=1
                                    ktemp["UpVolume"]=basedata["Quantity"]
                                else:
                                    ktemp["DownTick"]=1
                                    ktemp["DownVolume"]=basedata["Quantity"]
                                    ktemp["UnchVolume"]=0
                                    ktemp["UpTick"]=0
                                    ktemp["UpVolume"]=0
                            else:
                                if datatype==4:
                                    ktemp["DateTime"]=datetime.strptime(str(basedata["DateTime"].date())+str(basedata["DateTime"].hour)+":"+str(basedata["DateTime"].minute)+":00" ,'%Y-%m-%d%H:%M:%S').replace(tzinfo=self.tz)+timedelta(minutes=interval-1)
                                if datatype==5:
                                    ktemp["DateTime"]=datetime.strptime(str(basedata["DateTime"].date())+str(basedata["DateTime"].hour)+":"+str(basedata["DateTime"].minute)+":00" ,'%Y-%m-%d%H:%M:%S').replace(tzinfo=self.tz)+timedelta(days=interval-1)
                                ktemp["Symbol"]=symbol
                                ktemp["Open"]=basedata["Open"]
                                ktemp["High"]=basedata["High"]
                                ktemp["Low"]=basedata["Low"]
                                ktemp["Close"]=basedata["Close"]
                                ktemp["Volume"]=basedata["Volume"]
                                ktemp["OpenInterest"]=basedata["OpenInterest"]
                                if basedata["Close"]>datatemp[-1]['Close']:
                                    ktemp["DownTick"]=0
                                    ktemp["DownVolume"]=0
                                    ktemp["UnchVolume"]=0
                                    ktemp["UpTick"]=1
                                    ktemp["UpVolume"]=basedata["Volume"]
                                else:
                                    ktemp["DownTick"]=1
                                    ktemp["DownVolume"]=basedata["Volume"]
                                    ktemp["UnchVolume"]=0
                                    ktemp["UpTick"]=0
                                    ktemp["UpVolume"]=0
                            datatemp.append(ktemp)
                    else:
                        if datatype==2:
                            basedata['DateTime']=basedata['DateTime']+timedelta(seconds=interval)
                            basedata['Symbol']=basedata['Symbol']
                            basedata['Open']=basedata['Last']
                            basedata['High']=basedata['Last']
                            basedata['Low']=basedata['Last']
                            basedata['Close']=basedata['Last']
                            basedata['Volume']=basedata['Quantity']
                            basedata['OpenInterest']=basedata['OpenInterest']
                            basedata['DownTick']=0
                            basedata['DownVolume']=0
                            basedata['UnchVolume']=0
                            basedata['UpTick']=1
                            basedata['UpVolume']=basedata['Quantity']
                            basedata.pop("Ask",None)
                            basedata.pop("Bid",None)
                            basedata.pop("Last",None)
                            basedata.pop("Quantity",None)
                        if datatype==4:
                            basedata['DateTime']=basedata['DateTime']+timedelta(minutes=interval-1)
                        if datatype==5:
                            basedata['DateTime']=basedata['DateTime']+timedelta(days=interval-1)
                        datatemp.append(basedata)
                if symbol+"-"+str(datatype)+"-"+str(interval) in self.bardata.keys():
                    self.onbarupdate(datatype,interval,symbol,datatemp,False)
                if symbol+"-"+str(datatype)+str(interval)+":"+str(starttime)+"~"+str(endtime) in self.quotehistory.keys():
                    self.quotehistory[symbol+"-"+str(datatype)+str(interval)+":"+str(starttime)+"~"+str(endtime)]=datatemp
                    win32event.SetEvent(self.quotehistoryevent)

        # self.quotehistory[symbol+"-"+str(datatype)+":"+str(starttime)+"~"+str(endtime)]=data
        # win32event.SetEvent(self.quotehistoryevent)

    def onquotereal(self,datatype,symbol,data:dict):
        self.onquote(data)
        isduring,start=self.isduringdt(symbol,data["DateTime"])
        if isduring and symbol in str(self.bardata):
            realbar={"DateTime":self.dtfilter(symbol,data["DateTime"]),
                "Symbol":data["Symbol"],
                "Ask":data["Ask"],
                "Bid":data["Bid"],
                "Open":data["Open"],
                "High":data["High"],
                "Low":data["Low"],
                "Close":data["Last"],
                "Quantity": data["Quantity"],#data["Quantity"]
                "Volume":data["Volume"]}
            if "TC.F" in symbol or "TC.O" in symbol:
                realbar["OpenInterest"]=data["OpenInterest"]
            else:
                realbar["OpenInterest"]=0
            #self.voltemp=data["Volume"]
            self.onbarupdate(datatype,None,symbol,[realbar],True)
        arrsymb=symbol.split(".")
        if isduring and arrsymb[3] in str(self.linedata):
            self.underlyingprice[symbol]=data

    def ongreeklineupdate(self,datatype,interval,symbol,data:list,isreal:bool):
        if isreal:
            linearr=[i for i in self.linedata.keys() if symbol in i]
            islinecout=0
            for linekey in linearr:
                if self.linedata[linekey]:
                    islinecout=islinecout+1
            if islinecout==len(linearr):
                for linekey in linearr:
                    line=self.linedata[linekey]
                    linetypeinte=linekey.split("-")
                    linetype=int(linetypeinte[1])
                    interval=int(linetypeinte[2])
                    if symbol in self.linetemp.keys():
                        if self.linetemp[symbol] :
                            for te in self.linetemp[symbol]:
                                if te["DateTime"]<=line[-1]['DateTime']:
                                    for key,_ in  line[-1].items():
                                        if key!="DateTime":
                                            line[-1][key]=te[key]
                                else:
                                    temp={}
                                    if linetype==9 or linetype==820:
                                        if (te['DateTime']-line[-1]['DateTime']).seconds>interval*60:
                                            te['DateTime']=te['DateTime']+timedelta(minutes=interval-1)
                                        else:
                                            te['DateTime']=line[-1]['DateTime']+timedelta(minutes=interval)
                                    if linetype==10 or linetype==800:
                                        if (te['DateTime']-line[-1]['DateTime']).seconds>interval:
                                            te['DateTime']=te['DateTime']+timedelta(seconds=interval-1)
                                        else:
                                            te['DateTime']=line[-1]['DateTime']+timedelta(seconds=interval)
                                    if linetype==19:
                                        if (te['DateTime']-line[-1]['DateTime']).days>interval:
                                            te['DateTime']=te['DateTime']+timedelta(days=interval-1)
                                        else:
                                            te['DateTime']=line[-1]['DateTime']+timedelta(days=interval)
                                    for key,_ in  line[-1].items():
                                            temp[key]=te[key]
                                    line.append(temp)
                        del self.linetemp[symbol]
                    else:
                        te=data[0]
                        if te["DateTime"]<=line[-1]['DateTime']:
                            for key,_ in  line[-1].items():
                                if key!="DateTime":
                                    line[-1][key]=te[key]
                        else:
                            temp={}
                            if linetype==9 or linetype==820:
                                if (te['DateTime']-line[-1]['DateTime']).seconds>interval*60:
                                    te['DateTime']=te['DateTime']+timedelta(minutes=interval-1)
                                else:
                                    te['DateTime']=line[-1]['DateTime']+timedelta(minutes=interval)
                            if linetype==10 or linetype==800:
                                if (te['DateTime']-line[-1]['DateTime']).seconds>interval:
                                    te['DateTime']=te['DateTime']+timedelta(seconds=interval-1)
                                else:
                                    te['DateTime']=line[-1]['DateTime']+timedelta(seconds=interval)
                            if linetype==19:
                                if (te['DateTime']-line[-1]['DateTime']).days>interval:
                                    te['DateTime']=te['DateTime']+timedelta(days=interval-1)
                                else:
                                    te['DateTime']=line[-1]['DateTime']+timedelta(days=interval)
                            for key,_ in  line[-1].items():
                                temp[key]=te[key]
                            line.append(temp)
                        self.ongreeksline(linetype,interval,symbol,line,True)
            else:
                if symbol in self.linetemp.keys():
                    self.linetemp[symbol].append(data[0])
                else:
                    self.linetemp[symbol]=data
        else:
            self.linedata[symbol+"-"+str(datatype)+"-"+str(interval)]=data
            self.ongreeksline(datatype,interval,symbol,data,isreal)
    def ongreekshistory(self,datatype,symbol,starttime,endtime,data:list):
        # self.greekshistory[symbol+"-"+str(datatype)+":"+str(starttime)+"~"+str(endtime)]=data
        # win32event.SetEvent(self.greekshistoryevent)
        for interval in self.lineinterval[symbol+"-"+str(datatype)]:
            if interval==1:
                if symbol+"-"+str(datatype)+"-"+str(interval) in self.linedata.keys():
                    self.ongreeklineupdate(datatype,interval,symbol,data,False)
                if symbol+"-"+str(datatype)+str(interval)+":"+str(starttime)+"~"+str(endtime) in self.greekshistory.keys():
                    self.greekshistory[symbol+"-"+str(datatype)+str(interval)+":"+str(starttime)+"~"+str(endtime)]=data
                    win32event.SetEvent(self.greekshistoryevent)
            else:
                datatemp=[]
                for basedata in data:
                    basedata["DateTime"]=self.dtfilter(symbol,basedata["DateTime"])
                    if datatemp:
                        if basedata['DateTime']<=datatemp[-1]['DateTime']:
                            for key,_ in  datatemp[-1].items():
                                if key!="DateTime":
                                    datatemp[-1][key]=basedata[key]
                        else:
                            if datatype==9 or datatype==820:
                                if (basedata['DateTime']-datatemp[-1]['DateTime']).seconds>interval*60:
                                    basedata['DateTime']=basedata['DateTime']+timedelta(minutes=interval-1)
                                else:
                                    basedata['DateTime']=datatemp[-1]['DateTime']+timedelta(minutes=interval)
                            if datatype==10 or datatype==800:
                                if (basedata['DateTime']-datatemp[-1]['DateTime']).seconds>interval:
                                    basedata['DateTime']=basedata['DateTime']+timedelta(seconds=interval-1)
                                else:
                                    basedata['DateTime']=datatemp[-1]['DateTime']+timedelta(seconds=interval)
                            if datatype==19:
                                if (basedata['DateTime']-datatemp[-1]['DateTime']).days>interval:
                                    basedata['DateTime']=basedata['DateTime']+timedelta(days=interval-1)
                                else:
                                    basedata['DateTime']=datatemp[-1]['DateTime']+timedelta(days=interval)
                            datatemp.append(basedata)
                    else:
                        if datatype==9 or datatype==820:
                            basedata['DateTime']=basedata['DateTime']+timedelta(minutes=interval-1)
                        if datatype==10 or datatype==800:
                            basedata['DateTime']=basedata['DateTime']+timedelta(seconds=interval)
                        if datatype==19:
                            basedata['DateTime']=basedata['DateTime']+timedelta(days=interval-1)
                        datatemp.append(basedata)
                        
                if symbol+"-"+str(datatype)+"-"+str(interval) in self.linedata.keys():
                    self.ongreeklineupdate(datatype,interval,symbol,datatemp,False)
                if symbol+"-"+str(datatype)+str(interval)+":"+str(starttime)+"~"+str(endtime) in self.greekshistory.keys():
                    self.greekshistory[symbol+"-"+str(datatype)+str(interval)+":"+str(starttime)+"~"+str(endtime)]=datatemp
                    win32event.SetEvent(self.greekshistoryevent)
    def ongreeksreal(self,datatype,symbol,data:dict):
        if self.extendevent:
            self.extendevent.ongreeksreal(datatype,symbol,data)
        isduring,start=self.isduringdt(symbol,data["DateTime"])
        if isduring and symbol in str(self.linedata):
            realline={}
            if "TC.F" in symbol:
                realline={'DateTime':self.dtfilter(symbol,data["DateTime"]), 
                'Symbol': symbol, 
                'AnnualTradeday': data['AnnualTradeday'], 
                'TheoVal': None, 
                'IntVal':None, 
                'ATV': data['ATV'], 
                'ExtVal': data['ExtVal'], 
                'TV': data['TV'], 
                'IV': data['IV'], 
                'Last': self.underlyingprice[symbol]['Last'], 
                'CSkew': data['CSkew'], 
                'PSkew': data['PSkew'], 
                'CIV25D': data['CIV25D'], 
                'PIV25D': data['PIV25D'], 
                'CIV10D': data['CIV10D'], 
                'PIV10D': data['PIV10D'], 
                'CallVol':data['CallVol'],
                'PutVol':data['PutVol'],
                'CallOI':data['CallOI'],
                'PutOI':data['PutOI'],
                'CKUpCnt': data['CKUpCnt'], 
                'CKUpVol': data['CKUpVol'], 
                'CKDnCnt': data['CKDnCnt'], 
                'CKDnVol': data['CKDnVol'], 
                'PKUpCnt': data['PKUpCnt'], 
                'PKUpVol': data['PKUpVol'], 
                'PKDnCnt': data['PKDnCnt'], 'PKDnVol': data['PKDnVol']}
            if "TC.O" in symbol:
                arrsymb=symbol.split(".")
                greekonly={}
                if "SSE" in symbol or "SZSE" in symbol:
                    
                    usymbol="TC.S."+arrsymb[2]+"."+arrsymb[3]
                    ufsymbol="TC.F.U_"+arrsymb[2]+"."+arrsymb[3]+"."+arrsymb[4]
                    greekonly={'us': usymbol, 
                    'us_datetime': self.underlyingprice[usymbol]['DateTime'] if usymbol in self.underlyingprice.keys() else None, 
                    'us_p': self.underlyingprice[usymbol]['Last'] if usymbol in self.underlyingprice.keys() else None,
                    'us_bp1': self.underlyingprice[usymbol]['Bid'] if usymbol in self.underlyingprice.keys() else None, 
                    'us_sp1': self.underlyingprice[usymbol]['Ask'] if usymbol in self.underlyingprice.keys() else None, 
                    'uf': '', 
                    'uf_datetime':None, 
                    'uf_p': None, 
                    'uf_bp1': None, 
                    'uf_sp1': None, 
                    'usf': ufsymbol,
                    'usf_datetime':self.underlyingprice[ufsymbol]['DateTime'] if ufsymbol in self.underlyingprice.keys() else None, 
                    'usf_p': self.underlyingprice[ufsymbol]['Last'] if ufsymbol in self.underlyingprice.keys() else None}
                else:
                    usymbol="TC.F."+arrsymb[2]+"."+arrsymb[3]+"."+arrsymb[4]
                    ufsymbol="TC.F.U_"+arrsymb[2]+"."+arrsymb[3]+"."+arrsymb[4]
                    greekonly={'us': "", 
                    'us_datetime':None, 
                    'us_p': None,
                    'us_bp1': None, 
                    'us_sp1': None, 
                    'uf': usymbol, 
                    'uf_datetime':self.underlyingprice[usymbol]['DateTime'] if usymbol in self.underlyingprice.keys() else None, 
                    'uf_p': self.underlyingprice[usymbol]['Last'] if usymbol in self.underlyingprice.keys() else None, 
                    'uf_bp1': self.underlyingprice[usymbol]['Bid'] if usymbol in self.underlyingprice.keys() else None, 
                    'uf_sp1': self.underlyingprice[usymbol]['Ask'] if usymbol in self.underlyingprice.keys() else None, 
                    'usf': ufsymbol,
                    'usf_datetime':self.underlyingprice[ufsymbol]['DateTime'] if ufsymbol in self.underlyingprice.keys() else None, 
                    'usf_p': self.underlyingprice[ufsymbol]['Last'] if ufsymbol in self.underlyingprice.keys() else None}

                realline={'DateTime':self.dtfilter(symbol,data["DateTime"]), 
                'Symbol': symbol, 
                'AnnualTradeday': data['AnnualTradeday'], 
                'TheoVal': data['TheoVal'], 
                'IntVal':data['IntVal'], 
                'ATV': data['ATV'], 
                'ExtVal': data['ExtVal'], 
                'TV': data['TV'], 
                'IV': data['IV'], 
                'MIV': data['MIV'], 
                'CPIV': data['CPIV'], 
                'AIV': data['SIV'], 
                'BIV': data['BIV'], 
                'Delta': data['Delta'], 
                'Gamma': data['Gamma'], 
                'Vega': data['Vega'], 
                'Theta': data['Theta'], 
                'Rho': data['Rho'], 
                'LR': data['LR'], 
                'RealLR': data['RealLR'], 
                'OPR': data['OPR'], 
                'ROI': data['ROI'], 
                'BER': data['BER'], 
                'Charm': data['Charm'], 
                'Vanna': data['Vanna'], 
                'Vomma': data['Vomma'], 
                'Speed': data['Speed'], 
                'Zomma': data['Zomma'], 
                'Last': self.underlyingprice[symbol]['Last'], 
                'UnderlingPrice':self.underlyingprice[usymbol]['Last']  if usymbol in self.underlyingprice.keys() else None, 
                'Volume': self.underlyingprice[symbol]['Volume'], 
                'OI': self.underlyingprice[symbol]['OpenInterest'], 
                'Bid': self.underlyingprice[symbol]['Bid'], 
                'Bid1': self.underlyingprice[symbol]['Bid1'], 
                'Bid2': self.underlyingprice[symbol]['Bid2'], 
                'Bid3': self.underlyingprice[symbol]['Bid3'], 
                'Bid4': self.underlyingprice[symbol]['Bid4'], 
                'Bid5': self.underlyingprice[symbol]['Bid5'], 
                'Bid6': self.underlyingprice[symbol]['Bid6'], 
                'Bid7': self.underlyingprice[symbol]['Bid7'], 
                'Bid8': self.underlyingprice[symbol]['Bid8'], 
                'Bid9': self.underlyingprice[symbol]['Bid9'], 
                'BidVolume': self.underlyingprice[symbol]['BidVolume'], 
                'BidVolume1': self.underlyingprice[symbol]['BidVolume1'], 
                'BidVolume2': self.underlyingprice[symbol]['BidVolume2'], 
                'BidVolume3': self.underlyingprice[symbol]['BidVolume3'], 
                'BidVolume4': self.underlyingprice[symbol]['BidVolume4'], 
                'BidVolume5': self.underlyingprice[symbol]['BidVolume5'], 
                'BidVolume6': self.underlyingprice[symbol]['BidVolume6'], 
                'BidVolume7': self.underlyingprice[symbol]['BidVolume7'], 
                'BidVolume8': self.underlyingprice[symbol]['BidVolume8'], 
                'BidVolume9': self.underlyingprice[symbol]['BidVolume9'], 
                'Bid_UpdateDatetime': self.underlyingprice[symbol]['DateTime'], 
                'Bid1_UpdateDatetime':self.underlyingprice[symbol]['DateTime'], 
                'Bid2_UpdateDatetime':self.underlyingprice[symbol]['DateTime'], 
                'Bid3_UpdateDatetime':self.underlyingprice[symbol]['DateTime'], 
                'Bid4_UpdateDatetime':self.underlyingprice[symbol]['DateTime'], 
                'Ask': self.underlyingprice[symbol]['Ask'],
                'Ask1': self.underlyingprice[symbol]['Ask1'],
                'Ask2': self.underlyingprice[symbol]['Ask2'],
                'Ask3': self.underlyingprice[symbol]['Ask3'],
                'Ask4': self.underlyingprice[symbol]['Ask4'],
                'Ask5': self.underlyingprice[symbol]['Ask5'],
                'Ask6': self.underlyingprice[symbol]['Ask6'],
                'Ask7': self.underlyingprice[symbol]['Ask7'],
                'Ask8': self.underlyingprice[symbol]['Ask8'],
                'Ask9': self.underlyingprice[symbol]['Ask9'],
                'AskVolume': self.underlyingprice[symbol]['AskVolume'],
                'AskVolume1': self.underlyingprice[symbol]['AskVolume1'], 
                'AskVolume2': self.underlyingprice[symbol]['AskVolume2'],
                'AskVolume3': self.underlyingprice[symbol]['AskVolume3'], 
                'AskVolume4': self.underlyingprice[symbol]['AskVolume4'],
                'AskVolume5': self.underlyingprice[symbol]['AskVolume5'],
                'AskVolume6': self.underlyingprice[symbol]['AskVolume6'],
                'AskVolume7': self.underlyingprice[symbol]['AskVolume7'],
                'AskVolume8': self.underlyingprice[symbol]['AskVolume8'],
                'AskVolume9': self.underlyingprice[symbol]['AskVolume9'],
                'Ask_UpdateDatetime': self.underlyingprice[symbol]['DateTime'] , 
                'Ask1_UpdateDatetime': self.underlyingprice[symbol]['DateTime'], 
                'Ask2_UpdateDatetime': self.underlyingprice[symbol]['DateTime'], 
                'Ask3_UpdateDatetime': self.underlyingprice[symbol]['DateTime'], 
                'Ask4_UpdateDatetime': self.underlyingprice[symbol]['DateTime']}
                realline.update(greekonly) 
            self.ongreeklineupdate(datatype,None,symbol,[realline],True)

    def OnQuoteData(self, SymbolType, DataType, QuoteData):
        quote=client.Dispatch(QuoteData)
        if DataType==1 and SymbolType!=8: #实时
            temp={"DateTime":datetime.strptime(str(quote.TradeDate)+(" 0" if len(str(quote.FilledTime))==5 else " ")+str(quote.FilledTime),"%Y%m%d %H%M%S").replace(tzinfo=self.tz)+timedelta(hours=8),
                    "TradeDate":quote.GetValueFromIndex(101),
                    "Time":quote.FilledTime,
                    "Symbol":quote.Symbol,
                    "Open":iff(quote.OpeningPrice,10000000000),
                    "High":iff(quote.HighPrice,10000000000),
                    "Low":iff(quote.LowPrice,10000000000),
                    "Last":iff(quote.TradingPrice,10000000000),
                    "LowerLimit":iff(quote.LowerLimitPrice,10000000000),
                    "UpperLimit":iff(quote.UpperLimitPrice,10000000000),
                    "Quantity":iff(quote.TradeQuantity),
                    "Volume":iff(quote.TradeVolume),
                    "Turnover":iff(quote.GetValueFromIndex(7)),
                    "Ask":iff(quote.Ask,10000000000),
                    "Ask1":iff(quote.Ask1,10000000000),
                    "Ask2":iff(quote.Ask2,10000000000),
                    "Ask3":iff(quote.Ask3,10000000000),
                    "Ask4":iff(quote.Ask4,10000000000),
                    "Ask5":iff(quote.Ask5,10000000000),
                    "Ask6":iff(quote.Ask6,10000000000),
                    "Ask7":iff(quote.Ask7,10000000000),
                    "Ask8":iff(quote.Ask8,10000000000),
                    "Ask9":iff(quote.Ask9,10000000000),
                    "AskVolume":iff(quote.AskVolume),
                    "AskVolume1":iff(quote.AskVolume1),
                    "AskVolume2":iff(quote.AskVolume2),
                    "AskVolume3":iff(quote.AskVolume3),
                    "AskVolume4":iff(quote.AskVolume4),
                    "AskVolume5":iff(quote.AskVolume5),
                    "AskVolume6":iff(quote.AskVolume6),
                    "AskVolume7":iff(quote.AskVolume7),
                    "AskVolume8":iff(quote.AskVolume8),
                    "AskVolume9":iff(quote.AskVolume9),
                    "Bid":iff(quote.Bid,10000000000),
                    "Bid1":iff(quote.Bid1,10000000000),
                    "Bid2":iff(quote.Bid2,10000000000),
                    "Bid3":iff(quote.Bid3,10000000000),
                    "Bid4":iff(quote.Bid4,10000000000),
                    "Bid5":iff(quote.Bid5,10000000000),
                    "Bid6":iff(quote.Bid6,10000000000),
                    "Bid7":iff(quote.Bid7,10000000000),
                    "Bid8":iff(quote.Bid8,10000000000),
                    "Bid9":iff(quote.Bid9,10000000000),
                    "BidVolume":iff(quote.BidVolume),
                    "BidVolume1":iff(quote.BidVolume1),
                    "BidVolume2":iff(quote.BidVolume2),
                    "BidVolume3":iff(quote.BidVolume3),
                    "BidVolume4":iff(quote.BidVolume4),
                    "BidVolume5":iff(quote.BidVolume5),
                    "BidVolume6":iff(quote.BidVolume6),
                    "BidVolume7":iff(quote.BidVolume7),
                    "BidVolume8":iff(quote.BidVolume8),
                    "BidVolume9":iff(quote.BidVolume9),
                    "Change":iff(quote.Change,10000000000),
                    "OpenTime":quote.OpenTime,
                    "CloseTime":quote.CloseTime,
                    "Exchange":quote.Exchange,
                    "ExchangeName":quote.ExchangeName,
                    #"PreciseTime":quote.PreciseTime,
                    "ReferencePrice":iff(quote.ReferencePrice,10000000000),
                    "Security":quote.Security,
                    "SecurityName":quote.SecurityName,
                    "TotalAskCount":quote.TotalAskCount,
                    "TotalAskVolume":quote.TotalAskVolume,
                    "TotalBidCount":quote.TotalBidCount,
                    "TotalBidVolume":quote.TotalBidVolume,
                    "YClosedPrice":iff(quote.YClosedPrice,10000000000),
                    "YTradeVolume":iff(quote.YTradeVolume),
                    "InstrumentStatus":quote.GetValueFromIndex(121)}#开市：0  闭市：4  集合竞价：5   非交易时段：9
            if SymbolType==1: #证
                temp["SimMatchPrice"]=iff(quote.GetValueFromIndex(122),10000000000)
                temp["SimMatchvol"]=iff(quote.GetValueFromIndex(123))
                temp["SimMatchchg"]=iff(quote.GetValueFromIndex(124),10000000000)
                temp["FusePrice"]=iff(quote.GetValueFromIndex(145),10000000000)
                temp["FuseCountdown"]=iff(quote.GetValueFromIndex(252))
            elif SymbolType==2: #期货
                temp["OpenInterest"]=iff(quote.OpenInterest)
                temp["YOpenInterest"]=iff(quote.YOpenInterest)
                temp["OpenDate"]=iff(quote.BeginDate)
                temp["ExpireDate"]=iff(quote.EndDate)
                temp["ExpiryDays"]=iff(quote.ExpiryDate)
                temp["Month"]=quote.Month
                temp["SellCount"]=quote.SellCount
                temp["Settlement"]=iff(quote.SettlementPrice,10000000000)
                temp["ClosingPrice"]=iff(quote.ClosingPrice,10000000000)
                temp["FlagOfBuySell"]=quote.FlagOfBuySell
            elif SymbolType==3: #期权
                temp["OpenInterest"]=iff(quote.OpenInterest)
                temp["YOpenInterest"]=iff(quote.YOpenInterest)
                temp["OpenDate"]=iff(quote.BeginDate)
                temp["ExpireDate"]=iff(quote.EndDate)
                temp["Month"]=quote.Month
                temp["SellCount"]=quote.SellCount
                temp["Settlement"]=iff(quote.SettlementPrice,10000000000)
                temp["ClosingPrice"]=iff(quote.ClosingPrice)
                temp["CallPut"]=quote.CallPut
                temp["Future"]=quote.Future
                temp["StrikePrice"]=iff(quote.StrikePrice,10000000000)
                temp["TradeSymbol"]=quote.TradeSymbol
                temp["Underlying"]=quote.Underlying
                temp["SimMatchPrice"]=iff(quote.GetValueFromIndex(122),10000000000)
                temp["SimMatchvol"]=iff(quote.GetValueFromIndex(123))
                temp["SimMatchchg"]=iff(quote.GetValueFromIndex(124),10000000000)
                temp["FusePrice"]=iff(quote.GetValueFromIndex(145),10000000000)
                temp["FuseCountdown"]=iff(quote.GetValueFromIndex(252))
            self.onquotereal(DataType,quote.Symbol,temp)
            
        elif DataType==1 and SymbolType==8: #ATM symbol
            self.onATM(DataType,quote.GetStringData("Symbol"),{"Symbol":quote.GetStringData("Symbol"),"ATM":quote.GetStringData("ATM0_STK"),"OTM-1C":quote.GetStringData("ATM+1C_Symbol"),"OTM-1P":quote.GetStringData("ATM-1P_Symbol"),"OPTLIST":(quote.GetStringData("STKLIST").strip("|").split("|"))})
        elif DataType==6: #实时Greeks
            if "TC.F" in quote.Symbol:
                self.ongreeksreal(DataType,quote.Symbol,
                        {"DateTime":datetime.strptime(str(quote.TradingDay)+(" 0" if len(str(quote.TradingHours))==5 else " ")+str(quote.TradingHours),"%Y%m%d %H%M%S").replace(tzinfo=self.tz)+timedelta(hours=8),
                        "Time": quote.TradingHours,
                        "Symbol":quote.Symbol,
                        "CalendarDays": iff(quote.GetGreeksValue("CalendarDays")),
                        "TradingDays": iff(quote.GetGreeksValue("TDate")),
                        "AnnualTradeday":iff(quote.GetGreeksValue("TDTime"),10000000000),
                        "AnnualCalendarDay":iff(quote.GetGreeksValue("DTime"),10000000000),
                        "CTR":iff(quote.GetGreeksValue("CTR"),10000000000),
                        "YCTR":iff(quote.GetGreeksValue("YCTR"),10000000000),
                        "PTR":iff(quote.GetGreeksValue("PTR"),10000000000),
                        "YPTR":iff(quote.GetGreeksValue("YPTR"),10000000000),
                        "RCTR":iff(quote.GetGreeksValue("RCTR"),10000000000),
                        "RPTR":iff(quote.GetGreeksValue("RPTR"),10000000000),
                        "YRCTR":iff(quote.GetGreeksValue("YRCTR"),10000000000),
                        "YRPTR":iff(quote.GetGreeksValue("YRPTR"),10000000000),
                        "FCIV25":iff(quote.GetGreeksValue("25FCIV"),10000000000),
                        "FPIV25":iff(quote.GetGreeksValue("25FPIV"),10000000000),
                        "YFCIV25":iff(quote.GetGreeksValue("25FYdCIV"),10000000000),
                        "YFPIV25":iff(quote.GetGreeksValue("25FYdPIV"),10000000000),
                        "ExtVal":iff(quote.ExtVal,10000000000),
                        "TV":iff(quote.GetGreeksValue("TV"),10000000000),
                        "ATV":iff(quote.GetGreeksValue("ATV"),10000000000),
                        "YTV":iff(quote.GetGreeksValue("YTV"),10000000000),
                        "YATV":iff(quote.GetGreeksValue("YATV"),10000000000),
                        "HV_W4":iff(quote.HV_W4,10000000000),
                        "HV_W8":iff(quote.HV_W8,10000000000),
                        "HV_W13":iff(quote.HV_W13,10000000000),
                        "HV_W26":iff(quote.HV_W26,10000000000),
                        "HV_W52":iff(quote.HV_W52,10000000000),
                        "PutD":iff(quote.GetGreeksValue("Putd"),10000000000),
                        "CallD":iff(quote.GetGreeksValue("Calld"),10000000000),
                        "D25CStraddle":iff(quote.GetGreeksValue("25DCStraddle"),10000000000),
                        "D25PStraddle":iff(quote.GetGreeksValue("25DPStraddle"),10000000000),
                        "D25CTV":iff(quote.GetGreeksValue("25DCTV"),10000000000),
                        "D25PTV":iff(quote.GetGreeksValue("25DPTV"),10000000000),
                        "YPutD":iff(quote.GetGreeksValue("YPutd"),10000000000),
                        "YCallD":iff(quote.GetGreeksValue("YCalld"),10000000000),
                        "FIV":iff(quote.GetGreeksValue("FIV"),10000000000),
                        "YFIV":iff(quote.GetGreeksValue("YFIV"),10000000000),
                        "IV":iff(quote.GetGreeksValue("Volatility"),10000000000),
                        "PreIV":iff(quote.PreImpVol,10000000000),
                        "Straddle":iff(quote.GetGreeksValue("Straddle"),10000000000),
                        "YStraddle":iff(quote.GetGreeksValue("YStraddle"),10000000000),
                        "StraddleStrike":iff(quote.GetGreeksValue("StraddleStrike"),10000000000),
                        "StraddleWeight":iff(quote.GetGreeksValue("StraddleWeight")),
                        "CIV25D":iff(quote.GetGreeksValue("25DCIV"),10000000000),
                        "PIV25D":iff(quote.GetGreeksValue("25DPIV"),10000000000),
                        "CIV10D":iff(quote.GetGreeksValue("10DCIV"),10000000000),
                        "PIV10D":iff(quote.GetGreeksValue("10DPIV"),10000000000),
                        "YCIV25D":iff(quote.GetGreeksValue("25DYdCIV"),10000000000),
                        "YPIV25D":iff(quote.GetGreeksValue("25DYdPIV"),10000000000),
                        "YCIV10D":iff(quote.GetGreeksValue("10DYdCIV"),10000000000),
                        "YPIV10D":iff(quote.GetGreeksValue("10DYdPIV"),10000000000),
                        "VIX":iff(quote.VIX,10000000000),
                        "CallOI":iff(quote.GetGreeksValue("CallOI")),
                        "YCallOI":iff(quote.GetGreeksValue("YCallOI")),
                        "CallVol":iff(quote.GetGreeksValue("CallVol")),
                        "YCallVol":iff(quote.GetGreeksValue("YCallVol")),
                        "PutOI":iff(quote.GetGreeksValue("PutOI")),
                        "YPutOI":iff(quote.GetGreeksValue("YPutOI")),
                        "PutVol":iff(quote.GetGreeksValue("PutVol")),
                        "YPutVol":iff(quote.GetGreeksValue("YPutVol")),
                        "CKUpCnt":iff(quote.GetGreeksValue("CKUpCnt")),
                        "CKUpVol":iff(quote.GetGreeksValue("CKUpVol")),
                        "CKDnCnt":iff(quote.GetGreeksValue("CKDnCnt")),
                        "CKDnVol":iff(quote.GetGreeksValue("CKDnVol")),
                        "PKUpCnt":iff(quote.GetGreeksValue("PKUpCnt")),
                        "PKUpVol":iff(quote.GetGreeksValue("PKUpVol")),
                        "PKDnCnt":iff(quote.GetGreeksValue("PKDnCnt")),
                        "PKDnVol":iff(quote.GetGreeksValue("PKDnVol")),
                        "CSkew": quote.GetGreeksValue("Calld")/quote.GetGreeksValue("Volatility")*100 if quote.GetGreeksValue("Calld")>-9999999999999999 and quote.GetGreeksValue("Volatility")>-9999999999999999 else None,
                        "PSkew": quote.GetGreeksValue("Putd")/quote.GetGreeksValue("Volatility")*100 if quote.GetGreeksValue("Putd")>-9999999999999999 and quote.GetGreeksValue("Volatility")>-9999999999999999 else None})
            else:
                self.ongreeksreal(DataType,quote.Symbol,
                        {"DateTime":datetime.strptime(str(quote.TradingDay)+(" 0" if len(str(quote.TradingHours))==5 else " ")+str(quote.TradingHours),"%Y%m%d %H%M%S").replace(tzinfo=self.tz)+timedelta(hours=8),
                        'Time': quote.GetGreeksValue("TradingHours"),
                        "Symbol":quote.Symbol,
                        'CalendarDays': quote.GetGreeksValue("CalendarDays"),
                        'TradingDays': quote.GetGreeksValue("TDate"), 
                        'AnnualTradeday':iff(quote.GetGreeksValue("TDTime"),10000000000),
                        'AnnualCalendarDay':iff(quote.GetGreeksValue("DTime"),10000000000),
                        'Ask':iff(quote.Ask,10000000000), 
                        'Bid':iff(quote.Bid,10000000000), 
                        'Mid':iff(quote.GetGreeksValue("Mid"),10000000000), 
                        'MIV':iff(quote.GetGreeksValue("MIV"),10000000000), 
                        'Delta':iff(quote.GetGreeksValue("Delta"),10000000000), 
                        'ExtVal':iff(quote.GetGreeksValue("ExtVal"),10000000000), 
                        'TV':iff(quote.GetGreeksValue("TV"),10000000000), 
                        'ATV':iff(quote.GetGreeksValue("ATV"),10000000000),
                        'YTV':iff(quote.GetGreeksValue("YTV"),10000000000), 
                        'YATV':iff(quote.GetGreeksValue("YATV"),10000000000),
                        'Gamma':iff(quote.GetGreeksValue("Gamma"),10000000000), 
                        'IV':iff(quote.GetGreeksValue("ImpVol"),10000000000), 
                        'PreIV':iff(quote.GetGreeksValue("PreImpVol"),10000000000), 
                        'IntVal':iff(quote.GetGreeksValue("IntVal"),10000000000), 
                        'Rho':iff(quote.GetGreeksValue("Rho"),10000000000), 
                        'BIV':iff(quote.BIV,10000000000), 
                        'BIV2':iff(quote.GetGreeksValue("BIV2"),10000000000), 
                        'BIV3':iff(quote.GetGreeksValue("BIV3"),10000000000), 
                        'BIV4':iff(quote.GetGreeksValue("BIV4"),10000000000), 
                        'BIV5':iff(quote.GetGreeksValue("BIV5"),10000000000),
                        'SIV':iff(quote.SIV,10000000000), 
                        'SIV2':iff(quote.GetGreeksValue("SIV2"),10000000000), 
                        'SIV3':iff(quote.GetGreeksValue("SIV3"),10000000000), 
                        'SIV4':iff(quote.GetGreeksValue("SIV4"),10000000000), 
                        'SIV5':iff(quote.GetGreeksValue("SIV5"),10000000000), 
                        'TheoVal':iff(quote.GetGreeksValue("TheoVal"),10000000000), 
                        'Theta':iff(quote.GetGreeksValue("Theta"),10000000000),  
                        'Vega':iff(quote.GetGreeksValue("Vega"),10000000000), 
                        'CPIV':iff(quote.GetGreeksValue("CPIV"),10000000000),
                        'LR':iff(quote.GetGreeksValue("LR"),10000000000), 
                        'RealLR':iff(quote.GetGreeksValue("RealLR"),10000000000), 
                        'OPR':iff(quote.GetGreeksValue("OPR"),10000000000), 
                        'ROI':iff(quote.GetGreeksValue("ROI"),10000000000), 
                        'BER':iff(quote.GetGreeksValue("BER"),10000000000), 
                        'Charm':iff(quote.GetGreeksValue("Charm"),10000000000), 
                        'Vanna':iff(quote.GetGreeksValue("Vanna"),10000000000), 
                        'Vomma':iff(quote.GetGreeksValue("Vomma"),100000000),
                        'Speed':iff(quote.GetGreeksValue("Speed"),10000000000), 
                        'Zomma':iff(quote.GetGreeksValue("Zomma"),10000000000)})
        
        elif DataType==820 or DataType==800:
            dogshis=[]
            #print(quote,"  ",quote.GetStringData("Symbol")," ",quote.GetValueData("StartTime")," ",quote.GetValueData("EndTime")," ",quote.GetValueData("Type")," ",quote.GetValueData("Count"))
            for i in range(quote.GetValueData("Count")):  
                ttemp=str(int(quote.GetItemValue(i,1)/1000))
                symbol=quote.GetStringData("Symbol")
                if "TC.O" in symbol:
                    dogshis.append({"DateTime":datetime.strptime(str(quote.GetItemValue(i,0))+(" 0" if len(ttemp)==5 else " ")+ttemp,"%Y%m%d %H%M%S").replace(tzinfo=self.tz)+timedelta(hours=8),
                    "Symbol":quote.GetStringData("Symbol"),
                    'AnnualTradeday':iff(quote.GetItemValue(i,2),10000000000),
                    'TheoVal':iff(quote.GetItemValue(i,3),10000000000),
                    'IntVal':iff(quote.GetItemValue(i,4),10000000000),
                    'ATV':iff(quote.GetItemValue(i,5),10000000000),
                    'ExtVal':iff(quote.GetItemValue(i,6),10000000000),
                    'TV':iff(quote.GetItemValue(i,7),10000000000),
                    'IV':iff(quote.GetItemValue(i,8),10000000000),
                    'MIV':iff(quote.GetItemValue(i,9),10000000000),
                    'CPIV':iff(quote.GetItemValue(i,10),10000000000),
                    'AIV':iff(quote.GetItemValue(i,11),10000000000),
                    'BIV':iff(quote.GetItemValue(i,12),10000000000),
                    'Delta':iff(quote.GetItemValue(i,13),10000000000),
                    'Gamma':iff(quote.GetItemValue(i,14),10000000000),
                    'Vega':iff(quote.GetItemValue(i,15),10000000000),
                    'Theta':iff(quote.GetItemValue(i,16),10000000000),
                    'Rho':iff(quote.GetItemValue(i,17),10000000000),
                    'LR':iff(quote.GetItemValue(i,18),10000000000),
                    'RealLR':iff(quote.GetItemValue(i,19),10000000000),
                    'OPR':iff(quote.GetItemValue(i,20),10000000000),
                    'ROI':iff(quote.GetItemValue(i,21),10000000000),
                    'BER':iff(quote.GetItemValue(i,22),10000000000),
                    'Charm':iff(quote.GetItemValue(i,23),10000000000),
                    'Vanna':iff(quote.GetItemValue(i,24),10000000000),
                    'Vomma':iff(quote.GetItemValue(i,25),100000000),
                    'Speed':iff(quote.GetItemValue(i,26),10000000000),
                    'Zomma':iff(quote.GetItemValue(i,27),10000000000),
                    'Last':iff(quote.GetItemValue(i,28),10000000000),
                    'UnderlingPrice':iff(quote.GetItemValue(i,29),10000000000),
                    'Volume':iff(quote.GetItemValue(i,30)),
                    'OI':iff(quote.GetItemValue(i,31)),
                    #'sta':iff(quote.GetItemValue(i,32) ,
                    'Bid':iff(quote.GetItemValue(i,51),10000000000),
                    'Bid1':iff(quote.GetItemValue(i,52),10000000000),
                    'Bid2':iff(quote.GetItemValue(i,53),10000000000),
                    'Bid3':iff(quote.GetItemValue(i,54),10000000000),
                    'Bid4':iff(quote.GetItemValue(i,55),10000000000),
                    'Bid5':iff(quote.GetItemValue(i,56),10000000000),
                    'Bid6':iff(quote.GetItemValue(i,57),10000000000),
                    'Bid7':iff(quote.GetItemValue(i,58),10000000000),
                    'Bid8':iff(quote.GetItemValue(i,59),10000000000),
                    'Bid9':iff(quote.GetItemValue(i,60),10000000000),
                    'BidVolume':iff(quote.GetItemValue(i,61)),
                    'BidVolume1':iff(quote.GetItemValue(i,62)),
                    'BidVolume2':iff(quote.GetItemValue(i,63)),
                    'BidVolume3':iff(quote.GetItemValue(i,64)),
                    'BidVolume4':iff(quote.GetItemValue(i,65)),
                    'BidVolume5':iff(quote.GetItemValue(i,66)),
                    'BidVolume6':iff(quote.GetItemValue(i,67)),
                    'BidVolume7':iff(quote.GetItemValue(i,68)),
                    'BidVolume8':iff(quote.GetItemValue(i,69)),
                    'BidVolume9':iff(quote.GetItemValue(i,70)),
                    'Bid_UpdateDatetime':datetime.strptime(str(quote.GetItemValue(i,71))+(" 0" if len(str(int(quote.GetItemValue(i,76)/1000)))==5 else " ")+str(int(quote.GetItemValue(i,76)/1000)),"%Y%m%d %H%M%S").replace(tzinfo=self.tz)+timedelta(hours=8),
                    'Bid1_UpdateDatetime':datetime.strptime(str(quote.GetItemValue(i,72))+(" 0" if len(str(int(quote.GetItemValue(i,77)/1000)))==5 else " ")+str(int(quote.GetItemValue(i,77)/1000)),"%Y%m%d %H%M%S").replace(tzinfo=self.tz)+timedelta(hours=8),
                    'Bid2_UpdateDatetime':datetime.strptime(str(quote.GetItemValue(i,73))+(" 0" if len(str(int(quote.GetItemValue(i,78)/1000)))==5 else " ")+str(int(quote.GetItemValue(i,78)/1000)),"%Y%m%d %H%M%S").replace(tzinfo=self.tz)+timedelta(hours=8),
                    'Bid3_UpdateDatetime':datetime.strptime(str(quote.GetItemValue(i,74))+(" 0" if len(str(int(quote.GetItemValue(i,79)/1000)))==5 else " ")+str(int(quote.GetItemValue(i,79)/1000)),"%Y%m%d %H%M%S").replace(tzinfo=self.tz)+timedelta(hours=8),
                    'Bid4_UpdateDatetime':datetime.strptime(str(quote.GetItemValue(i,75))+(" 0" if len(str(int(quote.GetItemValue(i,80)/1000)))==5 else " ")+str(int(quote.GetItemValue(i,80)/1000)),"%Y%m%d %H%M%S").replace(tzinfo=self.tz)+timedelta(hours=8),
                    'Ask':iff(quote.GetItemValue(i,81),10000000000),
                    'Ask1':iff(quote.GetItemValue(i,82),10000000000),
                    'Ask2':iff(quote.GetItemValue(i,83),10000000000),
                    'Ask3':iff(quote.GetItemValue(i,84),10000000000),
                    'Ask4':iff(quote.GetItemValue(i,85),10000000000),
                    'Ask5':iff(quote.GetItemValue(i,86),10000000000),
                    'Ask6':iff(quote.GetItemValue(i,87),10000000000),
                    'Ask7':iff(quote.GetItemValue(i,88),10000000000),
                    'Ask8':iff(quote.GetItemValue(i,89),10000000000),
                    'Ask9':iff(quote.GetItemValue(i,90),10000000000),
                    'AskVolume':iff(quote.GetItemValue(i,91)),
                    'AskVolume1':iff(quote.GetItemValue(i,92)),
                    'AskVolume2':iff(quote.GetItemValue(i,93)),
                    'AskVolume3':iff(quote.GetItemValue(i,94)),
                    'AskVolume4':iff(quote.GetItemValue(i,95)),
                    'AskVolume5':iff(quote.GetItemValue(i,96)),
                    'AskVolume6':iff(quote.GetItemValue(i,97)),
                    'AskVolume7':iff(quote.GetItemValue(i,98)),
                    'AskVolume8':iff(quote.GetItemValue(i,99)),
                    'AskVolume9':iff(quote.GetItemValue(i,100)),
                    'Bid_UpdateDatetime':datetime.strptime(str(quote.GetItemValue(i,101))+(" 0" if len(str(int(quote.GetItemValue(i,106)/1000)))==5 else " ")+str(int(quote.GetItemValue(i,106)/1000)),"%Y%m%d %H%M%S").replace(tzinfo=self.tz)+timedelta(hours=8),
                    'Bid1_UpdateDatetime':datetime.strptime(str(quote.GetItemValue(i,102))+(" 0" if len(str(int(quote.GetItemValue(i,107)/1000)))==5 else " ")+str(int(quote.GetItemValue(i,107)/1000)),"%Y%m%d %H%M%S").replace(tzinfo=self.tz)+timedelta(hours=8),
                    'Bid2_UpdateDatetime':datetime.strptime(str(quote.GetItemValue(i,103))+(" 0" if len(str(int(quote.GetItemValue(i,108)/1000)))==5 else " ")+str(int(quote.GetItemValue(i,108)/1000)),"%Y%m%d %H%M%S").replace(tzinfo=self.tz)+timedelta(hours=8),
                    'Bid3_UpdateDatetime':datetime.strptime(str(quote.GetItemValue(i,104))+(" 0" if len(str(int(quote.GetItemValue(i,109)/1000)))==5 else " ")+str(int(quote.GetItemValue(i,109)/1000)),"%Y%m%d %H%M%S").replace(tzinfo=self.tz)+timedelta(hours=8),
                    'Bid4_UpdateDatetime':datetime.strptime(str(quote.GetItemValue(i,105))+(" 0" if len(str(int(quote.GetItemValue(i,110)/1000)))==5 else " ")+str(int(quote.GetItemValue(i,110)/1000)),"%Y%m%d %H%M%S").replace(tzinfo=self.tz)+timedelta(hours=8),
                    'us':quote.GetItemString(i,111),
                    'us_datetime':datetime.strptime(str(quote.GetItemValue(i,123))+(" 0" if len(str(int(quote.GetItemValue(i,124)/1000)))==5 else " ")+str(int(quote.GetItemValue(i,124)/1000)),"%Y%m%d %H%M%S").replace(tzinfo=self.tz)+timedelta(hours=8),
                    'us_p':iff(quote.GetItemValue(i,125),10000000000),
                    'us_bp1':iff(quote.GetItemValue(i,126),10000000000),
                    'us_sp1':iff(quote.GetItemValue(i,127),10000000000),
                    'uf':quote.GetItemString(i,128),
                    'uf_datetime':datetime.strptime(str(quote.GetItemValue(i,140))+(" 0" if len(str(int(quote.GetItemValue(i,141)/1000)))==5 else " ")+str(int(quote.GetItemValue(i,141)/1000)),"%Y%m%d %H%M%S").replace(tzinfo=self.tz)+timedelta(hours=8),
                    'uf_p':iff(quote.GetItemValue(i,142),10000000000),
                    'uf_bp1':iff(quote.GetItemValue(i,143),10000000000),
                    'uf_sp1':iff(quote.GetItemValue(i,144),10000000000),
                    'usf':quote.GetItemString(i,145),
                    'usf_datetime':datetime.strptime(str(quote.GetItemValue(i,157))+(" 0" if len(str(int(quote.GetItemValue(i,158)/1000)))==5 else " ")+str(int(quote.GetItemValue(i,158)/1000)),"%Y%m%d %H%M%S").replace(tzinfo=self.tz)+timedelta(hours=8),
                    'usf_p':iff(quote.GetItemValue(i,159),10000000000)})
                else:
                    dogshis.append({"DateTime":datetime.strptime(str(quote.GetItemValue(i,0))+(" 0" if len(ttemp)==5 else " ")+ttemp,"%Y%m%d %H%M%S").replace(tzinfo=self.tz)+timedelta(hours=8),
                    "Symbol":quote.GetStringData("Symbol"),
                    'AnnualTradeday':iff(quote.GetItemValue(i,2),10000000000),
                    'TheoVal':iff(quote.GetItemValue(i,3),10000000000),
                    'IntVal':iff(quote.GetItemValue(i,4),10000000000),
                    'ATV':iff(quote.GetItemValue(i,5),10000000000),
                    'ExtVal':iff(quote.GetItemValue(i,6),10000000000),
                    'TV':iff(quote.GetItemValue(i,7),10000000000),
                    'IV':iff(quote.GetItemValue(i,8),10000000000),
                    'Last':iff(quote.GetItemValue(i,28),10000000000),
                    #'sta':iff(quote.GetItemValue(i,32) ,
                    'CSkew':iff(quote.GetItemValue(i,33),10000000000),
                    'PSkew':iff(quote.GetItemValue(i,34),10000000000),
                    'CIV25D':iff(quote.GetItemValue(i,35),10000000000),
                    'PIV25D':iff(quote.GetItemValue(i,36),10000000000),
                    'CIV10D':iff(quote.GetItemValue(i,37),10000000000),
                    'PIV10D':iff(quote.GetItemValue(i,38),10000000000),
                    'CallVol':iff(quote.GetItemValue(i,39)),
                    'PutVol':iff(quote.GetItemValue(i,40)),
                    'CallOI':iff(quote.GetItemValue(i,41)),
                    'PutOI':iff(quote.GetItemValue(i,42)),
                    "CKUpCnt": iff(quote.GetItemValue(i,43)),
                    "CKUpVol": iff(quote.GetItemValue(i,44)),
                    "CKDnCnt": iff(quote.GetItemValue(i,45)),
                    "CKDnVol": iff(quote.GetItemValue(i,46)),
                    "PKUpCnt": iff(quote.GetItemValue(i,47)),
                    "PKUpVol": iff(quote.GetItemValue(i,48)),
                    "PKDnCnt": iff(quote.GetItemValue(i,49)),
                    "PKDnVol": iff(quote.GetItemValue(i,50))})

            self.ongreekshistory(DataType,quote.GetStringData("Symbol"),quote.GetValueData("StartTime"),quote.GetValueData("EndTime"),dogshis)
            self.quoteapi.unsubquote( DataType,quote.GetStringData("Symbol"),quote.GetValueData("StartTime"),quote.GetValueData("EndTime"))
        elif DataType==2:
            #print("OnQuoteData",quote,quote.Symbol," ",quote.StartTime," ",quote.EndTime," ",quote.SecurityType," ",quote.ItemCount)
            his=[]
            datacout=quote.ItemCount
            item= client.Dispatch('{36180946-1A4F-43F0-8621-E232E6A78ED4}')
            for i in range(datacout):
                if quote.GetItem(i,item):
                    his.append({"DateTime":datetime.strptime(str(item.Date)+(" 0" if len(str(item.FilledTime))==5 else " ")+str(item.FilledTime),"%Y%m%d %H%M%S").replace(tzinfo=self.tz)+timedelta(hours=8),
                        "Symbol":quote.Symbol,
                        "Ask":iff(item.Ask,10000000000),
                        "Bid":iff(item.Bid,10000000000),
                        "Last":iff(item.TradingPrice,10000000000),
                        "Quantity":iff(item.TradeQuantity),
                        "Volume":iff(item.TradeVolume),
                        "OpenInterest":iff(item.GetItemValue("OI"))})
            self.onquotehistory(DataType,quote.Symbol,quote.StartTime,quote.EndTime,his)
            self.quoteapi.unsubquote(DataType,quote.Symbol,quote.StartTime,quote.EndTime)
        elif DataType==4 or DataType==5:
            his=[]
            #print("OnQuoteData",quote,quote.Symbol," ",quote.StartTime," ",quote.EndTime," ",quote.DataType," ",quote.ItemCount)
            datacout=quote.ItemCount
            item= client.Dispatch('{9BF97ED8-6C16-4EEF-AA9B-E98357769308}')
            for i in range(datacout):
                if quote.GetItem(i,item):
                    if DataType==5:
                        t=70000
                    else:
                        t=item.Time
                    his.append({"DateTime":datetime.strptime(str(item.Date)+(" 0" if len(str(t))==5 else " ")+str(t),"%Y%m%d %H%M%S").replace(tzinfo=self.tz)+timedelta(hours=8),
                        "Symbol":quote.Symbol,
                        "Open":iff(item.Open,10000000000),
                        "High":iff(item.High,10000000000),
                        "Low":iff(item.Low,10000000000),
                        "Close":iff(item.Close,10000000000),
                        "Volume":iff(item.Volume),
                        "OpenInterest":iff(item.GetOptValue("OI")),
                        "DownTick":item.DownTick,
                        "DownVolume":item.DownVolume,
                        "UnchVolume":item.UnchVolume,
                        "UpTick":item.UpTick,
                        "UpVolume":item.UpVolume})
            self.onquotehistory(DataType,quote.Symbol,quote.StartTime,quote.EndTime,his)
            self.quoteapi.unsubquote(DataType,quote.Symbol,quote.StartTime,quote.EndTime)
        elif DataType==9 or DataType==19:   #GREEKS 1K:9 DK:19
            greekshis=[]
            #print("OnQuoteData",quote,quote.Symbol," ",quote.StartTime," ",quote.EndTime," ",quote.DataType," ",quote.ItemCount)
            datacout=quote.ItemCount
            item= client.Dispatch('{9BF97ED8-6C16-4EEF-AA9B-E98357769308}')
            for i in range(datacout):
                if quote.GetItem(i,item):
                    if "TC.F" in quote.Symbol:
                        greekshis.append({"DateTime":datetime.strptime(str(item.Date)+(" 0" if len(str(item.Time))==5 else " ")+str(item.Time),"%Y%m%d %H%M%S").replace(tzinfo=self.tz)+timedelta(hours=8),
                            'Symbol':quote.Symbol,
                        "CTR":iff(item.GetOptValue("CTR"),10000000000),
                        "PTR":iff(item.GetOptValue("PTR"),10000000000),
                        "RCTR":iff(item.GetOptValue("RCTR"),10000000000),
                        "RPTR":iff(item.GetOptValue("RPTR"),10000000000),
                        "FCIV25":iff(item.GetOptValue("25FCIV"),10000000000),
                        "FPIV25":iff(item.GetOptValue("25FPIV"),10000000000),
                        "ExtVal": iff(item.GetOptValue("ExtVal"),10000000000),
                        "TV":iff(item.GetOptValue("TV"),10000000000),
                        "ATV":iff(item.GetOptValue("ATV"),10000000000),
                        "HV_W4": iff(item.GetOptValue("HV_W4"),10000000000),
                        "HV_W8": iff(item.GetOptValue("HV_W8"),10000000000),
                        "HV_W13": iff(item.GetOptValue("HV_W13"),10000000000),
                        "HV_W26": iff(item.GetOptValue("HV_W26"),10000000000),
                        "HV_W52": iff(item.GetOptValue("HV_W52"),10000000000),
                        "PutD":iff(item.GetOptValue("Putd"),10000000000),
                        "CallD":iff(item.GetOptValue("Calld"),10000000000),
                        "D25CStraddle":iff(item.GetOptValue("25DCStraddle"),10000000000),
                        "D25PStraddle":iff(item.GetOptValue("25DPStraddle"),10000000000),
                        "D25CTV":iff(item.GetOptValue("25DCTV"),10000000000),
                        "D25PTV":iff(item.GetOptValue("25DPTV"),10000000000),
                        "FIV":iff(item.GetOptValue("FIV"),10000000000),
                        "IV":iff(item.GetOptValue("Volatility"),10000000000),
                        "Straddle":iff(item.GetOptValue("Straddle")),
                        "StraddleStrike":iff(item.GetOptValue("StraddleStrike"),10000000000),
                        "StraddleWeight":iff(item.GetOptValue("StraddleWeight"),10000000000),
                        "CIV25D":iff(item.GetOptValue("25DCIV"),10000000000),
                        "PIV25D":iff(item.GetOptValue("25DPIV"),10000000000),
                        "CIV10D":iff(item.GetOptValue("10DCIV"),10000000000),
                        "PIV10D":iff(item.GetOptValue("10DPIV"),10000000000),
                        "VIX": iff(item.GetOptValue("VIX"),10000000000)})
                    else:
                        greekshis.append({"DateTime":datetime.strptime(str(item.Date)+(" 0" if len(str(item.Time))==5 else " ")+str(item.Time),"%Y%m%d %H%M%S").replace(tzinfo=self.tz)+timedelta(hours=8),
                            'Symbol':quote.Symbol,
                        # 'Bid': iff(item.GetOptValue("Bid"),10000000000), 
                        # 'Mid':iff(item.GetOptValue("Mid"),10000000000), 
                        # 'MIV':iff(item.GetOptValue("MIV"),10000000000), 
                        'Delta':iff(item.GetOptValue("Delta"),10000000000),
                        'Gamma':iff(item.GetOptValue("Gamma"),10000000000), 
                        'Rho':iff(item.GetOptValue("Rho"),10000000000), 
                        'Theta':iff(item.GetOptValue("Theta"),10000000000),  
                        'Vega':iff(item.GetOptValue("Vega"),10000000000), 
                        'TV':iff(item.GetOptValue("TV"),10000000000),
                        'ATV':iff(item.GetOptValue("ATV"),10000000000),
                        "IV":iff(item.GetOptValue("Volatility"),10000000000),
                        'CPIV':iff(item.GetOptValue("CPIV"),10000000000)})
            self.ongreekshistory(DataType,quote.Symbol,quote.StartTime,quote.EndTime,greekshis)
            self.quoteapi.unsubquote(DataType,quote.Symbol,quote.StartTime,quote.EndTime)

        elif DataType==10: #GREEKS TICKS:10
            greekshis=[]
            #print("OnQuoteData",quote,quote.Symbol," ",quote.StartTime," ",quote.EndTime," ",quote.SecurityType," ",quote.ItemCount)
            datacout=quote.ItemCount
            item= client.Dispatch('{36180946-1A4F-43F0-8621-E232E6A78ED4}')
            for i in range(datacout):
                if quote.GetItem(i,item):
                    if "TC.F" in quote.Symbol:
                        greekshis.append({"DateTime":datetime.strptime(str(item.Date)+(" 0" if len(str(item.GetItemValue("TradingHours")))==5 else " ")+str(item.GetItemValue("TradingHours")),"%Y%m%d %H%M%S").replace(tzinfo=self.tz)+timedelta(hours=8),
                            'Symbol':quote.Symbol,
                        "CTR":iff(item.GetItemValue("CTR"),10000000000),
                        "PTR":iff(item.GetItemValue("PTR"),10000000000),
                        "RCTR":iff(item.GetItemValue("RCTR"),10000000000),
                        "RPTR":iff(item.GetItemValue("RPTR"),10000000000),
                        "FCIV25":iff(item.GetItemValue("25FCIV"),10000000000),
                        "FPIV25":iff(item.GetItemValue("25FPIV"),10000000000),
                        "ExtVal": iff(item.GetItemValue("ExtVal"),10000000000),
                        "TV":iff(item.GetItemValue("TV"),10000000000),
                        "ATV":iff(item.GetItemValue("ATV"),10000000000),
                        "HV_W4": iff(item.GetItemValue("HV_W4"),10000000000),
                        "HV_W8": iff(item.GetItemValue("HV_W8"),10000000000),
                        "HV_W13": iff(item.GetItemValue("HV_W13"),10000000000),
                        "HV_W26": iff(item.GetItemValue("HV_W26"),10000000000),
                        "HV_W52": iff(item.GetItemValue("HV_W52"),10000000000),
                        "PutD":iff(item.GetItemValue("Putd"),10000000000),
                        "CallD":iff(item.GetItemValue("Calld"),10000000000),
                        "D25CStraddle":iff(item.GetItemValue("25DCStraddle"),10000000000),
                        "D25PStraddle":iff(item.GetItemValue("25DPStraddle"),10000000000),
                        "D25CTV":iff(item.GetItemValue("25DCTV"),10000000000),
                        "D25PTV":iff(item.GetItemValue("25DPTV"),10000000000),
                        "FIV":iff(item.GetItemValue("FIV"),10000000000),
                        "IV":iff(item.GetItemValue("Volatility"),10000000000),
                        "Straddle":iff(item.GetItemValue("Straddle"),10000000000),
                        "StraddleStrike":iff(item.GetItemValue("StraddleStrike"),10000000000),
                        "StraddleWeight":iff(item.GetItemValue("StraddleWeight"),10000000000),
                        "CIV25D":iff(item.GetItemValue("25DCIV"),10000000000),
                        "PIV25D":iff(item.GetItemValue("25DPIV"),10000000000),
                        "CIV10D":iff(item.GetItemValue("10DCIV"),10000000000),
                        "PIV10D":iff(item.GetItemValue("10DPIV"),10000000000),
                        "VIX": iff(item.GetItemValue("VIX"),10000000000)})
                    else:
                        greekshis.append({"DateTime":datetime.strptime(str(item.Date)+(" 0" if len(str(item.GetItemValue("TradingHours")))==5 else " ")+str(item.GetItemValue("TradingHours")),"%Y%m%d %H%M%S").replace(tzinfo=self.tz)+timedelta(hours=8),
                            'Symbol':quote.Symbol,
                        # 'Bid': iff(item.GetItemValue("Bid"),10000000000), 
                        # 'Mid':iff(item.GetItemValue("Mid"),10000000000), 
                        # 'MIV':iff(item.GetItemValue("MIV"),10000000000), 
                        'Delta':iff(item.GetItemValue("Delta"),10000000000),
                        'Gamma':iff(item.GetItemValue("Gamma"),10000000000), 
                        'Rho':iff(item.GetItemValue("Rho"),10000000000), 
                        'Theta':iff(item.GetItemValue("Theta"),10000000000),  
                        'Vega':iff(item.GetItemValue("Vega"),10000000000), 
                        'TV':iff(item.GetItemValue("TV"),10000000000), 
                        'ATV':iff(item.GetItemValue("ATV"),10000000000),
                        "IV":iff(item.GetItemValue("Volatility"),10000000000),
                        'CPIV':iff(item.GetItemValue("CPIV"),10000000000)})
            self.ongreekshistory(DataType,quote.Symbol,quote.StartTime,quote.EndTime,greekshis)
            self.quoteapi.unsubquote(DataType,quote.Symbol,quote.StartTime,quote.EndTime)
    
    def OnSetTopic(self, strTopic, lParam, strParam, pvParam):
        if os.path.exists(pvParam):
            with open(pvParam.replace('\\','/'),'rb+') as symblist:
                sym=json.load(symblist,encoding="utf-8")
                self.onsymbolhistory(strParam,lParam,sym)  
        else:
            print("无法获取到历史合约，请确认账户是否有dogs权限")
        self.quoteapi.topicunsub("ICECREAM.RETURN")
    def OnServerTimeDiff(self, TimeDiff):
        self.ontimediff(TimeDiff)
    def OnSymbolClassificationsUpdate(self):
        self.symbollistready=True
    def OnHotMonthUpdate(self):
        self.hotmonthready=True
    def OnSymbolLookupUpdate(self):
        self.symblookready=True
    def OnInstrumentInfoUpdate(self):
        self.symbinfoready=True
class QuoteClass:
    def __init__(self,extendevent):
        #pythoncom.CoInitialize()
        pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
        obj = client.Dispatch("{A9728003-7B76-47BF-9F13-5D4102534292}")#clsctx=pythoncom.CLSCTX_ALL
        self.eventobj=client.WithEvents(obj, BaseEvents)
        self.eventobj.quoteapi=self
        self.eventobj.extendevent=extendevent
        self.cookie = Git.RegisterInterfaceInGlobal(obj, pythoncom.IID_IDispatch)
        self.tz = pytz.timezone('Etc/GMT+8')
    def connect(self,appid:str,servicekey:str):
        try:
            pythoncom.CoInitialize()
            disp = Git.GetInterfaceFromGlobal(self.cookie, pythoncom.IID_IDispatch)
            interp = client.Dispatch(disp)
            interp.Connect(".", appid, servicekey, 1)
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

    def subquote(self,datatype:int,symbol:str,startime:int,endtime:int):#"-1" :超過上限 "-10" 無報價權限
        if "TC.O" in symbol:
            greeksType = "REAL"
        else:
            greeksType = "Volatility"
        if datatype!=6:
            greeksType =""
        try:
            pythoncom.CoInitialize()
            disp = Git.GetInterfaceFromGlobal(self.cookie, pythoncom.IID_IDispatch)
            interp = client.Dispatch(disp)
            arg= client.Dispatch('{DD6AF848-6BA8-4F05-8570-059A3FDC962A}')
            arg.Symbol =symbol 
            arg.SecurityType = 9
            arg.StartTime =startime
            arg.EndTime =endtime
            arg.GreeksType=greeksType
            #arg1.ExtParam="ExtendGreeks=0"
            return interp.SubQuote(datatype,arg)
        except pythoncom.com_error as e:
            print("订阅错误：",e)

    def unsubquote(self,datatype:int,symbol:str,startime:int,endtime:int):
        if "TC.O" in symbol:
            greeksType = "REAL"
        else:
            greeksType = "Volatility"
        if datatype!=6:
            greeksType =""
        try:
            pythoncom.CoInitialize()
            disp = Git.GetInterfaceFromGlobal(self.cookie, pythoncom.IID_IDispatch)
            interp = client.Dispatch(disp)
            arg= client.Dispatch('{DD6AF848-6BA8-4F05-8570-059A3FDC962A}')
            arg.Symbol =symbol 
            arg.SecurityType = 6
            arg.StartTime =startime
            arg.EndTime =endtime
            arg.GreeksType=greeksType 
            return interp.UnsubQuote(datatype,arg)
        except pythoncom.com_error as e:
            print("订阅错误：",e)

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

    def getsymbol_ticksize(self,symbol:str):
        return self._getsymbolInfo("2",symbol)
    def getsymbol_session(self,symbol:str):
        return self._getsymbolInfo("3",symbol)
    def getsymbolvolume_multiple(self,symbol:str):
        return self._getsymbolInfo("6",symbol)
    def getsymbol_id(self,symbol:str):
        return self._getsymbolInfo("Instrument",symbol)
    def getsymbol_allinfo(self,symbol:str):
        return self._getsymbolInfo("ALL",symbol)
    def _getsymbolInfo(self,strType:str, symbol:str):
        try:
            pythoncom.CoInitialize()
            disp = Git.GetInterfaceFromGlobal(self.cookie, pythoncom.IID_IDispatch)
            interp = client.Dispatch(disp)
            return interp.GetInstrumentInfo(strType, symbol)
        except pythoncom.com_error as e:
            print("getsymbolInfo错误:",e)

    def getsymbolname(self, Keyword):
        try:
            pythoncom.CoInitialize()
            disp = Git.GetInterfaceFromGlobal(self.cookie, pythoncom.IID_IDispatch)
            interp = client.Dispatch(disp)
            interp.GetSymbolName(Keyword)
        except pythoncom.com_error as e:
            print("getsymbolName错误:",e)
            
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

    def subsymbolhistory(self,symboltype:str,dt:str):
        self.topicsub("ICECREAM.RETURN")
        self.topicpublish ("ICECREAM.RECOVER",int(dt), symboltype,None)#20221203, "OPT"


    def __getsymbollist(self, Classify, Exchange, Symbol, Month, CallPut):
        try:
            pythoncom.CoInitialize()
            disp = Git.GetInterfaceFromGlobal(self.cookie, pythoncom.IID_IDispatch)
            interp = client.Dispatch(disp)
            return interp.GetSymbolClassifications(Classify, Exchange, Symbol, Month, CallPut)
        except pythoncom.com_error as e:
            print("getsymbol错误:",e)

    def symbollookup(self, SymbolType, Keyword):
        try:
            pythoncom.CoInitialize()
            disp = Git.GetInterfaceFromGlobal(self.cookie, pythoncom.IID_IDispatch)
            interp = client.Dispatch(disp)
            return interp.SymbolLookup(SymbolType, Keyword)
        except pythoncom.com_error as e:
            print("symbollookup错误:",e)

    def isholiday(self, bstrDate, bstrSymbol):
        try:
            pythoncom.CoInitialize()
            disp = Git.GetInterfaceFromGlobal(self.cookie, pythoncom.IID_IDispatch)
            interp = client.Dispatch(disp)
            return interp.isHoliday(bstrDate, bstrSymbol)
        except pythoncom.com_error as e:
            print("isholiday错误:",e)

    def isunderlying(self, bstrSymbol):
        try:
            pythoncom.CoInitialize()
            disp = Git.GetInterfaceFromGlobal(self.cookie, pythoncom.IID_IDispatch)
            interp = client.Dispatch(disp)
            return interp.isUnderlying(bstrSymbol)
        except pythoncom.com_error as e:
            print("isunderlying错误:",e)

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
            print("topicunsub错误:",e)

    def getgeneralservice(self, Key):
        try:
            pythoncom.CoInitialize()
            disp = Git.GetInterfaceFromGlobal(self.cookie, pythoncom.IID_IDispatch)
            interp = client.Dispatch(disp)
            return interp.GetGeneralService(Key)
        except pythoncom.com_error as e:
            print("getgeneralservice错误:",e)

    # def join(self):
    #     pythoncom.PumpMessages()      
