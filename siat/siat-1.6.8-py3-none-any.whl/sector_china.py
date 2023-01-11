# -*- coding: utf-8 -*-
"""
本模块功能：中国行业板块市场分析
所属工具包：证券投资分析工具SIAT 
SIAT：Security Investment Analysis Tool
创建日期：2020年10月20日
最新修订日期：2020年10月21日
作者：王德宏 (WANG Dehong, Peter)
作者单位：北京外国语大学国际商学院
版权所有：王德宏
用途限制：仅限研究与教学使用，不可商用！商用需要额外授权。
特别声明：作者不对使用本工具进行证券投资导致的任何损益负责！
"""

#==============================================================================
#关闭所有警告
import warnings; warnings.filterwarnings('ignore')
from siat.common import *
from siat.translate import *
from siat.bond_base import *
from siat.stock import *
from siat.risk_adjusted_return import *
#==============================================================================

if __name__=='__main__':
    indicator="新浪行业"
    indicator="启明星行业"
    indicator="地域"
    indicator="行业"

def sector_list_china(indicator="新浪行业"):
    """
    功能：行业分类列表
    indicator="新浪行业","启明星行业","概念","地域","行业"
    来源网址：http://finance.sina.com.cn/stock/sl/#qmxindustry_1
    """
    #检查选项是否支持
    indicatorlist=["新浪行业","概念","地域","行业","启明星行业"]
    if indicator not in indicatorlist:
        print("#Error(sector_list_china): unsupported sectoring method",indicator)
        print("Supported sectoring methods:",indicatorlist)
        return None
    
    import akshare as ak
    try:
        df = ak.stock_sector_spot(indicator=indicator)
    except:
        print("#Error(sector_list_china): data source tentatively unavailable for",indicator)
        print("Possible reason: data source is self-updating.")
        print("Solution: have a breath of fresh air and try later.")
        return None
    
    sectorlist=list(df['板块'])
    #按照拼音排序
    sectorlist=list(set(list(sectorlist)))
    sectorlist=sort_pinyin(sectorlist)
    #解决拼音相同带来的bug：陕西省 vs 山西省
    if '陕西省' in sectorlist:
        pos=sectorlist.index('陕西省')
        if sectorlist[pos+1] == '陕西省':
            sectorlist[pos] = '山西省'
    if '山西省' in sectorlist:
        pos=sectorlist.index('山西省')
        if sectorlist[pos+1] == '山西省':
            sectorlist[pos+1] = '陕西省'
    listnum=len(sectorlist)
    
    if indicator != "行业":
        method=indicator
    else:
        method="证监会细分行业"
    print("\n===== 中国股票市场的行业/板块:",listnum,"\b个（按"+method+"划分） =====")

    if indicator in ["新浪行业","启明星行业","概念"]:
        #板块名字长度
        maxlen=0
        for s in sectorlist:        
            l=strlen(s)
            if l > maxlen: maxlen=l
        #每行打印板块名字个数
        rownum=int(80/(maxlen+2))
        
        for d in sectorlist:
            if strlen(d) < maxlen:
                dd=d+" "*(maxlen-strlen(d))
            else:
                dd=d
            print(dd,end='  ')
            pos=sectorlist.index(d)+1
            if (pos % rownum ==0) or (pos==listnum): print(' ')    

    if indicator in ["地域","行业"]:
        linemaxlen=60
        linelen=0
        for d in sectorlist:
            dlen=strlen(d)
            pos=sectorlist.index(d)+1
            #超过行长
            if (linelen+dlen) > linemaxlen:
                print(' '); linelen=0
            #是否最后一项
            if pos < listnum:
                print(d,end=', ')
            else:
                print(d+"。"); break
            linelen=linelen+dlen

    import datetime
    today = datetime.date.today()
    print("*** 信息来源：新浪财经,",today) 
    
    return df


#==============================================================================
if __name__=='__main__':
    sector_name="房地产"
    indicator="启明星行业"
    indicator="地域"
    indicator="行业"

def sector_code_china(sector_name):
    """
    功能：查找行业、板块名称对应的板块代码
    """
    import akshare as ak
    print("\n===== 查询行业/板块代码 =====")
    
    indicatorlist=["新浪行业","概念","地域","启明星行业","行业"]
    sector_code=''; found=0
    for i in indicatorlist:
        dfi=ak.stock_sector_spot(indicator=i)
        try:
            sector_code=list(dfi[dfi['板块']==sector_name]['label'])[0]
            #记录找到的板块分类
            indicator=i
            #记录找到的板块概述
            dff=dfi[dfi['板块']==sector_name]
            
            if found > 0: print(" ")
            if indicator == "行业": indicator = "证监会行业"
            print("行业/板块名称："+sector_name)
            print("行业/板块代码："+sector_code,end='')
            print(", "+indicator+"分类")
            found=found+1
        except:
            continue
    #未找到板块代码
    if sector_name == '':
        print("#Error(sector_code_china): unsupported sector name",sector_name)
        return 
    
    return 

if __name__=='__main__':
    sector_name="房地产"
    df=sector_code_china(sector_name)
    df=sector_code_china("医药生物")
    df=sector_code_china("资本市场服务")
    
#==============================================================================
if __name__=='__main__':
    comp="xxx"
    comp="涨跌幅"
    comp="成交量"
    comp="平均价格"
    comp="公司家数"
    
    indicator="+++"
    indicator="新浪行业"
    indicator="启明星行业"
    indicator="地域"
    indicator="行业"
    num=10

