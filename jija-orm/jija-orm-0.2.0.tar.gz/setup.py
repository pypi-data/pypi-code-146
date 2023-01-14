from setuptools import setup

setup(
    name='jija-orm',
    version='0.2.0',
    description='',
    packages=[
        'jija_orm',
        'jija_orm.config',
        'jija_orm.migrator',
        'jija_orm.executors',
    ],
    author='Kain',
    author_email='kainedezz.2000@gmail.com',
    zip_safe=False,

    install_requires=[
        'asyncpg==0.25.0',
        'aiofile==3.8.1'
    ]
)
