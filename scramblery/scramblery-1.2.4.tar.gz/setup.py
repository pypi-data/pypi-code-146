# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scramblery']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'scramblery',
    'version': '1.2.4',
    'description': '',
    'long_description': ' # Scramblery\n[![Downloads](https://pepy.tech/badge/scramblery)](https://pepy.tech/project/scramblery)\n[![PyPI version](https://badge.fury.io/py/scramblery.svg)](https://badge.fury.io/py/scramblery)\n[![Jekyll site CI](https://github.com/altunenes/scramblery/actions/workflows/jekyll.yml/badge.svg)](https://github.com/altunenes/scramblery/actions/workflows/jekyll.yml)\n[![Build status](https://ci.appveyor.com/api/projects/status/amuravq7o2afvv65?svg=true)](https://ci.appveyor.com/project/altunenes/scramblery)\n\nA simple tool to scramble your images or only faces from images or videos. You can find the online demo in javascript [here](https://altunenes.github.io/scramblery/scramblerydemo.html). For more information, please visit the [documentation](https://altunenes.github.io/scramblery/).\n\n\n#### Purpose of Package\n The purpose of this package is the creating scrambled images from images or videos. User can either scramble the whole image or only facial area.\n This is very useful tool in psychology experiments especially if you are working with faces. With a for loop you can scramble all the images in a folder and create a new folder with scrambled images. It was very long process to scramble images manually in the past and I feel like this package can be useful for many people. Hope this package will be useful for your research.\n\n#### Motivation\n\n- Image scrambling is important in psychology experiments because it allows researchers to control the content and structure of visual stimuli, while removing or altering specific features or patterns that might influence participants\' perception or response.\n\n- By scrambling an image, researchers can create a version of the image that preserves the overall luminance, contrast, and spatial layout, but that removes or distorts specific features or patterns that might be relevant for the experiment. For example, researchers might scramble an image of a face to remove the facial features, while preserving the overall brightness and contrast, or they might scramble an image of a scene to remove the objects, while preserving the spatial layout and color.\n  \n- It allows researchers to control for potential confounds and biases that might arise from the content of the stimuli. By removing or distorting specific features or patterns, researchers can create stimuli that are less predictable and less likely to elicit specific responses from participants. This can help researchers to isolate the effects of the manipulated variables, and to reduce the influence of confounding factors that might interfere with the interpretation of the results.\n\n#### **Features**\n- Scramble whole image with desired degree of scrambling (pixel values or pixel coordinates)\n- Scramble only facial area with desired degree of scrambling (pixel values or pixel coordinates)\n- Scramble only facial area in a video (useful for dynmaic stimuli) with desired degree of scrambling\n\n#### Installation\n- The package can be found in pypi. To install the package, run the following command in the terminal:\n- `pip install scramblery`\n#### Author\n\n  -  Main Maintainer: [Enes ALTUN]\n\n\n#### Usage\nAfter installing the package, you can import the package as follows:\n- `from scramblery import scramblery`\nThen use the functions as follows to scramble images. I added some examples below (see on the Github page)\n\n\nCode example:\n```python\nfrom scramblery import scramblery\nscramblery.scrambleimage("Lena.png", x_block=10, y_block=10, scramble_type=\'classic\',seed=None,write=True)\n#note: seed is optional, none means random seed\n```\nIf you want to scramble images in a folder, check the API section here for an example: [API](https://altunenes.github.io/scramblery/userguide/).\n\n\n#### Javascript Demo\n\nUpdate:\nAlso, with the same paradigm, I have created an animated version of scramblery. It\'s shuffling pixel values and coordinates in a given ratio then it\'s arranging them back in the original order. You can find the online demo in javascript [here](https://altunenes.github.io/scramblery/magic.html).\n\nexample (gif animation):\n\n\n### Contributon\n Any kind of contribution is welcome.\n',
    'author': 'altunenes',
    'author_email': 'enesaltun2@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/altunenes/scramblery',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
