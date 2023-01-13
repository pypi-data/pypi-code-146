from setuptools import setup

#
# setup.py, a shim to setup.cfg, and pyproject.toml. 
# It allows editable installs for dev and pip directlyinstalls from github (no pypi account!).
# pip install -e .
# pip install git+http://
#
# toml is a separate static file saying we want to use setuptools.
# setup.cfg is a separate static file saying we want to use setuptools.
#

setup()


# GitHub repositories as npm modules
# Gist as a package -> as long as it has a package.json
#-> npm install gist:7d867cda127e64d38f28 --save
# Run NPM Packages on Client with Steal.Js
# ObservableHQ exports as NPM packages and CDN runtime/inspector.

# <script type="module" src='https://gist.githubusercontent.com/karpatic/f93...ad2f2dbfa9c/raw/10d88b4adf11776cf3810aa5be2ce04931f51122/index.js' async></script>

# html page pulls github js which loads observablehq js runtime/inspector which loads the notebook.
# html page serves as a directory of pages. js loads specifics modules/ values from notebook which is live/edited.
