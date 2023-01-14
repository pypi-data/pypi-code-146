from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource
from genesys.app.config import SVN_PARENT_PATH, SVN_PARENT_URL
from genesys.app.services import queue_store
import os
from genesys.app.utils import config_helpers
from genesys.app.blueprints.asset.utils import rename_asset_task_file, rename_task_acl_section
from configparser import ConfigParser
from genesys.app import config

asset = Blueprint('asset', __name__)
api = Api(asset)

def rename_asset(data, project_name):
    for asset_task in data:
        acl_parser = ConfigParser()
        task_type = asset_task['task_type']
        project = asset_task['project']
        root = os.path.join(project['file_tree']['working']['mountpoint'], project['file_tree']['working']['root'], '')
        # replacing file tree mount point with genesys config mount point
        base_file_directory = asset_task['base_file_directory'].split(root,1)[1]
        new_base_file_directory = asset_task['new_base_file_directory'].split(root,1)[1]
        base_svn_directory = asset_task['base_svn_directory']
        new_base_svn_directory = asset_task['new_base_svn_directory']

        blend_file_url = os.path.join(SVN_PARENT_URL, base_file_directory)
        new_blend_file_url = os.path.join(SVN_PARENT_URL, new_base_file_directory)

        svn_authz_path = os.path.join(SVN_PARENT_PATH, project_name.replace(' ', '_').lower(), 'conf/authz')

        config_helpers.load_config(svn_authz_path, acl_parser)
        rename_asset_task_file(
            old_blend_file_url=blend_file_url,
            new_blend_file_url=new_blend_file_url)
        rename_task_acl_section(
            old_base_svn_directory= base_svn_directory,
            base_svn_directory= new_base_svn_directory,
            acl_parser= acl_parser,
            )
        config_helpers.write_config(svn_authz_path, acl_parser)

class Asset(Resource):
    def put(self, project_name):
        data = request.get_json()
        project_repo_url = os.path.join(SVN_PARENT_URL, project_name)
        if config.ENABLE_JOB_QUEUE:
            queue_store.job_queue.enqueue(
                rename_asset,
                args=(data, project_name),
                job_timeout=10,
            )
            return {"job": "running"}
        else:
            rename_asset(data, project_name)
            return jsonify(message=f'project created', project_name=project_name, svn_url=project_repo_url)

api.add_resource(Asset, '/asset/<string:project_name>')

