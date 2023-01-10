#!/usr/bin/env python3 

import os
from warnings import WarningMessage
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import balanced_accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, ConfusionMatrixDisplay

def median_of_ratios_normalisation(_data : pd.DataFrame) -> pd.DataFrame:
    """
    Normalize a dataframe with the median of ratios method 
    from DESeq2. 
    
   
    input data (as a pandas dataframe), e.g.:
    
            sample1    sample2    sample3
    gene1   0.00000    10.0000    4.00000
    gene2   2.00000    6.00000    12.0000
    gene3   33.5000    55.0000    200.000
    
    normalized output:
            sample1    sample2    sample3
    gene1   0.00000    10.6444    1.57882
    gene2   4.76032    6.38664    4.73646
    gene3   78.5453    58.5442    78.9410
    
    References
    ----------
    StatQuest: https://www.youtube.com/watch?v=UFB993xufUU
    HBC Harvard: https://hbctraining.github.io/DGE_workshop/lessons/02_DGE_count_normalization.html

    """
    # step 1: log normalize
    log_data = np.log(_data)

    # step 2: average rows
    row_avg = np.mean(log_data, axis=1)
    
    # step 3: filter rows with zeros
    rows_no_zeros = row_avg[row_avg != -np.inf].index
    
    # step 4: subtract avg log counts from log counts
    ratios = log_data.loc[rows_no_zeros].subtract(row_avg.loc[rows_no_zeros], axis=0)
    
    # step 5: calculate median of ratios
    medians = ratios.median(axis=0)
    
    # step 6: median -> base number
    scaling_factors = np.e ** medians
    
    # step 7: normalize!
    normalized_data = _data / scaling_factors
    return normalized_data

def calculate_percentile(df, my_percentile=50):
    '''
    Compute the q-th percentile of data.
    Returns the q-th percentile of the array elements.

    Parameters
    ----------
    my_percentile: float, optional
        Percentile which must be between 0 and 100.
      
    See also
    ---------
    numpy.percentile()
    https://numpy.org/doc/stable/reference/generated/numpy.percentile.html
    '''
    my_array = df.to_numpy()
    percentile_of_df = np.percentile(my_array, my_percentile)
    return percentile_of_df

def compute_metrics_classification(y_predictions, y_trues, positive_class):
    '''
    Compute a series of metrics for classification tasks

    Util function designed to work downstream of the search for the best model. 
    Will compute the following metrics:
      - balanced accuracy
      - precision
      - recall
      - f1 score

    Parameters
    ----------
    y_predictions: list
      List of class predictions. 
    y_trues: list
      List of the true values (from the test set)
    positive_class: str
      The name of the positive class for calculation of true positives, true negatives, etc. 

    Returns
    -------
    model_metrics_df: `pandas.core.frame.DataFrame`
      Dataframe with the balanced accuracy, precision, recall and f1 score calculated. 

    See also
    --------
    https://scikit-learn.org/stable/modules/model_evaluation.html
    '''
    
    balanced_accuracy = balanced_accuracy_score(y_pred=y_predictions, y_true=y_trues)
    precision = precision_score(y_pred=y_predictions, y_true=y_trues, pos_label=positive_class)
    recall = recall_score(y_pred=y_predictions, y_true=y_trues, pos_label=positive_class)
    f1 = f1_score(y_true=y_trues, y_pred=y_predictions, pos_label=positive_class)
    
    model_metrics_dict = {"balanced_accuracy": balanced_accuracy, "precision": precision, "recall": recall, "f1 score": f1}
    model_metrics_df = pd.DataFrame.from_dict(model_metrics_dict, orient="index", columns=["value"])
    model_metrics_df_rounded = model_metrics_df.round(3)

    return model_metrics_df_rounded 

def plot_confusion_matrix(y_predictions, y_trues):
    '''
    Plot confusion matrix

    Parameters
    ----------
    y_predictions: list
      List of class predictions. 
    y_trues: list
      List of the true values (from the test set)
    positive_class: str
      The name of the positive class for calculation of true positives, true negatives, etc. 

    Returns
    -------
    model_metrics_df: `pandas.core.frame.DataFrame`
      Dataframe with the balanced accuracy, precision, recall and f1 score calculated. 

    See also
    --------
    https://scikit-learn.org/stable/modules/model_evaluation.html
    '''
    cm = confusion_matrix(y_true=y_trues, y_pred=y_predictions)
    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm)
    disp.plot()
    plt.show()


def extract_samples_to_condition(df, name_grouping_var='genotype', separator_replicates='_'):
    '''
    A utility function to extract the grouping factor (e.g. 'genotype') from sample names. 
    
    Uses melting (wide to long) and split grouping variable from biological replicates using specified separator.
    
    Parameters
    ----------
    df: pandas.core.DataFrame
    name_grouping_var: str, optional 
        Name of the variable used as grouping variable (default is 'genotype').
    separator_replicates: str, optional
        The separator between the grouping variable and the biological replicates ( default is underscore '_')
    
    Returns
    -------
    A dataframe with the correspondence between samples and experimental condition (grouping variable).

    Notes
    -------
    Input dataframe
                        | genotypeA_rep1 | genotypeA_rep2 | genotypeA_rep3 | genotypeA_rep4 |
                        |----------------|----------------|----------------|----------------|
          feature_id
        | metabolite1   |   1246         | 1245           | 12345          | 12458          |
        | metabolite2   |   0            | 0              | 0              | 0              |
        | metabolite3   |   10           | 0              | 0              | 154            |
    
    Output dataframe
        
        | sample             | genotype       | replicate      |
        |--------------------|----------------|----------------|
        | genotypeA_rep1     |   genotypeA    | rep1           |
        | genotypeA_rep2     |   genotypeA    | rep2           |
        | genotypeA_rep3     |   genotypeA    | rep3           |
        | genotypeA_rep4     |   genotypeA    | rep4           |
        | etc.
    '''
    melted_df = pd.melt(df.reset_index(), id_vars='feature_id', var_name="sample")
    melted_df[[name_grouping_var, 'rep']] = melted_df["sample"].str.split(pat=separator_replicates, expand=True)
    melted_df_parsed = melted_df.drop(["feature_id", "value"], axis=1)
    melted_df_parsed_dedup = melted_df_parsed.drop_duplicates()
    return melted_df_parsed_dedup
