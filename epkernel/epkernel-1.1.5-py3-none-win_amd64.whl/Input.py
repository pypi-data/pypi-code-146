import os, sys, json
from epkernel import BASE
from epkernel.Action import Information
from epkernel.Edition import Job

#打开料号
def open_job(job:str, path:str):
    try:
       ret= json.loads(BASE.open_job(path, job))['paras']['status']
       return ret   
    except Exception as e:
        print(e)
        return False

def open_eps(job:str, path:str):
    try:
        open_jobs = Information.get_opened_jobs()
        if job in open_jobs: #存在
            return False
        else:
            ret = BASE.open_eps(job, path)
            ret_= json.loads(ret)
            if 'result' in ret_:
                if ret_['result']: #True
                    return ret_['result']
                else:
                    data= Information.get_opened_jobs()
                    if job in data:
                        Job.delete_job(job)
                        return False
                    else:
                        return False
    except Exception as e:
        print(e)
    return False

def file_identify(path:str)->dict:
    try:
        ret = BASE.file_identify(path)
        data = json.loads(ret)
        if 'paras' in data:
            return data['paras']
        return None
    except Exception as e:
        return None

def file_translate(path:str, job:str, step:str, layer:str, param:dict)->bool:
    try:
        file_format = param['format']
        if file_format == 'Gerber274x' or file_format == 'Excellon2' or file_format == 'DXF':
            ret = BASE.file_translate(path, job, step, layer, param, '', '', '', [])    
            data = json.loads(ret)
            if 'paras' in data:
                if 'result' in data['paras']:
                    return data['paras']['result']
    except Exception as e:
        return False
    return False