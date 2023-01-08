from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Use ChatGPT on command line'
LONG_DESCRIPTION = 'AI-Chat-Tool is a tool that brings ChatGPT to the command line.'

# Setting up
setup(
    name="ai-chat-tool",
    version=VERSION,
    author="matoval (Matthew Sandoval)",
    author_email="<matovalcode@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['click'],
    keywords=['chatgpt', 'ai', 'chat'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
