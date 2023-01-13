import os, sys, json
import math
from tkinter.font import BOLD
from epkernel import BASE
from epkernel.Action import Information

def set_attribute_filter(logic:int, attribute_list:list):
    """
    #设置属性筛选
    :param     logic:0 ：全部满足  1:有其一
    :param     attribute_list:要设置的属性列表
    :returns   :
    :raise    error:
    """
    try:
        BASE.filter_set_attribute(logic, attribute_list)
    except Exception as e:
        print(e)
    return 0

def select_features_by_filter(job:str, step:str, layers:list):
    """
    #根据筛选条件选择
    :param     job:
    :param     step:
    :param     layers:layer列表
    :returns   :
    :raises    error:
    """
    try:
        BASE.select_features_by_filter(job, step, layers)
    except Exception as e:
        print(e)
    return 0

def reset_select_filter():
    try:
        BASE.set_select_param(0x7F, False, [], 0, 0, -1, -1, [], 0, True)
    except Exception as e:
        print(e)
    return 0

def clear_select(job:str, step:str, layer = ''):
    try:
        layers = Information.get_layers(job)
        if layer == '':
            for layer in layers:
                BASE.clear_selected_features(job, step, layer)
        else:
            BASE.clear_selected_features(job, step, layer)
    except Exception as e:
        print(e)
    return 0
    
def set_featuretype_filter(positive:bool,negative:bool,text:bool,surface:bool,arc:bool,line:bool,pad:bool):
    '''
    需要筛选的feature类型,以二进制计算,计算顺序依次为:正极性,负极性,text,surface,arc,line,pad
    七个参数类型是bool,参数是True:参与计算求和,否则不参与计算求和。
    '''
    try:
        featuretype_sum=0
        ret = BASE.get_select_param()
        data = json.loads(ret)
        select_param = data['paras']['param']
        #print(data)  
        flag = select_param['attributes_flag']
        value = select_param['attributes_value']   
        symbols = select_param['symbols']
        pr_value = select_param['profile_value']
        sele = select_param['use_selection']
        minline = select_param['minline']
        maxline = select_param['maxline']
        dcode = select_param['dcode']
        has_symbol = select_param['has_symbols']
        featuretype_list= [positive,negative,text,surface,arc,line,pad]
        for index in range(len(featuretype_list)):
            if featuretype_list[index]==True:
                featuretype_list[index]=len(featuretype_list)-index-1
            else:
                featuretype_list[index]=None
        for type_ in featuretype_list:
            if type_!=None:
                featuretype_sum += math.pow(2,type_)
        BASE.set_select_param(featuretype_sum, has_symbol, symbols,minline, maxline,dcode, flag,value, pr_value,sele)
    except Exception as e:
        print(e)
        return None


def set_include_symbol_filter(symbol_list:list):
    """
    #设置include symbol筛选
    :param     symbol_list:设置筛选include_symbol的list
    :returns   :
    :raises    error:
    """
    try:
        ret = BASE.get_select_param()
        data = json.loads(ret)
        select_param = data['paras']['param']
        featuretype = select_param['featuretypes']
        flag = select_param['attributes_flag']
        value = select_param['attributes_value']   
        pr_value = select_param['profile_value']
        sele = select_param['use_selection']
        minline = select_param['minline']
        maxline = select_param['maxline']
        dcode = select_param['dcode']
        if symbol_list == '':
            BASE.set_select_param(featuretype, False, symbol_list,minline, maxline,dcode, flag,value, pr_value,sele)
        else :
            BASE.set_select_param(featuretype, True, symbol_list,minline, maxline,dcode, flag,value, pr_value,sele)

    except Exception as e:
        print(e)
    return 0

def reverse_select(job:str, step:str, layer:str):
    """
    #反选
    :param     job:
    :param     step:
    :param     layer:
    :returns   :
    :raises    error:
    """
    try:
        BASE.counter_election(job, step, layer)
    except Exception as e:
        print(e)
    return 0

def set_selection(is_standard:bool, is_clear:bool, all_layers:bool, is_select:bool, inside:bool, exclude:bool):
    try:
        BASE.set_selection(is_standard, is_clear, all_layers, is_select, inside, exclude)
    except Exception as e:
        print(e)
    return 0

#重置设置模式
def reset_selection():
    try:
        BASE.set_selection(True, True, True, True, True, True)
    except Exception as e:
        print(e)
    return 0

