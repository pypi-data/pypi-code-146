import logging
from os import environ, path, walk
import paramiko
from sys import exit


_logger = logging.getLogger('vxci.' + __name__)


def check_vars():
    return environ.get('COVERAGE_PASS', False)


def get_values():
    res = {
        'username': 'coverage',
        'password': environ.get('COVERAGE_PASS'),
        'commit_slug': environ.get('CI_COMMIT_REF_SLUG'),
        'project_name': environ.get('CI_PROJECT_NAME')
    }
    return res


def get_sftp_client(username, password):
    _logger.info('Connecting to the remote host')
    transport = paramiko.Transport(('coverage.vauxoo.com', 8451))
    transport.connect(username=username,
                      password=password)
    return paramiko.SFTPClient.from_transport(transport)


def push_files():
    values = get_values()
    # TODO: Match get_config(**kwargs) container_vol value and get_values
    values.update({'container_vol': values['commit_slug']})

    remote_path = '{commit_slug}-{project_name}'.format(**values)
    src_path = '{container_vol}/htmlcov'.format(**values)
    if not path.isdir(src_path):
        _logger.warn('Nothing to report from %s', src_path)
        _logger.warn('\nThis job is failing because the coverage report folder is empty this is due to:' +
                     '\n  - No tests were executed' +
                     '\n  - The test job is not properly configured' +
                     '\n  - The results from the tests are stored in a different folder that the expected' +
                     '\nPlease note that this job should be allowed to fail (allow_failure: true) and the pipeline'
                     '\n will be yellow until this is fixed, but this shouldn\'t avoid the merge unless is unexpected.' +
                     '\nFor more information check the project template: ' +
                     '\n https://git.vauxoo.com/vauxoo/project-template/blob/master/%7B%7Bcookiecutter.project_name%7D%7D/.gitlab-ci.yml')
        return False

    _logger.info('Pushing files from: %s', src_path)
    sftp = get_sftp_client(values.get('username'), values.get('password'))
    for root, dirs, files in walk(src_path):
        _logger.debug('Root: %s .. Dirs: %s .. Files: %s', root, dirs, files)
        remote = path.join(path.relpath(root, src_path), remote_path)
        _logger.debug('Creating remote folder: %s', remote)
        try:
            sftp.mkdir(remote)
        except Exception as error:
            _logger.warning(str(error))
            pass

        for f in files:
            _logger.debug('Uploading file: %s to %s', path.join(root, f), path.join(remote, f))
            sftp.put(path.join(root, f), path.join(remote, f))
    _logger.info('Pushed files')
    return True


def show_url():
    values = get_values()
    print("Coverage report can be found in:")
    print("https://coverage.vauxoo.com/{}-{}".format(values.get('commit_slug'), values.get('project_name')))


def push_coverage_result():
    if not check_vars():
        _logger.error('Variable COVERAGE_PASS is not defined, required to push the files')
        return False
    push_status = push_files()
    if push_status:
        show_url()
    return push_status
