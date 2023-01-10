from setuptools import setup

setup(name='kpmgdev-mlflow',
      version='1.0.4',
      description='kpmgdev-mlflow util package',
      url='https://github.com/yourusername/mypackage',
      author='KPMG Israel',
      author_email='akadosh@kpmg.com',
      license='MIT',
      packages=['kpmgdev-mlflow'],
      install_requires=['azure-core', 'azure-mlflow', 'openpyxl', 'scikit-learn',
                        'pandas', 'numpy'],
      zip_safe=False)