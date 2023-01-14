from pathlib import Path

from setuptools import find_packages, setup

from pytest_ver.lib.constants import Constants

mod_name = 'pytest_ver'
this_directory = Path(__file__).parent
long_desc = (this_directory / 'README.md').read_text()
long_version = Constants.version.replace('.', '_')

setup(
    name=mod_name,
    include_package_data=True,
    packages=find_packages(include=f'{mod_name}*', ),
    version=Constants.version,
    license='MIT',
    description='Pytest module with Verification Protocol, Verification Report and Trace Matrix',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    author='JA',
    author_email='cppgent0@gmail.com',
    url=f'https://github.com/cppgent0/{mod_name}',
    download_url=f'https://github.com/cppgent0/{mod_name}/archive/refs/tags/v_{long_version}.tar.gz',
    keywords=['verification', 'pytest'],
    install_requires=[
        'docx',
        'jsmin',
        'pytest',
        'pytest-check',
        'python-docx',
        'reportlab',
    ],
    classifiers=[
        # Choose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing :: Acceptance',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
)

print('OK   GenBuildInfo completed successfully')
