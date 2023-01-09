# coding: utf-8

import gzip

from vxci.get_addons import get_module_list, get_modules2test, get_tags, join_prefix_suffix
from vxbase import vtypes, net, fromenv
from vxci.tools_test import install_chrome_commands
import distutils.spawn
from docker import errors, from_env
import json
import logging
import tempfile
from os import environ, path, makedirs, chmod, remove, getcwd, chdir, listdir, rmdir
import re
import requests
import shlex
import subprocess
import sys
import time
from urllib3.exceptions import ReadTimeoutError
from unicodedata import normalize
from shutil import copy, rmtree
from jinja2 import Template


_logger = logging.getLogger('vxci.' + __name__)
_cli = from_env(timeout=7200).api
TO_SCAN = ['git.vauxoo.com',
           'github.com',
           'gitlab.com',
           'bitbucket.org',
           'git.islamicreliefcanada.ca']
INSTANCE_TYPES = ['develop', 'test', 'updates']


def pull_images(images):
    """ Pulls images needed for the build and test process """
    for image in images:
        _logger.info('Pulling: %s', image)
        _cli.pull(image)
    return images


def check_env_vars(*args, **kwargs):
    missing = []
    not_required = ['psql_image', 'push_image', 'install', 'allow_deprecated']
    for key in args:
        if key not in not_required and not (key.upper() in environ and environ[key.upper()]):
            missing.append(key.upper())
    for key in kwargs:
        if not (key.upper() in environ and environ[key.upper()]):
            if kwargs[key]:
                environ[key.upper()] = str(kwargs[key])
            elif key not in not_required:
                missing.append(key.upper())
    assert not missing, (
        "Some environment variables were not found: {keys}".format(
            keys=", ".join(missing)
        ))


def get_main_app(config):
    return config.get('main_app', get_module_list())


def generate_image_name(name):
    """ Generate the base image name using the ref name but cleaning it before,
    ATM only removes "." and "#" from the title to avoid issues with docker naming
    convention """
    res = re.sub(r'[\.#\$\=\+\;\>\,\<,\&\%]', '', name)
    res = re.sub(r'-_', '_', res)
    return res.lower()


def run_build_image(config):
    _logger.info('Building image')
    cmd = ('deployvcmd build -b {branch} -u {url} -v {version} -i {image} -O {repo}#{odoo_branch} -T {tag}'
           .format(branch=config['ci_commit_ref_name'], url=config['ci_repository_url'], repo=config['odoo_repo'],
                   odoo_branch=config['odoo_branch'], version=config['version'], image=config['base_image'],
                   tag=config['instance_image']))
    try:
        subprocess.check_call(shlex.split(cmd))
    except subprocess.CalledProcessError:
        _logger.exception('Could not build the image, please read the log above')
        sys.exit(1)
    images = _cli.images(config['instance_image'])
    if not images:
        _logger.error('Could not build the image, please read the log above')
        sys.exit(1)
    image_sha = images[0].get('Id')
    short_id = image_sha.split(':')[1][:10]
    tag = short_id
    git_sha = config["git_commit_sha"][:7]  # 7 is the default size "git rev-parse --short HEAD"
    if config.get('docker_image_repo'):
        tag = "%s-%s-%s" % (config['main_app'], config['version'], short_id)
        git_tag = "%s-%s-%s" % (config['main_app'], config['version'], git_sha)
        if is_dev_repo(config):
            tag = "%s-%s-dev%s" % (config['main_app'], config['version'], short_id)
    config.update({'image_tag': tag, 'image_git_tag': git_tag})


def clear_images(config):
    if config.get("vxci_no_clear_images"):
        return
    images = [config['instance_image'], config['postgres_image'], ]
    for image in images:
        try:
            _logger.info('Removing image %s', image)
            _cli.remove_image(image)
        except errors.APIError as error:
            if 'No such image' in error.explanation:
                pass
        _logger.info('Image %s deleted', image)


