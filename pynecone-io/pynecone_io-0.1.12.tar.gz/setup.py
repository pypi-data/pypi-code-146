# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pynecone',
 'pynecone..templates.app',
 'pynecone.compiler',
 'pynecone.components',
 'pynecone.components.base',
 'pynecone.components.datadisplay',
 'pynecone.components.disclosure',
 'pynecone.components.feedback',
 'pynecone.components.forms',
 'pynecone.components.graphing',
 'pynecone.components.layout',
 'pynecone.components.libs',
 'pynecone.components.media',
 'pynecone.components.navigation',
 'pynecone.components.overlay',
 'pynecone.components.tags',
 'pynecone.components.typography',
 'pynecone.middleware']

package_data = \
{'': ['*'],
 'pynecone': ['.templates/assets/*',
              '.templates/web/*',
              '.templates/web/pages/*',
              '.templates/web/styles/code/*',
              '.templates/web/utils/*']}

install_requires = \
['fastapi>=0.88.0,<0.89.0',
 'gunicorn>=20.1.0,<21.0.0',
 'httpx>=0.23.1,<0.24.0',
 'plotly>=5.10.0,<6.0.0',
 'pydantic==1.10.2',
 'redis>=4.3.5,<5.0.0',
 'rich>=12.6.0,<13.0.0',
 'sqlmodel>=0.0.8,<0.0.9',
 'typer==0.4.2',
 'uvicorn>=0.20.0,<0.21.0',
 'websockets>=10.4,<11.0']

entry_points = \
{'console_scripts': ['pc = pynecone.pc:main']}

