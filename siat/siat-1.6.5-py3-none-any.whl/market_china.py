# -*- coding: utf-8 -*-
"""
所属工具包：证券投资分析工具SIAT 
SIAT：Security Investment Analysis Tool
创建日期：2022年12月11日
最新修订日期：
作者：王德宏 (WANG Dehong, Peter)
作者单位：北京外国语大学国际商学院
作者邮件：wdehong2000@163.com
版权所有：王德宏
用途限制：仅限研究与教学使用，不可商用！商用需要额外授权。
特别声明：作者不对使用本工具进行证券投资导致的任何损益负责！
"""
#==============================================================================
#处理潜在的中文字符编码问题，免去中文字符前面加"u"
from __future__ import unicode_literals

#屏蔽所有警告性信息
import warnings; warnings.filterwarnings('ignore')
#==============================================================================
from siat.common import *
from siat.translate import *
from siat.grafix import *
from siat.security_prices import *

#==============================================================================
import matplotlib.pyplot as plt

title_txt_size=16
ylabel_txt_size=14
xlabel_txt_size=14

#==============================================================================
#==============================================================================
# 功能：沪深市场概况
#==============================================================================
if __name__=='__main__':
    market='SSE'
    market='SZSE'

def market_profile_china(market='SSE'):
    """
    功能：沪深市场概况
    """
    market1=market.upper()
    mktlist=['SSE','SZSE']
    if market1 not in mktlist:
        print("  #Error(market_profile_china): unsupported market",market)
        print("  Supported market abbreviation:",mktlist)
    import datetime as dt
    today=dt.date.today()
    
    import akshare as ak
    lang=check_language()
    
    if market1 == 'SSE':
        try:
            info=ak.stock_sse_summary()
        except:
            print("  #Error(market_profile_china): failed to retrieve SSE summary info")
            return

        if lang == 'Chinese':       
            print("\n=== 上海证券交易所上市股票概况 ===\n")
        else:
            print("\n    Exchange Stock Summary： Shanghai Stock Exchange\n")
            
        typelist=['股票','主板','科创板']
        typelist2=['Stock overall','Main board','STAR board']
        
        itemlist=['上市股票','总股本','流通股本','总市值','流通市值']
        itemlist2=['上市股票/只','总股本/亿股（份）','流通股本/亿股（份）','总市值/亿元','流通市值/亿元']
        itemlist2e=['Number of stocks','Total shares(100m)','Shares outstanding(100m)','Total capitalization(RMB 100m)','Outstandng capitalization(RMB 100m)']
        
        for t in typelist:
            subdf=info[['项目',t]]
            if lang == 'English':
                pos=typelist.index(t)
                t2=typelist2[pos]
                print('*** '+t2+':')
            else:
                print('*** '+t+':')
                
            lenlist=[]
            for m in itemlist2:
                l=hzlen(m)
                lenlist=lenlist+[l]
            maxlen=max(lenlist)
                
            for i in itemlist:
                
                try:
                    value=list(subdf[subdf['项目']==i][t])[0]
                    pos=itemlist.index(i)
                    
                    if lang == 'Chinese':
                        i2=itemlist2[pos]
                        blanknum=maxlen-hzlen(i2)
                        print('   ',i2+' '*blanknum+'：',end='')
                    else:
                        i2e=itemlist2e[pos]
                        blanknum=maxlen-hzlen(i2e)
                        print('   ',i2e+' '*blanknum+'：',end='')
                except:
                    pos=itemlist.index(i)
                    i2=itemlist2[pos]
                    value=list(subdf[subdf['项目']==i2][t])[0]
                    i2e=itemlist2e[pos]
                    
                    if lang == 'Chinese':
                        blanknum=maxlen-hzlen(i2)
                        print('   ',i2+' '*blanknum+'：',end='')
                    else:
                        blanknum=maxlen-hzlen(i2e)
                        print('   ',i2e+' '*blanknum+'：',end='')
                
                if i in ["上市股票",'上市公司']: #若是字符则转换成数字
                    value2=int(value)
                else:
                    value2=float(value)
                print("{:,}".format(value2))
                
        if lang == 'Chinese':
            #print("    注：部分上市公司同时发行A股和B股")
            print("\n    数据来源：上交所，",today)
        else:
            print("\n    Source: Shanghai Stock Exchange,",today)
            
        
    if market1 == 'SZSE':
        df=ak.stock_szse_summary()  
        df1=df[df['证券类别'].isin(['股票','主板A股','主板B股','中小板','创业板A股'])]
        
        #字段改名
        """
        df1.rename(columns={'证券类别':'type','数量(只)':'上市股票/只', \
            '总股本':'总股本/亿股（份）','总市值':'总市值/亿元', \
            '流通股本':'流通股本/亿股（份）','流通市值':'流通市值/亿元'},inplace=True)
        """
        df1.rename(columns={'证券类别':'type','数量':'上市股票/只', \
            '总市值':'总市值/亿元', \
            '流通市值':'流通市值/亿元'},inplace=True)
        #df1['总股本/亿股（份）']=df1['总股本/亿股（份）'].apply(lambda x:round(x/100000000.0,2))
        df1['总市值/亿元']=df1['总市值/亿元'].apply(lambda x:round(x/100000000.0,2))
        #df1['流通股本/亿股（份）']=df1['流通股本/亿股（份）'].apply(lambda x:round(x/100000000.0,2))
        df1['流通市值/亿元']=df1['流通市值/亿元'].apply(lambda x:round(x/100000000.0,2))
        
        del df1['成交金额']
        #del df1['成交量']
        df1.loc[(df1['type']=='股票'),'type']='总貌'
        df1.loc[(df1['type']=='创业板A股'),'type']='创业板'
        
        #itemlist=['数量','总股本/亿股（份）','流通股本/亿股（份）','总市值/亿元','流通市值/亿元']
        itemlist=['上市股票/只','总市值/亿元','流通市值/亿元']
        itemliste=['Number of stocks','Total capitalization(RMB 100m)','Outstandng capitalization(RMB 100m)']
        
        lenlist=[]
        for m in itemlist:
            l=hzlen(m)
            lenlist=lenlist+[l]
        maxlen=max(lenlist)        
        
        import pandas as pd
        info=pd.DataFrame(columns=('type','item','number'))
        df1s0=df1[df1['type']=='总貌']
        for i in itemlist:
            row=pd.Series({'type':'总貌','item':i,'number':list(df1s0[i])[0]})
            info=info.append(row,ignore_index=True)            
        
        df1s2=df1[df1['type']=='创业板']
        for i in itemlist:
            row=pd.Series({'type':'创业板','item':i,'number':list(df1s2[i])[0]})
            info=info.append(row,ignore_index=True) 

        df2=df1[df1['type'].isin(['主板A股', '主板B股', '中小板'])]
        for i in itemlist:
            row=pd.Series({'type':'主板','item':i,'number':df2[i].sum()})
            info=info.append(row,ignore_index=True)         
        
        if lang == 'Chinese':
            print("\n=== 深圳证券交易所上市股票概况 ===\n")
        else:
             print("\n    Exchange Stock Summary： Shenzhen Stock Exchange\n")
             
        typelist=['总貌','主板','创业板']
        typeliste=['Stock overall','Main board','GEM board']
        
        for t in typelist:
            subdf=info[info['type']==t]
            if lang == 'Chinese':
                print('*** '+t+':')
            else:
                pos=typelist.index(t)
                te=typeliste[pos]
                print('*** '+te+':')
                
            for i in itemlist:
                blanknum=maxlen-hzlen(i)
                value=list(subdf[subdf['item']==i]['number'])[0]
                
                if lang == 'Chinese':
                    print('   ',i+' '*blanknum+'：',end='')
                else:
                    pos=itemlist.index(i)
                    ie=itemliste[pos]
                    print('   ',ie+' '*blanknum+'：',end='')
                    
                print("{:,}".format(value))
        
        if lang == 'Chinese':
            print("\n    注：主板包括了中小板，数据来源：深交所，",today)
        else:
            print("\n    Note: SMB board included in Main board\n    Source: Shenzhen Stock Exchange,",today)
        
        info=df
        
    return info

