# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pynction', 'pynction.functors', 'pynction.monads', 'pynction.streams']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pynction',
    'version': '0.4.1',
    'description': 'Functional based library to support monads and other functional programming concepts',
    'long_description': '# Pynction 🐍\n\n[![](https://img.shields.io/pypi/v/pynction.svg?maxAge=3600)](https://pypi.org/project/pynction/)\n\n[![continuous_integration](https://github.com/niconunez96/pynction/actions/workflows/ci.yaml/badge.svg)](https://github.com/niconunez96/pynction/actions/workflows/ci.yaml)\n[![codecov](https://codecov.io/gh/niconunez96/pynction/branch/main/graph/badge.svg?token=YI2ZOWV29E)](https://codecov.io/gh/niconunez96/pynction)\n [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\nFunctional based library to support haskell monads like Either, Maybe in a scala fashion style. The library also contains Try monad inspired from vavr and a Stream class which is pretty similar to scala and java stream API\n\nInspired in: [VΛVR](https://github.com/vavr-io/vavr)\n\n## Why should you use it ?\n\nProbably if you have reached this library you already know something about functional programming and Monads.\nWell this library is another one that empowers your imperative code to start using functional programming concepts. This type of programming makes your code declarative as long as give you support to the most famous monads like `Maybe` and `Either`.\nThese monads make your interfaces explicit for error handling so paraphrasing `If it compiles, it works` this time it is `If mypy is happy, your code works`\n\n## Basic examples\n\n### Stream examples\n\n```python\nfrom pynction import stream_of, stream\n\n\nfoo = (\n    stream_of([1, 2, 3, 4])\n    .map(lambda a: a + 1)\n    .filter(lambda n: n % 2 == 0)\n    .flat_map(lambda n: [n, n * 2])\n    .to_list()\n)\n\n# foo => [2, 4, 4, 8]\n\nbar = (\n    stream("example", "e", "something")\n    .take_while(lambda s: s.startswith("e"))\n    .to_list()\n)\n\n# bar => ["example", "e"]\n```\n\n### Maybe examples\n\n```python\nfrom pynction import maybe, nothing\n\ndef divide_10_by(n: int) -> Maybe[int]:\n    if n == 0:\n        return nothing\n    return maybe(10 / n)\n\nresult = divide_10_by(2).get_or_else_get(-1)\n# result => 5\nresult = divide_10_by(0).get_or_else_get(-1)\n# result => -1\n```\n\n### Try examples\n\n```python\nfrom pynction import try_of\n\n\ndef add_10(n: int) -> int:\n    if n > 10:\n        raise Exception("n must be less than 10")\n    return n + 10\n\ntry_example_1 = try_of(lambda: add_10(11)).map(lambda a: a + 1)\ntry_example_1.on(\n    on_success=lambda a: print(f"Result: {a}"),\n    on_failure=lambda e: print(f"Error: {e}"),\n)\n# ==> Will print "Error: n must be less than 10"\n\ntry_example_2 = try_of(lambda: add_10(9)).map(lambda a: a + 1)\ntry_example_2.on(\n    on_success=lambda a: print(f"Result: {a}"),\n    on_failure=lambda e: print(f"Error: {e}"),\n)\n# ==> Will print "Result: 20"\n\n\n```\n\n### Either examples\n\n```python\nfrom pynction import left, right, Either\n\n\nLESS_THAN_10_LETTERS = Literal["LESS_THAN_10_LETTERS"]\nGREATER_THAN_100 = Literal["GREATER_THAN_100"]\nWordTransformationError = Literal[LESS_THAN_10_LETTERS, GREATER_THAN_100]\n\ndef make_upper_case_first_n_letters(word: str, number: int) -> Either[WordTransformationError, str]:\n    if len(word) < 10:\n        return left("LESS_THAN_10_LETTERS")\n    elif number > 100:\n        return left("GREATER_THAN_100")\n    else:\n        return right(word.upper()[0:number])\n\nresult = make_upper_case_first_n_letters("example", 10)\nprint(result) # ==> Will be Left("LESS_THAN_10_LETTERS")\n```\n\n## API\n\nCheck the [docs](https://pynction.vercel.app/)\n',
    'author': 'Nicolas Nuñez',
    'author_email': 'nicolas110996@gmail.com',
    'maintainer': 'Nicolas Nuñez',
    'maintainer_email': 'nicolas110996@gmail.com',
    'url': 'https://github.com/niconunez96/pynction',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
