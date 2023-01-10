import setuptools

setuptools.setup(name='pycpep',
        version='1.0.4',
        license='MIT',
        url='https://github.com/nirmalparmarphd/PyCpep',
        description='Predicts deviation in the heat capacity measurement for microDSC Tian-Calvet', 
        long_description='README.md',
        author='Nirmal Parmar',
        author_email='nirmalparmarphd@gmail.com',
        packages=setuptools.find_packages(),
        include_package_data=True,
        package_data={'': ['mdl/*.h5', 'mdl/*.pkl','mdl/*.hdf5']},
        install_requires=['scikit-learn','tensorflow','numpy', 'h5py','keras', 'gitpython', 'pandas'],
        zip_safe=False)
