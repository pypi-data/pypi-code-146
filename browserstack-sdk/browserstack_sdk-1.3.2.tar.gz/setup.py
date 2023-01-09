from os.path import abspath, join, dirname
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open(join(dirname(abspath(__file__)), 'LICENSE.txt'), encoding='utf8') as f:
    LICENSE = f.read()

# this provides the __version__ attribute at setup.py run time
exec(open('browserstack_sdk/_version.py').read())

setup(
    name='browserstack_sdk',
    packages=['browserstack_sdk'],
    version=__version__,
    description='Python SDK for browserstack selenium-webdriver tests',
    long_description='Python SDK for browserstack selenium-webdriver tests',
    author='BrowserStack',
    author_email='support@browserstack.com',
    keywords=['browserstack', 'selenium', 'python'],
    classifiers=[],
    install_requires=[
        'psutil',
        'pyyaml',
        'browserstack-local',
        'packaging',
        'requests',
        'requests_toolbelt'
    ],
    license=LICENSE,
    package_data={'': ['browserstack.generic.yml.sample', 'browserstack.framework.yml.sample']},
    include_package_data=True,
    entry_points = {'console_scripts': ['browserstack-sdk = browserstack_sdk.__init__:run_on_browserstack']}
)
