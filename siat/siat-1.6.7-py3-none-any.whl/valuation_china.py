# -*- coding: utf-8 -*-
"""
本模块功能：中国股市估值
作者：王德宏 (WANG Dehong, Peter)
作者单位：北京外国语大学国际商学院
作者邮件：wdehong2000@163.com
版权所有：王德宏
用途限制：仅限研究与教学使用，不可商用！商用需要额外授权。
特别声明：作者不对使用本工具进行证券投资导致的任何损益负责！
"""
#==============================================================================
#屏蔽所有警告性信息
import warnings; warnings.filterwarnings('ignore')
#==============================================================================
from siat.common import *
from siat.translate import *
from siat.grafix import *
from siat.security_prices import *
from siat.sector_china import *

#==============================================================================

if __name__ =="__main__":
    start='2020-1-1'; end='2022-10-9'
    measure='pb'; method='lyr'; value='value'; statistic='median'

def get_valuation_market_china(start,end,measure='pe',method='lyr',value='value',statistic='median'):
    """
    功能：中国A股市场估值趋势，一段时间内
    measure：默认市盈率'pe'，可选市净率pb
    method：默认滚动'ttm'，可选静态lyr
    value：默认数值'value'，可选分位数quantile
    statistic：默认使用中位数'median'，可选等权重equal-weighted
    """
    
    #检查日期的合理性
    result,startpd,endpd=check_period(start,end)
    if not result:
        print("  #Error(get_valuation_market_china): invalid date period",start,end)
        return None
    
    #检查选项
    measure1=measure.lower(); measurelist=['pe','pb']
    method1=method.lower(); methodlist=['ttm','lyr']
    value1=value.lower(); valuelist=['value','quantile']
    statistic1=statistic.lower(); statisticlist=['median','equal-weighted']
    
    if not (measure1 in measurelist):
        print("  #Error(get_valuation_market_china): invalid measurement",measure)
        print("  Valid measurement:")
        return None
    if not (method1 in methodlist):
        print("  #Error(get_valuation_market_china): invalid method",method)
        print("  Valid method:",methodlist)
        return None    
    if not (value1 in valuelist):
        print("  #Error(get_valuation_market_china): invalid value",value)
        print("  Valid value:",valuelist)
        return None
    if not (statistic1 in statisticlist):
        print("  #Error(get_valuation_market_china): invalid statistic",statistic)
        print("  Valid statistic:",statisticlist)
        return None

    # 构造组合矩阵   
    import pandas as pd
    matrix=pd.DataFrame([
        #['pe ttm value median','middlePETTM','市盈率(滚动TTM，全A股中位数)'],
        #['pe ttm value equal-weighted','averagePETTM','市盈率(滚动TTM，全A股等权平均)'],
        #['pe ttm quantile median','quantileInRecent10YearsMiddlePeTtm','市盈率分位数(滚动TTM，全A股中位数，近10年)'],
        #['pe ttm quantile equal-weighted','quantileInRecent10YearsAveragePeTtm','市盈率分位数(滚动TTM，全A股等权平均，近10年)'],
         
        #['pe lyr value median','middlePELYR','市盈率(静态LYR，全A股中位数)'],
        #['pe lyr value equal-weighted','averagePELYR','市盈率(静态LYR，全A股等权平均)'],
        #['pe lyr quantile median','quantileInRecent10YearsMiddlePeLyr','市盈率分位数(静态LYR，全A股中位数，近10年)'],
        #['pe lyr quantile equal-weighted','quantileInRecent10YearsAveragePeLyr','市盈率分位数(静态LYR，全A股等权平均，近10年)'],
         
        #['pb lyr value median','middlePB','市净率(静态LYR，全A股中位数)'],
        #['pb lyr value equal-weighted','equalWeightAveragePB','市净率(静态LYR，全A股等权平均)'],
        #['pb lyr quantile median','quantileInRecent10YearsMiddlePB','市净率分位数(静态LYR，全A股中位数，近10年)'],
        #['pb lyr quantile equal-weighted','quantileInRecent10YearsEqualWeightAveragePB','市净率分位数(静态LYR，全A股等权平均，近10年)'],
        
        ['pe ttm value median','middlePETTM','市盈率(TTM，全A股中位数)'],
        ['pe ttm value equal-weighted','averagePETTM','市盈率(TTM，全A股等权平均)'],
        ['pe ttm quantile median','quantileInRecent10YearsMiddlePeTtm','市盈率分位数(TTM，全A股近十年中位数)'],
        ['pe ttm quantile equal-weighted','quantileInRecent10YearsAveragePeTtm','市盈率分位数(TTM，全A股近十年等权平均)'],
         
        ['pe lyr value median','middlePELYR','市盈率(全A股中位数)'],
        ['pe lyr value equal-weighted','averagePELYR','市盈率(全A股等权平均)'],
        ['pe lyr quantile median','quantileInRecent10YearsMiddlePeLyr','市盈率分位数(全A股近十年中位数)'],
        ['pe lyr quantile equal-weighted','quantileInRecent10YearsAveragePeLyr','市盈率分位数(全A股近十年等权平均)'],
         
        ['pb lyr value median','middlePB','市净率(全A股中位数)'],
        ['pb lyr value equal-weighted','equalWeightAveragePB','市净率(全A股等权平均)'],
        ['pb lyr quantile median','quantileInRecent10YearsMiddlePB','市净率分位数(全A股近十年中位数)'],
        ['pb lyr quantile equal-weighted','quantileInRecent10YearsEqualWeightAveragePB','市净率分位数(全A股近十年等权平均)'],
        
        ], columns=['combine','field','desc'])

    #查找组合方式对应的字段名称
    combine=measure1+' '+method1+' '+value1+' '+statistic1
    try:
        field=matrix[matrix['combine']==combine]['field'].values[0]
        desc=matrix[matrix['combine']==combine]['desc'].values[0]
    except:
        #未查到组合
        print("  #Error(get_valuation_market_china): parameter combination not available for",combine)
        return None

    import akshare as ak
    
    #获取全A股市场的市盈率
    if measure1 == 'pe':
        try:
            mp = ak.stock_a_ttm_lyr()
        except:
            #akshare版本需要更新
            print("  #Error(get_valuation_market_china): may need to upgrade akshare")
            return None
    
        #截取选定的日期范围
        mp['Date']=mp['date']
        mp.sort_values(by=['Date'],ascending=True,inplace=True)
        mp.set_index(['Date'],inplace=True) 
        mp1=mp[(mp.index >= startpd) & (mp.index <=endpd)]
        
        mp9=mp1[['date',field,'close']]
        mp9['field']=mp9[field]
        mp9['index']=mp9['close']
        mp9['index name']="沪深300指数"
        mp9['measure']=measure1
        mp9['method']=method1
        mp9['value']=value1
        mp9['statistic']=statistic1
        mp9['desc']=desc
    
    
    #获取全A股市场的市净率
    if measure1 == 'pb':
        try:
            mp = ak.stock_a_all_pb()
        except:
            #akshare版本需要更新
            print("  #Error(get_valuation_market_china): may need to upgrade akshare")
            return None
    
        #截取选定的日期范围
        mp['Date']=mp['date']
        mp.sort_values(by=['Date'],ascending=True,inplace=True)
        mp.set_index(['Date'],inplace=True) 
        mp1=mp[(mp.index >= startpd) & (mp.index <=endpd)]
        
        mp9=mp1[['date',field,'close']]
        mp9['field']=mp9[field]
        mp9['index']=mp9['close']
        mp9['index name']="上证综合指数"
        mp9['measure']=measure1
        mp9['method']=method1
        mp9['value']=value1
        mp9['statistic']=statistic1
        mp9['desc']=desc
        
    df=mp9[['date','field','index','index name','measure','method','value','statistic','desc']]
    
    return df    

