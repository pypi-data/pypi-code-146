from distutils.core import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
  name = 'rcoc',
  package_data = {'': ['*.csv']},
  version = '1.1.15',
  license='MIT',
  description = 'RCOC - Random Country Or City name generator',
  author = 'touhf',
  author_email = 'tobytubar@gmail.com',
  url = 'https://github.com/touhf/rcoc',
  long_description=long_description,
  long_description_content_type="text/markdown",
  download_url = 'https://github.com/touhf/rcoc/archive/refs/tags/1.1.15.tar.gz',
  keywords = ['country', 'city', 'generator'],
  install_requires=[],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
)
