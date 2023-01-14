from setuptools import setup

try:
    with open("README.md") as rfile:
        long_description = rfile.read()
except:
    long_description = "https://github.com/ytcalifax/PyHasteBin (description failed to load)"

setup(
    name='PyHasteBin',
    version='1.2.4',
    packages=['postbin', "postbin.v2"],
    url='https://github.com/ytcalifax/PyHasteBin',
    python_requires=">=3.6",
    license='MIT',
    author='EEKIM10, ytcalifax',
    author_email='kcustom.businessonly@gmail.com',
    description='A simple two-function program that POSTs to hastebin',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    extras_require={"cli": "webbrowser"}
)
#
