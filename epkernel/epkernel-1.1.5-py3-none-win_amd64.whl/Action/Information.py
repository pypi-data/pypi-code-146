import os, sys, json, math
from epkernel import epcam, BASE

def check_matrix_info(job:str, step='', layers=[])->bool:
    try:
        if isinstance(job, str) and isinstance(step, str) and isinstance(layers, list):
            open_jobs = get_opened_jobs()
            if job in open_jobs: 
                if step == '' and layers == []:
                    return False
                step_lst= get_steps(job)
                layer_lst = get_layers(job)
                if step!='':
                    if step not in step_lst:
                        print('step不存在')
                        return False
                if layers!=[]:
                    for layer in layers:
                        if layer not in layer_lst:
                            print(layer + ' 不存在')
                            return False
            else:
                print(f'{job}:未打开,请查找原因!')
                return False
        else:
            print("请检查填写的参数类型!")
            return False
    except Exception as e:
        return False
        print(e)
    return True

def is_selected(job:str,step:str,layer:str)->bool:
    ret = BASE.is_selected(job,step,layer)
    ret = json.loads(ret)
    if 'result' in ret:
        return ret['result']
    return False

def get_drill_layer_name(job:str)->list:
    """
    #获取孔层layer名
    :param     job:
    :param     step:
    :return    drill_list:孔层名列表
    :raises    error:
    """
    try:
        ret = BASE.get_graphic(job)
        data = json.loads(ret)
        drill_list = []
        layer_info = data['paras']['info']
        for i in range(0, len(layer_info)):
            if layer_info[i]['type'] == 'drill' and layer_info[i]['context'] == 'board':
                drill_list.append(layer_info[i]['name'])
        return drill_list
    except Exception as e:
        print(e)
        #sys.exit(0)
    return []

def get_inner_layers(job:str)->list:
    """
    #获取内层layer_list
    :param     job:
    :returns   inner_layer_list:内层layername列表
    :raises    error:
    """
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        layer_info = data['paras']['info']
        board_layer_list=[]
        for i in range(0, len(layer_info)):
            if layer_info[i]['context'] == 'board' and layer_info[i]['type'] == 'signal':
                board_layer_list.append(layer_info[i]['name'])      
        if len(board_layer_list) <= 2:
            print('no inner layer!')
            return []
        else:
            board_layer_list.pop(-1)
            board_layer_list.pop(0)
            inner_layer_list = board_layer_list
        return inner_layer_list
    except Exception as e:
        print(e)
    return []

def get_board_layers(job:str)->list:
    try:
        ret = BASE.get_graphic(job)
        data = json.loads(ret)
        layer_list = []
        layer_info = data['paras']['info']
        if len(layer_info):
            for i in range(0, len(layer_info)):
                if layer_info[i]['context'] == 'board':
                    layer_list.append(layer_info[i]['name'])
        return layer_list
    except Exception as e:
        print(e)
        #sys.exit(0)
    return ''

def get_soldermask_layers(job:str)->list:
    """
    #获取防焊层list
    :param     job:
    :param     step:
    :returns   solder_mask_list:
    :raises    error:
    """
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        layer_info = data['paras']['info']
        solder_mask_list=[]
        for i in range(0, len(layer_info)):
            if layer_info[i]['context'] == 'board' and layer_info[i]['type'] == 'solder_mask':
                solder_mask_list.append(layer_info[i]['name'])      
        return solder_mask_list
    except Exception as e:
        print(e)
    return ''

def get_signal_layers(job:str)->list:
    """
    #获取内外层layer 名
    :param     job:
    :returns   inner_layer_list:内层layername列表
    :raises    error:
    """
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        layer_info = data['paras']['info']
        board_layer_list=[]
        for i in range(0, len(layer_info)):
            if layer_info[i]['context'] == 'board' and layer_info[i]['type'] == 'signal':
                board_layer_list.append(layer_info[i]['name'])
        return board_layer_list
    except Exception as e:
        print(e)
    return []

