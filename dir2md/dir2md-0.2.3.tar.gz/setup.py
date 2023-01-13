# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['dir2md']
install_requires = \
['fire>=0.5.0,<0.6.0']

entry_points = \
{'console_scripts': ['dir2md = dir2md:dir2md_cli',
                     'md2dir = dir2md:md2dir_cli']}

setup_kwargs = {
    'name': 'dir2md',
    'version': '0.2.3',
    'description': '',
    'long_description': '# dir2md \n\n`dir2md` is a command-line tool that converts directories of files into Markdown code blocks. It also provides a reverse function, md2dir, which converts Markdown code blocks back into their original files.\n\n## Installation \n\nInstall `dir2md` using `pip`: \n\n```bash \npip install dir2md \n```\n\n## Usage\n\n`dir2md` can be used as a command-line tool or imported as a module.\n\n### Command-Line Tool\n\nTo convert a directory of files to Markdown code blocks, run:\n\n```bash\ndir2md [files...]\n```\n\nThis will print the resulting Markdown to the console.\n\nTo convert Markdown code blocks back into their original files, run:\n\n```bash\nmd2dir [options] <input_file>\n```\n\nThis will create the files in the current working directory.\n\nFor more options and usage details, use the `--help` flag.\n\n### Module\n\n```bash\nimport dir2md\n\n# Convert a directory of files to Markdown code blocks\nmarkdown = dir2md.dir2md("file1.py", "file2.py")\n\n# Convert Markdown code blocks back into their original files\ndir2md.md2dir_save(markdown, output_dir="output/")\n```\n\n### Wildcard support\n\nYou can use wildcards (`*`) to pass multiple files at once.\n\nFor example, to include all Python files in the current directory:\n\n```bash\ndir2md *.py\n```\n\nTo do so recursively, use `**`:\n\n```bash\ndir2md **/*.py\n```\n\nNote that the wildcard statement only works if it is expanded by the shell before the command is run. This means that you must use it in the command line or in a shell script, and it will not work if you pass it as a string to a function that runs the command.\n\n',
    'author': 'IsaacBreen',
    'author_email': 'mail@isaacbreen.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
