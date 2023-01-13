import os, sys, json
from epkernel import BASE
import math

from epkernel.Action import Selection, Information

def delete_feature(job:str, step:str, layers:list):
    try:
        BASE.sel_delete(job, step, layers)
    except Exception as e:
        print(e)
    return 0

def break_features(job:str, step:str, layers:list, type:int):
    try:
        BASE.sel_break(job, step, layers, type)
    except Exception as e:
            print(e)
    return 0

def add_line(job:str, step:str, layers:list, symbol:str, start_x:int, start_y:int, end_x:int, end_y:int, polarity:bool, attributes:list)->None:
    try:
        layer = ''
        if len(layers) > 0:
            layer = layers[0]
        if polarity==True:
            polarity=1
        else:
            polarity=0
        BASE.add_line(job, step, layers, layer, symbol, start_x, start_y, end_x, end_y, polarity, 0, attributes)
    except Exception as e:
        print(e)
    return 0

def hierarchy_edit(job:str, step:str, layers:list, mode:int):
    try:
        BASE.sel_index(job, step, layers, mode)
    except Exception as e:
        print(e)
    return 0

def add_surface(job:str, step:str, layers:list, polarity:bool, attributes:list, points_location:list)->None:
    try:
        layer = ''
        if len(layers)> 0:
            layer = layers[0]
        if polarity==True:
            polarity=1
        else:
            polarity=0
        BASE.add_surface(job, step, layers, layer, polarity, 0, False, attributes, points_location)
    except Exception as e:
        print(e)
    return ''

def add_round_surface(job:str, step:str, layers:list, polarity:bool, attributes:list,center_x:int,center_y:int,radius:int)->None:
    try:
        layer = ''
        if len(layers)> 0:
            layer = layers[0]
        if polarity==True:
            polarity=1
        else:
            polarity=0
        point2_x = center_x + radius
        point2_y = center_y
        points_location = [[point2_x, point2_y],[center_x, center_y]]
        BASE.add_surface(job, step, layers, layer, polarity, 0, True, attributes, points_location)
    except Exception as e:
        print(e)
    return '' 

def contour2pad(job:str, step:str, layers:list, tol:float, minsize:float, maxsize:float, suffix:str):
    try:
        BASE.contour2pad(job, step, layers, tol, minsize, maxsize, suffix)
    except Exception as e:
        print(e)
    return ''

def resize_polyline(job:str, step:str, layers:list, size:float, sel_type:bool):
    try:
        BASE.resize_polyline(job, step, layers, size, sel_type)
    except Exception as e:
        print(e)
    return ''

def contourize(job:str, step:str, layers:list, accuracy:int, separate_to_islands:bool, size:int, mode:int):
    try:
        BASE.contourize(job, step, layers, accuracy, separate_to_islands, size, mode)
    except Exception as e:
        print(e)
    return ''

def add_pad(job:str, step:str, layers:list, symbol:str, location_x:int, location_y:int, polarity:bool, orient:int, attributes:list,special_angle=0)->None:
    try:
        layer=''
        if len(layers)>0:
            layer=layers[0]
        if polarity==True:
            polarity=1
        else:
            polarity=0
        BASE.add_pad(job, step, layers, layer, symbol, location_x, location_y, polarity, 0, orient,attributes,special_angle)
    except Exception as e:
        print(e)
    return ''

def change_feature_symbols(job:str, step:str, layers:list, symbol:str,pad_angle = False):
    try:
        BASE.change_feature_symbols(job, step, layers, symbol, pad_angle)
    except Exception as e:
        print(e)
    return 0

def create_profile(job:str, step:str, layer:str):
    try:
        BASE.create_profile(job, step, layer)
    except Exception as e:
        print(e)
    return 0
    
def step_repeat(job:str, parent_step:str, child_steps:list):
    """
    #拼板
    :param     parentstep: panel
    :param     childsteps: 拼入panel的step
    :returns    :
    :raise error:
    """
    try:
        BASE.step_repeat(job, parent_step, child_steps)
    except Exception as e:
        print(e)
    return 0

