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

'''
SRU algorithm implementation and interface classes
'''

import numpy as np
import pandas as pd
import os

import torch

import autoai_ts_libs.deps.tspy
from autoai_ts_libs.deps.tspy.multi_time_series import multi_time_series
from autoai_ts_libs.deps.tspy.time_series import time_series
from autoai_ts_libs.deps.tspy.ml.causal_modeling.algorithms.datamodel import tes
from autoai_ts_libs.deps.tspy.ml.causal_modeling.algorithms.estimators import CausalityEstimator

import autoai_ts_libs.deps.tspy.ml.causal_modeling.models.srunet as srunet
from autoai_ts_libs.deps.tspy.ml.causal_modeling.models.srunet import SRUNet, train_SRUNet



class SRUInputDatatypeAdapter:
    @staticmethod
    def from_array(data, labels, labels_kind):
        
        if labels_kind == 'product':
            assert len(labels) == 2
            
            num_nodes            = len(labels[0])
            num_features         = len(labels[1])
            num_total_samples, n = data.shape
            assert n == num_nodes * num_features
            
            multi_index = pd.MultiIndex.from_product(labels,
                                                     names=["nodes", "features"])
            
            time_points = list(range(0, num_total_samples))
            
            df = pd.DataFrame(data,
                              index=time_points, 
                              columns=multi_index)
            
        elif labels_kind == 'tuples':
            assert all(map(lambda x: x == 2, [len(item) for item in labels]))
            multi_index = pd.MultiIndex.from_tuples(labels,
                                                      names=["nodes", "features"])
            num_total_samples, n = data.shape
            
            assert len(labels) == n
            time_points = list(range(0, num_total_samples))
            
            df = pd.DataFrame(data, 
                              index=time_points, 
                              columns=multi_index)
        
        elif labels_kind == 'arrays':
            assert len(labels) == 2
            assert len(labels[0]) == len(labels[1])
            
            multi_index = pd.MultiIndex.from_arrays(labels,
                                                      names=["nodes", "features"])
            num_total_samples, n = data.shape
            time_points = list(range(0, num_total_samples))
            df = pd.DataFrame(data, 
                              index=time_points, 
                              columns=multi_index)
        
        elif labels_kind == 'single_feature':
            feature_name = 'feature_1'
            
            num_total_samples, n = data.shape
            assert len(labels) == n
            
            multi_index = pd.MultiIndex.from_product([labels, [feature_name]],
                                                names=["nodes", "features"])
            time_points = list(range(0, num_total_samples))
            df = pd.DataFrame(data, 
                              index=time_points, 
                              columns=multi_index)
            
        elif labels_kind == 'sizes':
            num_total_samples, n = data.shape
            assert n == sum(labels)
            tuple_labels = []
            for node_idx, num_features in enumerate(labels):
                for feature_idx in range(num_features):
                    tuple_label = ('node_%d' % (node_idx + 1,), 
                                   'feature_%d' % (feature_idx + 1,))
                    tuple_labels.append(tuple_label)
            df = SRUInputDatatypeAdapter.from_array(data, tuple_labels, 
                                                      labels_kind='tuples')  
        return df
    
    
    def from_dataframe(data, labels=None, labels_kind=None):
        columns = data.columns
        data_array  = data.to_numpy()
        num_total_samples, n = data_array.shape
        if isinstance(columns, pd.core.indexes.multi.MultiIndex):
            df = data.copy()
            df.columns.set_names(['nodes', 'features'], inplace=True)            
        else:
            node_labels    = columns.to_numpy().tolist()
            feature_labels = ['feature_1']
            multi_index = pd.MultiIndex.from_product([node_labels, feature_labels],
                                                     names=["nodes", "features"])
            df = data.copy()
            df.columns = multi_index
        
        return df
    
    @staticmethod
    def from_data(data, labels, labels_kind):
        
        if isinstance(data, pd.DataFrame):
            df = SRUInputDatatypeAdapter.from_dataframe(data)
        
        elif isinstance(data, np.ndarray):
            df = SRUInputDatatypeAdapter.from_array(data, labels, labels_kind)
            
        return df


    
