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
MMPC algorithm implementation and interface classes
"""

import numpy as np
import pandas as pd

import networkx as nx
from graphviz import Digraph

import autoai_ts_libs.deps.tspy
from autoai_ts_libs.deps.tspy.time_series import time_series
from autoai_ts_libs.deps.tspy.ml.causal_modeling.algorithms.estimators import CausalityEstimator
from autoai_ts_libs.deps.tspy.ml.causal_modeling.algorithms.mmpc_utils import mmpcBase 
from autoai_ts_libs.deps.tspy.ml.causal_modeling.algorithms.ParCorrTest import ParCorrTest


class MMPCInputDatatypeAdapter: 
    """ 
    This is a class that provides a namespace for a collection of static methods which given 

    1. a representation of multivariate timeseries data of some type including 
    dataframe, array, or autoai_ts_libs.deps.tspy timeseries,
    
    2. a specification of the location in the representation containing timestamps and event types 
    
    Returns a imeseries represented as a dataframe which is used internally by the MMPC algorithm. 
    """ 
    
    @staticmethod 
    def from_dataframe(data, ts_column=None):
        """ 
          Accept data as pandas dataframe
        """
        if (ts_column==None):
            return data
        else:
            data_copy = data.copy()
            _ = data_copy.pop(ts_column)
            return (data_copy)
        
    @staticmethod
    def from_timeseries(data, ts_column): 
        """ 
          Accept data as autoai_ts_libs.deps.tspy object
        """
        data_df = data.to_df() 
        data_df = MMPCInputDatatypeAdapter.from_dataframe(data_df, ts_column=ts_column) 
        return (data_df) 
        
        
    @staticmethod 
    def from_array(data, ts_column=None): 
        """ 
          Accept data as numpy array
        """            
        data_copy = np.copy(data) 
        if ~(ts_column == None): 
            ts_column_idx = int(ts_column) 
            data_copy = np.delete(data_copy, ts_column_idx, axis=1) 
        else: 
            data_df = pd.DataFrame(data_copy) 
        return data_df 
        
    
    @staticmethod 
    def from_data(data, ts_column=None):
        """ 
          Processes autoai_ts_libs.deps.tspy, pandas, or numpy array object into a format 
          suitable for MMPC algorithm. 
        """                    
        if isinstance(data, pd.DataFrame):
            df = MMPCInputDatatypeAdapter.from_dataframe(data, ts_column)
            
        elif isinstance(data, autoai_ts_libs.deps.tspy.data_structures.time_series.TimeSeries.TimeSeries):
            if (ts_column==None): ts_column='timestamp'
            df = MMPCInputDatatypeAdapter.from_timeseries(data, ts_column)
            
        elif isinstance(data, np.ndarray):
            df = MMPCInputDatatypeAdapter.from_array(data, ts_column)
                    
        return df
 

    
class MMPC(CausalityEstimator):
    """
    Causal discovery algorithm for time series based on conditional independence tests. 
    For more details see: https://arxiv.org/abs/1805.09909

    MMPC-p is a 2-step causal discovery method for large-scale time series
    datasets. In the first phase, possible causes are detected using conditional 
    independence tests. In the second phase, the possible causes are further pruned
    to remove false positives.

    By default 'ParCorrTest' conditional independence test is used. 
    """

    
    def __init__(self):
        super(MMPC, self).__init__()
        return
        
        
    def fit(self, 
            data, 
            cond_ind_test=ParCorrTest(), 
            K=2, 
            verbosity=0, 
            phase1_alpha=0.2, 
            beta=0.05, 
            tau_max=1, 
            seed=0): 
            
        """ 
        Fits MMPC causal model on multivariate timeseries data. 
        
        Parameters
        ----------
        
        cond_ind_test: conditional independence test function
            This can be any external test passed as a callable, default: ParCorrTest. 

        K: int 
            Number of elements removed at a time from candidate parents to calculate association in phase 1.

        verbosity: int, optional (default: 0)
            Verbose levels 0, 1, ...

        phase1_alpha: float 
            Significance threshold used in Phase 1 of MMPC algorithm. 

        beta: float
            Threshold used in phase 2 of MMPC algorithm

        tau_max: int 
            Maximum time lag

        seed: int
            Random seed value

        Returns
        -------

        self: MMPC object
            can be used to access internal variables after fit()
        """
        
        self.vars = data.columns
        
        dataset=data.to_numpy() 
        dataset=dataset.astype(float) 
        
        T = dataset.shape[0] 
        nvars = dataset.shape[1] 
        self.targets = np.arange(nvars) # set this to targets to run on the whole graph  
        
        
        self.mmpc_parcorr_phase1_results = dict([('CPC',dict()), ('minassocs',dict())]) 
        self.mmpc_parcorr_phase2_results = dict([('trimmed_CPC',dict()), ('pvalues',dict())]) 
                
        for target in self.targets: 
            self.mmpc = mmpcBase(
                dataset=dataset,
                cond_ind_test=cond_ind_test, 
                # to calculate assoc in Phase 1, remove at most 
                # K elements at a time from Candidate Parents 
                K=K, 
                verbosity=verbosity,
                phase1_alpha=phase1_alpha,
                # infer edges for target, can accomodate multiple targets. 
                # if we want it for all variables, then set selected_variables = None
                selected_variables=[target], 
                # test for parents among all variables. if we want to test for a subset, 
                # say [0,1] as parents, then set selected_parents = [0,1]
                selected_parents=None, 
                seed=seed
            )
            
            phase1 = self.mmpc.run_phase1(self.mmpc.phase1_alpha, tau_max=tau_max)
            CPC, minassocs = phase1['parents'], phase1['minassocs']
            
            self.mmpc_parcorr_phase1_results['CPC'].update(CPC)
            self.mmpc_parcorr_phase1_results['minassocs'].update(minassocs)
            
            phase2 = self.mmpc.run_phase2(tau_max=tau_max)
            trimmed_CPC, pvalues = phase2['parents'], phase2['pvalues']
            
            self.mmpc_parcorr_phase2_results['trimmed_CPC'].update(trimmed_CPC)
            self.mmpc_parcorr_phase2_results['pvalues'].update(pvalues) 
            
        self.A_pred = np.zeros((nvars,nvars), dtype=int)
        
        for target in self.targets:
            trimmed_CPC  = self.mmpc_parcorr_phase2_results['trimmed_CPC'][target]
            pvalues = self.mmpc_parcorr_phase2_results['pvalues'][target]
            parents = [parent for parent in trimmed_CPC if pvalues[parent]<=beta]
            self.A_pred[target, parents] = 1
        
        return(self)
        
        
    def get_weighted_causes(self, *argv, **kwargs):
        """ 
          Not Implemented
        """
        pass
            
    
    def causalgraph_as_adjmatrix(self):
        """
        Returns causal graph as a adjacency matrix (using numpy matrix)
        (i, j) = 1 implies j is the parent of node i
        """
        
        return(self.A_pred)
        

    def causalgraph_as_networkx(self):
        """
        Returns causal graph as a networkx digraph
        edge (i, j) implies j is the parent of node i
        """
                
        G = nx.DiGraph()
        
        G.add_nodes_from(self.vars)
        
        for target in self.targets:
            for parent in self.targets:
                if self.A_pred[target, parent]==1:
                    G.add_edge(self.vars[parent], self.vars[target])
        
        return(G)  
        
        
    def causalgraph_as_graphviz(self):
        """
        Returns causal graph as a graphiviz digraph
        edge (i, j) implies j is the parent of node i
        """
                
        dot = Digraph()
        
        # adding label set as nodes
        for i in self.vars:
            dot.node(i)
        
        for target in self.targets:
            for parent in self.targets:
                if self.A_pred[target, parent]==1:
                    dot.edge(self.vars[parent], self.vars[target])
        
        return(dot) 
        
