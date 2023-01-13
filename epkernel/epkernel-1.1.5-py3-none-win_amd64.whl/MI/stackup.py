import os,sys,json
from epkernel import BASE

def save_drill_belts(job:str, drillbelts:dict)->bool:
    try:
        step = drillbelts['stepName']
        infoList = drillbelts['info']
        copperLayerNum = drillbelts['copperLayerNum']
        _ret = BASE.save_drill_belts(job,step,infoList,copperLayerNum)
        ret = json.loads(_ret)['status']
        if ret == 'true':
            ret = True
        else:
            ret = False
        return ret 
    except Exception as e:
        print(e)
    return False

def get_drill_belts(job:str)->dict:
    try:
        ret = BASE.get_drill_belts(job)
        ret = json.loads(ret)['paras']['result']
        return ret
    except Exception as e:
        print(e)
    return {}

def add_drill_belt(job:str, params:dict)->int:
    try:
        drillLayerName = params['drillLayerName']
        startLayer = params['startLayer']
        endLayer = params['endLayer']
        drillBeltType = params['drillBeltType']
        drillNumber = params['drillNumber']
        _ret = BASE.add_drill_belt(job,drillLayerName,startLayer,endLayer,drillBeltType,drillNumber)
        ret = json.loads(_ret)['paras']['result']
        return ret
    except Exception as e:
        print(e)
    return None

def delete_drill_belt(job:str, index:int)->bool:
    try:
        _ret = BASE.delete_drill_belt(job,index)
        ret = json.loads(_ret)['status']
        if ret == 'true':
            ret = True
        else:
            ret = False
        return ret 
    except Exception as e:
        print(e)
    return False

def update_drill_belt(job:str, index:int, params:dict)->bool:
    try:
        updateDrillBeltPara = params
        _ret = BASE.update_drill_belt(job,index,updateDrillBeltPara)
        ret = json.loads(_ret)['status']
        if ret == 'true':
            ret = True
        else:
            ret = False
        return ret
    except Exception as e:
        print(e)
    return False

def clear_drill_belts(job:str)->bool:
    try:
        _ret = BASE.clear_drill_belts(job)
        ret = json.loads(_ret)['status']
        if ret == 'true':
            ret = True
        else:
            ret = False
        return ret
    except Exception as e:
        print(e)
    return False

def get_linked_cam_layer(job:str, index:int)->dict:
    try:
        ret = BASE.get_linked_cam_layer(job,index)
        ret = json.loads(ret)['paras']['result']
        return ret
    except Exception as e:
        print(e)
    return ' '

def auto_drill_belts(job:str, step:str)->bool:
    try:
        ret = BASE.auto_drill_belts(job,step)
        ret = json.loads(ret)['status']
        if ret == 'true':
            ret = True
        else:
            ret = False
        return ret
    except Exception as e:
        print(e)
    return False

def save_stackup(job:str, stackup:dict)->bool:
    try:
        stackupInfo = stackup
        ret = BASE.save_stackup(job,stackupInfo)
        ret = json.loads(ret)['status']
        if ret == 'true':
            ret = True
        else:
            ret = False
        return ret
    except Exception as e:
        print(e)
    return False

def get_stackup(job:str)->dict:
    try:
        _ret = BASE.get_stackup(job)
        ret = json.loads(_ret)['paras']['result']
        return ret
    except Exception as e:
        print(e)
    return {}

def add_stackup_segment(job:str, params:dict, index:int)->bool:
    try:
        stackupParams = params
        ret = BASE.add_stackup_segment(job,index,stackupParams)
        ret = json.loads(ret)['paras']['result']
        return ret
    except Exception as e:
        print(e)
    return False

def delete_stackup_segment(job:str, index:int)->bool:
    try:
        ret = BASE.delete_stackup_segment(job,index)
        ret = json.loads(ret)['paras']['result']
        return ret
    except Exception as e:
        print(e)
    return False

def update_stackup_segment(job:str, index:int, params:dict)->bool:
    try:
        updateParams = params
        ret = BASE.update_stackup_segment(job,index,updateParams)
        ret = json.loads(ret)['paras']['result']
        return ret
    except Exception as e:
        print(e)
    return False

def clear_stackup(job:str)->bool:
    try:
        _ret = BASE.clear_stackup(job)
        ret = json.loads(_ret)['status']
        if ret == 'true':
            ret = True
        else:
            ret = False
        return ret
    except Exception as e:
        print(e)
    return False































