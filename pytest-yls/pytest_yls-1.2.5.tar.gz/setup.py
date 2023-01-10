# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_yls']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.1.2,<8.0.0', 'tenacity>=8.0.1,<9.0.0', 'yls>=1,<2']

entry_points = \
{'pytest11': ['pytest_yls = pytest_yls']}

setup_kwargs = {
    'name': 'pytest-yls',
    'version': '1.2.5',
    'description': 'Pytest plugin to test the YLS as a whole.',
    'long_description': '# pytest-yls\n\n![PyPI](https://img.shields.io/pypi/v/pytest-yls)\n\nPytest plugin adding primitives for E2E/integration tests.\n\nPublic fixtures:\n- `yls_prepare`\n- `yls_prepare_with_settings`\n\nTo interact with the tested YLS use `Context` obtained by calling the fixture.\nFor more information about the `Context` class checkout\n[plugin.py](https://github.com/avast/yls/blob/master/pytest-yls/pytest_yls/plugin.py).\n\n### Example test\n\n```python\n\n# Add yls_prepare fixture\ndef test_completion_basic(yls_prepare):\n    # Prepare the tested file\n    # <$> marks the cursor position\n    contents = """rule test {\n    condition:\n        <$>\n}"""\n    \n    # Initialize the testing context by calling the fixture\n    context = yls_prepare(contents)\n\n    # You can now simulate requests on the context\n    # In this case we trigger the code completion\n    response = context.send_request(\n        methods.COMPLETION,\n        types.CompletionParams(\n            textDocument=types.TextDocumentIdentifier(uri=context.opened_file.as_uri()),\n            position=context.get_cursor_position(),\n        ),\n    )\n\n    # Assert the response how you want\n    assert response\n    for module in ["cuckoo", "elf", "pe", "time"]:\n        assert any(\n            module in item["label"] for item in response["items"]\n        ), f"{module=} is not in response"\n```\n\nFor more inspiration check out\n[yls/tests](https://github.com/avast/yls/tree/master/tests).\n\n## License\n\nCopyright (c) 2022 Avast Software, licensed under the MIT license. See the\n[`LICENSE`](https://github.com/avast/yls/blob/master/pytest-yls/LICENSE) file\nfor more details.\n',
    'author': 'Matej Kastak',
    'author_email': 'matej.kastak@avast.com',
    'maintainer': 'Matej Kašťák',
    'maintainer_email': 'matej.kastak@avast.com',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