if __name__ =="__main__":
    start='2020-1-1'; end='2022-10-9'
    df=get_valuation_market_china(start,end,measure='pe',method='lyr',value='value',statistic='median')

#==============================================================================
if __name__ =="__main__":
    start='2020-1-1'; end='2022-10-9'
    measures=['pb','pe']; methods='lyr'; values='value'; statistics='median'
    
    measures='pe'; methods=['lyr','ttm']; values='value'; statistics='median'


def valuation_market_china(start,end,measures=['pe','pb'], \
                           methods='lyr',values='value',statistics='median', \
                           twinx='auto',loc1='best',loc2='best'):
    """
    功能：比较中国全A股市场的估值指标变化趋势
    ----------
    start: 开始日期
    end: 结束日期
    measures: 估值指标市盈率'pe'或市净率'pb'
    methods: 滚动'ttm/静态取样'lyr'.
    values: 直接采用估值指标数值'value'或分位数'quantile'
    statistics: 采用中位数'median'或等权均值'equal-weighted'

    """
    
    #解析比较的指标，以第一个双指标为准
    found2=False
    parmlist=['measures','methods','values','statistics']
    for v in parmlist:
        
        #如果是一个字符串
        if isinstance(eval(v),str): 
            globals()[v+'1']=eval(v)
            globals()[v+'2']=eval(v)

        #如果是一个列表
        if isinstance(eval(v),list): 
            num = len(eval(v))
            #print("num=",num)
            
            if num == 0:
                print("  #Error(valuation_market_china)：need at least 1 parameter for",eval(v))
                return None,None
            
            if num == 1:
                globals()[v+'1']=eval(v)[0]
                globals()[v+'2']=eval(v)[0]
            
            
            if num >= 2:
                globals()[v+'1']=eval(v)[0]
                globals()[v+'2']=eval(v)[1]
                found2=True
                
    if not found2:
        print("  #Warning(valuation_market_china)：no comparing parameters from either of",parmlist)
        #return None,None
    """            
    print("measures1=",measures1,"measures2=",measures2)
    print("methods1=",methods1,"methods2=",methods2)
    print("values1=",values1,"values2=",values2)
    print("statistics1=",statistics1,"statistics2=",statistics2)
    """
    
    if values=='value':
        ylabeltxt='估值比率'
    else:
        ylabeltxt='分位数'
    titletxt='中国全A股市场估值的变化趋势'
    
    import datetime
    today = datetime.date.today()
    footnote="数据来源: 乐咕乐股，"+str(today)
    
    #获取指标1
    df1=get_valuation_market_china(start,end,measure=measures1,method=methods1,value=values1,statistic=statistics1)
    if df1 is None:
        print("  #Error(valuation_market_china)：no data available for the combination of",measures1,methods1,values1,statistics1)
        return None,None
    
    ticker1=df1['desc'].values[0]
    colname1='field'
    label1=''
    
    if not found2:  
        plot_line(df1,colname1,ticker1,ylabeltxt,titletxt,footnote, \
                      power=0,loc=loc1, \
                      date_fmt='%Y-%m-%d')
        return df1,None

    #获取指标2
    df2=get_valuation_market_china(start,end,measure=measures2,method=methods2,value=values2,statistic=statistics2)
    if df2 is None:
        print("  #Error(valuation_market_china)：no data available for the combination of",measures2,methods2,values2,statistics2)
        return None,None
    
    ticker2=df2['desc'].values[0]
    colname2='field'
    label2=''
    
    if twinx == 'auto':
        twinx=False
        
        max1=df1[colname1].max()
        max2=df2[colname2].max()
        bili=max1/max2
        if (bili > 2) or (bili < 0.5):
            twinx=True
    
    plot2_line2(df1,ticker1,colname1,label1, \
               df2,ticker2,colname2,label2, \
               ylabeltxt,titletxt,footnote, \
               twinx=twinx,loc1=loc1,loc2=loc2)
    #清除变量
    #"""    
    for v in parmlist:
        del globals()[v+'1'],globals()[v+'2']
    #"""
    
    return df1,df2

if __name__ =="__main__":
    start='2020-1-1'; end='2022-10-9'
    measures=['pe','pb']; methods='lyr'; values='value'; statistics='median'
    df1,df2=valuation_market_china(start,end,measures=['pe','pb'],methods='lyr',values='value',statistics='median')

