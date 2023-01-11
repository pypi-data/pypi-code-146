# -*- coding: utf-8 -*-
"""
本模块功能：期权定价趋势分析，仅限于中国大陆的期权产品
所属工具包：证券投资分析工具SIAT 
SIAT：Security Investment Analysis Tool
创建日期：2020年7月16日
最新修订日期：2020年8月5日
作者：王德宏 (WANG Dehong, Peter)
作者单位：北京外国语大学国际商学院
作者邮件：wdehong2000@163.com
版权所有：王德宏
用途限制：仅限研究与教学使用，不可商用！商用需要额外授权。
特别声明：作者不对使用本工具进行证券投资导致的任何损益负责！
"""
#==============================================================================
#关闭所有警告
import warnings; warnings.filterwarnings('ignore')
#==============================================================================

from siat.common import *
from siat.grafix import *
from siat.security_prices import *
from siat.option_pricing import *
from siat.fama_french import *

import pandas as pd
#==============================================================================
if __name__=='__main__':
    symbol='黄金期权'

def option_comm_dict_china(symbol="玉米期权"):
    """
    获取中国商品期权大类合约
    显示symbol类期权的可用合约列表
    """
    import akshare as ak
    import datetime
    today = datetime.date.today()
    
    try:
        #optiondict=ak.option_sina_commodity_dict(symbol=symbol)
        optiondict=ak.option_commodity_contract_sina(symbol=symbol)
        print("\n中国"+symbol+"的可用合约：")
        #contractlist=optiondict[symbol]
        contractlist=list(optiondict['合约'])
        contractlist.sort(reverse=False)
        #print(contractlist)
        printlist(contractlist,numperline=8,beforehand=' '*4,separator=' ')
        print('*** 注：合约代码后四位数字为合约到期日YYMM')
        print('    每种合约还将分为看涨(C)/看跌(P)两个方向和不同的行权价')
        print('    数据来源：新浪财经,',today)
        return optiondict
    except:
        print("  #Error(option_com_china): failed to get dict info for",symbol)
        print("  Solution: upgrade siat and akshare plug-in, then try again")
        print("  If problem remains, report to the author via wechat or email.")
        return None    

if __name__=='__main__':
    df=option_comm_dict_china(symbol='黄金期权')
#==============================================================================
if __name__=='__main__':
    symbol='黄金期权'
    contract='au2212'
    printout=True
    graph=True
    
def option_comm_china(symbol='',contract='',printout=True,graph=True):
    """
    获取中国商品期权大类
    若symbol=''或错误且contract=''时显示中国商品期权大类
    若symbol查到且contract=''或未查到时显示该类期权的合约列表
    若symbol查到且contract查到时显示该类期权合约的价格与持仓量分析
    """
    import akshare as ak
    import datetime
    today = datetime.date.today()
    
    symbollist=['豆粕期权','玉米期权','铁矿石期权','棉花期权','白糖期权','PTA期权', \
                '甲醇期权','橡胶期权','沪铜期权','黄金期权','菜籽粕期权', \
                    '液化石油气期权','动力煤期权']
    if not (symbol in symbollist):
        print("\n中国商品期权的常见品种：")
        #print(symbollist)
        printlist(symbollist,numperline=6,beforehand=' '*4,separator=' ')
        print('*** 数据来源：新浪财经,',today)
        return symbollist
    
    #symbol=underlying+'期权'
    if (symbol in symbollist) and (contract==''):
        optiondict=option_comm_dict_china(symbol)
        return optiondict
        
    try:
        df2=ak.option_commodity_contract_table_sina(symbol=symbol,contract=contract)
    except:
        print("  #Error(option_com_china): contract",contract,'not found in',symbol)
        optiondict=option_comm_dict_china(symbol)
        return optiondict 
    
    #df2cols=['买量C','买价C','最新价C','卖价C','卖量C','持仓量C','涨跌C','行权价','看涨期权合约','买量P','买价P','最新价P','卖价P','卖量P','持仓量P','涨跌P','看跌期权合约']
    df2cols=['看涨合约-买量','看涨合约-买价','看涨合约-最新价','看涨合约-卖价', \
             '看涨合约-卖量','看涨合约-持仓量','看涨合约-涨跌','行权价', \
             '看涨合约-看涨期权合约', \
             '看跌合约-买量','看跌合约-买价','看跌合约-最新价','看跌合约-卖价', \
             '看跌合约-卖量','看跌合约-持仓量','看跌合约-涨跌','看跌合约-看跌期权合约']
    df2.columns=df2cols

    df2['最新价C']=df2['看涨合约-最新价'].astype('float')
    df2['持仓量C']=df2['看涨合约-持仓量'].astype('float')
    df2['最新价P']=df2['看跌合约-最新价'].astype('float')
    df2['持仓量P']=df2['看跌合约-持仓量'].astype('float')
    df2['行权价']=df2['行权价'].astype('float')
    
    df2['看涨期权合约']=df2['看涨合约-看涨期权合约']   
    df2['看跌期权合约']=df2['看跌合约-看跌期权合约']
    
    df2.set_index('行权价',inplace=True)
    
    if printout:
        df2c=df2['看涨期权合约']
        df2c.dropna(inplace=True)
        df2clist=list(df2c)
        print("  \n中国"+symbol+contract+"的看涨期权合约：")
        printlist(df2clist,numperline=6,beforehand=' '*4,separator=' ')
        df2p=df2['看跌期权合约']
        df2p.dropna(inplace=True)
        df2plist=list(df2p)
        print("  \n中国"+symbol+contract+"的看跌期权合约：")  
        printlist(df2plist,numperline=6,beforehand=' '*4,separator=' ')

    if printout & graph:
        footnote="行权价-->\n\n"+"数据来源：新浪财经，"+str(today)
    
        print("\nRendering graphics for the relationships btw contract and strike prices...")
        titletxt="当前期权价格与行权价的关系："+symbol+contract
        plot_line2(df2,"看涨期权",'最新价C','价格', \
                   df2,"看跌期权",'最新价P','价格', \
                   '价格',titletxt,footnote,power=0,twinx=False)
    """
    print("Rendering graphics for the relationships btw call price and open interest ...")
    titletxt="当前期权价格与持仓量的关系："+symbol+contract+'的'+"看涨期权"
    plot_line2(df2,"看涨期权",'最新价C','价格', \
                 df2,"看涨期权",'持仓量C','持仓量', \
                 '',titletxt,footnote,power=0,twinx=True)

    print("Rendering graphics for the relationships btw put price and open interest ...")
    titletxt="当前期权价格与持仓量的关系："+symbol+contract+'的'+"看跌期权"
    plot_line2(df2,"看跌期权",'最新价P','价格', \
                 df2,"看跌期权",'持仓量P','持仓量', \
                 '',titletxt,footnote,power=0,twinx=True)

    print("Rendering graphics for the relationships btw open interests ...")
    titletxt="当前期权方向与持仓量的关系："+symbol+contract
    plot_line2(df2,"看涨期权",'持仓量C','持仓量', \
                 df2,"看跌期权",'持仓量P','持仓量', \
                 '',titletxt,footnote,power=0,twinx=False)
    """
    return df2
#==============================================================================


def check_contract(contract):
    """
    功能：检查新浪期权数据中一项合约是否存在
    """
    # 太啰嗦了，暂时不做了
    
#==============================================================================
if __name__=='__main__':
    contract='au2212C324'
    contract='pg2212C3850'
    contract=['au2212C324','au2212P324']
    contract=[]
    power=0
    twinx=False
    start='2022-7-1'
    end='2022-11-6'

