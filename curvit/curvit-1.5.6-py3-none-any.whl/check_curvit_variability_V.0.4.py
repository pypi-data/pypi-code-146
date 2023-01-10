#!/usr/bin/env python3

import numpy as np
from glob import glob
import warnings
warnings.filterwarnings("ignore")

def variability_measure(filename):
    data = np.genfromtxt(filename)
    variance = np.var(data[:, 1], ddof = 1) 
    mean_squared_error = np.mean(data[:, 2] ** 2)
    R = variance / mean_squared_error
    R = np.round(R, 2)
    return R
    
def normalized_excess_variance(filename):
    data = np.genfromtxt(filename)
    variance = np.var(data[:, 1], ddof = 1) 
    data_mean_squared = np.mean(data[:, 1]) ** 2
    mean_squared_error = np.mean(data[:, 2] ** 2)
    F = ((variance - mean_squared_error) / data_mean_squared) ** 0.5
    F = np.round(F, 2)
    
    F_err = ((((2 * len(data)) ** -0.5) * (mean_squared_error / (data_mean_squared * F))) ** 2 + \
    (((mean_squared_error / len(data)) ** 0.5) * data_mean_squared ** -0.5) ** 2) ** 0.5
    F_err = np.round(F_err, 2)
 
    return F, F_err 
    
datfiles = glob('*dat')
for dat in datfiles:
    R = variability_measure(dat)
    F, F_err = normalized_excess_variance(dat)
    if np.isnan(F) == False:
        print('{}, F = {}, F_err = {}, R = {}'.format(dat, F, F_err, R))
    
