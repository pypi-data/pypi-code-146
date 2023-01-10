from vxbase import vtypes
from docker import from_env
import subprocess
import shlex
from os import environ, unsetenv
import sys
import logging
import json


_logger = logging.getLogger('vxci.' + __name__)
_cli = from_env(timeout=600).api


def build_image():
    format_values = {
        'url': environ['CI_REPOSITORY_URL'],
        'version': environ['CI_COMMIT_REF_NAME'],
        'base': environ['BASE_IMAGE'],
        'odoo_repo': environ['ODOO_REPO'],
        'odoo_branch': environ['ODOO_BRANCH'],
        'name': environ['_IMAGE_NAME'],
    }
    _logger.info('Bulding image %s', environ['_IMAGE_NAME'])
    cmd = (
        'deployvcmd build -u {url} -v {version} -i {base} -O {odoo_repo}#{odoo_branch} -T {name}'
        .format(**format_values)
    )
    subprocess.check_call(shlex.split(cmd))
    image_sha = _cli.images(name=environ['_IMAGE_NAME'], quiet=True)
    res = image_sha and image_sha[0].decode().split(':')[1][:10]
    return res


def push_image(tags):
    if environ.get('https_proxy', False):
        unsetenv('https_proxy')
    for tag in tags:
        _logger.info('Pushing image %s to %s:%s', environ['_IMAGE_NAME'], environ['_IMAGE_REPO'], tag)
        _cli.tag(environ['_IMAGE_NAME'], environ['_IMAGE_REPO'], tag=tag)
        for result in _cli.push(environ['_IMAGE_REPO'], tag=tag, stream=True):
            result = json.loads(vtypes.decode(result))
            if result.get('error'):
                _logger.error(result.get('error'))
                sys.exit(1)

