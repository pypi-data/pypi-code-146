#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name='raclahe',
    version='0.1.2',    
    description='Original package to support Region Adaptive Magnetic Resonance Image Enhancement for improving CNN based segmentation of the prostate and prostatic zones paper',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dzaridis/RACLAHE_Image_Enhancement_for_CNN_model_segmentation',
    author='Dimitris Zaridis',
    author_email='dimzaridis@gmail.com',
    license='MIT',
    packages=['raclahe'],
    install_requires=['numpy','protobuf==3.19.6',
'scikit_image',
'pydicom',
'opencv_python==4.5.1.48',
'tensorflow==2.2.0',
'numpy',
'matplotlib',
'keras_unet_collection==0.1.11',
'pandas',
'glob2',
'nibabel==3.2.1'])

