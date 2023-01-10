from setuptools import setup


def read_files(files):
    data = []
    for file in files:
        with open(file, encoding='utf-8') as f:
            data.append(f.read())
    return "\n".join(data)


meta = {}
with open('strapi_api_client/version.py') as f:
    exec(f.read(), meta)

setup(
    name='strapi-api-client',
    version=meta['__version__'],
    packages=[
        'strapi_api_client',
        'strapi_api_client.resources'
    ],
    install_requires=[],
    url='https://github.com/culturepulse/strapi-api-client',
    license='MIT',
    author='Adam Žúrek',
    author_email='adam@culturepulse.ai',
    description='Strapi API Client is used for maintaining a communication with the '
                'Strapi CMS by HTTP transfer protocol.',
    long_description=read_files(['README.md', 'CHANGELOG.md']),
    long_description_content_type='text/markdown',
    classifiers=[
        # As from https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: System :: Networking',
        'Topic :: Communications',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