def clean_containers(config):
    """ Cleans any running container related to the same build to avoid any conflicts """
    if config.get("vxci_no_clear_containers"):
        return
    containers = _cli.containers(all=True, filters={'name': config['base_name']})
    for container in containers:
        try:
            _logger.info('Removing container %s', container.get('Name', container.get('Names')[0]))
            _cli.remove_container(container['Id'], force=True)
        except errors.NotFound:
            _logger.info('Container %s does not exist', container.get('Name', container.get('Names')[0]))


def reciveSignal(signalNumber, frame):
    clean_containers()
    clear_images()
    sys.exit(0)


def push_image(config, image_name, image_tag):
    img_repo = config.get('docker_image_repo') or config['image_repo']
    _logger.info('Pushing image %s to %s:%s', image_name, img_repo, image_tag)
    _cli.tag(image_name, img_repo, tag=image_tag)
    if is_docker_login(config):
        _logger.info('Logging in to push: %s', config['docker_repo'])
        _cli.login(config['docker_user'], config['docker_password'], registry=config['docker_repo'])
    for attempt in range(4):
        try:
            for result in _cli.push(img_repo, tag=image_tag, stream=True):
                result = json.loads(vtypes.decode(result))
                if result.get('error'):
                    _logger.error(result.get('error'))
                    sys.exit(1)
            else:
                break
        except ReadTimeoutError as error:
            if 'Read timed out' in error.message and attempt < 3:
                _logger.warn('An error raised while pushing the image, retrying (%s / 3)', attempt+1)
            else:
                raise

    _logger.info('Image pushed correctly')


def notify_orchest(config, is_latest=False):
    if not config.get('ci_project_id', '').isdigit():
        _logger.warning('No project id defined or is a string, not notifying to Orchest')
        return

    img_repo = config.get('docker_image_repo') or config['image_repo']
    image_name = '{image}:{tag}'.format(image=img_repo, tag=config['image_tag'])
    res = requests.post(
        config['orchest_registry'], data=json.dumps({
            'image_name': image_name, 'is_latest': is_latest, 'branch_name': config['ci_commit_ref_name'],
            'job_id': config['ci_job_id'], 'project_id': config['ci_project_id'],
            'commit': config['ci_commit_sha'][:7], 'customer_id': config['customer_img']}),
        headers={'Content-Type': 'application/json', 'Orchest-Token': config['orchest_token']})
    if res.status_code != 200:
        _logger.error('Failed to notify orchest about the new image: %s', res.text)
        sys.exit(1)
    data = res.json()
    if data.get('error'):
        _logger.error('Failed to notify orchest about the new image: %s',
                      data.get('error').get('data', {}).get('name'))
        sys.exit(1)
    _logger.info('Successfully notified orchest about the new image: %s', image_name)


def get_value(var_name, **kwargs):
    return kwargs[var_name] if var_name in kwargs else environ[var_name.upper()]


def is_dev_repo(config):
    return config.get('ci_commit_ref_name') != config['version'] or config.get('ci_project_namespace').endswith('-dev')


def slugify(s):
    slug = normalize('NFKD', s)
    slug = slug.encode('ascii', 'ignore').lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug.decode('ascii', 'ignore')).strip('-')
    return re.sub(r'[-]+', '-', slug)


def map_github_action(config):
    config['ci_commit_ref_name'] = config.get('github_ref_name')
    config['ci_job_id'] = config.get('github_run_id')
    config['ci_pipeline_id'] = config.get('github_run_number')
    config['ci_project_name'] = config.get('customer')
    repos = config.get('github_repository', '').split('/')
    if len(repos) > 1:
        config['ci_project_name'] = repos[1]
    config['ci_commit_ref_slug'] = slugify(config.get('github_ref_name'))
    config['ci_repository_url'] = net.urljoin(config.get('github_server_url'), config.get('github_repository'))
    config['ci_commit_sha'] = config.get('github_sha')
    config['ci_project_namespace'] = config.get('github_repository_owner')
    config['ci_project_id'] = config.get('github_repository')
    config['git_commit_sha'] = config.get('github_sha')