def option_comm_trend_china(contract,start='',end='',power=0, \
                            twinx=False,loc1='best',loc2='best'):
    """
    绘制期权合约价格历史价格趋势图
    若contract为一个合约，则绘制单折线图
    若contract为多于一个合约，则绘制前两个合约的双单折线图
    """
    
    contract1=contract2=''
    if isinstance(contract,str):
        contract1=contract
        contract2=''
    
    if isinstance(contract,list):
        if len(contract)==1:
            contract1=contract
            contract2=''    
        elif len(contract)>=2:
            contract1=contract[0]
            contract2=contract[1]    
            
    if contract1=='':
        print("  #Error(option_comm_trend_china): unknown option contract",contract)
        return None

    import pandas as pd
    start1=end1=''
    if not (start==''):
        try:
            start1=pd.to_datetime(start)
        except:
            print("  #Error(option_comm_trend_china): invalid date",start)
    if not (end==''):
        try:
            end1=pd.to_datetime(end)
        except:
            print("  #Error(option_comm_trend_china): invalid date",end)
    
    import akshare as ak
    import datetime
    today = datetime.date.today()
    footnote="数据来源：新浪财经，"+str(today)
    
    #绘制单折线
    if contract2=='':
        contract1,dict1=option_comm_contract_decode_china(contract1)
        try:
            #df3=ak.option_sina_commodity_hist(contract=contract1)
            df3=ak.option_commodity_hist_sina(symbol=contract1)
        except:
            print("  #Error(option_comm_trend_china): data unavailable for",contract1)
            print("  Possible reasons: no such contract or no tradings for the contract")
            return None
        
        if len(df3)==0:
            print("  #Warning(option_comm_trend_china): no record found for contract",contract1)
            return None            
        
        df3['date2']=pd.to_datetime(df3['date'])
        df3.set_index('date2',inplace=True)
        df3['close']=df3['close'].astype('float')
        
        if not (start1==''):
            df3=df3.drop(df3[df3.index < start1].index)
        if not (end1==''):
            df3=df3.drop(df3[df3.index > end1].index)        

        print("  Rendering graphics for option contract price trend...")
        titletxt="期权合约价格的运动趋势："+contract1
        footnote=contract1+'：'+dict1['标的物']+dict1['期权方向']+'，'+dict1['到期日']+'到期'+'，行权价'+dict1['行权价']+'\n'+footnote
        plot_line(df3,'close','收盘价','价格',titletxt,footnote,power=power)
        return df3
    
    #绘制双折线
    contract1ok=contract2ok=True
    if not (contract2==''):
        contract1,dict1=option_comm_contract_decode_china(contract1)
        try:
            df31=ak.option_commodity_hist_sina(symbol=contract1)   
            df31['date2']=pd.to_datetime(df31['date'])
            df31.set_index('date2',inplace=True)
            df31['close']=df31['close'].astype('float')
        except:
            print("  #Error(option_comm_trend_china): data unavailable for",contract1)
            print("  Possible reasons: no such contract or no tradings for the contract")
            contract1ok=False
        if contract1ok:
            if not (start1==''):
                df31=df31.drop(df31[df31.index < start1].index)
            if not (end1==''):
                df31=df31.drop(df31[df31.index > end1].index)            

            if len(df31)==0:
                #print("  #Warning(option_comm_trend_china): no record found for contract",contract1)
                contract1ok=False
        
        contract2,dict2=option_comm_contract_decode_china(contract2)
        try:
            df32=ak.option_commodity_hist_sina(symbol=contract2) 
            df32['date2']=pd.to_datetime(df32['date'])
            df32.set_index('date2',inplace=True)
            df32['close']=df32['close'].astype('float')
        except:
            print("  #Error(option_comm_trend_china): data unavailable for",contract2)
            print("  Possible reasons: no such contract or no tradings for the contract")
            contract2ok=False
        if contract2ok:
            if not (start1==''):
                df32=df32.drop(df32[df32.index < start1].index)
            if not (end1==''):
                df32=df32.drop(df32[df32.index > end1].index)   

            if len(df32)==0:
                #print("  #Warning(option_comm_trend_china): no record found for contract",contract2)
                contract2ok=False
        
        if contract1ok and contract2ok:
            print("  Rendering graphics for comparing two option contract price trends...")
            titletxt="期权价格的运动趋势对比："+contract1+'与'+contract2
            footnote=contract2+'：'+dict2['标的物']+dict2['期权方向']+'，'+dict2['到期日']+'到期'+'，行权价'+dict2['行权价']+'\n'+footnote
            footnote=contract1+'：'+dict1['标的物']+dict1['期权方向']+'，'+dict1['到期日']+'到期'+'，行权价'+dict1['行权价']+'\n'+footnote
            
            plot_line2(df31,contract1,'close','收盘价', \
                   df32,contract2,'close','收盘价', \
                       '价格',titletxt,footnote,twinx=twinx,loc1=loc1,loc2=loc2)
            return df31,df32
        elif contract1ok:
            print("  Rendering graphics for option contract price trend...")
            titletxt="期权合约价格的运动趋势："+contract1
            footnote=contract1+'：'+dict1['标的物']+dict1['期权方向']+'，'+dict1['到期日']+'到期'+'，行权价'+dict1['行权价']+'\n'+footnote
            
            plot_line(df31,'close','收盘价','价格',titletxt,footnote,power=power,loc=loc1)
            return df31            
        elif contract2ok:
            print("  Rendering graphics for option contract price trend...")
            titletxt="期权合约价格的运动趋势："+contract2
            footnote=contract2+'：'+dict2['标的物']+dict2['期权方向']+'，'+dict2['到期日']+'到期'+'，行权价'+dict2['行权价']+'\n'+footnote
            
            plot_line(df32,'close','收盘价','价格',titletxt,footnote,power=power,loc=loc1)
            return df32  
        else:
            print("  #Warning(option_comm_trend_china): no record found for contracts",contract1,'and',contract2)
            return None
        
#==============================================================================
if __name__=='__main__':
    contract='xu2112'
    contract='au2112C328'
    
def option_comm_contract_decode_china(contract):
    """
    例：
    contract='c2111'或'cf2111'
    contract='c2111C235'或'cf2111P235'
    """
    
    prelist=['m','c','i','cf','sr','ta','ma','ru','cu','au','rm','pg','zc']
    ualist=['豆粕','玉米','铁矿石','棉花','白糖','PTA','甲醇','橡胶','沪铜','黄金','菜籽粕','液化石油气','动力煤']
    
    import string
    ucletters=list(string.ascii_uppercase)    
    lcletters=list(string.ascii_lowercase)
    
    pos=0
    contract1=contract.lower()
    for c in contract1:
        if c in lcletters:
            pos=pos+1
        else:
            break
    prefix=contract1[:pos]
    yymm=contract1[pos:pos+4]
    maturity='20'+yymm[:2]+'-'+yymm[2:] #到期年月
    
    direction=''
    strike=''
    if len(contract1)>6:
        direction=contract1[pos+4:pos+5]
        direction=direction.upper()     #期权方向
        contract2=contract1[:pos+4]+direction+contract1[pos+5:]
        strike=contract1[pos+5:]        #行权价 

        if direction=='C':
            otype="看涨期权"
        elif direction=='P':
            otype="看跌期权"
        else:
            otype="未知"
    else:
        contract2=contract1
    
    try:
        pos1=prelist.index(prefix)
        ua=ualist[pos1]                 #期权标的物类别
    except:
        print("  #Error(option_comm_contract_decode_china): contract",contract,"not found")
        return None,None
    
    contract_notes={}
    contract_notes['合约']=contract2
    contract_notes['标的物']=ua
    contract_notes['到期日']=maturity
    if not (direction==''):
        contract_notes['期权方向']=otype
    if not (strike==''):
        contract_notes['行权价']=strike
    
    
    return contract2,contract_notes
#==============================================================================
#==============================================================================
# 以上为商品期权，以下为金融期权
#==============================================================================
#==============================================================================
if __name__=='__main__':
    detail=True
    detail=False
    
# 定义中国当前金融期权的所有品种   
option_fin_list=["华夏上证50ETF期权","华泰柏瑞沪深300ETF期权","嘉实沪深300ETF期权", \
                 "沪深300股指期权"]
underlying_fin_list=["510050.SS","510300.SS","159919.SZ","000300.SS"]
    
def option_fin_china(detail=False):
    """
    功能：描述当前中国市场中的金融期权，标注日期
    """
    
    if detail:
        heading="\n***"
    else:
        heading=' '
    lead_blanks=' '*3
    
    print("===== 中国金融期权表 =====")
    #华夏上证50ETF期权
    print(heading,"华夏上证50ETF期权")
    if detail:
        print(lead_blanks,"其他名称：上证50ETF期权")
        print(lead_blanks,"类别    ：欧式期权，无红利")
        print(lead_blanks,"标的证券：华夏上证50ETF基金（510050.SS）")
        #print(lead_blanks,"行权价格：1个平值合约、4个虚值合约、4个实值合约")
        print(lead_blanks,"上市日期：2015-2-9")
        print(lead_blanks,"到期月份：当月、下月及随后两个季月（季度末月）")
        print(lead_blanks,"到期日期：到期月份的第四个星期三（节假日顺延）")
        print(lead_blanks,"交易所  ：上海证券交易所")
    
    #华泰柏瑞沪深300ETF期权
    print(heading,"华泰柏瑞沪深300ETF期权")
    if detail:
        print(lead_blanks,"其他名称：上证沪深300ETF期权")
        print(lead_blanks,"类别    ：欧式期权，无红利")
        print(lead_blanks,"标的证券：华泰柏瑞沪深300ETF基金（510300.SS）")
        print(lead_blanks,"上市日期：2019-12-23")
        #print(lead_blanks,"行权价格：1个平值合约、4个虚值合约、4个实值合约")
        print(lead_blanks,"到期月份：当月、下月及随后两个季月（季度末月）")
        print(lead_blanks,"到期日期：到期月份的第四个星期三（节假日顺延）")
        print(lead_blanks,"交易所  ：上海证券交易所")   
    
    #嘉实沪深300ETF期权
    print(heading,"嘉实沪深300ETF期权")
    if detail:
        print(lead_blanks,"其他名称：深交所沪深300ETF期权")
        print(lead_blanks,"类别    ：欧式期权，无红利")
        print(lead_blanks,"标的证券：嘉实沪深300ETF基金（159919.SZ）")
        print(lead_blanks,"上市日期：2019-12-23")
        #print(lead_blanks,"行权价格：1个平值合约、4个虚值合约、4个实值合约")
        print(lead_blanks,"到期月份：1、2、3、6月")
        print(lead_blanks,"到期日期：到期月份的第四个星期三（遇法定节假日顺延）")
        print(lead_blanks,"交易所  ：深圳证券交易所")
    
    #沪深300股指期权
    print(heading,"沪深300股指期权")
    if detail:
        print(lead_blanks,"其他名称：中金所沪深300股指期权")
        print(lead_blanks,"类别    ：欧式期权，无红利")
        print(lead_blanks,"标的证券：沪深300指数（000300.SS，399300.SZ）")
        print(lead_blanks,"上市日期：2019-12-23")
        #print(lead_blanks,"行权价格：1个平值合约、4个虚值合约、4个实值合约")
        print(lead_blanks,"到期月份：当月、下2个月、随后3个季月（季度末月）")
        print(lead_blanks,"到期日期：到期月份的第三个星期五（节假日顺延）")
        print(lead_blanks,"交易所  ：中国金融期货交易所") 
    
    import datetime as dt; today=str(dt.date.today())
    print('\n',heading,"来源：上交所/深交所/中金所,",today)
    return
 
if __name__=='__main__':
    option_fin_china()
    option_fin_china(detail=True)
#==============================================================================
if __name__=='__main__':
    date='2021-11-1'

def get_yymm(date):
    
    import datetime as dt
    d=dt.datetime.strptime(date, '%Y-%m-%d')
    year=d.strftime('%Y')
    month=d.strftime('%m')
    yymm=str(year)[2:]+str(month)    
    
    return yymm

if __name__=='__main__':
    get_yymm('2020-03-25')    
#==============================================================================

if __name__=='__main__':
    start='2021-11-1'
    start=''
    num=12

def get_yymm_list(start='',num=12):
    """
    获取一个给定日期start及其后续的YYMM年月列表，共num个
    """
    
    import datetime as dt
    if start=='':
        start=str(dt.date.today())
    
    start1=dt.datetime.strptime(start, '%Y-%m-%d')
    date_list=[start1]
    
    from datetime import timedelta
    for d in range(1,num+1):
        date=start1+timedelta(days=d*30)
        date_list=date_list+[date]
    
    yymm_list=[]
    for d in date_list:
        year=d.strftime('%Y')
        month=d.strftime('%m')
        yymm=str(year)[2:]+str(month)        
        yymm_list=yymm_list+[yymm]
    
    return yymm_list

if __name__=='__main__':
    get_yymm_list()
    get_yymm_list(num=13)
    get_yymm_list('2021-1-11')
    get_yymm_list('2021-1-11',num=13)
    
#==============================================================================

if __name__=='__main__':
    symbol="华夏上证50ETF期权"
    symbol="华泰柏瑞沪深300ETF期权"
    symbol="嘉实沪深300ETF期权"
    symbol="沪深300股指期权"
    num=12
    
