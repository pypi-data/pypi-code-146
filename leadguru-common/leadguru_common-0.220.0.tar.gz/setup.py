import json
from urllib import request
from pkg_resources import parse_version
from setuptools import setup

package_name = "leadguru_common"


def versions():
    url = f'https://pypi.python.org/pypi/{package_name}/json'
    releases = json.loads(request.urlopen(url).read())['releases']
    return sorted(releases, key=parse_version, reverse=True)


version_parts = versions()[0].split(".")
version_parts[1] = f'{float(version_parts[1]) + 1}'
last_version = ".".join(version_parts[0:-1])

setup(name=package_name,
      version=f'{last_version}',
      description='LGT common builds',
      packages=['lgt'],
      include_package_data=True,
      install_requires=[
          'wheel',
          'google-cloud-pubsub==2.3.0',
          'google-cloud-storage==1.37.0',
          'requests',
          'aiohttp',
          'websockets',
          'loguru==0.2.4',
          'pydantic',
          'leadguru-data>=0.60.0',
          'pydantic==1.8.1',
          'pytz'
      ],
      author_email='developer@leadguru.co',
      zip_safe=False)
