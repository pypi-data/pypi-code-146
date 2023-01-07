# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netcheck']

package_data = \
{'': ['*']}

install_requires = \
['dnspython>=2.2,<3.0',
 'pydantic>=1.10,<2.0',
 'requests>=2.28,<3.0',
 'rich>=12.6,<13.0',
 'typer[all]>=0.7,<0.8']

entry_points = \
{'console_scripts': ['netcheck = netcheck.cli:app']}

setup_kwargs = {
    'name': 'netcheck',
    'version': '0.1.10',
    'description': '',
    'long_description': '![](.github/logo.png)\n\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/netcheck) [![Coverage Status](https://coveralls.io/repos/github/hardbyte/netcheck/badge.svg?branch=main)](https://coveralls.io/github/hardbyte/netcheck?branch=main) ![PyPI - Downloads](https://img.shields.io/pypi/dm/netcheck)\n\n# Netchecks Command Line Tool\n\nConfigurable command line application that can be used to test network conditions are as expected.\n\n\n## Quickstart\n\n\n\n### Installation\n\nInstall the Python package:\n\n```\npip install netcheck\n```\n\nOr run with Docker:\n\n```shell\ndocker run -it ghcr.io/netchecks/netchecks:latest\n```\n\n### Individual Assertions\n\nBy default `netcheck` outputs a JSON result to stdout: \n\n```shell\nnetcheck dns\n{\n  "status": "pass",\n  "spec": {\n    "type": "dns",\n    "nameserver": null,\n    "host": "github.com",\n    "timeout": 30.0\n  },\n  "data": {\n    "startTimestamp": "2022-12-27T22:07:44.592562",\n    "A": [\n      "20.248.137.48"\n    ],\n    "endTimestamp": "2022-12-27T22:07:44.610156"\n  }\n}\n```\n\nPass the `-v` flag to see log messages.\n\nEach check can be configured, e.g. you can specify the `server` and `host` for a `dns` check, and\ntell `netcheck` whether a particular configuration is expected to pass or fail:\n\n\n```shell\nnetcheck dns --server 1.1.1.1 --host hardbyte.nz --should-pass\n```\n\n```json\n{\n  "status": "pass",\n  "spec": {\n    "type": "dns",\n    "nameserver": "1.1.1.1",\n    "host": "hardbyte.nz",\n    "timeout": 30.0\n  },\n  "data": {\n    "startTimestamp": "2022-12-27T22:09:33.449567",\n    "A": [\n      "209.58.165.79"\n    ],\n    "endTimestamp": "2022-12-27T22:09:33.467162"\n  }\n}\n```\n\nNetcheck can check that particular checks fail:\n```shell\n$ netcheck dns --server=1.1.1.1 --host=made.updomain --should-fail\n```\n\nNote the resulting status will show **pass** if the check fails as expected, and **fail** if the check passes unexpectedly!\n\n```json\n{\n  "status": "pass",\n  "spec": {\n    "type": "dns",\n    "nameserver": "1.1.1.1",\n    "host": "made.updomain",\n    "timeout": 30.0\n  },\n  "data": {\n    "startTimestamp": "2022-12-27T22:10:07.726285",\n    "exception-type": "NXDOMAIN",\n    "exception": "The DNS query name does not exist: made.updomain.",\n    "endTimestamp": "2022-12-27T22:10:07.743219"\n  }\n}\n```\n\nA few http checks are also available:\n\n```shell\nnetcheck http --method=get --url=https://s3.ap-southeast-2.amazonaws.com --should-pass\n```\n\n```shell\n$ netcheck http --method=post --url=https://s3.ap-southeast-2.amazonaws.com --should-fail\n```\n\n```json\n{\n  "status": "pass",\n  "spec": {\n    "type": "http",\n    "timeout": 30.0,\n    "verify-tls-cert": true,\n    "method": "post",\n    "url": "https://s3.ap-southeast-2.amazonaws.com"\n  },\n  "data": {\n    "startTimestamp": "2022-12-27T22:11:33.696001",\n    "status-code": 405,\n    "exception-type": "HTTPError",\n    "exception": "405 Client Error: Method Not Allowed for url: https://s3.ap-southeast-2.amazonaws.com/",\n    "endTimestamp": "2022-12-27T22:11:33.900833"\n  }\n}\n```\n\n### Configuration via file\n\nThe main way to run `netcheck` is passing in a list of assertions. \nA json file can be provided with a list of assertions to be checked:\n\n```json\n{\n  "assertions": [\n    {\n      "name":  "deny-cloudflare-dns", \n      "rules": [\n        {"type": "dns", "server":  "1.1.1.1", "host": "github.com", "expected": "pass"}\n      ]\n    }\n  ]\n}\n```\n\nAnd the command can be called:\n\n\n```shell\n$ netcheck run --config tests/testdata/dns-config.json\n```\n\n```json\n{\n  "type": "netcheck-output",\n  "outputVersion": "dev",\n  "metadata": {\n    "creationTimestamp": "2022-12-27T22:16:43.438696",\n    "version": "0.1.7"\n  },\n  "assertions": [\n    {\n      "name": "default-dns",\n      "results": [\n        {\n          "status": "pass",\n          "spec": {\n            "type": "dns",\n            "shouldFail": false,\n            "nameserver": null,\n            "host": "github.com",\n            "timeout": null\n          },\n          "data": {\n            "startTimestamp": "2022-12-27T22:16:43.438704",\n            "A": [\n              "20.248.137.48"\n            ],\n            "endTimestamp": "2022-12-27T22:16:43.455657"\n          }\n        }\n      ]\n    }\n  ]\n}\n```\n\n## Coming Soon\n\n- Propagation of optional rule names and messages through to the output\n- Expected status codes and specific DNS errors.\n- JSON Schema for config file and outputs\n- More checks\n\n## Development\n\nUpdate version in pyproject.toml, push to `main` and create a release on GitHub. Pypi release will be carried\nout by GitHub actions. \n\n\n### Manual Release \nTo release manually, use Poetry:\n\n```shell\npoetry version patch\npoetry build\npoetry publish\n```\n\n### Testing\n\nPytest is used for testing. \n\n```shell\npoetry run pytest\n```\n',
    'author': 'Brian Thorne',
    'author_email': 'brian@hardbyte.nz',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
