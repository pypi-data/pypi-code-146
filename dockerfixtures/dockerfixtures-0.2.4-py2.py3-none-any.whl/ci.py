# -*- coding: utf-8; -*-
import json
import os
from typing import Mapping
from urllib.parse import urlparse
from urllib.request import Request, urlopen


CONTAINERIZED_CI_VENDOR_VARS = ('GITHUB_ACTION', 'CIRCLECI')


def __vendor_check_circleci(environment: Mapping[str, str]) -> bool:
    parsed_url = urlparse(environment['CIRCLE_BUILD_URL'])
    project_slug_bits = parsed_url.path.split('/')[1:4]
    url = ('https://circleci.com/api/v2/project/{}/{}/{}/job/{}'
           .format(*project_slug_bits,
                   environment['CIRCLE_BUILD_NUM'],
                   )
           )
    headers = {}
    if 'CIRCLECI_API_TOKEN' in environment:
        headers['Circle-Token'] = environment['CIRCLECI_API_TOKEN']
    with urlopen(Request(url, headers=headers, method='GET')) as response:
        data = json.load(response)

    # Okay for executor types machine & docker, not sure about other executor types (macos, ...)
    return data['executor']['type'] == 'docker'


def __always_containerized(_: Mapping[str, str]) -> bool:
    return True


__VENDOR_CHECKS = {'CIRCLECI': __vendor_check_circleci,
                   'GITHUB_ACTION': __always_containerized,
                   }


def is_containerized_ci() -> bool:
    if 'CI' not in os.environ:
        return False
    for var in CONTAINERIZED_CI_VENDOR_VARS:
        if var in os.environ:
            return __VENDOR_CHECKS[var](os.environ)
    return False


# vim: et:sw=4:syntax=python:ts=4:
