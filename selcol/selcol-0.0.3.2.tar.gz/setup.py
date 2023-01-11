from setuptools import find_packages, setup

install_requires = ["numpy", "onnxruntime"]
dev_requires = ["torch", "scikit-robot", "tqdm"]

setup(
    name="selcol",
    version="0.0.3.2",
    description="yet another percol implementation",
    author="Hirokazu Ishida",
    author_email="h-ishida@jsk.imi.i.u-tokyo.ac.jp",
    license="MIT",
    install_requires=install_requires,
    extras_require={"dev": dev_requires},
    packages=find_packages(exclude=("tests", "docs")),
    package_data={"selcol": ["py.typed"]},
    include_package_data=True
)
