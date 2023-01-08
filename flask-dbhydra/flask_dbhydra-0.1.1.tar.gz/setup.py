import setuptools
    
with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name='flask_dbhydra',
    version='0.1.1',
    author='DovaX',
    author_email='dovax.ai@gmail.com',
    description='Autogenerate Flask API for dbhydra ORM DB structure',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/DovaX/flask_dbhydra',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'flask','dbhydra'
     ],
    python_requires='>=3.6',
)
    