def option_fin_month_china(symbol,num=12):
    """
    功能：遍历并显示一个金融期货品种的到期年月YYMM
    """
    
    if not (symbol in option_fin_list):
        print("  #Warning(option_fin_month_china): info not found for",symbol)
        return None
    
    #当前年月开始的年月列表
    import datetime as dt; today=str(dt.date.today())
    yymm_list=get_yymm_list(today,num=num)
    
    import akshare as ak
    end_month_list=[]
    for yymm in yymm_list:
        #print('Scanning',yymm)
        try:
            df = ak.option_finance_board(symbol=symbol, end_month=yymm)
        except:
            continue
        else:
            if len(df)==0: continue
            
            if symbol=="华夏上证50ETF期权":
                y2m2=df['合约交易代码'][:1].values[0][7:11]
            
            if symbol=="华泰柏瑞沪深300ETF期权":
                y2m2=df['合约交易代码'][:1].values[0][7:11]
            
            if symbol=="嘉实沪深300ETF期权":
                d1=df['期权行权日'][:1].values[0]
                d2=d1.astype('str')
                yy=d2[2:4]; mm=d2[5:7]; y2m2=yy+mm
            
            if symbol=="沪深300股指期权":
                y2m2=df['instrument'][:1].values[0][2:6]                
            
            if y2m2==yymm:
                end_month_list=end_month_list+[yymm]
    
    print("\n=== 中国金融期权品种的到期日(YYMM) ===") 
    print(symbol+':')       
    print(end_month_list)

    import datetime as dt; today=str(dt.date.today())
    print("来源：上交所/深交所/中金所,",today)
    
    return
        

if __name__=='__main__':
    option_fin_month_china("华夏上证50ETF期权")
    option_fin_month_china("嘉实沪深300ETF期权")
    option_fin_month_china("华泰柏瑞沪深300ETF期权")
    option_fin_month_china("沪深300股指期权")

#==============================================================================
if __name__=='__main__':
    end_month='2112'
    nth=4 #第四个
    wd=3 #星期三

def nth_weekday(end_month,nth,wd):
    """
    功能：给定年月end_month的第nth个星期wd，求日期
    """
    import calendar
    import datetime
    c = calendar.Calendar(firstweekday=calendar.SUNDAY)
    
    myear=int('20'+end_month[:2])
    mmonth=int(end_month[2:])
    monthcal = c.monthdatescalendar(myear,mmonth)
    
    mdatelist=[]
    for mweek in monthcal:
        #print(mweek)
        for mday in mweek:
            #print(mday)
            if (mday.weekday()==(wd-1)) and (mday.month==mmonth):
                mdatelist=mdatelist+[mday]
    mdate=str(mdatelist[nth-1])
    
    return mdate

if __name__=='__main__':
    #求第四个星期三
    nth_weekday('2111',4,3)
    nth_weekday('2112',4,3)
#==============================================================================
if __name__=='__main__':
    symbol="华夏上证50ETF期权"
    symbol="华泰柏瑞沪深300ETF期权"
    symbol="嘉实沪深300ETF期权"
    symbol="沪深300股指期权"   
    end_month='2112'
    direction='call'
    printout=True
    
    
def option_fin_contracts(symbol,end_month,direction='call',printout=True):
    """
    功能：抓取指定金融期权品种和到期日年月的具体合约
    """
    
    if not (symbol in option_fin_list):
        print("  #Warning(option_fin_contracts): info not found for",symbol)
        return None
    
    import akshare as ak
    try:
        df = ak.option_finance_board(symbol=symbol, end_month=end_month)
    except:
        print("  #Error(option_fin_contracts): info unavailable for",symbol,'on maturity',end_month)
        return None
    
    #检查期权方向
    typelist=['CALL','PUT','BOTH']
    utype=direction.upper()
    if not (utype in typelist):
        print("  #Warning(option_fin_contracts): unsupported option direction",direction)
        print("  Supported option direction:",typelist)
        return None
    
    import pandas as pd
    contracts=pd.DataFrame()
    #==================================================================
    if symbol in ["华夏上证50ETF期权","华泰柏瑞沪深300ETF期权"]:
        #期权方向标志
        df['direction']=df['合约交易代码'].apply(lambda x:x[6:7])
        if utype=='CALL':
            df1=df[df['direction']=='C']
        elif utype=='PUT':
            df1=df[df['direction']=='P']
        else:
            df1=df
        
        #取交易日期
        df1['date']=df1.index[0][:8]
        contracts['date']=pd.to_datetime(df1['date'])
        
        #去掉前后空格
        df1['合约交易代码']=df1['合约交易代码'].apply(lambda x: x.strip())
        contracts['contract']=df1['合约交易代码']
        
        contracts['name']=contracts['contract']
        contracts['direction']=df1['direction']
        #contracts['Close']=df1['前结价']
        contracts['Strike']=df1['行权价']
        
        #到期日：到期月的第四个星期三
        mdate=nth_weekday(end_month,4,3)
        contracts['maturity']=mdate
        
        #标的物
        pos=option_fin_list.index(symbol)
        ua=underlying_fin_list[pos]
        contracts['underlying']=ua
        
    #=================================================================
    if symbol in ["嘉实沪深300ETF期权"]:
        #期权方向标志
        df['direction']=df['类型'].apply(lambda x:'C' if x in ["认购"] else 'P')
        if utype=='CALL':
            df1=df[df['direction']=='C']
        elif utype=='PUT':
            df1=df[df['direction']=='P']
        else:
            df1=df
        
        #去掉前后空格
        df1['合约编码']=df1['合约编码'].apply(lambda x: str(x).strip())
        contracts['contract']=df1['合约编码']
        
        contracts['name']=df1['合约简称']
        contracts['direction']=df1['direction']
        #????contracts['Close']=df1['前结价']
        try:
            contracts['Strike']=df1['行权价']
        except:
            contracts['Strike']=df1['行权价(元)']
        
        #行权日
        contracts['maturity']=df1['期权行权日'].apply(lambda x: x.strftime('%Y-%m-%d'))
        
        #标的物
        pos=option_fin_list.index(symbol)
        ua=underlying_fin_list[pos]
        contracts['underlying']=ua
        
        #取交易日期
        import datetime as dt; today=str(dt.date.today())
        contracts['date']=pd.to_datetime(today)
        
    #=================================================================
    if symbol in ["沪深300股指期权"]:
        """
        字段解读：
        instrument:合约编号
        position:持仓量
        volume:成交量
        lastprice:最新价
        updown:涨跌，涨跌=最新价-前结算价
        bprice:买价
        bamount:买量
        sprice:卖价
        samount:卖量
        """
        #期权方向标志
        df['direction']=df['instrument'].apply(lambda x:x[7:8])
        if utype=='CALL':
            df1=df[df['direction']=='C']
        elif utype=='PUT':
            df1=df[df['direction']=='P']
        else:
            df1=df
        
        #去掉前后空格
        df1['instrument']=df1['instrument'].apply(lambda x: x.strip())
        contracts['contract']=df1['instrument']
        
        contracts['name']=df1['instrument']
        contracts['direction']=df1['direction']
        #????contracts['Close']=df1['前结价']
        contracts['Strike']=df1['instrument'].apply(lambda x:x[9:13]).astype('int')
        
        #行权日:到期月份第三周的周三
        mdate=nth_weekday(end_month,3,3)
        #contracts['maturity']='20'+df1['instrument'].apply(lambda x:x[2:6])+'28'
        contracts['maturity']=mdate
        
        #标的物
        pos=option_fin_list.index(symbol)
        ua=underlying_fin_list[pos]
        contracts['underlying']=ua
        
        #取交易日期
        import datetime as dt; today=str(dt.date.today())
        contracts['date']=pd.to_datetime(today)
        
    contracts['Option']=symbol
    contracts['end_month']=end_month
    contracts.set_index('date',inplace=True)
    contracts.sort_values(by=['Strike'],ascending=True,inplace=True)
    
    #打印
    if printout:
        print("\n========= 中国金融期权合约 =========\n")
        print("期权品种：",symbol)
        print("到期年月：",end_month)
        print("合约方向：",utype)
        
        #改换中文字段栏
        collist=['contract','direction','maturity','underlying','Strike']
        collistcn=['期权合约','方向','到期日','标的证券','行权价']
        printdf=contracts[collist].copy()
        printdf.columns=collistcn
        
        #打印对齐
        pd.set_option('display.unicode.ambiguous_as_wide', True)
        pd.set_option('display.unicode.east_asian_width', True)
        pd.set_option('display.width', 180) # 设置打印宽度(**重要**)
        
        print(printdf.to_string(index=False))        
        
        import datetime as dt; today=str(dt.date.today())
        print("\n来源：新浪/上交所/深交所/中金所,",today)

    return contracts    
        
if __name__=='__main__': 
    symbol="华夏上证50ETF期权"
    symbol="华泰柏瑞沪深300ETF期权"
    symbol="嘉实沪深300ETF期权"
    symbol="沪深300股指期权"   
    end_month='2112'
    direction='call'       
    df=option_fin_contracts(symbol,end_month,direction='call')        

#==============================================================================
if __name__=='__main__':
    symbol="华夏上证50ETF期权"
    symbol="华泰柏瑞沪深300ETF期权"
    symbol="嘉实沪深300ETF期权"
    symbol="沪深300股指期权"   
    
    contract='510050C2206M02900'
    contract='90000871'
    end_month='2206'
    direction='call'
    
def option_fin_contract_parms(symbol,end_month,contract,direction='call'):
    """
    功能：抓取期权合约的到期日、行权价和标的证券
    """
    
    df=option_fin_contracts(symbol=symbol,end_month=end_month, \
            direction=direction,printout=False)
    
    df1=df[df['contract']==contract]
    if len(df1)==0:
        print("  #Warning(option_fin_contract_parms): contract not found for",contract)
        return None,None,None

    underlying=df1['underlying'].values[0]
    maturity=df1['maturity'].values[0]
    strike=float(df1['Strike'].values[0])
    
    return underlying,maturity,strike

if __name__=='__main__':
    option_fin_contract_parms("华夏上证50ETF期权",'2206','510050C2206M02900',direction='call')
#=============================================================================
if __name__=='__main__': 
    underlying='510050.SS'
    date='2021-11-19'
    days=30