def get_outer_layers(job:str)->list:
    """
    #获取外层list
    :param     job:
    :returns   outter_layer_list:外层layername列表
    :raises    error:
    """
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        layer_info = data['paras']['info']
        board_layer_list=[]
        index_list = []
        for i in range(0, len(layer_info)):
            if layer_info[i]['context'] == 'board' and layer_info[i]['type'] == 'signal':
                index_list.append(i)
        if index_list == []:
            print("no signal layer")
            return []
        for j in range(min(index_list),max(index_list)+1):
            board_layer_list.append(layer_info[j]['name'])
        outter_layer_list = []
        outter_layer_list.append(board_layer_list[0])
        if len(board_layer_list) == 1:
            return outter_layer_list
        else: 
            outter_layer_list.append(board_layer_list[-1])
        return outter_layer_list
    except Exception as e:
        print(e)
    return ''

def get_silkscreen_layers(job:str)->list:
    """
    #获取丝印层layer_list        
    :param     job:     
    :returns   layer_list:丝印层layername列表     
    :raises    error:    
    """
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        layer_info = data['paras']['info']
        layer_list = []
        for i in range(0, len(layer_info)):
            if layer_info[i]['context'] == 'board' and layer_info[i]['type'] == 'silk_screen':
                layer_list.append(layer_info[i]['name'])
        
        if len(layer_list) < 1:
            print("can't find silk_screen-layer!")

        return layer_list
    except Exception as e:
        print(e)
    return ''

def get_soldermask_layers(job:str)->list:
    """
    #获取防焊层list
    :param     job:
    :param     step:
    :returns   solder_mask_list:
    :raises    error:
    """
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        layer_info = data['paras']['info']
        solder_mask_list=[]
        for i in range(0, len(layer_info)):
            if layer_info[i]['context'] == 'board' and layer_info[i]['type'] == 'solder_mask':
                solder_mask_list.append(layer_info[i]['name'])      
        return solder_mask_list
    except Exception as e:
        print(e)
    return ''

#获取layer profile polygon
def get_profile(job:str, step:str)->list:
    try:
        _ret = BASE.get_profile(job, step)
        ret = json.loads(_ret)['points']
        return ret
    except Exception as e:
        print(e)
    return []

    
def get_layer_feature_count(job:str, step:str, layer:str)->int:
    ret = BASE.get_layer_feature_count(job, step, layer)
    ret = json.loads(ret)
    if 'featureNum' in ret:
        return int(ret['featureNum'])
    return -1

def get_steps(job:str)->list:
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        steps = data['paras']['steps']
        return steps
    except Exception as e:
        print(e)
    return []

def get_layers(job:str)->list:
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        layer_infos = data['paras']['info']
        layer_list = []
        for i in range(0, len(layer_infos)):
            layer_list.append(layer_infos[i]['name'])
        return layer_list
    except Exception as e:
        print(e)
    return []

def get_usersymbol_list(job:str)->list:
    try:
        ret = BASE.get_special_symbol_names(job)
        data = json.loads(ret)
        user_list = data['paras']
        return user_list
    except Exception as e:
        print(e)
    return []

def get_profile_box(job:str, step:str)->dict:  
    try:
        #转成小写
        job= job.lower()
        step= step.lower()
        info= check_matrix_info(job, step)
        if info:
            ret_= BASE.has_profile(job,step)
            data_= json.loads(ret_)['result']
            if data_:
                ret = BASE.get_profile_box(job, step)
                data = json.loads(ret)
                profile_box = data['paras']
                return profile_box
            print('没有profile!')
            return {}
        return None
    except Exception as e:
        print(e)
    return None

