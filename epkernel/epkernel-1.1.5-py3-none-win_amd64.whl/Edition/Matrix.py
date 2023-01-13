import os, sys, json
from epkernel import BASE
from epkernel.Edition import Layers
from epkernel.Action import Selection, Information

# 拷贝Layer
# jobname, org_layer_index, dst_layer, poi_layer_index
def copy_layer(jobname:str, old_layer_name:str):
    try:
        ret = BASE.get_matrix(jobname)
        data = json.loads(ret)
        layer_infos = data['paras']['info']
        src_layername=[]
        src_layername= Information.get_layers(jobname)
        if old_layer_name in src_layername:
            for i in range(0, len(layer_infos)):         
                if layer_infos[i]['name'] == old_layer_name:
                    old_layer_index = i + 1
        else:
            print('e')
            return 0
        dst_layer = ''
        # 新建空layer
        create_layer(jobname, 'jbz')
        ret2 = BASE.copy_layer(jobname, old_layer_index,
                               dst_layer, len(layer_infos) + 1)
        data2 = json.loads(ret2)
        new_layer = data2['paras']['newname']
        # 删除新层
        delete_layer(jobname, 'jbz')
        return new_layer
    except Exception as e:
        print(e)
        print('123456')
    return ''

# 创建layer
def create_layer(job:str, layer:str):
    try:
        index = -1  # 默认创建在末尾
        step = ''  # 在所有层创建
        BASE.create_new_layer(job, step, layer, index)
    except Exception as e:
        print(e)

# 删除layer
def delete_layer(job:str, layername:str):
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        layer_infos = data['paras']['info']
        for i in range(0, len(layer_infos)):
            if layer_infos[i]['name'] == layername:
                layer_index = i + 1
                BASE.delete_layer(job, layer_index)
                break
    except Exception as e:
        print(e)
    return 0

def insert_row(job:str, row_index:int,row_name:str):
    try:
        BASE.create_new_layer(job, '', row_name, row_index)
    except Exception as e:
        print(e)
    return 0

def insert_column(job:str, col_index:int,col_name:str):
    try:
        BASE.create_step(job, col_name, col_index)
    except Exception as e:
        print(e)
    return 0

# 创建step
def create_step(job:str, step:str):
    try:
        index = -1  # 默认创建在末尾
        BASE.create_step(job, step, index)
    except Exception as e:
        print(e)

def change_matrix_row(job:str, layer:str, context:str, type:str, layername:str, polarity = True):
    """
    #修改指定层别信息,若修改后信息与原层别一致，则此函数不执行
    :param     jobname:
    :param     layer:
    :param     context:
    :returns   :
    :raises    error:
    """
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        layer_infos = data['paras']['info']
        if polarity == True:
            polarity = 'positive'
        else:
            polarity = 'negative'
        for i in range(0, len(layer_infos)):
            if layer_infos[i]['name'] == layer:
                layer_index = i + 1
                layer_infos[i]['context'] = context
                layer_infos[i]['type'] = type
                layer_infos[i]['name'] = layername
                layer_infos[i]['polarity'] = polarity
        BASE.change_matrix(job, -1, layer_index, '',
                           layer_infos[layer_index-1])
    except Exception as e:
        print(e)
    return 0


def change_matrix_column(job:str, src_name:str, dst_name:str):
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        step_infos = data['paras']['steps']
        old_step_index = step_infos.index(src_name) + 1
        old_layer_index = -1
        new_layer_info = ''
        BASE.change_matrix(job, old_step_index,
                           old_layer_index, dst_name, new_layer_info)
    except Exception as e:
        print(e)


def delete_step(job:str, step:str):
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        step_infos = data['paras']['steps']
        for i in range(0, len(step_infos)):
            if step_infos[i] == step:
                step_index = i + 1
        BASE.delete_step(job, step_index)
    except Exception as e:
        print(e)
    return 0


def copy_step(job:str, src_step_name:str)->str:
    try:
        ret = BASE.get_matrix(job)
        data = json.loads(ret)
        step_infos = data['paras']['steps']
        for i in range(0, len(step_infos)):
            if step_infos[i] == src_step_name:
                old_step_index = i + 1
        dst_step = ''
        # 新建空
        create_step(job, 'jbz') 
        ret= Information.get_steps(job)
        ret2 = BASE.copy_step(job, old_step_index,
                              dst_step, len(step_infos)+1)
        data2 = json.loads(ret2)
        new_step = data2['paras']['newname']
        # 删除新层
        delete_step(job, 'jbz')
        return new_step
    except Exception as e:
        print(e)
    return ''

#备份多层（覆盖）(需备份层无选中feature)
def backup_layer(job:str, step:str, layers:list, suffix:str):
    try:
        layer_list = Information.get_layers(job)
        for layer in layers:
            new_layer = layer + suffix
            if new_layer not in layer_list:
                create_layer(job, new_layer)
            else:
                BASE.clear_selected_features(job, step, new_layer)
                Selection.reverse_select(job, step, new_layer) 
                Layers.delete_feature(job, step, new_layer)  
                BASE.clear_selected_features(job, step, new_layer)
            Layers.copy_other(job, step, layer, new_layer, False, 0, 0, 0, 0, 0, 0, 0)
    except Exception as e:
        print(e)
        return None
        

def move_layer(job:str, org_layer_index:int, dst_layer_index:int):
    try:
        jobname = job
        BASE.move_layer(jobname, org_layer_index, dst_layer_index)
    except Exception as e:
        print(e)
        return None