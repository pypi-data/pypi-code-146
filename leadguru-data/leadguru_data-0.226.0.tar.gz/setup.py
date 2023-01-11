import json
from urllib import request
from pkg_resources import parse_version
from setuptools import setup

package_name = "leadguru_data"

def versions():
    url = f'https://pypi.python.org/pypi/{package_name}/json'
    releases = json.loads(request.urlopen(url).read())['releases']
    return sorted(releases, key=parse_version, reverse=True)

version_parts = versions()[0].split(".")
version_parts[1] = f'{float(version_parts[1]) + 1}'
last_version = ".".join(version_parts[0:-1])

setup(name=package_name,
      version=f'{last_version}',
      description='LGT data builds',
      packages=['lgt_data'],
      include_package_data=True,
      install_requires=[
          'wheel',
          'pymongo',
          'python-dateutil',
          'nameparser',
          'mongoengine'
      ],
      author_email='developer@leadguru.co',
      zip_safe=False)

