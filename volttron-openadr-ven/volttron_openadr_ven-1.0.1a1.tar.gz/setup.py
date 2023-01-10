# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['openadr_ven']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=36.0.1,<37.0.0',
 'openleadr==0.5.27',
 'volttron>=10.0.2rc0,<11.0.0']

entry_points = \
{'console_scripts': ['volttron-openadr-ven = openadr_ven.agent:main']}

setup_kwargs = {
    'name': 'volttron-openadr-ven',
    'version': '1.0.1a1',
    'description': 'A Volttron agent that acts as a Virtual End Node (VEN) within the OpenADR 2.0b specification.',
    'long_description': '# OpenADRVen Agent\n\n\n[![Passing?](https://github.com/eclipse-volttron/volttron-openadr-ven/actions/workflows/run-tests.yml/badge.svg)](https://github.com/eclipse-volttron/volttron-openadr-ven/actions/workflows/run-tests.yml?query=branch%3Adevelop)\n[![pypi version](https://img.shields.io/pypi/v/volttron-openadr-ven.svg)](https://pypi.org/project/volttron-openadr-ven/)\n\n\nOpenADR (Automated Demand Response) is a standard for alerting and responding to the need to adjust electric power consumption in response to fluctuations in grid demand.\n\n\n# Prerequisites\n\n\n* Python 3.8\n\n\n# Installation\n\n\n1. Create and activate a virtual environment.\n\n   ```shell\n   python -m venv env\n   source env/bin/activate\n   ```\n\n1. Install volttron and start the platform.\n\n    ```shell\n    pip install volttron\n\n\n    # Start platform with output going to volttron.log\n    volttron -vv -l volttron.log &\n    ```\n\n1.  Install and start the Volttron OpenADRVen Agent.\n\n\n    ```shell\n    vctl install volttron-openadr-ven --agent-config <path to agent config> \\\n    --vip-identity openadr.ven \\\n    --start\n    ```\n\n1. View the status of the installed agent\n\n\n    ```shell\n    vctl status\n    ```\n\n1. Observe Data\n\n    The OpenADR publishes events on the message bus. To see these events in the Volttron log file, install a [Listener Agent](https://pypi.org/project/volttron-listener/):\n\n\n    ```\n    vctl install volttron-listener --start\n    ```\n\n\n    Once installed, you should see the data being published by viewing the Volttron logs file that was created in step 2.\n\n    To watch the logs, open a separate terminal and run the following command:\n\n\n    ```\n    tail -f <path to folder containing volttron.log>/volttron.log\n    ```\n\n\n# Agent Configuration\n\n\nThe required parameters for this agent are "ven_name" and "vtn_url". Below is an example of a correct configuration with optional parameters added.\n\n\n```json\n    {\n        "ven_name": "PNNLVEN",\n        "vtn_url": "https://eiss2demo.ipkeys.com/oadr2/OpenADR2/Simple/2.0b",\n        "cert_path": "~/.ssh/secret/TEST_RSA_VEN_210923215148_cert.pem",\n        "key_path": "~/.ssh/secret/TEST_RSA_VEN_210923215148_privkey.pem",\n        "debug": true,\n        "disable_signature": true\n    }\n```\n\n\nSave this configuration in a JSON file in your preferred location. An example of such a configuration is saved in the\nroot of this repository; the file is named `config_example1.json`\n\n# Testing\n\nIf you don\'t have a dedicated VTN to test the VolttronOpenADR against, you can setup a local VTN instead. This VTN will be hosted at localhost on port 8080 (i.e. 127.0.0.1:8080). This VTN will accept registrations from a VEN named \'ven123\', requests all reports that the VEN offers, and create an Event for the VEN. After setting up a local VTN, configure an VolttronOpenADRVen Agent against that local VTN and then install the agent on your VOLTTRON instance. Ensure that the VOLTTRON instance is running on the same host that the VTN is running on.\n\nTo setup a local VTN, we have provided a script and a custom agent configuration for convenience. Follow the steps below to setup a local VTN and corresponding Volttron OpenADRVen Agent:\n\n\n1. Create a virtual environment:\n\n\n    ```shell\n    python -m venv env\n    source env/bin/activate\n    ```\n\n\n1. Install [openleadr](https://pypi.org/project/openleadr/):\n\n    ```shell\n    pip install openleadr\n    ```\n\n1. At the top level of this project, run the VTN server in the foreground so that we can observe logs:\n\n    ```shell\n    python utils/vtn.py\n    ```\n\n1. Open up another terminal, create a folder called temp, and create another virtual environment:\n\n    ```shell\n    mkdir temp\n    cd temp\n    python -m venv env\n    source env/bin/activate\n    ```\n\n1. Install volttron:\n\n    ```shell\n    pip install volttron\n    ```\n\n1. Run volttron in the background:\n\n    ```shell\n    volttron -vv -l volttron.log &\n    ```\n\n1. Install the VolttronOpenADRVEN Agent using the configuration provided under `utils`:\n\n    ```shell\n    vctl install volttron-openadr-ven --agent-config utils/config_toy_ven.json --tag openadr --start\n    ```\n\n1. Observe the logs to verify that the Event from the local VTN was received by the VolttronOpenADRVEN agent\n\n    ```\n    tail -f volttron.log\n    ```\n\n\n# Development\n\n\nPlease see the following for contributing guidelines [contributing](https://github.com/eclipse-volttron/volttron-core/blob/develop/CONTRIBUTING.md).\n\n\nPlease see the following helpful guide about [developing modular VOLTTRON agents](https://github.com/eclipse-volttron/volttron-core/blob/develop/DEVELOPING_ON_MODULAR.md)\n\n\n# Disclaimer Notice\n\n\nThis material was prepared as an account of work sponsored by an agency of the\nUnited States Government.  Neither the United States Government nor the United\nStates Department of Energy, nor Battelle, nor any of their employees, nor any\njurisdiction or organization that has cooperated in the development of these\nmaterials, makes any warranty, express or implied, or assumes any legal\nliability or responsibility for the accuracy, completeness, or usefulness or any\ninformation, apparatus, product, software, or process disclosed, or represents\nthat its use would not infringe privately owned rights.\n\n\nReference herein to any specific commercial product, process, or service by\ntrade name, trademark, manufacturer, or otherwise does not necessarily\nconstitute or imply its endorsement, recommendation, or favoring by the United\nStates Government or any agency thereof, or Battelle Memorial Institute. The\nviews and opinions of authors expressed herein do not necessarily state or\nreflect those of the United States Government or any agency thereof.\n',
    'author': 'Mark Bonicillo',
    'author_email': 'mark.bonicillo@pnnl.gov',
    'maintainer': 'Volttron Team',
    'maintainer_email': 'volttron@pnnl.gov',
    'url': 'https://github.com/VOLTTRON/volttron-openadr-ven',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
