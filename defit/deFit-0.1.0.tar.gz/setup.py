import setuptools
import os
# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
setuptools.setup(
    name="deFit",
    version="0.1.0",
    author="Yueqin Hu",
    author_email="yueqinhu@bnu.edu.cn",
    license='GPL-3',
    description="Fitting Differential Equations to Time Series Data",
    long_description_content_type='text/markdown',
    long_description="\n".join(
        [
            open("README.md").read(),
            # open("CHANGELOG.md").read(),
            # open("AUTHORS.md").read(),
            # open("LICENSE.md").read(),
        ]),
    # description="Use numerical optimization to fit ordinary differential equations (ODEs) to time series data to examine the dynamic relationships between variables or the characteristics of a dynamical system. It can now be used to estimate the parameters of ODEs up to second order.",
    packages=setuptools.find_packages(),
    url="https://github.com/yueqinhu/defit",  # Optional
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'pandas',
        'scipy',
        'numpy',
        'pathlib',
        'matplotlib',
        'importlib-metadata; python_version == "3.8"',
    ],
    include_package_data=True,
    keywords="ordinary differential equation, optimization, numerical methods, Intensive longitudinal data, dynamical system, time series",  # Optional
    package_data={
        "defit": ["*.txt"],
        "defit.data": ["*.csv"],
    },
    project_urls={  # Optional
        "Documentation": "https://github.com/yueqinhu/defit/blob/main/Documents/UserGuidePython.md",
        # "Source Code": "https://github.com/yueqinhu/defit",
    },
)