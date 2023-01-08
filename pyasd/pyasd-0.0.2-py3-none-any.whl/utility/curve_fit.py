#!/usr/bin/env python

#=============================
#
# This script test the scipy
# function curve_fit to
# performe non-linear least
# square fitting of a set
# of data
#
#=============================

from __future__ import print_function
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def gen_noise(ndata,max_value,scale=0.1):
    return (np.random.rand(ndata)-0.5) *max_value*scale

 
def plot_fitting_function(xx,yy,func,fitted_args=(),accurate_args=(),
    xlabel='x',ylabel='y',
    figsize=(6,4),figname='Nonlinear_fitting_scipy',show=True):

    x_dense = np.linspace(np.min(xx),np.max(xx),1001)
    fig,ax = plt.subplots(1,1,figsize=figsize)
    ax.scatter(xx,yy,facecolor='C0',edgecolor='none',s=30,alpha=0.7,label='original')
    ax.plot(x_dense,func(x_dense,*fitted_args),'C1-',label='fitted')
    ax.plot(x_dense,func(x_dense,*accurate_args),'C2-',label='accurate')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    #ax.set_xticks(np.arange(0,4))
    ax.legend(scatterpoints=1)
    fig.tight_layout()
    fig.savefig(figname,dpi=500)
    if show:plt.show()
    return fig

def report_fitting(popt,pcov):
    print ('Fitted params = {}\nThe invariance is:\n{}\n'.format(popt,pcov))


def gen_dataset(func,ndata,args=()):
    # fitting the log magnetization function
    xx=np.linspace(1,100,ndata)
    yy=func(xx,*args)
    noise = gen_noise(ndata,np.max(np.abs(yy)),0.1)
    yy += noise # add some artificial "noise" to make the scatter points deviate from perfect values
    return xx,yy


if __name__=='__main__':
    from asd.utility.mag_thermal import logarithmic_magnetization
    # fitting the logarithmic magnetization function
    ntemperature = 201
    Tc = 45.
    beta = 0.3
    xx,yy = gen_dataset(logarithmic_magnetization,ntemperature,(Tc,beta))

    p0=(Tc-3,0)  # initial guess of parameters, optional
    popt,pcov=curve_fit(logarithmic_magnetization,xx,yy,p0)
    report_fitting(popt,pcov)

    kws = dict(figname='Log_magn',
    fitted_args=popt,
    accurate_args=(Tc,beta),
    xlabel='T (K)',ylabel='M')
    plot_fitting_function(xx,yy,logarithmic_magnetization,**kws)