def underlying_sigma(underlying,date,days=30):
    """
    功能：计算标的物价格的年化标准差
    underlying：标的证券代码
    date：当前日期
    days：历史期间长度，日历日天数，默认30个日历日
    """
    
    #年度交易日天数
    annual_trading_days=252
    
    #计算历史样本的开始日期
    import pandas as pd
    try:
        end=pd.to_datetime(date)
    except:
        print("  #Error(annualized_sigma): invalid date",date)
        return None,None
    
    from datetime import timedelta
    start=end-timedelta(days=days+1)
    start1=start.strftime('%Y-%m-%d')
    
    #抓取标的物的历史价格样本
    """
    try:
        df=get_prices(underlying,start1,date)
    except:
        print("  #Error(annualized_sigma): failed to retrieve info for",underlying)
        return None,None   
    """
    df=get_prices(underlying,start1,date)
    #标的物当前价格
    s0=df[-1:]['Close'].values[0]

    """
    #采用算数收益率
    df['ret']=df['Close'].pct_change()
    """
    
    #采用对数收益率
    df['Close_lag']=df['Close'].shift(1)
    df.dropna(inplace=True)
    import numpy as np
    df['ret']=np.log(df['Close']/df['Close_lag'])
    sigma=df['ret'].std()
    annualized_sigma=sigma*np.sqrt(annual_trading_days)
    
    return annualized_sigma,s0,df

if __name__=='__main__': 
    sigma1,_,_=underlying_sigma('510050.SS','2021-11-19',days=365)
    sigma2,_,_=underlying_sigma('510050.SS','2021-11-19',days=183)
    sigma3,_,_=underlying_sigma('510050.SS','2021-11-19',days=92)  
    sigma4,_,_=underlying_sigma('510050.SS','2021-11-19',days=60)
    sigma5,_,_=underlying_sigma('510050.SS','2021-11-19',days=30)
    print(sigma1,sigma2,sigma3,sigma4,sigma5)

#=============================================================================

#=============================================================================
if __name__=='__main__': 
    start='2021-1-1'
    end='2021-10-12'

def calc_days(start,end):
    """
    计算两个日期之间的年数
    """
    
    #检查日期期间的有效性
    valid,start1,end1=check_period(start,end)
    if not valid:
        print("  #Error(calc_days): date period invalid")
        return None
    
    diff=end1-start1
    #日历天数
    diff2=diff.days
    diff_in_years=diff2/365

    return diff2,round(diff_in_years,5)    

if __name__=='__main__': 
    days,_=calc_days('2020-10-31','2021-10-12')


#=============================================================================
if __name__=='__main__': 
    option="华泰柏瑞沪深300ETF期权"
    end_month='2206'
    contract='510300C2206M04500'
    direction='call'
    
    today='2021-11-19'
    sample_days=30
    
    rate_type='shibor'
    rate_period='3M'
    daysahead=30

def option_fin_pricing_china(option,end_month,contract,today,direction='call', \
                             sample_days=30,rate_type='shibor',rate_period='1Y',printout=True):
    """
    功能：将中国金融期权定价的过程整合在一起，提供默认选项，改善小白的使用体验
    注：波动率使用历史波动率
    """
    
    #第1步：查找计算金融期权预期价格所需要的参数
    ua,maturity,x=option_fin_contract_parms(option,end_month,contract,direction)
    if ua is None:
        print("  #Error(option_fin_pricing_china): info not found")
        print("  Possible reasons: one or some of the following")
        print("    Option not found for",option)
        print("    Maturity year-month not found for",end_month)
        print("    Contract not found for",contract,'as',direction.lower())
        print("    Contract not found in the above option + maturity")
        return None

    #第2步：计算标的证券价格收益率的历史波动率：
    sigma,s0,_=underlying_sigma(ua,today,days=sample_days)
    
    #第3步：查找年化无风险利率
    rate_type=rate_type.upper()
    if rate_type=='SHIBOR':
        rf=shibor_rate(today,rate_period) 
    elif rate_type=='TREASURY':
        rf=treasury_yield_china(today,rate_period)
    else:
        print("  #Error(option_fin_pricing_china): invalid rate type",rate_type.lower())
        return None
        
    #第4步：计算当前日期距离合约到期日的天数
    days,_=calc_days(today,maturity)
    #print("days is",days)
    
    #第5步：计算期权合约的预期价格
    #中国目前金融期权均为无红利的欧式期权，可以直接采用Black-Scholes期权定价模型
    expected_price=bs_pricing(s0,x,days,rf,sigma,direction,printout=False)  
    
    if printout:
        print("\n============ 中国金融期权定价 ============\n")
        
        print("*** 合约信息：")
        print("    合约代码:",contract)
        print("    期权品种:",option)
        print("    标的证券:",ua)
        print("    行权价格:",x)
        print("    到期年月:",end_month)
        print("    期权方向:",direction)
        
        print("*** 合约现状：")
        print("    定价日期:",today,'\b，标的市价:',s0)
        print("    距离到期:",days,'\b天')
        print("    历史波动率期间:",sample_days,'\b天')
        print("    历史波动率数值:",round(sigma,5))
        
        print("    无风险利率种类:",rate_type.lower(),'\b,',rate_period)
        print("    年化无风险利率:",round(rf*100,4),'\b%')
        
        print("*** 定价结果：")
        print("    定价模型: Black-Scholes")        
        print("    理论价格:",round(expected_price,5))
        
        print("\n注：历史/隐含波动率的差异是定价误差的主要原因")
        
        import datetime; pgm_date = datetime.date.today()         
        print("数据来源: 新浪/沪深所/中金所,",pgm_date)        
        
    return expected_price  
        
if __name__=='__main__': 
    option="华泰柏瑞沪深300ETF期权"
    end_month='2206'
    #看涨合约
    option_fin_contracts(option,end_month,direction='call') 
    contract='510300C2206M04500'
    eprice=option_fin_pricing_china(option,end_month,contract,today='2021-11-19', \
                             direction='call', \
                             sample_days=90,rate_type='shibor',rate_period='1Y')
    #理论价格：0.5748，实际收盘价：0.5584
    #查看实际价格网址：https://stock.finance.sina.com.cn/option/quotes.html
    eprice=option_fin_pricing_china(option,end_month,contract,today='2021-11-19', \
                             direction='call', \
                             sample_days=90,rate_type='shibor',rate_period='1Y') 
    #理论价格：0.5631，实际收盘价：0.5584
    
    #看跌合约   
    option_fin_contracts(option,end_month,direction='put') 
    contract='510300P2206M04500'
    eprice=option_fin_pricing_china(option,end_month,contract,today='2021-11-19', \
                             direction='put', \
                             sample_days=365,rate_type='shibor',rate_period='1Y')
    #理论价格：0.083，实际收盘价：0.0893  
    #查看实际价格网址：http://quote.eastmoney.com/center/gridlist.html#options_sahs300etf_rengu

    eprice=option_fin_pricing_china(option,end_month,contract,today='2021-11-19', \
                             direction='put', \
                             sample_days=365,rate_type='shibor',rate_period='1Y')
    #理论价格：0.086，实际收盘价：0.0893          
    #=============================
    
    option="华夏上证50ETF期权"
    end_month='2206'
    #看涨合约
    option_fin_contracts(option,end_month,direction='call') 
    contract='510050C2206M02900'
    eprice=option_fin_pricing_china(option,end_month,contract,today='2021-11-19', \
                             direction='call', \
                             sample_days=90,rate_type='shibor',rate_period='1Y')
    #理论价格：0.4264，实际收盘价：0.4411
    #查看网址：http://quote.eastmoney.com/center/gridlist.html#options_sz50etf_txbj
    eprice=option_fin_pricing_china(option,end_month,contract,today='2021-11-19', \
                             direction='call', \
                             sample_days=90,rate_type='shibor',rate_period='1Y') 
    #理论价格：0.4191，实际收盘价：0.4411
    
    #看跌合约   
    option_fin_contracts(option,end_month,direction='put')
    contract='510050P2206M02900'
    eprice=option_fin_pricing_china(option,end_month,contract,today='2021-11-19', \
                             direction='put', \
                             sample_days=365,rate_type='shibor',rate_period='1Y')
    #理论价格：0.0505，实际收盘价：0.0441    
    eprice=option_fin_pricing_china(option,end_month,contract,today='2021-11-19', \
                             direction='put', \
                             sample_days=365,rate_type='shibor',rate_period='1Y')
    #理论价格：0.0524，实际收盘价：0.0441          
    #=============================

    option="嘉实沪深300ETF期权"
    end_month='2206'
    option_fin_contracts(option,end_month,direction='call')    
    #看涨合约
    contract='90000905'   
    eprice=option_fin_pricing_china(option,end_month,contract,today='2021-11-19', \
                             direction='call', \
                             sample_days=90,rate_type='shibor',rate_period='1Y')
    #理论价格：0.5878，实际收盘价：0.57
    #查看网站：http://quote.eastmoney.com/center/gridlist.html#options_szetf_all
    eprice=option_fin_pricing_china(option,end_month,contract,today='2021-11-19', \
                             direction='call', \
                             sample_days=90,rate_type='shibor',rate_period='1Y')        
    #理论价格：0.5766，实际收盘价：0.57
    
    #看跌合约
    option_fin_contracts(option,end_month,direction='put')
    contract='90000906'   
    eprice=option_fin_pricing_china(option,end_month,contract,today='2021-11-19', \
                             direction='put', \
                             sample_days=365,rate_type='shibor',rate_period='1Y')
    #理论价格：0.0692，实际收盘价：0.0848
    eprice=option_fin_pricing_china(option,end_month,contract,today='2021-11-19', \
                             direction='put', \
                             sample_days=365,rate_type='shibor',rate_period='1Y')        
    #理论价格：0.072，实际收盘价：0.0848
    #=============================

    option="沪深300股指期权"
    end_month='2206'
    option_fin_contracts(option,end_month,direction='call')    
    #看涨合约
    contract='IO2206-C-4200'   
    eprice=option_fin_pricing_china(option,end_month,contract,today='2021-11-19', \
                             direction='call', \
                             sample_days=90,rate_type='shibor',rate_period='1Y')
    #理论价格：770.9，实际收盘价：700.6
    #查看网站：http://quote.eastmoney.com/center/gridlist.html#options_cffex_all
    eprice=option_fin_pricing_china(option,end_month,contract,today='2021-11-19', \
                             direction='call', \
                             sample_days=90,rate_type='shibor',rate_period='1Y')        
    #理论价格：759，实际收盘价：700.6
    
    #看跌合约
    option_fin_contracts(option,end_month,direction='put')
    contract='IO2206-P-4200'   
    eprice=option_fin_pricing_china(option,end_month,contract,today='2021-11-19', \
                             direction='put', \
                             sample_days=365,rate_type='shibor',rate_period='1Y')
    #理论价格：40.7，实际收盘价：49.2
    eprice=option_fin_pricing_china(option,end_month,contract,today='2021-11-19', \
                             direction='put', \
                             sample_days=365,rate_type='shibor',rate_period='1Y')        
    #理论价格：42.6，实际收盘价：49.2
    