def sector_rank_china(comp="涨跌幅",indicator="新浪行业",num=10):
    """
    功能：按照比较指标降序排列
    comp="涨跌幅",平均成交量（手），平均价格，公司家数
    indicator="新浪行业","启明星行业","概念","地域","行业"
    num：为正数时列出最高的前几名，为负数时列出最后几名
    """
    #检查选项是否支持
    #complist=["涨跌幅","成交量","平均价格","公司家数"]
    complist=["涨跌幅","平均价格","公司家数"]
    if comp not in complist:
        print("#Error(sector_rank_china): unsupported measurement",comp)
        print("Supported measurements:",complist)
        return None
    
    indicatorlist=["新浪行业","概念","地域","启明星行业","行业"]
    if indicator not in indicatorlist:
        print("#Error(sector_list_china): unsupported sectoring method",indicator)
        print("Supported sectoring method:",indicatorlist)
        return None
    
    import akshare as ak
    try:
        df = ak.stock_sector_spot(indicator=indicator)  
    except:
        print("#Error(sector_rank_china): data source tentatively unavailable for",indicator)
        print("Possible reason: data source is self-updating.")
        print("Solution: have a breath of fresh air and try later.")
        return None
    
    df.dropna(inplace=True)
    #出现列名重名，强制修改列名
    df.columns=['label','板块','公司家数','平均价格','涨跌额','涨跌幅', \
                '总成交量(手)','总成交额(万元)','个股代码','个股涨跌幅','个股股价', \
                '个股涨跌额','个股名称']
    df['均价']=round(df['平均价格'].astype('float'),2)
    df['涨跌幅%']=round(df['涨跌幅'].astype('float'),2)
    #平均成交量:万手
    df['平均成交量']=(df['总成交量(手)'].astype('float')/df['公司家数'].astype('float')/10000)
    df['平均成交量']=round(df['平均成交量'],2)
    #平均成交额：亿元
    df['平均成交额']=(df['总成交额(万元)'].astype('float')/df['公司家数'].astype('float'))/10000
    df['平均成交额']=round(df['平均成交额'],2)
    stkcd=lambda x: x[2:]
    df['个股代码']=df['个股代码'].apply(stkcd)
    try:
        df['个股涨跌幅%']=round(df['个股涨跌幅'].astype('float'),2)
    except:
        pass
    try:
        df['个股股价']=round(df['个股股价'].astype('float'),2)
    except:
        pass
    try:
        df['公司家数']=df['公司家数'].astype('int')
    except:
        pass
    df2=df[['板块','涨跌幅%','平均成交量','平均成交额','均价', \
            '公司家数','label','个股名称','个股代码','个股涨跌幅','个股股价']].copy()
    df2=df2.rename(columns={'个股名称':'代表个股','label':'板块代码'})
    
    #删除无效的记录
    df2=df2.drop(df2[df2['均价'] == 0.0].index)
    
    if comp == "涨跌幅":
        df3=df2[['板块','涨跌幅%','均价','公司家数','板块代码','代表个股']]
        df3.sort_values(by=['涨跌幅%'],ascending=False,inplace=True)
    """
    if comp == "成交量":
        df3=df2[['板块','平均成交量','涨跌幅%','均价','公司家数','板块代码','代表个股']]
        df3.sort_values(by=['平均成交量'],ascending=False,inplace=True)
    """
    if comp == "平均价格":
        df3=df2[['板块','均价','涨跌幅%','公司家数','板块代码','代表个股']]
        df3.sort_values(by=['均价'],ascending=False,inplace=True)
    if comp == "公司家数":
        df3=df2[['板块','公司家数','均价','涨跌幅%','板块代码','代表个股']]
        df3.sort_values(by=['公司家数'],ascending=False,inplace=True)
    df3.reset_index(drop=True,inplace=True)
        
    #设置打印对齐
    import pandas as pd
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    
    if indicator == "行业":
        indtag="证监会行业"
    else:
        indtag=indicator
    
    #处理空记录
    if len(df3) == 0:
        print("#Error(sector_rank_china):data source tentatively unavailable for",comp,indicator)
        print("Possible reason: data source is self-updating.")
        print("Solution: have a breath of fresh air and try later.")
        return
    
    print("\n===== 中国股票市场：板块"+comp+"排行榜（按照"+indtag+"分类） =====")
    if num > 0:
        print(df3.head(num))
    else:
        print(df3.tail(-num))
    
    import datetime
    today = datetime.date.today()
    footnote1="*注：代表个股是指板块中涨幅最高或跌幅最低的股票"
    print(footnote1)
    print(" 板块数:",len(df),"\b, 数据来源：新浪财经,",today,"\b（信息为上个交易日）") 

    return df3

#==============================================================================
if __name__=='__main__':
    sector="new_dlhy"
    sector="xyz"
        
    num=10

def sector_detail_china(sector="new_dlhy",comp="涨跌幅",num=10):
    """
    功能：按照板块内部股票的比较指标降序排列
    sector：板块代码
    num：为正数时列出最高的前几名，为负数时列出最后几名
    """
    debug=False

    #检查选项是否支持
    complist=["涨跌幅","换手率","收盘价","市盈率","市净率","总市值","流通市值"]
    if comp not in complist:
        print("#Error(sector_detail_china): unsupported measurement",comp)
        print("Supported measurements:",complist)
        return None
    
    #检查板块代码是否存在
    import akshare as ak
    indicatorlist=["新浪行业","概念","地域","启明星行业","行业"]
    sector_name=''
    for i in indicatorlist:
        dfi=ak.stock_sector_spot(indicator=i)
        if debug: print("i=",i)
        try:
            sector_name=list(dfi[dfi['label']==sector]['板块'])[0]
            #记录找到的板块分类
            indicator=i
            #记录找到的板块概述
            dff=dfi[dfi['label']==sector]
            break
        except:
            continue
    #未找到板块代码
    if sector_name == '':
        print("#Error(sector_detail_china): unsupported sector code",sector)
        return
    
    #板块成份股
    try:
        df = ak.stock_sector_detail(sector=sector)
    except:
        print("#Error(sector_rank_china): data source tentatively unavailable for",sector)
        print("Possible reason: data source is self-updating.")
        print("Solution: have a breath of fresh air and try later.")
        return None
    
    df.dropna(inplace=True)
    df['个股代码']=df['code']
    df['个股名称']=df['name']
    df['涨跌幅%']=round(df['changepercent'].astype('float'),2)
    df['收盘价']=round(df['settlement'].astype('float'),2)
    #成交量:万手
    df['成交量']=round(df['volume'].astype('float')/10000,2)
    #成交额：亿元
    df['成交额']=round(df['amount'].astype('float')/10000,2)
    df['市盈率']=round(df['per'].astype('float'),2)
    df['市净率']=round(df['pb'].astype('float'),2)
    #总市值：亿元
    df['总市值']=round(df['mktcap'].astype('float')/10000,2)
    #流通市值：亿元
    df['流通市值']=round(df['nmc'].astype('float')/10000,2)
    df['换手率%']=round(df['turnoverratio'].astype('float'),2)
    
    #删除无效的记录
    df=df.drop(df[df['收盘价'] == 0].index)
    df=df.drop(df[df['流通市值'] == 0].index)
    df=df.drop(df[df['总市值'] == 0].index)
    df=df.drop(df[df['市盈率'] == 0].index)
    
    df2=df[[ '个股代码','个股名称','涨跌幅%','收盘价','成交量','成交额', \
            '市盈率','市净率','换手率%','总市值','流通市值']].copy()
    
    if comp == "涨跌幅":
        df3=df2[['个股名称','个股代码','涨跌幅%','换手率%','收盘价','市盈率','市净率','流通市值']]
        df3.sort_values(by=['涨跌幅%'],ascending=False,inplace=True)
    if comp == "换手率":
        df3=df2[['个股名称','个股代码','换手率%','涨跌幅%','收盘价','市盈率','市净率','流通市值']]
        df3.sort_values(by=['换手率%'],ascending=False,inplace=True)
    if comp == "收盘价":
        df3=df2[['个股名称','个股代码','收盘价','换手率%','涨跌幅%','市盈率','市净率','流通市值']]
        df3.sort_values(by=['收盘价'],ascending=False,inplace=True)
    if comp == "市盈率":
        df3=df2[['个股名称','个股代码','市盈率','市净率','收盘价','换手率%','涨跌幅%','流通市值']]
        df3.sort_values(by=['市盈率'],ascending=False,inplace=True)
    if comp == "市净率":
        df3=df2[['个股名称','个股代码','市净率','市盈率','收盘价','换手率%','涨跌幅%','流通市值']]
        df3.sort_values(by=['市净率'],ascending=False,inplace=True)
    if comp == "流通市值":
        df3=df2[['个股名称','个股代码','流通市值','总市值','市净率','市盈率','收盘价','换手率%','涨跌幅%']]
        df3.sort_values(by=['流通市值'],ascending=False,inplace=True)
    if comp == "总市值":
        df3=df2[['个股名称','个股代码','总市值','流通市值','市净率','市盈率','收盘价','换手率%','涨跌幅%']]
        df3.sort_values(by=['总市值'],ascending=False,inplace=True)  
        
    df3.reset_index(drop=True,inplace=True)
        
    #设置打印对齐
    import pandas as pd
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    
    print("\n=== 中国股票市场："+sector_name+"板块，成份股排行榜（按照"+comp+"） ===")
    if num > 0:
        print(df3.head(num))
    else:
        print(df3.tail(-num))
    
    import datetime
    today = datetime.date.today()
    footnote1="*注：市值的单位是亿元人民币, "
    print(footnote1+"板块内成份股个数:",len(df))
    print(" 数据来源：新浪财经,",today,"\b（信息为上个交易日）") 

    return df2

