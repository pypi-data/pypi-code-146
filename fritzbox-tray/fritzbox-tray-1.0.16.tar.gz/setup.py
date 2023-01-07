import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                       'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='fritzbox-tray',
    version='1.0.16',
    includepackagedata=True,
    # packages=find_packages(exclude=("tests",)),
    packages=['src.fritzbox_tray'],
    description='A system tray application for interacting with FRITZ!Box devices',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['fritz', 'fritzbox', 'fritzbox-tray', 'fritzbox_tray', 'tray'],
    author='Andreas Violaris',
    url='https://github.com/aviolaris/fritzbox-tray',
    license='GPLv3',
    # packages=find_packages(where='src'),
    package_data={'': ['ft.ico']},
    install_requires=["certifi", "charset-normalizer", "idna", "Pillow", "pystray", "requests", "six", "urllib3"],
    # extras_require={
    #     'dev': ['tox', 'pytest'],
    # },
    entry_points={
        'gui_scripts': [
            'fritzbox-tray=fritzbox_tray.__main__:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
)