if __name__=='__main__':
    market_profile_china('SSE')
    market_profile_china('SZSE')

#==============================================================================
#==============================================================================
#==============================================================================
# 沪深市场详细信息
#==============================================================================
if __name__=='__main__':
    exchange='SZSE'
    category='price'
    
    df1sse1=market_detail_exchange_china(exchange='SSE',category='price')
    df1szse1=market_detail_exchange_china(exchange='SZSE',category='price')
    df1szse2=market_detail_exchange_china(exchange='SZSE',category='volume')
    df1szse3=market_detail_exchange_china(exchange='SZSE',category='return')
    df1szse4=market_detail_exchange_china(exchange='SZSE',category='valuation')


def market_detail_exchange_china(exchange='SSE',category='price'):
    """
    功能：给出中国当前最新的三大股票交易所的更多细节，单个交易所
    exchange：SSE, SZSE, BJSE
    输出：构造表格型数据框df，直接利用Jupyter Notebook格式输出
    数据来源：em东方财富
    """
    # 检查交易所
    exchange1=exchange.upper()
    exchlist=["SSE","SZSE","BJSE"]
    exchnamelist=["上海证券交易所","深圳证券交易所","北京证券交易所"]
    if not (exchange1 in exchlist):
        print("  #Error(market_detail_exchange_china): invalid exchange",exchange)
        print("  Valid exchange",exchlist)
        return None
    pos=exchlist.index(exchange1)
    exchname=exchnamelist[pos]  

    # 检查信息类别
    category1=category.upper()
    catelist=["PRICE","VOLUME","RETURN","VALUATION"]
    catenamelist=["当前股价","当前成交量","近期投资回报","市值与估值"]
    if not (category1 in catelist):
        print("  #Error(market_detail_exchange_china): invalid category",category)
        print(" Valid category",catelist)
        return None
    pos=catelist.index(category1)
    catename=catenamelist[pos]  
    
    # 获取交易所最新细节数据
    import akshare as ak
    try:
        if exchange1 == "SSE":
            df0=ak.stock_sh_a_spot_em()
        if exchange1 == "SZSE":
            df0=ak.stock_sz_a_spot_em()
        if exchange1 == "BJSE":
            df0=ak.stock_bj_a_spot_em()        
    except:
        print("  #Error(market_detail_exchange_china): info unavailable for",exchange,"\b, try again later")
        return None
        
    #DEBUG
    #print("  Check1:",len(df0))
    
    # 构造表格型数据框
    import pandas as pd
    item='项目'
    df1=pd.DataFrame(columns=(item,exchname))
    
    # 股票数量
    value=df0['代码'].count()
    dft=pd.DataFrame([["可交易股票数量",value]],columns=(item,exchname))
    df1=pd.concat([df1,dft],ignore_index=True)  
    numOfStocks=value
    
    #DEBUG
    #print("  Check2:",len(df1))


    if category1 == 'PRICE':
        # 大分类空行
        dft=pd.DataFrame([["股价价位",' ']],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)  

        # 昨收
        value=round(df0['昨收'].mean(),2)
        dft=pd.DataFrame([["    昨日收盘价均值",value]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)      

        # 今开
        value=round(df0['今开'].mean(),2)
        dft=pd.DataFrame([["    今日开盘价均值",value]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)      

        # 最新价
        value=round(df0['最新价'].mean(),2)
        dft=pd.DataFrame([["    最新价均值",value]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)      

        # 大分类空行
        dft=pd.DataFrame([["股价涨跌",' ']],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)  

        # 涨速
        value=round(df0['涨速'].mean(),4)
        dft=pd.DataFrame([["    当前涨速%",value]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)      

        # 5分钟涨跌
        value=round(df0['5分钟涨跌'].mean(),4)
        dft=pd.DataFrame([["    最近5分钟涨跌%",value]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)      

        # 大分类空行
        dft=pd.DataFrame([["今日与昨日相比",' ']],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)  

        # 振幅
        value=round(df0['振幅'].mean(),4)
        dft=pd.DataFrame([["    振幅均值%",value]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)    

        # 涨跌幅
        value=round(df0['涨跌幅'].mean(),4)
        dft=pd.DataFrame([["    涨跌幅均值%",value]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)    

        # 涨跌额
        value=round(df0['涨跌额'].mean(),2)
        dft=pd.DataFrame([["    涨跌额均值(元)",value]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)    
    
    #DEBUG
    #print("  Check3:",len(df1))


    if category1 == 'VOLUME':
        # 大分类空行
        dft=pd.DataFrame([["今日个股成交行情",' ']],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)  

        # 成交量
        value=round(df0['成交量'].mean()/10000,2)
        dft=pd.DataFrame([["    成交量均值(万手)",value]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)      

        # 成交额
        value=round(df0['成交额'].mean()/100000000,2)
        dft=pd.DataFrame([["    成交额均值(亿元)",value]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)      

        # 换手率
        value=round(df0['换手率'].mean(),2)
        dft=pd.DataFrame([["    换手率均值%",value]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)   

        # 大分类空行
        dft=pd.DataFrame([["今日与之前相比",' ']],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)  

        # 量比
        value=round(df0['量比'].mean(),2)
        dft=pd.DataFrame([["    量比均值(倍数)",value]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)      
    
    #DEBUG
    #print("  Check4:",len(df1))

    if category1 == 'RETURN':
        # 大分类空行
        dft=pd.DataFrame([["投资回报：近一季度",' ']],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)  

        # 60日涨跌幅
        value=round(df0['60日涨跌幅'].mean(),2)
        dft=pd.DataFrame([["    MRQ涨跌幅均值%",value]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)      

        value=round(df0['60日涨跌幅'].median(),2)
        dft=pd.DataFrame([["    MRQ涨跌幅中位数%",value]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)      

        value=round(df0['60日涨跌幅'].std(),2)
        dft=pd.DataFrame([["    MRQ涨跌幅标准差%",value]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True) 

        df0t=df0[df0['60日涨跌幅']>0]
        value=df0t['60日涨跌幅'].count()
        dft=pd.DataFrame([["    MRQ上涨股票占比%",round(value / numOfStocks *100,2)]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)         

        # 大分类空行
        dft=pd.DataFrame([["投资回报：年初至今",' ']],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)  

        # 年初至今涨跌幅
        value=round(df0['涨跌幅'].mean(),2)
        dft=pd.DataFrame([["    YTD涨跌幅均值%",value]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)      

        value=round(df0['年初至今涨跌幅'].median(),2)
        dft=pd.DataFrame([["    YTD涨跌幅中位数%",value]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)      

        value=round(df0['年初至今涨跌幅'].std(),2)
        dft=pd.DataFrame([["    YTD涨跌幅标准差%",value]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True) 

        df0t=df0[df0['年初至今涨跌幅']>0]
        value=df0t['年初至今涨跌幅'].count()
        dft=pd.DataFrame([["    YTD上涨股票占比%",round(value / numOfStocks *100,2)]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)         
    
    #DEBUG
    #print("  Check5:",len(df1))


    if category1 == 'VALUATION':
        # 大分类空行
        dft=pd.DataFrame([["总市值",' ']],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)  

        # 总市值
        value=round(df0['总市值'].sum() / 1000000000000,2)
        dft=pd.DataFrame([["    市场总市值(万亿元)",value]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)   
        totalMarketValue=value

        value=round(df0['总市值'].mean() / 1000000000,2)
        dft=pd.DataFrame([["    个股总市值均值(十亿元)",value]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)      

        value=round(df0['总市值'].median() / 1000000000,2)
        dft=pd.DataFrame([["    个股总市值中位数(十亿元)",value]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)      
        
        value=round(df0['总市值'].std() / 1000000000,2)
        dft=pd.DataFrame([["    个股总市值标准差(十亿元)",value]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)   
        
        # 大分类空行
        dft=pd.DataFrame([["流通市值",' ']],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)  

        # 流通市值
        value=round(df0['流通市值'].sum() / 1000000000000,2)
        dft=pd.DataFrame([["    市场流通市值(万亿元)",value]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)
        outstandingMarketValue=value

        # 流通比率
        value=round(outstandingMarketValue / totalMarketValue * 100,2)
        dft=pd.DataFrame([["    市场流通比率%",value]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)   
        
        value=round(df0['流通市值'].mean() / 1000000000,2)
        dft=pd.DataFrame([["    个股流通市值均值(十亿元)",value]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)      

        value=round(df0['流通市值'].median() / 1000000000,2)
        dft=pd.DataFrame([["    个股流通市值中位数(十亿元)",value]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)      

        value=round(df0['流通市值'].std() / 1000000000,2)
        dft=pd.DataFrame([["    个股流通市值标准差(十亿元)",value]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)      

        # 大分类空行
        dft=pd.DataFrame([["估值状况：市盈率",' ']],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)  

        # 市盈率-动态
        value=round(df0['市盈率-动态'].mean(),2)
        dft=pd.DataFrame([["    个股市盈率均值",value]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)  

        value=round(df0['市盈率-动态'].median(),2)
        dft=pd.DataFrame([["    个股市盈率中位数",value]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)  

        value=round(df0['市盈率-动态'].std(),2)
        dft=pd.DataFrame([["    个股市盈率标准差",value]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)  

        # 大分类空行
        dft=pd.DataFrame([["估值状况：市净率",' ']],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)  

        # 市净率
        value=round(df0['市净率'].mean(),2)
        dft=pd.DataFrame([["    个股市净率均值",value]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)  

        value=round(df0['市净率'].median(),2)
        dft=pd.DataFrame([["    个股市净率中位数",value]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)  

        value=round(df0['市净率'].std(),2)
        dft=pd.DataFrame([["    个股市净率标准差",value]],columns=(item,exchname))
        df1=pd.concat([df1,dft],ignore_index=True)  
    
    #DEBUG
    #print("  Check6:",len(df1))

    df1.set_index(item,inplace=True)
    
    #DEBUG
    #print("  Check7:",len(df1))
    
    return df1  


#==============================================================================
#==============================================================================
if __name__=='__main__':
    category='price'
    
    df1=market_detail_china(category='price')
    df1=market_detail_china(category='price')

def market_detail_china(category='price',prettytab=True,plttab=False, \
                        colWidth=0.3,tabScale=2,figsize=(10,6),fontsize=13,cellLoc='center'):
    """
    功能：给出中国当前最新的三大股票交易所的更多细节，合成
    输出：构造表格型数据框df，直接利用Jupyter Notebook格式输出
    数据来源：em东方财富
    """

    # 检查信息类别
    category1=category.upper()
    catelist=["PRICE","VOLUME","RETURN","VALUATION"]
    catenamelist=["当前股价","当前成交量","近期投资回报","市值与估值"]
    if not (category1 in catelist):
        print("  #Error(market_detail_exchange_china): invalid category",category)
        print(" Valid category",catelist)
        return None
    
    # 合并三大交易所
    import pandas as pd
    df=pd.DataFrame()
    exchlist=["SSE","SZSE","BJSE"]
    for e in exchlist:
        dft=market_detail_exchange_china(exchange=e,category=category)
        if dft is None:
            print("  #Error(market_detail_china): info inaccessible for",e,"\b, try later")
            return None
        
        if len(df)==0:
            df=dft
        else:
            df=pd.merge(df,dft,left_index=True,right_index=True)
    
    # 处理索引字段
    newcollist=['项目']+list(df)
    df['项目']=df.index
    df=df[newcollist]    

    # 将空缺值替换为空格
    df.fillna('',inplace=True)    
    
    import datetime as dt
    nowstr0=str(dt.datetime.now())
    nowstr=nowstr0[:19]
    
    # 前置空格个数
    heading=' '*1
    
    # 表格输出方式设置
    plttab = not prettytab
    
    if category1=='PRICE':
        titletxt="中国三大股票交易所横向对比：股价与涨跌"
        if prettytab:
            market_detail_china2table(df,titletxt=titletxt)
        if plttab:
            pandas2plttable(df,titletxt=titletxt,colWidth=colWidth,tabScale=tabScale, \
                            figsize=figsize,fontsize=fontsize,cellLoc=cellLoc)
        
        print(heading,"信息来源：东方财富，","统计时间:",nowstr)
        print(heading,"注：")
        print(heading,"☆昨日指的是上一个交易日")
        print(heading,"☆使用实时数据，不同日期/每天不同时刻统计的结果可能不同")
        print(heading,"☆若在非开市时间统计，部分结果数据可能出现空缺")
        print(heading,"☆涨速：平均每分钟股价变化率，表示股价变化速度")
        print(heading,"☆振幅：最高最低价差绝对值/昨收，表示股价变化活跃程度")
        print(heading,"☆涨跌幅：(最新价-昨收)/昨收，表示相对昨日的变化程度")
        print(heading,"☆涨跌额：最新价-昨收，，表示相对昨日的变化金额")
        print(heading,"☆5分钟涨跌：最新5分钟内股价的涨跌幅度")
        print(heading,"☆可交易股票数量：将随着股票停复牌情况变化")
    
    if category1=='VOLUME':
        titletxt="中国三大股票交易所横向对比：成交状况"
        if prettytab:
            market_detail_china2table(df,titletxt=titletxt)
        if plttab:
            pandas2plttable(df,titletxt=titletxt,colWidth=colWidth,tabScale=tabScale, \
                            figsize=figsize,fontsize=fontsize,cellLoc=cellLoc)

        print(heading,"信息来源：东方财富，","统计时间:",nowstr)
        print(heading,"注：")
        print(heading,"☆昨日指的是上一个交易日")
        print(heading,"☆使用实时数据，不同日期/每天不同时刻统计的结果可能不同")
        print(heading,"☆若在非开市时间统计，部分结果数据可能出现空缺")
        print(heading,"☆量比：当前平均每分钟成交量与过去5个交易日均值之比，表示当前成交量的变化")
        print(heading,"☆成交量：当前成交股数，表示交易活跃度")
        print(heading,"☆换手率：成交量/流通股数，表示成交量占比")
        print(heading,"☆成交额：当前开市后的累计成交金额")
        print(heading,"☆可交易股票数量：将随着股票停复牌情况变化")
    
    if category1=='RETURN':
        titletxt="中国三大股票交易所横向对比：投资回报"
        if prettytab:
            market_detail_china2table(df,titletxt=titletxt)
        if plttab:
            pandas2plttable(df,titletxt=titletxt,colWidth=colWidth,tabScale=tabScale, \
                            figsize=figsize,fontsize=fontsize,cellLoc=cellLoc)
        
        print(heading,"信息来源：东方财富，","统计时间:",nowstr)
        print(heading,"注：")
        print(heading,"☆昨日指的是上一个交易日")
        print(heading,"☆使用实时数据，不同日期/每天不同时刻统计的结果可能不同")
        print(heading,"☆若在非开市时间统计，部分结果数据可能出现空缺")
        print(heading,"☆MRQ：最近一个季度，即最近60个交易日")
        print(heading,"☆YTD：今年以来的累计情况")
        print(heading,"☆可交易股票数量：将随着股票停复牌情况变化")
    
    if category1=='VALUATION':
        titletxt="中国三大股票交易所横向对比：市值与估值"
        if prettytab:
            market_detail_china2table(df,titletxt=titletxt)
        if plttab:
            pandas2plttable(df,titletxt=titletxt,colWidth=colWidth,tabScale=tabScale, \
                            figsize=figsize,fontsize=fontsize,cellLoc=cellLoc)
        
        print(heading,"信息来源：东方财富，","统计时间:",nowstr)
        print(heading,"注：")
        print(heading,"☆昨日指的是上一个交易日")
        print(heading,"☆使用实时数据，不同日期/每天不同时刻统计的结果可能不同")
        print(heading,"☆若在非开市时间统计，部分结果数据可能出现空缺")
        print(heading,"☆市净率：这里为静态市盈率，按季/中/年报计算")
        print(heading,"☆市盈率：这里为动态市盈率，即市盈率TTM，过去12个月的连续变化")
        print(heading,"☆可交易股票数量：将随着股票停复牌情况变化")
    
    return df

#==============================================================================
if __name__=='__main__':
    titletxt="This is a title"
    leftColAlign='l'
    otherColAlign='c'
    tabborder=False


def market_detail_china2table(df,titletxt,firstColSpecial=True,leftColAlign='l',otherColAlign='c',tabborder=False):
    """
    功能：将一个df转换为prettytable格式，打印，在Jupyter Notebook下整齐
    专门为函数market_detail_china制作，不包括索引字段
    """  
    #列名列表
    col=list(df)
    
    # 第一列长度取齐处理
    if firstColSpecial:
        #第一列的最长长度
        firstcol=list(df[col[0]])
        maxlen=0
        for f in firstcol:
            flen=hzlen(f)
            if flen > maxlen:
                maxlen=flen
        
        #将第一列内容的长度取齐
        df[col[0]]=df[col[0]].apply(lambda x:equalwidth(x,maxlen=maxlen,extchar=' ',endchar=' '))    

    collist=list(df)
    
    from prettytable import PrettyTable
    import sys
    # 传入的字段名相当于表头
    tb = PrettyTable(collist, encoding=sys.stdout.encoding) 
    
    for i in range(0, len(df)): 
        tb.add_row(list(df.iloc[i]))
    
    firstcol=collist[0]
    restcols=collist[1:]
    tb.align[firstcol]=leftColAlign
    for e in restcols:
        tb.align[e]=otherColAlign
    
    # 边框设置：使用dir(tb)查看属性
    import prettytable as pt
    if not tabborder:
        # 无边框
        #tb.set_style(pt.PLAIN_COLUMNS) 
        # 空一行，分离标题行与表体
        #print()
        tb.junction_char=' '
        tb.horizontal_char=' '
        tb.vertical_char=' '
    
    # 设置标题
    tb.title=titletxt
    
    print(tb)
    
    return
    
#==============================================================================
#==============================================================================
#==============================================================================
#==============================================================================
#==============================================================================
