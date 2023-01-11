"""
straighten.py

Modules for correcting psc. 

"""

import math

import numpy as np

from sklearn.linear_model import LinearRegression

from scipy.sparse import csc_matrix, eye, diags
from scipy.sparse.linalg import spsolve

from ..abf.abf_obj import ABF
from .preprocessing_utils import _find_sweep_data

import warnings
warnings.filterwarnings('ignore')

###################################################################################################
###################################################################################################

lin=LinearRegression()

def straighten(data, time_segment = 10): 
    """
    Straighten baseline using updated current psc following
    baseline exclusion <= dropoff threshold.
    
    Arguments
    ---------
    data (list of objects):
        list of data objects processed using loader.py.
        
    time_segment (int): 
        second intervals to segment psc for baseline removal and correction.
        
    Returns
    -------
    psc_corrected (arr): 
        straightened psc.
        
    """
    
    if isinstance(data, list): 
        for obj in data: 
            if isinstance(obj, ABF):
                
                # collect baseline subtraction sweepdata
                #----------------------------------------
                
                try: 
                    sweepdata = obj.baselinecorr_sweepdata_dropped
                    
                    try: 
                        if math.isnan(sweepdata): 
                            sweepdata = obj.baselinecorr_sweepdata # default to preprocessed + baselinecorr
                    except: 
                        pass
                        
                except AttributeError:
                    try: 
                        sweepdata = obj.baselinecorr_sweepdata
                    except AttributeError:
                        raise AttributeError("NOTE: do not conduct psc straightening without a baseline subtactraction ...")
                    
                try: 
                    obj.preprocessed_params
                except AttributeError: 
                    obj.preprocessed_params = ({})
                    
                # find srate 
                #-----------
                
                _, srate = _find_sweep_data(obj)
                
                # baseline subtraction
                #---------------------
                # note: to only be conducted in 
                # recordings from voltage clamp 
                # hence, no multidimensional arrays
                
                if len(sweepdata) == 1: 
                    
                    # segment sweepdata
                    #-------------------
                    
                    rec_len = len(sweepdata[0])/srate
                    segment_current = np.array_split(sweepdata[0], int(rec_len/time_segment))
                    
                    # straighten sweepdata
                    # in timeseries segments
                    #-----------------------
                    
                    corrected_psc = np.array([])
                    for x in range(len(segment_current)): 
                        modpoly_output = IModPoly(segment_current[x], degree=4, repitition=1000, gradient=0.01)
                        corrected_psc = np.concatenate([corrected_psc, modpoly_output])
                    
                    # initiate instance
                    #-------------------
                    
                    obj.straightened_sweepdata = [corrected_psc]
                    obj.preprocessed_params.update({'straightening_time_segment': time_segment, 'iterations': 1000,\
                                                    'degree': 4, 'gradient': 0.01}) # set attr params 
                    
                else: 
                    raise ValueError("voltage clamp recordings to only be used"
                                    f"for baseline subtraction | {len(sweepdata)} sweepdata found ...")
                    
            else:
                raise TypeError("no data object found ...")
                
        return data


def poly(input_array_for_poly, degree_for_poly):
    """
    qr factorization of a matrix. q` is orthonormal and `r` is upper-triangular.
    
    >   QR decomposition is equivalent to Gram Schmidt orthogonalization, which builds a sequence of orthogonal polynomials
        that approximate your function with minimal least-squares error
    >   in the next step, discard the first column from above matrix.
    >   for each value in the range of polynomial, starting from index 0 of pollynomial range, (for k in range(p+1))
        create an array in such a way that elements of array are (original_individual_value)^polynomial_index (x**k)
    >   concatenate all of these arrays created through loop, as a master array. This is done through (np.vstack)
    >   transpose the master array, so that its more like a tabular form(np.transpose)
    
    Arguments
    ---------
    input_array_for_poly (arr): 
        input array 
        
    degree_for_poly (int): 
        poly order 
    
    adapted from: https://github.com/StatguyUser/BaselineRemoval/blob/master/src/BaselineRemoval.py
    
    """
    
    input_array_for_poly = np.array(input_array_for_poly)
    X = np.transpose(np.vstack((input_array_for_poly**k for k in range(degree_for_poly+1))))
    
    return np.linalg.qr(X)[0][:,1:]