#==============================================================================
if __name__=='__main__':
    ticker='600021'
    ticker='000661'
    ticker='999999'
    sector="new_dlhy"
    sector="yysw"
    sector="xyz"

def sector_position_china(ticker,sector="new_dlhy"):
    """
    功能：查找一只股票在板块内的百分数位置
    ticker：股票代码
    sector：板块代码
    """
    
    import akshare as ak
    import numpy as np
    import pandas as pd    
    
    #检查板块代码是否存在
    indicatorlist=["新浪行业","概念","地域","启明星行业","行业"]
    sector_name=''
    for i in indicatorlist:
        dfi=ak.stock_sector_spot(indicator=i)
        try:
            sector_name=list(dfi[dfi['label']==sector]['板块'])[0]
            #记录找到的板块分类
            indicator=i
            #记录找到的板块概述
            dff=dfi[dfi['label']==sector]
            break
        except:
            continue
    #未找到板块代码
    if sector_name == '':
        print("#Error(sector_position_china): unsupported sector code",sector)
        return None
    
    #板块成份股
    try:
        #启明星行业分类没有成份股明细
        df = ak.stock_sector_detail(sector=sector)
    except:
        print("#Error(sector_position_china): sector detail not available for",sector,'by',indicator)
        print("Possible reason: data source is self-updating.")
        print("Solution: have a breath of fresh air and try later.")
        return None

    #清洗原始数据: #可能同时含有数值和字符串，强制转换成数值
    df['changepercent']=round(df['changepercent'].astype('float'),2)
    df['turnoverratio']=round(df['turnoverratio'].astype('float'),2)
    df['settlement']=round(df['settlement'].astype('float'),2)
    df['per']=round(df['per'].astype('float'),2)
    df['pb']=round(df['pb'].astype('float'),2)
    df['nmc']=round(df['nmc'].astype('int')/10000,2)
    df['mktcap']=round(df['mktcap'].astype('int')/10000,2)
    
    #检查股票代码是否存在
    sdf=df[df['code']==ticker]
    if len(sdf) == 0:
        print("#Error(sector_position_china): retrieving",ticker,"failed in sector",sector,sector_name)
        print("#Try later if network responses slowly.")
        return None       
    sname=list(sdf['name'])[0]
    
    #确定比较范围
    complist=['changepercent','turnoverratio','settlement','per','pb','nmc','mktcap']
    compnames=['涨跌幅%','换手率%','收盘价(元)','市盈率','市净率','流通市值(亿元)','总市值(亿元)']
    compdf=pd.DataFrame(columns=['指标名称','指标数值','板块百分位数%','板块中位数','板块最小值','板块最大值'])
    for c in complist:
        v=list(sdf[c])[0]
        vlist=list(set(list(df[c])))
        vlist.sort()
        vmin=round(min(vlist),2)
        vmax=round(max(vlist),2)
        vmedian=round(np.median(vlist),2)
        
        pos=vlist.index(v)
        pct=round((pos+1)/len(vlist)*100,2)
        
        s=pd.Series({'指标名称':compnames[complist.index(c)], \
                     '指标数值':v,'板块百分位数%':pct,'板块中位数':vmedian, \
                    '板块最小值':vmin,'板块最大值':vmax})
        compdf=compdf.append(s,ignore_index=True) 
        
    compdf.reset_index(drop=True,inplace=True)     

    print("\n======= 股票在所属行业/板块的位置分析 =======")
    print("股票: "+sname+" ("+ticker+")")
    print("所属行业/板块："+sector_name+" ("+sector+", "+indicator+"分类)")
    print("")
    
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    
    print(compdf.to_string(index=False))
    
    import datetime
    today = datetime.date.today()
    print("*板块内成份股个数:",len(df),"\b, 数据来源：新浪财经,",today,"\b（信息为上个交易日）")

    return df,compdf    
    

#==============================================================================

def invest_concept_china(num=10):
    """
    废弃！
    功能：汇总投资概念股票名单，排行
    来源网址：http://finance.sina.com.cn/stock/sl/#qmxindustry_1
    """
    print("\nWarning: This function might cause your IP address banned by data source!")
    print("Searching stocks with investment concepts in China, it may take long time ...")
    
    #找出投资概念列表
    import akshare as ak
    cdf = ak.stock_sector_spot(indicator="概念")
    cdf.sort_values(by=['label'],ascending=True,inplace=True)
    clist=list(cdf['label'])
    cnames=list(cdf['板块'])
    cnum=len(clist)
    
    import pandas as pd
    totaldf=pd.DataFrame()
    import time
    i=0
    #新浪财经有反爬虫，这个循环做不下去
    for c in clist:
        print("...Searching for conceptual sector",c,cnames[clist.index(c)],end='')
        try:
            sdf = ak.stock_sector_detail(c)
            sdf['板块']=cnames(clist.index(c))
            totaldf=pd.concat([totaldf,sdf],ignore_index=True)
            print(', found.')
        except:
            print(', failed:-(')
            #continue
                    #等待一会儿，避免被禁访问
        time.sleep(10)
        i=i+1
        if i % 20 == 0:
            print(int(i/cnum*100),'\b%',end=' ')
    print("...Searching completed.")
    
    if len(totaldf) == 0:
        print("#Error(sector_rank_china): data source tentatively banned your access:-(")
        print("Solutions:1) try an hour later, or 2) switch to another IP address.")
        return None
    
    #分组统计
    totaldfrank = totaldf.groupby('name')['板块','code'].count()
    totaldfrank.sort_values(by=['板块','code'],ascending=[False,True],inplace=True)
    totaldfrank['name']=totaldfrank.index
    totaldfrank.reset_index(drop=True,inplace=True)

    #更新每只股票持有的概念列表
    for i in totaldfrank.index:
        tdfsub=totaldf[totaldf['name']==totaldfrank.loc[i,"name"]]
        sectors=str(list(tdfsub['板块'])) 
        # 逐行修改列值
        totaldfrank.loc[i,"sectors"] = sectors

    #合成
    totaldf2=totaldf.drop('板块',axix=1)
    totaldf2.drop_duplicates(subset=['code'],keep='first',inplace=True)
    finaldf = pd.merge(totaldfrank,totaldf2,how='inner',on='name')
    
    return finaldf
    
    
