# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['scup']
setup_kwargs = {
    'name': 'scup',
    'version': '0.4.4',
    'description': 'SCUP as in SQL Covertor Utility Program',
    'long_description': 'Note: This utility is currently more suitable to be used in a notebook settings, as it will prompt user for input. A Version more fir to be used in programming will soon be released.\n\nI was recently doing an online training, the instructor was showing examples on MySQL database. I however preferred running those exampkes on my test database i.e. MS SQL Server on Azure Cloud. \n\nAfter a few classes i realized that MYSQL has host of simple to understand SQL queries, where as its SQL server equivalent was big chunky queries.\n(I am talking about system SQL query which you run against the metdata such as SHOW TABLES, SHOW DATABASE etc)\n\nwith this idea i have created this utility to provide syntax to some imp queries, which we are required to run every now and then.\n\nrun [print(scup.sqlserver(\'list\'))] to see a complete list queries, this utility support.\n\nversion = "0.4.4" -->  Added Query 9, and added header to 1,2,3 and 9 query\n\nversion = "0.4.3" --> Added header to #3 and #6 query , # more details \n\nversion = "0.4.2" --> Bug - List command but erroring - local variable \'ssquery\' referenced before assignment\n\nversion = "0.4.1" --> fixed a small bug, nevermind :)\n\nversion = "0.4.0" --> Added option to call queries by numbers\n\nversion = "0.3.0" --> Changed scup.py function ms2ssf() name to sqlserver(). added many other sqls.\n\nversion = "0.2.3" --> Package Name changed from MSS to SCUP as pypi showed conflict. (SCUP as in SQL Covertor Utility Program)\n\nversion = "0.2.2" --> List command added and reponse to no query match added\n\nversion = "0.2.0" --> 3 Show commands working\n\nversion = "0.2.1" --> Patch - test scripts was commented out\n\n--------------------------------------------------------------------------------------------------\n\nCOMMANDS HELP  ()\n\n        1. SHOW DATABASES (conn.execute(scup.sqlserver(\'SHOW DATABASES\')).fetchall())\n        2. SHOW TABLES : will prompt for Schema name\n        3. SHOW TABLES FROM database_name : will prompt for Database name\n        4. SHOW CHECK_CONSTRAINTS FROM TABLE : will prompt for Table Name (uses LIKE)\n        5. DESCRIBE TABLE  : will prompt for Database name\n        6. SHOW INDEX FROM TABLE  : will prompt for Schema and Table name\n        7. DATABASE STATUS  : will prompt for Database name \n        8. SHOW VIEWS : will prompt for Schema name',
    'author': 'Akansha K',
    'author_email': 'akanshakaushik0995@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
