# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scheduler', 'scheduler.migrations']

package_data = \
{'': ['*'], 'scheduler': ['static/scheduler/js/*']}

install_requires = \
['Flake8-pyproject>=1.2,<2.0',
 'croniter>=1.3,<2.0',
 'django-model-utils>=4.3,<5.0',
 'django-rq>=2.6,<3.0',
 'django>=3.2,<=4.2']

setup_kwargs = {
    'name': 'django-rq-scheduler',
    'version': '2023.2.0',
    'description': 'A database backed job scheduler for Django RQ with Django',
    'long_description': '# Django RQ Scheduler \n[![Django CI](https://github.com/dsoftwareinc/django-rq-scheduler/actions/workflows/test.yml/badge.svg)](https://github.com/dsoftwareinc/django-rq-scheduler/actions/workflows/test.yml)\n![badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/cunla/b756396efb895f0e34558c980f1ca0c7/raw/django-rq-scheduler-4.json)\n[![badge](https://img.shields.io/pypi/dm/django-rq-scheduler)](https://pypi.org/project/django-rq-scheduler/)\n\n> Notice:\n> Starting v2023.1, requirement for rq_scheduler was removed and instead\n> one of the django-rq workers should run with `--with-scheduler` parameter\n> as mentioned [here](https://github.com/rq/django-rq#support-for-scheduled-jobs).\n\n\nA database backed job scheduler for Django RQ.\nBased on original [django-rq-scheduler](https://github.com/isl-x/django-rq-scheduler) - Now supports Django 4.0.\n\nThis allows remembering scheduled jobs, their parameters, etc.\n\n# Installation\n\n1. Use pip to install:\n   ```shell\n   pip install django-rq-scheduler\n   ```\n\n2. In `settings.py`, add `django_rq` and `scheduler` to  `INSTALLED_APPS`:\n   ```python\n   INSTALLED_APPS = [\n       ...\n       \'django_rq\',\n       \'scheduler\',\n       ...\n   ]\n   ```\n\n3. Configure Django RQ. See https://github.com/ui/django-rq#installation\n   \n   Add at least one Redis Queue to your `settings.py`:\n   ```python\n   RQ_QUEUES = {\n     \'default\': {\n         \'HOST\': \'localhost\',\n         \'PORT\': 6379,\n         \'DB\': 0,\n         \'PASSWORD\': \'some-password\',\n         \'DEFAULT_TIMEOUT\': 360,\n     },\n   }\n   ```\n\n4. Run migrations.\n    ```shell\n    ./manage.py migrate\n    ```\n\n# Usage\n\n## Making a method in your code a schedulable job to be run by a worker.\n\nSee http://python-rq.org/docs/jobs/ or https://github.com/ui/django-rq#job-decorator\n\nAn example:\n\n**myapp.jobs.py**\n\n```python\nfrom django_rq import job\n\n@job\ndef count():\n    return 1 + 1\n```\n\n## Scheduling a Job\n\n### Scheduled Job\n\n1. Sign in to the Django Admin site, http://localhost:8000/admin/ and locate the **Django RQ Scheduler** section.\n\n2. Click on the **Add** link for Scheduled Job.\n\n3. Enter a unique name for the job in the **Name** field.\n\n4. In the **Callable** field, enter a Python dot notation path to the method that defines the job. For the example above, that would be `myapp.jobs.count`\n\n5. Choose your **Queue**. Side Note: The queues listed are defined in the Django Settings.\n\n6. Enter the time the job is to be executed in the **Scheduled time** field. Side Note: Enter the date via the browser\'s local timezone, the time will automatically convert UTC.\n\n7. Click the **Save** button to schedule the job.\n\n### Repeatable Job\n\n1. Sign in to the Django Admin site, http://localhost:8000/admin/ and locate the **Django RQ Scheduler** section.\n\n2. Click on the **Add** link for Repeatable Job\n\n3. Enter a unique name for the job in the **Name** field.\n\n4. In the **Callable** field, enter a Python dot notation path to the method that defines the job. For the example above, that would be `myapp.jobs.count`\n\n5. Choose your **Queue**. Side Note: The queues listed are defined in the Django Settings.\n\n6. Enter the time the first job is to be executed in the **Scheduled time** field. Side Note: Enter the date via the browser\'s local timezone, the time will automatically convert UTC.\n\n7. Enter an **Interval**, and choose the **Interval unit**. This will calculate the time before the function is called again.\n\n8. In the **Repeat** field, enter the number of time the job is to be run. Leaving the field empty, means the job will be scheduled to run forever.\n\n9. Click the **Save** button to schedule the job.\n\n# Advanced usage using jobs with args\n\ndjango-rq-scheduler supports \n```python\n\nfrom django_rq import job\n@job\ndef job_args_kwargs(*args, **kwargs):\n    func = "test_args_kwargs({})"\n    args_list = [repr(arg) for arg in args]\n    kwargs_list = [k + \'=\' + repr(v) for (k, v) in kwargs.items()]\n    return func.format(\', \'.join(args_list + kwargs_list))\n```\n\n\n### Schedule job with custom arguments to be calculated when scheduling\n\n1. Sign in to the Django Admin site, http://localhost:8000/admin/ and locate the **Django RQ Scheduler** section.\n\n2. Click on the **Add** link for Scheduled Job.\n\n3. Enter a unique name for the job in the **Name** field.\n\n4. In the **Callable** field, enter a Python dot notation path to the method that defines the job. For the example above, that would be `myapp.jobs.job_args_kwargs`\n\n5. Choose your **Queue**. Side Note: The queues listed are defined in the Django Settings.\n\n6. Enter the time the job is to be executed in the **Scheduled time** field. Side Note: Enter the date via the browser\'s local timezone, the time will automatically convert UTC.\n\n7. Click the **Save** button to schedule the job.\n\n8. Add arguments to the job, pick argument type.\n\n9. Add arguments with keys to the job, pick argument type and value.\n\n# Reporting issues or Features requests\n\nPlease report issues via [GitHub Issues](https://github.com/dsoftwareinc/django-rq-scheduler/issues) .\n\n',
    'author': 'Daniel Moran',
    'author_email': 'daniel.maruani@gmail.com',
    'maintainer': 'Daniel Moran',
    'maintainer_email': 'daniel.maruani@gmail.com',
    'url': 'https://github.com/dsoftwareinc/django-rq-scheduler',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
