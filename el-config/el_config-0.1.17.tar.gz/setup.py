# -*- coding: utf-8 -*-

from setuptools import setup
from distutils.util import convert_path


_package_name = 'el_config'

_namespace_dict = {}
_version_path = convert_path(f'{_package_name}/__version__.py')
with open(_version_path) as _version_file:
    exec(_version_file.read(), _namespace_dict)
_package_version = _namespace_dict['__version__']

setup(
    name = _package_name,
    packages = [_package_name],
    version = f"{_package_version}",
    license='MIT',
    description = 'Python-box based custom config package for python projects.',
    long_description = open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    author = 'Batkhuu Byambajav',
    author_email = 'batkhuu@ellexi.com',
    url = 'https://bitbucket.org/ellexiinc/el_config/',
    download_url = f'https://bitbucket.org/ellexiinc/el_config/get/release-{_package_version}.tar.gz',
    keywords = [_package_name, 'config', 'configs', 'python-box', 'custom-config'],
    install_requires = [
            'el-validator>=0.1.12',
            'python-box[PyYAML]>=5.4.1'
        ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
)
