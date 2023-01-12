import setuptools
from setuptools import find_packages

from etsy_apiv3 import __version__

setuptools.setup(
    name="etsy-apiv3",
    version=__version__,
    author="Esat Yılmaz",
    author_email="esatyilmaz3500@gmail.com",
    description="Etsy APIV3 SDK",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9.1',
    install_requires=[
        "Async_OAuthlib>=0.0.9",
        "pycountry>=22.1.10",
        "pydantic>=1.10.2",
        "requests>=2.27.1",
        "requests_oauthlib>=1.3.0",
        "setuptools>=58.1.0",
        
    ]
)
