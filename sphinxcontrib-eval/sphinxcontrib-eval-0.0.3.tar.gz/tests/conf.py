"""Configure the Sphinx documentation builder.

https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

from sphinxcontrib.eval import eval_sh

extensions = [
    "sphinxcontrib.eval",
]

eval_funcs = {"sh": eval_sh}
