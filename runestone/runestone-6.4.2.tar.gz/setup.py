# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['runestone',
 'runestone.accessibility',
 'runestone.activecode',
 'runestone.animation',
 'runestone.assignment',
 'runestone.blockly',
 'runestone.cellbotics',
 'runestone.chapterdb',
 'runestone.clickableArea',
 'runestone.codelens',
 'runestone.common',
 'runestone.datafile',
 'runestone.disqus',
 'runestone.dragndrop',
 'runestone.fitb',
 'runestone.groupsub',
 'runestone.hparsons',
 'runestone.khanex',
 'runestone.lp',
 'runestone.matrixeq',
 'runestone.mchoice',
 'runestone.meta',
 'runestone.parsons',
 'runestone.poll',
 'runestone.pretext',
 'runestone.question',
 'runestone.quizly',
 'runestone.reveal',
 'runestone.selectquestion',
 'runestone.server',
 'runestone.shortanswer',
 'runestone.showeval',
 'runestone.spreadsheet',
 'runestone.tabbedStuff',
 'runestone.timed',
 'runestone.utility',
 'runestone.video',
 'runestone.wavedrom',
 'runestone.webgldemo']

package_data = \
{'': ['*'],
 'runestone': ['dist/*'],
 'runestone.accessibility': ['css/*'],
 'runestone.animation': ['js/*'],
 'runestone.codelens': ['js/*'],
 'runestone.common': ['project_template/*',
                      'project_template/_sources/*',
                      'project_template/_static/*',
                      'project_template/_templates/plugin_layouts/sphinx_bootstrap/*',
                      'project_template/_templates/plugin_layouts/sphinx_bootstrap/static/*',
                      'project_template/_templates/plugin_layouts/sphinx_bootstrap/static/img/*'],
 'runestone.lp': ['css/*'],
 'runestone.matrixeq': ['css/*', 'js/*'],
 'runestone.showeval': ['js/LICENSE.txt'],
 'runestone.webgldemo': ['css/*', 'js/*']}

install_requires = \
['CodeChat>=1.8.6',
 'Paver>=1.2.4',
 'SQLAlchemy>=1.4.0',
 'Sphinx>=4.4.0',
 'click>=8,<9',
 'cogapp>=2.5',
 'jinja2<3.1.0',
 'six>1.12',
 'sphinxcontrib-paverutils>=1.17,<6.0.0']

entry_points = \
{'console_scripts': ['runestone = runestone.__main__:cli']}

