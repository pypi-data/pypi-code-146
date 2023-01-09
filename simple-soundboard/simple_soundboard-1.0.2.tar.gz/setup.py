# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['simple_soundboard']

package_data = \
{'': ['*'], 'simple_soundboard': ['static/img/*', 'static/simple_soundboard/*']}

install_requires = \
['fastapi>=0.88.0,<0.89.0',
 'paho-mqtt>=1.6.1,<2.0.0',
 'pygame>=2.1.2,<3.0.0',
 'ujson>=5.6.0,<6.0.0',
 'uvicorn>=0.20.0,<0.21.0']

entry_points = \
{'console_scripts': ['simple_soundboard = simple_soundboard.web_ui:start']}

setup_kwargs = {
    'name': 'simple-soundboard',
    'version': '1.0.2',
    'description': 'Simple Soundboard',
    'long_description': '# Simple Soundboard\nSimple soundboard web app that plays sounds on a central server\n\n## Installation\nInstall through pip with\n\n`pip install simple_soundboard`\n\n## Usage\nEdit config in ~/simple_soundboard/config.json\nStart by running\n`simple_soundboard`\n\n### MQTT API\nMQTT Server is configured in ~/simple_soundboard/config.json\nMQTT API includes\n```\nsimple_soundboard/stop_all\nsimple_soundboard/stop_sounds\nsimple_soundboard/fadeout\nsimple_soundboard/pause_music\nsimple_soundboard/resume_music\nsimple_soundboard/play/<topic_from_web_ui>\n```\n\nNo payload required\n\nThe server output two MQTT topic\n```\nsimple_soundboard/stopped_all\nsimple_soundboard/stopped_sounds\nsimple_soundboard/playing/<topic_from_web_ui> (If MQTT Topic is set)\n```\nwill be published\n\n## TODO\n- Make the config editable online\n- Multiple music?\n\n\n## Development\ngit clone this project\n\nCreate a new venv\n\n`python3 -m venv --system-site-packages ./venv`\n\nSource it\n\n`source ./venv/bin/activate`\n\nInstall all dependancies with poetry\n\n`poetry install`\n\nInstall git hooks\n\n`pre-commit install`\n\n### Upload to pypi\n\nSource the venv\n\n`source ./venv/bin/activate`\n\nInstall twine\n\n`pip install twine`\n\nConfig your pypi credentials in the file `~/.pypirc`\n\n```python\n[pypi]\nusername = pypi_username\npassword = pypi_password\n```\n\nRun\n\n```python\npoetry install\ntwine check dist/*\ntwine upload dist/*\n```\n',
    'author': 'Martin Rioux',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9.0,<4.0.0',
}


setup(**setup_kwargs)
