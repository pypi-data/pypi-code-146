import json
from jbg_util.basic_util import get_instance_from_dict
from jbg_util.input_util import collect_input
import os 
from pathlib import Path
import shutil
from dataclasses import fields


class FileManager:
    @staticmethod        
    def save_obj_to_file(file_path : str, d):
        with open(file_path,'wt',encoding='utf-8') as f:
            f.write(json.dumps(d))
    
    @staticmethod
    def get_obj_from_file(file_path : str):
        with open(file_path,'rt',encoding='utf-8') as f:
            lines=f.read()
            if lines=='':
                return {}
            return json.loads(lines)
            
    @staticmethod
    def get_instance_from_file(file_path : str, cls):
        d = FileManager.get_obj_from_file(file_path)
        return get_instance_from_dict(d,cls)
        
    @staticmethod
    def get_instances_from_file(file_path : str, cls):
        dicts = FileManager.get_obj_from_file(file_path)
        return [get_instance_from_dict(d,cls) for d in dicts]
       
    @staticmethod
    def save_str_to_file(file_path : str, s):
        with open(file_path,'wt',encoding='utf-8') as f:
            return f.write(s)

    @staticmethod
    def get_str_from_file(file_path : str):
        with open(file_path,'rt',encoding='utf-8') as f:
            return f.read()    
            
    @staticmethod
    def delete_all_files_in_folder(folder_path):
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        FileManager.ensure_folder_exists(folder_path)
        
    @staticmethod
    def ensure_folder_exists(folder_path):
        Path(folder_path).mkdir(parents=True, exist_ok=True)
        
    @staticmethod
    def ensure_file_exists(file_path):
        if not os.path.exists(file_path):
            FileManager.save_str_to_file(file_path,'')
        
    @staticmethod
    def collect_and_save_input_for_undefined_fields(file_path : str, cls, is_valid_fxn=None):
        map = FileManager.get_obj_from_file(file_path)
        for field in fields(cls):
            if field.name not in map:
                new_val=collect_input(field, is_valid_fxn)
                map[field.name]=new_val
        FileManager.save_obj_to_file(file_path,map)
        return get_instance_from_dict(map,cls) 
        
    @staticmethod
    def collect_and_save_input(file_path : str, cls = None):
        map = FileManager.get_obj_from_file(file_path)
        new_map={}
        for key,dflt_val in map.items():
            new_val=input(f'{key} (default={dflt_val}): ')
            if new_val=='':
                new_val=dflt_val
            new_map[key]=new_val
        FileManager.save_obj_to_file(file_path,new_map)  
        
        if cls is not None:
            return get_instance_from_dict(new_map,cls)
        return new_map
        
    @staticmethod
    def get_row_count_in_file(file_path : str) -> int:
        with open(file_path,'rt',encoding='utf-8') as f:
            return len(f.readlines())