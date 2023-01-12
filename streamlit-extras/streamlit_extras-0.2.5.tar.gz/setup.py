# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['streamlit_extras',
 'streamlit_extras.add_vertical_space',
 'streamlit_extras.altex',
 'streamlit_extras.annotated_text',
 'streamlit_extras.app_logo',
 'streamlit_extras.badges',
 'streamlit_extras.buy_me_a_coffee',
 'streamlit_extras.camera_input_live',
 'streamlit_extras.card',
 'streamlit_extras.chart_annotations',
 'streamlit_extras.chart_container',
 'streamlit_extras.colored_header',
 'streamlit_extras.customize_running',
 'streamlit_extras.dataframe_explorer',
 'streamlit_extras.echo_expander',
 'streamlit_extras.embed_code',
 'streamlit_extras.faker',
 'streamlit_extras.function_explorer',
 'streamlit_extras.image_coordinates',
 'streamlit_extras.image_in_tables',
 'streamlit_extras.keyboard_text',
 'streamlit_extras.keyboard_url',
 'streamlit_extras.let_it_rain',
 'streamlit_extras.mandatory_date_range',
 'streamlit_extras.markdownlit',
 'streamlit_extras.mention',
 'streamlit_extras.metric_cards',
 'streamlit_extras.no_default_selectbox',
 'streamlit_extras.st_keyup',
 'streamlit_extras.stateful_button',
 'streamlit_extras.stodo',
 'streamlit_extras.stoggle',
 'streamlit_extras.switch_page_button',
 'streamlit_extras.toggle_switch',
 'streamlit_extras.vertical_slider',
 'streamlit_extras.word_importances']

package_data = \
{'': ['*']}

install_requires = \
['htbuilder==0.6.1',
 'markdownlit>=0.0.5',
 'protobuf!=3.20.2',
 'st-annotated-text>=3.0.0',
 'streamlit-camera-input-live>=0.2.0',
 'streamlit-card>=0.0.4',
 'streamlit-embedcode>=0.1.2',
 'streamlit-faker>=0.0.2',
 'streamlit-image-coordinates>=0.1.1,<0.2.0',
 'streamlit-keyup>=0.1.9',
 'streamlit-toggle-switch>=1.0.2',
 'streamlit-vertical-slider>=1.0.2',
 'streamlit>=1.0.0']

setup_kwargs = {
    'name': 'streamlit-extras',
    'version': '0.2.5',
    'description': 'A library to discover, try, install and share Streamlit extras',
    'long_description': '\n<a href="https://extras.streamlitapp.com" title="Python Version"><img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg"></a><br>\n<a href="https://github.com/arnaudmiribel/streamlit-extras/" title="Python Version"><img src="https://img.shields.io/badge/Python-3.9%2B-blue&style=flat"></a>\n<a href="https://badge.fury.io/py/streamlit-extras"><img src="https://badge.fury.io/py/streamlit-extras.svg" alt="PyPI version" height="18"></a>\n<a href="https://hits.seeyoufarm.com"><img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Farnaudmiribel%2Fstreamlit-extras&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=visits&edge_flat=false"/></a>\n\n\n# 🪢 streamlit-extras\n\n\n<strong>A Python library with useful Streamlit extras</strong>\n\n`streamlit-extras` is a Python library putting together useful Streamlit bits of code (<b><i>extras</i></b>).\n\n---\n\n<p align="center">\n     Try out and explore available extras in our playgrounds at <a href="https://extras.streamlitapp.com">extras.streamlitapp.com</a>.<br><br>\n     <img src="https://user-images.githubusercontent.com/7164864/186383332-147e820d-cd02-4962-b8b9-91fe9f675dfe.gif" width="500px"></img>\n</p>\n\n\n\n---\n\n## Highlights\n\n- 📙&nbsp; <b>Discover:</b> Visit the gallery <a href="https://extras.streamlitapp.com">extras.streamlitapp.com</a> to discover all extras in their natural habitat.\n- \U0001f6dd&nbsp; <b>Try:</b> The gallery comes with a Streamlit-based playground for some extras. Try it before you <strike>buy</strike> install it!\n- ⬇️&nbsp; <b>Install:</b> `streamlit-extras` is a PyPI package with all extras included. Get them all using pip!\n- \U0001faf4&nbsp; <b>Share:</b> Go ahead and share your own extras, it\'s just [a PR away](https://extras.streamlitapp.com/Contribute)!\n\n## Getting Started\n\n### Installation\n\n```\npip install streamlit-extras\n```\n\n### Usage\n\nHere\'s an example with one of the easiest extras around, <a href="https://extras.streamlitapp.com/Toggle%20button">stoggle</a>\n```python\nfrom streamlit_extras.stoggle import stoggle\n\nstoggle(\n    "Click me!",\n    """🥷 Surprise! Here\'s some additional content""",\n)\n```\n\n<img src="https://user-images.githubusercontent.com/16867691/192553812-f91c801b-e820-470b-84c6-4563504c6ce5.gif"></img>\n\n## Documentation\n\nVisit <a href="https://extras.streamlitapp.com">extras.streamlitapp.com</a>\n\n## Contribution\n\nPRs are welcome! Guidelines here at <a href="https://extras.streamlitapp.com/Contribute">extras.streamlitapp.com/Contribute</a>\n\n<sup>README template taken from <a href="https://github.com/LukasMasuch/streamlit-pydantic">LukasMasuch/streamlit-pydantic</a></sup>\n',
    'author': 'Arnaud Miribel',
    'author_email': 'arnaudmiribel@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8, !=2.7.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*, !=3.7.*',
}


setup(**setup_kwargs)
