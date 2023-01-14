from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource
from genesys.app.config import (SVN_PARENT_PATH,
                                SVN_PARENT_URL,
                                LOGIN_NAME)
from genesys.app.blueprints.task.utils import create_task_file, delete_task_file
from genesys.app.services import svn_service, queue_store
from genesys.app.utils import config_helpers
import os
from configparser import ConfigParser, NoSectionError, NoOptionError
from genesys.app import config

task = Blueprint('task', __name__)
api = Api(task)

def update_svn_acl(data, project_name):
    if data['person'][LOGIN_NAME] != '':
        acl_parser = ConfigParser()
        svn_authz_path = os.path.join(SVN_PARENT_PATH, project_name.replace(' ', '_').lower(), 'conf/authz')
        file_name = os.path.basename(data['base_svn_directory']).rsplit('.', 1)[0]
        base_map_svn_directory = os.path.join(os.path.dirname(data['base_svn_directory']), 'maps', file_name)
        config_helpers.load_config(svn_authz_path, acl_parser)
        svn_service.svn_update_acl(
            base_svn_directory=data['base_svn_directory'],
            acl_parser=acl_parser,
            person=data['person'][LOGIN_NAME],
            permission=data['permission']
        )
        #set permission for maps folders
        splited_file_map_folder_url = data['base_svn_directory'].split(':', 1)
        base_file_directory = f"{splited_file_map_folder_url[0]}{splited_file_map_folder_url[1]}"
        blend_file_url = os.path.join(SVN_PARENT_URL, base_file_directory)
        file_folder_url = os.path.dirname(blend_file_url)
        file_name = os.path.basename(base_file_directory).rsplit('.', 1)[0]
        file_map_folder_url = os.path.join(file_folder_url, 'maps', file_name)

        try:
            if not svn_service.is_svn_url(file_map_folder_url):
                svn_service.svn_make_dirs(file_map_folder_url, log_message=f'created {file_map_folder_url}')
            svn_service.svn_update_acl(
                base_svn_directory=base_map_svn_directory,
                acl_parser=acl_parser,
                person=data['person'][LOGIN_NAME],
                permission=data['permission']
            )
        except NoSectionError:
            if not svn_service.is_svn_url(file_map_folder_url):
                svn_service.svn_make_dirs(file_map_folder_url, log_message=f'created {file_map_folder_url}')
            acl_parser[base_map_svn_directory] = {
                '@admin':'rw',
                '@super_reader':'r',
                '*':''
            }
        except NoOptionError:
            if not svn_service.is_svn_url(file_map_folder_url):
                svn_service.svn_make_dirs(file_map_folder_url, log_message=f'created {file_map_folder_url}')
            
        if data['permission'] == 'rw':
            for i in data['dependencies']:
                dependency_file_name = os.path.basename(i).rsplit('.', 1)[0]
                dependency_base_map_svn_directory = os.path.join(os.path.dirname(i), 'maps', dependency_file_name)
                svn_service.svn_update_acl(
                    base_svn_directory=i,
                    acl_parser=acl_parser,
                    person=data['person'][LOGIN_NAME],
                    permission='r'
                )

                splited_dependency_file_map_folder_url = i.split(':', 1)
                dependency_base_file_directory = f"{splited_dependency_file_map_folder_url[0]}{splited_dependency_file_map_folder_url[1]}"
                dependency_blend_file_url = os.path.join(SVN_PARENT_URL, base_file_directory)
                dependency_file_folder_url = os.path.dirname(dependency_blend_file_url)
                dependency_file_name = os.path.basename(dependency_base_file_directory).rsplit('.', 1)[0]
                dependency_file_map_folder_url = os.path.join(dependency_file_folder_url, 'maps', file_name)
                try:
                    if not svn_service.is_svn_url(dependency_file_map_folder_url):
                        svn_service.svn_make_dirs(dependency_file_map_folder_url, log_message=f'created {dependency_file_map_folder_url}')
                    svn_service.svn_update_acl(
                        base_svn_directory=dependency_base_map_svn_directory,
                        acl_parser=acl_parser,
                        person=data['person'][LOGIN_NAME],
                        permission='r'
                    )
                except NoSectionError:
                    if not svn_service.is_svn_url(dependency_file_map_folder_url):
                        svn_service.svn_make_dirs(dependency_file_map_folder_url, log_message=f'created {dependency_file_map_folder_url}')
                    acl_parser[dependency_base_map_svn_directory] = {
                        '@admin':'rw',
                        '@super_reader':'r',
                        '*':''
                    }
                except NoOptionError:
                    if not svn_service.is_svn_url(dependency_file_map_folder_url):
                        svn_service.svn_make_dirs(dependency_file_map_folder_url, log_message=f'created {dependency_file_map_folder_url}')


                
        elif data['permission'] == 'none':
            for i in data['dependencies']:
                dependency_file_name = os.path.basename(i).rsplit('.', 1)[0]
                dependency_base_map_svn_directory = os.path.join(os.path.dirname(i), 'maps', dependency_file_name)
                svn_service.svn_update_acl(
                    base_svn_directory=i,
                    acl_parser=acl_parser,
                    person=data['person'][LOGIN_NAME],
                    permission='d'
                )

                splited_dependency_file_map_folder_url = i.split(':', 1)
                dependency_base_file_directory = f"{splited_dependency_file_map_folder_url[0]}{splited_dependency_file_map_folder_url[1]}"
                dependency_blend_file_url = os.path.join(SVN_PARENT_URL, base_file_directory)
                dependency_file_folder_url = os.path.dirname(dependency_blend_file_url)
                dependency_file_name = os.path.basename(dependency_base_file_directory).rsplit('.', 1)[0]
                dependency_file_map_folder_url = os.path.join(dependency_file_folder_url, 'maps', file_name)
                try:
                    if not svn_service.is_svn_url(dependency_file_map_folder_url):
                        svn_service.svn_make_dirs(dependency_file_map_folder_url, log_message=f'created {dependency_file_map_folder_url}')
                    svn_service.svn_update_acl(
                        base_svn_directory=dependency_base_map_svn_directory,
                        acl_parser=acl_parser,
                        person=data['person'][LOGIN_NAME],
                        permission='d'
                    )
                except NoSectionError:
                    if not svn_service.is_svn_url(dependency_file_map_folder_url):
                        svn_service.svn_make_dirs(dependency_file_map_folder_url, log_message=f'created {dependency_file_map_folder_url}')
                    acl_parser[dependency_base_map_svn_directory] = {
                        '@admin':'rw',
                        '@super_reader':'r',
                        '*':''
                    }
                except NoOptionError:
                    if not svn_service.is_svn_url(dependency_file_map_folder_url):
                        svn_service.svn_make_dirs(dependency_file_map_folder_url, log_message=f'created {dependency_file_map_folder_url}')
        config_helpers.write_config(svn_authz_path, acl_parser)


