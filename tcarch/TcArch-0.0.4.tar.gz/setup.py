'''Package description'''
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    name='TcArch',
    description='Script to test ...',
    keywords='twincat',
    url='https://github.com/TobiasFreyermuth/TcArch',
    author='Tobias Freyermuth',
    author_email='Tobias.Freyermuth@posteo.net',
    license='MIT',
    python_requires='>=3.10',
    install_requires=[
        'lxml>=4.0.0'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.10'
    ],
    py_modules=['TcArch'],
    package_dir={'': 'src'},
    packages=find_packages("src"),
    package_data={"TcArch": ["VERSION"]},
    include_package_data=True,
    long_description_content_type='text/markdown',
    long_description=long_description,
    extras_require={
        "dev": [
            "pytest>=7.0",
        ]
    },
)