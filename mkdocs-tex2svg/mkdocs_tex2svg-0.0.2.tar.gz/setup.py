import os
import sys
from setuptools import setup

username = os.getenv('TWINE_USERNAME')
password = os.getenv('TWINE_PASSWORD')

VERSION = '0.0.2'
GIT_MESSAGE_FOR_THIS_VERSION ="""Add configuration param for priority of the plugin
"""

if sys.argv[-1] == 'publish':
    if os.system("pip freeze | grep build"):
        print("'build' is not installed.\nUse `pip install build`.\nExiting.")
        sys.exit()
    if os.system("pip freeze | grep twine"):
        print("'twine' is not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    os.system("python -m build")
    if ((username is not None) and (password is not None)):
        os.system(f"python -m twine upload dist/* -u {username} -p {password}")
    else:
        os.system(f"python -m twine upload dist/*")
    print(f"You probably also want to git push project, create v{VERSION} tag, and push it too :\n")
    gitExport=input("Do you want to do it right now? [y(default) / n]")
    if gitExport=="y" or gitExport=="":
        os.system(f"git add . && git commit -m 'v{VERSION} : {GIT_MESSAGE_FOR_THIS_VERSION}' && git push")
        os.system(f"git tag -a {VERSION} -m 'v{VERSION}'")
        os.system(f"git push --tags")
    else:
        print("You may still consider adding the following new tag later on :")
        print(f"git tag -a {VERSION} -m 'v{VERSION}'")
        print(f"git push --tags")
    sys.exit()

setup(
    name="mkdocs_tex2svg",
    version=VERSION,
    py_modules=["mkdocs_tex2svg"],
    install_requires=['Markdown>=2.3.1'],
    author="Rodrigo Schwencke",
    author_email="rod2ik.dev@gmail.com",
    description="Converts (inline and/or block) LaTeX snippets in Mkdocs, as SVGs, natively & dynamically compatible with Mkdocs Light & Dark Themes, directly from your Markdown",
    long_description_content_type="text/markdown",
    long_description="""Project Page : [rod2ik/mkdocs-tex2svg](https://gitlab.com/rod2ik/mkdocs-tex2svg)

This project is part of other mkdocs-related projects.  
If you're interested, please consider having a look at this page for a more complete list of all our mkdocs-related projects:

* https://eskool.gitlab.io/mkhack3rs/

This project is the initial work of :

* Rodrigo Schwencke at [rod2ik/mkdocs-tex2svg](https://gitlab.com/rod2ik/mkdocs-tex2svg)

In order to get it work with pip (python3) and mkdocs.

If you use python 2, please consider using the original extension instead.

Licences:

* All newer parts (Rodrigo Schwencke) are [GPLv3+](https://opensource.org/licenses/GPL-3.0)
* Older parts (Cesare Morel, Steffen Prince, Jawher Moussa) are [MIT License](http://www.opensource.org/licenses/mit-license.php)""",
    license="GPLv3+",
    url="https://gitlab.com/rod2ik/mkdocs-tex2svg.git",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: Documentation',
        'Topic :: Text Processing',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows :: Windows 10',
    ],
)
