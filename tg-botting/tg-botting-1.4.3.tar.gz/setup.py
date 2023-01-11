import codecs
import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.4.3'
DESCRIPTION = 'python library for easy creation of a telegram bot.'
LONG_DESCRIPTION = 'A package that allows you to create bots for telegram using its entire API.'

setup(
    name="tg-botting",
    version=VERSION,
    url='https://github.com/2sweetheart2/tg_botting/tree/master',
    author="Sweetie (Roma Fomkin)",
    author_email="<2004sweetheart2004@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=['tg_botting'],
    install_requires=['pyrogram', 'requests', 'aiohttp', 'datetime', 'TgCrypto'],
    keywords=['python', 'bot', 'tg', 'tg bot', 'telegram', 'telegram bot', 'botting'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ]
)