def surface_repair(job:str, step:str, layers:list, scope:int, radius:int, remove_type:int, is_round:bool):
    try:
        ret= Information.check_matrix_info(job,step,layers)
        if ret==True:
            BASE.remove_sharp_angle(job, step, layers, scope, radius, remove_type, is_round)
    except Exception as e:
        print(e)
    return 


def line2pad(job:str, step:str, layers:list):
    try:
        ret= Information.check_matrix_info(job,step,layers)
        if ret==True:
            BASE.line2pad_new(job, step, layers)
    except Exception as e:
        print(e)
    return 

def surface2outline(job:str, step:str, layers:list, width:float):
    try:
        ret= Information.check_matrix_info(job,step,layers)
        if ret==True:
            BASE.surface2outline(job, step, layers, width)
    except Exception as e:
        print(e)
    return 

def modify_attributes(job:str, step:str, layers:list, mode:int, attributes:list):
    try:
        BASE.modify_attributes(job, step, layers, mode, attributes)
    except Exception as e:
        print(e)
    return 

def add_arc(job:str, step:str, layers:list, symbol:str, start_x:int, start_y:int, end_x:int, end_y:int, center_x:int, center_y:int,cw:bool,polarity:int, attributes:list)->None:
    try:
        layer=''
        if len(layers)>0:
            layer=layers[0]
        if polarity==True:
            polarity=1
        else:
            polarity=0
        dcode = 0
        BASE.add_arc(job, step, layers, layer, symbol, start_x, start_y, end_x, end_y, center_x, center_y,cw,polarity, dcode, attributes)
    except Exception as e:
        print(e)
    return None

def layer_compare(job1:str, step1:str, layer1:str, job2:str, step2:str, layer2:str, tol:int, isGlobal:bool, consider_SR:bool, comparison_map_layername:str, map_layer_resolution:int)->None:
    try:
        BASE.layer_compare(job1, step1, layer1, job2, step2, layer2, tol, isGlobal, consider_SR, comparison_map_layername, map_layer_resolution)
    except Exception as e:
        print(e)
    return None

#将指定层中选中的feature拷贝至目标层，若无选中feature则将指定层资料整层拷贝
def copy_other(src_job:str, src_step:str, src_layer:str, dst_layer:str, invert:bool, offset_x:int, offset_y:int, mirror:int, resize:float, rotation:float, x_anchor:float, y_anchor:float):
    try:
        BASE.sel_copy_other(src_job, src_step, [src_layer], [dst_layer], invert, offset_x, offset_y, 
                    mirror, resize, rotation, x_anchor, y_anchor)
    except Exception as e:
        print(e)
    return None

#将指定料号的step下的指定层的所有feature信息拷贝至目标料号的step下的对应层中
def copy_features2dstjob(src_job:str, src_step:str, src_layer:str, dst_job:str, dst_step:str, dst_layer:str, mode:bool, invert:bool)->None:
    try:
        BASE.copy_layer_features(src_job, src_step, [src_layer], dst_job, dst_step, [dst_layer], mode, invert)
    except Exception as e:
        print(e)
    return ''

#将指定料号指定层中选中的feature移动至目标料号下的目标层中，
def move2other_layer(src_job:str, src_step:str, src_layers:list, dst_job:str, dst_step:str, dst_layer:str, invert:bool, offset_x:int, offset_y:int, mirror:int, resize:float, rotation:float, x_anchor:float, y_anchor:float)->None:
    try:
        BASE.sel_move_other(src_job, src_step, src_layers, dst_job, dst_step, dst_layer, invert, offset_x, offset_y, 
                    mirror, resize, rotation, x_anchor, y_anchor)
    except Exception as e:
        print(e)
    return ''

def change_text(job:str, step:str, layers:list, text:str, font:str, x_size:int, y_size:int, width:int, polarity:bool, mirror:int,angle=0)->None:
    try:
        if polarity==True:
            polarity=1
        else:
            polarity=-1
        BASE.change_text(job, step, layers, text, font, x_size, y_size, width, polarity, mirror,angle)
    except Exception as e:
        print(e)
    return 0

