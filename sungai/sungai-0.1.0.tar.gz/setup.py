"""
Sungai.

- Project URL: https://github.com/hugocartwright/sungai
"""
from pathlib import Path

from setuptools import find_packages, setup

setup_args = dict(
    name='sungai',
    python_requires='>3.6.0',
    version="0.1.0",
    description='Sungai is a directory rating tool',
    license='MIT License',
    packages=find_packages(),
    author='Hugo Cartwright',
    author_email='hugo.cartw@gmail.com',
    keywords=['Python'],
    url='https://github.com/hugocartwright/sungai',
    download_url='https://pypi.org/project/sungai/',
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type='text/markdown',
    project_urls={
        'Source': 'https://github.com/hugocartwright/sungai',
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
    install_requires=[
        'numpy',
        'scipy',
    ],
    entry_points={
        'console_scripts': [
            'sungai = sungai:run_sungai',
        ]
    }
)

if __name__ == '__main__':
    setup(**setup_args)