#=============================================================================
#=============================================================================
#=============================================================================
#沪深300股指期权价格运动
#=============================================================================
if __name__=='__main__': 
    printout=True

def hs300option_maturity(printout=True):
    """
    功能：获取沪深300股指期权的到期年月
    注意：只保留YYMM
    """
    
    import akshare as ak
    mdict=ak.option_cffex_hs300_list_sina()
    
    mkey="沪深300指数"
    mvalue=mdict[mkey]
    
    mlist=[]
    for m in mvalue:
        m4=m[-4:]
        mlist=mlist+[m4]
    mlist.sort()
    
    if printout:
        import datetime; today = datetime.date.today()
        footnote="数据来源: 新浪财经/东方财富, "+str(today)
        
        print("\n=== 沪深300股指期权的到期日(YYMM) ===\n")
        print(mlist)
        print(footnote)
        
    return mlist

if __name__=='__main__':     
    mlist=hs300option_maturity()    
#=============================================================================
if __name__=='__main__': 
    direction="Call"
    maturity="2306"
    direction="Call"
    printout=True

def hs300option_exercise(maturity,direction="Call",printout=True):
    """
    功能：获取沪深300股指期权的行权点位
    maturity: 到期年月YYMM
    direction: 看涨期权Call或看跌期权Put
    
    """
    #检查期权的看涨看跌方向
    directionl=direction.lower()
    if not (directionl in ["call","put"]):
        print("  #Error(hs300option_exercise): option direction must either Call or Put")
        return None
    
    #检查期权的到期日是否有效
    mlist=mlist=hs300option_maturity(printout=False)
    if not (maturity in mlist):
        print("  #Error(hs300option_exercise): maturity not available for", maturity)
        print("  Currently available",mlist)
        return None
    
    symbol="沪深300股指期权"
    import akshare as ak
    df=ak.option_finance_board(symbol=symbol, end_month=maturity)    
    df['maturity']=df['instrument'].apply(lambda x: x[2:6])
    df['direction']=df['instrument'].apply(lambda x: x[7:8])
    df['exercise']=df['instrument'].apply(lambda x: x[9:13])
    
    if directionl == "call":
        df2=df[df["direction"]=='C']
    else:
        df2=df[df["direction"]=='P']
        
    exerciselist=list(df2["exercise"])
    exerciselist.sort()
    
    if printout:
        
        print("\n=== 沪深300股指期权的行权点位 ===\n")
        print("到期日：",maturity,"\b，方向：",direction)
        #对列表分组打印
        n=9
        for e in [exerciselist[i:i+n] for i in range(0,len(exerciselist),n)]:
            print(e)
    
        import datetime; today = datetime.date.today()
        footnote="数据来源: 新浪财经/东方财富, "+str(today)
        print("\n"+footnote)

    return  exerciselist   

if __name__=='__main__': 
    elist=exerciselist=hs300option_exercise(maturity="2306",direction="Call")
#=============================================================================
if __name__=='__main__': 
    maturity="2306"
    exercise=4500
    direction="Call"
    
    option=["2306",4500,'Call']
"""
def hs300option_price(maturity,exercise,direction="Call", \
                      loc1='best',loc2='best', \
                      graph=True):
"""
def hs300option_price(option, \
                      loc1='best',loc2='best', \
                      graph=True):

    """
    功能：绘制沪深300股指期权的历史价格曲线
    option的结构：[maturity,exercise,direction]，例如["2306",3900,"Call"]
    """
    
    #结构期权参数
    maturity,exercise,direction=option_decode(option)
    
    #获取行权点位列表
    exerciselist=hs300option_exercise(maturity=maturity,direction=direction,printout=False)
    
    #检查行权点位
    exercisestr=str(exercise)
    if not (exercisestr in exerciselist):
        print("  #Error(hs300option_price): no such exercise point for", exercisestr)
        return None

    #合成新浪期权合约编号
    if direction.lower() == "call":
        directionL='C'
    else:
        directionL='P'
    symbol='io'+maturity+directionL+exercisestr

    #获取期权历史价格
    import akshare as ak
    hs300op = ak.option_cffex_hs300_daily_sina(symbol=symbol)
    datelist=list(hs300op['date'])
    start=datelist[0]
    end=datelist[-1]
    
    hs300op['Date']=pd.to_datetime(hs300op['date'])
    hs300op.set_index('Date',inplace=True)
    hs300op.sort_index(ascending=True,inplace=True) 
    hs300op2=hs300op[["close"]]
    hs300op2.rename(columns={'close':'SO Close'},inplace=True)    
    
    if graph:
        #获取股指历史价格
        hs300=get_price("000300.SS",start,end)
        hs3002=hs300[["Close"]]
        hs3002.rename(columns={'Close':'SI Close'},inplace=True)    
        
        #合成期权和股指
        hs300_op_zs=pd.merge(hs300op2,hs3002,how="left",left_index=True,right_index=True)
        hs300_op_zs["SO Exercise"]=float(exercise)
        
        """
        #计算期权的内在价值
        if directionL == "C":
            hs300_op_zs["IV"]=hs300_op_zs["SI Close"]-hs300_op_zs["SO Exercise"]
        else:
            hs300_op_zs["IV"]=-hs300_op_zs["SI Close"]+hs300_op_zs["SO Exercise"]
        hs300_op_zs["Intrinsic Value"]=hs300_op_zs["IV"].apply(lambda x: 0 if x<0 else x)
        """
        collabel_so='期权价格'
        collabel_si='沪深300指数'
        titletxt_so_si='沪深300股指期权：期权价格 vs 标的指数，'+ectranslate(direction)
        colname='Close'; ylabeltxt=''    
        
        footnote1="新浪期权代码："+symbol+"，到期日"+maturity+"，行权股指点位"+exercisestr
        import datetime; today = datetime.date.today()
        footnote2="数据来源: 新浪财经/东方财富, "+str(today)
        footnote=footnote1+"\n"+footnote2
        
        plot_line2_twinx(hs300_op_zs,'','SO Close',collabel_so, \
                         hs300_op_zs,'','SI Close',collabel_si, \
                             titletxt_so_si,footnote,loc1=loc1,loc2=loc2)    
    
    return hs300op2

if __name__=='__main__': 
    df=hs300option_price(maturity="2306",exercise=3900,direction="Call")    
#=============================================================================
if __name__=='__main__': 
    option1=["2306",3900,"Call"]
    option2=["2210",3900,"Put"]

def hs300option_compare(option1,option2,loc1='best',loc2='best',twinx=False):
    """
    功能：比较两个沪深300股指期权的价格曲线
    option的结构：[maturity,exercise,direction]，例如["2306",3900,"Call"]
    """
    #提取期权参数
    try:
        maturity1=option1[0]
        exercise1=option1[1]
        direction1=option1[2]
    except:
        print("  #Error(hs300option_compare): invalid option descroption",option1)
        print("  Option structure: [maturity YYMM,exercise point, direction Call or Put]")
        print("  For example, [\"2306\",3900,\"Call\"]")
        return None,None
    
    try:
        maturity2=option2[0]
        exercise2=option2[1]
        direction2=option2[2]
    except:
        print("  #Error(hs300option_compare): invalid option descroption",option2)
        print("  Option structure: [maturity YYMM,exercise point, direction Call or Put]")
        print("  For example, [\"2306\",3900,\"Call\"]")
        return None,None    
    
    if option1 == option2:
        print("  #Warning(hs300option_compare): expecting two different options for comparison:-(")
        return

    #设定是否同轴
    if direction1 == direction2:
        twinx=False
    else:
        twinx=True
    
    #获取期权价格
    df1=hs300option_price([maturity1,exercise1,direction1],graph=False)
    df2=hs300option_price([maturity2,exercise2,direction2],graph=False)
    
    #内连接：取共同日期期间
    import pandas as pd
    df12=pd.merge(df1,df2,how="inner",left_index=True,right_index=True)

    if not twinx:
        ticker1="期权1："+option_description(option1)
    else:
        ticker1="期权1"
    colname1='SO Close_x'

    if not twinx:
        ticker2="期权2："+option_description(option2)
    else:
        ticker2="期权2"
    colname2='SO Close_y'
    
    ylabeltxt="期权价格"
    titletxt='沪深300股指期权：价格运动与影响因素'
    
    if not twinx:
        footnote1=''
    else:
        footnote1="期权1"+str(option1)+"，期权2"+str(option2)+'\n'
    import datetime; today = datetime.date.today()
    footnote2="数据来源: 新浪财经/东方财富, "+str(today)
    footnote=footnote1+footnote2
    
    plot2_line2(df12,ticker1,colname1,'', \
               df12,ticker2,colname2,'', \
               ylabeltxt,titletxt,footnote, \
               twinx=twinx, \
               loc1=loc1,loc2=loc2, \
               date_range=False,date_freq=False)        
        
    return df12  
    
if __name__=='__main__': 
    
    #不同到期日
    option1=["2306",3900,"Call"]
    option2=["2210",3900,"Call"]
    df=hs300option_compare(option1,option2,loc1='lower left',loc2='upper right')
    
    #不同行权点位
    option1=["2306",3900,"Call"]
    option2=["2306",4500,"Call"]
    df=hs300option_compare(option1,option2,loc1='lower left',loc2='upper right')
    
    #不同方向：看涨vs看跌
    option1=["2306",4500,"Call"]
    option2=["2306",4500,"Put"]
    df=hs300option_compare(option1,option2,loc1='upper center',loc2='lower center')

#==============================================================================
if __name__=='__main__': 
    option=["2306",3900,"Call"]
    