class SRU(CausalityEstimator):
    '''
    
    **Note:** *Please refer to `autoai_ts_libs.deps.tspy/ml/causal_modeling/examples/sru` for detailed descriptions and usage of `SRU` class methods in convenient notebook format.*

    References:
    [1] Oliva, Junier B., BarnabÃ¡s PÃ³czos, and Jeff Schneider. "The statistical recurrent unit." 
    International Conference on Machine Learning. PMLR, 2017.

    [2] Khanna, Saurabh, and Vincent YF Tan. "Economy Statistical Recurrent Units For Inferring Nonlinear Granger Causality." 
    International Conference on Learning Representations. 2019.
    
    [3] Neal Parikh and Stephen Boyd. "Proximal algorithms." 
    Foundations and Trends in optimization 1, no. 3 (2014): 127-239.
        
    [4] https://github.com/sakhanna/SRU_for_GCI/blob/master/models/sru.py

    The idea of the Statistical Recurrent Unit (SRU) was introduced in [1].
    SRUs were leveraged specifically for Granger causality computations in [2].

    In this effort, we follow [2] and internally we base our developments on one of its models, namely their code in [4].
    In our implementation of the underlying model as `models/srunet.py` we support richer representations of individual events in a timeseries:
    Such an event in the present code can be represented as a vector of arbitrary dimensions `num_features`, 
    rather than a scalar which is the case for [2,4].
    
    
    Individual/minimal input for SRU model `x(t)`:
    A vector which is the concatenation of the representations of events at time `t` from all timeseries.
    
    Individual/minimal output `x[i](t+1)` (from the model for timeseries `i`):
    A vector which is the representation of the next event (at time point `t+1`), for timeseries `i`.
    Similarly for all timeseries.

    Operations summary:
    
    1. `u[i](t-1)`              => `r[i](t)`
    2. `(x(t), r[i](t))`        => `phi[i](t)`
    3. `(u[i](t-1), phi[i](t))` => `u[i](t)`     
    4. `u[i](t)`                => `o[i](t)`
    5. `o[i](t)`                => `x[i](t+1)` prediction

    For the semantics of `u`, `r`, `phi`, `o` vectors please see below.
    
    Anatomy of the model for timeseries/node/variable `i`:
    
    - There are 4 single NN layers (ReLU + Linear) in each model (for operations 1., 2., 4., 5.) and we learn the 
      weight parameters (weight matrix and bias vector) in their Linear parts.
    - Weight matrices in the models are the most useful artifacts that are leveraged in the results. More specifically:
    - The weight matrix from `u[i](t-1)` to `r[i](t)` in operation 1:  `W[r]`
    - The weight matrix from `x(t)` to `phi[i](t)`    in operation 2:  `W[in]`
    - The weight matrix from `r[i](t)` to `phi[i](t)` in operation 2:  `W[f]`
    - The weight matrix from `u[i](t)` to `o[i](t)`   in operation 4:  `W[o]`
    - The weight matrix from module import symbol `o[i](t)` to `x[i](t+1)` in operation 5:  `W[y]`

    Parameters
    ----------
    num_nodes : int
        The number of timeseries of events. This is also referred as the number of variables or nodes in the literature. 
        An `SRU` estimator object will internally host `num_nodes` models after training: one model per timeseries.

    num_features : int
        The number of elements in the vector representation of each timeseries event at any timepoint `t`.
        The internal trained model for timeseries `i` at time point `t` is expecting a vector `x(t)` as input to produce a
        prediction for the representation of the next event (at time point `t+1`), for this timeseries, `x[i](t+1)`, as output.
        Input vector `x(t)` is the concatenation of the representations of events at time `t` from all timeseries, so it has 
        `num_nodes * num_features` elements. Output vector `x[i](t+1)` has `num_features` elements.

    dim_stats : int
        The number of elements (dimension) for each of the intermediate, statistics-related vectors produced internally by the model
        for any timeseries `i`. `dim_stats` is used if the dimension of a specific statistics-related vector is not explicitly passed
        as a separate argument. These statistics-related vectors are:

        - feedback vector `r[i](t)`, which mixes multiscale summary statistics from previous time point
        - recurrent statistics vector `phi[i](t)` which mixes input `x(t)` and the feedback vector `r[i](t-1)`
        - vector of nonlinear causal features `o[i](t)`, which nonlinearly transforms current multiscale summary statistics vector `u[i](t)`
        - multiscale summary statistics vector `u[i](t)`.

        The default is 20.

    A : list of float
        The list of weights for linearly combining statistics from multiple time scales.
        Time scale `j`, for a particular timeseries `i` at time point `t` is represented by a vector `u[i][j](t)`.
        Concatenating those vectors from all time scales ("subvectors") we get the multiscale summary statistics vector `u[i](t)`.
        The default is [0.0, 0.01, 0.05, 0.1, 0.99].

    dim_iid_stats : int
        The dimension of recurrent statistics vector `phi[i](t)`.
        The default is None.

    dim_rec_stats : int 
        The dimension of multiscale summary statistics vector.
        The default is None.

    dim_final_stats : int
        The dimension of the vector of nonlinear causal features `o[i](t)`.
        The default is None. 

    dim_rec_stats_feedback : int
        The dimension of feedback vector `r[i](t)`.
        The default is None.

    mu1 : float
       mu1 is the regularization term corresponding to lambda_1 as in the following note:
       There is an *entrywise l1* regularization term involing all other learnable weight matrices and bias vectors. 
       Again, this term is *not smooth* and its proximal operator is "elementwise soft-thresholding"; it has a regularization parameter `lambda_1`. 
       It can be implemented by applying `torch.nn.SoftShrink(lambda_1 * learning_rate)` on all entries of the weight matrices and bias vectors 
       (on top of the update the smooth loss term has effected): 
       Shift the entry closer to 0 by lambda_1 * learning rate; zero it if its distance from zero is less than the shift. 
       Please see 6.7.1 and 6.5.2 in [3].
       The default is 0.0 (no regularization).

    mu2 : float
        mu2 is the regularization term coresponding to lambda_l2 as in the following note:
        There is a an l1-l2 regularization term involving `W[in]`: assuming num_features=1 this basically says that `l2_norm` 
        is applied to the columns of `W[in]` and then these norms are added together: the latter step essentially is equivalent to 
        taking the `l1_norm` of the vector of `l2_norms`).
        This term, which is *not smooth*, has a regularization parameter `lambda_12` so `W[in]` has to be newly updated, 
        on top of its update due to the `loss_term` optimization step using the *proximal gradient descent*: 
        Columns `w` of current `W[in]` for the case `l2_norm < lambda_12 * learning_rate` are zeroed (multiplied by zero); 
        otherwise their are scaled by the factor `(l2_norm - lambda_12 * learning_rate) / l2_norm < 1`. 
        Note that:

        - `torch.nn.SoftShrink(lambda_12 * learning_rate)` applied to the `l2_norm` of a column `w` and then divided by 
          `l2_norm`, will serve as the multiplication factor for `w` in both cases.
        - `torch.clamp(l2_norm, small_value)` "protects" from particularly small `l2_norms` in the division 
          (setting a lower bound for the norm) and can be used in place of `l2_norm divisor`.

        This implements the *group-wise soft-thresholding operator* (as used in proximal gradient descent): *"blockwise soft-thresholding"*.
        Please see 6.5.4 in [3].
        The default is 0.0 (no regularization).

    batch_size : int
        batch size
        A *batch* consists of batch_size successive in time input vectors: `x(t[1]), x(t[2]),..., x(t[batch_size])`,
        with `t[1] <= t[2] <=... <=t[batch_size]`, or `next(t[k]) = t[k+1])`. 
        Note that we do not have explicitly `t[1]=t, t[2]=t+1, ... t[batch_size]=t+batch_size-1` but *time is definitely ordered*.
        We'll use the same notation for convenience where "t+1" will mean "next(t)", the time of the event after that happening at time `t`.
        The default is 50.

    block_size : int
        block size
        In practice we do use a subset of consecutive vectors in a batch, called a *block*, with `block_size <= batch_size`. 
        For different iterations, when it comes to a particular batch, we can start from a random index in the batch and 
        take the next `block_size` entries for training.
        The default is 20.

    max_iters : int
        The number of iterations during training.
        Each iteration processes events from `batch_size` successive time points.
        The default is 1000.

    learning_rate : float
        Learning rate for the Adam optimizer used.
        Please refer to more details for Adam in https://arxiv.org/abs/1412.6980 .
        The default is 0.001.

    learning_rate_gamma : float
        Multiplicative factor of learning rate decay.
        Please refer to the documentation of `gamma` as in 
        https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.StepLR.html for more details.
        The default is 0.99.

    learning_rate_update_gap : int
        Period of learning rate decay.
        Please refer to the documentation of `step_size` as in 
        https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.StepLR.html for more details.
        The default is 4.

    staggering_train_window : int
        Flag deciding the strategy for computing the offset of effective training points (`block_size` in number) 
        within a batch (`batch_size` such successive points in number). If `staggering_train_window` is 0 then the first
        `block_size` points in the batch are effectively used (offset=0). For nonzero choices, a randomly computed offset into the batch
        is first computed and then the `block_size` elements starting at this offset index in the batch are used. 
        The default is 1.

    stopping_threshold : float
        Threshold in the loss function: 10 successive iterations with loss less than 
        `stopping_threshold` will result in exiting the training iteration loop.
        The default is 1e-5.

    train_verbosity_level : int
        Verbosity level during training; if set to 0, no messages are emitted.
        The default is 0.


    All the above parameters become attributes of the trained SRU model.
    A trained SRU model object (i.e. after its `fit()` method is invoked) has the following as additional attributes:   

    Attributes
    ----------

    n_inp_channels : int
        The number of input channels for each of internal timeseries models hosted in a trained SRU model object.
        This is equal to `num_nodes * num_features`.

    n_out_channels : int
        The number of output channels for each of internal timeseries models hosted in a trained SRU model object.
        This is equal to `num_features`.

    nodename_list : list of string
        The list of names of the nodes (timeseries/variables) used in training.

    weight_dict : dictionary of numpy arrays
        The keys of the dictionary are the names of the nodes.
        The value for a key is the numpy array containing the learnt weights from tensor W[in] in the trained model
        for the corresponding node.  

    loss_pairs_dict : dictionary of pytorch tensors
        The keys of the dictionary are the names of the nodes.
        The value for a key is a tensor of shape `max_iters x 2` containing 
        smooth loss and regularization loss scalar value pairs.

    model_state_dict_dict : dictionary of model state dictionaries
        The keys of the dictionary are the names of the nodes. 
        The value for a key is the state dictionary of the trained model for the corresponding node.
        This state dictionary is the result of calling method `state_dict()` on the trained pytorch model.

    hidden_state_dict : dictionary of pytorch tensors
        The keys of the dictionary are the names of the nodes.
        The value for a key is the tensor containing the last multiscale summary statistics vector
        produced during training.

    model_dict : dictionary of models
        The keys of the dictionary are the names of the nodes. 
        The value for a key is the trained pytorch model.

    
    '''

    def __init__(self, 
                num_nodes,                
                num_features,             
                                         
                dim_stats                 = 20,
                                          
                A                         = [0.0, 0.01, 0.05, 0.1, 0.99],
                                          
                dim_iid_stats             = None,
                dim_rec_stats             = None,
                dim_final_stats           = None,
                dim_rec_stats_feedback    = None,
                                         
                mu1                       = 0.0,
                mu2                       = 0.0,
                batch_size                = 50,
                block_size                = 20,
                max_iters                 = 1000,
                                         
                learning_rate             = 0.001,
                learning_rate_gamma       = 0.99,
                learning_rate_update_gap  = 4,
                staggering_train_window   = 1,
                stopping_threshold        = 1e-5,
                train_verbosity_level     = 0
    ):
        
        
        self.num_nodes    = num_nodes
        self.num_features = num_features
        
        n_inp_channels              = num_nodes * num_features
        n_out_channels              = num_features
        
        self.n_inp_channels         = n_inp_channels
        self.n_out_channels         = n_out_channels

        self.dim_stats              = dim_stats
        
        self.A                      = A
        self.dim_iid_stats          = dim_stats if dim_iid_stats == None else dim_iid_stats
        self.dim_rec_stats          = dim_stats if dim_rec_stats == None else dim_rec_stats
        self.dim_final_stats        = dim_stats if dim_final_stats == None else dim_final_stats
        self.dim_rec_stats_feedback = dim_stats if dim_rec_stats_feedback == None else dim_rec_stats_feedback

        self.mu1                      = mu1
        self.mu2                      = mu2
        self.batch_size               = batch_size
        self.block_size               = block_size
        self.max_iters                = max_iters

        self.learning_rate            = learning_rate
        self.learning_rate_gamma      = learning_rate_gamma
        self.learning_rate_update_gap = learning_rate_update_gap
        self.staggering_train_window  = staggering_train_window
        self.stopping_threshold       = stopping_threshold
        self.train_verbosity_level    = train_verbosity_level
        

        self.nodename_list = None

    
    def fit(self,
            data,
            labels=None,
            labels_kind=None):

        '''
        Computes causal relations between timeseries using data in either

        1. Pandas dataframe
        2. Numpy array

        Parameters
        ----------
        data:
            type `pandas.DataFrame` or `numpy.ndarray`

            * :class:`~pandas.DataFrame`
            * :class:`~numpy.ndarray`

        labels : list of label specifications or None
            Depending on the `label_kind`, `labels` can be:
            - a list of two label sequences if `labels_kind == 'product'`
            - a list of pair tuples if `labels_kind == 'tuples'`
            - a list of two arrays if `labels_kind == 'arrays'`
            - a list of labels if `labels_kind == 'single_feature'`
            - a list of sizes if `labels_kind == 'sizes'` 
            - None if `labels_kind == None`
            Note that `labels` and `labels_kind` can be None only when data type is `pandas.DataFrame`. 
            In this case the (node, feature) pair tuple of labels for each sequence of scalar values
            is either extracted from the `MultiIndex` index structures of the dataframe, or if usch a structure is not present
            the assumption is that there is one feature per node (named `feature_1') and the Index structure contains the names 
            of the nodes.
            The default is None.

        labels_kind : string
            Specification on how to produce (node, feature) pair tuple of labels for each sequence of scalar values in `data`.
            If `labels_kind` is not `None` then data is expected to be a numpy array with each of its successive columns corresponding
            to a sequence of scalar value for successive (node, feature) pair tuples of labels. As examples:
            - if `labels_kind == 'product'`, then for `labels` containing a sequence of node names `N = ['n1', 'n2']` and a sequence of 
              feature names `F = ['f1', 'f2']` the list of succesive (node, feature) pair tuples of labels will be the cartesian product
              N x F: [('n1', 'f1'), ('n1', 'f2'), ('n2', 'f1'), ('n2', 'f2')].
            - if `labels_kind == 'tuples'` then `labels` will be the successive (node, feature) pair tuples of labels; 
              for the previous example: `labels = [('n1', 'f1'), ('n1', 'f2'), ('n2', 'f1'), ('n2', 'f2')`
            - if `labels_kind == arrays` then for the previous example:
              `labels = array([['n1', 'n1', 'n2', 'n2'], ['f1', 'f2', 'f1', 'f2']])`
            - if `labels_kind == 'single_feature'` and `labels` is the list of nodes [`n1`, `n2`], then the 
              successive (node, feature) pair tuples of labels for the (two) columns of the data array will be:
              `[('n1', 'feature_1'), ('n2', 'feature_1')]`.
            - if `labels_kind == sizes` and labels is the list of sizes [2, 2] (these are the numbers of features for each node and they are equal)
              then the successive (node, feature) pair tuples of labels for the (four) columns of the data array will be:
              `[('node_1', 'feature_1'), ('node_1', 'feature_2'), ('node_2', 'feature_1'), ('node_2', 'feature_2']`.
            Note if `labels_kind` is None then this implies that `labels` is None and that a dataframe has been provided as `data`.
            Then the (node, feature) pair tuples of labels are constructed as noted in `labels` documentation.
            The default is None.

        Returns
        -------
        self : object
            Fitted SRU estimator.
        '''
        
        dataframe = SRUInputDatatypeAdapter.from_data(data, labels, labels_kind)
        
        ### Checking code
        nodename_list = []
        feature_dict  = {}
        current_nodename = None
        nodename_count   = 0
        
        dataframe_labels = dataframe.columns.tolist()
        for nodename, feature in dataframe_labels:
            if current_nodename != nodename:
                current_nodename = nodename
                nodename_count +=1
            if nodename not in set(nodename_list):
                nodename_list.append(nodename)
        assert nodename_count ==  len(nodename_list)

        feature_dict        = {nodename : [] for nodename in nodename_list}
        for nodename, feature in dataframe_labels:
            feature_dict[nodename].append(feature)
        feature_lists = list(map(tuple, list(feature_dict.values())))
        assert len(set(feature_lists)) ==  1
        ###
        
        self.nodename_list = nodename_list
        tensor     = torch.from_numpy(dataframe.to_numpy())
        train_data = tensor.T
        
        
        # training pararameters that could also be pushed to the supplied argument list;
        # however perhaps less frequent to change
        learning_rate            = self.learning_rate
        learning_rate_gamma      = self.learning_rate_gamma
        learning_rate_update_gap = self.learning_rate_update_gap
        staggering_train_window  = self.staggering_train_window
        stopping_threshold       = self.stopping_threshold
        train_verbosity_level    = self.train_verbosity_level

        batch_size = self.batch_size
        block_size = self.block_size
        max_iters  = self.max_iters
        mu1        = self.mu1
        mu2        = self.mu2
        
    
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')        

        some_nodename = nodename_list[0]
        some_features = feature_dict[some_nodename]
        
        data_num_nodenames         = len(nodename_list)
        data_num_features          = len(some_features)
        data_num_nodename_features = data_num_nodenames * data_num_features
        
        # the number of all features from all nodes/services combined is
        # equal to the input vector size (n_inp_channels)
        assert self.n_inp_channels == data_num_nodename_features
        num_nodename_features = self.n_inp_channels
        
        # the number of features per service is equal to the
        # output vector size (n_out_channels)
        assert self.n_out_channels == data_num_features
        num_features = self.n_out_channels

        num_total_samples = train_data.shape[1]
        num_batches       = int(num_total_samples / batch_size)

        ############################################################
        # train model in the models
        ############################################################
        weight_dict           = {}
        loss_pairs_dict       = {}
        model_state_dict_dict = {}
        hidden_state_dict     = {}
        for predicted_nodeidx, predicted_nodename in enumerate(nodename_list):
            model = srunet.SRUNet(self.n_inp_channels,
                                  self.n_out_channels,
                                  self.dim_iid_stats,
                                  self.dim_rec_stats,
                                  self.dim_rec_stats_feedback,
                                  self.dim_final_stats,
                                  self.A,
                                  device)

            model = model.to(device)
            
            model, loss_pairs = srunet.train_SRUNet(model,
                                                    train_data,
                                                    device,
                                                    num_batches,
                                                    batch_size,
                                                    block_size,
                                                    predicted_nodeidx,
                                                    num_features,
                                                    max_iters,
                                                    mu1,
                                                    mu2,
                                                    learning_rate,
                                                    learning_rate_gamma,
                                                    learning_rate_update_gap,
                                                    staggering_train_window,
                                                    stopping_threshold,
                                                    train_verbosity_level)
            
            weight_dict[predicted_nodename]     = model.lin_xr2phi.weight[:, :num_nodename_features].detach().clone().numpy()
            loss_pairs_dict[predicted_nodename] = loss_pairs
            
            model_state_dict_dict[predicted_nodename] = model.state_dict()

            # model hidden state
            hidden_state_dict[predicted_nodename]     = model.u_t_prev.clone()
            
        self.device = device
        
        self.weight_dict           = weight_dict
        self.loss_pairs_dict       = loss_pairs_dict
        self.model_state_dict_dict = model_state_dict_dict
        self.hidden_state_dict     = hidden_state_dict

        return self
        

    def save_models(self, trained_model_dir):
        '''
        Saves the trained pytorch models in SRU object under a directory.

        Parameters
        ----------
        trained_model_dir : string
            The directory under which the trained pytorch models are saved;
            one model per node/timeseries/variable.
        '''
        
        if not os.path.exists(trained_model_dir):
            os.makedirs(trained_model_dir)
        for predicted_nodeidx, predicted_nodename in enumerate(self.nodename_list):
            trained_model_fpath = os.path.join(trained_model_dir, 'model_{}.pickle'.format(predicted_nodename))
            model_data = {'state_dict'   : self.model_state_dict_dict[predicted_nodename],
                          'hidden_state' : self.hidden_state_dict[predicted_nodename]}
            torch.save(model_data, trained_model_fpath)
        

    def load_models(self, trained_model_dir):
        '''
        Loads trained pytorch models.

        Parameters
        ----------
        trained_model_dir : string
            The directory under which the trained pytorch models are located;
            one model per node/timeseries/variable.
        '''
                
        model_dict        = {}
        hidden_state_dict = {}

        for predicted_nodeidx, predicted_nodename in enumerate(self.nodename_list):
            trained_model_fpath = os.path.join(trained_model_dir, 'model_{}.pickle'.format(predicted_nodename))
    
            model = SRUNet(self.n_inp_channels,
                          self.n_out_channels,
                          self.dim_iid_stats,
                          self.dim_rec_stats,
                          self.dim_rec_stats_feedback,
                          self.dim_final_stats,
                          self.A,
                          self.device);
            model_data = torch.load(trained_model_fpath);

            state_dict   = model_data['state_dict']
            model.load_state_dict(state_dict)
            model.eval();
            model_dict[predicted_nodename] = model

            # model hidden state
            hidden_state                          = model_data['hidden_state']
            hidden_state_dict[predicted_nodename] = hidden_state
               
        self.model_dict        = model_dict
        self.hidden_state_dict = hidden_state_dict


    def compute_prediction_deviations(self, test_data, concurrent_lists=None, hidden_state='keep'):
        '''
        Computes a list of "prediction deviations" which are defined as means of norms of differences between predicted and actual vector 
        representations of events contained in a test dataset. The list contains one entry per time point; the mean is over the norms 
        of differences of event representations for events occuring in nodes/timeseries/variables selected.
        
        Parameters
        ----------
        test_data : pytorch tensor
            This is  tensor of shape `(num_time_points) x (num_nodes * num_features)` containing the vector representations of successive
            time points in the test dataset for all nodes. The ordering of scalar values in any single column of the tensor 
            (i.e. a particular timepoint) is assumed that aligns with the ordering of successive (node, feature) pair tuples of labels in the
            training data.
        
        concurrent_lists : list of list of string
            The list of node name lists which are assumed concurrently active at consecutive time points.
            If None all node names are assumed active at each time point.
            The default is None.
    
        
        hidden_state : string
            Strategy for managing the hidden state, which is the multiscale summary statistics vector to use, 
            prior to applying the trained model for prediction. Three strategies are available: 
            1. `keep`; do not reset the hidden state
            2. `zero`; reset the hidden state to zeros prior to applying the model
            3. `model`; reset the hidden state to the value it had attained at the end of training. 
            To allow for the third option we additionaly save the last multiscale summary statistics vector produced during training, 
            as part of the "standard" model weight parameters.
            The default is 'keep'.
        '''
        
        service_to_idx = {service : idx for idx, service in enumerate(self.nodename_list)}
        num_features   = self.n_out_channels

        services       = self.nodename_list
        
        # means of prediction errors for test data entries
        diff_norm_mean_list = []

        num_points     = test_data.shape[0]
        # diff_norm_dict = {service : [None for _ in range(num_points)] for service in services}

        for i in range(test_data.shape[0] - 1):
            diff_norm_list = []
            if concurrent_lists is None:
                current_services = services
            else:
                current_services = concurrent_lists[i]   
            
            for service in current_services:

                # get what is the "next" feature vector for the service
                idx = service_to_idx[service]
                start_idx = idx * num_features
                end_idx   = start_idx + num_features
                next_vector = test_data[i + 1, :][start_idx:end_idx].numpy()

                # use the separately trained model for the service...
                model              = self.model_dict[service]

                # allow for explicitly selecting the hidden state prior forward() invocation
                model_hidden_state = self.hidden_state_dict[service]
                if hidden_state == 'model':
                    model.u_t_prev = model_hidden_state.clone()
                elif hidden_state == 'zero':
                    model.u_t_prev = torch.zeros_like(model_hidden_state)
        
                model.eval();
                # model.train();

                # ...to get the "predicted next" feature vector for this service
                # TODO: could look also to predictions for other services "concurrently" happenning "next"
                next_predicted_vector = model.forward(test_data[i, :]).detach().clone().numpy().ravel()

                # how far apart is the predicted feature vector for the service from what is actually
                # the next feature vector for the service (based on the model for the service)
                diff_norm = np.linalg.norm(next_vector - next_predicted_vector)
                diff_norm_list.append(diff_norm)
                
            # accumulate the means of the prediction errors
            diff_norm_mean = np.mean(diff_norm_list)
            diff_norm_mean_list.append(diff_norm_mean)

        prediction_deviations = diff_norm_mean_list
        return prediction_deviations
    
    
    
    def compute_weighted_graph(self): 
        '''
        This function can be called after fit() to compute the weighted causal graph.
        
        Returns
        -------
        A weighted causal graph as a numpy array.
        The (i, j) entry in the array denotes the causal influence of node j (cause) to node i (effect).
        Note that the numpy array is normalized: its max entry is 1.
        '''

        nodename_list = self.nodename_list
        
        n_nodes    = len(nodename_list)
        n_features = self.n_out_channels
        wt_graph   = np.zeros((n_nodes, n_nodes))


        for (i, nodename) in enumerate(nodename_list):    

            assertstr = "Node:" + nodename + ", expected weight matrix shape: %d x %d" % (n_features, n_nodes*n_features)
            assert self.weight_dict[nodename].shape[0] == n_features, assertstr
            assert self.weight_dict[nodename].shape[1] == n_nodes*n_features, assertstr

            for j in range(n_nodes):
                wts = self.weight_dict[nodename][:, j*n_features:(j+1)*n_features] 
                wt_graph[i, j] = np.linalg.norm( wts ) # L2 norm 

        wt_graph = wt_graph/np.max(wt_graph) # normalize wt(i, j) \in [0,1] 
        return wt_graph  
    

