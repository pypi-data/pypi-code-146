# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['markdownparser']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'markdownparser',
    'version': '0.1.6',
    'description': '',
    'long_description': '# MarkdownParser\n\nMarkdownParser 是一个 Markdown 语法解析器,用于实现md到html标签的转换\n\n## 安装\n\n```bash\npip install markdownparser\n```\n\n## 快速使用\n\n```python\nimport MarkdownParser\n\nhtml = MarkdownParser.parse(\'# Hello World\')\nprint(html)\n\n#<div class=\'markdown-body\'><h1>Hello World!</h1></div>\n```\n\n其他接口函数\n\n- `parseFile(file_name:str)->str`: 解析文件\n- `parseToRoot(text:str)->Block`: 逐行解析,得到一颗未优化的树\n- `parseToTree(text:str)->Block`: 优化,得到正确的markdown解析树\n\n其中Block类属性见\'base_class.py`,可以通过print打印查看\n\n接口类\n\n- `Markdown`\n\n## 不支持\n\n- 四个空格变为代码段(不想支持)\n- [^1]的引用方式(不想支持)\n- Latex数学公式(不会支持)\n- Setext 形式的标题(不想支持)\n- 上标 / 下标 / 下划线(不想支持)\n- SpecialTextBlock中叠加使用有可能会有bug(没想好怎么支持)\n\n## 其他特性\n\n- 最外层为div包裹,类名为 `markdown-body`\n- 代码段会根据语言加入一个类名便于后期高亮 `class="language-cpp"`, 未定义语言则为 `language-UNKNOWN`\n- 列表嵌套稍有不同,ul/ol+li完全体\n\n## 相关参考\n\n- [Github Markdown CSS](https://cdn.jsdelivr.net/npm/github-markdown-css@4.0.0/github-markdown.css)',
    'author': 'luzhixing12345',
    'author_email': 'luzhixing12345@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/luzhixing12345/MarkdownParser',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