#==============================================================================
# 行业估值：申万宏远行业，韭圈儿
#==============================================================================
if __name__=='__main__':
    top=5
    vtype='PE'
    vsorting='quantile'
    printout=True
    graph=True
    axisamp=3
    px=False
    
def industry_valuation_sw(top=10,vtype='PE',vsorting='quantile', \
                          graph=True,axisamp=1.2,px=False):
    """
    功能：列示申万行业指数估值最高和最低的行业
    vtype: PE, PB, dividend
    vsorting: 分位数绝对值
    """
    
    import akshare as ak
    df = ak.index_value_name_funddb()    
    
    # 筛选申万行业指数
    substr='(申万)'
    df['申万标志']=df['指数名称'].apply(lambda x: substr in x)
    df1=df[df['申万标志']]
    df1['行业代码']=df1['指数代码'].apply(lambda x: x[:6])
    df1['行业名称']=df1['指数名称'].apply(lambda x: x[:x.index(substr)])
    
    #检查估值类型
    typelist=['pe','pb','dividend']
    vtypeu=vtype.lower()
    if not (vtypeu in typelist):
        print("  #Warning(industry_valuation_sw): unsupported valuation type",vtype)
        print("  Supported types:",typelist)
        return None
    
    #检查排序类型
    sortlist=['quantile','value']
    vsortingu=vsorting.lower()
    if not (vsortingu in sortlist):
        print("  #Warning(industry_valuation_sw): unsupported sorting type",vsorting)
        print("  Supported types:",sortlist)
        return None
    
    #排序：高位优先
    if vtypeu == 'pe':
        if vsortingu == 'value':
            df2=df1.sort_values(by='最新PE',ascending=False)
            collist=['行业名称','最新PE','PE分位','最新PB','PB分位','股息率','股息率分位','行业代码']
            colname='最新PE'
        else:
            df2=df1.sort_values(by='PE分位',ascending=False)
            collist=['行业名称','PE分位','最新PE','PB分位','最新PB','股息率','股息率分位','行业代码']
            colname='PE分位'
        
    if vtypeu == 'pb':
        if vsortingu == 'value':
            df2=df1.sort_values(by='最新PB',ascending=False)
            collist=['行业名称','最新PB','PB分位','最新PE','PE分位','股息率','股息率分位','行业代码']
            colname='最新PB'
        else:
            df2=df1.sort_values(by='PB分位',ascending=False)
            collist=['行业名称','PB分位','最新PB','最新PE','PE分位','股息率','股息率分位','行业代码']
            colname='PB分位'
        
    if vtypeu == 'dividend':
        if vsortingu == 'value':
            df2=df1.sort_values(by='股息率',ascending=False)
            collist=['行业名称','股息率','股息率分位','最新PB','PB分位','最新PE','PE分位','行业代码']
            colname='股息率'
        else:
            df2=df1.sort_values(by='股息率分位',ascending=False)
            collist=['行业名称','股息率分位','股息率','最新PB','PB分位','最新PE','PE分位','行业代码']
            colname='股息率分位'
            
    df2.reset_index(drop=True,inplace=True)
    df2.index=df2.index+1
    df3=df2[collist]
    
    if top > 0:
        df4=df3.head(top)
    elif top < 0:
        df4=df3.tail(-top)
    else:
        df4=df3
    df5=df4.set_index('行业名称')
    df5.sort_values(by=colname,ascending=True,inplace=True)

    #绘图
    if graph:
        if top > 0:
            prefix="最高的"
        else:
            prefix="最低的"

        if vsortingu=='quantile':
            suffix="数百分比"
            footnote1="分位数表示历史上比当前便宜的百分比，"
        else:
            suffix="数值"
            footnote1=''
            
        titletxt="估值分析：基于"+colname+suffix+"，"+prefix+str(abs(top))+"个行业"
        
        import datetime
        today = datetime.date.today()
        footnote0="注：申万宏源行业分类，"
        footnote2="数据来源: 申万宏源/韭圈儿，"+str(today)
        footnote=footnote0+footnote1+footnote2
        
        if not px:
            fig=plot_barh(df5,colname,titletxt,footnote,axisamp=axisamp)
        else:
            fig=plot_barh2(df5,colname,titletxt,footnote)
        
    return df2

if __name__=='__main__':
    df=industry_valuation_sw(top=10,vtype='PE',vsorting='quantile',axisamp=2.3)
    df=industry_valuation_sw(top=-10,vtype='PE',vsorting='quantile',axisamp=1.2)
    df=industry_valuation_sw(top=10,vtype='PE',vsorting='value',axisamp=1.5)
    df=industry_valuation_sw(top=-10,vtype='PE',vsorting='value',axisamp=1.6)
    
    df=industry_valuation_sw(top=10,vtype='PB',vsorting='quantile',axisamp=2.1)
    df=industry_valuation_sw(top=-10,vtype='PB',vsorting='quantile',axisamp=1.2)
    df=industry_valuation_sw(top=10,vtype='PB',vsorting='value',axisamp=2)
    df=industry_valuation_sw(top=-10,vtype='PB',vsorting='value',axisamp=1.6)
    
    df=industry_valuation_sw(top=10,vtype='dividend',vsorting='quantile',axisamp=32)
    df=industry_valuation_sw(top=-10,vtype='dividend',vsorting='quantile',axisamp=1.2) 
    df=industry_valuation_sw(top=10,vtype='dividend',vsorting='value',axisamp=2)
    df=industry_valuation_sw(top=-10,vtype='dividend',vsorting='value',axisamp=1.3)    
#==============================================================================
#==============================================================================
if __name__=='__main__':
    industry='食品饮料'
    start='2021-1-1'
    end='2022-11-15'
    vtype='PE'
    
    graph=True
    loc='best'
    
