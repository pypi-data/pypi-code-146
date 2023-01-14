import os
from genesys.app.services import svn_service
from genesys.app.config import SVN_PARENT_PATH, SVN_PARENT_URL, TEMPLATE_FILES_DIR
from genesys.app.utils import config_helpers
from configparser import ConfigParser
from genesys.app.config import (SVN_PARENT_PATH,
                                SVN_PARENT_URL,
                                LOGIN_NAME)
import bpy

def create_task_file(project_name, base_file_directory, base_svn_directory):
    "creates file tasks"
    acl_parser = ConfigParser()
    svn_authz_path = os.path.join(SVN_PARENT_PATH, project_name.replace(' ', '_').lower(), 'conf/authz')
    blend_file_url = os.path.join(SVN_PARENT_URL, base_file_directory)

    config_helpers.load_config(svn_authz_path, acl_parser)

    file_folder_url = os.path.dirname(blend_file_url)
    file_name = os.path.basename(base_file_directory).rsplit('.', 1)[0]
    file_map_folder_url = os.path.join(file_folder_url, 'maps', file_name)
    base_map_svn_directory = os.path.join(os.path.dirname(base_svn_directory), 'maps', file_name)

    if not svn_service.is_svn_url(file_folder_url):
        svn_service.svn_make_dirs(file_folder_url, log_message=f'created {file_folder_url}')
    if not svn_service.is_svn_url(file_map_folder_url):
        svn_service.svn_make_dirs(file_map_folder_url, log_message=f'created {file_map_folder_url}')
    if not svn_service.is_svn_url(blend_file_url):
        collection = bpy.data.collections.new(file_name)
        bpy.context.scene.collection.children.link(collection)
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(TEMPLATE_FILES_DIR,'blender.blend'))
        svn_service.svn_import(path=os.path.join(TEMPLATE_FILES_DIR,'blender.blend'),
                                    repo_url=blend_file_url,
                                    log_message=f'created {blend_file_url}')
                                   
    create_new_task_acl(base_svn_directory=base_svn_directory, base_map_svn_directory=base_map_svn_directory, acl_parser=acl_parser)
    config_helpers.write_config(svn_authz_path, acl_parser)

def create_new_task_acl(base_svn_directory:str, base_map_svn_directory:str, acl_parser):
    "create svn access entry for task file and set all users to no acces"
    if base_svn_directory in acl_parser:
        pass
    else:
        acl_parser[base_svn_directory] = {
            '@admin':'rw',
            '@super_reader':'r',
            '*':''
        }
        acl_parser[base_map_svn_directory] = {
            '@admin':'rw',
            '@super_reader':'r',
            '*':''
        }

def delete_task_file(project_name, base_file_directory):
    #FIXME  remove acl
    blend_file_url = os.path.join(SVN_PARENT_URL, base_file_directory)
    if svn_service.is_svn_url(blend_file_url):
        svn_service.svn_delete(blend_file_url, log_message=f'created {blend_file_url}')