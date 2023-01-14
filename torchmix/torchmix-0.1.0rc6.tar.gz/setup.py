# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torchmix',
 'torchmix.components',
 'torchmix.components.containers',
 'torchmix.core',
 'torchmix.nn',
 'torchmix.third_party']

package_data = \
{'': ['*']}

install_requires = \
['einops>=0.6.0', 'hydra-core>=1.0.0', 'hydra-zen>=0.8.0', 'jaxtyping>=0.2.0']

setup_kwargs = {
    'name': 'torchmix',
    'version': '0.1.0rc6',
    'description': 'A collection of useful PyTorch modules',
    'long_description': '<h1 align="center">torchmix</h1>\n\n<h3 align="center">The missing component library for PyTorch</h3>\n\n<br />\n\n`torchmix` is a collection of PyTorch modules that aims to simplify your model development process with pre-made PyTorch components. We\'ve included a range of operations, from basic ones like `Repeat` and `Add`, to more complex ones like `WindowAttention` in the [Swin-Transformer](https://arxiv.org/abs/2103.14030). Our goal is to make it easy for you to use these various operations with minimal code, so you can focus on building your project rather than writing boilerplate.\n\nWe\'ve designed `torchmix` to be as user-friendly as possible. Each implementation is kept minimal and easy to understand, using [`einops`](https://github.com/arogozhnikov/einops) to avoid confusing tensor manipulation (such as `permute`, `transpose`, and `reshape`) and [`jaxtyping`](https://github.com/google/jaxtyping) to clearly document the shapes of the input and output tensors. This means that you can use `torchmix` with confidence, knowing that the components you\'re working with are clean and reliable.\n\n**Note: `torchmix` is a prototype that is currently in development and has not been tested for production use. The API may change at any time.**\n\n## Install\n\nTo use `torchmix`, you will need to have `torch` already installed on your environment.\n\n```sh\npip install torchmix\n```\n\n## Documentation\n\nTo learn more, check out our [documentation](https://torchmix.vercel.app).\n\n## Contributing\n\nThe development of `torchmix` is an open process, and we welcome any contributions or suggestions for improvement. If you have ideas for new components or ways to enhance the library, feel free to open an issue or start a discussion. We welcome all forms of feedback, including criticism and suggestions for significant design changes. Please note that `torchmix` is currently in the early stages of development and any contributions should be considered experimental. Thank you for your support of `torchmix`!\n\n## License\n\n`torchmix` is licensed under the MIT License.\n',
    'author': 'junhsss',
    'author_email': 'junhsssr@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
