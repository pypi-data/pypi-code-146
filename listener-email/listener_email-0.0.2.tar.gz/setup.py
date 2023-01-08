# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['listener_email']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'listener-email',
    'version': '0.0.2',
    'description': 'Listener Email - Remind you of changes in your listener through email!',
    'long_description': '<div align="center">\n  <img id="listener_email" width="96" alt="listener_email" src="repository_icon/icon.svg">\n  <p>『 listener_email - Let listener send email! 』</p>\n  <a href=\'README_zh.md\'>中文 Readme</a>\n</div>\n\n[📚 Introduction](#-Introduction)\n\n[📦 How to use](#-How-to-use)\n\n[⏳ Rate of progress](#-Rate-of-progress)\n\n[📌 Precautions](#-Precautions)\n\n[🧑\u200d💻 Contributor](#-Contributor)\n\n[🔦 Declaration](#-Declaration)\n\n---\n\n# 📚 Introduction\n\nRemind you of changes in your listener through email!\n\n# 📦 How to use\n\nSee example in [example.py](https://github.com/Cierra-Runis/listener_email/blob/master/src/listener_email/example.py) for more information\n\n- install `listener_email` by `pip install listener_email`\n- then import it by adding `from listener_email import sent_email, ListenerEmail`\n- add configured `email.json` file such as [example.json](https://github.com/Cierra-Runis/listener_email/blob/master/src/listener_email/example_json.json) at repository\n- at last use `sent_email()` to sent your email\n\n# ⏳ Rate-of-progress\n\nDone, but it will revise if necessary\n\n# 📌 Cautions\n\n- `custom_html` should be as simple as possible\n\n# 🧑\u200d💻 Contributor\n\n<a href="https://github.com/Cierra-Runis/listener_email/graphs/contributors">\n  <img src="https://contrib.rocks/image?repo=Cierra-Runis/listener_email" />\n</a>\n\n# 🔦 Declaration\n\n[![License](https://img.shields.io/github/license/Cierra-Runis/listener_email)](https://github.com/Cierra-Runis/listener_email/blob/master/LICENSE)\n\nThis project is licensed under the terms of the `GNU GPL v3.0` license. See [LICENSE](https://github.com/Cierra-Runis/listener_email/blob/master/LICENSE) for more details\n',
    'author': 'Cierra_Runis',
    'author_email': 'byrdsaron@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Cierra-Runis/listener_email',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
