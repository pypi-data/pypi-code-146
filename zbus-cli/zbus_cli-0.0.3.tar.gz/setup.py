from setuptools import setup, find_packages

setup(
    name="zbus_cli",  # Required
    version="0.0.3",  # Required
    extras_require={
        'completion': ['argcomplete3'],
    },
    packages=find_packages(),
    python_requires=">=3.7, <4",
    zip_safe=False,
    author='huangxin',
    author_email='huangxin13066@cvte.com',
    description='Framework for ZBUS command line tools.',
    long_description="""\
The framework provides a single command line script which can be extended with
commands and verbs.""",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={  # Optional
        "console_scripts": [
            "zbus=zbus_cli.cli:main"
        ],
        "zbuscli.command": [
            'topic=zbus_topic.command.topic:TopicCommand',
            'serivce=zbus_service.command.service:ServiceCommand'
        ],
        "zbustopic.verb": [
            'echo=zbus_topic.verb.echo:EchoVerb',
            'hz=zbus_topic.verb.hz:HzVerb',
            'pub=zbus_topic.verb.pub:PubVerb',
            'delay=zbus_topic.verb.delay:DelayVerb',
        ],
        "zbusservice.verb": [
            'call=zbus_service.verb.call:CallVerb',
        ],
    }
)
