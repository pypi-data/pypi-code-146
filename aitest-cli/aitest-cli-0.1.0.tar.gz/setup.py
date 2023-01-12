from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name = 'aitest-cli',
    version = '0.1.0',
    author = 'aitest',
    author_email = 'vishwas@appliedaiconsulting.com',
    license = 'MIT License',
    description = 'aitest',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/vijay022/aitest-cli',
    py_modules = ['aitest_tool','app/aitest_application'],
    packages = find_packages(),
    install_requires = [requirements],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    entry_points = '''
        [console_scripts]
        aitest=aitest_tool:main        
    '''
)

