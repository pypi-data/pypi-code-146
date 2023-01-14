##################################################################################
AUTHOR = 'Imran Nazir'
BATCH = 2022-2024
ROLLNO='MSDSF22M002'
##################################################################################


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def data_summary(df, name=""):
    # Printing basic detail of data like name, size, shape
    print(f"Data Summary")
    print(f"Size {df.size}")
    print(f"Features {df.shape[1]}")
    print(f"Records {df.shape[0]}")
    print("="*100)

    
    # Getting Numerical and Categorical columns Separately
    cat_cols = df.select_dtypes(np.object).columns
    num_cols = df.select_dtypes(np.number).columns

    # Printing the Numerical columns
    print("Dataset has following Numerical columns...")
    for i, j in enumerate(num_cols):
        print(f" {i+1}) {j}")
    
    print("="*100)
    
    # Printing the Categorical columns
    print("Dataset has following Categorical columns...")
    for i, j in enumerate(cat_cols):
        print(f" {i+1}) {j}")
    
    print("="*100)
    
    # Displaying statistical properties of data like mean, median, max, min
    print("Statistical Properties of Data....")
    display(df.describe(include="all"))
    print("="*100)
    
    # Displaying correlation of numerical features
    corr = df.corr(method="kendall").style.background_gradient("YlOrRd_r")
    print("Correlation of Numerical features....")
    display(corr)
    

def null_summary(data_frame):
	'''
	this function gets data frame as argument 
	and return summary of null values present in the datast
	'''
	nulls=data_frame.isnull().sum()
	fig,ax = plt.subplots(figsize=(12,8))
	sns.barplot(x=nulls.values,y=nulls.index)
	for container in ax.containers:
	    ax.bar_label(container)
	ax.set(title="Summary of Null Values")
	plt.show()

def null_percent(data_frame,limit):
	'''
	this function returns the feature that contains percentage 
	of null values greater than equal to limit
	'''
    nulls_percent=data_frame.isnull().sum()/data_frame.shape[0]*100
    return nulls_percent[nulls_percent>=limit]





