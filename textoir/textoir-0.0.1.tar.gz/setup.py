from setuptools import setup,find_packages
setup(name='textoir',
      version='0.0.1',
      description='TEXTOIR is the first high-quality Text Open Intent Recognition platform.',
      author='wangxin',
      author_email='1506542922@qq.com',
      python_requires='>=3.6',
      install_requires= ['botocore==1.21.13','certifi==2021.5.30','charset-normalizer==2.0.4','easydict>=1.9','idna==3.2','jmespath==0.10.0',
                         'joblib==1.0.1','mkl-fft>=1.2.0','mkl-random==1.2.0','mkl-service==2.3.0','pandas==1.1.5','Pillow>=8.2.0',
                         'python-dateutil==2.8.2','pytz==2021.1','regex==2021.8.3','requests==2.26.0','s3transfer==0.5.0','scikit-learn==0.24.2',
                         'scipy==1.5.4','sklearn==0.0','threadpoolctl==2.2.0','transformers==4.16.2','torch==1.7.1','torchaudio>=0.7.0a0+a853dff',
                         'torchvision>=0.8.2','tqdm==4.62.0','urllib3==1.26.6',
                         'absl-py == 0.15.0','asgiref == 3.5.2','astunparse == 1.6.3','backports.zoneinfo == 0.2.1','beautifulsoup4 == 4.11.1',
                         'boto3 == 1.24.16','botocore == 1.27.16','cachetools == 5.2.0','certifi == 2022.6.15','charset-normalizer == 2.0.12',
                         'click == 8.1.3','cycler == 0.11.0','daal == 2021.3.0','Django == 3.2','django-filter == 2.4.0','easydict == 1.9',
                         'faiss-gpu == 1.7.2','filelock == 3.7.1','flatbuffers == 1.12','fonttools == 4.33.3','gast == 0.4.0','gdown == 4.5.1',
                         'google-auth == 2.8.0','google-auth-oauthlib == 0.4.6','google-pasta == 0.2.0','grpcio == 1.34.1','h5py == 3.1.0',
                         'huggingface-hub == 0.8.1','idna == 3.3','importlib-metadata == 4.11.4','jmespath == 1.0.1','joblib == 1.1.0','Keras == 2.4.3',
                         'keras-nightly == 2.5.0.dev2021032900','Keras-Preprocessing == 1.1.2','kiwisolver == 1.4.3','Markdown == 3.3.7',
                         'matplotlib == 3.5.2','munkres == 1.1.4','nlpaug == 1.1.11','nltk == 3.7','numpy == 1.19.5','oauthlib == 3.2.0','opencv-python == 4.5.4.58',
                         'opt-einsum == 3.3.0','packaging == 21.3','pandas == 1.4.3','Pillow == 9.1.1','protobuf == 3.19.4','pyasn1 == 0.4.8','pyasn1-modules == 0.2.8',
                         'PyMySQL == 0.10.1','pyparsing == 3.0.9','PySocks == 1.7.1','python-dateutil == 2.8.2','pytorch-metric-learning == 1.5.0','pytorch-pretrained-bert == 0.6.2',
                         'pytz == 2022.1','regex == 2022.6.2','requests == 2.28.0','requests-oauthlib == 1.3.1','rsa == 4.8','s3transfer == 0.6.0','scikit-learn == 0.24.1',
                         'scikit-learn-intelex == 2021.3.0','scipy == 1.8.1','six == 1.15.0','sklearn == 0.0','soupsieve == 2.3.2.post1','sqlparse == 0.4.2',
                         'tbb == 2021.6.0','tensorboard == 2.9.1','tensorboar-data-server == 0.6.1','tensorboard-plugin-wit == 1.8.1','tensorflow-estimator == 2.5.0',
                         'tensorflow-gpu == 2.5.1','termcolor == 1.1.0','threadpoolctl == 3.1.0','tokenizers == 0.12.1','torch == 1.8.1+cu111','torchvision == 0.9.1',
                         'tqdm == 4.64.0','transformers == 4.20.1','typing-extensions == 3.7.4.3','urllib3 == 1.26.9','Werkzeug == 2.1.2','wrapt == 1.12.1','zipp == 3.8.0'], # 定义依赖哪些模块
      packages=find_packages(),  # 系统自动从当前目录开始找包
      # 如果有的包不用打包，则只能指定需要打包的文件
      #packages=['代码1','代码2','__init__']  #指定目录中需要打包的py文件，注意不要.py后缀
      license='apache 3.0'
      )


#name : 打包后包的文件名
#version : 版本号
#author : 作者
#author_email : 作者的邮箱
#py_modules : 要打包的.py文件
#packages: 打包的python文件夹
#include_package_data : 项目里会有一些非py文件,比如html和js等,这时候就要靠include_package_data 和 package_data 来指定了。package_data:一般写成{‘your_package_name’: [“files”]}, include_package_data还没完,还需要修改MANIFEST.in文件.MANIFEST.in文件的语法为: include xxx/xxx/xxx/.ini/(所有以.ini结尾的文件,也可以直接指定文件名)
#license : 支持的开源协议
#description : 对项目简短的一个形容
#ext_modules : 是一个包含Extension实例的列表,Extension的定义也有一些参数。
#ext_package : 定义extension的相对路径
#requires : 定义依赖哪些模块
#provides : 定义可以为哪些模块提供依赖
#data_files :指定其他的一些文件(如配置文件),规定了哪些文件被安装到哪些目录中。如果目录名是相对路径,则是相对于sys.prefix或sys.exec_prefix的路径。如果没有提供模板,会被添加到MANIFEST文件中。
