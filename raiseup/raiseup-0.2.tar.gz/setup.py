import setuptools

setuptools.setup(
    name='raiseup',
    version='0.2',
    author='Barney Gale and XploreInfinity',
    url='https://github.com/XploreInfinity/raiseup',
    license='MIT',
    description='Python library for requesting root privileges',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=["raiseup"],
    project_urls={
        "Bug Tracker": "https://github.com/XploreInfinity/raiseup/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: BSD :: FreeBSD",
    ],
)