#获取拼版中最小和最大坐标
def get_inner_profile_box(job:str,step:str)->dict:
    try:
        repeat_infos=BASE.get_step_repeat(job,step)    #获取拼板信息
        repeat_infos=json.loads(repeat_infos)
        repeat_infos=repeat_infos['result']
        xminlist=[]
        yminlist=[]
        xmaxlist=[]
        ymaxlist=[]
        for repeat_info in repeat_infos:
            repeat_infox=repeat_info['X']
            repeat_infoy=repeat_info['Y']
            set_box=BASE.get_profile_box(job, repeat_info['NAME'])
            set_box=json.loads(set_box)['paras']
            datum_x=json.loads(BASE.get_step_header_infos(job, repeat_info['NAME']))['x_datum']
            datum_y=json.loads(BASE.get_step_header_infos(job, repeat_info['NAME']))['y_datum']
            x_offset = repeat_infox - datum_x
            y_offset = repeat_infoy - datum_y
            pts=[]
            pts.append([set_box['Xmin']+x_offset,set_box['Ymin']+y_offset])
            pts.append([set_box['Xmin']+x_offset,set_box['Ymax']+y_offset])
            pts.append([set_box['Xmax']+x_offset,set_box['Ymax']+y_offset])
            pts.append([set_box['Xmax']+x_offset,set_box['Ymin']+y_offset])
            width=set_box['Xmax']-set_box['Xmin']
            height=set_box['Ymax']-set_box['Ymin']
            if repeat_info['MIRROR']:
                pts.clear()
                pts.append([set_box['Xmin']+x_offset-width,set_box['Ymin']+y_offset])
                pts.append([set_box['Xmin']+x_offset-width,set_box['Ymax']+y_offset])
                pts.append([set_box['Xmin']+x_offset,set_box['Ymax']+y_offset])
                pts.append([set_box['Xmin']+x_offset,set_box['Ymin']+y_offset])

            if repeat_info['ANGLE']!=0:
                value = math.acos(-1) / 180
                ratio = -1 * repeat_info['ANGLE'] * value
                if repeat_info['MIRROR']:
                    ratio = -1 * (360-repeat_info['ANGLE']) * value
                for pt in pts:
                    a = pt[0]
                    b = pt[1]
                    pt[0]=(a - repeat_infox)*math.cos(ratio) - (b - repeat_infoy)*math.sin(ratio) + repeat_infox
                    pt[1]=(a - repeat_infox)*math.sin(ratio) + (b - repeat_infoy)*math.cos(ratio) + repeat_infoy
            allx=[]
            ally=[]
            for pt in pts:
                allx.append(pt[0])
                ally.append(pt[1])
            allx.sort()
            ally.sort()
            xmin=allx[0]
            ymin=ally[0]
            set_length=allx[-1]-allx[0]
            set_width=ally[-1]-ally[0]    
            length= (repeat_info['NX']-1)*repeat_info['DX']+set_length
            width = (repeat_info['NY']-1)*repeat_info['DY']+set_width
            xmax=xmin+length
            ymax=ymin+width
            xminlist.append(xmin)
            yminlist.append(ymin)
            xmaxlist.append(xmax)
            ymaxlist.append(ymax)
        xminlist.sort()
        yminlist.sort()
        xmaxlist.sort(reverse=True)
        ymaxlist.sort(reverse=True)
        gSRxmin=xminlist[0]
        gSRymin=yminlist[0]
        gSRxmax=xmaxlist[0]
        gSRymax=ymaxlist[0]
        gSRxcenter = (gSRxmax-gSRxmin)/2
        gSRycenter = (gSRymax-gSRymin)/2
        infos={}
        infos['gSRxmin']=gSRxmin
        infos['gSRymin']=gSRymin
        infos['gSRxmax']=gSRxmax
        infos['gSRymax']=gSRymax
        infos['gSRxcenter'] = gSRxcenter
        infos['gSRycenter'] = gSRycenter
        return infos
    except Exception as e:
        print(e)
    return {}

