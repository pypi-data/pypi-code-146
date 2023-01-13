# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 14:10:08 2022

@author: man Yip
"""
import pandas as pd
from DagLpDp import DAGLP
import numpy as np

def value_counts_weight(data,weight=None):
    if not isinstance(data,pd.core.series.Series):
        data = pd.Series(data)
    data.name = 'data'
        
    if weight is None:
        weight=pd.Series(np.ones_like(data),index=data.index)
    elif not isinstance(weight,pd.core.series.Series):
        weight = pd.Series(weight)
    weight = weight.loc[data.index]
    weight.name = 'weight'
    
    df = pd.concat([data,weight],axis=1)
    cnt = df.groupby('data',dropna=False)['weight'].sum()
    distr = cnt / cnt.sum()
    return cnt,distr

#截断两头长尾
def trancate_by_distr(distr,min_distr):
    curr=0
    rm_points = []
    for k,v in distr.items():
        curr+=v
        if curr < min_distr:
            rm_points.append(k)
        else:
            rm_points.append(k) #由于是右开区间，所以需要游标多走一位
            break
    
    tmp2 = distr.iloc[::-1]
    curr=0
    for k,v in tmp2.items():
        curr+=v
        if curr < min_distr:
            rm_points.append(k)
        else:
            break        
    return list(distr.loc[~distr.index.isin(rm_points)].index.values)

def gen_connect_table(legal_points,distr,threshold_distr,min_distr):
    ma = distr.keys().max() 
    distr[ma + 0.001] = 0   
    legal_points = legal_points+[ma + 0.001]     
    tables={}
    curr_from = distr.keys().min()
    cursor = 0
    while(cursor < len(legal_points)):
        for end in legal_points[cursor:]:
            v = distr.loc[curr_from:end].sum() - distr.loc[end]
            if v >= min_distr:
                tables[(curr_from,end)] = -1 * (v-threshold_distr)**2
                # tables[(curr_from,end)] = 1 / (v-threshold_distr)**2
        curr_from = legal_points[cursor]  
        cursor+=1
    return tables

#spec_value=[{-9999,-9998},{-8888,-8887,None}]
#如果spec_value中的一个集合中包含None，则空值会被合并。如果没有任何组包含None，则空值自成一组
def freq_cut(data,threshold_distr,min_distr,weight=None,spec_value=None):
    if threshold_distr > 1:
        threshold_distr = 1/threshold_distr
    cnt,distr = value_counts_weight(data,weight)
    distr = distr.loc[distr.index.notna()]
    if spec_value is not None:
        for i in spec_value:
            distr = distr.loc[~distr.index.isin(i)]      
    legal_points = trancate_by_distr(distr,min_distr)
    tables = gen_connect_table(legal_points,distr.copy(),threshold_distr,min_distr)
    dlp = DAGLP(tables)
    if not dlp.done:
        return None
    fc = dlp.max_full_path
    if len(fc) == 0:
        return ['[%s,%s]'%(distr.keys().min(),distr.keys().max())]
    
    bins = []
    for i,v in enumerate(fc):
        if i < len(fc)-2:
            tmp = '[%s,%s)'%(v,fc[i+1])
            bins.append(tmp)
        elif i == len(fc)-2:
            tmp = '[%s,%s]'%(v,distr.keys().max())
            bins.append(tmp)  
    def _sort(s):
        v1 = s[s.index('[')+1 : s.index(',')]
        return float(v1) 
    bins = sorted(bins,key = _sort)
    if spec_value is not None:
        for i in spec_value:
            bins.append(str(i))
    return bins

#已经去掉特殊值的data,未经去特殊值处理的data，不能调用这个内部方法
def _ext_bins(data,bins):
    bin_min_value=None
    bin_min_index=-1
    bin_max_value=None
    bin_max_index=-1
    
    for i,b in enumerate(bins):
        if b[0]=='{':
            continue
        coma = b.index(',')
        v1 = float(b[1:coma])
        if bin_min_value is None or v1 < bin_min_value:
            bin_min_value=v1
            bin_min_index=i
        v2 = float(b[coma+1:-1])
        if bin_max_value is None or (v2 > bin_max_value and b[-1]==']'):
            bin_max_value = v2
            bin_max_index = i
    
    data_min = data.min()
    data_max = data.max()
    
    if bin_min_value is not None and data_min < bin_min_value:
        b = bins[bin_min_index]
        coma = b.index(',')
        bins[bin_min_index] = '%s%s%s'%(b[0],data_min,b[coma:])
        
    if bin_max_value is not None and data_max > bin_max_value:
        b = bins[bin_max_index]
        coma = b.index(',')
        bins[bin_max_index] = '%s%s%s'%(b[:coma+1],data_max,b[-1])
    

def cut_by_bins(data,bins):
    data_bin = pd.Series(data)
    label = pd.Series('',data_bin.index)
    done_none = False
    for b in bins:
        if b[0]=='{':
            if 'None' in b:
                ind = data_bin.loc[data_bin.isna()].index
                label.loc[ind]=b
                data_bin = data_bin.loc[~data_bin.index.isin(ind)]
                done_none = True
            ind = data_bin.loc[data_bin.isin(eval(b))].index
            label.loc[ind] = b
            data_bin = data_bin.loc[~data_bin.index.isin(ind)]
                     
    _ext_bins(data_bin,bins)
    
    for b in bins:
        if b[0]=='{':
          continue
      
        coma = b.index(',')
        v1 = float(b[1:coma])

        if b[0] =='[':
            cond1 = data_bin>=v1
        elif b[0]=='(':
            cond1 = data_bin>v1
        
        v2 = float(b[coma+1:-1])
        if b[-1] ==']':
            cond2 = data_bin <= v2
        elif b[-1]==')':
            cond2 = data_bin < v2
            
        ind = data_bin.loc[cond1 & cond2].index
        label.loc[ind] = b
        data_bin = data_bin.loc[~data_bin.index.isin(ind)]
    if not done_none:   
        label.loc[data_bin.loc[data_bin.isna()].index]='{None}'
        
    if isinstance(data,list):
        label = label.to_list()
        
    if isinstance(data,tuple):
        label = tuple(label)
        
    return label


def freq_cut_array(datas,threshold_distr,min_distr,cutby=0,weight=None,spec_value=None):
    if isinstance(cutby,list):
        bins = cutby
    else:
        bins = freq_cut(datas[cutby],threshold_distr,min_distr,weight,spec_value)
    label_arr = []
    for i in datas:
       cut_by_bins(i,bins)
       
    for i in datas:  
       tmp =  cut_by_bins(i,bins)
       label_arr.append(tmp)    
    return label_arr,bins

def sort_label(s):
    if pd.isna(s):
        return np.inf
    elif s.startswith('['):
        s = s[1:s.index(',')]
        try:
            return float(s)
        except:
            return s
    else:
        return np.inf