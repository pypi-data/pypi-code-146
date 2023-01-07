# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['manim_voiceover',
 'manim_voiceover.services',
 'manim_voiceover.services.coqui',
 'manim_voiceover.services.recorder']

package_data = \
{'': ['*']}

install_requires = \
['humanhash3>=0.0.6,<0.0.7',
 'manim',
 'mutagen>=1.46.0,<2.0.0',
 'pip>=21.0.1',
 'pydub>=0.25.1,<0.26.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'sox>=1.4.1,<2.0.0']

extras_require = \
{'all': ['azure-cognitiveservices-speech>=1.24.0,<2.0.0',
         'PyAudio>=0.2.12,<0.3.0',
         'gTTS>=2.2.4,<3.0.0',
         'pyttsx3>=2.90,<3.0',
         'pynput>=1.7.6,<2.0.0',
         'playsound>=1.3.0,<2.0.0'],
 'azure': ['azure-cognitiveservices-speech>=1.24.0,<2.0.0'],
 'gtts': ['gTTS>=2.2.4,<3.0.0'],
 'pyttsx3': ['pyttsx3>=2.90,<3.0'],
 'recorder': ['PyAudio>=0.2.12,<0.3.0',
              'pynput>=1.7.6,<2.0.0',
              'playsound>=1.3.0,<2.0.0']}

entry_points = \
{'manim.plugins': ['manim_voiceover = manim_voiceover']}

setup_kwargs = {
    'name': 'manim-voiceover',
    'version': '0.2.2',
    'description': 'Manim plugin for all things voiceover',
    'long_description': '# Manim Voiceover\n\n<p>\n    <a href="https://github.com/ManimCommunity/manim-voiceover/workflows/Build/badge.svg"><img src="https://github.com/ManimCommunity/manim-voiceover/workflows/Build/badge.svg" alt="Github Actions Status"></a>\n    <a href="https://pypi.org/project/manim_voiceover/"><img src="https://img.shields.io/pypi/v/manim_voiceover.svg?style=flat&logo=pypi" alt="PyPI Latest Release"></a>\n    <a href="https://pepy.tech/project/manim_voiceover"><img src="https://pepy.tech/badge/manim_voiceover/month?" alt="Downloads"> </a>\n    <a href="https://manim_voiceover.readthedocs.io/en/latest/?badge=latest"><img src="https://readthedocs.org/projects/manim_voiceover/badge/?version=latest" alt="Documentation Status"></a>\n    <a href="https://github.com/ManimCommunity/manim-voiceover/blob/main/LICENSE"><img src="https://img.shields.io/github/license/ManimCommunity/manim-voiceover.svg?color=blue" alt="License"></a>\n    <a href="https://manim.community/discord"><img src="https://dcbadge.vercel.app/api/server/qY23bthHTY?style=flat" alt="Discord"></a>\n</p>\n\nManim Voiceover is a [Manim](https://manim.community) plugin for all things voiceover:\n\n- Add voiceovers to Manim videos *directly in Python* without having to use a video editor.\n- Record voiceovers with your microphone during rendering with a simple command line interface.\n- Develop animations with auto-generated AI voices from various free and proprietary services.\n- Per-word timing of animations, i.e. trigger animations at specific words in the voiceover, even for the recordings. This works thanks to [OpenAI Whisper](https://github.com/openai/whisper).\n\nHere is a demo:\n\nhttps://user-images.githubusercontent.com/2453968/198145393-6a1bd709-4441-4821-8541-45d5f5e25be7.mp4\n\nCurrently supported TTS services (aside from the CLI that allows you to records your own voice):\n\n- [Azure Text to Speech](https://azure.microsoft.com/en-us/services/cognitive-services/text-to-speech/) (Recommended for AI voices)\n- [Coqui TTS](https://github.com/coqui-ai/TTS/)\n- [gTTS](https://github.com/pndurette/gTTS/)\n- [pyttsx3](https://github.com/nateshmbhat/pyttsx3)\n\n[Check out the documentation for more details.](https://voiceover.manim.community/)\n\n## Installation\n\n[Installation instructions in Manim Voiceover docs.](https://voiceover.manim.community/en/latest/installation.html)\n\n## Get started\n\n[Check out the docs to get started with Manim Voiceover.](https://voiceover.manim.community/en/latest/quickstart.html)\n\n## Examples\n\n[Check out the example gallery to get inspired.](https://voiceover.manim.community/en/latest/examples.html)\n\n\n',
    'author': 'The Manim Community Developers',
    'author_email': 'contact@manim.community',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://voiceover.manim.community',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
