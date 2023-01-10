import setuptools
from src.BubotObj.OcfDevice.subtype.WebServer import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='Bubot_WebServer',
    version=__version__,
    author="Razgovorov Mikhail",
    author_email="1338833@gmail.com",
    description="Web server for Bubot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/businka/Bubot_WebServer",
    package_dir={'': 'src'},
    package_data={
        '': ['*.md', '*.json', '*.css', '*.woff', '*.woff2', '*.js', '*.svg', '*.png', '*.css', '*.html'],
    },
    packages=setuptools.find_namespace_packages(where='src'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Framework :: AsyncIO",
    ],
    python_requires='>=3.7',
    zip_safe=False,
    install_requires=[
        'motor>=3',
        'aiohttp>=3.7,<4',
        'aiohttp-session>=2.9',
        'Bubot_Core>=0.1.4',
    ]
)