#==============================================================================
#==============================================================================
#申万行业分类：https://www.swhyresearch.com/institute_sw/allIndex/analysisIndex
#==============================================================================
#==============================================================================
def industry_sw_list():
    """
    功能：输出申万指数代码df。
    输入：
    输出：df
    """
    import pandas as pd
    industry=pd.DataFrame([
        
        #市场表征指数F
        ['F','801001','申万50'],['F','801002','申万中小'],['F','801003','申万Ａ指'],
        ['F','801005','申万创业'],['F','801250','申万制造'],['F','801260','申万消费'],
        ['F','801270','申万投资'],['F','801280','申万服务'],['F','801300','申万300指数'],
        
        #一级行业指数
        ['I','801010','农林牧渔'],['I','801030','基础化工'],['I','801040','钢铁'],
        ['I','801050','有色金属'],['I','801080','电子'],['I','801110','家用电器'],
        ['I','801120','食品饮料'],['I','801130','纺织服饰'],['I','801140','轻工制造'],
        ['I','801150','医药生物'],['I','801160','公用事业'],['I','801170','交通运输'],
        ['I','801180','房地产'],['I','801200','商贸零售'],['I','801210','社会服务'],
        ['I','801230','综合'],['I','801710','建筑材料'],['I','801720','建筑装饰'],
        ['I','801730','电力设备'],['I','801740','国防军工'],['I','801750','计算机'],
        ['I','801760','传媒'],['I','801770','通讯'],['I','801780','银行'],
        ['I','801790','非银金融'],['I','801880','汽车'],['I','801890','机械设备'],
        ['I','801950','煤炭'],['I','801960','石油石化'],['I','801970','环保'],
        ['I','801980','美容护理'],
        
        #风格指数
        ['S','801811','大盘指数'],['S','801812','中盘指数'],['S','801813','小盘指数'],
        ['S','801821','高市盈率指数'],['S','801822','中市盈率指数'],['S','801823','低市盈率指数'],
        ['S','801831','高市净率指数'],['S','801832','中市净率指数'],['S','801833','低市净率指数'],
        ['S','801841','高股价指数'],['S','801842','中价股指数'],['S','801843','低价股指数'],
        ['S','801851','亏损股指数'],['S','801852','微利股指数'],['S','801853','绩优股指数'],
        ['S','801862','活跃指数'],['S','801863','新股指数'],
        
        
        ], columns=['type','code','name'])

    return industry

if __name__=='__main__':
    idf=industry_sw_list()

#==============================================================================
if __name__=='__main__':
    itype='I'
    numberPerLine=5
    colalign='left'
    
    print_industry_sw(itype='I',numberPerLine=5,colalign='right')

def print_industry_sw(itype='I',numberPerLine=5,colalign='left'):
    """
    打印所有申万行业列表，名称(代码)
    """
    df=industry_sw_list()
    df1=df[df['type']==itype]
    df1['name_code']=df1.apply(lambda x: x['name']+'('+x['code']+')',axis=1)
    
    ilist=list(df1['name_code'])
    print("\n*** 申万行业分类：共计"+str(len(ilist))+'个行业(板块)')
    
    printInLine_md(ilist,numberPerLine=numberPerLine,colalign=colalign)
    
    return

#==============================================================================
if __name__=='__main__':
    iname='食品饮料'
    iname='银行'
    numberPerLine=5
    colalign='right'
    
    print_industry_component_sw(iname,numberPerLine=5,colalign='right')

def print_industry_component_sw(iname,numberPerLine=5,colalign='left'):
    """
    打印申万行业的成分股，名称(代码)
    """
    
    icode=industry_sw_code(iname)
    
    clist,cdf=industry_stock_sw(icode,top=1000)    

    cdf['icode']=cdf['证券代码'].apply(lambda x: x+'.SS' if x[:1] in ['6'] else (x+'.SZ' if x[:1] in ['0','3'] else x+'.BJ' ))
    cdf['name_code']=cdf.apply(lambda x: x['证券名称']+'('+x['icode']+')',axis=1)
    
    ilist=list(cdf['name_code'])
    import datetime as dt; stoday=dt.date.today()    
    print("\n*** "+iname+'行业(板块)包括的股票：共计'+str(len(ilist))+'只，'+str(stoday)+"统计")
    
    printInLine_md(ilist,numberPerLine=numberPerLine,colalign=colalign)
    
    return
    
#==============================================================================
def industry_sw_name(icode):
    """
    功能：将申万指数代码转换为指数名称。
    输入：指数代码
    输出：指数名称
    """
    industry=industry_sw_list()

    try:
        iname=industry[industry['code']==icode]['name'].values[0]
    except:
        #未查到
        print("  #Warning(industry_sw_name): industry code not found",icode)
        iname=icode
   
    return iname

if __name__=='__main__':
    icode='801862'
    industry_sw_name(icode)

#==============================================================================
def industry_sw_code(iname):
    """
    功能：将申万指数名称转换为指数代码。
    输入：指数名称
    输出：指数代码
    """
    industry=industry_sw_list()

    try:
        icode=industry[industry['name']==iname]['code'].values[0]
    except:
        #未查到
        print("  #Warning(industry_sw_code): industry name not found",iname)
        return None
   
    return icode

if __name__=='__main__':
    iname='申万创业'
    industry_sw_code(iname)

#==============================================================================
def industry_sw_codes(inamelist):
    """
    功能：将申万指数名称/列表转换为指数代码列表。
    输入：指数名称/列表
    输出：指数代码列表
    """
    industry=industry_sw_list()

    icodelist=[]
    if isinstance(inamelist,str):
        icode=industry_sw_code(inamelist)
        if not (icode is None):
            icodelist=[icode]
        else:
            print("  #Warning(industries_sw_code): industry name not found",inamelist)
            return None

    if isinstance(inamelist,list):
        if len(inamelist) == 0:
            print("  #Warning(industries_sw_code): no industry code found in",inamelist)
            return None
        
        for i in inamelist:
            icode=industry_sw_code(i)
            if not (icode is None):
                icodelist=icodelist+[icode]
            else:
                print("  #Warning(industries_sw_code): industry code not found",i)
                return None
   
    return icodelist

if __name__=='__main__':
    inamelist='申万创业'
    industry_sw_codes(inamelist)
    
    inamelist=['申万创业','申万投资','申万制造','申万消费']
    industry_sw_codes(inamelist)
