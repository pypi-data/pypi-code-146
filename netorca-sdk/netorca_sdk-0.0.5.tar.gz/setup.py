from distutils.core import setup
setup(
  name = 'netorca_sdk',
  packages = ['netorca_sdk', 'netorca_sdk.elements', 'netorca_sdk.utils'],
  version = '0.0.5',
  license='MIT',
  description = 'A package for interacting with the NetOrca API',
  author = 'Scott Rowlandson',
  author_email = 'scott@netautomate.org',
  url = 'https://gitlab.com/netorca_public/netorca_sdk/',
  keywords = ['netorca', 'orchestration', 'netautomate'],
  install_requires=[
          'requests',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
  ],
)