def industry_valuation_history_sw(industry,start,end,vtype='PE', \
                                  graph=True,loc='best'):
    """
    功能：绘制一个申万行业的历史估值趋势
    vtype: PE, PB, dividend
    
    """
    #检查日期期间
    result,start1,end1=check_period(start,end)
    if not result:
        print("  #Warning(industry_valuation_history_sw): invalid date period",start,end)
        return None
    
    #检查估值类型
    typelist=['pe','pb','dividend']
    vtypeu=vtype.lower()
    if not (vtypeu in typelist):
        print("  #Warning(industry_valuation_history_sw): unsupported valuation type",vtype)
        print("  Supported types:",typelist)
        return None

    vtypelist=['pe','pb','dividend']
    typelist=['市盈率','市净率','股息率']
    pos=vtypelist.index(vtypeu)
    vtypes=typelist[pos]

    # 获取行业估值历史数据
    import akshare as ak
    sindustry=industry+'(申万)'
    try:
        df = ak.index_value_hist_funddb(symbol=sindustry, indicator=vtypes)  
    except:
        print("  #Warning(industry_valuation_history_sw): industry not found",industry)
        return None

    import pandas as pd
    df['date']=pd.to_datetime(df['日期'])
    df.set_index('date',inplace=True)
    df1=df[[vtypes]]
    
    #筛选期间
    df2=df1[(df1.index >= start1) & (df1.index <= end1)]

    #绘图
    if graph:
        df2['平均值']=df2[vtypes].mean()
        df2['中位数']=df2[vtypes].median()
        
        titletxt="行业估值趋势："+industry+'，'+vtypes   
        
        footnote0="注：申万宏源行业指数，"
        footnote1=''
        import datetime
        today = datetime.date.today()
        footnote2="数据来源: 申万宏源/韭圈儿，"+str(today)
        footnote=footnote0+footnote1+footnote2
        
        colname=vtypes
        collabel=vtypes
        ylabeltxt=vtypes
        
        draw_lines(df2,y_label=ylabeltxt,x_label=footnote, \
                   axhline_value=0,axhline_label='', \
                   title_txt=titletxt,data_label=False,resample_freq='D')
        
    return df2

if __name__=='__main__':
    df=industry_valuation_history_sw(industry,start,end,vtype='PE')
    df=industry_valuation_history_sw(industry,start,end,vtype='PB')
    df=industry_valuation_history_sw(industry,start,end,vtype='dividend')
    
    df=industry_valuation_history_sw(industry='纺织服饰',start=start,end=end,vtype='PE')
    df=industry_valuation_history_sw(industry='纺织服饰',start=start,end=end,vtype='PB')
    df=industry_valuation_history_sw(industry='纺织服饰',start=start,end=end,vtype='dividend')

#==============================================================================
if __name__=='__main__':
    industries=['食品饮料','纺织服饰']
    start='2021-1-1'
    end='2022-11-15'
    vtypes='PE'
    
    industries='纺织服饰'
    vtypes=['PE','PB']
    
    graph=True
    loc1='lower left'
    loc2='upper right'

def compare_industry_valuation_sw(industries,start,end,vtypes='PE', \
                                  graph=True,loc1='best',loc2='best'):
    """
    功能：比较多个申万行业或者两个指标的历史估值趋势
    条件：若industries为列表且多个，则取vtype的第一个值；
    若industries为字符串或者列表但只有一个，则取vtype的前两个值比较，双轴
    vtypes: PE, PB, dividend
    
    """
    
    #检查日期期间的合理性
    
    
    vtypelist=['pe','pb','dividend']
    typelist=['市盈率','市净率','股息率']

    #检查行业个数：多个行业+单指标
    if isinstance(industries,list) & (len(industries) >= 2):
        
        if isinstance(vtypes,str): 
            vtype=vtypes
        elif isinstance(vtypes,list): 
            vtype=vtypes[0]

        vtypeu=vtype.lower()
        pos=vtypelist.index(vtypeu)
        vtypec=typelist[pos]
        
        import pandas as pd
        df=pd.DataFrame()        
        for i in industries:
            dft=industry_valuation_history_sw(i,start=start,end=end,vtype=vtype,graph=False)
            if not (dft is None):
                dft.rename(columns={vtypec:i},inplace=True)
                if len(df) == 0:
                    df=dft
                else:
                    df=pd.merge(df,dft,how='outer',left_index=True,right_index=True)
            else:
                continue
            
        #绘图
        if graph:
            titletxt="行业估值趋势对比："+vtypec   
            
            footnote0="注：申万宏源行业指数，"
            footnote1=''
            import datetime
            today = datetime.date.today()
            footnote2="数据来源: 申万宏源/韭圈儿，"+str(today)
            footnote=footnote0+footnote1+footnote2
            
            ylabeltxt=vtypec
            
            draw_lines(df,y_label=ylabeltxt,x_label=footnote, \
                       axhline_value=0,axhline_label='', \
                       title_txt=titletxt,data_label=False,resample_freq='D')

        return df

    #检查行业个数：一个行业+双指标
    if  ((isinstance(industries,str) | (isinstance(industries,list) & (len(industries) == 1)))) \
        & (isinstance(vtypes,list) & (len(vtypes) >= 2)):
        
        if isinstance(industries,str): 
            industry=industries
        elif isinstance(industries,list): 
            industry=industries[0]
        
        if isinstance(vtypes,str): 
            ivtypelist=[vtypes]
        elif isinstance(vtypes,list): 
            ivtypelist=vtypes[:2]
        
        import pandas as pd
        df=pd.DataFrame()        
        for t in ivtypelist:
            
            dft=industry_valuation_history_sw(industry,start=start,end=end,vtype=t,graph=False)
            
            if len(df) == 0:
                df=dft
            else:
                df=pd.merge(df,dft,how='outer',left_index=True,right_index=True)
                
        #绘图
        if graph:
            titletxt="行业估值趋势对比："+industry   
            
            footnote0="注：申万宏源行业指数，"
            footnote1=''
            import datetime
            today = datetime.date.today()
            footnote2="数据来源: 申万宏源/韭圈儿，"+str(today)
            footnote=footnote0+footnote1+footnote2
            
            collist=list(df)
            colname1=label1=collist[0]
            colname2=label2=collist[1]
            
            plot_line2(df,'',colname1,label1, \
                       df,'',colname2,label2, \
                           ylabeltxt='',titletxt=titletxt,footnote=footnote, \
                           twinx=True, \
                           resample_freq='D',loc1=loc1,loc2=loc2, \
                           color1='red',color2='blue')
            
        return df

    #检查行业个数：一个行业+一个指标
    if  ((isinstance(industries,str) | (isinstance(industries,list) & (len(industries) == 1)))) \
        & ((isinstance(vtypes,str) | (isinstance(vtypes,list) & (len(vtypes) == 1)))):

        if isinstance(industries,str): 
            industry=industries
        elif isinstance(industries,list): 
            industry=industries[0]
        
        if isinstance(vtypes,str): 
            ivtype=vtypes
        elif isinstance(vtypes,list): 
            ivtype=vtypes[0]
            
        df=industry_valuation_history_sw(industry,start,end,vtype=ivtype, \
                                          graph=graph,loc=loc1)
        return df
            
