import subprocess
import json
import sys
import os

import requests


def error(msg, code=1):
    print(msg, file=sys.stderr)
    exit(code)


def ensure_docker():
    result = subprocess.run(['docker', 'version', '--format', '{{json .}}'],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        error('Docker not found on this system. Make sure that docker is installed, running and reachable.')
    res = json.loads(result.stdout.decode())
    print(f'.. Found docker client {res["Client"]["Version"]}, server {res["Server"]["Version"]}')

    result = subprocess.run(['docker', 'compose', 'version'])
    if result.returncode != 0:
        error('Docker compose plugin not found on this system. Make sure you have docker compose installed. \n'
              'E.g. on ubuntu, you can install it with \'sudo apt-get install docker-compose-plugin\'')
    print('.. Found docker compose plugin')


def _test_mender_artifact(artifact_path):
    result = subprocess.run([artifact_path, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        res = result.stdout.decode()
        print('.. Found mender artifact ' + res)
        return True
    return False


def _download_file(url, target):
    with requests.get(url) as r:
        r.raise_for_status()
        with open(target, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


def ensure_mender_artifact(artifact_path):
    if os.path.exists(artifact_path) and os.path.isfile(artifact_path):
        if _test_mender_artifact(artifact_path):
            return

    try:
        if sys.platform == 'linux':
            _download_file('https://downloads.mender.io/mender-artifact/3.9.0/linux/mender-artifact', artifact_path)
        elif sys.platform == 'darwin':
            _download_file('https://downloads.mender.io/mender-artifact/3.9.0/darwin/mender-artifact', artifact_path)
        else:
            error(f'Error: Platform {sys.platform} not supported. No available mender artifact.')
    except Exception as e:
        print(e, file=sys.stderr)
        error('Failed to download mender artifact. Retry later.')

    os.chmod(artifact_path, 755)
    if not _test_mender_artifact(artifact_path):
        error(f'Error: Failed to execute mender artifact at {artifact_path}. Aborting.')

