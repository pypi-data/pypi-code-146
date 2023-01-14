# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pydiverse',
 'pydiverse.pipedag',
 'pydiverse.pipedag.backend',
 'pydiverse.pipedag.backend.table',
 'pydiverse.pipedag.backend.table.util',
 'pydiverse.pipedag.context',
 'pydiverse.pipedag.core',
 'pydiverse.pipedag.engine',
 'pydiverse.pipedag.errors',
 'pydiverse.pipedag.materialize',
 'pydiverse.pipedag.materialize.util',
 'pydiverse.pipedag.util']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.39,<2.0.0',
 'attrs>=22.1.0',
 'contextvars>=2.4',
 'msgpack>=1.0.4',
 'networkx>=2.8',
 'packaging>=21.3',
 'pandas>=1.4.3,<2.0.0',
 'pynng>=0.7.1',
 'python-box>=6.1.0',
 'structlog>=22.1.0',
 'tomli>=2.0.1',
 'typing-extensions>=4.1.0,<5']

extras_require = \
{'docs': ['Sphinx>=5.1.1',
          'sphinx-rtd-theme>=1.0.0',
          'sphinxcontrib-apidoc>=0.3.0'],
 'filelock': ['filelock>=3.7.1'],
 'ibm-db2': ['ibm-db>=3.1.4', 'ibm-db-sa>=0.3.8'],
 'mssql': ['pyodbc>=4.0.35', 'pytsql>=1.1.4'],
 'prefect': ['prefect>=1.3,<2'],
 'zookeeper': ['kazoo>=2.8.0']}