if __name__=='__main__':
    df=compare_industry_valuation_sw(industries=['纺织服饰','国防军工','食品饮料'], \
                                     start='2017-1-1',end='2022-11-15', \
                                     vtypes='PE',loc1='lower left',loc2='upper right')

    df=compare_industry_valuation_sw(industries=['纺织服饰'], \
                                     start='2017-1-1',end='2022-11-15', \
                                     vtypes='PE',loc1='lower left',loc2='upper right')

    df=compare_industry_valuation_sw(industries=['纺织服饰'], \
                                     start='2017-1-1',end='2022-11-15', \
                                     vtypes=['PE','PB'],loc1='lower left',loc2='upper right')

#==============================================================================
#==============================================================================
if __name__=='__main__':
    end='2022-11-18'
    start=date_adjust(end,-365*5)
    valuation=['PE','PB','dividend']
    return_delay=['Annual','Quarterly','Monthly']
    industries='all'
    
    lo_est_betas_list,betas_list,idfall=valuation2return_sw(start,end,valuation=valuation,return_delay=return_delay)

def valuation2return_sw2(start,end,valuation=['PE','PB','dividend'], \
                        return_delay=['Annual','Quarterly','Monthly'], \
                            industries='all'):
    """
    废弃！!!
    功能：测试估值指标对滞后一段时间收益率的影响。若正向（负向）影响，行业估值未低估（高估）
    start, end: 测试期间
    valuation: 估值指标，可为单项指标或列表。市盈率PE, 市净率PB, 股息率dividend
    return_delay: 滞后时间长度，可为单项指标或列表。Monthly一个月=21天，Quarterly一个季度=63天，Annual一年=252天
    """
    # 检查日期的合理性

    # 检查估值指标的类型
    valuationlist=['pe','pb','dividend']
    if isinstance(valuation,str):
        valuation_list=[valuation]
    elif isinstance(valuation,list):
        valuation_list=valuation
    for v in valuation_list:
        if not (v.lower() in valuationlist):
            print("  #Warning(valuation2return_sw): unsupported type of valuation:",v)
            print("  supported types of valuation:",valuationlist)
            return None

    # 检查估值指标的类型
    return_delaylist=['annual','quarterly','monthly']
    measurelist=['Annual Ret','Quarterly Ret','Monthly Ret']
    shiftlist=[252,63,21]
    
    if isinstance(return_delay,str):
        return_delay_list=[return_delay]
    elif isinstance(return_delay,list):
        return_delay_list=return_delay
        
    measure_list=[]
    shift_days_list=[]
    for v in return_delay_list:
        if not (v.lower() in return_delaylist):
            print("  #Warning(valuation2return_sw): unsupported type of return delay:",v)
            print("  supported types of return delay:",return_delaylist)
            return None
        
        pos=return_delaylist.index(v.lower())
        measure=measurelist[pos]
        measure_list=measure_list+[measure]
        shift_days=shiftlist[pos]
        shift_days_list=shift_days_list+[shift_days]

    # 获取行业历史数据，本步骤所需时间较长=========================================
    industry_data=get_industry_sw('I')
    if not (industries.lower() == 'all'):
        industry_codes=industry_sw_codes(industries)
    else:
        industry_codes=list(set(list(industry_data['ticker'])))
    
    # 计算基础数据，本步骤所需时间较长============================================
    idf,idfall=calc_industry_sw(industry_data,start,end)

    # 构造回归数据，进行回归，记录回归结果
    import pandas as pd
    from scipy import stats

    #屏蔽函数内print信息输出的类
    import os, sys
    class HiddenPrints:
        def __enter__(self):
            self._original_stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')

        def __exit__(self, exc_type, exc_val, exc_tb):
            sys.stdout.close()
            sys.stdout = self._original_stdout
    
    betas_list=[]
    lo_est_betas_list=[]
    print("Calculating industry valuations, it may take great time, please wait ...")
    for m in measure_list:
        
        #计算收益率
        ret_df=compare_industry_sw(idfall,industry_codes,measure=m,graph=False)
        industry_names=list(ret_df)
        pos=measure_list.index(m)
        d=shift_days_list[pos]
    
        ret_collist=list(ret_df)
        ret_reg=pd.DataFrame()
        # 构造用于回归的数据结构    
        for i in ret_collist:
            tmpdf=ret_df[[i]]
            tmpdf['行业']=i
            tmpdf.rename(columns={i:'ret'},inplace=True)
            
            if len(ret_reg)==0:
                ret_reg=tmpdf
            else:
                ret_reg=ret_reg.append(tmpdf)
        
        # 计算估值指标
        for val in valuation_list:
            with HiddenPrints():
                val_df=compare_industry_valuation_sw(industry_names,start=start,end=end,
                                                 vtypes=val,graph=False)
            
            # 滞后估值指标
            val_df2=val_df.shift(d)
            val_collist=list(val_df2)
            val_reg=pd.DataFrame()
            
            for i in val_collist:
                tmpdf=val_df2[[i]]
                tmpdf['行业']=i
                tmpdf.rename(columns={i:val},inplace=True)
                
                if len(val_reg)==0:
                    val_reg=tmpdf
                else:
                    val_reg=val_reg.append(tmpdf)
        
            #合成    
            val_reg['日期']=val_reg.index
            ret_reg['日期']=ret_reg.index
            
            df_reg=val_reg.merge(ret_reg,how='inner',on=['日期','行业'])
            df_reg.set_index('日期',inplace=True)
            
            df_reg.dropna(inplace=True)
            
            output=stats.linregress(df_reg[val],df_reg['ret'])
            (beta,alpha,r_value,p_value,std_err)=output
            
            if p_value < 0.001: siglevel='***'
            elif p_value < 0.01: siglevel='** '
            elif p_value < 0.05: siglevel='*  '
            else: siglevel='   '
            r_sqr=round(r_value**2,4)
            
            betas=pd.DataFrame(columns=('估值指标','收益率指标','行业','截距','估值系数','p值','显著性','R-sqr'))
            row=pd.Series({'估值指标':val,'收益率指标':m,'行业':'全行业','截距':alpha,'估值系数':beta, \
                           'p值':p_value,'显著性':siglevel,'R-sqr':r_sqr})
            betas=betas.append(row,ignore_index=True) 
            
            industry_list=list(set(list(df_reg['行业']))) 
            for i in industry_list:
                dftmp=df_reg[df_reg['行业']==i]
                
                output=stats.linregress(dftmp[val],dftmp['ret'])
                (beta,alpha,r_value,p_value,std_err)=output
                
                if p_value < 0.001: siglevel='***'
                elif p_value < 0.01: siglevel='** '
                elif p_value < 0.05: siglevel='*  '
                else: siglevel='   '
                r_sqr=round(r_value**2,4)
                
                row=pd.Series({'估值指标':val,'收益率指标':m,'行业':i,'截距':alpha,'估值系数':beta, \
                               'p值':p_value,'显著性':siglevel,'R-sqr':r_sqr})
                betas=betas.append(row,ignore_index=True) 
            
            if val.lower() in ['pe','pb']:
                betas['估值判断']=betas['估值系数'].apply(lambda x: '可能高估' if x <0 else '可能低估')
                betas.sort_values(by=['估值系数','显著性'],ascending=[False,False],inplace=True)
            elif val.lower() in ['dividend']:
                betas['估值判断']=betas['估值系数'].apply(lambda x: '可能高估' if x >0 else '可能低估')
                betas.sort_values(by=['估值系数','显著性'],ascending=[True,False],inplace=True)
            
            lo_est_betas=betas[(betas['行业']=='全行业') | (betas['估值判断']=='可能低估')]    
            
            betas.reset_index(drop=True,inplace=True)
            betas.index=betas.index + 1
            betas_list=betas_list+[betas]
            lo_est_betas_list=lo_est_betas_list+[lo_est_betas]
    
        # 整理各个行业的综合评价
        # 合并betas
        allbetas=pd.DataFrame()
        for b in betas_list:
            allbetas=allbetas.append(b)
        
        valtable=pd.DataFrame(columns=('行业', \
                                    ('PE','Annual Ret'), \
                                    ('PE','Quarterly Ret'), \
                                    ('PE','Monthly Ret'), \
                                    ('PB','Annual Ret'), \
                                    ('PB','Quarterly Ret'), \
                                    ('PB','Monthly Ret'), \
                                    ('dividend','Annual Ret'), \
                                    ('dividend','Quarterly Ret'), \
                                    ('dividend','Monthly Ret'), \
                                    ))
        valtable_list=list(valtable)
        valtable_list.remove('行业')
        industry_names=list(set(list(allbetas['行业'])))
        for i in industry_names:
            pos=industry_names.index(i)
            row=pd.Series({'行业':i})
            valtable=valtable.append(row,ignore_index=True) 
            
            for v in valtable_list:
                val,ret=v
                try:
                    val_value=allbetas[(allbetas['估值指标']==val) & (allbetas['收益率指标']==ret) & (allbetas['行业']==i)]['估值判断'].values[0]
                    if val_value == '可能低估':
                        val_value1='低估'
                    else:
                        val_value1='高估'
                        
                    sig_value=allbetas[(allbetas['估值指标']==val) & (allbetas['收益率指标']==ret) & (allbetas['行业']==i)]['显著性'].values[0]
                    vsvalue=val_value1+sig_value
                    
                    valtable.at[pos,v]=vsvalue
                except:
                    continue
    
    valtable.fillna('不确定',inplace=True)
    
    # 排序，低估在前，PE优先
    fld1=valtable_list[0]
    fld2=valtable_list[1]
    fld3=valtable_list[2]
    valtable.sort_values(by=[fld1,fld2,fld3],ascending=[True,True,True],inplace=True)
    valtable.reset_index(drop=True,inplace=True)

    print("Successfully valuated",len(valtable),'industries')
    print("Valuation completed by mixing PE/PB/dividend with Annual/Quarterly/Monthly")
    
    return valtable,betas_list

