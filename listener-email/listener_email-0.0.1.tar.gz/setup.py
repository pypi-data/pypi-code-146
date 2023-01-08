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
    'version': '0.0.1',
    'description': 'Listener Email - Remind you of changes in your listener through email!',
    'long_description': '<div align="center">\n  <img id="listener_email" width="96" alt="listener_email" src="repository_icon/icon.svg">\n  <p>『 listener_email - Let listener send email! 』</p>\n  <a href=\'README_zh.md\'>中文 Readme</a>\n</div>\n\n[📚 Introduction](#-Introduction)\n\n[📦 How to use](#-How-to-use)\n\n[⏳ Rate of progress](#-Rate-of-progress)\n\n[📌 Precautions](#-Precautions)\n\n[🧑\u200d💻 Contributor](#-Contributor)\n\n[🔦 Declaration](#-Declaration)\n\n---\n\n# 📚 Introduction\n\nRemind you of changes in your listener through email!\n\n# 📦 How to use\n\nCopy, paste then revise `README` file and the image in `repository_icon` folder\n\n# ⏳ Rate-of-progress\n\nDone, but it will revise if necessary\n\n# 📌 Precautions\n\n- Remember to revise the `id` and `alt` attribute in `<img>`\n- Remember to revise the repository name in Contributor\n\n# 🧑\u200d💻 Contributor\n\n<a href="https://github.com/Cierra-Runis/listener_email/graphs/contributors">\n  <img src="https://contrib.rocks/image?repo=Cierra-Runis/listener_email" />\n</a>\n\n# 🔦 Declaration\n\nMainly for personal use\n',
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
