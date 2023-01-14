from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup_args = dict(
     name='shynais',
     version='0.0.07',
     packages=find_packages(),
     author="Shivam Sharma",
     author_email="shivamsharma1913@gmail.com",
     description="Shyna question power package.BASIC",
     long_description=long_description,
     long_description_content_type="text/markdown",
    )

install_requires = [
    "setuptools",
    "wheel",
    "ShynaDatabase",
    "ShynaWeather",
    "ShynaGreetings",
    "Shynatime",
    'haversine',
    'Shyna_speaks',
    "python-telegram-bot",
    "ShynaTelegramBotNotification",
    "wget"
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
