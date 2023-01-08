from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name='QCpython',
    version='1.0',
    description = "",
    long_description= long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    author="Brennan Freeze, Paris Osuch, Aundre Barras, Soren Richenberg",
    author_email="freezebrennan@gmail.com, osuch@sonoma.edu, barras@sonoma.edu, richenbe@sonoma.edu",
    package_dir={'': 'src'},
    packages=find_packages('src'),
    url='https://github.com/QCpyDevs/QCpy',
    keywords='Quantum Computing, Visualization, Simulation, Linear Algebra, ',
    install_requires=[
          "numpy",
          "matplotlib",
      ],

)