#  /************** Begin Copyright - Do not add comments here **************
#   * Licensed Materials - Property of IBM
#   *
#   *   OCO Source Materials
#   *
#   *   (C) Copyright IBM Corp. 2020, All Rights Reserved
#   *
#   * The source code for this program is not published or other-
#   * wise divested of its trade secrets, irrespective of what has
#   * been deposited with the U.S. Copyright Office.
#   ***************************** End Copyright ****************************/

"""
Implementation of partial correlation conditional independence test
"""


import numpy as np 
from pybnesian import LinearCorrelation
import pandas as pd

class ParCorrTest:
    """
    Processes inputs and invokes the partial correlation test using LinearCorrelation function from pybnesian library.     
    """

    def __init__(self):
        self.measure="Partial Correlation Test"


    def set_data(self,data_array):
        assert isinstance(data_array,np.ndarray), 'ParCorrTest class can be initialized only with a numpy ndarray'
        assert len(data_array.shape)==2, 'ParCorrTest class needs a 2-D array'
        self.T=data_array.shape[0]
        self.N=data_array.shape[1]
        self.data=data_array



    def run_test(self,x,y,z,tau_max=1):
        assert x<self.N, 'x should be an integer index less than total number of vars'
        assert y<self.N, 'y should be an integer index less than total number of vars'
        if isinstance(z,tuple):
            z=list(z)
        assert isinstance(z,list), 'z should be a list of integers'
        assert tau_max>0, 'tau_max should be at least 1'

        # Collecting valid X_{t-tau_max} as X'
        x_prime=self.data[0:self.T-tau_max,x]
        # Collecting valid Y_{t} as Y'
        y_prime=self.data[tau_max:,y]
        array_tested=np.vstack((x_prime,y_prime))
        ind_x=0
        ind_y=1

        ######Collecting conditioning variables as Z_prime #########
        # Collecting valid Y_{t-1}....Y_{t-tau_max}
        for i in range(1,tau_max+1):
            np.vstack((array_tested,self.data[tau_max-i:self.T-i,y]))
        # For every c in list z, collecting c_{t-1}.....c_{t-tau_max}
        # If z list is empty the following two lines will not run
        for c in z:
            for i in range(1,tau_max+1):
                np.vstack((array_tested,self.data[tau_max-i:self.T-i,c]))

        #Transpose array_tested
        array_tested=np.transpose(array_tested)


        #Collecting all conditioning variables' indices in array_tested
        ind_z=list(np.arange(array_tested.shape[1]-2)+2)
        ind_z=[str(s) for s in ind_z]
        #Call the pnb_correlation tester after shuffling rows randomly
        np.random.shuffle(array_tested)
        return self.call_pnb_linear_correlation(array_tested,str(ind_x),str(ind_y),ind_z)


    def call_pnb_linear_correlation(self,array_tested,x,y,z):
        assert isinstance(array_tested,np.ndarray), 'Expects a numpy ndarray'
        cols=array_tested.shape[1]
        data_frame=pd.DataFrame(array_tested,columns=[str(i) for i in np.arange(cols)])
        if len(z)==1:
            return LinearCorrelation(data_frame).pvalue(x,y,z[0])
        if len(z)>1:
            return LinearCorrelation(data_frame).pvalue(x,y,z)
        else:
            return LinearCorrelation(data_frame).pvalue(x,y)





