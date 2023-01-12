from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='provider-switch',
    version='0.0.20',
    description='provider-switch',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Tai Nguyen',
    author_email='tai.nguyen@hiip.asia',
    keywords=['Python 3'],
    download_url='https://pypi.org/project/provider-switch/'
)

install_requires = [
    'boto3'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
