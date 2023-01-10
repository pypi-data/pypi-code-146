# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['htag', 'htag.runners']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'htag',
    'version': '0.9.12',
    'description': 'GUI toolkit for building GUI toolkits (and create beautiful applications for mobile, web, and desktop from a single python3 codebase)',
    'long_description': '# HTag : "H(tml)Tag"\n\n<img src="https://manatlan.github.io/htag/htag.png" width="100" height="100">\n\n[![Test](https://github.com/manatlan/htag/actions/workflows/on_commit_do_all_unittests.yml/badge.svg)](https://github.com/manatlan/htag/actions/workflows/on_commit_do_all_unittests.yml)\n\n<a href="https://pypi.org/project/htag/">\n    <img src="https://badge.fury.io/py/htag.svg?x" alt="Package version">\n</a>\n\n\nA new python library to create UI (or UI toolkit), which render nativly in anything which can render **html/js/css**.\nThoses can be a browser, a pywebview, an android/apk, or anything based on cef, depending on an [htag runner](https://manatlan.github.io/htag/runners/)\xa0!\nAs it\'s based on html/js rendering: you can easily mix powerful JS libs with powerful PY3 libs : and make powerful python apps !\n\n * For a **desktop app** : You can use the [PyWebView runner](https://manatlan.github.io/htag/runners/#pywebwiew), which will run the UI in a pywebview container (or "ChromeApp runner", in a local chrome app mode).\xa0\n * For a **web app** : You can use the [WebHTTP runner](https://manatlan.github.io/htag/runners/#webhttp), which will run the UI in a web server, and serve the UI on client side, in a browser.\xa0\n * For a **android app** : You can use the [AndroidApp runner](https://manatlan.github.io/htag/runners/#androidapp), which will run the UI in a kiwi webview thru tornado webserver, and can be embedded in an apk ([recipes](https://github.com/manatlan/htagapk))\n * For a **pyscript app** : you can use the [PyScript runner](https://manatlan.github.io/htag/runners/#pyscript), which will run completly in client side\n\nBut yes … the promise is here : **it\'s a GUI toolkit for building "beautiful" applications for mobile, web, and desktop from a single codebase**.\n\n[DOCUMENTATION](https://manatlan.github.io/htag/)\n\n[DEMO/TUTORIAL](https://htag.glitch.me/)\n\n[Changelog](https://github.com/manatlan/htag/releases)\n\n[Available on pypi.org](https://pypi.org/project/htag/)\n\n[Announcement on reddit (22/07/14)](https://www.reddit.com/r/Python/comments/vysnci/htag_a_new_gui_tookit_for_webdesktopandroid_from/)\n\n## To have a look\n\nTODO: need to find a super demo ;-)\n\n## ROADMAP to 1.0.0\n\n * rock solid (need more tests)\n * setup minimal docs ;-)\n * ~~top level api could change (Tag() -> create a Tag, Tag.mytag() -> create a TagBase ... can be a little bit ambiguous)~~\n * ~~manage "query params" from url to initialize Tags/routes~~\n * ~~I don\'t really like the current way to generate js in interaction : need to found something more solid.~~\n * ~~the current way to initiate the statics is odd (only on real (embedded) Tag\'s) : should find a better way (static like gtag ?!)~~\n\nand more technicals :\n- ~~better js try/catch to sort js/py error + try/catch on http com error (for thoses which kill session webhttp/pye) ~~\n- ~~getStateImage is non sense coz it\'s str\'ing (why not returning the str ?!)~~\n- ~~mix the Tag.__init__ with the old system (like this: it\'s unmaintable)~~\n- ~~introduce a virtual tag/placeholder~~\n- ~~DISPLAY a warning (or exception in STRICT_MODE?), when a render method use a "tag creation" (ex: Tag.div("hello")), because it will always be rendered !!!!!~~\n- tests, tests & tests !\n\n## History\n\nAt the beginning, there was [guy](https://github.com/manatlan/guy), which was/is the same concept as [python-eel](https://github.com/ChrisKnott/Eel), but more advanced.\nOne day, I\'ve discovered [remi](https://github.com/rawpython/remi), and asked my self, if it could be done in a *guy way*. The POC was very good, so I released\na version of it, named [gtag](https://github.com/manatlan/gtag). It worked well despite some drawbacks, but was too difficult to maintain. So I decided to rewrite all\nfrom scratch, while staying away from *guy* (to separate, *rendering* and *runners*)... and [htag](https://github.com/manatlan/htag) was born. The codebase is very short, concepts are better implemented, and it\'s very easy to maintain.\n\n\n',
    'author': 'manatlan',
    'author_email': 'manatlan@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/manatlan/htag',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
