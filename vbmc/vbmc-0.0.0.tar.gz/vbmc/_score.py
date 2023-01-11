import numpy as np

__all__ = [
    'angularyResolved','spatiallyResolved',
    ]


def angularyResolved(v,w,nPh,nn):
    da = np.pi/2/nn # Δα
    alpha = np.array([(i + 1/2)*da for i in range(nn)])
    alpha_ = np.array([(i)*da for i in range(nn+1)])
    do = 4*np.pi*np.sin(alpha)*np.sin(da/2) # ΔΩ
    at = np.arccos(abs(v.T[2])) # 光子の射出角度
    ar = []
    for i in range(nn):
        index = np.where((alpha_[i] < at)&(alpha_[i+1] >= at))[0]
        ar.append(w[index].sum())
    return alpha,np.array(ar)/(do*nPh)


def spatiallyResolved(p,w,nPh,nn,dr):
    rr = np.array([(i+1/2)*dr for i in range(nn)])
    rr_ = np.array([(i)*dr for i in range(nn+1)])
    da = 2*np.pi*rr*dr

    r = np.sqrt(p.T[0]**2 + p.T[1]**2)
    sr = []
    for i in range(nn):
        index = np.where((rr_[i] < r)&(rr_[i+1]>=r))[0]
        sr.append(w[index].sum())
    return rr,np.array(sr)/nPh/da
