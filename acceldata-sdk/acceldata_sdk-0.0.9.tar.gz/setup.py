from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3'
]

# description = None
# try:
#     import pypandoc
#     description = pypandoc.convert('README.md', 'rst')
# except (IOError, ImportError):
#     description = open('README.md').read()

# Change MIN_TORCH_BACKEND_VERSION_SUPPORTED in constants as well if needed while updating version here

setup(
    name='acceldata_sdk',
    version='0.0.9',
    description='Acceldata SDK.' + '\n\n' + open('README.txt').read(),
    long_description=open('README.md').read() + '\n\n' + open('DATASOURCE_README.md').read() + '\n\n'  + open('CHANGELOG.txt').read(),
    long_description_content_type="text/markdown",
    url='',
    author='acceldata',
    author_email='apisupport@acceldata.io',
    license='MIT License',
    classifiers=classifiers,
    keywords='acceldata-sdk',
    packages=find_packages(),
    install_requires=['requests', 'dataclasses', 'typing', 'requests-toolbelt', 'semantic-version']
)