def option_description(option):
    """
    功能：将期权合约的表示方法转换为字符串，供打印使用
    option：[到期年月YYMM,行权价格,行权方向]
    返回：字符串，到期如YYMM，行权价XXX，ZZ期权
    """
    
    try:
        maturity=option[0]
        exercise=str(option[1])
        direct=option[2].lower()
        if direct=="call":
            direction="看涨期权"
        elif direct=="put":
            direction="看跌期权"
        else:
            direction="期权方向未知"
    except:
        print("  #Error(option_description): invalid option description structure",option)
        print("  Expecting structure: [maturity YYMM,exercise price, direction Call or Put]")
        return None
    
    option_str="到期日"+maturity+"，行权价"+exercise+"，"+direction
    
    return option_str

if __name__=='__main__': 
    option=["2306",3900,"Call"]
    option_description(option)

#==============================================================================
if __name__=='__main__': 
    option=["2306",3900,"Call"]
    
def option_decode(option):
    """
    功能：将期权合约的表示方法分解为各个单项
    option：[到期年月YYMM,行权价格,行权方向]
    返回：到期如YYMM，行权价XXX，Call或Put
    """
    
    try:
        maturity=option[0]
        exercise=option[1]
        direct=option[2].capitalize()
    except:
        print("  #Error(option_decode): invalid option description structure",option)
        print("  Expecting structure: [maturity YYMM,exercise price, direction Call or Put]")
        return None
    
    return maturity,exercise,direct

if __name__=='__main__': 
    option=["2306",3900,"Call"]
    option_decode(option)                
#==============================================================================
if __name__=='__main__':     
    option='50ETF'
    maturity='2209'
    exercise=3000
    trade_date='2022-9-26'
    printout=True

def fin_option_risk_sse(option,maturity,exercise,trade_date,printout=True):
    """
    功能：显示指定上交所金融期权的风险指标
    option: 期权名称
    maturity: 到期年月YYMM
    exercise: 行权点位
    direction: 方向，看涨看跌
    """
    
    #初始检查：期权名称
    optionlist=["50ETF","300ETF","500ETF"]
    if not (option in optionlist):
        print("  #Error(fin_option_risk_sse): option not found in SSE for",option)
        return None
   
    #初始检查：交易日期
    if not check_date(trade_date):
        print("  #Error(fin_option_risk_sse): invalid date",trade_date)
        return None
    akdate=convert_date_ts(trade_date)
    
    import pandas as pd
    import akshare as ak
    
    #获取交易日数据
    try:
        df = ak.option_risk_indicator_sse(date=akdate)
    except:
        print("  #Warning(fin_option_risk_sse): no data retrieved for this date",trade_date)
        return None
    
    df['Date']=df['TRADE_DATE']
    df['date']=df['TRADE_DATE']
    df['Date']=pd.to_datetime(df['Date'])
    df.set_index('Date',inplace=True)
    df.sort_index(ascending=True,inplace=True) 
        
    df['direction']=df['CONTRACT_ID'].apply(lambda x: x[6:7])
    df['underlying']=df['CONTRACT_ID'].apply(lambda x: x[:6])
    df['ETF end']=df['CONTRACT_SYMBOL'].apply(lambda x: x.find('ETF')+3)
    df['option']=df.apply(lambda x: x['CONTRACT_SYMBOL'][:x['ETF end']],axis=1)
    df['exercise']=df['CONTRACT_ID'].apply(lambda x: float(x[12:]))
    
    #进一步检查：到期日
    df['maturity']=df['CONTRACT_ID'].apply(lambda x: x[7:11])
    #进一步检查：到期日
    if not (maturity in list(df['maturity'])):
        print("  #Error(fin_option_risk_sse): maturity not found in SSE for",maturity)
        
        df_maturity=df[(df['option']==option) & (df['exercise']==exercise)]
        maturitylist=list(set(list(df_maturity['maturity'])))
        maturitylist.sort()
        print("  On "+trade_date+", available maturities:",maturitylist)
        return None
    
    #进一步检查：行权点位
    if not (exercise in list(df['exercise'])):
        print("  #Error(fin_option_risk_sse): exericse point not found in SSE for",exercise)
        
        df_exercise=df[(df['option']==option) & (df['maturity']==maturity)]
        exerciselist=list(set(list(df_exercise['exercise'])))
        exerciselist.sort()
        exerciselist2=list(map(int,exerciselist))
        print("  Available exercises:",exerciselist2)
        return None
    
        
    df['delta']=df['DELTA_VALUE']
    df['theta']=df['THETA_VALUE']
    df['gamma']=df['GAMMA_VALUE']
    df['vega']=df['VEGA_VALUE']
    df['rho']=df['RHO_VALUE']
    df['implied volatility']=df['IMPLC_VOLATLTY']
    
    itemlist=["date",'option','underlying','direction','maturity','exercise', \
              'delta','theta','gamma','vega','rho','implied volatility']
    df2=df[itemlist]
    
    #提取符合条件的记录
    df9=df2[(df2['option']==option) \
            & (df2['maturity']==maturity) & (df2['exercise']==exercise)]
    #综合检查：全部条件
    if len(df9) == 0:
        print("  #Error(fin_option_risk_sse): options not available combining",option,maturity,exercise)
        df9tmp=df2[(df2['option']==option) & (df2['maturity']==maturity)]
        execlist=list(df9tmp['exercise'])
        exerciselist=[]
        for e in execlist:
            eint=int(e)
            exerciselist=exerciselist+[eint]
        print("  Exercises available under",option,maturity,"\b:",exerciselist)
        return None

    df9C=df9[(df9['direction']=='C')]
    underlying=df9C['underlying'][0]+'.SS'
    deltaC=df9C['delta'][0]    
    thetaC=df9C['theta'][0]
    gammaC=df9C['gamma'][0]
    vegaC=df9C['vega'][0]
    rhoC=df9C['rho'][0]
    impvolC=df9C['implied volatility'][0]
    
    df9P=df9[df9['direction']=='P']
    deltaP=df9P['delta'][0]    
    thetaP=df9P['theta'][0]
    gammaP=df9P['gamma'][0]
    vegaP=df9P['vega'][0]
    rhoP=df9P['rho'][0]
    impvolP=df9P['implied volatility'][0]
    
    print("\n===== 上交所金融期权风险指标 =====\n")
    print("***期权:",option,"\b，交易日期：",trade_date)
    print("标的物代码:",underlying,"\b，到期时间:",maturity,"\b，行权股指点位:",exercise)

    print("\n***风险指标：")
    print("【看涨】Delta =",deltaC,"\b，Theta =",thetaC,"\b，Gamma =",gammaC,"\b，Vega =",vegaC,"\b，Rho =",rhoC)
    print("隐含波动率 =",impvolC)    

    print("【看跌】Delta =",deltaP,"\b，Theta =",thetaP,"\b，Gamma =",gammaP,"\b，Vega =",vegaP,"\b，Rho =",rhoP)
    print("隐含波动率 =",impvolP)    

    import datetime; today = datetime.date.today()
    footnote="数据来源: 新浪财经/东方财富, "+str(today)
    print('\n'+footnote)
    
    return df9

if __name__=='__main__':     
    df=fin_option_risk_sse(option='50ETF',maturity='2209',exercise=3000,date='2022-9-26')

#==============================================================================
if __name__=='__main__':     
    option='50ETF'
    maturity='2209'
    exercise=3000
    trade_date='2022-9-26'
    printout=True

