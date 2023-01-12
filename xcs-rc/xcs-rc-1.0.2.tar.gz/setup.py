import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='xcs-rc',
    version='1.0.2',
    url='https://github.com/nuggfr/xcs-rc-python',
    license='MIT',
    author='Nugroho Fredivianus',
    author_email='nuggfr@gmail.com',
    description='Accuracy-based Learning Classifier Systems with Rule Combining',
    long_description = long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(include=['xcs_rc']),
    install_requires=['pandas','numpy'],
    keywords='machine learning, reinforcement learning, classifier systems, rule-based',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