def get_selected_features_box(job:str, step:str, layers:list)->dict:
    try:
        job= job.lower()
        step= step.lower()
        for layer in range(len(layers)):
            layers[layer] = layers[layer].lower()
        info= check_matrix_info(job, step,layers)
        if info:                
            ret = BASE.get_selected_features_box(job, step, layers)
            data = json.loads(ret)
            features_box=[]
            for value in data.values():
                features_box.append(value)
            if len(set(features_box))==1:
                print("No features are selected!")
                return {}
            else:
                return data
        return None
    except Exception as e:
        print(e)
    return None


def get_rest_cu_rate(job:str,step:str,layer:str,thickness:int)->float:
    try:
        resolution_define = 1000
        ret = BASE.get_rest_cu_rate(job,step,layer,resolution_define,thickness)
        cu_t = json.loads(ret)['result']
        data = float(cu_t.split('/')[1])/100
        return data
    except Exception as e:
        print(e)
        return -1
        
def get_opened_jobs()->list:
    try:
        ret= BASE.get_opened_jobs()
        data= json.loads(ret)
        if 'paras' in data:
            return data['paras']
        else:
            return []
    except Exception as e:
        print(repr(e))
        return None

#获取选中feature的坐标,symbolname,极性, 角度, 是否镜像
def get_selected_features_infos(job:str, step:str, layer:str)->list:
    try:
        ret = BASE.get_selected_feature_infos(job, step, layer)
        data = json.loads(ret)
        featureinfos = []
        if data['paras'] != False:
            return data['paras']
    except Exception as e:
        print(e)
    return None

def get_selected_features_count(job:str, step:str, layer = '')->int:
    try:
        if layer != '':
            count_sum=0
            features_count = get_selected_features_infos(job,step,layer)
            if features_count!=None:
                count_sum = len(features_count)
            else:
                count_sum = 0
            return count_sum
        else:
            sum = 0
            layers = get_layers(job)
            for i in layers:
                feature_count = get_selected_features_infos(job,step,i)
                if feature_count !=None:
                    count = len(feature_count)
                else:
                    count = 0
                sum = sum+count
            return sum
    except Exception as e:
        print(e)
    return None

#获取当前状态下筛选器的筛选状态
def get_select_param()->dict:
    try:
        featuretype_list= ['positive','negative','text','surface','arc','line','pad']
        ret= BASE.get_select_param()
        data = json.loads(ret)
        if data['paras']!=False:
            infos= data['paras']['param']
            featuretypes= infos['featuretypes']
            result= BASE.Dec2Bin(featuretypes)
            if len(result)!=7 and featuretypes>32:
                result.reverse()
                result_new= result
                result_new.append(0)
                result_new.reverse()
            else:
                result_new=result
            bool_lst=[]
            for value in result_new:
                if value==1:
                    bool_lst.append(True)
                else:
                    bool_lst.append(False)
            new_lst = dict(zip(featuretype_list, bool_lst))
            infos['featuretypes']=new_lst
            return infos
    except Exception as e:
        print(repr(e))
    return None

def get_system_attr_defines()->list:
    try:
        ret = BASE.get_system_attr_defines()
        data = json.loads(ret)
        if data['paras'] != False:
            return data['paras']
    except Exception as e:
        print(e)
    return None

def get_user_attr_defines()->list:
    try:
        ret = BASE.get_user_attr_defines()
        data = json.loads(ret)
        if data['paras'] != False:
            return data['paras']
    except Exception as e:
        print(e)
    return None

def get_powerground_layers(job:str)->list:
    try:
        ret = BASE.get_graphic(job)
        data = json.loads(ret)
        power_ground_list = []
        layer_info = data['paras']['info']
        for i in range(0, len(layer_info)):
            if layer_info[i]['context'] == 'board' and layer_info[i]['type'] == 'power_ground':
                power_ground_list.append(layer_info[i]['name'])
        if len(power_ground_list)<1:
            print("can't find power_ground-layers!")
            return []
        return power_ground_list
    except Exception as e:
        print(e)
    return None
    