setup_kwargs = {
    'name': 'pynecone-io',
    'version': '0.1.12',
    'description': 'The easiest way to build web apps.',
    'long_description': '<div align="center">\n\n<h1 align="center">\n  <img width="600" src="docs/images/logo.svg#gh-light-mode-only" alt="Pynecone Logo">\n  <img width="600" src="docs/images/logo_white.svg#gh-dark-mode-only" alt="Pynecone Logo">\n</h1>\n\n**Build performant, customizable web apps in pure Python.**\n\n[![PyPI version](https://badge.fury.io/py/pynecone-io.svg)](https://badge.fury.io/py/pynecone-io)\n![tests](https://github.com/pynecone-io/pynecone/actions/workflows/build.yml/badge.svg)\n![versions](https://img.shields.io/pypi/pyversions/pynecone-io.svg)\n[![License](https://img.shields.io/badge/License-Apache_2.0-yellowgreen.svg)](https://opensource.org/licenses/Apache-2.0)  \n\n<div align="left">\n\n## Getting Started\n\nPynecone is a full-stack Python framework that makes it easy to build and deploy web apps in minutes. All the information for getting started can be found in this README. However, a more detailed explanation of the following topics can be found on our website:\n\n<div align="center">\n\n### [Docs](https://pynecone.io/docs/getting-started/introduction) | [Component Library](https://pynecone.io/docs/library) | [Gallery](https://pynecone.io/docs/gallery) | [Deployment](https://pynecone.io/docs/hosting/deploy) \n\n<div align="left">\n\n## Installation\n  \nPynecone requires the following to get started:\n\n* Python 3.7+\n* [Node.js 12.22.0+](https://nodejs.org/en/) (Don\'t worry, you\'ll never have to write any Javascript)\n\n```\n$ pip install pynecone-io\n```\n\n*NOTE:* Make sure you install the correct package: `pynecone-io`, not `pynecone`.\n\n## Create your first Pynecone App\n\nInstalling Pynecone also installs the `pc` command line tool. Test that the install was successful by creating a new project. \n\nReplace my_app_name with your project name:\n\n```\n$ mkdir my_app_name\n$ cd my_app_name\n$ pc init\n```\n\nWhen you run this command for the first time, we will download and install `bun` automatically.\n\nThis command initializes a template app in your new directory.\nYou can run this app in development mode:\n```\n$ pc run\n```\n\nYou should see your app running at http://localhost:3000. (Note that the port may be different if you have another app running on port 3000, please notice the terminal output)\n\n\nNow you can modify the source code in `my_app_name/my_app_name.py`. Pynecone has fast refreshes so you can see your changes instantly when you save your code.\n\n\n## Example Pynecone App\n\nLet\'s go over an example of creating a UI around Dalle. For simplicity of the example below, we call the OpenAI Dalle API, but you could replace this with any ML model locally.\n\n<div align="center">\n<img src="docs/images/dalle.gif" alt="drawing" width="550" style="border-radius:2%"/>\n<div align="left">\n\nHere is the complete code to create this. This is all done in one Python file!\n\n```python\nimport pynecone as pc\nimport openai\n\nopenai.api_key = "YOUR_API_KEY"\n\nclass State(pc.State):\n    """The app state."""\n    prompt = ""\n    image_url = ""\n    image_processing = False\n    image_made = False\n\n    def process_image(self):\n        """Set the image processing flag to true and indicate image is not made yet."""\n        self.image_processing = True\n        self.image_made = False        \n\n    def get_image(self):\n        """Get the image from the prompt."""\n        response = openai.Image.create(prompt=self.prompt, n=1, size="1024x1024")\n        self.image_url = response["data"][0]["url"]\n        self.image_processing = False\n        self.image_made = True\n\ndef index():\n    return pc.center(\n        pc.vstack(\n            pc.heading("DALL-E", font_size="1.5em"),\n            pc.input(placeholder="Enter a prompt..", on_blur=State.set_prompt),\n            pc.button(\n                "Generate Image",\n                on_click=[State.process_image, State.get_image],\n                width="100%",\n            ),\n            pc.divider(),\n            pc.cond(\n                State.image_processing,\n                pc.circular_progress(is_indeterminate=True),\n                pc.cond(\n                     State.image_made,\n                     pc.image(\n                         src=State.image_url,\n                         height="25em",\n                         width="25em",\n                    )\n                )\n            ),\n            bg="white",\n            padding="2em",\n            shadow="lg",\n            border_radius="lg",\n        ),\n        width="100%",\n        height="100vh",\n        bg="radial-gradient(circle at 22% 11%,rgba(62, 180, 137,.20),hsla(0,0%,100%,0) 19%)",\n    )\n\n# Add state and page to the app.\napp = pc.App(state=State)\napp.add_page(index, title="Pynecone:DALL-E")\napp.compile()\n```\nLet\'s break this down.\n\n### **UI In Pynecone**\n\nLets start by talking about the UI this Pynecone App.\n\n```python \ndef index():\n    return pc.center(\n        ...\n    )\n```\nThis index function defines the frontend of the app. We use different components such as `center`, `vstack`, `input`, and `button` to build the front end. Components can be nested to create complex layouts and styled using CSS\'s full power. Just pass them in as keyword args.\n\nPynecone comes with [50+ built-in components](https://pynecone.io/docs/library) to help you get started. We are actively adding more components, plus it\'s easy to create your own components.\n\n### **State**\n\n``` python\nclass State(pc.State):\n    """The app state."""\n    prompt = ""\n    image_url = ""\n    image_processing = False\n    image_made = False\n```\nThe state defines all the variables (called vars) in an app that can change and the functions that change them.\nHere the state is comprised of a `prompt` and `image_url`. There are also the booleans `image_processing` and `image_made` to indicate when to show the circular progress and image.\n\n### **Event Handlers**\n\n```python\n    def process_image(self):\n        """Set the image processing flag to true and indicate image is not made yet."""\n        self.image_processing = True\n        self.image_made = False        \n\n    def get_image(self):\n        """Get the image from the prompt."""\n        response = openai.Image.create(prompt=self.prompt, n=1, size="1024x1024")\n        self.image_url = response["data"][0]["url"]\n        self.image_processing = False\n        self.image_made = True\n```\nWithin the state, we define functions called event handlers that change the state vars. Event handlers are the way that we can modify the state in Pynecone. They can be called in response to user actions, such as clicking a button or typing in a text box. These actions are called events.\n\nOur dalle app has two event handlers, `process_image` to indicate that the image is being generated and `get_image`, which calls the OpenAI API.\n\n### **Routing** \n\nFinally we define our app and tell it what state to use.\n```python\napp = pc.App(state=State)\n```\nWe add a route from the root of the app to the index component. We also add a title that will show up in the page preview/ browser tab.\n```python\napp.add_page(index, title="Pynecone:DALL-E")\napp.compile()\n```\nYou can create a multi-page app by adding more routes.\n\n## Status\n\nAs of December 2022, Pynecone has just been released publicly and is in the **Alpha Stage**.\n\n - :large_orange_diamond: **Public Alpha**: Anyone can install and use Pynecone. There may be issues, but we are working to resolve them activly.\n - **Public Beta**: Stable enough for non-enterprise use-cases.\n - **Public Hosting Beta**: **Optionally** Deploy and Host your own apps on Pynecone!\n - **Public**: Pynecone is production ready.\n\nPynecone has new releases and features coming every week! Make sure to: :star: star and :eyes: watch this repository to stay up to date.\n \n## Contributing\n\nWe welcome contributions of any size! Below are some good ways to get started in the Pynecone community.\n\n- **GitHub Discussions**: A great way to talk about features you want added or things that are confusing/need clarification.\n- **GitHub Issues**: These are an excellent way to report bugs. Additionally, you can try and solve an existing issue and submit a PR.\n\nWant to join our Pynecone team or learn more about our framework? Send us an email [here](mailto:founders@pynecone.io), and we can schedule a call to discuss Pynecone and how you can start contributing.\n\nWe are actively looking for contributors, no matter your skill level or experience.\n\n## More Information \n\nMore information about Pynecone can be found on our website:\n- [pynecone.io](https://pynecone.io)\n  \nJoin Our Discord:\n- [Discord Link](https://discord.gg/T5WSbC2YtQ)\n\n## License\n\nPynecone is open-source and licensed under the [Apache License 2.0](LICENSE).\n\n## Contributors\n\n<a href="https://github.com/picklelo"><img src="https://avatars.githubusercontent.com/u/6270214?v=4" width="50" height="50" alt=""/></a> \n<a href="https://github.com/Alek99"><img src="https://avatars.githubusercontent.com/u/38776361?s=400&u=bd6c163fe787c2de1a26c881598e54b67e2482dd&v=4" width="50" height="50" alt=""/></a> \n<a href="https://github.com/kbrgl"><img src="https://avatars.githubusercontent.com/u/13417496?v=4" width="50" height="50" alt=""/></a> \n<a href="https://github.com/Lendemor"><img src="https://avatars.githubusercontent.com/u/4015177?v=4" width="50" height="50" alt=""/></a> \n<a href="https://github.com/FHU-yezi"><img src="https://avatars.githubusercontent.com/u/50828953?v=4" width="50" height="50" alt=""/></a> \n',
    'author': 'Nikhil Rao',
    'author_email': 'nikhil@pynecone.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pynecone.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
