"""
This script contains code for generating plots like roc-auc, precision, recall, confusion matrix, etc.
"""

# Imports
import matplotlib.pyplot as plt
import seaborn as sns
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S')
logger = logging.getLogger(__name__)


"""
Author: vickyparmar
File: classic_ml_plots.py
Created on: 07-10-2022, Fri, 1:51:58

Last modified by: vickyparmar
Last modified on: 07-10-2022, Fri, 1:51:59
"""

