#!/usr/bin/env python
# coding: utf-8

# # Multilayer Perceptron
# 
# - A final model in form of object built by <i>mlp_component</i> called MultilayerPerceptron
# - methods in MultilayerPerceptron have its own purpose:
# 1. `__init__` : Define the required structure of mlp architecture 
# 2. `compile` : Specify how you want mlp to behave
# 3. `fit` : fit data with the given epoch, batch size, and more
# 4. `predict` : predicting input (**not test on regression, multi-classification yet** )

# In[1]:


#import import_ipynb


# In[2]:


from .mlp_component import *                          #linear_forward ,.... linear_backward_model
from .compute_cost import *
from .update_params import *
from .debug_util import *                       # gradient_check_n
from .initializer import *
from .activation import *
from .losses import *                           # binary_cross_entropy_loss, BCE_dAL
from .optimizer import initialize_v, initialize_s
from .load import data_loader
from .metrics import accuracy_score


from .utils.py_util import dictionary_to_vector, vector_to_dictionary, gradients_to_vector, pd_to_np

# %% External module
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from time import time
import math
from copy import deepcopy


# In[ ]:


__all__ = ['MultilayerPerceptron']


# In[5]:


class MultilayerPerceptron:
    """
    A L-layer Perceptron Neural Network
    - Able to fit with the predictors (X) and the response (Y)
    - Able to predict_proba and predict with threshold
    
    To see the last fit model parameter, uses self.param where self refer to the fit model
    """

    def __init__(self, layer_dims : list , hidden_activation_function : str , output_activation_function : str ):
        
        """
        Launch the MultilayerPerceptron architecture with the given hyperparameter
        
        Arguments:
         1. layer_dims --- Number of units from input layer to output layer
         2. hidden_activation_function --- Activation function for all hidden layer(s) in forward model (relu,leakyrelu,tanh,sigmoid)
         3. output_activation_function --- Activation function for all hidden layer(s) in forward model (sigmoid,softmax, linear)
        """
        
        self.layer_dims = layer_dims
        self.L = len(layer_dims) - 1
        self.hidden_activation_function = hidden_activation_function
        self.output_activation_function = output_activation_function
        
        
    def compiles(self, lr = 1e-4, loss='binary_cross_entropy_loss', initialization = 'random' ,regularization = None ,
                 optimizer = None, **kwargs):
        """Compile options for training Deep-L layer Neural network
        
        Arguments
        ------------------------
        lr --- (initial) learning rate for gradient descent 
        
        loss : str --- loss function of the predicted value and the observation (default : binary_cross_entropy_loss_function)
                             [binary_cross_entropy_loss, cross_entropy_loss_function, MSE]
                             
                        Warning : If your output activation function is Linear, then MSE MUST be your loss
                 
        initialization --- weight initialization technique (default:random)
                             ['zero','random','xavier','he']
                            
        regularization --- regularization technique (default:None)
                             [None, 'L2','dropout']
        
        optimization (Not done) --- optimization technique (default:None)
                             [None, 'momentum' , 'nesterov_momentum' , 'adagrad' , 'rmsprop' , 'adam','nadam']
        
        Keyword Arguments
        ------------------------
        lambd ---   L2 Regularization parameter
                    *When regularization is 'L2'
        
        keep_prob_sequence --- Keep probability of the nodes for every layer
                                *When regularization is 'Dropout' 
        """
        
        _allowed_loss = {'binary_cross_entropy_loss','cross_entropy_loss'}
        _allowed_initialization = {'zero','random',
                                   'xavier','he'}
        
        _allowed_regularization = {'L2', 'L1',
                                   'dropout',
                                      None}

        _allowed_optimizer = {'momentum','nesterov_momentum',    
                              'adagrad','rmsprop',
                              'adam','nadam',
                                 None}
        
        assert loss in _allowed_loss,  'Invalid Loss: ' + loss
        assert initialization in _allowed_initialization,  'Invalid Initialization: ' + initialization
        assert regularization in _allowed_regularization,  'Invalid Regularization: ' + regularization
        assert optimizer in _allowed_optimizer,  'Invalid Optimizer: ' + optimizer        
        
        self.lr = lr
        
        map_loss = {'binary_cross_entropy_loss':binary_cross_entropy_loss, 'cross_entropy_loss' : cross_entropy_loss, 'MSE' : MSE}
        map_dZL_loss = {'binary_cross_entropy_loss':BCE_dZL, 'cross_entropy_loss' : CE_dZL, 'MSE' : MSE_dZL}
        self.loss_function = map_loss[loss]
        self.dZL_loss_function = map_dZL_loss[loss]
        self.initialization = initialization
        self.regularization = regularization
        self.optimizer = optimizer
        
        allowed_kwargs = {'lambd',
                          'keep_prob_sequence',
                          'beta1',
                          'use_nesterov',
                          'beta2',
                          'eps'}
        for kwarg in kwargs.keys():                                                 # .. validate all acceptable keyword arguments
            assert kwarg in allowed_kwargs, 'Invalid keyword argument: ' + kwarg
        
        if self.regularization:                                                     # .. validate keyword argument for regularization
            reg_assertion_dct = {'L2' : {'lambd'},
                                 'dropout': {'keep_prob'}}
            required = reg_assertion_dct.get(self.regularization)   # {'lambd'}
            assert required <= set(kwargs), f'Missing argument {required}'

        
        if self.optimizer:
            optmz_assertion_dct = {'momentum' : {'beta1'},
                                   'rmsprop': {'beta2','eps'},
                                  'adam' : {'beta1','beta2','eps'}}            
            required = optmz_assertion_dct.get(self.optimizer)
            assert required <= set(kwargs), f'Missing one of these arguments {required}'        
            
        self.kwargs_model = kwargs
        
    def fit(
        self,
        X: pd.DataFrame,
        Y: pd.Series,
        Epochs: int,
        batch_size:int=32 ,
        seed:int = 42,
        report_cost: bool = True,
        grad_check:bool = False,
        refit: bool = True,
        **kwargs
    ):
        """
        Fit the launched Deep L layer with the given data X , Y

        Arguments:
         X --- Pandas Dataframe of predictors
         Y --- Pandas Series of response (0 : negative, 1:positive)
         Epoch --- number of epochs 
         batch_size --- Size of batch (Stochastic:1,Mini batch:around 1 and m, Batch: m) 
         seed --- Random seed for shuffling the row in DataFrame (for non-batch gradient descent)
         report_cost --- report the cost epochs every 1000 epoch
         grad_check --- Numerically test on the precision of backprop gradient
         refit --- reinitialize the parameter and fitting again
         
        Keyword Argument:
         evry_report_epoch = 1000
        """
        allowed_kwargs = {'evry_report_epoch'}
        for kwarg in kwargs.keys():                                                 # .. validate all acceptable keyword arguments
            assert kwarg in allowed_kwargs, 'Invalid keyword argument: ' + kwarg         
            
        self.X , self.Y = X, Y ;df = pd.concat([X,Y],axis=1)
        mini_batches : list = data_loader(df,batch_size,Y.columns)
        if refit:                                                                 # ..Restart fitting ? Initiate the param 
            self.param = initiate_param(self.layer_dims, self.initialization)
            t = 1  
            self.kwargs_model.update({'t':t})                                     # kwargs for optimizer 
        
        else:
            self.kwargs_model.update({'t':t})  
        cost_list = []                                                            # .. for report_cost = True
        
        if report_cost:
            if {'evry_report_epoch'} <= set(kwargs):
                evry_report_epoch = kwargs['evry_report_epoch']
            else:
                evry_report_epoch = 1000
                
        for epoch in range(1,Epochs+1):                                           # ..Each epoch
            cost = 0 
            
            for batch in range(len(mini_batches)):          
                                                                                  
                mini_batch = mini_batches[batch]                                  # ..Preprocessing Each batch
                mini_batch_X , mini_batch_y = mini_batch[0], mini_batch[1]
                
                mini_batch_X = mini_batch_X.to_numpy().T
                mini_batch_y = mini_batch_y.to_numpy().T
                m = mini_batch_y.shape[1]; # Size of each batch
                nrow = np.shape(mini_batch_X)[0] # Number of feature
                
                AL, cache = L_model_forward(mini_batch_X, self.param,                                 # ..Forward Prop
                                           hidden_activation_function=self.hidden_activation_function, 
                                           output_activation_function=self.output_activation_function,
                                            **self.kwargs_model )                                      # ..kwargs for dropout

                
                kwargs_regularization = {'lambd':self.kwargs_model['lambd'], 'param':self.param} if self.regularization in {'L2','L1'} else {}
                cost += compute_cost(AL, mini_batch_y,                                           # ..Compute cost function for reporting to user only 
                                     self.loss_function,
                                     self.regularization,
                                     **kwargs_regularization)

                self.grads = L_model_backward(AL, mini_batch_y, cache,                          # ..Backward Prop                   
                                         self.hidden_activation_function,
                                        self.output_activation_function,
                                        self.dZL_loss_function)

                if (grad_check and epoch % evry_report_epoch == 0):                                          # ..Gradient checking for every 1000 epochs
                    gradient_check_n(self.param , self.grads, mini_batch_X, mini_batch_y ,
                                    self.hidden_activation_function,
                                    self.output_activation_function,
                                    self.loss_function,
                                    self.regularization,
                                    **kwargs_regularization)
                    

                self.kwargs_model.update({'m': m})                                             # ..Update paramater by gradient
                
                if self.optimizer and self.kwargs_model['t'] == 1:
                    self.kwargs_model.update({'v': initialize_v(self.grads)})                 # .. (HELP) required each optimizer to not all have v or s 
                    self.kwargs_model.update({'s': initialize_s(self.grads)})
                
                self.param, optmz_cache = update_params(param = self.param, 
                                                      grads = self.grads, 
                                                      lr=self.lr,
                                                      regularization=self.regularization,
                                                      optimizer=self.optimizer,
                                                      **self.kwargs_model)                           #..kwargs for L2 regularization
                
                if self.optimizer: 
                    v, s = optmz_cache[0], optmz_cache[1]
                    t = self.kwargs_model['t'] 
                    self.kwargs_model.update({ 'v': v, 's': s ,'t':t+1}) 
            
            cost_list.append(np.squeeze(cost)/len(mini_batches))
            
            if (report_cost and epoch % evry_report_epoch == 0):
                print(f"Epoch {epoch}/{Epochs} : ===Cost=== : {np.squeeze(cost)/len(mini_batches)}")
                
        if report_cost:                                                      #..Done fitting and show plot of cost f.
            plt.plot(cost_list ,)       
            plt.xlabel("Epoch")
            plt.ylabel("Cost function")
            plt.show()
    
    @pd_to_np
    def predict(self,X , predict_proba = True, threshold: float = 0.5):
        AL, _ = L_model_forward(X.T, self.param, 
                                hidden_activation_function=self.hidden_activation_function,
                                output_activation_function=self.output_activation_function   # linear if regression
                               )
        if predict_proba :
            AL_ = AL
        
        else:
            if AL.shape[0] == 1 :
                AL_ = np.where(AL>=threshold,1,0)
                AL_ = np.squeeze(AL_)

                assert AL_.ndim == 1

                return AL_

            elif AL.shape[0] > 1 : 
                # Multi-class or Multi-label classification
                if self.output_activation_function == 'softmax':
                    AL_ = np.argmax(AL,axis=0)
                    AL_ = self.Y.columns[AL_]
                    AL_ = AL_.values

                    assert AL_.ndim == 1

                elif self.output_activation_function == 'sigmoid':
                    print('Under Maintainance for Multi-label')
                    pass

            else:
                AL_ = AL
        
        return AL_
   
    @classmethod
    def initiate_by_hyperparam_dict(cls,hyperparam):
        """
        Launch the Deep_L_layer with the given hyperparameter in form of dictionary
        
        Arguments:
        hyperparam: A dictionary with key:
        
         layer_dims --- Number of units of that L layer
         hidden_activation_function --- Activation function for all hidden layer(s) in forward model (relu,leakyrelu,tanh,sigmoid)
         last_hidden_activation_function --- Activation function for all hidden layer(s) in forward model (sigmoid,linear)
         
          {"layer_dims" : [ncol,8,6,4,2,1],
          "hidden_activation_function" : 'tanh' ,
          "output_activation_function" : 'sigmoid' }
          
        Supported activation
        """

        # Required hyperparameter attributes
        layer_dims = hyperparam['layer_dims']
        hidden_activation_function = hyperparam["hidden_activation_function"]
        output_activation_function = hyperparam["output_activation_function"]
        
        return cls(layer_dims,hidden_activation_function,output_activation_function)
    
    
    def __repr__(self):
        return f"MultilayerPerceptron({self.layer_dims}, {self.hidden_activation_function}, {self.output_activation_function})"

    def __str__(self):
        return f"A {self.L - 1} Layer Perceptron (Forward activation :{self.hidden_activation_function},Backward activation :{self.last_activation_function})"


# ---
