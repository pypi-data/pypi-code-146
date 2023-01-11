from setuptools import setup

setup(
    name = 'selenium-shortcuts',
    packages = ['selenium_shortcuts'],
    install_requires = ['requests', 'undetected-chromedriver'],
    version = '3.2',
    description = 'Selenium shortcut functions',
    url = 'https://github.com/xjxckk/selenium-shortcuts/',
    download_url = 'https://github.com/xjxckk/selenium-shortcuts/archive/refs/tags/v1.2.tar.gz',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
    )