def IModPoly(input_array, degree=2, repitition=100, gradient=0.001):
    """
    IModPoly from paper: Automated Autofluorescence Background Subtraction Algorithm for Biomedical Raman Spectroscopy,
    by Zhao, Jianhua, Lui, Harvey, McLean, David I., Zeng, Haishan (2007)
    
    Arguments
    ---------
    degree (int):
        polynomial degree, default is 2        
    
    repitition (int):
        how many iterations to run, default is 100
    
    gradient (float):
        gradient for polynomial loss, default is 0.001. It measures incremental gain over each iteration. 
        If gain in any iteration is less than this, further improvement will stop.
        
    adapted from: https://github.com/StatguyUser/BaselineRemoval/blob/master/src/BaselineRemoval.py
        
    """

    yold=np.array(input_array)
    yorig=np.array(input_array)
    corrected=[]

    nrep=1
    ngradient=1

    polx=poly(list(range(1,len(yorig)+1)),degree)
    ypred=lin.fit(polx,yold).predict(polx)
    Previous_Dev=np.std(yorig-ypred)

    #iteration1
    yold=yold[yorig<=(ypred+Previous_Dev)]
    polx_updated=polx[yorig<=(ypred+Previous_Dev)]
    ypred=ypred[yorig<=(ypred+Previous_Dev)]

    for i in range(2,repitition+1):
        if i>2:
            Previous_Dev=DEV
        ypred=lin.fit(polx_updated,yold).predict(polx_updated)
        DEV=np.std(yold-ypred)

        if np.abs((DEV-Previous_Dev)/DEV) < gradient:
            break
        else:
            for i in range(len(yold)):
                if yold[i]>=ypred[i]+DEV:
                    yold[i]=ypred[i]+DEV
                    
    baseline=lin.predict(polx)
    corrected=yorig-baseline
    
    return corrected


def ZhangFit(input_array, lambda_=100, porder=1, repitition=15):
    """
    Implementation of Zhang fit for Adaptive iteratively reweighted penalized least squares for baseline fitting.
    Modified from Original implementation by Professor Zhimin Zhang at https://github.com/zmzhang/airPLS/
    
    Arguments
    ---------
    lambda_ (int): 
        parameter that can be adjusted by user. The larger lambda is,  the smoother the resulting background. 
        
    porder (int): 
        adaptive iteratively reweighted penalized least squares for baseline fitting. 
        
    repitition (int): 
        how many iterations to run, and default value is 15.
        
    adapted from: https://github.com/StatguyUser/BaselineRemoval/blob/master/src/BaselineRemoval.py
        
    """

    yorig=np.array(input_array)
    corrected=[]

    m=yorig.shape[0]
    w=np.ones(m)
    
    for i in range(1,repitition+1):
        corrected=_WhittakerSmooth(yorig,w,lambda_, porder)
        d=yorig-corrected
        dssn=np.abs(d[d<0].sum())
        if(dssn<0.001*(abs(yorig)).sum() or i==repitition):
            
            if(i==repitition): print('WARING max iteration reached!')
            break
        
        w[d>=0]=0 # d>0 means that this point is part of a peak, so its weight is set to 0 in order to ignore it
        w[d<0]=np.exp(i*np.abs(d[d<0])/dssn)
        w[0]=np.exp(i*(d[d<0]).max()/dssn) 
        w[-1]=w[0]
        
    return yorig-corrected


def _WhittakerSmooth(x, w, lambda_, differences = 1):
    """
    Penalized least squares algorithm for background fitting
    
    Arguments
    ---------
    x:
        input data (i.e. chromatogram of spectrum)
        
    w:
        binary masks (value of the mask is zero if a point belongs to peaks and one otherwise)
        
    lambda_:
        parameter that can be adjusted by user. The larger lambda is, the smoother the resulting background
        
    differences:
        integer indicating the order of the difference of penalties

    Returns
    -------
    The fitted background vector
    
    adapted from: https://github.com/StatguyUser/BaselineRemoval/blob/master/src/BaselineRemoval.py
        
    """
    
    X=np.matrix(x)
    m=X.size
    i=np.arange(0,m)
    E=eye(m,format='csc')
    D=E[1:]-E[:-1] # numpy.diff() does not work with sparse matrix. This is a workaround.
    W=diags(w,0,shape=(m,m))
    A=csc_matrix(W+(lambda_*D.T*D))
    B=csc_matrix(W*X.T)
    background=spsolve(A,B)
    
    return np.array(background)