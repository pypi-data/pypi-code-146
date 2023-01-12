# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fish_databricks_jobs', 'fish_databricks_jobs.services']

package_data = \
{'': ['*']}

install_requires = \
['databricks-cli>=0.17.0,<0.18.0',
 'tabulate>=0.9.0,<0.10.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['fish-databricks-jobs = fish_databricks_jobs.cli:app',
                     'jobser = fish_databricks_jobs.cli:app']}

setup_kwargs = {
    'name': 'fish-databricks-jobs',
    'version': '0.7.6',
    'description': 'cli and sdk to manage Jobs in Databricks',
    'long_description': "# fish-databricks-jobs \n\nfish-databricks-jobs is cli and python sdk to manage Jobs for Databricks. e.g assign permissions to multiple jobs. User can filter jobs by job name or tags.  \n\nThe functionality of current [databricks-cli(v0.17.4)](https://pypi.org/project/databricks-cli/) is limited on the `jobs` api. e.g it can not assign job permission.\n\nWith `fish-databricks-jobs`, you can assign job permission, e.g: \n\nto assign group `mygroup` with permission `can_manage` to job by filter `843966944901662`(job_id) \n```angular2html\n$ fish-databricks-jobs permission-assign mygroup --type group --level can_manage --filter 843966944901662\n```\n# Requirements\n- Python Version >= 3.7 \n# Installation\n```\n$ pip install --upgrade fish-databricks-jobs\n```\n```angular2html\n$ fish-databricks-jobs --version\nVersion: 0.6.8\n```\n# Usage\n### permission-assign\n```\n$ fish-databricks-jobs permission-assign -h\n\n Usage: fish-databricks-jobs permission-assign [OPTIONS] NAME\n\n Assign permission to user\n\n╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────╮\n│ *    name      TEXT  User name, group name or serive principal id. Who will receive the permisssion. [default: None]    │\n│                      [required]                                                                                         │\n╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\n╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────╮\n│    --type     -t      [user|principal|group]                Permission receiver type. [default: user]                   │\n│ *  --level    -l      [can_view|can_manage|can_manage_run]  Permission level. [default: None] [required]                │\n│    --filter   -f      TEXT                                  filter jobs, case insensitively. [default: None]            │\n│    --profile  -p      TEXT                                  profile name in ~/.databrickscfg [default: DEFAULT]         │\n│    --force                                                  Attempt to assign permission without prompting for          │\n│                                                             confirmation. **Use this flag with caution**                │\n│    --help     -h                                            Show this message and exit.                                 │\n╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\n```\n### use as sdk to list jobs\n```angular2html\nfrom fish_databricks_jobs.services.jobs import JobsService, Job\nhost, token = 'https://example.cloud.databricks.com','exampletokenc0e27d8b91fd8c0144f0a23'\njob_list = JobsService(host, token).list()\ndf = spark.createDataFrame(job_list)\n\ndisplay(df)\n```\n# Config authentication\nfish-databricks-jobs uses same config file as `databricks-cli`. e.g.`~/.databrickscfg` for macOS. Similar for Windows.\n```\n[DEFAULT]\nhost = https://example.cloud.databricks.com\ntoken = exampletokenc0e27d8b91fd8c0144f0a23\n```\n\n\n\n",
    'author': 'Tim Chen',
    'author_email': 'firstim@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/firstim/fish-databricks-jobs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