#==============================================================================
if __name__=='__main__':
    start='2018-1-1'
    end='2022-10-31'
    measure='Exp Ret%'
    itype='I'
    graph=True
    axisamp=0.8
    
def industry_ranking_sw(start,end,measure='Exp Ret%', \
                                itype='I',period="day", \
                                graph=True,axisamp=0.8):
    """
    完整版，全流程
    功能：模板，遍历某类申万指数，计算某项业绩指标，汇集排序
    itype: F表征指数，I行业指数，S风格指数
    period="day"; choice of {"day", "week", "month"}
    绘图：柱状图，可选
    """
    #检查日期的合理性
    result,start1,end1=check_period(start,end)
    
    #检查itype的合理性
    
    #获得指数代码
    idf=industry_sw_list()
    idf1=idf[idf['type']==itype]
    ilist=list(idf1['code'])

    #循环获取指标
    import pandas as pd
    import akshare as ak
    import datetime
    df=pd.DataFrame(columns=['date','ticker','start','end','item','value'])

    print("\nSearching industry prices, it may take great time, please wait ...")
    for i in ilist:
        
        print("  Processing industry",i,"\b, please wait ...")
        #抓取指数价格，选取期间范围
        dft = ak.index_hist_sw(symbol=i,period="day")
        
        dft['ticker']=dft['代码']
        dft['date']=dft['日期'].apply(lambda x: pd.to_datetime(x))
        dft.set_index('date',inplace=True)
        dft['Open']=dft['开盘']
        dft['High']=dft['最高']
        dft['Low']=dft['最低']
        dft['Close']=dft['收盘']
        dft['Adj Close']=dft['收盘']
        dft['Volume']=dft['成交量']
        dft['Amount']=dft['成交额']
        
        dft.sort_index(ascending=True,inplace=True)
        #dft1=dft[(dft.index>=start1) & (dft.index<=end1)]
        dft2=dft[['ticker','Open','High','Low','Close','Adj Close','Volume','Amount']]

        #计算指标
        dft3=all_calculate(dft2,i,start,end)
        dft4=dft3.tail(1)
        
        #记录
        idate=dft4.index.values[0]
        idate=pd.to_datetime(idate)
        iend=idate.strftime('%Y-%m-%d')
        try:
            ivalue=round(dft4[measure].values[0],2)
            s=pd.Series({'date':idate,'ticker':i,'start':start,'end':iend,'item':measure,'value':ivalue})
            df=df.append(s,ignore_index=True) 
        except:
            print("  #Error(industry_ranking_sw): measure not supported",measure)
            return None
        
    df.sort_values(by='value',ascending=True,inplace=True)
    df['name']=df['ticker'].apply(lambda x: industry_sw_name(x))
    df.set_index('name',inplace=True)
    colname='value'
    titletxt="行业板块分析：业绩排名"
    import datetime; today=datetime.date.today()
    footnote0=ectranslate(measure)+' ==>\n'
    footnote1='申万行业分类，观察期：'+start+'至'+iend+'\n'
    footnote2="数据来源: 申万宏源, "+str(today)
    footnote=footnote0+footnote1+footnote2
    
    plot_barh(df,colname,titletxt,footnote,axisamp=axisamp) 
    #plot_barh2(df,colname,titletxt,footnote)

    return df
    
if __name__=='__main__':
    start='2018-1-1'
    end='2022-10-31'
    measure='Exp Ret%'
    itype='I'
    graph=True
    axisamp=0.8
    
    df=industry_sw_search_template(start,end,measure='Exp Ret%',axisamp=0.8)
    
#==============================================================================
#==============================================================================
if __name__=='__main__':
    start='2018-1-1'
    end='2022-10-31'
    measure='Exp Ret%'
    itype='F'
    period="day"
    industry_list='all'    
    
def get_industry_sw(itype='I',period="day",industry_list='all'):
    """
    功能：遍历某类申万指数，下载数据
    itype: F表征指数，I行业指数，S风格指数
    period="day"; choice of {"day", "week", "month"}
    industry_list: 允许选择部分行业
    """
    
    #检查itype的合理性
    typelist=['F','I','S','A']
    if not (itype in typelist):
        print("  #Error(get_industry_sw): unsupported industry category",itype)
        print("  Supported industry category",typelist)
        print("  F: Featured, I-Industry, S-Styled, A-All (more time))")
        return None
    
    #获得指数代码
    if industry_list=='all':
        idf=industry_sw_list()
        
        if itype == 'A':
            ilist=list(idf['code'])
        else:
            idf1=idf[idf['type']==itype]
            ilist=list(idf1['code'])
    else:
        ilist=industry_list
        
    #循环获取指标
    import pandas as pd
    import akshare as ak
    import datetime
    df=pd.DataFrame()

    print("Searching industry information, please wait ...")
    num=len(ilist)
    if num <= 10:
        steps=5
    else:
        steps=10
        
    total=len(ilist)
    for i in ilist:
        
        #print("  Retrieving information for industry",i)
        
        #抓取指数价格
        try:
            dft = ak.index_hist_sw(symbol=i,period="day")
        except:
            print("  #Warning(get_industry_sw): unsupported industry",i)
            continue
        
        dft['ticker']=dft['代码']
        dft['date']=dft['日期'].apply(lambda x: pd.to_datetime(x))
        dft.set_index('date',inplace=True)
        dft['Open']=dft['开盘']
        dft['High']=dft['最高']
        dft['Low']=dft['最低']
        dft['Close']=dft['收盘']
        dft['Adj Close']=dft['收盘']
        dft['Volume']=dft['成交量']
        dft['Amount']=dft['成交额']
        
        dft.sort_index(ascending=True,inplace=True)
        dft2=dft[['ticker','Open','High','Low','Close','Adj Close','Volume','Amount']]
        
        df=df.append(dft2)
        
        current=ilist.index(i)
        print_progress_percent(current,total,steps=steps,leading_blanks=2)
    
    #num=list(set(list(df['ticker'])))
    print("  Successfully retrieved",len(df),"records in",len(ilist),"industries")
    #print("  Successfully retrieved",len(df),"records in",num,"industries")
    return df

    
if __name__=='__main__':
    df=get_industry_sw('F')

#==============================================================================
if __name__=='__main__':
    start='2018-1-1'
    end='2022-10-31'
    df=get_industry_sw('F')
    
