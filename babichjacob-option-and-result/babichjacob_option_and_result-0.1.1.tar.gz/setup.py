# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['option_and_result']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'babichjacob-option-and-result',
    'version': '0.1.1',
    'description': "A Python implementation of Rust's Option and Result",
    'long_description': '<h1 align="center">🤷 Option and Result</h1>\n\nThis library uses code copy and pasted from [Peijun Ma\'s `option` library](https://github.com/MaT1g3R/option), which they have generously published under the MIT license. 🙏\n\nThis is a Python implementation of Rust\'s [`Option`](https://doc.rust-lang.org/std/option/index.html) and [`Result`](https://doc.rust-lang.org/std/result/index.html) types in order to help make fallible functions identifiable and more robust than typical exceptions.\n\n## 💻 Installation\n\nThis package is [published to PyPI as `babichjacob-option-and-result`](https://pypi.org/project/babichjacob-option-and-result/).\n\n## 🛠 Usage\n\n```py\nfrom option_and_result import NONE, Some, Ok, Err\n\nmaybe_a_number = Some(17)\nassert maybe_a_number.unwrap() == 17\n\nnothing = NONE()\nassert nothing.is_none()\n\nnumber_result = maybe_a_number.ok_or("not a number")\nassert number_result == Ok(17)\n\nresult_that_is_err = Err("gah! an error!")\ncombinatoric_result = number_result.and_(result_that_is_err)\n\nassert combinatoric_result.unwrap_err() == "gah! an error!"\n\n# more methods on Options and Results are available like the Rust documentation shows\n\n# there is also MatchesNone, MatchesSome, MatchesOk, and MatchesErr \n# for use with Python 3.10\'s new structural pattern matching feature\n```\n\n## 😵 Help! I have a question\n\nCreate an issue and I\'ll try to help.\n\n## 😡 Fix! There is something that needs improvement\n\nCreate an issue or pull request and I\'ll try to fix.\n\n## 📄 License\n\nMIT\n\n## 🙏 Attribution\n\n_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_\n',
    'author': 'J or Jacob Babich',
    'author_email': 'jacobbabichpublic+git@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/babichjacob/python-option-and-result',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10',
}


setup(**setup_kwargs)
