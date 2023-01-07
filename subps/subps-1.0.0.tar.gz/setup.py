import setuptools

with open('README.md', 'r', encoding='utf-8') as info:
    long_description = info.read()

setuptools.setup(
    name='subps',
    version='1.0.0',
    author='René Rath',
    author_email='contact@superstes.eu',
    description='Wrapper script for subprocess usage',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/superstes/python3-subps',
    project_urls={
        'Repository': 'https://github.com/superstes/python3-subps',
        'Bug Tracker': 'https://github.com/superstes/python3-subps/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.3'
)
