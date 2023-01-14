from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name='futils',
    version='1.3.0',
    description='A cli tool for managing documents and media files',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Giovanni Aguirre',
    author_email='giovanni.fi05@gmail.com',
    url='https://github.com/giobyte8/futils',

    packages=find_packages(),
    scripts=['fu/futils.py'],
    install_requires=[
        'python-resize-image==1.1.19',
        'typer==0.3.2',
        'rich==10.0.0'
    ],
    entry_points={
        'console_scripts': [
            'futils=fu.futils:app',
            'fu=fu.futils:app'
        ]
    },

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)