#==============================================================================
#==============================================================================
if __name__=='__main__':
    end='2022-11-22'
    start=date_adjust(end,-365*5)
    itype='I'
    industries='all'
    
    lo_est_betas_list,betas_list,idfall=valuation2return_sw(start,end,valuation=valuation,return_delay=return_delay)

def valuation2return_sw(start,end,itype='I',industries='all'):
    """
    功能：测试三种估值指标对滞后一段时间收益率的影响。
    测试行业哑元变量对估值指标的调节作用，借此判断。若正向（负向）影响，行业估值未低估（高估）
    start, end: 测试期间
    itype: 申万指数种类，默认行业类别I, 市场表征F, 投资风格F，全部A
    industries: 指定具体的指数列表，用于节省处理时间，默认all
    """
    #设定相关参数
    # 估值指标，市盈率PE, 市净率PB, 股息率dividend，三项合用
    valuation=['PE','PB','dividend']
    # 估值指标对收益率影响的滞后时间长度
    # Monthly一个月=21天，Quarterly一个季度=63天，Annual一年=252天。分别回归，用于观察期间长短的影响
    # 用于判断过去某个时点的估值指标能够对当前的收益率产生影响，以及何种影响
    return_delay=['Annual','Quarterly','Monthly']
    
    # 检查日期的合理性
    flag,start1,end1=check_period(start,end)
    if not flag:
        print("  #Error(valuation2return_sw): invalid date period",start,end)
        return None

    # 检查估值指标的类型
    valuationlist=['pe','pb','dividend']
    if isinstance(valuation,str):
        valuation_list=[valuation]
    elif isinstance(valuation,list):
        valuation_list=valuation
    for v in valuation_list:
        if not (v.lower() in valuationlist):
            print("  #Warning(valuation2return_sw): unsupported type of valuation:",v)
            print("  supported types of valuation:",valuationlist)
            return None

    # 检查估值指标的类型
    return_delaylist=['annual','quarterly','monthly']
    measurelist=['Annual Ret','Quarterly Ret','Monthly Ret']
    shiftlist=[252,63,21]
    
    if isinstance(return_delay,str):
        return_delay_list=[return_delay]
    elif isinstance(return_delay,list):
        return_delay_list=return_delay
        
    measure_list=[]
    shift_days_list=[]
    for v in return_delay_list:
        if not (v.lower() in return_delaylist):
            print("  #Warning(valuation2return_sw): unsupported type of return delay:",v)
            print("  supported types of return delay:",return_delaylist)
            return None
        
        pos=return_delaylist.index(v.lower())
        measure=measurelist[pos]
        measure_list=measure_list+[measure]
        shift_days=shiftlist[pos]
        shift_days_list=shift_days_list+[shift_days]

    #屏蔽函数内print信息输出的类
    import os, sys
    class HiddenPrints:
        def __enter__(self):
            self._original_stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')

        def __exit__(self, exc_type, exc_val, exc_tb):
            sys.stdout.close()
            sys.stdout = self._original_stdout

    # 步骤1：获取行业历史数据，本步骤所需时间较长=========================================
    industry_data=get_industry_sw(itype=itype)
    if not (industries.lower() == 'all'):
        industry_codes=industry_sw_codes(industries)
    else:
        industry_codes=list(set(list(industry_data['ticker'])))
    
    # 步骤2：计算基础数据，本步骤所需时间较长============================================
    idf,idfall=calc_industry_sw(industry_data,start,end)

    # 步骤3：构造回归数据，进行回归，记录回归结果
    import pandas as pd
    coefdflist=[]
    print("Calculating industry valuations, it may take great time, please wait ...")
    
    total=len(measure_list)*len(valuation_list)
    for m in measure_list:
        
        # （1）计算收益率
        #print("  Processing measure",m)
        ret_df=compare_industry_sw(idfall,industry_codes,measure=m,graph=False)
        industry_names=list(ret_df)
        pos=measure_list.index(m)
        d=shift_days_list[pos]
    
        ret_collist=list(ret_df)
        ret_reg=pd.DataFrame()
        obs_num=0
        # 构造用于回归的数据结构    
        for i in ret_collist:
            tmpdf=ret_df[[i]]
            tmpdf['行业']=i
            tmpdf.rename(columns={i:'ret'},inplace=True)
            
            if len(ret_reg)==0:
                ret_reg=tmpdf
            else:
                ret_reg=ret_reg.append(tmpdf)
        
        # （2）处理估值指标
        df=pd.DataFrame()
        for val in valuation_list:
            
            #print("    Handling valuation",val,'with measure',m)
            
            # （a）计算估值指标
            with HiddenPrints():
                val_df=compare_industry_valuation_sw(industry_names,start=start,end=end,
                                                 vtypes=val,graph=False)
            # （b）滞后估值指标
            val_df2=val_df.shift(d)
            val_collist=list(val_df2)
            val_reg=pd.DataFrame()
            
            for i in val_collist:
                tmpdf=val_df2[[i]]
                tmpdf['行业']=i
                tmpdf.rename(columns={i:val},inplace=True)
                
                if len(val_reg)==0:
                    val_reg=tmpdf
                else:
                    val_reg=val_reg.append(tmpdf)
        
            # （c）合成滞后的估值指标和收益率    
            val_reg['日期']=val_reg.index
            ret_reg['日期']=ret_reg.index
            
            df_reg=val_reg.merge(ret_reg,how='inner',on=['日期','行业'])
            df_reg.set_index('日期',inplace=True)
            df_reg2=index2date(df_reg,date_field='date')
            
            df_reg2.dropna(inplace=True)
            
            if len(df)==0:
                df=df_reg2
            else:
                df=pd.merge(df,df_reg2,how='outer',on=['date','行业'])

            # 本步骤所需时间漫长，显示当前进度
            current=measure_list.index(m)*len(valuation_list)+valuation_list.index(val)
            print_progress_percent(current,total,steps=5,leading_blanks=2)
            
        # （3）增加额外的自变量：PB/PE表示净资产产生利润的能力
        #print("Model regression for the impact on industrial returns by prior valuation ...")
        # PE*PB表示利润与净资产对于股价的联合支撑作用
        df['PBdivPE']=df['PB']/df['PE']
        df['PBxPE']=df['PB']*df['PE']
        xList=['PE','PB','dividend','PBdivPE','PBxPE']
        
        # （4）构造哑元变量：行业，年度
        df['year']=df['date'].apply(lambda x:x[:4])
        df2,indDummies,yDummies=df_fe2(df,industry_field="行业",year_field='year')
        obs_num=obs_num+len(df2)
        
        # （5）多元回归，记录行业哑元变量的回归系数和显著性
        coefdf=multi_ols(df2,xList=xList,y='ret',industryDummies=indDummies,yearDummies=yDummies)
        coefdf2=coefdf.T[indDummies].T
        coefdf2['val']=coefdf2['coef'].apply(lambda x: '低估' if x >0 else '高估')                
        coefdf2['估值判断']=coefdf2['val']+coefdf2['sig']
        coefdf2['measure']=m                
            
        coefdflist=coefdflist+[coefdf2]    
    
    # 步骤4：制作多行业多期的估值评价矩阵
    allbetas=pd.DataFrame()
    for b in coefdflist:
        b['行业0']=b.index
        b['行业']=b['行业0'].apply(lambda x:x[1:])
        if b['measure'].values[0]=='Annual Ret':
            b.rename(columns={'估值判断': '年度估值判断'}, inplace=True)
            b2=b[['行业','年度估值判断']]
        elif b['measure'].values[0]=='Quarterly Ret':
            b.rename(columns={'估值判断': '季度估值判断'},inplace=True)
            b2=b[['行业','季度估值判断']]
        else:
            b.rename(columns={'估值判断': '月度估值判断'},inplace=True)
            b2=b[['行业', '月度估值判断']]
            
        if len(allbetas)==0:
            allbetas=b2
        else:
            allbetas=pd.merge(allbetas,b2,how='outer',on=['行业'])
        
    allbetas.fillna('未知',inplace=True)
    
    allbetas['score1']=allbetas['年度估值判断'].apply(lambda x: val_score(x))
    allbetas['score2']=allbetas['季度估值判断'].apply(lambda x: val_score(x))
    allbetas['score3']=allbetas['月度估值判断'].apply(lambda x: val_score(x))
    allbetas['score']=allbetas['score1']+allbetas['score2']+allbetas['score3']
    
    loest=len(allbetas[allbetas['score']<0])
    hiest=len(allbetas[allbetas['score']>0])
    
    allbetas.sort_values(by=['score','行业'],ascending=[True,True],inplace=True)
    
    allbetas.reset_index(drop=True,inplace=True)
    allbetas2=allbetas[['行业', '年度估值判断', '季度估值判断', '月度估值判断']]
    allbetas2.index=allbetas2.index+1

    print("\nResults:")
    modelstr='ret = lagged('+xList[0]
    for x in xList[1:]:
        modelstr=modelstr+' + '+x
    modelstr=modelstr+')'+' + '+'Industry/Year dummies'
    print("  Valuation model:",modelstr)
    print("  Depenbdent: using Annual/Quarterly/Monthly ret respectively")
    
    print("  Sample period:",start,'to',end,'\b, total',obs_num,'observations for regression')
    
    print(" ",len(allbetas2),'industries valuated,',str(loest)+'('+str(hiest)+') might be under(over) estimated from future return perspective')
    
    # 在Jupyter Notebook可直接显示返回的变量，格式整齐
    return allbetas2