def add_text(job:str, step:str, layers:list, symbol:str, fontname:str, text:str, xsize:int, ysize:int, linewidth:int, location_x:int, location_y:int,polarity:bool,orient:int,  attributes:list,special_angle=0)->None:
    try:
        layer = ''
        if len(layers)>0:
            layer = layers[0]
        if polarity == True:
            polarity = 1
        else:
            polarity = 0
        BASE.add_text(job, step, layer, symbol, fontname, text, xsize, ysize, linewidth, location_x, location_y, polarity,orient, 0, layers, attributes,special_angle)
    except Exception as e:
        print(e)
    return ''     

def change_polarity(job:str,step:str,layers:list,polarity:int,type:int)->bool:
    try:
        sel_type = type
        _ret = BASE.sel_polarity(job, step, layers, polarity, sel_type)
        ret = json.loads(_ret)['status']
        if ret == 'true':
            ret = True
        else:
            ret = False
        return ret
    except Exception as e:
        print(e)
        return False


def fill_profile(job:str,step:str,layer:str,profile_resize:int,child_profile_resize:int,avoid_drill_size:int,fill_by_pattern:bool,symbolname:str,dx:int,dy:int,avoid_drill=True)->bool:
    try:
        _ret = BASE.fill_profile(job,step,layer,profile_resize,child_profile_resize,avoid_drill_size,fill_by_pattern,symbolname,dx,dy,avoid_drill)
        ret = json.loads(_ret)['result']
        return ret
    except Exception as e:
        print(e)
        return False        
        
def use_line_fill_contours(job:str,step:str,layer:str,dx:int,dy:int,linewidth:int,x_offset:int,y_offset:int,angle:int):
    try:
        BASE.fill_select_feature_by_grid(job,step,layer,dx,dy,linewidth,x_offset,y_offset,angle)
    except Exception as e:
        print(e)
    return None


def move2same_layer(job:str, step:str, layers:list, offset_x:int, offset_y:int):
    try:
        jobname = job
        stepname = step
        layernames = layers
        BASE.move_same_layer(jobname, stepname, layernames, offset_x, offset_y)
    except Exception as e:
        print(e)
    return None
    
def resize_global(job:str, step:str, layers:list, type:int, size:int):
    try:
        sel_type = type
        BASE.resize_global(job, step, layers, sel_type, size)
    except Exception as e:
        print(e)
    return None

def clip_area_use_reference(job:str, step:str, layers:list, reference_layer:str, margin:float, clipcontour:bool, text:bool,surface:bool,arc:bool,line:bool,pad:bool):
    try:
        jobname = job
        stepname = step
        work_layers = layers
        positive = True
        negative = True
        featuretype_sum = 0
        featuretype_list= [positive,negative,text,surface,arc,line,pad]
        for index in range(len(featuretype_list)):
            if featuretype_list[index]==True:
                featuretype_list[index]=len(featuretype_list)-index-1
            else:
                featuretype_list[index]=None
        for type_ in featuretype_list:
            if type_!=None:
                featuretype_sum += math.pow(2,type_)
        BASE.clip_area_use_reference(jobname, stepname, work_layers, reference_layer, margin, clipcontour, featuretype_sum)
    except Exception as e:
        print(e)
    return None

def clip_area_use_manual(job:str, step:str, layers:list, points:list, margin:float,  clipcontour:bool, clipinside:bool, text:bool, surface:bool, arc:bool, line:bool, pad:bool):
    try:
        jobname = job
        stepname = step
        positive = True
        negative = True
        featuretype_sum = 0
        featuretype_list= [positive,negative,text,surface,arc,line,pad]
        for index in range(len(featuretype_list)):
            if featuretype_list[index]==True:
                featuretype_list[index]=len(featuretype_list)-index-1
            else:
                featuretype_list[index]=None
        for type_ in featuretype_list:
            if type_!=None:
                featuretype_sum += math.pow(2,type_)
        for i in layers:
            layer = i
            BASE.load_layer(job,step,layer)
            BASE.clip_area_use_manual(jobname, stepname, layers, points, margin, clipcontour,clipinside, featuretype_sum)
    except Exception as e:
        print(e)
    return None

