import setuptools

setuptools.setup(name='pycpil',
        version='1.0.1',
        license='MIT',
        url='https://github.com/nirmalparmarphd/PyCpil',
        description='PyCpil is a pip pkg to calculate isobaric heat capacity of ionic liquids and ionanofluids (nanofluids)', 
        long_description=('README.md'),
        author='Nirmal Parmar',
        author_email='nirmalparmarphd@gmail.com',
        packages=setuptools.find_packages(),
        install_requires=['pandas'],
        zip_safe=False)
