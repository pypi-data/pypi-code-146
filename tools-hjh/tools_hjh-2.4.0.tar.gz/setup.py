from setuptools import setup

setup (
    name='tools_hjh',
    version='2.4.0',
    author='HuaJunhao',
    author_email='huajunhao6@yeah.net',
    install_requires=[
          'dbutils'
        # , 'pillow'
        , 'pymysql'
        , 'cx_Oracle'
        , 'paramiko'
        # , 'zipfile36'
        # , 'crypto'
        , 'requests'
        # , 'selenium'
    ],
    packages=['tools_hjh']
)
