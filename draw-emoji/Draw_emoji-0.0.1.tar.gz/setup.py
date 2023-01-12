from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.1'
DESCRIPTION = 'A emoji and skin toned emoji extraction package'
LONG_DESCRIPTION = 'A package that extract emojis and skin toned emojis from the given text input'

# Setting up
setup(
    name="Draw_emoji",
    version=VERSION,
    author="Pradhyumna Poralla",
    author_email="<pradhyumnaporalla99@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'emoji', 'Emoji', 'skin', 'Skin', 'skintoned', 'Skintoned'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)