class Task(Resource):
    def post(self, project_name):
        data = request.get_json()
        project_repo_url = os.path.join(SVN_PARENT_URL, project_name)
        project = (data['project'])
        root = os.path.join(project['file_tree']['working']['mountpoint'], project['file_tree']['working']['root'],'')
        # replacing file tree mount point with genesys config mount point
        base_file_directory = data['base_file_directory'].split(root,1)[1]
        if config.ENABLE_JOB_QUEUE:
            queue_store.job_queue.enqueue(
                create_task_file,
                args=(project_name, base_file_directory, data['base_svn_directory']),
                job_timeout=10,
            )
            return {"job": "running"}
        else:
            create_task_file(project_name=project_name,
                                base_file_directory=base_file_directory,
                                base_svn_directory=data['base_svn_directory'],
                                all_persons=data['all_persons'])
            return jsonify(message=f'task created')

    def delete(self, project_name):
        data = request.get_json()
        project_repo_url = os.path.join(SVN_PARENT_URL, project_name)
        project = (data['project'])
        root = os.path.join(project['file_tree']['working']['mountpoint'], project['file_tree']['working']['root'],'')
        # replacing file tree mount point with genesys config mount point
        base_file_directory = data['base_file_directory'].split(root,1)[1]
        if config.ENABLE_JOB_QUEUE:
            queue_store.job_queue.enqueue(
                delete_task_file,
                args=(project_name, base_file_directory),
                job_timeout=10,
            )
            return {"job": "running"}
        else:
            delete_task_file(project_name, base_file_directory, task_type=data['task_type'])
            return jsonify(message=f'task deleted')


class Task_File_Access_Control(Resource):
    def put(self, project_name):
        data = request.get_json()
        if config.ENABLE_JOB_QUEUE:
            queue_store.job_queue.enqueue(
                update_svn_acl,
                args=(data, project_name),
                job_timeout=10,
            )
            return {"job": "running"}
        else:
            update_svn_acl(data, project_name)
            project_repo_url = os.path.join(SVN_PARENT_URL, project_name)
            return jsonify(message=f'project created', project_name=project_name, svn_url=project_repo_url)


api.add_resource(Task, '/task/<string:project_name>')
api.add_resource(Task_File_Access_Control, '/task_acl/<string:project_name>')