import numpy as np
from scipy import integrate
from scipy.signal import butter, lfilter

mases = {
        'H':1.0080, 'C':12.0107, 'O':15.9994, 'Ce':140.116, 'Pr':140.90766, 
        'Na':22.989769, 'Bi':208.9804, 'Ti':47.867, 'Sr':87.62, 'Gd':157.25,
        'Ce':140.116,
        }
charges = {
        'H':1, 'C':4, 'O':-2, 'Ce':3, 'Pr':3, 
        'Na':1, 'Bi':3, 'Ti':4, 'Sr':2, 'Gd':3,
        }
mases_to_symbols = {
        1.0080:'H', 12.0107:'C', 15.9994:'O', 87.62:'Sr', 47.867:'Ti',
        140.116:'Ce', 140.90766:'Pr', 140.908:'Pr',
        }
kb_ev = 8.6173303*10**-5 #eV/K
kb_J = 1.38064852*10**-23 #J/K
h_J = 6.62607e-34 #J*s
hb_J = 1.0545718e-34 #J*s
ev2J = 1.60217662*10**-19
ev2H = 0.037
J2ev = 1/ev2J
cm2hz = 0.02998*10**12
eV_per_Angstrom_2_Ha_per_Bohr = 1/51.42208619083232
Angstrom_2_Bohr = 1/0.529177208 
    
def flatten(t):
    return [item for sublist in t for item in sublist]

def fonter():
    import matplotlib 
    font = {'family' : 'sans-serif',
            'weight' : 'normal',
            'size'   : 24}
    matplotlib.rc('font', **font)

def coth(x):
    return 1/np.tanh(x)

def angle(a,b):
    r = np.dot(a, b)/(np.linalg.norm(a, axis=0)*np.linalg.norm(b, axis=0))
    return np.arccos(r)

def u_rotate(phi, u):
    norm_u = np.power(np.sum(np.power(u,2)),.5)
    u = u/norm_u
    rot_mat = np.zeros((3, 3))
    
    rot_mat[0,0] = np.cos(phi)+np.power(u[0],2)*(1-np.cos(phi))
    rot_mat[0,1] = u[0]*u[1]*(1-np.cos(phi))-u[2]*np.sin(phi)
    rot_mat[0,2] = u[0]*u[2]*(1-np.cos(phi))+u[1]*np.sin(phi)
    
    rot_mat[1,0] = u[0]*u[1]*(1-np.cos(phi))+u[2]*np.sin(phi)
    rot_mat[1,1] = np.cos(phi)+np.power(u[1],2)*(1-np.cos(phi))
    rot_mat[1,2] = u[2]*u[1]*(1-np.cos(phi))-u[0]*np.sin(phi)
    
    rot_mat[2,0] = u[0]*u[2]*(1-np.cos(phi))-u[1]*np.sin(phi)
    rot_mat[2,1] = u[2]*u[1]*(1-np.cos(phi))+u[0]*np.sin(phi)
    rot_mat[2,2] = np.cos(phi)+np.power(u[2],2)*(1-np.cos(phi))
    return rot_mat

def m_rotate(angle, axis):
    rot_mat = np.zeros((3, 3))
    if axis == "x":
        rot_mat[0, :] = [1, 0, 0]
        rot_mat[1, :] = [0, np.cos(angle), -np.sin(angle)]
        rot_mat[2, :] = [1, np.sin(angle), np.cos(angle)]
    if axis == "y":
        rot_mat[0, :] = [np.cos(angle), 0, np.sin(angle)]
        rot_mat[1, :] = [0, 1, 0]
        rot_mat[2, :] = [-np.sin(angle), 0, np.cos(angle)]
    if axis == "z":
        rot_mat[0, :] = [np.cos(angle), -np.sin(angle), 0]
        rot_mat[1, :] = [np.sin(angle), np.cos(angle), 0]
        rot_mat[2, :] = [0, 0, 1]
    return rot_mat

