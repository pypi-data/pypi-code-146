# Copyright (C) 2022 Indoc Research
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# read the contents of your README file
from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text()

setuptools.setup(
    name='pilot-platform-common',
    version='0.2.0',
    author='Indoc Research',
    author_email='etaylor@indocresearch.org',
    description='Generates entity ID and connects with Vault (secret engine) to retrieve credentials',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'python-dotenv==0.19.1',
        'httpx==0.23.0',
        'aioredis>=2.0.0,<3.0.0',
        'aioboto3==9.6.0',
        'xmltodict==0.13.0',
        'minio==7.1.8',
        'python-json-logger==2.0.2',
    ],
    include_package_data=True,
    package_data={
        '': ['*.crt'],
    },
)