#==============================================================================
def val_score(val_comment):
    """
    功能：基于估值判断给出评分，仅用于排序，无其他实际意义
    """
    #print(val_comment,len(val_comment))
    if val_comment == '未知':
        score=0
        
    if val_comment == '低估   ':
        score=-1
    if val_comment == '低估*  ':
        score=-2
    if val_comment == '低估** ':
        score=-3
    if val_comment == '低估***':
        score=-4
        
    if val_comment == '高估   ':
        score=1
    if val_comment == '高估*  ':
        score=2
    if val_comment == '高估** ':
        score=3
    if val_comment == '高估***':
        score=4
        
    return score
        
        
        
        
#==============================================================================
if __name__ == '__main__':
    date_field='date'
    
def index2date(df,date_field='date'):
    """
    功能：从日期型df.index取出日期，类型YYYY-MM-DD，放在新字段date_field中。
    """
    
    df[date_field+'pd']=df.index
    df[date_field]=df[date_field+'pd'].apply(lambda x: x.strftime("%Y-%m-%d"))
    del df[date_field+'pd']

    return df    
    
#==============================================================================



def df_fe2(df,industry_field,year_field):
    """
    功能：基于df做出industry_field和year_field的哑元变量'i'+industry_field和'y'+year_field
    
    """
    ilist=[]
    ylist=[]
    
    #生成行业哑元变量，全部预置为0和1
    industry_list=list(set(list(df[industry_field])))
    industry_list.sort(reverse=False)
    for i in industry_list:
        df['i'+i]=df[industry_field].apply(lambda x: 1 if x==i else 0)
        ilist=ilist+['i'+i]

    #生成年度哑元变量，全部预置为0和1
    year_list=list(set(list(df[year_field])))
    year_list.sort(reverse=False)
    for i in year_list:
        df['y'+i]=df[year_field].apply(lambda x: 1 if x==i else 0)
        ylist=ylist+['y'+i]
    
    return df,ilist,ylist

