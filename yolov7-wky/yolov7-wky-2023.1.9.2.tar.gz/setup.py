import setuptools
from pathlib import Path

VERSION = '2023.01.09.2'

requirements = [
    'flatbuffers==23.1.4',
    'onnxsim==0.4.13',
    'tensorflow_probability==0.16.0',
    'matplotlib>=3.2.2',
    'numpy>=1.18.5,<1.24.0',
    'opencv-python>=4.1.1',
    'Pillow>=7.1.2',
    'PyYAML>=5.3.1',
    'requests>=2.23.0',
    'scipy>=1.4.1',
    'torch==1.11.0',
    'torchvision==0.12.0',
    'tqdm>=4.41.0',
    'protobuf<4.21.3',
    'tensorboard>=2.4.1',
    'pandas>=1.1.4',
    'seaborn>=0.11.0',
    'ipython',
    'psutil',
    'thop'
]

this_directory = Path(__file__).parent
long_description = (this_directory / "README.dst").read_text()


def setup():
    setuptools.setup(
        packages=setuptools.find_packages(),
        include_package_data=True,
        install_requires=requirements,
        python_requires='>=3.10',
        author='biantsh',
        version=VERSION,
        name='yolov7-wky',
        long_description=long_description,
        long_description_content_type='text/markdown',
        entry_points={
            'console_scripts': [
                'yolov7_detect=python_scripts.detect:main',
                'yolov7_export=python_scripts.export:main',
                'yolov7_hubconf=python_scripts.hubconf:main',
                'yolov7_test=python_scripts.test:main',
                'yolov7_train=python_scripts.train:main',
                'yolov7_train_aux=python_scripts.train_aux:main'
            ],
        },
    )


if __name__ == '__main__':
    setup()
