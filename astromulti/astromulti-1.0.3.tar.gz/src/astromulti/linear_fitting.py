from scipy.odr import ODR, Data as odrdata, unilinear as odrlinear
import numpy as np
from inspect import signature


def spidx( FDs, FDers, freqs, freqers, nsamps ):
    """
    Measure the spectral index with correct errors
    """

    # prepare MC samples and remove negatives (all the corresponding elements of each -ve/0 will be removed)
    fd_samps = np.stack([ np.random.normal( loc=cent, scale=np.abs(sigma), size=nsamps ) for cent,sigma in zip(FDs,FDers) ])
    fr_samps = np.stack([ np.random.normal( loc=cent, scale=np.abs(sigma), size=nsamps ) for cent,sigma in zip(freqs,freqers) ])
    pos_mask = (fd_samps>0).all(axis=0) & (fr_samps>0).all(axis=0)
    deleting = np.where(~pos_mask)[0]
    fd_samps = np.log(np.delete(fd_samps,deleting,1))
    fr_samps = np.log(np.delete(fr_samps,deleting,1))

    # get spidx for each set and measure mean & std
    spx_samps = []
    if len(FDs)>2:
        for mc_idx in range(np.shape(fd_samps)[1]):
            m0,_,_,_ = OLSy( fr_samps[:,mc_idx],fd_samps[:,mc_idx] )
            spx_samps.append(m0)
    else:
        for mc_idx in range(np.shape(fd_samps)[1]):
            m0 = ( fd_samps[:,mc_idx][0]-fd_samps[:,mc_idx][1] ) / ( fr_samps[:,mc_idx][0]-fr_samps[:,mc_idx][1] )
            spx_samps.append(m0)
    spidx_mc = np.nanmean(spx_samps)
    spidxe_mc= np.nanstd(spx_samps)

    # sometimes MC gives error that's too small. In that case, use the usual fit (unless it's only two points of course)
    if len(FDs)>2:
        spidx_ols,_,spidxe_ols,_ = line_fit( np.log(freqs), np.log(FDs), 'OLSy' )
    else:
        spidxe_ols = 0.
    if spidxe_mc > spidxe_ols:
        return [spidx_mc,spidxe_mc]
    else:
        return [spidx_ols,spidxe_ols]


def plane_fit( points ):
    '''
    Plane equation: a*x + b*y + c = z
    Matrix equation: R * S = Z
        where R = [ [x1,y1,1] , ... , [xn,yn,1] ]   (nx3 matrix; input x&y)
              Z = [ z1 , ... , zn ]                 (nx1 matrix; input heights)
              S = [ a,b,c ] = (R.T * R).I *R.T *Z   (3x1 matrix; output)
              (unique solution)
    If R.T * R is singular, then its inverse (Q) doesn't exist. Numpy will raise an error in this case.
    Check https://en.wikipedia.org/wiki/Ordinary_least_squares if in doubt
    '''

    R = np.matrix(np.stack([ points[:,0], points[:,1], np.ones(len(points)) ]).T)   # x's, y's, 1's (see R in the comment above)
    Z = np.matrix(points[:,2]).T                                                    # z's
    Q = (R.T * R).I                                                                 # cofactor matrix? Not sure if the name is correct, but the formula is correct
    S = Q * R.T * Z                                                                 # solution (estimate of a,b,c)
    resids = np.linalg.norm( Z - R*S )                                              # rms residuals
    s_sqrd = resids**2/ (len(points)-3)                                             # s**2 = residuals**2 / degrees of freedom
    errors = np.sqrt(np.diagonal(s_sqrd*Q))                                         # errors of the estimated parameters
    values = np.array(S.flatten())[0]                                               # estimated parameters

    return values, errors


def line_fit( x, y, regr_type=None, xe=None, ye=None, MCsamps=None, MCtype=None ):
    '''
    Performs line fitting of y vs x
    regr_type = 'OLSy'   (ordinary least squares: normal ie minimizes y-residuals)
             or 'OLSx'   (ordinary least squares: reversed ie minimizes x-residuals, done by flipping X and Y)
             or 'swapxy' (geometric mean of OLSy and OLSx)
             or 'MC'     (Monte Carlo simulation, includes errors)
    x and y should be 1D arrays of same size corresponding to each other.
    Uncertainties in x & y will be used only for regr_type='MC'
    Returns slope, intercept, slope_error, intercept_error
    '''

    fdict = { 'OLSy'  : OLSy,
              'OLSx'  : OLSx,
              'swapxy': swapxy,
              'MC'    : MC
             }
    if (xe is None and ye is not None) or (xe is not None and ye is None):
        print('NOTE: there is uncertainty given only for one variable, so, not using any.')
        xe,ye = None,None

    nparams = len(signature(fdict[regr_type]).parameters)
    if nparams==6:
        if MCtype is not None:
            if MCtype=='MC':
                raise RuntimeError("MCtype cannot be 'MC'!")
            [m,b,sm,sb] = fdict[regr_type](x,y,xe,ye,MCsamps,fdict[MCtype])
        else:
            print("MCtype not given, using swapxy.")
            [m,b,sm,sb] = fdict[regr_type](x,y,xe,ye,MCsamps,fdict['swapxy'])
    if nparams==2:
        if xe is not None and ye is not None:
            print('NOTE: Uncertainties will not be used for the input regr_type.')
        [m,b,sm,sb] = fdict[regr_type](x,y)

    return [m,b,sm,sb]


