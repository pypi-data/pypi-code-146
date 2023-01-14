from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name='futils',
    version='1.3.1',
    description='A cli tool for managing documents and media files',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Giovanni Aguirre',
    author_email='giovanni.fi05@gmail.com',
    url='https://github.com/giobyte8/futils',

    packages=find_packages(),
    scripts=['fu/futils.py'],
    install_requires=[
        'exif==1.0.4',
        'python-resize-image==1.1.19',
        'rich==13.0.1',
        'typer==0.3.2'
    ],
    entry_points={
        'console_scripts': [
            'futils=fu.futils:app',
            'fu=fu.futils:app'
        ]
    },

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)