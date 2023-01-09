from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='pil_plus',
    version='0.2',
    license='APACHE-2.0',
    author="Fahad Maqsood Qazi",
    author_email='qazifahadmaqsood@gmail.com',
    long_description_content_type='text/markdown',
    long_description=long_description,
    py_modules=['pil_plus'],
    url='https://github.com/fahadmaqsood/pil_plus',
    keywords=['PIL', 'image processing', 'PIL wrapper', 'easy PIL', 'pillow'],
    install_requires=[
          'opencv-python',
          'pillow',
          'matplotlib',
          'numpy',
          'backgroundremover'
      ],
)