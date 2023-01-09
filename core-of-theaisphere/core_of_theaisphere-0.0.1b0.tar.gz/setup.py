from setuptools import setup, find_packages
import core_of_theaisphere
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

DESCRIPTION = "Package sitting at the core of theAIsphere"

# Setting up
setup(
    name="core_of_theaisphere",
    version=core_of_theaisphere.__version__,
    url=core_of_theaisphere.__homepage__,
    author=core_of_theaisphere.__author__,
    author_email=core_of_theaisphere.__email__,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['pyyaml', 'tqdm', 'pandas', 'scikit-learn', 'matplotlib', 'seaborn',
                      'optuna', 'xgboost', 'catboost', 'lightgbm', 'numpy', 'colorlog', ],
    # 'tensorflow'],
    keywords=['python', 'theaisphere', 'core'],
    license="MIT",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ]
)
