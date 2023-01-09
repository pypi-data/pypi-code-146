import setuptools

from src.blockly_executor.__version__ import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='blockly_executor',
    version=__version__,
    test_requires=[],
    url='https://gitlab.com/razgovorov/blockly_executor',
    license='MIT',
    author='Razgovorov Mikhail',
    author_email='1338833@gmail.com',
    description='blockly xml interpreter and debugger',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Natural Language :: Russian',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
        "Operating System :: OS Independent"
    ],
    keywords='blockly',
    python_requires='>=3.9',
    zip_safe=False,
    install_requires=[
        'Bubot_Helpers>=0.0.10',
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src")
)
