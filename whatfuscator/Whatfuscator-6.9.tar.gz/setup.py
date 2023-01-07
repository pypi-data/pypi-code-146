from setuptools import setup, find_packages


__name__ = "Whatfuscator"
__version__ = "6.9"
setup(
    name=__name__,
    version=__version__,
    license='MIT',
    author="vesper",
    author_email='email@example.com',
    packages=find_packages(),
    keywords='obfuscate',
    install_requires=[
          'requests',
      ],

)