#取消选中
def unselect_features(job:str, step:str, layer:str):
    try:
        BASE.unselect_features(job, step, layer)
    except Exception as e:
        print(e)
    return 0

def select_feature_by_polygon(job:str, step:str, layer:str, selectpolygon:list):
    try:
        BASE.select_feature(job, step, layer, selectpolygon, {}, 1, True) # 1：框选 
    except Exception as e:
        print(e)
    return 0

def select_feature_by_point(job:str, step:str, layer:str, location_x:int,location_y:int):
    try:
        selectpolygon=[]
        min = 1 #nm
        selectpolygon.append([location_x-min,location_y-min])
        selectpolygon.append([location_x+min,location_y-min])
        selectpolygon.append([location_x+min,location_y+min])
        selectpolygon.append([location_x-min,location_y+min])
        selectpolygon.append([location_x-min,location_y-min])
        BASE.select_feature(job, step, layer, selectpolygon, {}, 0, True) # 0：点选  
    except Exception as e:
        print(e)
    return 0
    
#0:all 1:in 2:out
def set_inprofile_filter(mode:int):
    try:
        ret = BASE.get_select_param()
        data = json.loads(ret)
        select_param = data['paras']['param']
        BASE.set_select_param(select_param['featuretypes'], select_param['has_symbols'], select_param['symbols'], 
                                select_param['minline'], select_param['maxline'],
                                select_param['dcode'], select_param['attributes_flag'],
                                select_param['attributes_value'], mode,
                                select_param['use_selection'])
    except Exception as e:
        print(e)
    return 0

def select_feature_by_id(job:str, step:str, layer:str, ids:list):
    try:
        ret= Information.check_matrix_info(job,step,[layer])
        if ret==True:
            BASE.select_feature_by_id(job, step, layer, ids)
    except Exception as e:
        print(e)
    return 

def filter_by_mode(jobname:str, step:str, layer:str, reference_layers:list, mode:int, positive:bool,negative:bool,text:bool,surface:bool,arc:bool,line:bool,pad:bool, symbolflag:int,symbolnames:list, attrflag = -1,
                    attrlogic = 0, attributes = []):
    try:
        feature_type_ref=0
        featuretype_list= [positive,negative,text,surface,arc,line,pad]
        for index in range(len(featuretype_list)):
            if featuretype_list[index]==True:
                featuretype_list[index]=len(featuretype_list)-index-1
            else:
                featuretype_list[index]=None
        for type_ in featuretype_list:
            if type_!=None:
                feature_type_ref += math.pow(2,type_)
        BASE.filter_by_mode(jobname, step, layer, reference_layers, mode, feature_type_ref, symbolflag , symbolnames, attrflag = -1,
                    attrlogic = 0, attributes = [])
    except Exception as e:
        print(e)
        return None

def unselect_features_by_filter(job:str, step:str, layers:list):
    try:
        BASE.unselect_features_by_filter(job, step, layers)
    except Exception as e:
        print(e)
    return 
    
def set_symbol_filter(has_symbols:bool, symbol_list:list):
    try:
        ret = BASE.get_select_param()
        data = json.loads(ret)
        select_param = data['paras']['param']
        featuretype = select_param['featuretypes']
        flag = select_param['attributes_flag']
        value = select_param['attributes_value']   
        pr_value = select_param['profile_value']
        sele = select_param['use_selection']
        minline = select_param['minline']
        maxline = select_param['maxline']
        dcode = select_param['dcode']
        symbols = []
        for j in symbol_list:
            ss = []
            s = ''
            n = ''
            for i in range(len(j)):
                if j[i].isdigit() or j[i] == '.':
                    if not s == '':
                        ss.append(s)
                        s = ''
                    n += j[i]
                    if i == len(j) - 1:
                        ss.append(n)
                        n = ''  
                else:
                    s += j[i]
                    if not n == '':
                        ss.append(n)
                        n = ''
                    if i == len(j) - 1:
                        ss.append(s)
                        s = ''
            cc = ''
            for d in ss:
                if d.isdigit() or '.' in d:
                    if '.' in d:
                        e1 = d.split('.')[0]
                        e2 = d.split('.')[1]
                        if len(e2) < 3:
                            e2 = e2.ljust(3, '0')
                        d = e1 + '.' + e2    
                cc += d
            symbols.append(cc)
        BASE.set_select_param(featuretype, has_symbols, symbols, minline, maxline, dcode, flag, value, pr_value, sele)
    except Exception as e:
        print(e)
    return 0    
    
    
    
    
    
    