# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thumbnails_readme']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.4.0,<10.0.0', 'pdf2image>=1.16.2,<2.0.0']

setup_kwargs = {
    'name': 'thumbnails-readme',
    'version': '0.1.2',
    'description': 'Create thumbnails from Git folders',
    'long_description': '# thumbnails-readme --- Create thumbnails\n\n---\n![PyPI Version](https://img.shields.io/pypi/v/thumbnails-readme.svg)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/thumbnails-readme.svg)\n[![Downloads](https://pepy.tech/badge/thumbnails-readme)](https://pepy.tech/project/thumbnails-readme)\n[![GitHub license](https://img.shields.io/github/license/firefly-cpp/thumbnails-readme.svg)](https://github.com/firefly-cpp/thumbnails-readme/blob/master/LICENSE)\n![GitHub commit activity](https://img.shields.io/github/commit-activity/w/firefly-cpp/thumbnails-readme.svg)\n[![Average time to resolve an issue](http://isitmaintained.com/badge/resolution/firefly-cpp/thumbnails-readme.svg)](http://isitmaintained.com/project/firefly-cpp/thumbnails-readme "Average time to resolve an issue")\n[![Percentage of issues still open](http://isitmaintained.com/badge/open/firefly-cpp/thumbnails-readme.svg)](http://isitmaintained.com/project/firefly-cpp/thumbnails-readme "Percentage of issues still open")\n\n## Description\nThe "thumbnails-readme" package is a simple library devoted to automatically generating thumbnails from a directory. It is explicitly designed to create thumbnails from Git folders and show thumbnails in the README file of that Git folder.\n\n## How it works?\n\nFirst step: program finds graphical material in your directories\n* [\'fig1.pdf\', \'fig2.pdf\', \'fig3.pdf\', \'fig4.pdf\']\n\nSecond step: program generates thumbnails for each material identified in folders\n![2023-01-05 10_54_02-000244](https://user-images.githubusercontent.com/33880044/210753771-7612a1c4-c7ec-4c75-9033-69652b816841.png)\n\nThird step: program appends thumbnails into README\n`![Thumbnail](/image_thumbnails/PDFpismenka-interval_thumb.png)`\n\n![2023-01-05 11_06_43-000251](https://user-images.githubusercontent.com/33880044/210754629-b974ba51-781e-4f32-9ce9-519b57a8bfd0.png)\n\n## Installation\n\n```sh\npip install thumbnails-readme\n```\n\n## Additional dependencies\n\n### Windows\nWindows users have to download poppler for Windows. Add poppler\npath in your Python file (see the main example).\n\n``` poppler_path = path/to/your/poppler/bin/ ```\n\nfor example: ```poppler_path = C:/Program Files/poppler-0.68.0/bin```\n\n### Linux\nLinux users can install poppler-utils from the main repositories.\n\n### Example\n\n``` python\n# Maximum thumbnail size - lower the number, smaller the thumbnail\nMAX_SIZE = (128, 128)\n\n# PDF quality, lower the number, lower the quality\npdf_quality = 15\n\n# Skiplist - which directories to ignore\nskiplist = (\n    ".git",\n    )\n\n\n# Path to your directory\npath = os.getcwd()\npath = os.path.dirname(path)\n\n# Path to the folder, you want new thumbnails to be placed in\npath_to_thumbnails_folder = Path(path + "/image_thumbnails")\n\n# Path to README.md file to be written to\npath_to_readme = Path(path + "/README.md")\n```\n\n## Run the script\n\n``` python\n# Prepare thumbnails folder (check if exists, delete old thumbnails and create new ones)\nthumbnails_readme.prepare_thumbnails_folder(path_to_thumbnails_folder)\n\n# Prepare README.md file (check if exists, delete last modifications and place newly generated ones)\nthumbnails_readme.prepare_readme(path_to_readme)\n\n# Generate thumbnails\nthumbnails_readme.generate_thumbnails(path, path_to_thumbnails_folder, path_to_readme, MAX_SIZE, pdf_quality, skiplist)\n```\n\n## License\n\nThis package is distributed under the MIT License. This license can be found online at <http://www.opensource.org/licenses/MIT>.\n\n## Disclaimer\n\nThis framework is provided as-is, and there are no guarantees that it fits your purposes or that it is bug-free. Use it at your own risk!\n',
    'author': 'Rok Kukovec',
    'author_email': 'rok.kukovec1@um.si',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/firefly-cpp/thumbnails-readme',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
