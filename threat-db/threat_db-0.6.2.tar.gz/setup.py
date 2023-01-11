# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['threat_db']

package_data = \
{'': ['*']}

install_requires = \
['flask-jwt-extended>=4.4.4,<5.0.0',
 'flask>=2.2.2,<3.0.0',
 'gql[all]>=3.4.0,<4.0.0',
 'grpcio>=1.51.1,<2.0.0',
 'itsdangerous>=2.1.2,<3.0.0',
 'orjson>=3.8.3,<4.0.0',
 'packageurl-python>=0.10.4,<0.11.0',
 'protobuf==3.20.1',
 'pydgraph>=21.3.2,<22.0.0',
 'rich>=12.6.0,<13.0.0',
 'uwsgi>=2.0.21,<3.0.0']

entry_points = \
{'console_scripts': ['threat_db = threat_db.cli:main',
                     'threat_db_admin = threat_db.admincli:main']}

setup_kwargs = {
    'name': 'threat-db',
    'version': '0.6.2',
    'description': 'A graphql server for vulnerabilities powered by dgraph',
    'long_description': '# Introduction\n\nThreatDB is a graph database for application components and vulnerabilities powered by dgraph. Currently, CycloneDX 1.4 SBoM and VEX files could be imported and queried with this project.\n\n## Development setup\n\n```\ngit clone https://github.com/ngcloudsec/threat-db.git\ncd threat-db\nmkdir -p $HOME/dgraph $HOME/threatdb_data_dir\ndocker compose up\n```\n\nThis would start a threat db api server (PORT: 9000) and an instance of [dgraph](https://dgraph.io) standalone (PORTS: 8080, 9080).\n\n## Create schemas\n\nTo create the schemas and the first administrator user.\n\n```\ngit clone https://github.com/ngcloudsec/threat-db.git\npip install poetry\npoetry install\nexport DGRAPH_API_KEY=changeme\npoetry run threat_db_admin --init --dgraph-host localhost:9080 --graphql-host http://localhost:8080/graphql\npoetry run threat_db_admin --create-root-user --dgraph-host localhost:9080 --graphql-host http://localhost:8080/graphql\n```\n\nCopy the user id and password from the logs.\n\n## Import data\n\n```\nmkdir -p $HOME/threatdb_data_dir\nthreat_db --data-dir $HOME/threatdb_data_dir\n```\n\nWhen invoked with docker compose, any .vex.json files present in the directory `THREATDB_DATA_DIR` would be imported automatically. For testing purposes, you can download some sample VEX files from [here](https://github.com/ngcloudsec/images-info/actions/workflows/build.yml)\n\n## Rest API\n\n### Generate access token\n\n```\ncurl -X POST http://0.0.0.0:9000/login -d "username=user id&password=password" -H "Content-Type: application/json"\n```\n\nUseful one-liner for automation\n\n```\nexport ACCESS_TOKEN=$(curl -X POST http://0.0.0.0:9000/login -d \'{"username":"username","password":"password"}\' -H "Content-Type: application/json" | jq -r \'.access_token\')\n```\n\n```\ncurl http://0.0.0.0:9000/healthcheck\n```\n\n### whoami\n\n```\ncurl http://0.0.0.0:9000/whoami -H "Authorization: Bearer $ACCESS_TOKEN"\n```\n\n### Import data\n\n```\ncurl -F \'file=@/tmp/bom.json\' http://0.0.0.0:9000/import -H "Authorization: Bearer $ACCESS_TOKEN"\n```\n\n## Cloud Setup\n\nRefer to the instructions under [contrib](contrib/microk8s/INSTALL.md) to setup a microk8s cluster with threat-db and dgraph.\n\n## Discord support\n\nThe developers could be reached via the [discord](https://discord.gg/DCNxzaeUpd) channel.\n',
    'author': 'Team ngcloudsec',
    'author_email': 'cloud@ngcloud.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': '',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
