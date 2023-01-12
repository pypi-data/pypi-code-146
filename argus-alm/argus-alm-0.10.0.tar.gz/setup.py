# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['argus',
 'argus.backend',
 'argus.backend.controller',
 'argus.backend.events',
 'argus.backend.models',
 'argus.backend.plugins',
 'argus.backend.plugins.driver_matrix_tests',
 'argus.backend.plugins.sct',
 'argus.backend.service',
 'argus.backend.util',
 'argus.client',
 'argus.client.driver_matrix_tests',
 'argus.client.sct',
 'argus.db']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'scylla-driver>=3.24.8,<4.0.0']

setup_kwargs = {
    'name': 'argus-alm',
    'version': '0.10.0',
    'description': 'Argus',
    'long_description': '# Argus\n\n## Description\n\nArgus is a test tracking system intended to provide observability into automated test pipelines which use long-running resources. It allows observation of a test status, its events and its allocated resources. It also allows easy comparison between particular runs of a specific test.\n\n## Installation notes\n\n### Prerequisites\n\n- Python >=3.10.0 (system-wide or pyenv)\n\n- NodeJS >=16 (with npm)\n\n- Yarn (can be installed globally with `npm -g install yarn`)\n\n- nginx\n\n- poetry >=1.2.0b1\n\n### From source\n\n#### Production\n\nPerform the following steps:\n\nCreate a user that will be used by uwsgi:\n\n```bash\nuseradd -m -s /bin/bash argus\nsudo -iu argus\n```\n\n(Optional) Install pyenv and create a virtualenv for this user:\n\n```bash\npyenv install 3.10.0\npyenv virtualenv argus\npyenv activate argus\n```\n\nClone the project into a directory somewhere where user has full write permissions\n\n```bash\ngit clone https://github.com/scylladb/argus ~/app\ncd ~/app\n```\n\nInstall project dependencies:\n\n```bash\npoetry install --with default,dev,web-backend,docker-image\nyarn install\n```\n\nCompile frontend files from `/frontend` into `/public/dist`\n\n```bash\nyarn webpack\n```\n\nCreate a `argus.local.yaml` configuration file (used to configure database connection) and a `argus_web.yaml` (used for webapp secrets) in your application install directory.\n\n```bash\ncp argus_web.example.yaml argus_web.yaml\ncp argus.yaml argus.local.yaml\n```\n\nOpen `argus.local.yaml` and add the database connection information (contact_points, user, password and keyspace name).\n\nOpen `argus_web.yaml` and change the `SECRET_KEY` value to something secure, like a sha512 digest of random bytes. Fill out GITHUB_* variables with their respective values.\n\nCopy nginx configuration file from `docs/configs/argus.nginx.conf` to nginx virtual hosts directory:\n\nUbuntu:\n\n```bash\nsudo cp docs/configs/argus.nginx.conf /etc/nginx/sites-available/argus\nsudo ln -s /etc/nginx/sites-enabled/argus /etc/nginx/sites-available/argus\n```\n\nRHEL/Centos/Alma/Fedora:\n\n```bash\nsudo cp docs/configs/argus.nginx.conf /etc/nginx/conf.d/argus.conf\n```\n\nAdjust the webhost settings in that file as necessary, particularly `listen` and `server_name` directives.\n\nCopy systemd service file from `docs/config/argus.service` to `/etc/systemd/system` directory:\n\n```bash\nsudo cp docs/config/argus.service /etc/systemd/system\n```\n\nOpen it and adjust the path to the `start_argus.sh` script in the `ExecStart=` directive and the user/group, then reload systemd daemon configuration and enable (and optionally start) the service.\n\nWARNING: `start_argus.sh` assumes pyenv is installed into `~/.pyenv`\n\n```bash\nsudo systemctl daemon-reload\nsudo systemctl enable --now argus.service\n```\n\n#### Development\n\nClone the project into a directory somewhere\n\n```bash\ngit clone https://github.com/scylladb/argus\ncd argus\n```\n\nInstall project dependencies:\n\n```bash\npoetry install --with default,dev,web-backend,docker-image\nyarn install\n```\n\nCompile frontend files from `/frontend` into `/public/dist`. Add --watch to recompile files on change.\n\n```bash\nyarn webpack --watch\n```\n##### Configuration\nCreate a `argus.local.yaml` configuration file (used to configure database connection) and a `argus_web.yaml` (used for webapp secrets) in your application install directory.\n\nSee `Production` section for more details.\nTo configure Github authentication follow steps:\n1. Authorize OAuth App\n   1. go to your Account Settings (top right corner) -> Developer settings (left pane) -> OAuth Apps\n   2. Click Create New OAuth App button\n   3. Fill the fields (app name: `argus-dev`, homepage URL `http://localhost:5000`, Auth callback URL: `http://localhost:5000/profile/oauth/github`)\n   4. Confirm and get the tokens/ids required for config\n2. Create Jenkins token for your account\n   1. Go to `Configure` in top right corner\n   2. Click `Add new Token`\n   3. Get it and paste to config to `JENKINS_API_TOKEN` param\n##### Database Initialization\n\nYou can initialize a scylla cluster in any way you like, either using docker image with docker-compose or using cassandra cluster manager. You will need to create the keyspace manually before you can sync database models.\n\nCreate keyspace according to your configuration.\ne.g. (need to test if it works with RF=1 if not, make it 3)\n```\nCREATE KEYSPACE argus WITH replication = {\'class\': \'SimpleStrategy\', \'replication_factor\' : 1}\n```\n\nInitial sync can be done as follows:\n\n```py\nfrom argus.backend.db import ScyllaCluster\nfrom argus.db.testrun import TestRun\ndb = ScyllaCluster.get()\n\ndb.sync_models() # Syncronizes Object Mapper models\nTestRun.init_own_table() # Syncronizes TestRun table (separate from python-driver Object Mapper)\n\n```\n\nYou can also use `flask sync-models` afterwards during development when making small changes to models.\n\nIt is recommended to set up jenkins api key and run `flask scan-jenkins` afterwards to get basic release/group/test structure.\n\nThere are scripts in `./scripts` directory that can be used to download data from production, upload them into your dev db and fix their relations to other models in your instance of the application. Specifically, `download_runs_from_prod.py` requires additional config, `argus.local.prod.yaml` which is the config used to connect to the production cluster. The scripts are split to prevent mistakes and accidentally affecting production cluster.\n\n##### Configuration\n\nCreate a `argus.local.yaml` configuration file (used to configure database connection) and a `argus_web.yaml` (used for webapp secrets) in your application install directory.\n\n```bash\ncp argus_web.example.yaml argus_web.yaml\ncp argus.yaml argus.local.yaml\n```\n\nOpen `argus.local.yaml` and add the database connection information (contact_points, user, password and keyspace name).\n\nOpen `argus_web.yaml` and change the `SECRET_KEY` value to something secure, like a sha512 digest of random bytes. Fill out GITHUB_* and JENKINS_* variables with their respective values.\n\nRun the application from CLI using:\n\n```bash\nFLASK_ENV="development" FLASK_APP="argus_backend:start_server" FLASK_DEBUG=1 CQLENG_ALLOW_SCHEMA_MANAGEMENT=1 flask run\n```\n\nOmit `FLASK_DEBUG` if running your own debugger (pdb, pycharm, vscode)\n',
    'author': 'Alexey Kartashov',
    'author_email': 'alexey.kartashov@scylladb.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/scylladb/argus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
