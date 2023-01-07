# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['com2fun', 'com2fun.simulated_function']

package_data = \
{'': ['*']}

install_requires = \
['openai>=0.25.0,<0.26.0']

setup_kwargs = {
    'name': 'com2fun',
    'version': '0.1.4',
    'description': 'Transform document into function',
    'long_description': '# com2fun - Transform document into function.\n\nThis liabrary leverages\xa0[OpenAI API](https://github.com/openai/openai-python)\xa0to predict the output of a function based on its documentation.\n\n## Install\n\n```\npip install --upgrade com2fun\n```\n\n## Usage\n\nBasic usage:\n```\n@com2fun.com2fun\ndef top(category: str, n) -> list[str]:\n    """top n items"""\n\nIn  [1]: top("fish", 5)\nOut [1]: [\'salmon\', \'tuna\', \'cod\', \'mackerel\', \'halibut\']\nIn  [2]: type(top("fish", 5))\nOut [2]: list\nIn  [3]: top("Pen Brand", 3)\nOut [3]: [\'Pilot\', \'Uni-ball\', \'Zebra\']\n```\n\nSpecifiy output format by document:\n```\n@com2fun.com2fun\ndef SWOT(action: str) -> dict:\n    """\n    SWOT analysis is a powerful tool used to assess an organization’s strengths, \n    weaknesses, opportunities, and threats. It helps organizations focus their \n    resources and actions on areas where they have the most potential for success \n    and makes strategic decisions more transparent.\n    \n    Generate a SWOT analysis to assist business owners, managers, and individuals \n    in making tough decisions.\n    \n    Return a dictionary like \n    {\n        "strengths": [ (summary, explanation), ...],\n        "weaknesses": [...],\n        "oppotunities": [...],\n        "threats": [...],\n    }\n    """\n\nIn  [4]: print(SWOT("provide additional training for customer service staff"))\nOut [4]:\n{\'strengths\': [(\'Increased customer satisfaction\',\n   \'Providing additional training for customer service staff will help them better understand customer needs and provide better service, leading to increased customer satisfaction.\')],\n \'weaknesses\': [(\'Cost of training\',\n   \'Providing additional training for customer service staff will require additional resources, such as time and money, which can be a significant cost to the organization.\')],\n \'opportunities\': [(\'Improved customer service\',\n   \'Providing additional training for customer service staff will help them better understand customer needs and provide better service, leading to improved customer service.\')],\n \'threats\': [(\'Lack of resources\',\n   \'Providing additional training for customer service staff may require additional resources, such as time and money, which may not be available to the organization.\')]}\n```\n\nChain of thought:\n```\n@com2fun.com2fun\ndef solve_elementary_math(question: str) -> dict:\n    """\n    {"debug": {"step by step explanation": list[str]},\n     "return": float}\n    """\nIn  [5]: solve_elementary_math("Maurita and Felice each take 4 tests. Here are the results of Maurita’s 4 tests: 4, 4, 4, 4. Here are the results for 3 of Felice’s 4 tests: 3, 3, 3. If Maurita’s mean for the 4 tests is 1 point higher than Felice’s, what’s the score of Felice’s 4th test?")\nOut [5]:\n{\'debug\': {\'step by step explanation\': [\'Maurita and Felice each took 4 tests.\',\n   \'Maurita got 4, 4, 4, 4 on her tests.\',\n   \'Felice got 3, 3, 3 on 3 of her tests.\',\n   \'Maurita’s mean for the 4 tests is 1 point higher than Felice’s.\',\n   \'We need to find the score of Felice’s 4th test.\',\n   \'Maurita’s mean is 4, so Felice’s mean must be 3.\',\n   \'The sum of Felice’s 4 tests must be 3 + 3 + 3 + x = 12.\',\n   \'Therefore, x = 12 - 9 = 3.\',\n   \'The score of Felice’s 4th test is 3.\']},\n \'return\': 3.0}\n```\n\n## Add Example\n\n```\nIn  [1]: top.add_example(\'continents\', 3)([\'Asia\', \'Africa\', \'North America\'])\n```\n\n## Different Prompt Formats\n\n### Python Interpreter\n\n```\nIn  [2]: pirnt(top.invoke_prompt("Pen Brand", 3))\n>>> 1\n1\n>>> def top(category: str, n) -> list[str]:\n>>>     """Return a list of top-n items in a category."""\n>>>     _top(*locals())\n>>>\n>>> top(\'continents\', 3)\n[\'Asia\', \'Africa\', \'North America\']\n>>> top(\'Pen Brand\', 3)\n\n```\n\n### Flat\n\n```\n@functools.partial(com2fun.com2fun, SF=com2fun.FlatSF)\ndef text2tex(text: str) -> str:\n    pass\n\nIn  [1]: text2tex.add_example("x divided by y")(r"\\frac{x}{y}")\nIn  [2]: print(text2tex.invoke_prompt("integrate f(x) from negative infinity to infinity"))\ndef text2tex(text: str) -> str:\n    pass\n###\n\'x divided by y\'\n---\n\\frac{x}{y}\n###\n\'integrate f(x) from negative infinity to infinity\'\n---\n\n```\n\n### Template\nThis format is inspired by [lambdaprompt](https://github.com/approximatelabs/lambdaprompt).\n\n```\nIn  [1]: text2tex = com2fun.prompt("{} into latex: ")\nIn  [2]: text2tex.add_example("x divided by y")(r"\\frac{x}{y}")\nIn  [3]: print(text2tex.invoke_prompt("integrate f(x) from negative infinity to infinity"))\nx divided by y into latex: \\frac{x}{y}\nintegrate f(x) from negative infinity to infinity into latex: \n```\n',
    'author': 'Zhengmian Hu',
    'author_email': 'huzhengmian@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
