import os
from genesys.app.services import svn_service

def create_project_folders(project_repo):
    base_directories = ['edit', 'lib', 'refs', 'scenes', 'tools']
    for directory in base_directories:
        url = os.path.join(project_repo, directory)
        svn_service.svn_mkdir(url=url, log_message=f'create {url}')