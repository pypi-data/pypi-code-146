from setuptools import setup
  
long_description = 'Package to check if private repository libraries have a public doppelgaenger with the same name. The goal is to prevent a dependency confusion attack on the PyPi ecosystem.'
  
setup(
        name ='pvpcheck',
        version ='1.1.0',
        author ='Robert Cooper Buer McKee',
        author_email ='RCBM@duck.com',
        url ='https://github.com/rcmckee/pvpcheck',
        description ='Package to check if private repository libraries have a public doppelgaenger with the same name. The goal is to prevent a dependency confusion attack on the PyPi ecosystem.',
        long_description = long_description,
        long_description_content_type ="text/markdown",
        license ='MIT',
        packages = ["pvpcheck"],
        entry_points ={
            'console_scripts': [
                'pvpcheck = pvpcheck.public_vs_private_pypi_check:main'
            ]
        },
        classifiers =(
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ),
        keywords ='pypi dependency confusion attack python package pvpcheck public private library index comparison ',
        install_requires = [],
        zip_safe = False
)