from setuptools import setup

setup( 
    name="smartfox", 
    version="0.0.1.dev0", 
    description="An SDK for Smartfox API", 
    long_description=""" 
        An SDK for Smartfox API
    """, 
    author = "@jfk344",
    author_email = "info@jfk.rocks",
    url="https://gitlab.com/jfk344/python-smartfox-sdk",
    packages=['smartfox'],
    install_requires=[ 
        'requests == 2.22.0',
    ],
    python_requires='>=3.6'
)