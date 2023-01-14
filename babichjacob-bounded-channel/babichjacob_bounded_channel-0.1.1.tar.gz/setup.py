# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bounded_channel']

package_data = \
{'': ['*']}

install_requires = \
['babichjacob-option-and-result>=0.1.2,<0.2.0']

setup_kwargs = {
    'name': 'babichjacob-bounded-channel',
    'version': '0.1.1',
    'description': 'A Python implementation of tokio::sync::mpsc::channel',
    'long_description': '<h1 align="center">🪢 Bounded Channel</h1>\n\nThis library uses documentation copied and pasted from [Tokio\'s `sync::mpsc` library](https://docs.rs/tokio/latest/tokio/sync/mpsc/index.html), which they have generously published under the MIT license. 🙏\n\nThis is a Python implementation of [their bounded channel](https://docs.rs/tokio/latest/tokio/sync/mpsc/fn.channel.html).\n\n## 💻 Installation\n\nThis package is [published to PyPI as `babichjacob-bounded-channel`](https://pypi.org/project/babichjacob-bounded-channel/).\n\n## 🛠 Usage\n\n```py\nfrom asyncio import create_task, gather, run, sleep\nfrom itertools import count\n\nfrom bounded_channel import bounded_channel, Receiver, Sender\n\n\nasync def producer(sender: Sender[int]):\n    "Produces integer values as long as there is a receiver to receive them"\n    for value in count():\n        await sleep(0.02)\n\n        res = await sender.send(value)\n\n        # No receivers are listening anymore\n        if res.is_err():\n            break\n\n\nasync def consumer(receiver: Receiver[int]):\n    async for value in receiver:\n        await sleep(0.03)\n\n        print("received", value)\n\n        if value >= 100:\n            # Signal to please stop producing values\n            receiver.close()\n            # From then on, the remaining buffered values will be received\n            # until they run out for good (to a maximum of 165 or so)\n            # (it\'s dependent on the difference of speed between the producer and consumer)\n\n    # Alternatively, the loop could be broken out of\n    # and any extra buffered values would be ignored\n\n\nasync def main():\n    sender, receiver = bounded_channel(64)\n\n    producer_task = create_task(producer(sender))\n    consumer_task = create_task(consumer(receiver))\n\n    # Drop extra references to the sender and receiver\n    del sender\n    del receiver\n    # so their RAII semantics behave properly\n\n    await gather(producer_task, consumer_task)\n\n\nrun(main())\n```\n\n## 😵 Help! I have a question\n\nCreate an issue and I\'ll try to help.\n\n## 😡 Fix! There is something that needs improvement\n\nCreate an issue or pull request and I\'ll try to fix.\n\n## 📄 License\n\nMIT\n\n## 🙏 Attribution\n\n_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_\n',
    'author': 'J or Jacob Babich',
    'author_email': 'jacobbabichpublic+git@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/babichjacob/python-bounded-channel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10',
}


setup(**setup_kwargs)
