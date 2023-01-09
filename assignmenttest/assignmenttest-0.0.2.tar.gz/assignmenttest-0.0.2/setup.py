from setuptools import setup, find_packages


VERSION = '0.0.2'
DESCRIPTION = 'test file'
LONG_DESCRIPTION = 'A package that allows to test.'

# Setting up
setup(
    name="assignmenttest",
    version=VERSION,
    author="Aman and Akanksha",
    author_email="<mail@neuralnine.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
