import re

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

VERSION_FILE="bfgsupport/_version.py"
with open(VERSION_FILE, 'r') as f_version:
    version_string = f_version.read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, version_string, re.M)
if mo:
    version_string = mo.group(1)
else:
    raise RuntimeError(f'Unable to find version string in {VERSION_FILE}.')


setup_args = dict(
    name='bfgsupport',
    version=version_string,
    description='"""A collection of modules that supports dealing and bidding in Bid for Game applications."""',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='jeff watkins',
    author_email='support@bidforgame.com',
    keywords=['Application, User'],
    url='https://psionman@bitbucket.org/psionman/bfgsupport.git',
    download_url='https://pypi.org/project/bfgsupport/',
)

install_requires = [
    'username', 'nose', 'pytest'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)