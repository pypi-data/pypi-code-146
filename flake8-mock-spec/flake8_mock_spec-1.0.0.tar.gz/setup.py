# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['flake8_mock_spec']
install_requires = \
['flake8>=5']

entry_points = \
{'flake8.extension': ['TMS = flake8_mock_spec:Plugin']}

setup_kwargs = {
    'name': 'flake8-mock-spec',
    'version': '1.0.0',
    'description': 'A linter that checks mocks are constructed with the spec argument',
    'long_description': "# flake8-mock-spec\n\nDo you use mocks and are concerned you are calling methods or accessing\nattributes the mocked objects don't have? If not, you should be as that is a\nsure way to inject bugs into your code and still have your tests pass. The\n`flake8-mock-spec` linter enforces the use of the `spec` argument on mocks\nensuring that your use of mocks is compliant with the interface of the object\nbeing mocked.\n\n## Getting Started\n\n```shell\npython -m venv venv\nsource ./venv/bin/activate\npip install flake8-mock-spec\nflake8 test_source.py\n```\n\nOn the following code:\n\n```Python\n# test_source.py\nfrom unittest import mock\n\ndef test_foo():\n    mocked_foo = mock.Mock()\n```\n\nThis will produce warnings such as:\n\n```shell\nflake8 test_source.py\ntest_source.py:5:22: TMS001 unittest.mock.Mock instances should be constructed with the spec or spec_set argument, more information: https://github.com/jdkandersson/flake8-mock-spec#fix-tms001\n```\n\nThis can be resolved by changing the code to:\n\n```Python\n# test_source.py\nfrom unittest import mock\n\nfrom foo import Foo\n\ndef test_foo():\n    mocked_foo = mock.Mock(spec=Foo)\n```\n\n## Rules\n\nA few rules have been defined to allow for selective suppression:\n\n* `TMS001`: checks that `unittest.mock.Mock` instances are constructed with the\n  `spec` or `spec_set` argument.\n* `TMS002`: checks that `unittest.mock.MagicMock` instances are constructed with\n  the `spec` or `spec_set` argument.\n\n### Fix TMS001\n\nThis linting rule is triggered by creating a `unittest.mock.Mock` instance\nwithout the `spec` or `spec_set` argument. For example:\n\n```Python\nfrom unittest import mock\n\ndef test_foo():\n    mocked_foo = mock.Mock()\n```\n\nThis example can be fixed by using the `spec` or `spec_set` argument in the\nconstructor:\n\n```Python\nfrom unittest import mock\n\nfrom foo import Foo\n\ndef test_foo():\n    mocked_foo = mock.Mock(spec=Foo)\n```\n\n```Python\nfrom unittest import mock\n\nfrom foo import Foo\n\ndef test_foo():\n    mocked_foo = mock.Mock(spec_set=Foo)\n```\n\n### Fix TMS002\n\nThis linting rule is triggered by creating a `unittest.mock.MagicMock` instance\nwithout the `spec` or `spec_set` argument. For example:\n\n```Python\nfrom unittest import mock\n\ndef test_foo():\n    mocked_foo = mock.MagicMock()\n```\n\nThis example can be fixed by using the `spec` or `spec_set` argument in the\nconstructor:\n\n```Python\nfrom unittest import mock\n\nfrom foo import Foo\n\ndef test_foo():\n    mocked_foo = mock.MagicMock(spec=Foo)\n```\n\n```Python\nfrom unittest import mock\n\nfrom foo import Foo\n\ndef test_foo():\n    mocked_foo = mock.MagicMock(spec_set=Foo)\n```\n",
    'author': 'David Andersson',
    'author_email': 'david@jdkandersson.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