def calc_industry_sw(df,start,end):
    """
    功能：遍历某类申万指数，计算某项业绩指标，汇集排序
    df: 来自于get_industry_sw
    输出：最新时刻数据idf，全部时间序列数据idfall
    """
    #检查日期的合理性
    result,start1,end1=check_period(start,end)
    if not result:
        print("  #Error(calc_industry_sw): invalid date period",start,end)
        return None
    
    #获得指数代码
    ilist=list(set(list(df['ticker'])))
    ilist.sort()

    #循环获取指标
    import pandas as pd
    import datetime
    idf=pd.DataFrame()
    idfall=pd.DataFrame()

    print("Calculating industry performance, please wait ...")
    num=len(ilist)
    if num <= 10:
        steps=5
    else:
        steps=10
        
    total=len(ilist)
    for i in ilist:
        
        #print("  Processing industry",i)
        
        #抓取指数价格
        dft = df[df['ticker']==i]
        dft.sort_index(ascending=True,inplace=True)
        dft2=dft

        #计算指标
        dft3=all_calculate(dft2,i,start,end)
        dft3['start']=start

        #截取绘图区间
        dft3a=dft3[(dft3.index >= start1) & (dft3.index <= end1)]
        
        dft4=dft3a.tail(1)
        idf=idf.append(dft4)
        idfall=idfall.append(dft3a)

        current=ilist.index(i)
        print_progress_percent(current,total,steps=steps,leading_blanks=2) 
    
    print("  Successfully processed",len(ilist),"industries")
    return idf,idfall
    
if __name__=='__main__':
    start='2018-1-1'
    end='2022-10-31'
    idf,idfall=calc_industry_sw(df,start,end)
    
#==============================================================================
#==============================================================================
if __name__=='__main__':
    measure='Exp Ret%'
    graph=True
    axisamp=0.8
    
def rank_industry_sw(idf,measure='Exp Ret%',graph=True,axisamp=0.8,px=False):
    """
    功能：遍历某类申万指数的某项业绩指标，汇集排序
    绘图：水平柱状图
    """
  
    #获得指标数据
    try:
        gdf=idf[['ticker',measure,'start']]
        num1=len(gdf)
    except:
        print("  #Error(rank_industry_sw): unsupported measurement",measure)
        return None

    gdf.dropna(inplace=True)
    num2=len(gdf)
    if num2==0:
        print("  #Error(rank_industry_sw): no data found for",measure)
        return None

    if num2 < num1:
        print("  #Warning(rank_industry_sw):",num1-num2,"industries removed since no data found for",measure)
        
    gdf[measure]=gdf[measure].apply(lambda x: round(x,1))
    istart=gdf['start'].values[0]
    idate=gdf.index.values[0]
    idate=pd.to_datetime(idate)
    iend=idate.strftime('%Y-%m-%d')

    gdf['name']=gdf['ticker'].apply(lambda x: industry_sw_name(x))
    gdf.set_index('name',inplace=True)
    gdf.sort_values(by=measure,ascending=True,inplace=True)

    if graph:
        colname=measure
        titletxt="行业板块分析：最新业绩排名"
        import datetime; today=datetime.date.today()
        footnote0=ectranslate(measure)+' -->\n\n'
        footnote1='申万行业分类，'+iend+'快照'
        footnote2='观察期：'+istart+'至'+iend+'，'
        footnote3="数据来源: 申万宏源, "+str(today)+'统计'
        footnote=footnote0+footnote1+'\n'+footnote2+footnote3
        if not px:
            footnote=footnote0+footnote1+'\n'+footnote2+footnote3
            plot_barh(gdf,colname,titletxt,footnote,axisamp=axisamp)
        else: #使用plotly_express
            titletxt="行业板块业绩排名："+ectranslate(measure)
            footnote=footnote1+'。'+footnote2+footnote3
            plot_barh2(gdf,colname,titletxt,footnote)

    return gdf
    
if __name__=='__main__':
    measure='Exp Ret%'
    axisamp=0.8
    
    gdf=analyze_industry_sw(idf,measure='Exp Ret%',axisamp=0.8)
    gdf=analyze_industry_sw(idf,measure='Exp Ret Volatility%',axisamp=1.6)
    gdf=analyze_industry_sw(idf,measure='Exp Ret LPSD%',axisamp=1.7)
    gdf=analyze_industry_sw(idf,measure='Annual Ret Volatility%',axisamp=1.3)
    gdf=analyze_industry_sw(idf,measure='Annual Ret%',axisamp=1.0)
    gdf=analyze_industry_sw(idf,measure='Quarterly Ret%',axisamp=0.3)
    gdf=analyze_industry_sw(idf,measure='Monthly Ret%',axisamp=0.6)
    
#==============================================================================
if __name__=='__main__':
    industry_list=['801050','801080']
    measure='Exp Ret%'
    start='2020-11-1'
    end='2022-10-31'
    itype='I'
    period="day"
    graph=True

def compare_mindustry_sw(industry_list,measure,start,end, \
                         itype='I',period="day",graph=True):
    """
    功能：比较多个行业industry_list某个指标measure在时间段start/end的时间序列趋势
    industry_list: 至少有两项，若太多了则生成的曲线过于密集
    特点：完整过程
    """    
    #检查行业代码的个数不少于两个
    if len(industry_list) < 2:
        print("  #Warning(compare_mindustry_sw): need at least 2 indistries to compare")
        return None
    
    #检查行业代码是否在范围内
    ilist_all=list(industry_sw_list()['code'])
    for i in industry_list:
        if not (i in ilist_all):
            print("  #Warning(compare_mindustry_sw): unsupported industry",i)
            return None
    
    
    #检查日期期间的合理性
    result,startpd,endpd=check_period(start,end)
    if not result:
        print("  #Error(compare_mindustry_sw): invalid date period",start,end)
        return None
    
    
    #获取数据
    ddf=get_industry_sw(itype=itype,period=period,industry_list=industry_list)
    
    #计算指标
    _,idf=calc_industry_sw(ddf,start,end)
    
    #转换数据表结构为横排并列，适应绘图要求
    ilist=list(set(list(idf['ticker'])))
    import pandas as pd
    dfs=pd.DataFrame()
    notfoundlist=[]
    for i in ilist:
        
        dft=idf[idf['ticker']==i]
        istart=idf['start'].values[0]
        
        try:
            dft1=pd.DataFrame(dft[measure])
        except:
            print("  #Error(compare_mindustry_sw) unsupported measurement",measure)
            return None
        dft1.dropna(inplace=True)
        if len(dft1)==0:
            notfoundlist=notfoundlist+[i]
            continue
        
        dft1.rename(columns={measure:industry_sw_name(i)},inplace=True)
        if len(dfs)==0:
            dfs=dft1
        else:
            dfs=pd.merge(dfs,dft1,how='outer',left_index=True,right_index=True)
    
    if len(notfoundlist) > 0:
        print("  #Warning(compare_mindustry_sw): industry measure not found",notfoundlist)
        
    #绘制多条曲线
    idate=dfs.index.values[-1]
    idate=pd.to_datetime(idate)
    iend=idate.strftime('%Y-%m-%d')

    #截取绘图区间
    result,istartpd,iendpd=check_period(istart,iend)
    dfs1=dfs[(dfs.index >= istartpd) & (dfs.index <= iendpd)]
    
    y_label=measure
    import datetime; today = datetime.date.today()
    if graph:
        colname=measure
        title_txt="行业板块分析：市场发展趋势"
        import datetime; today=datetime.date.today()
        footnote1='\n申万行业分类，观察期：'+istart+'至'+iend+'\n'
        footnote2="数据来源: 申万宏源, "+str(today)+'统计'
        footnote=footnote1+footnote2

        draw_lines(dfs1,y_label,x_label=footnote, \
                   axhline_value=0,axhline_label='', \
                   title_txt=title_txt, \
                   data_label=False,resample_freq='H',smooth=True)
    
    return dfs
    