def OLSy(x,y):
    '''
    y = m*x + c
    Y-on-X regression (Y is the dependent variable, X has no error)
    '''

    p,V = np.polyfit(x,y,1,cov=True)
    m_e = np.sqrt(V[0][0])
    c_e = np.sqrt(V[1][1])

    return [p[0], p[1], m_e, c_e]


def OLSx(x,y):
    '''
    y = m*x + c
    X-on-Y regression (X is the dependent variable, Y has no error)
    Done by inverting X and Y:
        compare the following
        1] x = y/m    - c/m     (obtained from y=m*x+c)
        2] x = p[0]*y + p[1]    (obtained from flipping x and y)
        So  p[0]=1/m  &  p[1]=-c/m=-c*p[0]
        =>  m=1/p[0]  &  c=-p[1]/p[0]
    '''

    p,V = np.polyfit(y,x,1,cov=True)
    m_e1= np.sqrt(V[0][0])
    c_e1= np.sqrt(V[1][1])

    m   = 1/p[0]
    m_e = m_e1 /p[0]**2
    c   = -p[1]/p[0]
    c_e = ( p[1]*m_e1 + p[0]*c_e1 )/p[0]**2

    return [m, c, m_e, c_e]


def swapxy(X,Y):
    '''
    geometric mean of OLSx & OLSy
    Are the values of intercept and error correct?? TODO
    '''

    m1,c1,m1e,c1e = OLSy(X,Y)
    m2,c2,m2e,c2e = OLSx(X,Y)
    cx = np.mean(X)
    cy = np.mean(Y)

    m   = np.sqrt(m1*m2)
    #m_e = (m1*m2e+m2*m1e)/2/m
    m_e = np.abs(m1-m2)/2
    c   = cy - m*cx
    c_e = np.sqrt( np.abs(c1-c2)**2 + c1e**2 + c2e**2 )

    return [m,c,m_e,c_e]


def MC(x,y,xe,ye,nsamples,funcname):
    '''
    TODO
    y = m*x + c
    Uses several (nsamples) simulations of 'funcname'
    For each point (xi,yi), a MC sim is done with Gaussian distribution
    ie, xi,yi is the center and (xie,yie) is its width
    Final mean and std of all slopes/intercepts are returned.
    NOTE: this may take a long time if nsamples is too large
    '''

    print("Must check again if all is well in this function!")

    # remove NaNs because np.random.normal is giving weird shape mismatch error
    x = x[~np.isnan(x)]
    y = y[~np.isnan(y)]
    xe = xe[~np.isnan(xe)]
    ye = ye[~np.isnan(ye)]

    # prepare MC samples
    x_samps = np.stack([ np.random.normal(loc=cent, scale=np.abs(sigma), size=nsamples) for cent,sigma in zip(x,xe) ])
    y_samps = np.stack([ np.random.normal(loc=cent, scale=np.abs(sigma), size=nsamples) for cent,sigma in zip(y,ye) ])

    # get slope and intercept for all MC samples
    m_samps = []
    c_samps = []
    me_samps = []
    ce_samps = []
    for mc_idx in range(nsamples):
        m0,c0,me0,ce0 = funcname( x_samps[:,mc_idx],y_samps[:,mc_idx] )
        m_samps.append(m0)
        c_samps.append(c0)
        me_samps.append(me0)
        ce_samps.append(ce0)

    # prepare weights
    mwts = np.abs(1/np.array(me_samps))**2
    cwts = np.abs(1/np.array(ce_samps))**2

    # final results
    m = np.average( m_samps, weights=mwts )
    c = np.average( c_samps, weights=cwts )
    me = np.average((m_samps-m)**2, weights=mwts)
    ce = np.average((c_samps-c)**2, weights=cwts)

    #return [ np.mean(m_samps), np.mean(c_samps), np.std(m_samps), np.std(c_samps) ]
    return [ m, c, me, ce ]




