def get_config(**kwargs):
    rand_str = 'hd103sl'
    res = {}
    for k, v in environ.items():
        res.update({k.lower(): v})

    for key in kwargs:
        res.update({key.lower(): get_value(key, **kwargs)})

    if fromenv.is_github():
        _logger.debug('Inside github action')
        map_github_action(res)
    res.update({'private_deploy_key': res.get('private_deploy_key', False)})
    img_name = generate_image_name('{0}_{1}'.format(
        res['ci_commit_ref_name'], res['ci_job_id']))
    res.update({'base_name': img_name})

    if res.get('psql_image'):
        postgres_image = res.get('psql_image')
    else:
        postgres_image = 'vauxoo/docker-postgresql:{0}-ci'.format(res.get('psql_version', '9.6'))
    res.update({'postgres_image': postgres_image})

    customer = res.get('customer', res.get('ci_project_name')).strip()
    version_tag = res.get('version').replace('.', '')
    customer_img = '{customer}{ver}'.format(customer=customer,
                                            ver=version_tag)
    if not res.get('image_repo', False) and not res.get('image_tag', False):
        image_repo = '{url}/{image}'.format(url=res.get('image_repo_url'),
                                            image=customer_img)
        res.update({'image_repo': image_repo})
        instance_image = generate_image_name('instance{0}_{1}'.format(
            res.get('base_name'), res.get('ci_pipeline_id')))
    else:
        instance_image = '{}:{}'.format(res['image_repo'], res['image_tag'])

    res.update({'instance_image': instance_image})

    res.update({
        'customer': customer,
        'version_tag': version_tag,
        'customer_img': customer_img,
        'container_name': '{}_instance_{}_{}'.format(res['base_name'], res['ci_pipeline_id'], rand_str)
    })

    res.update({'docker_repo': res.get('docker_repo', 'quay.io')})
    res.update({'image_repo_url': res.get('image_repo_url', 'quay.io/vauxoo')})
    res.update({'postgres_container': 'postgres{0}_{1}_{2}'.format(res['base_name'], res['ci_pipeline_id'], rand_str)})
    res.update({
        'main_app': get_main_app(res)
    })

    # Host folder where the artifacts will be stored after the testes were executed
    res.update({'container_vol': res.get('ci_commit_ref_slug')})

    # The work dir inside the container, the config and coverage result will be stored here
    res.update({'coverage_workdir': '/home/odoo'})

    # Where the results will be stored, html and xml files. Ths odoo logs will be stored here, but won't be uploaded
    # to the coverage server
    res.update({'coverage_reports': '/tmp/coverage_reports'})
    return res


def docker_login(config):
    """ Execute docker login from the actual console because whe done via the api they won't persist """
    cmd = 'sh -c "echo \'{passw}\' | docker login --username \'{login}\' --password-stdin {repo}"'.format(
        passw=config['docker_password'],
        login=config['docker_user'],
        repo=config['docker_repo']
    )
    subprocess.Popen(shlex.split(cmd))


def check_docker():
    """ Checks if the docker binary is present in the running environment """
    return distutils.spawn.find_executable("docker")


def is_docker_login(config):
    """ Check if we have all we need to docker login (via cli or api), that is:

    - We have docker binary available
    - We have the env vars properly set (DOCKER_PASSWORD and DOCKER_USER)"""
    return check_docker() and config.get('docker_password', False) and config.get('docker_user', False)


