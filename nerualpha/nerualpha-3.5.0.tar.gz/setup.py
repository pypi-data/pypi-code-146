# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nerualpha',
 'nerualpha.providers',
 'nerualpha.providers.assets',
 'nerualpha.providers.assets.contracts',
 'nerualpha.providers.events',
 'nerualpha.providers.logger',
 'nerualpha.providers.meetings',
 'nerualpha.providers.meetings.contracts',
 'nerualpha.providers.messages',
 'nerualpha.providers.messages.contracts',
 'nerualpha.providers.numbers',
 'nerualpha.providers.numbers.contracts',
 'nerualpha.providers.scheduler',
 'nerualpha.providers.scheduler.contracts',
 'nerualpha.providers.state',
 'nerualpha.providers.voice',
 'nerualpha.providers.voice.contracts',
 'nerualpha.providers.vonageAI',
 'nerualpha.providers.vonageAI.contracts',
 'nerualpha.providers.vonageAPI',
 'nerualpha.providers.vonageAPI.contracts',
 'nerualpha.request',
 'nerualpha.services',
 'nerualpha.services.commandService',
 'nerualpha.services.config',
 'nerualpha.services.jwt',
 'nerualpha.session',
 'nerualpha.webhookEvents',
 'nerualpha.webhookEvents.messenger',
 'nerualpha.webhookEvents.mms',
 'nerualpha.webhookEvents.sms',
 'nerualpha.webhookEvents.viber',
 'nerualpha.webhookEvents.whatsapp']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT[crypto]', 'aiohttp', 'pendulum', 'requests']

setup_kwargs = {
    'name': 'nerualpha',
    'version': '3.5.0',
    'description': 'neru-sdk for python developers',
    'long_description': "## To build the SDK locally:\nBecause I've been experiencing some issues with the build process on `Mac M1`, I decided to use docker to install dependencies and build the SDK. I've created a `Dockerfile` that can be used to build the SDK. \n\nI mount the current directory to the container to have the artifacts after the build process available on the host machine in `/dist` folder.\n\nThe `Dockerfile` is located in the `python` directory. To build the SDK, run the following command:\n\n```bash\n# Build the docker image\ndocker build -t neru-sdk-python .\n```\n\n```bash\n# Build the SDK\nmake build\n```",
    'author': 'Sergei Rastrigin',
    'author_email': 'sergei.rastrigin@vonage.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.5,<4.0.0',
}


setup(**setup_kwargs)
