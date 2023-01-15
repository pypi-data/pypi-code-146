from setuptools import Extension, setup

setup(
    name='msur-crc',
    version='1.0.1',
    license='MIT',
    author='Photon94',
    author_email='299792458.photon.94@gmail.com',
    install_requires=[
            'importlib-metadata; python_version >= "3.8"',
        ],
    ext_modules=[
        Extension(name='msur_crc.crc16', sources=['crc16/crc16.c'])
    ],
    zip_safe=False,
    long_description='''
MSU Robotics Team CRC library

.. _msur-crc: https://github.com/msu-robotics/msur-crc''',
    url='https://github.com/msu-robotics/msur-crc',
    project_urls={
            "Source": "https://github.com/msu-robotics/msur-crc",
        },
)