def get_layer_info(job:str,context:str,type:list)->list:
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        layer_infos = data['paras']['info']
        layer_list =[]
        for i in range(0,len(layer_infos)):
            for j in range(len(type)):
                if layer_infos[i]['context'] ==context and layer_infos[i]['type']==type[j]:
                    layer_dict = {}
                    layer_dict['name'] = layer_infos[i]['name']
                    layer_dict['context'] = layer_infos[i]['context']
                    layer_dict['type'] = layer_infos[i]['type']
                    layer_dict['start_name'] = layer_infos[i]['start_name']
                    layer_dict['end_name'] = layer_infos[i]['end_name']
                    layer_dict['polarity'] = layer_infos[i]['polarity']
                    layer_list.append(layer_dict)
        return layer_list
    except Exception as e:
        print(e)
    return []

def get_step_info(job:str,step:str)->list:
    try:
        ret = BASE.get_step_repeat(job,step)
        data = json.loads(ret)
        step_info = data['result']
        step_list = []
        for i in range(0,len(step_info)):
            step_dict = {}
            step_dict['NAME'] = step_info[i]['NAME']
            step_dict['X'] = step_info[i]['X']
            step_dict['Y'] = step_info[i]['Y']
            step_dict['DX'] = step_info[i]['DX']
            step_dict['DY'] = step_info[i]['DY']
            step_dict['NX'] = step_info[i]['NX']
            step_dict['NY'] = step_info[i]['NY']
            step_dict['ANGLE'] = step_info[i]['ANGLE']
            step_dict['MIRROR'] = step_info[i]['MIRROR']
            step_list.append(step_dict)
        return step_list
    except Exception as e:
        print(e)
    return []
    

def get_layer_information(job:str)->list:
    try:
        _ret = BASE.get_matrix(job)
        data = json.loads(_ret)
        ret =[]
        ret = data['paras']['info']
        signal_list = []
        solder_list = []
        silk_list = []
        paste_list = []
        j = 0
        for j in range(0,len(ret)):
            if ret[j]['context'] =='board'and ret[j]['type'] == 'signal':
                signal_list.append(ret[j]['row'])
            elif ret[j]['context'] =='board'and ret[j]['type'] == 'solder_mask':
                solder_list.append(ret[j]['row'])
            elif ret[j]['context'] =='board'and ret[j]['type'] == 'silk_screen':
                silk_list.append(ret[j]['row'])
            elif ret[j]['context'] == 'board' and ret[j]['type'] == 'solder_paste':
                paste_list.append(ret[j]['row'])
        b = len(signal_list)
        b_list = signal_list[1:(b-1)]
        for i in ret:
                index = i['row']
                if index == signal_list[0]:
                    i['orientation'] = "top_signal"
                elif index == signal_list[-1]:
                    i['orientation'] = "bottom_signal"
                elif (index in b_list):
                    i['orientation'] = 'inner'
                elif (index in solder_list):
                    l1 = abs(signal_list[0]-index) 
                    l2 = abs(signal_list[-1]-index) 
                    if l1<l2:
                        i['orientation'] = 'top_solder_mask'
                    elif l1>l2:
                        i['orientation'] = 'bottom_solder_mask'
                elif (index in silk_list):
                    l1 = abs(signal_list[0]-index)
                    l2 = abs(signal_list[-1]-index)
                    if l1<l2:
                        i['orientation'] = 'top_silk_screen'
                    elif l1>l2:
                        i['orientation'] = 'bottom_silk_screen'
                elif (index in paste_list):
                    l1 = abs(signal_list[0]-index)
                    l2 = abs(signal_list[-1]-index)
                    if l1<l2:
                        i['orientation'] = 'top_solder_paste'
                    elif l1>l2:
                        i['orientation'] = 'bottom_solder_paste'
                else:
                    i['orientation'] = ''
        return ret
    except Exception as e:
        print(e)
    return []