def transform_features(job:str,step:str,layer:str,mode:int,rotate:bool,scale:bool,mirror_X:bool,mirror_Y:bool,duplicate:bool,datumPoint:dict,angle:float,xscale:float,yscale:float,xoffset:int,yoffset:int):
    try:
        jobname = job
        stepname = step
        layername = layer
        BASE.transform(jobname,stepname,layername,mode,rotate,scale,mirror_X,mirror_Y,duplicate,datumPoint,angle,xscale,yscale,xoffset,yoffset)
    except Exception as e:
        print(e)
    return None

def rounding_line_corner(job:str, step:str, layers:list, radius:int):
    try:
        BASE.rounding_line_corner(job,step,layers,radius)
    except Exception as e:
        print(e)
    return 

def use_pattern_fill_contours(job:str,step:str,layer:str,symbolname:str,dx:float,dy:float,break_partial:bool,cut_primitive:bool,origin_point:bool,outline:bool,outlinewidth = 0,outline_invert = False,odd_offset = 0,even_offset = 0):
    try:
        BASE.use_pattern_fill_contours(job,step,layer,symbolname,dx,dy,break_partial,cut_primitive,origin_point,outline,outlinewidth,outline_invert,odd_offset = 0,even_offset = 0)
    except Exception as e:
        print(e)
    return 

def clip_area_use_profile(job:str, step:str, layers:list,  clipinside:bool, clipcontour:bool, margin:float, text:bool, surface:bool, arc:bool, line:bool, pad:bool):
    try:
        positive = True
        negative = True
        featuretype_sum = 0
        featuretype_list= [positive,negative,text,surface,arc,line,pad]
        for index in range(len(featuretype_list)):
            if featuretype_list[index]==True:
                featuretype_list[index]=len(featuretype_list)-index-1
            else:
                featuretype_list[index]=None
        for type_ in featuretype_list:
            if type_!=None:
                featuretype_sum += math.pow(2,type_)
        for i in layers:
            layer = i
            BASE.load_layer(job,step,layer)
            BASE.clip_area_use_profile(job, step, layers, clipinside, clipcontour, margin, featuretype_sum)
    except Exception as e:
        print(e)
    return None

def layer_compare_point(job1:str, step1:str, layer1:str, job2:str, step2:str, layer2:str, tol = 22860,isGlobal = True,consider_SR = True, map_layer_resolution = 5080000)->list:
    try:
        point = BASE.layer_compare_point(job1, step1, layer1, job2, step2, layer2, tolerance = 22860, mode = True, consider_SR = True, map_layer_resolution = 5080000)
        points = json.loads(point)['result']
        return points
    except Exception as e:
        print(e)
    return [] 
    
def flatten_step(job:str, step:str ,flatten_layer:str, dst_layer:str)->bool:
    try:
        layers = Information.get_layers(job)
        ret = BASE.get_all_step_repeat_steps(job,step)
        steps = json.loads(ret)['steps']
        if steps != None:
            for i in range(0,len(layers)):
                for j in range(0,len(layers)):
                    if layers[i] == dst_layer and layers[j] == flatten_layer:
                        _ret = BASE.flatten_step(job,step,flatten_layer,dst_layer)
                        ret = json.loads(_ret)['status']
                        if ret =='true':
                            ret = True
                        else:
                            ret = False
                        return ret
        else:
            pass
    except Exception as e:
        print(e)
    return False

def profile_to_outline(job:str, step:str, layers:list, linewidth:int):
    try:
        BASE.profile_to_outerline(job,step,layers,linewidth)
    except Exception as e:
        print(e)
    return None

def arc2lines(job:str, step:str, layers:list, radius:float, sel_type:bool):
    try:
        if sel_type == True:
            sel_type = 0
        else:
            sel_type = 1
        BASE.arc2lines(job,step,layers,radius,sel_type)
    except Exception as e:
        print(e)
    return None







