import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np




def features_summary(data_frame):
    # Getting Numerical and Categorical columns Separately
    num_cols = df.select_dtypes(np.number).columns
    for feature_name in num_cols:
        print(f"Exploring {str(feature_name).upper()}........")
        print(f"Mean of {feature_name}     : {data_frame[feature_name].mean()}")
        print(f"Median of {feature_name}   : {data_frame[feature_name].median()}")
        print(f"Mode of {feature_name}     : {data_frame[feature_name].mode()}")
        print(f"Variance of {feature_name} : {data_frame[feature_name].var()}")
        print(f"Skewness of {feature_name} : {data_frame[feature_name].skew()}")
        print(f"Maximum of {feature_name}  : {data_frame[feature_name].max()}")
        print(f"Minimum of {feature_name}  : {data_frame[feature_name].min()}")
        # Drawing plots
        plt.figure(figsize=(17, 4))
        fig=plt.figure(figsize=(17, 4))
        plt.subplot(131)
        sns.kdeplot(data_frame[feature_name])
        #boxplots
        plt.subplot(132)
        sns.boxplot(data_frame[feature_name])
  


def drop_features(data_frame,features,criteria=None,inplace=False):
    '''
    this function allow us to drop features in the dataset based on the criteria
    '''
    if inplace==True and criteria==None:
        return data_frame.drop(features,axis=1,inplace=True)
    elif inplace==True and criteria=="nan":
        nulls=(data_frame.isnull().sum()/data_frame.shape[0])*100
        return data_frame.drop(nulls[nulls>=30].index,axis=1,inplace=True)
    elif inplace==False and criteria==None:
        return data_frame.drop(features,axis=1)
    else:
        return data_frame.drop(features,axis=1)