from setuptools import setup, find_packages

setup(
    name="pyreusion",
    version="1.1.1.0",
    author="JoeYoung",
    author_email="1022104172@qq.com",
    description="Common method integration in the process of Python programming.",
    url="https://github.com/Arludesi/pyreusion.git", 
    python_requires='>=3.6',
    classifiers=['License :: OSI Approved :: GNU General Public License v3 (GPLv3)',],
    packages=find_packages(),

    tests_require=[
        'pytest>=3.3.1',
    ],

    # package_data={
    #     '': ['*.*'],
    #            },

    # exclude_package_data={
    #     '*':['*.bat']
    #            }
)
