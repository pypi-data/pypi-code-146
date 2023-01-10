from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='devops-intc',
    version='0.1.15',
    author='Emilio Reyes, James Gregg',
    author_email='emilio.reyes@intel.com, james.r.gregg@intel.com',
    description='Testing PyPi',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=install_requires,
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires='>=3.7',
    entry_points={
        'console_scripts': ['say-hello=devops_intc.main:main']
    },
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
