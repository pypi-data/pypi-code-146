# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sovereign',
 'sovereign.modifiers',
 'sovereign.sources',
 'sovereign.utils',
 'sovereign.views']

package_data = \
{'': ['*'], 'sovereign': ['static/*', 'static/sass/*', 'templates/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'PyYAML>=5.4,<6.0',
 'aiofiles>=22.1.0,<23.0.0',
 'cachelib>=0.1.1,<0.2.0',
 'croniter>=1.3.5,<2.0.0',
 'cryptography>=38.0.3,<39.0.0',
 'fastapi>=0.88.0,<0.89.0',
 'glom>=20.11.0,<21.0.0',
 'gunicorn>=20.1.0,<21.0.0',
 'requests>=2.28.1,<3.0.0',
 'structlog==21.5.0',
 'uvicorn>=0.20.0,<0.21.0',
 'uvloop>=0.17.0,<0.18.0']

extras_require = \
{'boto': ['boto3>=1.17.0,<2.0.0'],
 'caching': ['cashews[redis]>=5.0.0,<6.0.0'],
 'orjson': ['orjson>=3.4.7,<4.0.0'],
 'sentry': ['sentry-sdk>=0.19.5,<0.20.0'],
 'statsd': ['datadog>=0.39.0,<0.40.0'],
 'ujson': ['ujson>=5.4.0,<6.0.0']}

entry_points = \
{'console_scripts': ['sovereign = sovereign.server:main'],
 'sovereign.modifiers': ['sovereign_3rd_party_test = '
                         'sovereign.modifiers.test:Test'],
 'sovereign.sources': ['file = sovereign.sources.file:File',
                       'inline = sovereign.sources.inline:Inline']}

setup_kwargs = {
    'name': 'sovereign',
    'version': '0.17.0',
    'description': 'Envoy Proxy control-plane written in Python',
    'long_description': 'sovereign\n=========\n\nMission statement\n-----------------\nThis project implements a JSON control-plane based on the [envoy](https://envoyproxy.io) [data-plane-api](https://github.com/envoyproxy/data-plane-api)\n\nThe purpose of `sovereign` is to supply downstream envoy proxies with \nconfiguration in near-realtime by responding to discovery requests.\n\nMechanism of Operation\n----------------------\ntl;dr version:\n```\n* Polls HTTP/File/Other for data\n* (optional) Applies transforms to the data\n* Uses the data to generate Envoy configuration from templates\n```\n\nIn a nutshell, Sovereign \ngathers contextual data (*"sources"* and *"template context"*), \noptionally applies transforms to that data (using *"modifiers"*) and finally \nuses the data to generate envoy configuration from either python code, or jinja2 templates.\n\nThis is performed in a semi-stateless way, where the only state is data cached in memory.\n\nTemplate context is intended to be statically configured, whereas *Sources* \nare meant to be dynamic - for example, fetching from an API, an S3 bucket, \nor a file that receives updates.\n\n*Modifiers* can mutate the data retrieved from sources, just in case the data \nis in a less than favorable structure.\n\nBoth modifiers and sources are pluggable, i.e. it\'s easy to write your own and \nplug them into Sovereign for your use-case.\n\nCurrently, Sovereign supports only providing configuration to Envoy as JSON. \nThat is to say, gRPC is not supported yet. Contributions in this area are highly\nappreciated!\n\nThe JSON configuration can be viewed in real-time with Sovereign\'s read-only web interface.\n\nRequirements\n------------\n* Python 3.8+\n\nInstallation\n------------\n```\npip install sovereign\n```\n\nDocumentation\n-------------\n[Read the docs here!](https://vsyrakis.bitbucket.io/sovereign/docs/)\n\n:new: Read-only user interface\n------------------------\nAdded in `v0.5.3`!\n\nThis interface allows you to browse the resources currently returned by Sovereign.\n\n![Sovereign User Interface Screenshot](https://bitbucket.org/atlassian/sovereign/src/master/assets/sovereign_ui.png)\n\nLocal development\n=================\n\nRequirements\n------------\n* Docker\n* Docker-compose\n\nInstalling dependencies for dev\n-------------------------------\nI recommend creating a virtualenv before doing any dev work\n\n```\npython3 -m venv venv\nsource venv/bin/activate\npip install -r requirements-dev.txt\n```\n\nRunning locally\n---------------\nRunning the test env\n\n```\nmake run\n```\n    \nRunning the test env daemonized\n\n```\nmake run-daemon\n```\n\nPylint\n\n```\nmake lint\n```\n\nUnit tests\n\n```\nmake unit\n```\n\nAcceptance tests\n\n```\nmake run-daemon acceptance\n```\n\n\nContributors\n============\n\nPull requests, issues and comments welcome. For pull requests:\n\n* Add tests for new features and bug fixes\n* Follow the existing style\n* Separate unrelated changes into multiple pull requests\n\nSee the existing issues for things to start contributing.\n\nFor bigger changes, make sure you start a discussion first by creating\nan issue and explaining the intended change.\n\nAtlassian requires contributors to sign a Contributor License Agreement,\nknown as a CLA. This serves as a record stating that the contributor is\nentitled to contribute the code/documentation/translation to the project\nand is willing to have it used in distributions and derivative works\n(or is willing to transfer ownership).\n\nPrior to accepting your contributions we ask that you please follow the appropriate\nlink below to digitally sign the CLA. The Corporate CLA is for those who are\ncontributing as a member of an organization and the individual CLA is for\nthose contributing as an individual.\n\n* [CLA for corporate contributors](https://na2.docusign.net/Member/PowerFormSigning.aspx?PowerFormId=e1c17c66-ca4d-4aab-a953-2c231af4a20b)\n* [CLA for individuals](https://na2.docusign.net/Member/PowerFormSigning.aspx?PowerFormId=3f94fbdc-2fbe-46ac-b14c-5d152700ae5d)\n\n\nLicense\n========\n\nCopyright (c) 2018 Atlassian and others.\nApache 2.0 licensed, see [LICENSE.txt](LICENSE.txt) file.\n\n\n',
    'author': 'Vasili Syrakis',
    'author_email': 'vsyrakis@atlassian.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/sovereign/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