setup_kwargs = {
    'name': 'runestone',
    'version': '6.4.2',
    'description': 'Sphinx extensions for writing interactive documents.',
    'long_description': "RunestoneComponents\n===================\n\n.. image:: https://img.shields.io/pypi/v/Runestone.svg\n   :target: https://pypi.python.org/pypi/Runestone\n   :alt: PyPI Version\n\n.. image:: https://img.shields.io/pypi/dm/Runestone.svg\n   :target: https://pypi.python.org/pypi/Runestone\n   :alt: PyPI Monthly downloads\n\n.. image:: https://github.com/RunestoneInteractive/RunestoneComponents/workflows/Python%20package/badge.svg\n\nPackaging of the Runestone components for publishing educational materials using Sphinx and restructuredText. Check out the `Overview <http://interactivepython.org/runestone/static/overview/overview.html>`_ To see all of the extensions in action.\n\nRunestone Version 6\n-------------------\n\n**Important** December 2021 - merged Runestone 6 to master branch.  In runestone 6.0 we assume that you are using the new `bookserver` for serving books.  This is installed automatically as part of the Docker build in the main RunestoneServer.  But you can also `pip install bookserver` to run a small scale server that uses sqllite.  Eventually `bookserver` will replace the super simple server you get when you run `runestone serve`\n\nDocumentation\n-------------\n\nWriting **new** books using the Runestone RST markup language is deprecated as of Summer 2022.  It is strongly recommended that you use the `PreTeXt <https://pretextbook.org>`_ markup language for writing new books.\n\n* Take a look at the `Sample Book <https://pretextbook.org/examples/sample-book/annotated/sample-book.html>` Especially Chapter 3, the section titled Interactive Exercises.  The activecode, CodeLens and all the rest of the interactives that you see in that sample book are powered by the components in this repository.  This repository will remain the home of those interctive components.\n\n* Take a look at the `PreTeXt Guide <https://pretextbook.org/doc/guide/html/guide-toc.html>`_ It contains comprehensive documentation on writing in PreTeXt.\n\n* As an Author you will want to use the PreTeXt CLI for writing books.   Experienced Runestone authors will find the pretext cli to be quite familiar, but better organized with fewer mysterious configuration files. See `PreTeXt-CLI <https://pretextbook.org/doc/guide/html/guide-toc.html>`\n\n\nQuick Start\n-----------\n\n* `pip install pretext`\n* Create a folder for your book project then run\n* `pretext new` to create a new book.\n\n\nOld Documentation\n-----------------\n\nI will keep this around for a while during the transition to PreTeXt.\n\nTo get started with Runestone restructuredText as the markup language:\n\n* `pip install runestone`\n\nTo start a project, create a new folder and then run the following command (installed by pip)  in that new folder ``runestone init``  For example:\n\n::\n\n    mkdir myproject\n    cd myproject\n    runestone init\n\n\nThe init command will ask you some questions and setup a default project for you. The default response is in square brackets, example ``[false]``.\n\nTo build the included default project run\n\n::\n\n    runestone build\n\n*Note:* If you come across version conflict with ``six`` library while building the project, ``pip install --ignore-installed six`` command might be useful.\n\nYou will now have a build folder with a file index.html in it, along with some default content.  The contents of the build folder are suitable for hosting anywhere that you can serve static web content from!  For a small class you could even serve the content using the provided Python webserver::\n\n    $ runestone serve\n\nNow from your browser you can open up ``http://localhost:8000/index.html``  You should see the table of contents for a sample page like this:\n\n.. image:: images/runeCompo-index.png\n    :width: 370\n\n\nIf you edit ``_sources/index.html`` or ``_sources/overview.rst`` and then rebuild and serve again you will see your changes.  The best documentation is probably the overview.rst file itself, as it demonstrates how to use all of the common components and shows most of their options.\n\n\n**Windows Users** I have tested the installation, along with init, build, and serve on Windows 8.1.\nThe biggest pain is probably setting your PATH environment variable so you can simply type the commands\nfrom the shell.  Please note that I am not a regular user of windows, I only test things on my VMWare\ninstallation every so often.  If you are new to using Python on windows I recommend you check out this\nlink on `Using Python with Windows <https://docs.python.org/3.4/using/windows.html>`_\n\n\nDeveloping and Hacking\n----------------------\n\nSo, you would like to help out with developing the Runestone Components.  Great We welcome all the help we can get.  There is plenty to do no matter what your experience level.  There are a couple of prerequisites.\n\n1. You will need a version of Python, I currently develop on 3.9 or higher, but test on 3.8 and later.\n\n2. You will need nodejs and npm as well since there is a LOT of Javascript code in the components.\n\nTo get everything set up do the following\n\n1.  Make a Fork of this repository. and ``git clone`` the repository to your development machine.\n\n2.  Install `Poetry  <https://python-poetry.org/docs/>`_\n\n3.  From the top level RunestoneComponents folder run ``npm install`` this will install the packaging tools that are needed for Javascript development.  ``npm run`` gives you a list of commands  The key command is ``npm run build`` this will combine all of the Javascript and CSS files for all the components into a single runestone.js file.  If you are doing some really deep development and want to avoid building a book, you can put your html in public/index.html and use the ``npm run start`` command.  This will automatically rebuild runestone.js and refresh the webpage every time you save a change.\n\n\n4.  When you have some changes to share, make a Pull Request.\n\n(See the RunestoneServer repository and **http://runestoneinteractive.org** for more complete documentation on how this project works.)\n\nCode Style\n----------\n\nWe use ``black`` to automatically style Python.  You can set up your editor to automatically run black whenever you save, or you can run it manually.\n\nWe use ``prettier`` to automatically style Javascript.\n\nRun ``jshint`` on your code we have some options configured for this project.\n\nWriting Tests\n-------------\n\nA great way to contribute to the Runestone Components repository is to add to our test suite.\n\nOur goal is to have unit tests which rely on Selenium (a library that helps simulate interactions in a web browser) for each directive, to see if the JavaScript that powers the directives is working correctly.\n\n**In order to get started with writing a test/writing additional tests, you will need the following:**\n\n\n* Download the latest `ChromeDriver <https://chromedriver.storage.googleapis.com/index.html>`_., which is a driver that simulates Google Chrome.\n\n* On linux you will need to install Xvfb ``apt-get install xvfb``\n\n* You'll also need to have done the above installation.\n\n* We have converted to using poetry for our dependency management.  To run `runestone` while in development mode `poetry run runestone ...`  OR you can run `poetry shell` to start up a shell with a virtual environment activated.\n\n\n**To run tests:**\n\n* Make sure the directory containing the ChromeDriver executable is in your ``PATH`` environment variable. e.g. ``PATH=$PATH:path/to/chromedriver`` at your command line (or edit your ``.bash_profile``).\n\n* Check out the existing tests, e.g. the ``test_question.py`` file that tests the Question directive, which you can find at the path ``/runestone/question/test/test_question.py``, for an example.\n\n* Each directive's individual set of tests requires a mini book. You'll see a ``_sources`` folder for each existing test containing an ``index.rst`` file. That file contains a title, as required by ``.rst``, and whatever directive examples you want to test.\n\n* Finally, to run a test, ensuring that you have accessed a directive folder, type the following at the command prompt:\n\n  * ``poetry run pytest``\n\nRunning pytest from the main directory will run all the tests.  To run a single test you can navigate to the\ndirectory of the test, or you can run ``poetry run pytest -k XXX`` where XXX is a substring that matches some part of\nthe test functions name.\n\n.. note::\n\n  8081 is the default test port.\n  If you are running another server on this port, you may encounter an error.\n  See the Python files, e.g. ``test_question.py``, to see how this is set up.\n\nYou should then see some test output, showing a pass (``ok``), FAIL, or error(s).\n\nIf you have an error relating to PhantomJS/a driver in the output, you probably have a PATH or driver installation problem.\n\n**To write a new test:**\n\n* Create a ``test`` directory inside a directive's folder\n\n* Create a Python file to hold the test suite inside that directory, e.g. ``test_directivename.py``\n\n* Run ``runestone init`` inside that folder and answer the following prompts\n\n* Write the appropriate directive example(s) inside the ``index.rst`` file (which will be created as a result of ``runestone init``)\n\n* Edit the Python file you created as appropriate (see documentation for the Python ``unittest`` module `In the Python docs <https://docs.python.org/2/library/unittest.html>`_.)\n\n\nNotes for more Advanced Users\n-----------------------------\n\nIf you already have an existing `Sphinx <http://sphinx-doc.org>`_  project and you want to incorporate the runestone components into your project you can just make a couple of simple edits to your existing ``conf.py`` file.\n\n* First add the following import line ``from runestone import runestone_static_dirs, runestone_extensions``\n* Then modify your extensions.  You may have a different set of extensions already enabled, but it doesn't matter just do this:  ``extensions = ['sphinx.ext.mathjax'] + runestone_extensions()``\n* Then modify your html_static_path:  ``html_static_path = ['_static']  + runestone_static_dirs()``  Again you may have your own set of static paths in the initial list.\n\n\nSee https://github.com/bnmnetp/runestone/wiki/DevelopmentRoadmap to get a sense for how this is all going to come together.\n\nResearchers\n-----------\n\nIf you use Runestone in your Research or write about it, please reference ``https://runestone.academy`` and cite this paper:\n\n::\n\n   @inproceedings{Miller:2012:BPE:2325296.2325335,\n    author = {Miller, Bradley N. and Ranum, David L.},\n    title = {Beyond PDF and ePub: Toward an Interactive Textbook},\n    booktitle = {Proceedings of the 17th ACM Annual Conference on Innovation and Technology in Computer Science Education},\n    series = {ITiCSE '12},\n    year = {2012},\n    isbn = {978-1-4503-1246-2},\n    location = {Haifa, Israel},\n    pages = {150--155},\n    numpages = {6},\n    url = {http://doi.acm.org/10.1145/2325296.2325335},\n    doi = {10.1145/2325296.2325335},\n    acmid = {2325335},\n    publisher = {ACM},\n    address = {New York, NY, USA},\n    keywords = {cs1, ebook, sphinx},\n   }\n",
    'author': 'Brad Miller',
    'author_email': 'bonelake@mac.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/RunestoneInteractive/RunestoneComponents',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
