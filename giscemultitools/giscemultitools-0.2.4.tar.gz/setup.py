from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    INSTALL_REQUIRES = f.readlines()

setup(
    name='giscemultitools',
    description='Llibreria d\'utilitats',
    author='GISCE',
    author_email='devel@gisce.net',
    url='http://www.gisce.net',
    version='0.2.4',
    license='General Public Licence 2',
    long_description='''Long description''',
    provides=['giscemultitools'],
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
    entry_points="""
            [console_scripts]
            gisce_github=giscemultitools.githubutils.scripts.github_cli:github_cli
            gisce_slack=giscemultitools.slackutils.scripts.slack_cli:slack_cli
        """,
    scripts=[]
)
