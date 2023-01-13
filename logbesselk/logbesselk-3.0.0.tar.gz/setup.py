# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['logbesselk', 'logbesselk.jax', 'logbesselk.tensorflow']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'logbesselk',
    'version': '3.0.0',
    'description': 'Provide function to calculate the modified Bessel function of the second kind',
    'long_description': '# logbesselk\nProvide function to calculate the modified Bessel function of the second kind\nand its derivatives.\n\n## Reference\nTakashi Takekawa, Fast parallel calculation of modified Bessel function\nof the second kind and its derivatives, SoftwareX, 17, 100923, 2022.\n\n## Author\nTAKEKAWA Takashi <takekawa@tk2lab.org>\n\n\n## For Tensorflow\n\n### Require\n- Python (>=3.8)\n- Tensorflow (>=2.6)\n\n### Installation\n```shell\npip install tensorflow logbesselk\n```\n\n### Examples\n```python\nimport tensorflow as tf\nfrom logbesselk.tensorflow import log_bessel_k\n\n# return tensor\nlog_k = log_bessel_k(v=1.0, x=1.0)\nlog_dkdv = log_bessel_k(v=1.0, x=1.0, m=1, n=0)\nlog_dkdx = log_bessel_k(v=1.0, x=1.0, m=0, n=1)\n\n# build graph at first execution time\nlog_bessel_k_tensor = tf.function(log_bessel_k)\nlog_bessel_dkdv_tensor = tf.function(lambda v, x: log_bessel_k(v, x, 1, 0))\nlog_bessel_dkdx_tensor = tf.function(lambda v, x: log_bessel_k(v, x, 0, 1))\n\nn = 1000\nfor i in range(10):\n    v = 10. ** (2. * tf.random.uniform((n,)) - 1.)\n    x = 10. ** (3. * tf.random.uniform((n,)) - 1.)\n\n    log_k = log_bessel_k_tensor(v, x)\n    log_dkdv = log_bessel_dkdv_tensor(v, x)\n    log_dkdx = log_bessel_dkdx_tensor(v, x)\n```\n\n\n## For jax\n\n### Require\n- Python (>=3.8)\n- jax (>=0.3)\n\n### Installation\n```shell\npip install jax[cuda] -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html\npip install logbesselk\n```\n\n### Examples\n```python\nimport jax\nfrom logbesselk.jax import log_bessel_k\n\n# return jnp.array\nlog_k = log_bessel_k(v=1.0, x=1.0)\nlog_dkdv = log_bessel_k(v=1.0, x=1.0, m=1, n=0)\nlog_dkdx = log_bessel_k(v=1.0, x=1.0, m=0, n=1)\n\n# build graph at first execution time\nlog_bessel_k_jit = jax.jit(jax.vmap(log_bessel_k))\nlog_bessel_dkdv_jit = jax.jit(jax.vmap(lambda v, x: log_bessel_k(v, x, 1, 0)))\nlog_bessel_dkdx_jit = jax.jit(jax.vmap(lambda v, x: log_bessel_k(v, x, 0, 1)))\n\ntrial = 10\nn = 1000\nfor i in range(trial):\n    v = 10. ** jax.random.uniform(i, (n,), minval=-1., maxval=1.)\n    x = 10. ** jax.random.uniform(i, (n,), minval=-1., maxval=2.)\n\n    log_k = log_bessel_k_tensor(v, x)\n    log_dkdv = log_bessel_dkdv_tensor(v, x)\n    log_dkdx = log_bessel_dkdx_tensor(v, x)\n```\n',
    'author': 'TAKEKAWA Takashi',
    'author_email': 'takekawa@tk2lab.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tk2lab/logbesselk',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
