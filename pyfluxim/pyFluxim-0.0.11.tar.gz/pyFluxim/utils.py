import numpy as np  
import matplotlib.pyplot as plt
from datetime import datetime, date

def sort_ids(ids, prefix=''):
    g = {}
    elements = []
    for x in ids:
        y = x.split('.')
        k,c = int(y[0]),'.'.join(y[1:])
        elements.append(k)
        if len(y)>1:
            g[k] = g.get(k,[]) + [c]
    sortd_list = []
    for x in sorted(elements):
        sortd_list.append(prefix+str(x))
        if x in g:
            sortd_list += sort_ids(g[x],f'{prefix}{x}.')
    return sortd_list
 
def getChunk(data, chunk):
    chunks = [-1]+[x[0] for x in np.argwhere(np.isnan(data))]
    if chunk>=len(chunks):
        raise ValueError("The data does not contain enough chunk")
    else:
        chunks += [len(data)]
        return data[chunks[chunk]+1:chunks[chunk+1]]

def getJVparams(V,I):
    MPP = np.min(V*I)
    impp = np.argmin(V*I)
    iV = V.argsort()
    Isc = np.interp(0,V[iV],I[iV])
    iI = I.argsort()
    Voc = np.interp(0,I[iI],V[iI])
    return {
        "MPP":MPP,
        "Vmpp":V[impp],
        "Impp":I[impp],
        "Voc":Voc,
        "Isc":Isc,
        "FF":(I[impp]*V[impp])/(Voc*Isc)}
    
def plotJV(res, hyst=True, up=True, down=True, ax=None, **kargs):
    if ax is None:
        ax = plt.gca()
    V = res["voltage"]
    I = res["current"]
    numC = np.sum(np.isnan(V))
    if hyst and numC>1:
        for i in range(2):
            Vx = getChunk(V,i)
            UP = Vx[0]<Vx[-1]
            if UP and up or not UP and down:
                ax.plot(Vx, getChunk(I,i)*1e3, label=["down","up"][UP])
    else:
        ax.plot(V, I, label=kargs.get("label",""))
    ax.set_xlabel("Voltage [V]")
    ax.set_ylabel("Current [mA]")
    return ax
    
def flux2timestamp(ts):
    """
    convert a flux time stamp tuple to a python tuple.
    
    return (datetime object, fractional seconds)
    """
    return (datetime.fromtimestamp(ts[1]-2082844800), ts[0]/2**64)
    
def PT100res2temp(Rt, R0=100):
    """
    convert the resistivity measured of a PT100 to its equivalent temperature (in °C)
    """
    
    A = 0.003909
    B = -5.775e-7
    return (np.sqrt(A**2-4*B*(1-(Rt/R0)))-A)/(2*B)