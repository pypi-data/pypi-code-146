import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setuptools.setup(
  name = "gitstats-py",
  version = "1.0.5",
  description = "This library gives you some user metrics in batch from a set of github repositories.",
  long_description = long_description,
  long_description_content_type = "text/markdown",
  author = "Pablo Pazo Jiménez",
  author_email = "ppazo@us.es",
#To find more licenses or classifiers go to: https://pypi.org/classifiers/
  license = "GNU General Public License v3 (GPLv3)",
 packages=setuptools.find_packages(),
  classifiers = [
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
  "Operating System :: OS Independent",
],
  zip_safe=True,
  python_requires = ">=3.0",
  install_requires= install_requires,
  entry_points={
        'console_scripts': [
            'gitstats = gitstats.get_stats:get_stats'
        ]
    }
)