def gaussian(x, sigma, xo):
    return (1/(sigma*(2*np.pi**.5)))*np.exp(-.5*((x-xo)/sigma)**2)

def intgr(x, y):    
    I = [0]
    for i in range(1, len(x)):
        I.append(integrate.simps(y[:i+1], x[:i+1]))
    I = np.array(I)
    return I

def intgrt(x, y):    
    I = [0]
    for i in range(1, len(x)):
        I.append(np.trapz(y[:i+1], x[:i+1]))
    I = np.array(I)
    return I

def smooth(y, box_pts):
    beg = y[0]
    y = y - beg
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth+beg

def smooths(x, n):
    if n==0:
        return x
    else:
        xn = np.zeros((len(x)))
        xn[0] = np.mean(x[:2])
        xn[1] = np.mean(x[:3])
        xn[2] = np.mean(x[:4])
        xn[-1] = np.mean([x[-1], x[-2]])
        xn[-2] = np.mean([x[-1], x[-2], x[-3]])
        xn[-3] = np.mean([x[-1], x[-2], x[-3], x[-4]])
            
        for i in range(n,len(x)-n):
            xn[i] = np.mean(x[i-n:i+n+1])
        return xn
    
def vdos(x, tstep, isvelocity=False):
    if isvelocity:
        v=x
    else:
        v = np.gradient(x, axis=0)
    l = len(v)
    cor = np.array([np.correlate(v[:,i], v[:,i], mode='full')[l:] for i in range(x.shape[1])]).T
    # cor = cor/cor[0,:]
    freq = (.5/tstep)*np.arange(int(l/2))/int(l/2)
    vdos = []
    for i in range(cor.shape[1]):
        vdos.append(np.abs(np.fft.rfft(cor[:,i])[:int(l/2)]))
    vdos = np.array(vdos)
    return freq, vdos

def my_fft(x, tstep):
    l = len(x)
    freq = (.5/tstep)*np.arange(int(l/2))/int(l/2)
    fft_result = np.abs(np.fft.rfft(x)[:int(l/2)])
    return freq, fft_result

def bmeos(v, e0, v0, b0, b0p):
    return e0 + (9*v0*b0/16)*(
            b0p*(-1+(v0/v)**(2/3))**3 + 
            ((-1+(v0/v)**(2/3))**2)*(6-4*(v0/v)**(2/3))
            )

def lowpass(y, highcut=80, fs=1):
    if highcut>0:
        yo = y[0]
        y=y-yo
        fs = 1000/fs
        nyq = 0.5 * fs
        high = highcut / nyq
        b, a = butter(7, high, btype='low')
        return  lfilter(b, a, y)+yo
    else:
        return y

#lowpcut and highcut in Thz, fs is sampling in fs
def bandpass(y, lowcut, highcut, fs):
    yo = y[0]
    y=y-yo
    fs = 1000/fs
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(7, [low, high], btype='band')
    return  lfilter(b, a, y)+yo

#lowpcut and highcut in Thz, fs is sampling in fs
def highpass(y, highcut=80, fs=1):
    yo = y[0]
    y=y-yo
    fs = 1000/fs
    nyq = 0.5 * fs
    high = highcut / nyq
    b, a = butter(7, high, btype='highpass')
    return  lfilter(b, a, y)+yo

def corelate(a,b):
    c1 = np.max(np.correlate(a, a, mode='full'))
    c2 = np.max(np.correlate(b, b, mode='full'))
    c = np.correlate(a, b, mode='full')/(np.sqrt(c1*c2))
    cl = np.flipud(c[:int((len(c)+1)/2)])
    cp = c[int((len(c))/2):]
    return (cp+cl)/2

def acorelate(x):
    c = np.correlate(x, x, mode='full')
    break_point = int(np.floor(len(c)/2))
    cl = np.flipud(c[:break_point+1])
    cp = c[break_point:]
    return (cl+cp)/2

