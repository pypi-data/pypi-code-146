# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anime1']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'fake-useragent>=1.1.1,<2.0.0',
 'lxml>=4.9.2,<5.0.0',
 'pathlib>=1.0.1,<2.0.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'anime1',
    'version': '0.1.0',
    'description': 'CLI access to anime1.me (beta)',
    'long_description': '# anime1.py\nCLI access to anime1.me (beta)\n\n![Cover image](cover.png)\n\n## Usage\n\n- Install all dependencies\n- Launch the script\n- Enter URL:\n  - https://anime1.me/19159 plays a single episode\n  - https://anime1.me/category/2022%e5%b9%b4%e7%a7%8b%e5%ad%a3/%e5%ad%a4%e7%8d%a8%e6%90%96%e6%bb%be allows you to select episode from series then play it\n- Controls are handled by MPV: https://github.com/mpv-player/mpv\n\n## Legal Issues\n\nAs with similar software like ani-cli and you-get, anime1.py only gathers information from the respective site. \n\nThe legal disclaimer therefore applies here as well. See https://github.com/soimort/you-get\n\n> This software is distributed under the MIT license.\n> In particular, please be aware that\n> > THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n\n> Translated to human words:\n> *In case your use of the software forms the basis of copyright infringement, or you use the software for any other illegal purposes, the authors cannot take any responsibility for you.*\n> We only ship the code here, and how you are going to use it is left to your own discretion.\n\n## Future plans\n\n- Better GUI\n- Integrate into you-get? (far far future)\n',
    'author': 'evnchn',
    'author_email': 'evanchan040511@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
