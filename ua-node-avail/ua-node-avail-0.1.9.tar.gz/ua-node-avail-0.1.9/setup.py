import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()


setuptools.setup(
        name="ua-node-avail",
        version="0.1.9",
        scripts=['bin/node_avail', "bin/job_memcheck"],
        author="Tristan Maxson",
        author_email="tgmaxson@gmail.com",
        description="Tool to monitor node availablility at UA",
        long_description=long_description,
        long_description_content_type="text/markdown",
        project_urls={
            'Gitlab': 'https://gitlab.com/szilvasi-lab/ua-node-avail'
            },
        python_requires=">=3",
        install_requires=[
            'columnar',
        ],
        packages=setuptools.find_packages(),
        classifiers=[
            "Intended Audience :: Science/Research",
            "Programming Language :: Python :: 3",
            "Topic :: Scientific/Engineering"]
        )