def get_all_selected_features_count(job:str, step:str)->int:
    try:
        sum = 0
        layers = get_layers(job)
        feature_list = []
        feature_dict = {}
        for i in layers:
            layer = i
            ret = is_selected(job,step,layer)
            if ret ==True:
                count = get_selected_features_count(job,step,layer)
                sum = sum+count
            else:
                count = 0
            feature_dict[layer] = count
        feature_list.append(feature_dict)
        feature_list.append(sum)
        return feature_list
    except Exception as e:
        print(e)
    return None

def get_drill_info(job:str, step:str, layer:str)->list:
    try:
        layer_info = get_layer_information(job)
        for i in range(0,len(layer_info)):
            if layer_info[i]['name']==layer and layer_info[i]['context'] == 'board' and layer_info[i]['type'] =='drill':
                _ret = BASE.auto_get_drill_info(job,step,layer)
                ret = json.loads(_ret)['result']['data']['drills']
                return ret
    except Exception as e:
        print(e)
    return None
    
def get_all_features_report(job:str, step:str, layer:str)->dict:
    try:
        BASE.load_layer(job, step, layer)
        _ret = BASE.get_all_features_report(job,step,layer)
        ret = json.loads(_ret)['paras']
        return ret
    except Exception as e:
        print(e)
    return {}    

    
def get_layer_report(job:str, layer:str)->dict:
    try:
        aa =BASE.get_matrix(job)
        ret = json.loads(aa)['paras']['info']
        signal_list = []
        solder_list = []
        silk_list = []
        j = 0
        for j in range(0,len(ret)):
            if ret[j]['context'] =='board'and ret[j]['type'] == 'signal':
                signal_list.append(ret[j]['row'])
            elif ret[j]['context'] =='board'and ret[j]['type'] == 'solder_mask':
                solder_list.append(ret[j]['row'])
            elif ret[j]['context'] =='board'and ret[j]['type'] == 'silk_screen':
                silk_list.append(ret[j]['row'])
        b = len(signal_list)
        b_list = signal_list[1:(b-1)]
        for i in range(0,len(ret)):
            if ret[i]['name'] == layer:
                index = ret[i]['row']
                layer_dict = {}
                if index == signal_list[0]:
                    layer_dict['location'] = "outer_top"
                elif index == signal_list[-1]:
                    layer_dict['location'] = "outer_bottom"
                elif (index in b_list):
                    layer_dict['location'] = 'inner'
                elif (index in solder_list):
                    l1 = abs(signal_list[0]-index) 
                    l2 = abs(signal_list[-1]-index) 
                    if l1<l2:
                        layer_dict['location'] = 'top'
                    elif l1>l2:
                        layer_dict['location'] = 'bottom'
                elif (index in silk_list):
                    l1 = abs(signal_list[0]-index)
                    l2 = abs(signal_list[-1]-index)
                    if l1<l2:
                        layer_dict['location'] = 'top'
                    elif l1>l2:
                        layer_dict['location'] = 'bottom'
                layer_dict['context'] = ret[i]['context']
                layer_dict['type'] = ret[i]['type']
        return layer_dict
    except Exception as e:
        print(e)
    return {}

def get_outerlayer_closest_soldermask(job:str, layer:str)->str:
    try:
        ret  = BASE.get_matrix(job)
        ret = json.loads(ret)['paras']['info']
        signal_list = []
        for i in range(0,len(ret)):
            if ret[i]['name'] ==layer and ret[i]['type'] == 'solder_mask' and ret[i]['context'] == 'board':
                index = ret[i]['row']
                break
        for n in range(0,len(ret)):
            if ret[n]['context'] =='board'and ret[n]['type'] == 'signal':
                signal_list.append(ret[n]['row'])
        l1 = abs(signal_list[0]-index)
        l2 = abs(signal_list[-1]-index)
        if l1<l2:
            top = signal_list[0]
        elif l1>l2:
            top = signal_list[-1]
        for m in range(0,len(ret)):
            if ret[m]['row'] == top:
                name = ret[m]['name']
                break
        return name
    except Exception as e:
        print(e)
    return ''

