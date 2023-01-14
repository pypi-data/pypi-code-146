from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource
from genesys.app.config import (SVN_PARENT_PATH,
                                SVN_PARENT_URL,
                                LOGIN_NAME)
from genesys.app.blueprints.task.utils import create_task_file
from genesys.app.blueprints.project.routes import create_project
from genesys.app.services import svn_service, queue_store
from genesys.app.utils import config_helpers
import os
from configparser import ConfigParser
from genesys.app import config

refresh = Blueprint('refresh', __name__)
api = Api(refresh)

def refresh_project_files(data, project_name):
    project = (data['project'])
    root = os.path.join(project['file_tree']['working']['mountpoint'], project['file_tree']['working']['root'],'')
    # replacing file tree mount point with genesys config mount point
    base_file_directory = data['base_file_directory'].split(root,1)[1]
    project_repo_url = os.path.join(SVN_PARENT_URL, project_name)
    if not svn_service.is_svn_url(project_repo_url):
        create_project(project_name)
    create_task_file(project_name=project_name,
                    base_file_directory=base_file_directory,
                    base_svn_directory=data['base_svn_directory'])


def refresh_svn_acl(data, acl_parser):
    base_svn_directory = data['base_svn_directory']
    file_name = os.path.basename(base_svn_directory).rsplit('.', 1)[0]
    base_map_svn_directory = os.path.join(os.path.dirname(base_svn_directory), 'maps', file_name)
    permission = data['permission']

    all_users = list()
    for person in data['persons']:
        if person[LOGIN_NAME] != '':
            all_users.append(person[LOGIN_NAME])
    if all_users:
        for user in all_users:
            svn_service.svn_update_acl(
                base_svn_directory=base_svn_directory,
                acl_parser=acl_parser,
                person=user,
                permission=permission
            )
            svn_service.svn_update_acl(
                base_svn_directory=base_map_svn_directory,
                acl_parser=acl_parser,
                person=user,
                permission=permission
            )
            if data['permission'] == 'rw':
                for dependency in data['dependencies']:
                    dependency_file_name = os.path.basename(dependency).rsplit('.', 1)[0]
                    dependency_base_map_svn_directory = os.path.join(os.path.dirname(dependency), 'maps', dependency_file_name)
                    svn_service.svn_update_acl(
                        base_svn_directory=dependency,
                        acl_parser=acl_parser,
                        person=user,
                        permission='r'
                    )
                    svn_service.svn_update_acl(
                        base_svn_directory=dependency_base_map_svn_directory,
                        acl_parser=acl_parser,
                        person=user,
                        permission='r'
                    )
    else:
        if base_svn_directory not in acl_parser:
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

def refresh_project_data(all_data, project_name):
    new_acl_parser = ConfigParser()
    svn_authz_path = os.path.join(SVN_PARENT_PATH, project_name, 'conf/authz')
    new_acl_parser['groups'] = {
                'admin':'super-user',
                'super_reader':'super-reader',
                'maps':'',
                'edit':'',
            }
    new_acl_parser['/'] = {
                '*':'r',
                '@admin':'rw',
                '@super_reader':'r',
            }
    for data in all_data:
        refresh_project_files(data, project_name)
    for data in all_data:
        refresh_svn_acl(data, new_acl_parser)

    config_helpers.write_config(svn_authz_path, new_acl_parser)




class All_Task_File_Access_Control(Resource):
    def post(self, project_name):
        data = request.get_json()
        if config.ENABLE_JOB_QUEUE:
            queue_store.job_queue.enqueue(
                refresh_project_data,
                args=(data, project_name),
                job_timeout=10,
            )
            return {"job": "running"}
        else:
            refresh_project_data(data, project_name)
            project_repo_url = os.path.join(SVN_PARENT_URL, project_name)
            return jsonify(message=f'project created', project_name=project_name, svn_url=project_repo_url)

api.add_resource(All_Task_File_Access_Control, '/refresh/<string:project_name>')