def fin_option_risk_sse2(option,maturity,exercise,trade_date, \
                         printout=True,loc='best'):
    """
    功能：显示指定上交所金融期权的风险指标
    option: 期权名称
    maturity: 到期年月YYMM
    exercise: 行权点位
    direction: 方向，看涨看跌
    """
    
    #初始检查：期权名称
    optionlist=["50ETF","300ETF","500ETF"]
    if not (option in optionlist):
        print("  #Error(fin_option_risk_sse): option not found in SSE for",option)
        return None
   
    #初始检查：交易日期
    if not check_date(trade_date):
        print("  #Error(fin_option_risk_sse): invalid date",trade_date)
        return None
    akdate=convert_date_ts(trade_date)
    
    import pandas as pd
    import numpy as np
    import akshare as ak
    
    #获取交易日数据
    try:
        df = ak.option_risk_indicator_sse(date=akdate)
    except:
        print("  #Warning(fin_option_risk_sse): failed to retrieved data for",trade_date)
        return None
    
    df['Date']=df['TRADE_DATE']
    df['date']=df['TRADE_DATE']
    df['Date']=pd.to_datetime(df['Date'])
    df.set_index('Date',inplace=True)
    df.sort_index(ascending=True,inplace=True) 
        
    df['direction']=df['CONTRACT_ID'].apply(lambda x: x[6:7])
    df['underlying']=df['CONTRACT_ID'].apply(lambda x: x[:6])
    df['ETF end']=df['CONTRACT_SYMBOL'].apply(lambda x: x.find('ETF')+3)
    df['option']=df.apply(lambda x: x['CONTRACT_SYMBOL'][:x['ETF end']],axis=1)
    df['exercise']=df['CONTRACT_ID'].apply(lambda x: float(x[12:]))
    
    #进一步检查：到期日
    df['maturity']=df['CONTRACT_ID'].apply(lambda x: x[7:11])
    #进一步检查：到期日
    if not (maturity in list(df['maturity'])):
        print("  #Error(fin_option_risk_sse): maturity not found in SSE for",maturity)
        
        df_maturity=df[(df['option']==option) & (df['exercise']==exercise)]
        maturitylist=list(set(list(df_maturity['maturity'])))
        maturitylist.sort()
        print("  On "+trade_date+", available maturities:",maturitylist)
        return None
    
    #进一步检查：行权点位
    if not (exercise in list(df['exercise'])):
        print("  #Error(fin_option_risk_sse): exericse point not found in SSE for",exercise)
        
        df_exercise=df[(df['option']==option) & (df['maturity']==maturity)]
        exerciselist=list(set(list(df_exercise['exercise'])))
        exerciselist.sort()
        exerciselist2=list(map(int,exerciselist))
        print("  Available exercises:",exerciselist2)
        return None
    
        
    df['Delta']=df['DELTA_VALUE']
    df['Gamma']=df['GAMMA_VALUE']
    df['Theta']=df['THETA_VALUE']
    df['Vega']=df['VEGA_VALUE']
    df['Rho']=df['RHO_VALUE']
    df['Implied Volatility']=df['IMPLC_VOLATLTY']
    
    itemlist=["date",'option','underlying','direction','maturity','exercise', \
              'Delta','Gamma','Theta','Vega','Rho','Implied Volatility']
    df2=df[itemlist]
    
    #提取符合条件的记录
    df9=df2[(df2['option']==option) \
            & (df2['maturity']==maturity) & (df2['exercise']==exercise)]
    #综合检查：全部条件
    if len(df9) == 0:
        print("  #Error(fin_option_risk_sse): options not available fulfilling",option,maturity,exercise)
        return None

    #绘制看涨看跌期权风险对比柱状图
    #排序，保证看涨期权排在前面
    df9.sort_values(by='direction',ascending=True,inplace=True)
    #df9b=df9[['delta','theta','gamma','vega','rho','implied volatility']]
    df9b=df9[['Delta','Gamma','Theta','Vega','Rho']]
    dfg=df9b.T
    dfg.columns=['看涨期权','看跌期权'] 

    #fig = plt.figure()
    import matplotlib.pyplot as plt
    plt.rcParams['figure.figsize']=(12.8,7.2)
    plt.rcParams['figure.dpi']=300
    """
    c=dfg.plot(kind='bar', y=['看涨期权','看跌期权'],figsize=(16, 8),width=0.8,
               color=['green','red'],fontsize=16)
    """
    #柱状图填充图案
    hatch_par = ['/', '', '|', '-', '+', 'x', 'o', 'O', '.', '*']
    c=dfg.plot(kind='bar', y=['看涨期权','看跌期权'],width=0.8,
               color=['green','red'],fontsize=16)
    
    #display the percentages above the bars as shown above 数据标签列表
    x=np.arange(len(dfg.index))
    yv=np.array(list(dfg['看涨期权']))
    ys=np.array(list(dfg['看跌期权']))
    
    import numpy as np
    textupper=0.01
    textlower=0.065
    for a,b in zip(x,yv): ##控制标签位置：横坐标，纵坐标
        if b >= 0:
            plt.text(a-0.2,b+textupper,'%.3f'%b,ha = 'center',va = 'bottom',fontsize=14)
        else:
            plt.text(a-0.2,b-textlower,'%.3f'%b,ha = 'center',va = 'bottom',fontsize=14)
    for a,b in zip(x,ys):
        if b >= 0:
            plt.text(a+0.2,b+textupper,'%.3f'%b,ha = 'center',va = 'bottom',fontsize=14)
        else:
            plt.text(a+0.2,b-textlower,'%.3f'%b,ha = 'center',va = 'bottom',fontsize=14)
   
    #绘制图片边框
    c.spines['top'].set_visible(True)
    c.spines['right'].set_visible(True)
    c.spines['bottom'].set_visible(True) #保留横坐标边框
    c.spines['left'].set_visible(True)
    
    plt.xticks(rotation=0)

    #option,maturity,exercise,trade_date
    footnote0="风险指标\n"
    footnote1="注："+"到期年月"+maturity+"，行权股指点位"+str(exercise)+"，交易日"+trade_date
    import datetime; today = datetime.date.today()
    footnote2="数据来源: 新浪财经/东方财富, 制图"+str(today)
    footnote=footnote0+footnote1+"\n"+footnote2
    plt.xlabel(footnote,fontweight='bold',fontsize=xlabel_txt_size)
    plt.ylabel('希腊值') # y轴空轴
    
    #use font size 16 for the title, and, 标题字号
    plt.title("上交所金融期权的希腊值："+option+"期权",fontsize=18)

    #use font size 14 for the bar labels, percentages, and legend, 图例颜色
    plt.legend(fontsize=16,loc=loc)
    
    plt.show
    
    return df9

if __name__=='__main__':     
    df=fin_option_risk_sse2(option='50ETF', \
                            maturity='2209', \
                            exercise=3000, \
                            trade_date='2022-9-26')

#==============================================================================
#==============================================================================
if __name__=='__main__':     
    option='50ETF'
    maturity='2209'
    exercise=3000
    date='2022-9-26'
    graph=True
    loc1='best'
    loc2='best'

def fin_option_maturity_risk_sse(option,exercise,trade_date, \
                                 measure='delta', \
                                 twinx=False,graph=True,loc1='best',loc2='best', \
                                 date_range=False,date_freq=False,date_fmt='%Y-%m'):
    """
    功能：绘制指定上交所金融期权的风险指标曲线，风险因素：到期日maturity(横轴)，各个风险指标(纵轴，看涨/看跌)
    option: 期权名称
    maturity: 到期年月YYMM
    exercise: 行权点位
    direction: 方向，看涨看跌
    """
    
    #初步检查：期权名称
    optionlist=["50ETF","300ETF","500ETF"]
    if not (option in optionlist):
        print("  #Error(fin_option_maturity_risk_sse): option not found in SSE for",option)
        return None
    
    #初步检查：交易日期
    if not check_date(trade_date):
        print("  #Error(fin_option_maturity_risk_sse): invalid date",trade_date)
        return None
    akdate=convert_date_ts(trade_date)
    
    #初步检查：风险指标
    measurelist=['delta','theta','gamma','vega','rho','implied volatility']
    if not (measure in measurelist):
        print("  #Error(fin_option_maturity_risk_sse): invalid measure",measure)
        print("  Valid measure:",measurelist)
        return None
    
    import pandas as pd
    import akshare as ak
    try:
        df = ak.option_risk_indicator_sse(date=akdate)
    except:
        print("  #Warning(fin_option_maturity_risk_sse): no data available for this date",trade_date)
        return None
    
    df['tdate']=df['TRADE_DATE']
    df['direction']=df['CONTRACT_ID'].apply(lambda x: x[6:7])
    df['underlying']=df['CONTRACT_ID'].apply(lambda x: x[:6])
    df['maturity']=df['CONTRACT_ID'].apply(lambda x: x[7:11])
    
    df['exercise']=df['CONTRACT_ID'].apply(lambda x: float(x[12:]))
    if not (exercise in list(df['exercise'])):
        print("  #Error(fin_option_maturity_risk_sse): exericse point not found in SSE for",exercise)
        
        df_exercise=df[(df['option']==option)]
        exerciselist=list(set(list(df_exercise['exercise'])))
        exerciselist.sort()
        exerciselist2=list(map(int,exerciselist))
        print("  Available exercises:",exerciselist2)
        return None
    
    #获得期权名称
    df['ETF end']=df['CONTRACT_SYMBOL'].apply(lambda x: x.find('ETF')+3)
    df['option']=df.apply(lambda x: x['CONTRACT_SYMBOL'][:x['ETF end']],axis=1)
    
    #获得风险指标    
    df['delta']=df['DELTA_VALUE']
    df['theta']=df['THETA_VALUE']
    df['gamma']=df['GAMMA_VALUE']
    df['vega']=df['VEGA_VALUE']
    df['rho']=df['RHO_VALUE']
    df['implied volatility']=df['IMPLC_VOLATLTY']
    
    itemlist=["tdate",'option','underlying','direction','maturity','exercise', \
              'delta','theta','gamma','vega','rho','implied volatility']
    df2=df[itemlist]
    
    df9=df2[(df2['option']==option) & (df2['exercise']==exercise)]
    if len(df9) == 0:
        print("  #Error(fin_option_maturity_risk_sse): options not available fulfilling",option,exercise)
        return None
    
    df9['Date']=df9['maturity'].apply(lambda x: '20'+x[:2]+'-'+x[2:4]+'-26')
    df9['Date']=pd.to_datetime(df9['Date'])
    df9.set_index('Date',inplace=True)
    df9.sort_index(ascending=True,inplace=True) 
    
    df9.sort_values(by=['direction','maturity'],ascending=True,inplace=True)
    
    df9C=df9[df9['direction']=='C']
    df9P=df9[df9['direction']=='P']
    underlying=df9C['underlying'][0]+'.SS'

    #绘图：看涨+看跌
    ticker1="看涨期权"; colname1=measure
    #label1=measure
    ticker2="看跌期权"; colname2=measure
    #label2=measure
    #ylabeltxt="风险指标"
    ylabeltxt=ectranslate(measure)
    titletxt='上交所金融期权风险：'+option+'期权，到期时间对'+ylabeltxt+"的影响"
    
    footnote0="到期时间（不同期权）\n"
    footnote1=option+"期权"+"，行权股指点位"+str(exercise)+"，交易日"+trade_date
    import datetime; today = datetime.date.today()
    footnote2="数据来源: 新浪财经/东方财富, 制图"+str(today)
    footnote=footnote0+footnote1+"\n"+footnote2
    
    plot2_line2(df9C,ticker1,colname1,'', \
               df9P,ticker2,colname2,'', \
               ylabeltxt,titletxt,footnote, \
               twinx=twinx, \
               loc1=loc1,loc2=loc2, \
               date_range=date_range,date_freq=date_freq,date_fmt=date_fmt)        
    
    return df9

if __name__=='__main__':     
    df=fin_option_maturity_risk_sse(option='300ETF',exercise=4500,trade_date='2022-9-26',measure='implied volatility')

#==============================================================================
if __name__=='__main__':     
    option='300ETF'
    maturity='2209'
    exercise=3000
    trade_date='2022-9-26'
    measure='implied volatility'
    graph=True
    loc1='best'
    loc2='best'

