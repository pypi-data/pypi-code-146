from setuptools import setup

setup(name='PyWaves',
      version='0.9.0',
      description='Object-oriented library for the Waves blockchain platform',
      url='http://github.com/pywaves/pywaves',
      author='PyWaves Developers',
      author_email='dev@pywaves.org',
      license='MIT',
      packages=['pywaves', 'pywaves/protobuf', 'pywaves/protobuf/waves'],
      keywords = ['waves', 'blockchain', 'analytics'],
      install_requires=[
	    'base58==0.2.5',
            'pyblake2',
            'python-axolotl-curve25519',
            'requests',
	    'google-api-python-client',
	    'protobuf==3.19.6'
      ]
      )


