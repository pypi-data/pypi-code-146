from genesys.app.config import SVN_PARENT_PATH, SVN_PARENT_URL, PROJECTS_FOLDER, FILE_MAP
from genesys.app.blueprints.project.utils import create_project_folders, create_project_file_map
from genesys.app.services import svn_service, project_service
import os
import shutil

def create_project(project_name):
    import time
    time.sleep(10)
    project_svn_folder = os.path.join(SVN_PARENT_PATH, project_name)
    project_repo_url = os.path.join(SVN_PARENT_URL, project_name)
    project_folder = os.path.join(PROJECTS_FOLDER, project_name)
    svn_authz_path = os.path.join(SVN_PARENT_PATH, project_name, 'conf/authz')

    svn_service.create_svn_repo(project_svn_folder)
    svn_service.svn_check_out(project_repo_url, project_folder)
    create_project_folders(project_folder)
    create_project_file_map(project_folder, file_map=FILE_MAP)
    svn_service.svn_commit_all(project_folder, 'event commit')

def rename_project(old_project_name, new_project_name):
    new_project_folder = os.path.join(PROJECTS_FOLDER, new_project_name)
    old_project_folder = os.path.join(PROJECTS_FOLDER, old_project_name)
    new_project_svn_folder = os.path.join(SVN_PARENT_PATH, new_project_name)
    old_project_svn_folder = os.path.join(SVN_PARENT_PATH, old_project_name)
    new_project_repo_url = os.path.join(SVN_PARENT_URL, new_project_name)
    # old_project_repo_url = os.path.join(svn_parent_url, old_project_name)
    shutil.move(old_project_svn_folder, new_project_svn_folder)
    shutil.move(old_project_folder, new_project_folder)
    svn_service.svn_relocate(new_project_repo_url, new_project_folder)