def fin_option_exercise_risk_sse(option,maturity,trade_date, \
                                 measure='delta', \
                                 graph=True,loc1='best',loc2='best'):
    """
    功能：绘制指定上交所金融期权的风险指标曲线，风险因素：行权点位exercise(横轴)，各个风险指标(纵轴，看涨/看跌)
    option: 期权名称
    maturity: 到期年月YYMM
    exercise: 行权点位
    direction: 方向，看涨看跌
    """
    
    #初步检查：期权名称
    optionlist=["50ETF","300ETF","500ETF"]
    if not (option in optionlist):
        print("  #Error(fin_option_exercise_risk_sse): option not found in SSE for",option)
        return None
    
    #初步检查：日期
    if not check_date(trade_date):
        print("  #Error(fin_option_exercise_risk_sse): invalid date",trade_date)
        return None
    akdate=convert_date_ts(trade_date)
    
    #初步检查：风险指标
    measurelist=['delta','theta','gamma','vega','rho','implied volatility']
    if not (measure in measurelist):
        print("  #Error(fin_option_exercise_risk_sse): invalid measure",measure)
        print("  Valid measure:",measurelist)
        return None
    
    print("\nStarting to search information necessary, please wait ...")
    import pandas as pd
    import akshare as ak
    try:
        #print("akdate =",akdate)
        df = ak.option_risk_indicator_sse(date=akdate)
    except:
        print("  #Warning(fin_option_exercise_risk_sse): no data available on",trade_date)
        return None
    
    df['tdate']=df['TRADE_DATE']
    df['direction']=df['CONTRACT_ID'].apply(lambda x: x[6:7])
    df['underlying']=df['CONTRACT_ID'].apply(lambda x: x[:6])
    
    #进一步检查：到期日
    df['maturity']=df['CONTRACT_ID'].apply(lambda x: x[7:11])
    if not (maturity in list(df['maturity'])):
        print("  #Error(fin_option_exercise_risk_sse): maturity not found in SSE for",maturity)
        
        df_maturity=df[(df['option']==option)]
        maturitylist=list(set(list(df_maturity['maturity'])))
        maturitylist.sort()
        print("  On "+trade_date+", available maturities:",maturitylist)
        return None
    
    df['exercise']=df['CONTRACT_ID'].apply(lambda x: float(x[12:]))
    
    #获得期权名称
    df['ETF end']=df['CONTRACT_SYMBOL'].apply(lambda x: x.find('ETF')+3)
    df['option']=df.apply(lambda x: x['CONTRACT_SYMBOL'][:x['ETF end']],axis=1)
    
    #获得风险指标    
    df['delta']=df['DELTA_VALUE']
    df['theta']=df['THETA_VALUE']
    df['gamma']=df['GAMMA_VALUE']
    df['vega']=df['VEGA_VALUE']
    df['rho']=df['RHO_VALUE']
    df['implied volatility']=df['IMPLC_VOLATLTY']
    
    itemlist=["tdate",'option','underlying','direction','maturity','exercise', \
              'delta','theta','gamma','vega','rho','implied volatility']
    df2=df[itemlist]
    
    df9=df2[(df2['option']==option) & (df2['maturity']==maturity)]
    if len(df9) == 0:
        print("  #Error(fin_option_exercise_risk_sse): options not available fulfilling",option,maturity)
        return None
    df9.sort_values(by=['direction','exercise'],ascending=True,inplace=True)
    
    df9C=df9[df9['direction']=='C']
    df9P=df9[df9['direction']=='P']
    underlying=list(set(list(df9C['underlying'])))[0]+'.SS'

    #绘图：看涨+看跌
    import matplotlib.pyplot as plt
    
    dftmp=df9C
    labeltxt="看涨期权"
    plt.plot(dftmp.exercise,dftmp[measure],'-',label=labeltxt, \
             linestyle='-',color='blue',linewidth=2)    

    dftmp=df9P
    labeltxt="看跌期权"
    plt.plot(dftmp.exercise,dftmp[measure],'-',label=labeltxt, \
             linestyle='--',color='orange',linewidth=2)    
        
    plt.legend(loc=loc1,fontsize=legend_txt_size)
    ylabeltxt=ectranslate(measure)
    plt.ylabel(ylabeltxt,fontsize=ylabel_txt_size)
    
    footnote1="行权股指点位"
    footnote2=option+"期权"+"，到期时间"+maturity+"，交易日"+trade_date
    
    import datetime; today = datetime.date.today()
    footnote3="数据来源: 新浪财经/东方财富, 制图"+str(today)
    footnote=footnote1+"\n"+footnote2+"\n"+footnote3    
    plt.xlabel(footnote,fontsize=xlabel_txt_size)
    
    titletxt='上交所金融期权风险：'+option+'期权，股指点位对'+ylabeltxt+'的影响'
    plt.title(titletxt,fontweight='bold',fontsize=title_txt_size)
    plt.show()
    plt.close()
    
    return df9

if __name__=='__main__':     
    df=fin_option_exercise_risk_sse(option='300ETF',maturity='2209',trade_date='2022-9-26',measure='implied volatility')

#==============================================================================
if __name__=='__main__':     
    option='50ETF'
    maturity='2209'
    exercise=3500
    start='2022-9-10'
    end="2022-9-26"
    graph=True
    loc1='best'
    loc2='best'
    date_range=False
    date_freq=False

def fin_option_time_risk_sse(option,maturity,exercise,start,end, \
                             measure='delta', \
                             graph=True,loc1='best',loc2='best', \
                             date_range=False,date_freq=False,twinx=False):
    """
    功能：绘制指定上交所金融期权的风险指标曲线，风险因素：随时间推移start/end(横轴)，各个风险指标(纵轴，看涨/看跌)
    option: 期权名称
    maturity: 到期年月YYMM
    exercise: 行权点位
    start: 开始日期
    end: 结束日期
    date_range: True标注每个日期，False为系统自动
    date_freq: 日期标注频率，仅在date_range为True时起作用，例如'2D'为每隔2天，'2M'为每隔2个月，'1Y'为每年，False为每天
    """
    
    #初步检查：期权名称
    optionlist=["50ETF","300ETF","500ETF"]
    if not (option in optionlist):
        print("  #Error(fin_option_time_risk_sse): option not found in SSE for",option)
        return None
    
    #初步检查：交易日期
    flag,startpd,endpd=check_period(start,end)
    if not flag:
        print("  #Error(fin_option_time_risk_sse): invalid date or period",start,end)
        return None
    
    #初步检查：风险指标
    measurelist=['delta','theta','gamma','vega','rho','implied volatility']
    if not (measure in measurelist):
        print("  #Error(fin_option_time_risk_sse): invalid measure",measure)
        print("  Valid measure:",measurelist)
        return None

    print("\nStarting to search information necessary, please wait ...")
    import pandas as pd
    import akshare as ak
    
    #循环获取各个交易日的指标
    df=pd.DataFrame()
    curdate=start; curdatepd=startpd
    print("Searching information on ",end='')
    while curdatepd <= endpd:
        print(curdate,end=' ')
        akdate=convert_date_ts(curdate)    
        try:
            dftmp = ak.option_risk_indicator_sse(date=akdate)
        except:
            curdate=date_adjust(curdate,adjust=1)
            continue
        df=df.append(dftmp)
        curdate=date_adjust(curdate,adjust=1)
        curdatepd=pd.to_datetime(curdate)
    print(' ')
    
    #整理数据    
    df['Date']=df['TRADE_DATE']
    df['date']=df['TRADE_DATE']
    df['Date']=pd.to_datetime(df['Date'])
    df.set_index('Date',inplace=True)
    df.sort_index(ascending=True,inplace=True) 
        
    df['direction']=df['CONTRACT_ID'].apply(lambda x: x[6:7])
    df['underlying']=df['CONTRACT_ID'].apply(lambda x: x[:6])
    
    #获得期权名称
    df['ETF end']=df['CONTRACT_SYMBOL'].apply(lambda x: x.find('ETF')+3)
    df['option']=df.apply(lambda x: x['CONTRACT_SYMBOL'][:x['ETF end']],axis=1)
    
    df['maturity']=df['CONTRACT_ID'].apply(lambda x: x[7:11])
    df['exercise']=df['CONTRACT_ID'].apply(lambda x: float(x[12:]))
    #进一步检查：到期日
    if not (maturity in list(df['maturity'])):
        print("  #Error(fin_option_time_risk_sse): maturity not found in SSE for",maturity)
        
        df_maturity=df[(df['option']==option) & (df['exercise']==exercise)]
        maturitylist=list(set(list(df_maturity['maturity'])))
        maturitylist.sort()
        print("  Available maturities:",maturitylist)
        return None
    #进一步检查：行权点位
    if not (exercise in list(df['exercise'])):
        print("  #Error(fin_option_time_risk_sse): exericse point not found in SSE for",exercise)
        
        df_exercise=df[(df['option']==option) & (df['maturity']==maturity)]
        exerciselist=list(set(list(df_exercise['exercise'])))
        exerciselist.sort()
        exerciselist2=list(map(int,exerciselist))
        print("  Available exercises:",exerciselist2)
        return None
    
    #获得风险指标    
    df['delta']=df['DELTA_VALUE']
    df['theta']=df['THETA_VALUE']
    df['gamma']=df['GAMMA_VALUE']
    df['vega']=df['VEGA_VALUE']
    df['rho']=df['RHO_VALUE']
    df['implied volatility']=df['IMPLC_VOLATLTY']
    
    itemlist=["date",'option','underlying','direction','maturity','exercise', \
              'delta','theta','gamma','vega','rho','implied volatility']
    df2=df[itemlist]
    
    df9=df2[(df2['option']==option) & (df2['maturity']==maturity) & (df2['exercise']==exercise)]
    if len(df9) == 0:
        print("  #Error(fin_option_time_risk_sse): options not available fulfilling",option,maturity,exercise)
        return None
    df9.sort_values(by=['date','direction','maturity'],ascending=True,inplace=True)
    
    df9C=df9[df9['direction']=='C']
    df9P=df9[df9['direction']=='P']
    underlying=list(set(list(df9C['underlying'])))[0]+'.SS'

    #绘图：看涨+看跌
    ticker1="看涨期权"; colname1=measure
    #label1=measure
    ticker2="看跌期权"; colname2=measure
    #label2=measure
    #ylabeltxt="风险指标"
    ylabeltxt=ectranslate(measure)
    titletxt='上交所金融期权风险：'+option+'期权，时间流逝对'+ylabeltxt+'的影响'
    
    footnote0="时间流逝（同一期权）\n"
    footnote1=option+"期权"+"，行权股指点位"+str(exercise)+"，到期时间"+maturity
    import datetime; today = datetime.date.today()
    footnote2="数据来源: 新浪财经/东方财富, 制图"+str(today)
    footnote=footnote0+footnote1+"\n"+footnote2
    
    if not date_range:
        ndays=date_delta(start,end)
        if ndays <= 20: 
            date_range=True
        elif ndays <= 40:
            date_range=True; date_freq='2D'
        elif ndays <=60:
            date_range=True; date_freq='3D'
        elif ndays <=80:
            date_range=True; date_freq='4D'
    
    plot2_line2(df9C,ticker1,colname1,'', \
               df9P,ticker2,colname2,'', \
               ylabeltxt,titletxt,footnote, \
               twinx=twinx, \
               loc1=loc1,loc2=loc2, \
               date_range=date_range,date_freq=date_freq)        
    
    return df9

if __name__=='__main__':     
    df=fin_option_time_risk_sse(option='300ETF',maturity='2209',exercise=4500,start='2022-8-26',end='2022-9-26',measure='implied volatility')
#==============================================================================
#=============================================================================
#=============================================================================
#=============================================================================    