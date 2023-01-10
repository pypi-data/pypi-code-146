from distutils.core import setup

setup(
    name='handyfunctions',  # How you named your package folder (MyLib)
    packages=['handyfunctions'],  # Chose the same as "name"
    version='0.1',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='This package contains several handy python functions for deep learning projects',  # Give a short description about your library
    author='Isaac Osei Agyemang',  # Type in your name
    author_email='agyemangisaac45@gmail.com',  # Type in your E-Mail
    url='https://github.com/user/reponame',  # Provide either the link to your github or to your website
    download_url='https://github.com/user/reponame/archive/v_01.tar.gz',  # I explain this later on
    keywords=['Deep learning', 'Computer vision', 'Convolutional neural networks'],  # Keywords that define your package best
    install_requires=[  # I get to this in a second
        'opencv-python',
        'numpy',
        'matplotlib',
        'sklearn',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3.6',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
