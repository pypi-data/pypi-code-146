# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['dbtool']
install_requires = \
['dbutils']

setup_kwargs = {
    'name': 'dbtool',
    'version': '0.2.0',
    'description': 'A lightweight db tools for sql.',
    'long_description': "#  dbtool\nA lightweight db tools for sql.\n\n```\npip install dbtool\n```\n\n```\n# sqlite3 ....\ndb = dbtool.connect('sqlite:///:memory:')\ndb = dbtool.connect('mysql://root:123456@127.0.0.1:3306/test',  mincached=1, maxconnections=20)\n\n# sql\ndb.execute(sql)\ndb.execute_fetchone(sql)\ndb.execute_cursor(sql)\ndb.execute_batch(sql)\ndb.execute_script(sql)\n\n# crud\ndb.insert(user)\ndb.update(user)\ndb.delete(User, {'id': 1})\ndb.find(User, {'status': 1})\ndb.find_one(User, {'id': 1})\ndb.find_count(User, {'status': 1})\n\n# transactions\nwith db.transaction():\n    db.execute(sql1)\n\n```\n\ndb vs driver\n\n- sqlite - sqlite3\n- mysql - pymysql\n- postgresql - psycopg2\n- sqlserver - pymssql",
    'author': 'Mario Luo',
    'author_email': 'luokaiqiongmou@foxmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
