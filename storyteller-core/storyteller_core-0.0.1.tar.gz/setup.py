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
 'soundfile>=0.11.0,<0.12.0',
 'transformers>=4.25.1,<5.0.0',
 'tts>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['storyteller = storyteller.__main__:main']}

setup_kwargs = {
    'name': 'storyteller-core',
    'version': '0.0.1',
    'description': 'Multimodal AI Story Teller, built with Stable Diffusion, GPT, and neural text-to-speech',
    'long_description': '# StoryTeller\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\nA multimodal AI story teller, built with [Stable Diffusion](https://huggingface.co/spaces/stabilityai/stable-diffusion), GPT, and neural text-to-speech (TTS).\n\nGiven a prompt as an opening line of a story, GPT writes the rest of the plot; Stable Diffusion draws an image for each sentence; a TTS model narrates each line, resulting in a fully animated video of a short story, replete with audio and visuals.\n\n![out](https://user-images.githubusercontent.com/25360440/210071764-51ed5872-ba56-4ed0-919b-d9ce65110185.gif)\n\n\n## Quickstart\n\n1. Clone the repository.\n\n```\n$ git clone https://github.com/jaketae/storyteller.git\n```\n\n2. Install package requirements.\n\n```\n$ pip install --upgrade pip wheel\n$ pip install -e .\n# for dev requirements, do:\n# pip install -e .[dev]\n```\n\n3. Run the demo. The final video will be saved as `/out/out.mp4`, alongside other intermediate images, audio files, and subtitles.\n\n```\n$ storyteller\n# alternatively with make, do:\n# make run\n```\n\n## Usage\n\n1. Load the model with defaults.\n\n```python\nfrom storyteller import StoryTeller\n\nstory_teller = StoryTeller.from_defaults()\nstory_teller.generate(...)\n```\n\n2. Alternatively, configure the model with custom settings.\n\n```python\nfrom storyteller import StoryTeller, StoryTellerConfig\n\nconfig = StoryTellerConfig(\n    writer="gpt2-large",\n    painter="CompVis/stable-diffusion-v1-4",\n    max_new_tokens=100,\n    diffusion_prompt_prefix="Van Gogh style",\n)\n\nstory_teller = StoryTeller(config)\nstory_teller.generate(...)\n```\n\n## License\n\nReleased under the [MIT License](LICENSE).\n',
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
