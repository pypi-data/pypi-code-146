# read version from installed package
from importlib.metadata import version
__version__ = version("pkgs_test")

# populate package namespace
from pkgs_test.pkgs_test import count_words, load_text, clean_text
from pkgs_test.plotting import plot_words