#==============================================================================
def sig_level(p):
    """
    功能：基于p值给出显著性星星个数
    
    """
    if p >=0.05:
        sig="   "
    elif 0.05 > p >= 0.01:
        sig='*  '
    elif 0.01 > p >= 0.001:
        sig="** "
    else:
        sig="***"
        
    return sig

#==============================================================================

def multi_ols(df,xList,y,industryDummies,yearDummies):
    """
    功能：多元线性回归, y=f(X)，需要系数和显著性
    df: 所有数据
    xList: 自变量列表，不包括行业和年度哑元变量
    y： 因变量
    industryDummies： 行业哑元变量列表
    yearDummies： 年度哑元变量列表
    """
    import statsmodels.formula.api as smf
    
    #构造模型表达式：y~x1+x2+.....
    model=''
    allXVars=xList+industryDummies+yearDummies
    for x in allXVars:
        if model == '':
            model=y+'~'+x
        else:
            model=model+'+'+x
    
    #形成smf模型
    reg = smf.ols(formula=model,data=df)    
    
    #线性回归
    result=reg.fit()   
    #print(result.summary())

    #自变量各个系数及其显著性
    import pandas as pd
    coefMatrix=pd.DataFrame([result.params,result.pvalues],index=["coef","p"]).T
    
    coefMatrix['sig']=coefMatrix['p'].apply(lambda x: sig_level(x))
    
    #整个模型的显著性：F-test
    modelSig=result.f_pvalue
    
    return coefMatrix

#==============================================================================
