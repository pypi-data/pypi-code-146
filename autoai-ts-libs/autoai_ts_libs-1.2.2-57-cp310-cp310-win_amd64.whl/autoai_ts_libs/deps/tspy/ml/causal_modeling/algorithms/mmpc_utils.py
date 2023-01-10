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
MMPC algorithm utility routines
"""

import itertools as it
import numpy as np

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.metaestimators import _BaseComposition

class mmpcBase(_BaseComposition, BaseEstimator, TransformerMixin):
    r"""MMPC-p causal discovery for time series datasets.

    MMPC-p is a 2-step causal discovery method for large-scale time series
    datasets. In the first step, possible causes are detected using conditional 
    independence tests. In the second step, the possible causes are further pruned
    to remove false positives.
    
    The implementation is based on [2], which extends [1] to time series data. 
    We briefly summarize the method here. 

    MMPC-p tries to recover the Directed Information Graph between time series 
    variables. The Directed Information Graph is a graphical representation 
    of causal structure between time series variables- a variable :math:`X` 
    has a causal effect on variable :math:`Y` if the edge :math:`X\rightarrow Y`
    exists in the graph. 
    
    The DI graph also captures conditional independence relationships between
    variables. The future of a variable :math:`Y` is conditionally independent of
    the past of non-parent variables, conditioned on the past of :math:`Y`
    and its parents.

    We can now use these conditional independencies to discover the presence
    (or absence) of edges in the graph. We can use any parametric or non parametric
    conditional independence tester to test for conditional independencies. For a
    possible parent :math:`X`, target :math:`Y`, and conditioning set :math:`Z`,
    let :math:`CI(X;Y|Z)` denote the p-value of a CI tester for the test
    :math:`X^{t-1} ~\perp~ Y^{t} | Z^{t-1}, Y^{t-1}`. A high p-value means
    that :math:`X` does not have a causal edge to :math:`Y`. 
    A low p-value means an edge between :math:`X` and :math:`Y` could exist.

    Say we have :math:`N` variables :math:`\{X_1, \cdots, X_N\}`with some 
    unknown DI graph connecting them. Without loss of generality, we can
    try to recover the incoming edges to :math:`X_1`, and then repeat 
    the same process for all variables in the graph.

    MMPC-p estimates causal links by a two-step procedure:

    1.  Phase 1: Estimate a candidate parent set, which is a superset of parents 
    of :math:`X_1`, with the iterative phase 1 algorithm, implemented as run_phase1.

    2.  Phase 2: Prune the candidate parent set to remove irrelevant variables.
    This is implemented as run_phase2.

    The main free parameters of MMPC-p (in addition to free parameters of the
    conditional independence test statistic) are the maximum time delay
    :math:`\tau_{\max}` (``tau_max``) and the significance threshold in 
    Phase 1 :math:`\alpha` (``phase1_alpha``). 
    The maximum time delay depends on the application and should be chosen according to the
    maximum causal time lag expected in the complex system. Only RCIT and CCIT testers
    can work with time lag > 1. ParCorr and RCOT must use time lag=1.
    :math:`\alpha` should not be seen as a
    significance test level in Phase 1, since the iterative
    hypothesis tests do not allow for a precise confidence level. :math:`\alpha`
    rather takes the role of a regularization parameter in model-selection
    techniques. The candidate set at the end of Phase 1 should
    include the true parents and at the same time be small in size to reduce the
    estimation dimension of Phase 2 and improve its power.

    References
    ----------
    [1] Tsamardinos, Ioannis, Laura E. Brown, and Constantin F. Aliferis. "The max-min hill-climbing Bayesian network structure learning algorithm." Machine learning 65.1 (2006): 31-78.
    [2] Pegueroles, Bernat Guillen, et al. "Structure Learning from Time Series with False Discovery Control." arXiv preprint arXiv:1805.09909 (2018).

    Examples
    --------
    >>> import numpy
    >>> from pcmci import PCMCI
    >>> from di_testers import ParCorr
    >>> import tigramite.data_processing as pp
    >>> numpy.random.seed(42)
    >>> # Example process to play around with
    >>> # Each key refers to a variable and the incoming links are supplied as a
    >>> # list of format [((driver, lag), coeff), ...]
    >>> links_coeffs = {0: [((0, -1), 0.8)],
                        1: [((1, -1), 0.8), ((0, -1), 0.5)],
                        2: [((2, -1), 0.8), ((1, -2), -0.6)]}
    >>> data, _ = pp.var_process(links_coeffs, T=1000)
    >>> # Data must be array of shape (time, variables)
    >>> print data.shape
    (1000, 3)
    >>> cond_ind_test = ParCorr()
    >>> mmpc = MMPC(cond_ind_test=cond_ind_test, selected_variables=[2], phase1_alpha=0.2, verbosity=1)
    >>> mmpc.fit(data)
    ##########################
    # Starting phase 1 of MMPC
    ##########################
    Parameters:
    selected_variables = [2]
    independence test = par_corr
    tau_max = 1
    phase1_alpha = 0.2
    ## Variable 2
    #candidate parents of variable X2 after Phase 1:
    variable: 0 minassoc=0.200000
    variable: 1 minassoc=0.200000
    ##########################
    # Starting phase 2 of MMPC
    ##########################
    ## Variable $X^2$
    p-value of no edge between X^0 --> X^2 : 0.001619
    p-value of no edge between X^1 --> X^2 : 0.000000


    Parameters
    ----------
    cond_ind_test : conditional independence test object
        This can be ParCorr or other classes from ``di_testers.py`` or an
        external test passed as a callable. This test can be based on the class
        di_testers.CondIndTest. If a callable is passed, it
        must have the signature::

            class CondIndTest():
                # with set_data function that initializes a TxN data nump array
                #measure attribute that names the test

                # and functions
                # * run_test(X, Y, Z, tau_max) : where X,Y,Z are 
                #  lists of indices and tau_max is the delay variable
                #   return (p-value)
                

    selected_variables : list of integers, optional (default: None)
        Specify to estimate parents only for selected variables. If None is
        passed, parents are estimated for all variables.

    verbosity : int, optional (default: 0)
        Verbose levels 0, 1, ...

    Attributes
    ----------

    iterations : dictionary
        Dictionary containing further information on algorithm steps.

    N : int
        Number of variables.

    T : int
        Time series sample length.


    pvalues_of_edges: dictionary
        Dictionary of the form {child: {parent: pval}} for child in selected_variables, and parent, pval are candidate parents with their respective corrected pvalues


    """
    def __init__(self,dataset,
                 cond_ind_test=None,
                 phase1_alpha = 0.2,
                 K = 2,
                 tau_max = 1,
                 subsample = 1.,
                 selected_variables=None,
                 selected_parents=None,
                 ground_truth=None,
                 verbosity=0,
                 seed=0):

        # Set the verbosity for debugging/logging messages
        self.verbosity = verbosity

        self.K = K
        self.tau_max = tau_max
        self.phase1_alpha = phase1_alpha
        self.selected_variables = selected_variables   
        self.selected_parents = selected_parents
        self.cond_ind_test = cond_ind_test
        self.ground_truth = ground_truth
        self.subsample = subsample
        self.seed = seed
        self._set_data(dataset)

    def _set_data(self,dataset):
        # Store the shape of the data in the T and N variables
        self.cond_ind_test.set_data(dataset)
        self.T, self.N = dataset.shape
        # Some checks
        if self.selected_variables is not None:
            if (np.any(np.array(self.selected_variables) < 0) or
               np.any(np.array(self.selected_variables) >= self.N)):
                raise ValueError("selected_variables must be within 0..N-1")
        else:
            self.selected_variables = np.arange(self.N,dtype=int)

        np.random.seed(self.seed)
        idx = np.arange(self.T - 2*self.tau_max)
        np.random.shuffle(idx)
        self.dataframe_idx = idx[:int(idx.shape[-1]*self.subsample)]
    def set_params(self, **kwargs):
        cond_ind_test_params = {}
        valid_params = self.get_params(deep=True)

        for d_item in kwargs:
            if 'cond_ind_test__' in d_item:
                cond_ind_test_params[d_item.split('cond_ind_test__')[1]] = kwargs[d_item]
            else:
                key = d_item.split('__')[-1]
                value = kwargs[d_item]
                if key not in valid_params:
                    raise ValueError('Invalid parameter %s for estimator %s. '
                                'Check the list of available parameters '
                                 'with `estimator.get_params().keys()`.' %
                                 (key, self))
                setattr(self, key, value)
                valid_params[key] = value
        self.cond_ind_test.set_params(**cond_ind_test_params)
        return self
    def _run_phase1_single(self, j,
                              phase1_alpha,
                              tau_max=1,
                              ):
        if self.selected_parents is None:
            nodes = [node for node in range(self.N) if node!=j]
        else:
            nodes = self.selected_parents
        
        # Iteration through increasing number of conditions, i.e. from 
        # [0,max_conds_dim] inclusive
        converged = False
        CPC = []
        self.last_node_added = None
        self._minassocs = dict([(n, phase1_alpha) for n in nodes]) 
        while not converged:
            converged = True
            max_assoc = 0
            max_node = None
            candidate_list = [node for node in nodes if node not in CPC]
            for x in candidate_list:
                auxassoc = self._minassoc(x, j, CPC, phase1_alpha, tau_max)
                self._minassocs[x] = auxassoc 
                if auxassoc > max_assoc:
                    max_assoc = auxassoc
                    max_node = x
                #print("max_node {} max_assoc {}".format(max_node, max_assoc))
            if (max_assoc > 0) & (max_node != None):
                CPC.append(max_node)
                self.last_node_added = max_node
                if self.verbosity > 1:
                    print("Node X%d added to candidate parents of X%d"% (max_node,j) )
                converged = False
        return {'parents':CPC, 'minassocs': self._minassocs.copy()}
    
    def _pval(self, parent, target, cond, tau_max):
        # Y = [(target,0)] 
        # X = [(parent,i) for i in range(-1*tau_max,0)] 
        # Z = [(c,i) for c,i in it.product(cond, range(-1*tau_max,0))]
        # Z = Z + [(target,i) for i in range(-1*tau_max,0)]

        try:
            pval = self.cond_ind_test.run_test(parent, target, cond, tau_max)
        except Exception as e:
            print('exception found: {}. skipping test.'.format(e))
            pval = 1.0
        return pval

    def _assoc(self, parent, target, cond, alpha, tau_max):
        pval = self._pval(parent, target, cond, tau_max)
        return alpha - min(pval,alpha)#max(pval,alpha) - alpha

    def _minassoc(self, var, target, locCPC, alpha, tau_max):
        #If the conditioning set is null, handle separately
        if(len(locCPC)==0):
            min_assoc=self._assoc(var,target,[],alpha,tau_max)
            if self.verbosity > 1:
                print("\t\t link X{} --> X{} , S: [], assoc: {}".format(var, target, min_assoc))
            return min_assoc
        
        min_assoc = min(alpha, self._minassocs[var]) 

        #If the conditioning set is non null    
        # test on sets by removing at most K elements at a time
        # from locCPC. 
        # if locCPC is smaller than K, then search over all subsets
        min_size = max(-1, len(locCPC)-self.K-1)
        for i in range(len(locCPC),min_size,-1):
            if min_assoc == 0.:
                return min_assoc
            for S in it.combinations(locCPC, i):
                if self.last_node_added in S:
                    auxassoc = self._assoc(var,target, list(S), alpha, tau_max)
                    if self.verbosity > 1:
                        print("\t\t link X{} --> X{} , S: {}, assoc: {}".format(var, target, list(S), auxassoc))

                    if auxassoc < min_assoc:
                        min_assoc = auxassoc
        return min_assoc

    def run_phase1(self,
                      phase1_alpha,
                      tau_max=1,
                      ):

        #self._set_data(dataset)
       
        # Print information about the selected parameters
        if self.verbosity > 0:
            print('##########################')
            print('# Starting phase 1 of MMPC')
            print('##########################')
            print("\n\nParameters:")
            if len(self.selected_variables) < self.N:
                print("selected_variables = %s" % self.selected_variables)
            print("independence test = %s" % self.cond_ind_test.measure
                  + "\ntau_max = %d" % tau_max
                  + "\nphase1_alpha = %s" % phase1_alpha)
            print("\n")

        
        # Initialize all parents
        self.CPC = dict()
        self.minassocs = dict([(n, dict()) for n in self.selected_variables])
        # Loop through the selected variables
        for j in self.selected_variables:
            # Print the status of this variable
            if self.verbosity > 0:
                print("\n## Variable %s" % j)
            results = \
                self._run_phase1_single(j,
                                           tau_max=tau_max,
                                           phase1_alpha=phase1_alpha)
            # Record the results for this variable
            self.CPC[j] = results['parents']
            self.minassocs[j] = results['minassocs']
            if self.verbosity > 0:
                print("#candidate parents of variable X%d after Phase 1:"%j)
                for parent in self.CPC[j]:
                    print("variable: %d minassoc=%f"%(parent,self.minassocs[j][parent]))
                print()
        # Return the parents
        return {'parents': self.CPC.copy(), 'minassocs': self.minassocs.copy()}

    def run_phase2(self,
                tau_max=1):
        self.pvalues_of_edges = dict()
        self.trimmed_CPC = dict()

        if self.verbosity > 0:
            print('##########################')
            print('# Starting phase 2 of MMPC')
            print('##########################')
        for j in self.selected_variables:
            if self.verbosity > 0:
                print('## Variable $X^%d$'%j) 
            CPC = self.CPC[j].copy()
            self.trimmed_CPC[j], self.pvalues_of_edges[j] = self._run_phase2_single(j, CPC, tau_max) 
       
            if self.verbosity > 0:
                for parent in self.trimmed_CPC[j]:
                    print("p-value of no edge between X^%d --> X^%d : %f"%(parent,j,self.pvalues_of_edges[j][parent]))

        return {'parents': self.trimmed_CPC.copy(), 'pvalues': self.pvalues_of_edges.copy()} 
    
    def _run_phase2_single(self, j, CPC, tau_max):
        n_candidates = len(CPC)
        curr_candidate = 0
        pvalues_of_edges = dict([(n,0.) for n in CPC])  
        while curr_candidate < n_candidates:
            var = CPC.pop(0)
            pvalues_of_edges[var] = self._maxpval(var, j, CPC, tau_max)
            if pvalues_of_edges[var] == 1:
                pvalues_of_edges.pop(var, None)
            else:
                CPC.append(var)
            curr_candidate += 1
        return CPC, pvalues_of_edges

    def _maxpval(self, parent, target, CPC, tau_max):
        if (len(CPC) == 0):
            pval =self._pval(parent, target,[], tau_max) 
            if self.verbosity > 1:
                print("\t\t no link X{} --> X{} , S: [], pval: {}".format(parent, target, pval))
            return pval 
        # print("Entering min assoc non-trivially")
        # We don't need to check c!=var because var is in [c for c in cols if c not in CPC]
        max_pval = 0. 
        for i in range(len(CPC),-1,-1):
            if max_pval == 1.:
                if self.verbosity > 0:
                    print("\t\t no link X{} --> X{} , S: {}, pval: {}".format(parent, target, list(S), max_pval))
                return max_pval
            for S in it.combinations(CPC, i):
                if i == 0 :
                    auxpval = self._pval(parent, target, [], tau_max)
                else:
                    auxpval = self._pval(parent, target, S, tau_max)

                if self.verbosity > 1:
                    print("\t\t no link X{} --> X{} , S: {}, pval: {}".format(parent, target, list(S), auxpval))
                if auxpval > max_pval:
                    max_pval = auxpval
        return max_pval

    def fit(self, dataset, Y=None): 

        results_phase1 = self.run_phase1(tau_max=self.tau_max,
                                         phase1_alpha=self.phase1_alpha)
        results_phase2 = self.run_phase2( tau_max=self.tau_max)
                       
        # Return the dictionary
        return self
    
    def predict(self, X=None):
        if self.pvalues_of_edges is not None:
            pass
        else:
            if X is None:
                raise Exception("please provide data")
            self.fit(X)
        return self.pvalues_of_edges
            
    
