import setuptools

setuptools.setup(name='pycpil',
        version='1.0.0',
        license='MIT',
        url='https://github.com/nirmalparmarphd/PyCpil',
        description='Predicts deviation in the heat capacity measurement for microDSC Tian-Calvet', 
        long_description=('README.md'),
        author='Nirmal Parmar',
        author_email='nirmalparmarphd@gmail.com',
        packages=setuptools.find_packages(),
        install_requires=['pandas'],
        zip_safe=False)
