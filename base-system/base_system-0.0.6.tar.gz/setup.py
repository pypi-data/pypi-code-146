import os

from setuptools import setup, find_packages

# with open("README.md") as f:
#     long_description = f.read()

# with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
#     README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="base_system",
    version='0.0.6',
    description="Medical system base data",
    keywords='base_system',
    # long_description=README,
    long_description_content_type="text/markdown",
    author='zcjwin',
    author_email='win_zcj@163.com',
    url="https://devcloud.huaweicloud.com/",
    include_package_data=True,
    packages=find_packages(include=('base_system', 'work_scheduling',)),
    zip_safe=False,
    install_requires=[
        'Django>=2.0',
        'djangorestframework>=3.7.0',
        'xlrd2>=1.3.4',
        'pyDes>=2.0.1',
        'drf-excel>=2.1.0',
    ],
    tests_require=[
        'coveralls>=1.11.1',
        'django-allauth==0.50.0',
        'djangorestframework-simplejwt==4.6.0',
        'responses==0.12.1',
        'unittest-xml-reporting==3.0.4',
    ],
    test_suite='runtests.runtests',
    setup_requires=["setuptools_scm"],
    # use_scm_version=True,  # 是否使用pip install git+https://的方式安装
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Framework :: Django",
        "Framework :: Django :: 2",
        "Framework :: Django :: 3",
        "Framework :: Django :: 4",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)

# 打包上传
# python setup2.py bdist_wheel --universal
# python setup2.py bdist_wheel upload

# python setup.py sdist
# pip install twine
# twine upload dist/SongUtils-0.0.1.tar.gz
