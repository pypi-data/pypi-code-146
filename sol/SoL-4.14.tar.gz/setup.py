# -*- coding: utf-8 -*-
# :Project:   SoL
# :Created:   sab 27 set 2008 10:57:57 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2008–2010, 2013–2018, 2020, 2021, 2023 Lele Gaifax
#

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.rst'), encoding='utf-8') as f:
    CHANGES = f.read()
with open(os.path.join(here, 'version.txt'), encoding='utf-8') as f:
    VERSION = f.read().strip()

requires = [
    'alembic',
    'babel',
    'metapensiero.extjs.desktop',
    'metapensiero.sqlalchemy.proxy',
    'pillow',
    'pycountry',
    'pygal',
    'pygal-maps-world',
    'pynacl',
    'pyramid',
    'pyramid-mako',
    'pyramid-tm',
    'python-rapidjson',
    'reportlab',
    'ruamel.yaml',
    'setuptools',
    'sqlalchemy',
    'transaction',
    'waitress',
    'zope.sqlalchemy',
    ]

setup(
    name='SoL',
    version=VERSION,
    description="Carrom tournaments management",
    long_description=README + '\n\n' + CHANGES,
    long_description_content_type='text/x-rst',

    author="Lele Gaifax",
    author_email="lele@metapensiero.it",
    url="https://gitlab.com/metapensiero/SoL",

    license="GPLv3+",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: JavaScript",
        "Operating System :: OS Independent",
        "Framework :: Pyramid",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved ::"
        " GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Natural Language :: Italian",
        "Topic :: Games/Entertainment",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Development Status :: 5 - Production/Stable",
    ],
    keywords='web, wsgi, pyramid, carrom, tournaments, swiss system, knockout system',

    packages=['alembic'] + find_packages('src'),
    package_dir={'': 'src',
                 'alembic': 'alembic'},

    include_package_data=True,

    zip_safe=False,
    install_requires=requires,

    entry_points="""\
    [paste.app_factory]
    main = sol:main

    [console_scripts]
    soladmin = sol.scripts.admin:main
    """,
)
