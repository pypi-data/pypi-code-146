from setuptools import setup

setup(name='kpmgdev-mlflow',
      version='1.0.6',
      description='kpmgdev-mlflow util package',
      url='https://github.com/yourusername/mypackage',
      author='KPMG Israel',
      author_email='akadosh@kpmg.com',
      license='MIT',
      packages=['kpmgdev-mlflow'],
      install_requires=['azure-core', 'azureml-mlflow', 'openpyxl',
                        'pandas', 'numpy'],
      zip_safe=False)