if __name__=='__main__':
    mdf=compare_mindustry_sw(industry_list,measure,start,end)

#==============================================================================
if __name__=='__main__':
    industry_list=['801050','801080']
    measure='Exp Ret%'
    start='2020-11-1'
    end='2022-10-31'
    itype='I'
    period="day"
    graph=True

def compare_industry_sw(idfall,industry_list,measure,graph=True):
    """
    功能：比较多个行业industry_list某个指标measure在时间段start/end的时间序列趋势
    industry_list: 至少有两项，若太多了则生成的曲线过于密集
    特点：需要依赖其他前序支持
    #获取数据
    ddf=get_industry_sw(itype=itype,period=period,industry_list=industry_list)
    
    #计算指标
    idf=calc_industry_sw(ddf,start,end,latest=False)
    
    """    
    #检查行业代码的个数不少于两个
    if len(industry_list) < 2:
        print("  #Warning(compare_mindustry_sw): need at least 2 indistries to compare")
        return None
    
    #检查行业代码是否在范围内
    ilist_all=list(industry_sw_list()['code'])
    for i in industry_list:
        if not (i in ilist_all):
            print("  #Warning(compare_mindustry_sw): unsupported or no such industry",i)
            return None
    
    #转换数据表结构为横排并列，适应绘图要求
    import pandas as pd
    dfs=pd.DataFrame()
    notfoundlist=[]
    for i in industry_list:
        
        try:
            dft=idfall[idfall['ticker']==i]
        except:
            print("  #Error(compare_mindustry_sw) unsupported or no such industry",i)
            return None
        
        if not (len(dft)==0):
            istart=dft['start'].values[0]
        else:
            print("  #Error(compare_mindustry_sw) unsupported or no such industry",i)
            return None

        try:
            dft1=pd.DataFrame(dft[measure])
        except:
            print("  #Error(compare_mindustry_sw) unsupported measurement",measure)
            return None
        dft1.dropna(inplace=True)
        if len(dft1)==0:
            notfoundlist=notfoundlist+[i]
            #print("  #Warning(compare_mindustry_sw): no data found for industry",i,"on",measure)
            continue
        
        dft1.rename(columns={measure:industry_sw_name(i)},inplace=True)
        if len(dfs)==0:
            dfs=dft1
        else:
            dfs=pd.merge(dfs,dft1,how='outer',left_index=True,right_index=True)
    
    if len(notfoundlist)>0:
        print("  #Warning(compare_mindustry_sw):",measure,"data not found for industries",notfoundlist)
    
    #绘制多条曲线
    idate=dfs.index.values[-1]
    idate=pd.to_datetime(idate)
    iend=idate.strftime('%Y-%m-%d')
    
    #截取数据区间
    result,istartpd,iendpd=check_period(istart,iend)
    dfs1=dfs[(dfs.index >= istartpd) & (dfs.index <= iendpd)]
    
    if graph:
        y_label=measure
        colname=measure
        title_txt="行业板块分析：市场发展趋势"
        
        import datetime; today=datetime.date.today()
        footnote1='\n申万行业分类，观察期：'+istart+'至'+iend+'\n'
        footnote2="数据来源: 申万宏源, "+str(today)+'统计'
        footnote=footnote1+footnote2

        draw_lines(dfs1,y_label,x_label=footnote, \
                   axhline_value=0,axhline_label='', \
                   title_txt=title_txt, \
                   data_label=False,resample_freq='H',smooth=True)

    return dfs1
    
if __name__=='__main__':
    mdf=compare_industry_sw(idfall,industry_list,measure)

#==============================================================================
if __name__=='__main__':
    start='2018-1-1'
    end='2022-10-31'
    df=get_industry_sw('F')
    idf,idfall=calc_industry_sw(df,start,end)
    base_return='Annual Ret%'
    graph=True

def compare_industry_sw_sharpe(idfall,industries,base_return='Annual Ret%',graph=True):
    """
    功能：比较申万行业的夏普比率
    idfall: 由calc_industry_sw函数获得
    industries: 仅限idfall中的行业
    
    缺陷：未考虑无风险利率
    """
    
    #获得年度收益率TTM
    aret=compare_industry_sw(idfall,industries,measure=base_return,graph=False)
    if aret is None:
        return None
    
    #获得年度收益率波动率TTM
    pos=base_return.index('%')
    base_risk=base_return[:pos]+' Volatility%'
    aretrisk=compare_industry_sw(idfall,industries,measure=base_risk,graph=False)
    
    #合成
    industrylist=list(aret)  
    atmp=pd.merge(aret,aretrisk,how='inner',left_index=True,right_index=True)
    for i in industrylist:
        atmp[i]=atmp[i+'_x']/atmp[i+'_y']
        
    sdf=atmp[industrylist]
    if graph:
        y_label='夏普比率（基于'+ectranslate(base_return)+'）'
        title_txt="行业板块分析：市场发展趋势"
        
        istart=sdf.index[0].strftime('%Y-%m-%d')
        iend=sdf.index[-1].strftime('%Y-%m-%d')
        footnote1='\n申万行业分类，观察期：'+istart+'至'+iend+'\n'
        import datetime; today=datetime.date.today()
        #footnote2="数据来源: 申万宏源, "+str(today)+'统计（未计入无风险利率）'
        footnote2="数据来源: 申万宏源, "+str(today)+'统计'
        footnote=footnote1+footnote2

        draw_lines(sdf,y_label,x_label=footnote, \
                   axhline_value=0,axhline_label='', \
                   title_txt=title_txt, \
                   data_label=False,resample_freq='H',smooth=True)
    
    return sdf

if __name__=='__main__':
    industries=['801005', '801270', '801250', '801260']
    sdf=compare_industry_sw_sharpe(idfall,industries,base_return='Annual Ret%')
    sdf=compare_industry_sw_sharpe(idfall,industries,base_return='Quarterly Ret%')
    
    sdf=compare_industry_sw_sharpe(idfall,industries,base_return='Exp Ret%')
    
#==============================================================================
if __name__=='__main__':
    start='2018-1-1'
    end='2022-10-31'
    df=get_industry_sw('F')
    idf,idfall=calc_industry_sw(df,start,end)
    base_return='Exp Ret%'
    graph=True
    
    df=rank_industry_sw_sharpe(idfall,base_return='Exp Ret%',axisamp=0.8)

