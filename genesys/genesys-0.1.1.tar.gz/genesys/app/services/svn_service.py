import subprocess
import os
from configparser import ConfigParser, NoSectionError
from genesys.app.utils import config_helpers
from genesys.app.config import SVN_PARENT_PATH

def create_svn_repo(project_svn_repo_path):
    subprocess.run(['svnadmin', 'create', project_svn_repo_path], stdout=None)

def svn_check_out(project_repo_url, project_folder):
    subprocess.run(['svn', 'co', project_repo_url, project_folder], stdout=subprocess.DEVNULL)

def svn_commit_all(project_folder, svn_commit_message):
    subprocess.run(['svn', 'cleanup', project_folder], stdout=subprocess.DEVNULL)
    subprocess.run(['svn', 'add', project_folder, '--force'], stdout=subprocess.DEVNULL)
    subprocess.run(['svn', 'cleanup', project_folder], stdout=subprocess.DEVNULL)
    subprocess.run(['svn', 'commit', project_folder, '-m', svn_commit_message], stdout=subprocess.DEVNULL)

def svn_relocate(new_url, working_path):
    subprocess.run(['svn', 'relocate', new_url, working_path], stdout=subprocess.DEVNULL)

def svn_delete(url, log_message):
    subprocess.run(['svn', 'delete', '-m', log_message, url], stdout=subprocess.DEVNULL)
    url_dir_name = os.path.dirname(url)
    proc = subprocess.run(['svn', 'list', url_dir_name], stdout=subprocess.PIPE)
    if is_svn_url(url_dir_name) and not bool(proc.stdout.decode()):
        svn_delete(url_dir_name, log_message='deleted')

def is_svn_url(url):
    proc = subprocess.run(['svn', 'list', url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return not bool(proc.returncode)

def svn_rename(old_url, new_url, log_message):
    subprocess.run(['svn', 'rename', '-m', log_message, '--parents', old_url, new_url], stdout=subprocess.DEVNULL)
    url_dir_name = os.path.dirname(old_url)
    proc = subprocess.run(['svn', 'list', url_dir_name], stdout=subprocess.PIPE)
    if is_svn_url(url_dir_name) and not bool(proc.stdout.decode()):
        svn_delete(url_dir_name, log_message='deleted')

def svn_mkdir(url, log_message):
    subprocess.run(['svn', 'mkdir', '-m', log_message, url], stdout=subprocess.DEVNULL)

def svn_make_dirs(url, log_message):
    subprocess.run(['svn', 'mkdir', '-m', log_message, '--parents', url], stdout=subprocess.DEVNULL)

def svn_import(path, repo_url, log_message):
    subprocess.run(['svn', 'import', '-m', log_message, path, repo_url], stdout=subprocess.DEVNULL)

def default_acl(project_name):
    svn_authz_path = os.path.join(SVN_PARENT_PATH, project_name.replace(' ', '_').lower(), 'conf/authz')
    acl_parser = ConfigParser()
    acl_parser['groups'] = {
                'admin':'super-user',
                'super_reader':'super-reader',
                'maps':'',
                'edit':'',
            }
    acl_parser['/'] = {
                '*':'r',
                '@admin':'rw',
                '@super_reader':'r',

            }
    config_helpers.write_config(svn_authz_path, acl_parser)

def svn_update_acl(base_svn_directory, acl_parser, person, permission):
    if base_svn_directory not in acl_parser:
        acl_parser[base_svn_directory] = {
            '@admin':'rw',
            '@super_reader':'r',
            '*':''
        }
    if acl_parser.has_option(base_svn_directory, person):
        if permission == 'rw':
            acl_parser.set(base_svn_directory, person, permission)
        elif permission == 'r':
            if acl_parser.get(base_svn_directory, person) != 'rw':
                acl_parser.set(base_svn_directory, person, permission)
        elif permission == 'd':
            if acl_parser.get(base_svn_directory, person) != 'rw':
                acl_parser.remove_option(base_svn_directory, person)
        elif permission == 'none':
            acl_parser.remove_option(base_svn_directory, person)
    else:
        if permission in {'r', 'rw'}:
            acl_parser.set(base_svn_directory, person, permission)


def svn_read_file(url):
    proc = subprocess.run(['svn', 'cat', url], stdout=subprocess.PIPE)
    file = proc.stdout.decode("utf-8")
    return file

def svn_propset(url, prop_name, prop_val):
    subprocess.run(['svn', 'propset', prop_name, prop_val, url], stdout=subprocess.DEVNULL)