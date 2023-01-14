# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zood']

package_data = \
{'': ['*'],
 'zood': ['config/*', 'config/img/*', 'config/js/*', 'config/js/prismjs/*']}

install_requires = \
['MarkdownParser>=0.2.0,<0.3.0', 'PyYAML>=6.0,<7.0']

entry_points = \
{'console_scripts': ['zood = zood.main:main']}

setup_kwargs = {
    'name': 'zood',
    'version': '0.5.0',
    'description': 'web page documentation & comment generation documentation',
    'long_description': '# zood\n\nzood 是一个辅助文档生成的Python库, zood的页面风格更倾向于纯文档内容而非博客\n\n## 主题预览\n\n[![20230101121438](https://raw.githubusercontent.com/learner-lu/picbed/master/20230101121438.png)](https://luzhixing12345.github.io/zood/)\n\n## 安装与使用\n\n```bash\npip install zood\n```\n\n参见 [用户使用文档](https://luzhixing12345.github.io/zood/)\n\n## 参考\n\n- [UI](https://remixicon.com/)',
    'author': 'kamilu',
    'author_email': 'luzhixing12345@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/luzhixing12345/zood',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
