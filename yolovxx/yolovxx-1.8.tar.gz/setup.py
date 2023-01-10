from distutils.core import setup
setup(
  name = 'yolovxx',         # How you named your package folder (MyLib)
  packages = ['yolovxx', 'yolovxx.yolov7', 'yolovxx.yolov7.nets',
               'yolovxx.yolov7.utils', 'yolovxx.yolox', 'yolovxx.yolox.nets',
               'yolovxx.yolox.utils', 'yolovxx.yolov5', 'yolovxx.yolov5.nets',
               'yolovxx.yolov5.utils'],  # Chose the same as "name"
  version = '1.8',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'run all yolo detectors (training and inference)',   # Give a short description about your library
  author = 'NasAir',                   # Type in your name
  author_email = 'me@domain.com',      # Type in your E-Mail
  url = 'https://hoolme.ai',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
        'scipy',   
        'numpy',   
        'matplotlib',
        'opencv_python',
        'torch',
        'torchvision',
        'tqdm',
        'Pillow',
        'h5py',
        'tensorboard',
        'thop',
        'onnx',
        'onnxsim',
        'onnxruntime',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)