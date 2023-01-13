import os, sys, json
from epkernel import epcam, BASE
from epkernel.Action import Information,Selection

def save_eps(job:str, path:str):
    try:
        filename = os.path.basename(path)
        suffix = os.path.splitext(filename)[1]
        if suffix == '.eps':
            BASE.setJobParameter(job,job)
            BASE.save_eps(job,path)
            return True
        else:
            pass
    except Exception as e:
        print(e)
    return False

def save_gerber( job:str, step:str, layer:str, filename:str,  resize:int, angle:float, scalingX:float, scalingY:float, mirror:bool, rotate:bool, scale:bool, cw:bool,  mirrorpointX:int, mirrorpointY:int, rotatepointX:int, rotatepointY:int, scalepointX:int, scalepointY:int, mirrorX:bool, mirrorY:bool, numberFormatL=2, numberFormatR=6, zeros=2, unit=0):
    try:
        _type = 0
        gdsdbu = 0.01
        profiletop = False
        cutprofile = True
        isReverse = False
        cut_polygon = []
        if mirrorX == True and mirrorY ==True:
            mirrordirection = 'XY'
        elif mirrorX==True and mirrorY ==False:
            mirrordirection = 'Y'
        elif mirrorX==False and mirrorY ==True:
            mirrordirection = 'X'
        else:
            mirrordirection = 'NO'
        _ret = BASE.layer_export(job, step, layer, _type, filename, gdsdbu, resize, angle, scalingX, scalingY, isReverse,
                    mirror, rotate, scale, profiletop, cw, cutprofile, mirrorpointX, mirrorpointY, rotatepointX,
                    rotatepointY, scalepointX, scalepointY, mirrordirection, cut_polygon,numberFormatL,numberFormatR,
                    zeros,unit)
        ret = json.loads(_ret)['status']
        if ret == 'true':
            ret = True
        else:
            ret = False
        return ret
    except Exception as e:
        print(e)
    return False

def save_drill(job:str, step:str, layer:str, path:str, isMetric:bool, number_format_l=2, number_format_r=6, zeroes=2, unit=0, tool_unit=1, x_scale=1, y_scale=1, x_anchor=0, y_anchor=0):
    try:
        layer_info = Information.get_layer_information(job)
        for i in range(0,len(layer_info)):
            if layer_info[i]['name']==layer and layer_info[i]['context'] == 'board' and layer_info[i]['type'] =='drill':
                BASE.drill2file(job, step, layer,path,isMetric,number_format_l,number_format_r,
                    zeroes,unit,tool_unit,x_scale,y_scale,x_anchor,y_anchor, manufacator = '', tools_order = [])
                return True
    except Exception as e:
        print(e)
    return False

def save_rout(job:str, step:str, layer:str, path:str, number_format_l=2,number_format_r=6,zeroes=2,unit=0,tool_unit=1,x_scale=1,y_scale=1,x_anchor=0,y_anchor=0, break_arcs = False):
    try:
        layer_info = Information.get_layer_information(job)
        for i in range(0,len(layer_info)):
            if layer_info[i]['name'] == layer and layer_info[i]['context'] == 'board' and layer_info[i]['type'] == 'rout':
                repeat = BASE.get_all_step_repeat_steps(job,step)
                data = json.loads(repeat)
                step_repeat = []
                if  not data['steps'] == None:
                    for _step in data['steps']:
                        step_repeat.append(_step)
                step_repeat.append(step)
                can_back = True
                for j in range(0,len(step_repeat)):
                    _step = step_repeat[j]
                    Selection.reverse_select(job, _step, layer)
                    ret = Information.get_selected_features_infos(job,_step,layer)
                    if ret == None:
                        can_back=False
                        return False
                    Selection.clear_select(job, _step, layer)
                    if len(ret) == 0:
                        can_back=False
                        return False
                    for k in range(0,len(ret)):
                        attribute = ret[k]['attributes']
                        has_chain = False
                        for m in range(0,len(attribute)):
                            if  '.rout_chain' in attribute[m]:
                                has_chain = True
                        if  has_chain == False:
                                can_back=False
                                return False
                if can_back==True:
                    BASE.rout2file(job, step, layer,path,number_format_l,number_format_r,zeroes,unit,tool_unit,x_scale,y_scale,x_anchor,y_anchor, 0, 0, 0, 0, 0, break_arcs)
                return True
    except Exception as e:
        print(e)
    return False

def save_job(job:str,path:str)->bool:
    try:
        layers = Information.get_layers(job)
        steps = Information.get_steps(job)
        for step in steps:
            for layer in layers:
                BASE.load_layer(job,step,layer)
        BASE.save_job_as(job,path)
        return True
    except Exception as e:
        print(e)
    return False

def save_dxf(job:str,step:str,layers:list,savePath:str):
    try:
        _ret = BASE.dxf2file(job,step,layers,savePath)
        ret = json.loads(_ret)['paras']['result']
        return ret
    except Exception as e:
        print(e)
    return False

def save_pdf(job:str, step:str, layers:list, layercolors:list, outputpath:str, overlap:bool)->bool:
    try:
        (outputpath,pdfname) = os.path.split(outputpath)
        layer_sum = len(layers)
        colors_sum = len(layercolors)
        b = True
        if layer_sum != colors_sum:
            b = False
        else:
            for i in range(0,colors_sum):
                color = layercolors[i]
                if len(color) !=4:
                    b = False
                    break
        if b == True:
            _ret = BASE.output_pdf(job,step,layers,layercolors,outputpath,pdfname,overlap)
            ret = json.loads(_ret)['status']
            if ret == 'true':
                ret = True
            else:
                ret = False
            return ret
    except Exception as e:
        print(e)
    return False

def save_gds(job:str, step:str, layer:str, filename:str, gdsdbu:float):
    try:
        _type = 1
        resize = 0
        angle = 0
        scalingX = 1
        scalingY = 1
        isReverse = False
        mirror = False
        rotate = False
        scale = False
        profiletop =False
        cw = False
        cutprofile =   True
        mirrorpointX = 0
        mirrorpointY = 0
        rotatepointX = 0
        rotatepointY = 0
        scalepointX = 0
        scalepointY = 0
        mirrordirection = 'X'
        cut_polygon = []
        numberFormatL = 2
        numberFormatR = 6
        zeros = 0
        unit = 0
        _ret = BASE.layer_export(job, step, layer, _type, filename, gdsdbu, resize, angle, scalingX, scalingY, isReverse,
                    mirror, rotate, scale, profiletop, cw, cutprofile, mirrorpointX, mirrorpointY, rotatepointX,
                    rotatepointY, scalepointX, scalepointY, mirrordirection, cut_polygon,numberFormatL,numberFormatR,
                    zeros,unit)
        ret = json.loads(_ret)['status']
        if ret == 'true':
            ret = True
        else:
            ret = False
        return ret
    except Exception as e:
        print(e)
    return False


