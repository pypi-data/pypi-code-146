# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['feedfilter']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'feedgen>=0.9.0,<0.10.0',
 'feedparser>=6.0.10,<7.0.0',
 'pytz>=2022.6',
 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['feed-filter = feedfilter:main']}

setup_kwargs = {
    'name': 'feedfilter',
    'version': '1.0.1',
    'description': 'Modify RSS/Atom feeds',
    'long_description': "# feed-filter\n\nFilter for modifying feed data.  By default, reads feed from stdin and writes a\nmodified feed to stdout in either Atom (default) or RSS format.\n\nfeed-filter can modify the titles of entries via a regular expression\n(python re syntax) and also add the entry's date to the far end of the\ntitle as an aid to sorting for feed readers that cannot have both a\nprimary sort and secondary sort fields.\n\nfeed-filter can also optionaly make some modification to the content\nsuch as converting URLs into links.\n\n## Options\n\n### --title-re and --title-sub\n\nThe --title-re option specifies a regular expression.  And the --title-sub option can use backrefferences to the RE in --title-re.\n\nSo for example, if you have the following options\n> --title-re='([^•]+ • )?(Re: )?(.*)' --title-sub='\\3'\n\nIt will make the following modification to the title\n\nOriginal title:\n> Tutorials and videos • Re: Part design Tutorials and much more ...\n\nModified title:\n> Part design Tutorials and much more ...\n\nThat change did 2 things.  It removed a common prefix (forum title) that all entries have, and also removed the 'Re: ' that is added to replies.\n\nIf you wanted to keep the prefix, but just remove the 'Re: ', then\nchange the second option like the example below:\n\n> --title-re='([^•]+ • )?(Re: )?(.*)' --title-sub='\\1\\3'\n\nAnd the modified title will now be\n\nModified title:\n> Tutorials and videos • Part design Tutorials and much more ...\n\nEither of the above two examples can be helpfull for modifying a feed\nfor a forum so that you can sort the entries by title (headline) so\nall posts and their responses are groups together.\n\n### --add-date-to-title\n\nJust grouping all related posts together is helpfull, but you probably\nwant to display them in the order they were created.  If you happen to\nhave a feed reader that can sort on titles with a secondary sort on\nthe date, then you are all set.  But if you can only do one sort\n(title), the posts may be in the wrong order.  This is where the\n--add-date-to-title option comes in.\n\nIt does pretty much what it says.  It appends the posting's date to\nthe end of the title after a bunch of spaces.  All the spaces are just\nto hide the date string.  The date aids in sorting.  Now when you sort\non the title, the entries will implicitly have a secondary sort on the\ndate due to its inclusion in the titles.\n\n### --add-posts\n\nFor each entry, it attempts to download a topic-specific rss or atom\nfeed and adds each entry in place of the original entry.  This is\nusefull for sites whos forum feed only shows the topics (first post)\nand not any replies.  Note that this option won't work on many sites\ndue to having to parse web pages.  Raise issue for any site that\ndoesn't seem to work.  Titles on additional posts fetched will all\nbe taken from the original entry.\n\n### --auto-links\n\nIn the content sections, anything that looks like a URL but is not already\nan HTML link, will be made into a link.\n\n### --output-fmt\n\nValue can be either 'atom' (default), 'rss', or 'summary'.  The\n'summary' options just prints out a few fields in plain text format.\nUsed primary for debugging.\n\n### Others\n\nRun feed-filter with the --help option to see what other options\nare available.\n\n\n# Installation\n\nThis [package](https://pypi.org/project/feedfilter/) is on [PyPI.org](https://pypi.org/), so just install with pip or pipx like\n\n```\npipx install feedfilter\n```\n\n# Development setup\n\nIt is recommended that you do any development in a virtual\nenvironment.  If you use direnv, a .envrc file is provided.  You\nshould always look it over before allowing it to be used.\n\npoetry is required.  You can install it in your virtual enviroment\nfor this project via ```pip install poetry``` or alternatively via\n\n```\npipx install poetry\n```\n\nOnce that is installed, just run\n```\nmake install-requirements\n  or\npoetry install\n```\n\nTo run feed-filter in development, you should be able to just run\n\n```\nfeed-filter <args>\n```\n\n## Building\n\nTo create a build (sdist, wheel) run the following\n\n```\nmake build\n```\n\nResults will be in the dist/ directory.\n\n# Licensing\n\nThis project is licensed under the GNU GPL version 3 or later.  See the\nLICENSE file in the top-level directory.\n",
    'author': 'Jim Bauer',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/jim_bauer/feed-filter',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