def scan_keys(folder):
    """ Performs a ssk-key scan in the list of hosts and add the keys to the
    known_hosts files

    :param folder: The folder where the file will be stored
    """
    known_hosts = path.join(folder, 'known_hosts')
    with open(known_hosts, 'a') as known_file:
        for host in TO_SCAN:
            try:
                keys = subprocess.check_output(['ssh-keyscan', host], stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as error:
                _logger.warn(('Could not scan %s host, if you get any error cloning '
                              'from this provider, please try again later'), host)
                _logger.warn('Error was: %s', error.output)
            else:
                for line in vtypes.decode(keys).split('\n'):
                    clean = line.strip()
                    if clean:
                        known_file.write(clean + '\n')
    subprocess.check_call(['ls', '-l', folder])


def add_private_key(key, folder):
    """ Generates the id_rsa file if it doesn't exist with the proper
    format and permissions.

    :param key: The key content
    :param folder: The folder where the id_rsa file will be stored
    """
    ssh_file = path.join(folder, 'id_rsa')
    if path.isfile(ssh_file):
        _logger.info('The id_rsa file already exists, nothing to do')
        return
    with open(ssh_file, 'w') as ssh_key:
        ssh_key.write(key)
    try:
        subprocess.check_call(['dos2unix', ssh_file])
    except subprocess.CalledProcessError:
        _logger.error('You need to install dos2unix to check the key')
    chmod(ssh_file, 0o0600)


def check_ssh_folder():
    """ Check if the folder exists and create it

    :return: The full path to the .ssh folder
    """
    home_path = path.expanduser(path.join('~', '.ssh'))
    if not path.isdir(home_path):
        makedirs(home_path)
    return home_path


def check_credentials(config):
    _logger.info('Check ssh folder')
    ssh_folder = check_ssh_folder()
    if config['private_deploy_key']:
        _logger.info('Adding private key')
        add_private_key(config['private_deploy_key'], ssh_folder)

    _logger.info('Scan hosts keys')
    scan_keys(ssh_folder)

    if is_docker_login(config):
        _logger.info('Logging in %s', config['docker_repo'])
        docker_login(config)


def prepare(**kwargs):
    if not fromenv.is_github():
        check_env_vars(**kwargs)
    config = get_config(**kwargs)
    check_credentials(config)
    return config


def save_imagename(work_dir, config):
    if path.isfile(work_dir):
        remove(work_dir)
    if not path.isdir(work_dir):
        makedirs(work_dir)
    filename = path.join(work_dir, "image_name.env")
    with open(filename, "w") as f:
        img = config.get('docker_image_repo') or config['image_repo']
        f.write("export IMAGE_REPO={}\n".format(img))
        f.write("export IMAGE_TAG={}\n".format(config['image_tag']))


def get_coverage_env_variables(config):
    coverage_info = {
        "COVERAGE_RCFILE": "%(coverage_reports)s/.coveragerc" % config,
        "COVERAGE_EXTRACSSFILE": "%(coverage_reports)s/.coverage.css" % config,
        "COVERAGE_FILE": "%(coverage_reports)s/.coverage_%(ci_job_name)s" % config,
        "COVERAGE_HOME": "/home/odoo/instance/extra_addons/%(ci_project_name)s" % config,
        "COVERAGE_CONTEXT": "job_%(ci_job_name)s" % config,
        "EXCLUDE_COVERAGE": config.get("exclude_coverage"),
        "COVERAGE_PRECISION": config.get("coverage_precision"),
        "COVERAGE_DYNAMIC_CONTEXT": config.get("coverage_dynamic_context"),
    }
    return coverage_info


def odoo_config2psql_env(config):
    """Translate odoo configuration parameters to psql environment variables
    In order to be able to run 'psql' command directly without extra parameters
    to connect to databases"""
    psql_env = {}
    for key, value in config.items():
        if not key.startswith("DB_"):
            continue
        new_key = key.replace("DB_", "PG") if key != "DB_NAME" else "PG_DATABASE"
        psql_env[new_key] = value
    return psql_env


def start_instance(config):
    coverage_info = get_coverage_env_variables(config)
    env = {
        "DB_USER": "odoo",
        "DB_PASSWORD": "odoo",
        "DB_HOST": config['postgres_container'],
        "ODOO_CONFIG_FILE": "/home/odoo/.openerp_serverrc",
        "AUTOSTART": "false",
        # Enable this to debug coverage
        # "COVERAGE_DEBUG": "config,dataio,process",
    }
    env.update(coverage_info)
    psql_env = odoo_config2psql_env(env)
    env.update(psql_env)
    config.update({key.lower(): value for key, value in coverage_info.items()})
    for env_var in ['COUNTRY', 'LANGUAGE']:
        env.update({env_var: environ.get(env_var, "")})
    links = {
        config['postgres_container']: config['postgres_container']
    }
    host_config = _cli.create_host_config(links=links)
    _logger.info('Starting container %s', config['container_name'])
    _logger.debug('Env vars %s', json.dumps(env, sort_keys=True, indent=4))
    container = _cli.create_container(image=config['instance_image'],
                                      name=config['container_name'],
                                      environment=env,
                                      host_config=host_config)
    _cli.start(container=container.get('Id'))
    _logger.info(container)


def start_postgres(config):
    try:
        _logger.info('Pulling postgresql image %s', config['postgres_image'])
        _cli.pull(config['postgres_image'])
    except errors.ImageNotFound:
        _logger.error(('Image %s not found.'
                      ' Make sure variables are properly set and that the Psql version exists'),
                      config['postgres_image'])
        raise
    _logger.info('Starting container %s', config['postgres_container'])
    container = _cli.create_container(image=config['postgres_image'],
                                      name=config['postgres_container'],
                                      environment={'POSTGRES_PASSWORD': 'postgres',
                                                   'PGDATA': '/var/lib/postgresql/data/pgdata'},
                                      volumes=['/var/lib/postgresql/data/pgdata', ],
                                      host_config=_cli.create_host_config(tmpfs={
                                          '/var/lib/postgresql/data/pgdata': '',
                                      }))
    _cli.start(container=container.get('Id'))
    _logger.info(container)


def exec_cmd(container, cmd, user=None, stream=False, workdir=None, tty=False):
    lines = []
    container_id = _cli.inspect_container(container).get('Id')
    _logger.debug('Executing command "{cmd}" in container "{con}".'.format(cmd=cmd, con=container))
    try:
        exec_id = _cli.exec_create(container_id, cmd, user=user, workdir=workdir, tty=tty)
    except errors.APIError as error:
        _logger.error('Error: %s', error.explanation)
        raise
    res = _cli.exec_start(exec_id.get('Id'), stream=stream)
    if stream:
        _logger.info("--->> Start of the stream <<---")
        for line in res:
            line = vtypes.decode(line)
            print(line.strip('\n'), flush=True)
            lines.append(line)
        _logger.info("--->> End of the stream <<---")
        return lines
    return vtypes.decode(res)


def create_postgres_user(config):
    cmd = "psql -c \"create user odoo with password 'odoo' superuser\""
    retry = 0
    while retry < 4:
        res = exec_cmd(config['postgres_container'], cmd, 'postgres')
        if 'could not connect to server' in res or 'connection to server on socket' in res:
            retry += 1
            _logger.info('Waiting for the postgres container to start (retrying %s)', retry)
            time.sleep(3)
        else:
            break
    return res


def is_running(config):
    retry = True
    retries = 0
    while retry and retries <= 10:
        try:
            res = exec_cmd(config['container_name'], 'supervisorctl status odoo')
        except errors.APIError as err:
            retries += 1
            _logger.warn('Container error, retrying %s', retries)
            _logger.debug('Error: %s', err)
            time.sleep(5)
            continue
        _logger.info('is_running: %s', res.strip())
        if 'STARTING' in res or 'STOPPING' in res:
            _logger.warn('The Odoo process is in an intermediate state, retrying')
            time.sleep(5)
        elif 'RUNNING' in res:
            return True
        elif 'STOPPED' in res:
            return False
        elif res == '' or 'no such file' in res:
            retries += 1
            _logger.warn('Supervisor returned empty or not running yet, retrying %s', retries)
            time.sleep(5)
        else:
            retries += 1
            _logger.warn('Unknown state: %s', res)
            time.sleep(5)


def install_module(config):
    module = config['main_app']
    extra = ''
    if config.get('language', False):
        extra += ' --load-language={lang}'.format(lang=config.get('language'))
    install_wdemo = (
        "/home/odoo/instance/odoo/odoo-bin -d wdemo -i {mod}"
        "{extra} --stop-after-init".format(mod=module, extra=extra)
    )
    install_wodemo = (
        "/home/odoo/instance/odoo/odoo-bin -d wodemo -i {mod}"
        "{extra} --stop-after-init --without-demo=all".format(mod=module, extra=extra)
    )
    _logger.info('Verifying supervisorctl')
    is_running(config)
    _logger.info('Stopping odoo')
    exec_cmd(config['container_name'], 'supervisorctl stop odoo')
    _logger.info('\nInstalling %s with demo', module)
    _logger.debug('Command : %s', install_wdemo)
    wdemo_res = exec_cmd(config['container_name'], install_wdemo, 'odoo', stream=True)
    wdemo_log = resume_log(wdemo_res, config['allow_deprecated'])
    _logger.info('\nInstalling %s without demo', module)
    _logger.debug('Command : %s', install_wodemo)
    wodemo_res = exec_cmd(config['container_name'], install_wodemo, 'odoo', stream=True)
    wodemo_log = resume_log(wodemo_res, config['allow_deprecated'])
    show_log(wdemo_log[1], 'Installation with demo', config)
    show_log(wodemo_log[1], 'Installation without demo', config)
    _logger.debug('Installation wdemo res: %s', wdemo_log[0])
    _logger.debug('Installation wodemo res: %s', wodemo_log[0])
    if not wdemo_log[0] or not wodemo_log[0]:
        return False
    return True


def container_coverage_reports(config, combine=False):
    cover_reports = []
    if combine:
        # Use /bin/sh to propagate the "_*" into the container instead of the host
        cmd = '/bin/sh -c "coverage combine --keep {coverage_reports}/.coverage_*"'.format(**config)
        cover_reports.append(cmd)

    cover_reports.append('coverage report -m --show-missing')
    if combine:
        # Only get html and xml in push_coverage job
        cover_reports.extend([
            'coverage html -d {coverage_reports}/htmlcov'.format(**config),
            'coverage xml -o {coverage_reports}/coverage.xml'.format(**config),
        ])

    status, msg = (True, "")
    for cr in cover_reports:
        cmd_res = exec_cmd(config['container_name'], cr, 'odoo', stream=False, workdir=config.get('coverage_home'))
        _logger.info("Coverage reports command: %s Result:\n%s", cr, cmd_res)
        if status and "Coverage failure" in cmd_res:
            status, msg = (False, cmd_res.splitlines()[-1])

    cmd = 'docker cp {container_name}:{coverage_reports}/. {container_vol}/.'.format(**config)
    subprocess.call(shlex.split(cmd))

    return (status, msg)


def test_module(config):
    modules2test = get_modules2test('.', config.get('include'), config.get('exclude'))
    odoo_test_tags = [i.strip() for i in (config.get('odoo_test_tags') or '').strip().split(',')]
    tags = get_tags(modules2test, odoo_test_tags)
    _logger.debug("module: %s", modules2test)
    extra = ''
    if config.get('language', False):
        extra += ' --load-language={lang}'.format(lang=config.get('language'))

    extra += ' --test-tags={tags}'.format(tags=tags)
    _logger.debug("extra: %s", extra)

    test_command = (
        "unbuffer coverage run /home/odoo/instance/odoo/odoo-bin -d test -i {mod} --test-enable --workers 0 "
        "{extra} --stop-after-init".format(mod=','.join(modules2test), extra=extra)
    )
    _logger.info('Verifying supervisorctl')
    is_running(config)
    _logger.info('Stopping odoo')
    exec_cmd(config['container_name'], 'supervisorctl stop odoo')
    prepare_coverage(config)
    install_test_deps(config)

    _logger.info('\nRunning tests for %s', modules2test)
    _logger.info('Command : %s', test_command)
    test_res = exec_cmd(config['container_name'], test_command, 'odoo', stream=True, workdir=config.get('coverage_home'))

    test_log = resume_log(test_res, config['allow_deprecated'])
    success = test_log[0]
    show_log(test_log[1], 'Installation with demo and tests', config)
    save_logs(config, test_res)

    container_coverage_reports(config)

    # Parse template for all instance types and run queries for each one
    for instance_type in INSTANCE_TYPES:
        _logger.info("Deactivating database using instance type: %s", instance_type)
        sql_container_fname = "/tmp/%s.sql" % instance_type
        with tempfile.NamedTemporaryFile("w") as f_sql:
            # Using ROLLBACK in order to avoid errors because of constraints
            # e.g. "CREATE ROLE" more than one time raises "already exists"
            f_sql.write("BEGIN;\n%s;\nROLLBACK;" % join_prefix_suffix(
                deactivate2queries(instance_type), prefix="", suffix=";"))
            f_sql.flush()
            subprocess.call(["docker", "cp", f_sql.name, "%s:%s" % (config['container_name'], sql_container_fname)])
        exec_cmd(config['container_name'], ["chown", "odoo:odoo", sql_container_fname])
        cmd_query = ["/bin/sh", "-c", 'psql test -v ON_ERROR_STOP=1 -aXtAf "%s" && echo "pass"' % sql_container_fname]
        query_res = exec_cmd(config['container_name'], cmd_query, 'odoo')
        query_res_lines = query_res.splitlines()
        if "pass" in query_res_lines[-1:]:
            continue
        _logger.error("Result deactivating database using instance type: %s\n%s", instance_type, '\n'.join(query_res_lines))
        success = False
    return success

def copy_files(src, dst):
    for file_name in listdir(src):
        source = path.join(src, file_name)
        destination = path.join(dst, file_name)
        if path.isfile(source):
            copy(source, destination)


def install_test_deps(config):
    _logger.debug('Installing dependencies to run tests')
    exec_cmd(config.get('container_name'), 'touch /home/odoo/full_test-requirements.txt')
    exec_cmd(config.get('container_name'), 'pip3 install -r /home/odoo/full_test-requirements.txt')

    exec_cmd(config.get('container_name'), 'apt update')
    exec_cmd(config.get('container_name'), 'apt install expect-dev tcl8.6')

    for install_chrome_command in install_chrome_commands(config.get("chrome_version")):
        exec_cmd(config.get('container_name'), install_chrome_command)


def prepare_coverage(config):
    if not path.isdir(config.get('container_vol')):
        makedirs(config.get('container_vol'))
    fcoveragerc = path.join(config.get('container_vol'), '.coveragerc')
    with open(fcoveragerc, "w") as f_coveragerc:
        f_coveragerc.write(get_coverage_content(config))
    copy(path.join(path.abspath(path.dirname(__file__)), "templates", "coverage.css"),
         path.join(config.get('container_vol'), '.coverage.css'))

    _logger.debug('Create workdir %s', exec_cmd(config['container_name'], 'mkdir -p {coverage_reports}'.format(**config), user='odoo'))

    cp_cover_cmd = 'docker cp {container_vol}/. {container_name}:{coverage_reports}/.'.format(**config)
    subprocess.call(shlex.split(cp_cover_cmd))

    _logger.debug('Changed permissions for coverage %s', exec_cmd(config['container_name'], 'chown -R odoo:odoo {coverage_reports}'.format(**config)))

    exec_cmd(config.get('container_name'), 'pip3 install coverage')


def save_logs(config, logs):
    odoo_log = path.join(config.get('container_vol'), 'odoo.log.gz_%(ci_job_name)s' % config)
    _logger.info("Save log in %s cwd %s", odoo_log, getcwd())
    with gzip.open(odoo_log, "wb") as fodoo_log:
        for line in logs:
            fodoo_log.write(line.encode("UTF-8"))


def get_coverage_content(config):
    modules2test = get_modules2test('.', config.get('include'), config.get('exclude'))
    include_coverage = "%s/*" % join_prefix_suffix(modules2test, "./", "/*,")
    with open(path.join(path.abspath(path.dirname(__file__)), "templates", "coveragerc"), "r") as f_coveragerc:
        coveragerc_content = f_coveragerc.read().format(include_coverage=include_coverage)
    return coveragerc_content

def show_log(log, title, config):
    _logger.info('='*50)
    _logger.info('%s', title)
    if config['allow_deprecated']:
        _logger.warning('+++ Deprecated methods allowed')
    _logger.info('='*50)
    _logger.info('+-- Critical errors %s', len(log.get('critical')))
    _logger.info('+-- Errors %s', len(log.get('errors')))
    _logger.info('+-- Import errors %s', len(log.get('import_errors')))
    _logger.info('+-- Deprecation Warnings %s', len(log.get('warnings_deprecated')))
    _logger.info('+-- Warnings %s', len(log.get('warnings')))
    _logger.info('+-- Translation Warnings %s', len(log.get('warnings_trans')))
    _logger.info('*'*50)


def resume_log(log_lines, allow_deprecated=False):
    """Gets the log lines from -u (modules or all) and parse them to get the totals
    according to the filters dict

    :param log_lines: each element of the list is a log line
    :return: dict with key filters as keys and a list with all matched lines
    """
    def critical(line):
        criteria = re.compile(r'.*\d\sCRITICAL\s.*')
        return criteria.match(line)

    def errors(line):
        criteria = re.compile(r'.*\d\sERROR\s.*')
        return criteria.match(line)

    def warnings_trans(line):
        criteria = re.compile(
            r'.*\d\sWARNING\s.*no translation for language.*')
        return criteria.match(line)

    def warnings_deprecated(line):
        criteria = re.compile(
            r'.*\d\sWARNING\s.*Deprecated method.*')
        return criteria.match(line)

    def import_errors(line):
        criteria = re.compile(r'^ImportError.*')
        return criteria.match(line)

    def warnings(line):
        criteria = re.compile(r'.*\d\sWARNING\s.*')
        return criteria.match(line) \
            and 'no translation for language' not in line \
            and 'Deprecated method' not in line \
            and 'odoo.tests.runner: 0 failed, 0 error(s) of 0 tests when loading database' not in line \
            and (' py.warnings: ' not in line or '/extra_addons/' in line)  # silent py.warnings raised from odoo core

    filters = {
        'critical': critical,
        'errors': errors,
        'warnings': warnings,
        'warnings_trans': warnings_trans,
        'warnings_deprecated': warnings_deprecated,
        'import_errors': import_errors
    }
    success = True
    res = {name: [] for name in filters}
    # Read log file removing ASCII color escapes:
    # http://serverfault.com/questions/71285
    color_regex = re.compile(r'\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]')
    is_module_loaded = False
    is_build_ended = False
    for line in log_lines:
        if isinstance(line, bytes):
            line = line.decode("UTF-8")
        original_line = line.strip()
        if ".modules.loading: Modules loaded." in original_line:
            is_module_loaded = True
        elif "Initiating shutdown" in original_line:
            # Using the same way than runbot:
            # https://github.com/odoo/runbot/blob/964a88cb/runbot/models/build_config.py#L998
            is_build_ended = True
        # Remove colorized when exists to regex
        stripped_line = color_regex.sub('', original_line)
        for name, criteria in filters.items():
            if criteria(stripped_line):
                if name in ['critical', 'errors']:
                    success = False
                elif name == 'warnings_deprecated' and not allow_deprecated:
                    success = False
                res.get(name).append(original_line)
                break
    if not success:
        _logger.error("Error or traceback found in logs")
    elif not is_module_loaded:
        _logger.error("Modules loaded not found in logs")
    elif not is_build_ended:
        _logger.error('No "Initiating shutdown" found in logs, maybe because of cpu limit or Aborted (core dumped).')
    return success and is_module_loaded and is_build_ended, res


def run_image_tests(config, test_only=False):
    clean_containers(config)
    start_postgres(config)
    resp = create_postgres_user(config)
    _logger.info(resp)
    start_instance(config)
    if not test_only:
        res = install_module(config)
    else:
        res = test_module(config)
    clean_containers(config)
    return res


def generate_coverage_reports(config):
    clean_containers(config)
    coverage_env = get_coverage_env_variables(config)
    config.update({key.lower(): value for key, value in coverage_env.items()})
    pull_images([config['instance_image']])
    container = _cli.create_container(
        image=config['instance_image'],
        name=config['container_name'],
        environment=coverage_env,
    )
    _cli.start(container=container.get('Id'))
    _logger.info(container)
    prepare_coverage(config)
    status, msg = container_coverage_reports(config, combine=True)
    clean_containers(config)
    return status, msg


def deactivate2queries(instance_type):
    deactivate_path = 'deactivate.jinja'
    if not path.isfile(deactivate_path):
        _logger.debug("Deactivate file %s does not exists", deactivate_path)
        return []
    with open(deactivate_path) as f_deactivate:
        template_str = f_deactivate.read()
    template = Template(template_str)
    rendered_template = template.render(instance_type=instance_type)
    queries = [q[1] for q in sorted(json.loads(rendered_template).items())]
    _logger.debug("Template rendered for instance type %s:\n%s\n", instance_type, '\n'.join(queries))
    return queries
