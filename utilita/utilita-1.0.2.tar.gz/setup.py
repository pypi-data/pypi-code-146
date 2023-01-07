from distutils.core import setup
setup(
  name = 'utilita', # How you named your package folder (MyLib)
  packages = ['utilita'], # Chose the same as "name"
  version = '1.0.2', # Start with a small number and increase it with every change you make
  license= 'MIT', # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'a utility library', # Give a short description about your library
  author = 'Jason Yung',
  author_email = 'json.yung@gmail.com',
  url = 'https://github.com/json2d/utilita', # Provide either the link to your github or to your website
  download_url = 'https://github.com/json2d/utilita/archive/v0.4.0.tar.gz',
  keywords = ['starter', 'template', 'python', 'thing'], # Keywords that define your package best
  install_requires= ['isoweek', 'pendulum>=2', 'deprecated', 'openpyxl>=3,<4', 'pandas>=1', 'sendgrid>=6.0.0'],
  classifiers=[
    'Development Status :: 3 - Alpha', # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers', # Define your audience
    'Topic :: Utilities',
    'License :: OSI Approved :: MIT License', # Again, pick a license
    'Programming Language :: Python :: 3', # Specify which pyhton versions that you want to support
    # 'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)