from sys import version
import setuptools, os, json
from urllib.request import urlopen

#versionhash = os.popen("git ls-remote https://gitlab.com/02742/bunzbar.git | head -c 7").read()

js = json.load(urlopen("https://pypi.org/pypi/bunzbar/json"))
vs=len(js['releases'])

long_description = open("README.md", 'r').read()

setuptools.setup(
    name='bunzbar',
    version='0.'+str(vs+1),
    description = (f'Display useful information in status bar. Even stabler that the old 0.{vs} version.' ),
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='02742',
    packages=setuptools.find_packages(),
    classifiers=[
	"Programming Language :: Python :: 3",
	"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    entry_points={
        'console_scripts': [
            'bunzbar = bunzbar:__main__'
        ],    
    },
    install_requires=[
        'tsv-calendar',
        'psutil'
    ],
)