def rank_industry_sw_sharpe(idfall,base_return='Exp Ret%',graph=True,axisamp=0.8,px=False):
    """
    功能：比较申万行业最近的夏普比率，绘制水平柱状图
    idfall: 由calc_industry_sw函数获得
    
    缺陷：未考虑无风险利率
    """

    allindustries=list(set(list(idfall['ticker'])))
    df=compare_industry_sw_sharpe(idfall,allindustries,base_return=base_return,graph=False)
    dftail1=df.tail(1)
    dftail2=dftail1.T
    col=list(dftail2)[0]
    
    dftail3=dftail2.sort_values(by=col,ascending=True)
    dftail3[col]=dftail3[col].apply(lambda x: round(x,2))
        
    istart=idfall['start'].values[0]
    idate=idfall.index.values[-1]
    idate=pd.to_datetime(idate)
    iend=idate.strftime('%Y-%m-%d')

    if graph:
        colname=col
        titletxt="行业板块分析：最新业绩排名"
        import datetime; today=datetime.date.today()
        footnote0='夏普比率(基于'+ectranslate(base_return)+') -->\n\n'
        footnote1='申万行业分类，'+iend+'快照'
        footnote2='观察期：'+istart+'至'+iend+'，'
        footnote3="数据来源: 申万宏源, "+str(today)+'统计'
        footnote=footnote0+footnote1+'\n'+footnote2+footnote3
        if not px:
            footnote=footnote0+footnote1+'\n'+footnote2+footnote3
            plot_barh(dftail3,colname,titletxt,footnote,axisamp=axisamp)
        else: #使用plotly_express
            titletxt="行业板块业绩排名：夏普比率(基于"+ectranslate(base_return)+')'
            footnote=footnote1+'。'+footnote2+footnote3
            plot_barh2(dftail3,colname,titletxt,footnote)

    return dftail3

    
#==============================================================================
if __name__=='__main__':
    industry='801843'
    top=5

def industry_stock_sw(industry='801270',top=5):
    """
    功能：获取申万行业指数的成分股
    排序：按照权重从大到小，重仓优先
    """
    # 检查行业代码的合理性
    inddf=industry_sw_list()
    ilist=list(inddf['code'])
    if not (industry in ilist):
        print("  #Warning(industry_stock_sw): industry code not found",industry)
        return None
    
    import akshare as ak
    try:
        cdf = ak.index_component_sw(industry)
    except:
        print("  #Warning(industry_stock_sw): industry code not found",industry)
        return None

    #排名
    cdf.sort_values(by='最新权重',ascending=False,inplace=True)    
    cdf.reset_index(drop=True,inplace=True)
    cdf['序号']=cdf.index+1
    
    if top > 0:
        cdf1=cdf.head(top)
    else:
        cdf1=cdf.tail(-top)
        
    clist=list(cdf1['证券代码'])
    clist1=[]
    for c in clist:
        first=c[:1]
        if first == '6':
            clist1=clist1+[c+'.SS']
        else:
            clist1=clist1+[c+'.SZ']
    
    return clist1,cdf1
    
if __name__=='__main__':
    clist,cdf=industry_stock_sw(industry='801005',top=10)
    clist,cdf=industry_stock_sw(industry='801005',top=-10)
#==============================================================================
if __name__ =="__main__":
    
    # 新冠疫情三年
    start='2020-2-1'; end='2022-12-20'
    idf,idfall=get_industry_info_sw(start,end)

def get_industry_info_sw(start,end):
    """
    功能：获得申万行业历史数据
    start: 开始日期
    end: 结束日期
    
    返回：idf, idfall，供进一步分析使用。
    """
    
    # 检查日期期间的合理性
    result,startpd,endpd=check_period(start,end)
    if not result:
        print("  #Error(get_industry_info_sw): invalid date period from",start,'to',end)
        return None,None
    
    print("This may need great great time depending on network/computer speed, take a break ...")
    print("\n*** Step 1:")
    # 获取行业历史数据，本步骤所需时间较长
    df=get_industry_sw('I')
    
    print("\n*** Step 2:")
    # 计算基础数据，本步骤所需时间较长
    idf,idfall=calc_industry_sw(df,start,end)
    
    return idf,idfall    

#==============================================================================
if __name__ =="__main__":
    start='2022-1-1'
    end='2022-12-20'
    tickers=['600600.SS','600132.SS','000729.SZ','002461.SZ','600573.SS']
    measures=['Exp Ret%']    
    market_index='000001.SS'
    window=252
    colalign='right'
    
    rs=rank_msecurity_performance(tickers,start,end,measures=['Exp Ret%'])

def rank_msecurity_performance(tickers,start,end, \
                            measures=['Exp Ret%'], \
                            market_index='000001.SS',window=252,colalign='right'):
    """
    功能：列示多只股票多个指标的对比，从高到低
    
    """
    print("Searching for multiple security information, please wait ......") 
    #屏蔽函数内print信息输出的类
    import os, sys
    class HiddenPrints:
        def __enter__(self):
            self._original_stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')

        def __exit__(self, exc_type, exc_val, exc_tb):
            sys.stdout.close()
            sys.stdout = self._original_stdout

    rar_list=['treynor','sharpe','sortino','alpha']
    rar_list_e=['Treynor Ratio','Sharpe Ratio','Sortino Ratio','Jensen alpha']
    rar_list_c=['特雷诺比率','夏普比率','索替诺比率','阿尔法值']

    import pandas as pd
    df=pd.DataFrame()
    allmeasures=measures+rar_list
    for m in allmeasures:
        # 显示进度条
        print_progress_percent2(m,allmeasures,steps=len(allmeasures),leading_blanks=4)
        
        if not (m in rar_list):
            with HiddenPrints():
                dft=compare_msecurity(tickers,measure=m,start=start,end=end,graph=False)
            dft['指标']=ectranslate(m)
        else:
            with HiddenPrints():
                dft=compare_mrar(tickers,rar_name=m,start=start,end=end, \
                             market_index=market_index,window=window,graph=False)
            mpos=rar_list.index(m)
            mname=rar_list_c[mpos]
            dft['指标']=mname
        dft1=dft.tail(1)
        cols1=list(dft1)
        cols1.remove('指标')
        for c in cols1:
            dft1[c]=dft1[c].apply(lambda x: round(float(x),4))
            
        if len(df) == 0:
            df=dft1
        else:
            df=pd.concat([df,dft1])
            
    df.set_index('指标',inplace=True)
    df1=df.T
    cols=list(df1)
    
    # 横向指标求和，作为排序依据
    #df1['value']=df1.loc[:,cols].apply(lambda x: x.sum(),axis=1)
    df1.sort_values('夏普比率',ascending=False,inplace=True)
    #del df1['value']
    
    df1.reset_index(inplace=True)
    df1.rename(columns={'index':'股票'},inplace=True)
    
    alignlist=['center']+[colalign]*(len(allmeasures)-1)
    
    print("\n*** 股票多重指标比较\n")
    print(df1.to_markdown(index=False,tablefmt='plain',colalign=alignlist))
    
    print("\n*** 观察期：",start,'至',end,'\b，表中数据为',end+'快照')
    print("    表中的夏普比率/索替诺比率/阿尔法值均为TTM滚动值")
    import datetime; today=datetime.date.today()
    print("    数据来源：新浪财经/东方财富，"+str(today)+'统计')
    
    return df1
#==============================================================================

#==============================================================================

    