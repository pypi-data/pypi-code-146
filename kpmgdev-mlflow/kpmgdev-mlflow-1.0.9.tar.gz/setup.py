from setuptools import setup

setup(name='kpmgdev-mlflow',
      version='1.0.9',
      description='kpmgdev-mlflow util package',
      url='https://github.com/yourusername/mypackage',
      author='KPMG Israel',
      author_email='akadosh@kpmg.com',
      license='MIT',
      packages=['kpmgdev.mlflow'],
      install_requires=['azureml-core', 'azureml-mlflow', 'openpyxl',
                        'pandas', 'numpy', 'torch'],
      zip_safe=False)