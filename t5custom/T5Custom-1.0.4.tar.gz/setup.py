from setuptools import setup, find_packages

VERSION = '1.0.4'
DESCRIPTION = 'Custom T5 model creation with own csv training dataset'
LONG_DESCRIPTION = """To run this customT5 need a training dataset which have two coloumns "UseCase" which is a target and "Sentences" which is a source variable.

Ex:
	!pip install T5Custom

    from T5Custom import main
	import pandas as pd
	path = "https://github.com/nikuraj006/customeT5/blob/main/T5_training%20Data.csv"
	df = pd.read_csv(path).dropna()
	
	main.trainModel(df,True) # to train Model
	
	
"""

# Setting up
setup(
    name="T5Custom",
    version=VERSION,
    author="Sushil Ranjan",
    author_email="nikuraj006@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["pandas","sklearn","scikit-learn","torch","numpy","transformers","flask","pytorch_lightning","flask-cors","num2words"],
    keywords=['python', 'T5', 'T5-Base', 'T5-Large', 'T5-Small'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
