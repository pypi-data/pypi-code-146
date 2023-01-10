# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bittrade_kraken_rest',
 'bittrade_kraken_rest.connection',
 'bittrade_kraken_rest.endpoints',
 'bittrade_kraken_rest.endpoints.private',
 'bittrade_kraken_rest.endpoints.public',
 'bittrade_kraken_rest.exceptions',
 'bittrade_kraken_rest.models',
 'bittrade_kraken_rest.models.private',
 'bittrade_kraken_rest.models.websocket']

package_data = \
{'': ['*']}

install_requires = \
['orjson>=3.8.3,<4.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'reactivex>=4.0.4,<5.0.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'bittrade-kraken-rest',
    'version': '0.12.3',
    'description': 'Kraken REST library',
    'long_description': '# ELM Bittrade\'s Kraken REST package & optional CLI\n\n## Install\n\n`pip install bittrade-kraken-rest` or `poetry add bittrade-kraken-rest`\n\nNot all Kraken endpoints are implemented yet.\n\n# Public endpoints\n\n```python\nfrom bittrade_kraken_rest import get_server_time\n\nserver_time = get_server_time().run()\nprint(server_time) # GetServerTimeResult(unixtime=1673053481, rfc1123=\'Sat, 07 Jan 23 01:04:41 +0000\')\n```\n\n*The above example is complete, it should run as is*\n\nBring Your Own ~~Credentials~~ Signature (Private endpoints)\n---\n\nTLDR; Don\'t agree to pass your API secret to third-party code; instead sign the requests yourself, with your own code. It\'s safer.\n\nThis library doesn\'t want to ever access your Kraken secret keys.\n\nMost libraries expect you to provide your api key and secret. I\'m not comfortable doing that with third-party code, even open sourced.\n\nHere instead, the library prepares the request, which you then sign using your own code and the library finishes the job. It has NO access to your secret.\n\nThankfully this is quite straightforward: you need to implement a `sign(x: tuple[PreparedRequest, str, dict[str, Any]]) -> PreparedRequest` method which sets the correct headers. Below is an example of such a signature function:\n\n```python\nfrom os import getenv\nimport urllib, hmac, base64, hashlib\nfrom pathlib import Path\n\n# Taken from https://docs.kraken.com/rest/#section/Authentication/Headers-and-Signature\ndef generate_kraken_signature(urlpath, data, secret):\n    post_data = urllib.parse.urlencode(data)\n    encoded = (str(data["nonce"]) + post_data).encode()\n    message = urlpath.encode() + hashlib.sha256(encoded).digest()\n    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)\n    signature_digest = base64.b64encode(mac.digest())\n    return signature_digest.decode()\n\n# Here the key/secret are loaded from a .gitignored folder, but you can use environment variables or other method of configuration\ndef sign(x: tuple[PreparedRequest, str, dict[str, Any]]):\n    request, url, data = x\n    request.headers["API-Key"] = Path("./config_local/key").read_text()\n    request.headers["API-Sign"] = generate_kraken_signature(\n        url, data, Path("./config_local/secret").read_text()\n    )\n    return request\n\n```\n\nWith that in place, a observable pipe will get you the result you need:\n\n\n```python\nfrom bittrade_kraken_rest import get_websockets_token_request, get_websockets_token_result\nfrom reactivex import operators\n\nresult = get_websockets_token_request().pipe(\n    operators.map(sign),\n    get_websockets_token_result()\n).run()\n```\n\n### Full example with signature function\n\n```python\nfrom os import getenv\nimport urllib, hmac, base64, hashlib\nfrom pathlib import Path\nfrom bittrade_kraken_rest import get_websockets_token_request, get_websockets_token_result\nfrom reactivex import operators\n\n# Taken from https://docs.kraken.com/rest/#section/Authentication/Headers-and-Signature\ndef generate_kraken_signature(urlpath, data, secret):\n    post_data = urllib.parse.urlencode(data)\n    encoded = (str(data["nonce"]) + post_data).encode()\n    message = urlpath.encode() + hashlib.sha256(encoded).digest()\n    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)\n    signature_digest = base64.b64encode(mac.digest())\n    return signature_digest.decode()\n\n# Here the key/secret are loaded from a .gitignored folder, but you can use environment variables or other method of configuration\ndef sign(x: tuple[PreparedRequest, str, dict[str, Any]]):\n    request, url, data = x\n    request.headers["API-Key"] = Path("./config_local/key").read_text()\n    request.headers["API-Sign"] = generate_kraken_signature(\n        url, data, Path("./config_local/secret").read_text()\n    )\n    return request\n\nresult = get_websockets_token_request().pipe(\n    operators.map(sign),\n    get_websockets_token_result()\n).run()\n\n```\n\n*The above example is complete, it should run as is*\n\n### Observables\n\nThe above examples use `.run()` to trigger the observable subscription but Observables make it very easy to create pipes, retries and more. All operators can be found on the [RxPy read the docs](https://rxpy.readthedocs.io/en/latest/).\n\n## Tests\n\n```\npytest\n```\n\nNote that integration tests require a valid key/secret pair saved as `key` and `secret` files in a `.config_local` folder placed at the root of the repo.\n\n## CLI\n\n\nThe CLI has been moved to [its own repo](https://github.com/TechSpaceAsia/bittrade-kraken-cli)\n',
    'author': 'Matt Kho',
    'author_email': 'matt@techspace.asia',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/TechSpaceAsia/bittrade-kraken-rest',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