def get_soldermask_closest_signal(job:str, layer:str)->str:
    try:
        ret  = BASE.get_matrix(job)
        ret = json.loads(ret)['paras']['info']
        silk_list = []
        for i in range(0,len(ret)):
            if ret[i]['name'] ==layer and ret[i]['context'] == 'board' and ret[i]['type'] == 'signal':
                index = ret[i]['row']
                break
        for n in range(0,len(ret)):
            if ret[n]['context'] =='board'and ret[n]['type'] == 'solder_mask':
                silk_dict = {}
                silk_dict['row'] = ret[n]['row']
                silk_dict['name'] = ret[n]['name']
                silk_list.append(silk_dict)
        datum = []
        b = []
        for m in silk_list:
            d = abs(m['row']-index)
            b.append(d)
            silk = {}
            silk['name'] = m['name']
            silk['delta'] = d
            datum.append(silk)
        a = min(b)
        for o in datum:
            delta = o['delta']
            if a == delta:
                layername = o['name']
        return layername
    except Exception as e:
        print(e)
    return ''

def get_drill_cross(job:str, layer:str)->list:
    try:
        ret = BASE.get_matrix(job)
        ret = json.loads(ret)['paras']['info']
        layer_list = []
        drill_list=[]
        for i in range(0,len(ret)):
            if ret[i]['name'] ==layer and ret[i]['type'] == 'drill' and ret[i]['context'] == 'board':
                start = ret[i]['start_name']
                end = ret[i]['end_name']
                break
        for n in range(0,len(ret)):
            if ret[n]['name'] == start or ret[n]['name'] == end:
                drill_list.append(ret[n]['row'])
                name_list = list(range(math.ceil(drill_list[0]), math.floor(drill_list[-1]) + 1))
        for m in range(0,len(ret)):
            b = ret[m]['row']
            if (b in name_list):
                layer_dict = {}
                layer_dict['name'] = ret[m]['name']
                layer_dict['index'] = ret[m]['row']
                layer_list.append(layer_dict)
        return layer_list
    except Exception as e:
        print(e)
    return []

def get_rout_cross(job:str, layer:str)->list:
    try:
        ret = BASE.get_matrix(job)
        ret = json.loads(ret)['paras']['info']
        layer_list = []
        rout_list=[]
        for i in range(0,len(ret)):
            if ret[i]['name'] ==layer and ret[i]['context'] == 'board' and ret[i]['type'] == 'rout':
                start = ret[i]['start_name']
                end = ret[i]['end_name']
                break
        for n in range(0,len(ret)):
            if ret[n]['name'] == start or ret[n]['name'] == end:
                rout_list.append(ret[n]['row'])
        name_list = list(range(math.ceil(rout_list[0]), math.floor(rout_list[-1]) + 1))
        for m in range(0,len(ret)):
            b = ret[m]['row']
            if (b in name_list):
                layer_dict = {}
                layer_dict['name'] = ret[m]['name']
                layer_dict['index'] = ret[m]['row']
                layer_list.append(layer_dict)
        return layer_list
    except Exception as e:
        print(e)
    return []
    
def get_datum_point(job:str, step:str)->dict:
    try:
        _ret = BASE.get_step_header_infos(job,step)
        ret = json.loads(_ret)
        point_dict = {}
        point_dict['x_datum'] = ret['x_datum']
        point_dict['y_datum'] = ret['y_datum']
        return point_dict
    except Exception as e:
        print(e)
    return {}    
    
    
    
    
    
    
    
    