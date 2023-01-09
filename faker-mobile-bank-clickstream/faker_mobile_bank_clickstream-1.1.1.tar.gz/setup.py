from distutils.core import setup

setup(
    name = 'faker_mobile_bank_clickstream',
    packages = ['faker_mobile_bank_clickstream'],
    version = '1.1.1',  
    description = 'Mobile Banking Clickstream Faker Provider for Python',
    author = '',
    author_email = '',
    url = 'https://github.com/manganganath/faker-mobile-bank-clickstream',
    download_url = 'https://github.com/manganganath/faker-mobile-bank-clickstream',
    keywords = ['clickstream', 'bank', 'mobile', 'app'],
    install_requires=['Faker'],
    zip_safe=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
    python_requires=">=3.6",
    license='Apache License, Version 2.0',
)
