# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['saxproject']

package_data = \
{'': ['*']}

install_requires = \
['jinja2>=3.1.2,<4.0.0',
 'parse>=1.19.0,<2.0.0',
 'requests-wsgi-adapter>=0.4.1,<0.5.0',
 'requests>=2.28.1,<3.0.0',
 'webob>=1.8.7,<2.0.0',
 'whitenoise>=6.3.0,<7.0.0']

setup_kwargs = {
    'name': 'saxproject',
    'version': '1.1.1',
    'description': '',
    'long_description': '<div align="center" id="top">\n  <img src="https://raw.githubusercontent.com/rise-consulting/saxproject/main/.github/sax.png?raw=true" alt="Sax" height="100px"/>\n</div>\n\n<br />\n\n<div align="center">\n  <h1>Python Web Framework built for real projects</h1>\n  &#xa0;\n  \n  ## 📖 [Documentation](https://rise-consulting.github.io/saxproject) 📖\n\n  &#xa0;\n\n[![PyPI](https://img.shields.io/pypi/v/saxproject.svg)](https://pypi.org/project/saxproject/)\n[![CI/CD](https://github.com/rise-consulting/saxproject/actions/workflows/release.yml/badge.svg)](https://github.com/rise-consulting/saxproject/actions/workflows/release.yml)\n[![Coverage Status](https://coveralls.io/repos/github/rise-consulting/saxproject/badge.svg)](https://coveralls.io/github/rise-consulting/saxproject)\n\n[![GitHub](https://img.shields.io/github/license/rise-consulting/saxproject)](https://github.com/rise-consulting/saxproject/blob/main/LICENSE.md)\n[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](code_of_conduct.md)\n\n</div>\n\n<hr>\n\n<p align="center">\n  <a href="#-about">About</a> &#xa0; | &#xa0;\n  <a href="#-features">Features</a> &#xa0; | &#xa0;\n  <a href="#-technologies">Technologies</a> &#xa0; | &#xa0;\n  <a href="#-installation">Installation</a> &#xa0; | &#xa0;\n  <a href="#-license">License</a> &#xa0; | &#xa0;\n  <a href="https://github.com/max-bertinetti" target="_blank">Author</a>\n</p>\n\n&#xa0;\n\n## 🎯 About\n\nSaxproject is a Python web framework built for learning purposes and evolving for working on real projects.\n\nIt\'s a WSGI framework and can be used with any WSGI application server such as [Gunicorn](https://gunicorn.org/).\n\n&#xa0;\n\n## ✨ Features\n\n✔️ WSGI compatibility\\\n✔️ Flask and Django style routing.\\\n✔️ Json / HTML / Text Responses\\\n✔️ Templates\\\n✔️ Static Files\\\n✔️ Middleware\\\n✔️ Test\\\n✔️ ORM with SQLite\n\n&#xa0;\n\n## 🚀 Technologies\n\nThe following tools were used in this project:\n\n- [Parse](https://pypi.org/project/parse/)\n- [Jinja2](https://pypi.org/project/Jinja2/)\n- [Whitenoise](https://pypi.org/project/whitenoise/)\n- [WebOb](https://pypi.org/project/WebOb/)\n- [Pytest](https://pypi.org/project/pytest/)\n- [Requests](https://pypi.org/project/requests/)\n- [Requests-wsgi-adapter](https://pypi.org/project/requests-wsgi-adapter/)\n\n&#xa0;\n\n## 🏁 Installation\n\n```shell\npip install saxproject\n```\n\n&#xa0;\n\n## 📝 License\n\nThis project is under license from MIT. For more details, see the [LICENSE](https://github.com/rise-consulting/saxproject/blob/main/LICENSE.md) file.\n\nMade with ❤️ & ☕ by <a href="https://github.com/rise-consulting" target="_blank">Rise Consulting</a>\n\n&#xa0;\n\n<a href="#top">Back to top</a>\n',
    'author': 'Massimiliano Bertinetti',
    'author_email': 'max-b@murena.io',
    'maintainer': 'Massimiliano Bertinetti',
    'maintainer_email': 'max-b@murena.io',
    'url': 'https://rise-consulting.github.io/saxproject/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