setup_kwargs = {
    'name': 'pydiverse-pipedag',
    'version': '0.2.0',
    'description': 'A pipeline orchestration library executing tasks within one python session. It takes care of SQL table (de)materialization, caching and cache invalidation. Blob storage is supported as well for example for storing model files.',
    'long_description': '# pydiverse.pipedag\n\n[![CI](https://github.com/pydiverse/pydiverse.pipedag/actions/workflows/ci.yml/badge.svg)](https://github.com/pydiverse/pydiverse.pipedag/actions/workflows/ci.yml)\n\nA pipeline orchestration library executing tasks within one python session. It takes care of SQL table\n(de)materialization, caching and cache invalidation. Blob storage is supported as well for example\nfor storing model files.\n\nThis is an early stage version 0.x which lacks documentation. Please contact\nhttps://github.com/orgs/pydiverse/teams/code-owners if you like to become an early adopter\nor to contribute early stage usage examples.\n\n## Usage\n\npydiverse.pipedag can either be installed via pypi with `pip install pydiverse-pipedag` or via conda-forge\nwith `conda install pydiverse-pipedag -c conda-forge`.\n\n## Example\n\nA flow can look like this (i.e. put this in a file named `run_pipeline.py`):\n\n```python\nfrom pydiverse.pipedag import materialize, Table, Flow, Stage\nimport sqlalchemy as sa\nimport pandas as pd\n\nfrom pydiverse.pipedag.context import StageLockContext, RunContext\nfrom pydiverse.pipedag.util import setup_structlog\n\n\n@materialize(lazy=True)\ndef lazy_task_1():\n    return sa.select([sa.literal(1).label("x"), sa.literal(2).label("y")])\n\n\n@materialize(lazy=True, input_type=sa.Table)\ndef lazy_task_2(input1: sa.Table, input2: sa.Table):\n    query = sa.select([(input1.c.x * 5).label("x5"), input2.c.a]).select_from(\n        input1.outerjoin(input2, input2.c.x == input1.c.x)\n    )\n    return Table(query, name="task_2_out", primary_key=["a"])\n\n\n@materialize(lazy=True, input_type=sa.Table)\ndef lazy_task_3(input: sa.Table, my_stage: Stage):\n    return sa.text(f"SELECT * FROM {my_stage.transaction_name}.{input.name}")\n\n\n@materialize(lazy=True, input_type=sa.Table)\ndef lazy_task_4(input: sa.Table, prev_stage: Stage):\n    return sa.text(f"SELECT * FROM {prev_stage.name}.{input.name}")\n\n\n@materialize(nout=2, version="1.0.0")\ndef eager_inputs():\n    dfA = pd.DataFrame(\n        {\n            "a": [0, 1, 2, 4],\n            "b": [9, 8, 7, 6],\n        }\n    )\n    dfB = pd.DataFrame(\n        {\n            "a": [2, 1, 0, 1],\n            "x": [1, 1, 2, 2],\n        }\n    )\n    return Table(dfA, "dfA"), Table(dfB, "dfB_%%")\n\n\n@materialize(version="1.0.0", input_type=pd.DataFrame)\ndef eager_task(tbl1: pd.DataFrame, tbl2: pd.DataFrame):\n    return tbl1.merge(tbl2, on="x")\n\n\ndef main():\n    with Flow() as f:\n        with Stage("stage_1"):\n            lazy_1 = lazy_task_1()\n            a, b = eager_inputs()\n\n        with Stage("stage_2") as stage2:\n            lazy_2 = lazy_task_2(lazy_1, b)\n            lazy_3 = lazy_task_3(lazy_2, stage2)\n            eager = eager_task(lazy_1, b)\n\n        with Stage("stage_3"):\n            lazy_4 = lazy_task_4(lazy_2, stage2)\n        _ = lazy_3, lazy_4, eager  # unused terminal output tables\n\n    # Run flow\n    result = f.run()\n    assert result.successful\n\n    # Run in a different way for testing\n    with StageLockContext():\n        result = f.run()\n        assert result.successful\n        assert result.get(lazy_1, as_type=pd.DataFrame)["x"][0] == 1\n\n\nif __name__ == "__main__":\n    # initialize logging\n    setup_structlog()\n    main()\n```\n\nCreate a file called `pipedag.yaml` in the same directory:\n\n```yaml\nname: pipedag_tests\ntable_store_connections:\n  postgres:\n    # Postgres: this can be used after running `docker-compose up`\n    url: "postgresql://{$POSTGRES_USERNAME}:{$POSTGRES_PASSWORD}@127.0.0.1:6543/{instance_id}"\n\ninstances:\n  __any__:\n    # listen-interface for pipedag context server which synchronizes some task state during DAG execution\n    network_interface: "127.0.0.1"\n    # classes to be materialized to table store even without pipedag Table wrapper (we have loose coupling between\n    # pipedag and pydiverse.transform, so consider adding \'pydiverse.transform.Table\' in your config)\n    auto_table: ["pandas.DataFrame", "sqlalchemy.sql.elements.TextClause", "sqlalchemy.sql.selectable.Selectable"]\n    fail_fast: true\n\n    instance_id: pipedag_default\n    table_store:\n      class: "pydiverse.pipedag.backend.table.SQLTableStore"\n\n      # Postgres: this can be used after running `docker-compose up`\n      table_store_connection: postgres\n      create_database_if_not_exists: True\n\n      # print select statements before being encapsualted in materialize expressions and tables before writing to\n      # database\n      print_materialize: true\n      # print final sql statements\n      print_sql: true\n\n    blob_store:\n      class: "pydiverse.pipedag.backend.blob.FileBlobStore"\n      base_path: "/tmp/pipedag/blobs"\n\n    lock_manager:\n      class: "pydiverse.pipedag.backend.lock.ZooKeeperLockManager"\n      hosts: "localhost:2181"\n\n    orchestration:\n      class: "pydiverse.pipedag.engine.SequentialEngine"\n```\n\nIf you don\'t have a postgres, Microsoft SQL Server, or IBM DB2 database at hand, you can\nstart a postgres database with the following `docker-compose.yaml` file:\n\n```yaml\nversion: "3.9"\nservices:\n  postgres:\n    image: postgres\n    environment:\n      POSTGRES_USER: sa\n      POSTGRES_PASSWORD: Pydiverse23\n      POSTGRES_PORT: 6543\n    ports:\n      - 6543:5432\n  zoo:\n    image: zookeeper\n    environment:\n      ZOO_4LW_COMMANDS_WHITELIST: ruok\n    ports:\n      - 2181:2181\n```\n\nRun `docker-compose up` in the directory of your `docker-compose.yaml` and then execute\nthe flow script as follows with a shell like `bash` and a python environment that\nincludes `pydiverse-pipedag`, `pandas`, and `sqlalchemy`:\n\n```bash\nexport POSTGRES_USERNAME=sa\nexport POSTGRES_PASSWORD=Pydiverse23\npython run_pipeline.py\n```\n\nFinally, you may connect to your localhost postgres database `pipedag_default` and\nlook at tables in schemas `stage_1`..`stage_3`.\n\nIf you don\'t have a SQL UI at hand, you may use `psql` command line tool inside the docker container.\nCheck out the `NAMES` column in `docker ps` output. If the name of your postgres container is\n`example_postgres_1`, then you can look at output tables like this:\n\n```bash\ndocker exec example_postgres_1 psql --username=sa --dbname=pipedag_default -c \'select * from stage_1.dfa;\'\n```\n\nOr more interactively:\n\n```bash\ndocker exec -t -i example_postgres_1 bash\npsql --username=sa --dbname=pipedag_default\n\\dt stage_*.*\nselect * from stage_2.task_2_out;\n```\n\n## Troubleshooting\n\n### Installing mssql odbc driver for linux\n\nInstalling with\ninstructions [here](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver16#suse18)\nworked.\nBut `odbcinst -j` revealed that it installed the configuration in `/etc/unixODBC/*`. But conda installed pyodbc brings\nits own `odbcinst` executable and that shows odbc config files are expected in `/etc/*`. Symlinks were enough to fix the\nproblem. Try `python -c \'import pyodbc;print(pyodbc.drivers())\'` and see whether you get more than an empty list.\nFurthermore, make sure you use 127.0.0.1 instead of localhost. It seems that /etc/hosts is ignored.\n',
    'author': 'QuantCo, Inc.',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
