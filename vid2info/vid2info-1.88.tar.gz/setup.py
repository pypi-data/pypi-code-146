from setuptools import setup, find_namespace_packages

setup(
    name='vid2info',
    version='1.88',
    packages=find_namespace_packages(),
    package_dir={'vid2info': 'vid2info'},
    url='https://github.com/Eric-Canas/vid2info',
    license='MIT',
    author='Eric Canas',
    author_email='elcorreodeharu@gmail.com',
    description='Vid2Info is an easy-to-use Computer Vision pipeline that implements Detection, Tracking and, '
                'optionally, Segmentation.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'numpy',
        'matplotlib',
        'pycocotools',
        'scipy',
        'cython',
        'opencv-python',
    ],
    dependency_links=['https://github.com/samson-wang/cython_bbox.git#egg=cython-bbox'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3',
    ]
)
