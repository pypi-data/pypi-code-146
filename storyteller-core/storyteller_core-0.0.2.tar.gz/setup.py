# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['storyteller']

package_data = \
{'': ['*']}

install_requires = \
['diffusers>=0.11.1,<0.12.0',
 'nltk>=3.8.1,<4.0.0',
 'pre-commit[dev]>=2.21.0,<3.0.0',
 'soundfile>=0.11.0,<0.12.0',
 'transformers>=4.25.1,<5.0.0',
 'tts>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['storyteller = storyteller.cli:main']}

setup_kwargs = {
    'name': 'storyteller-core',
    'version': '0.0.2',
    'description': 'Multimodal AI Story Teller, built with Stable Diffusion, GPT, and neural text-to-speech',
    'long_description': '# StoryTeller\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\nA multimodal AI story teller, built with [Stable Diffusion](https://huggingface.co/spaces/stabilityai/stable-diffusion), GPT, and neural text-to-speech (TTS).\n\nGiven a prompt as an opening line of a story, GPT writes the rest of the plot; Stable Diffusion draws an image for each sentence; a TTS model narrates each line, resulting in a fully animated video of a short story, replete with audio and visuals.\n\n![out](https://user-images.githubusercontent.com/25360440/210071764-51ed5872-ba56-4ed0-919b-d9ce65110185.gif)\n\n## Installation\n\n### PyPI\n\nStory Teller is available on [PyPI](https://pypi.org/project/storyteller-core/).\n\n```\n$ pip install storyteller-core\n```\n\n### Source\n\n1. Clone the repository.\n\n```\n$ git clone https://github.com/jaketae/storyteller.git\n$ cd storyteller\n```\n\n2. Install dependencies.\n\n```\n$ pip install .\n```\n\n*Note: For Apple M1/2 users, [`mecab-python3`](https://github.com/SamuraiT/mecab-python3) is not available. You need to install `mecab` before running `pip install`. You can do this with [Hombrew](https://www.google.com/search?client=safari&rls=en&q=homebrew&ie=UTF-8&oe=UTF-8) via `brew install mecab`. For more information, refer to [this issue](https://github.com/SamuraiT/mecab-python3/issues/84).*\n\n\n3. (Optional) To develop locally, install `dev` dependencies and install pre-commit hooks. This will automatically trigger linting and code quality checks before each commit.\n\n```\n$ pip install -e .[dev]\n$ pre-commit install\n```\n\n## Quickstart\n\nThe quickest way to run a demo is through the CLI. Simply type\n\n```\n$ storyteller\n```\n\nThe final video will be saved as `/out/out.mp4`, alongside other intermediate images, audio files, and subtitles.\n\nTo adjust the defaults with custom parametes, toggle the CLI flags as needed.\n\n```\n$ storyteller --help\nusage: storyteller [-h] [--writer_prompt WRITER_PROMPT]\n                   [--painter_prompt_prefix PAINTER_PROMPT_PREFIX] [--num_images NUM_IMAGES]\n                   [--output_dir OUTPUT_DIR] [--seed SEED] [--max_new_tokens MAX_NEW_TOKENS]\n                   [--writer WRITER] [--painter PAINTER] [--speaker SPEAKER]\n                   [--writer_device WRITER_DEVICE] [--painter_device PAINTER_DEVICE]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --writer_prompt WRITER_PROMPT\n  --painter_prompt_prefix PAINTER_PROMPT_PREFIX\n  --num_images NUM_IMAGES\n  --output_dir OUTPUT_DIR\n  --seed SEED\n  --max_new_tokens MAX_NEW_TOKENS\n  --writer WRITER\n  --painter PAINTER\n  --speaker SPEAKER\n  --writer_device WRITER_DEVICE\n  --painter_device PAINTER_DEVICE\n```\n\n## Usage\n\nFor more advanced use cases, you can also directly interface with Story Teller in Python code.\n\n1. Load the model with defaults.\n\n```python\nfrom storyteller import StoryTeller\n\nstory_teller = StoryTeller.from_default()\nstory_teller.generate(...)\n```\n\n2. Alternatively, configure the model with custom settings.\n\n```python\nfrom storyteller import StoryTeller, StoryTellerConfig\n\nconfig = StoryTellerConfig(\n    writer="gpt2-large",\n    painter="CompVis/stable-diffusion-v1-4",\n    max_new_tokens=100,\n)\n\nstory_teller = StoryTeller(config)\nstory_teller.generate(...)\n```\n\n## License\n\nReleased under the [MIT License](LICENSE).\n',
    'author': 'Jaesung Tae',
    'author_email': 'jaesungtae@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
