from setuptools import setup

setup(name='nb2mail_unify',
      version='0.6',
      description='Convert notebooks to email - bug fix for Unifydb',
      url='https://github.com/scottpersinger/nb2mail',
      author='Neal Fultz',
      author_email='nfultz@gmail.com',
      license='BSD',
      packages=['nb2mail'],
      install_requires=['jupyter'],
      zip_safe=False,
      include_package_data=True,
      entry_points = {
          'nbconvert.exporters': [
              'mail = nb2mail:MailExporter',
          ],
          'nbconvert.postprocessors': [
              'sendmail = nb2mail:SendMailPostProcessor',
          ]
      }
)
