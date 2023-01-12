from setuptools import find_packages, setup

from ai_dashboard import __version__

requirements = [
    "marko>=1.2.2",
    "requests>=2.0.0",
    "plotly>=5.3.1",
    "pandas>=1.3.5",
    # "kaleido>=0.1.0", #leave this out since static isn't used at the moment
]


test_requirements = [
    "pytest",
    "pytest-xdist",
    "pytest-cov",
]


setup(
    name="ai_dashboard",
    version=__version__,
    url="https://tryrelevance.com/",
    author="Relevance AI",
    author_email="dev@tryrelevance.com",
    packages=find_packages(),
    setup_requires=["wheel"],
    install_requires=requirements,
    package_data={
        "": [
            "*.ini",
        ]
    },
    extras_require=dict(
        tests=test_requirements,
    ),
)
