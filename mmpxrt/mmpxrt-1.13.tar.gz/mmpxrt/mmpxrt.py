"""
Created on Tue Aug 20 15:35:05 2019

@author: Michal Smid, IoP ASCR 2015-2017, HZDR 2018-2019
                ||/
 M~M~P~X~R~T   |/|
 Michal       ///-----------<
   Mosaic    |/| \
     Python |//   \
       X-          \
         Ray        \
           Tracing=======
"""

import pickle
from mpl_toolkits.mplot3d import Axes3D
import random
import matplotlib.pyplot as plt
from astropy.io import ascii
import numpy as np
import time
import sys
import multiprocessing
import pdb
import math
import os
from datetime import datetime
#import numba as nb
### Utils & small

def init():
    """
    Initializes the mmmpxrt dictionary of parameters.

    Retrurns:
        dict: dictionary of dictionaries with default values of all parameters.
    """
    #pyversion('/usr/bin/python3.6')
    crystal={}
    geometry={}
    source={}
    simulation={}

### Simulation parameters

    simulation['name']='someMMpXRTsimulation' #Defines the output filename of results.
    simulation['version']="1.12"
    simulation['comment']='someMMpXRTsimulation' #This is just written in the figure as subtitle for convinience.
    simulation['num_processes']=1 #Number of processors to be used by the simulation.
    simulation['out_data_directory']='./datafiles/' #Where the ouptupt data are stored.
    simulation['DetectorXlim']=[]
    #How much rays should be calculated. The more the better, but longer.
    simulation['numraysB']=1e5 #Number of rays for the broadband simulation.
    simulation['numraysM']=1e5 #Number of rays for the monocrhomatic simulation.
    simulation['numraysE']=4 # Optional exponent setting. If numraysE>0, numraysB=(10**(numraysE) numraysM=(10**(numraysE-1)

    simulation['progressmod']=200 #after how much to update the progressbar
    simulation['outputdump']=1e8

    #Window nad pixels for figure of Point spread function [mm]. -1 lets the automatic work.
    simulation['PSFWindowX']=-1
    simulation['PSFWindowY']=-1
    simulation['PSFStepY']=-1
    simulation['PSFStepX']=-1

    simulation['non_central_PSFs']=0 #instead of broadband simulation, I will simulate a bunnch of PSFs

    #numerical parameters, default values should be ok for most cases.
    #When details of mossaic stuff at non-optimal angles are important, having higher values makes more precision, like e.g. width=30, numpoints=50 was used for mossaicity section of the CPC paper
    simulation['numerical_mossaic_phimap_width']=10
    simulation['numerical_mossaic_phimap_numpoints']=14
    simulation['numerical_intersect_halving']=0 #selects whcih algorithm is used for torus_line_intersect; 0-the standard, pretty fast; 1-'halving of interval': more robust, slower

    simulation['DetectorStepY']=-1
    simulation['DetectorStepX']=-1
### Crystal
    ## General
    crystal['d2']=4.00 #crystal spacing 2d [Angstrom]
       #old, wrong definitions:
        #crystal['radius_width']=1500 #Crystal radius along its width [mm] (dispersion plane) - defines range
       #crystal['radius_length']=100 #Crystal radius along its length [mm] (spatial focusing) - defines the geometry
    crystal['radius_l']=1e9 #Crystal radius of curvature along its length [mm] (in dispersion plane) - defines spectral range etc.
    crystal['radius_w']=1e9 #Crystal radius curvature along its width [mm] (spatial focusing) - defines the geometry
    crystal['length']=40 #Crystal length [mm]
    crystal['width']=25 #Crystal width[mm]

  ## Parameters for mossaic crystals
    crystal['mosaicity']=0 #Mosaicity (mosaic distribution spread) fwhm, [°].   Zero means that monocrystal is used.
    crystal['crystalliteRockingcurveWidth']=0e-4 #[rad]
    crystal['crystalPeakReflectivity']=1 #[-] Usually around 0.45 for HOPGs.

    crystal['thickness']=0 #How penetration of rays into crystals is done:
    #-1:  The exponential probability distribution is used, limited by maxThickness
    # 0:  Everything is reflected from the crystal surface
    # >0: Homogeneous depth distribution with given maximal this number stating the maximal depth [mm]

    crystal['penetrationDepth']=-1 # [mm] penetration depth of photons into the crystal, assuming exponential distribution; if set to -1, the reference is used.
    crystal['penetrationDepthMultiplier']=1
    crystal['maxThickness']=0 #real thickness of crystal if exponential distribution is used (thickness=-1)

    crystal['mosaicCrystal_penetration_depth_reference']=695e-3 #mm; measured or estimated penetration depth at energy specified below
    crystal['mosaicCrystal_penetration_depth_reference_energy']=8045 #eV; energy, where reference penetration depth is estimated
    crystal['mosaicCrystalTransmission']='C_700um_transmission.dat' #File with crystal material transmission as a function of x-ray energy, used to get mean penetration depth
    crystal['mosaicCrystalTransmission_thickness']=700e-3 #mm, thickness of sample whose transmission is tabelated in file 'mosaicCrystalTransmission'


  ## Parameters for monocrystals (non-mosaic)
    crystal['rockingCurveFWHM']=0 #[rad]
    crystal['integrated_reflectivity']=1 #[rad]
    # The codes assumes square rocking curve with above given width & integral.
    # The peak reflectivity is calculated as  integrated_reflectivity / rockingCurveFWHM.

### Geometry
    #Main distances [mm]. Positive value will be taken, -1 will make calculation for vonHamos geomtery:
    geometry['CrystalSource']=-1
    geometry['CrystalDetector']=-1
    geometry['defocusation']=1.00 #Multiplication factor for the Crystal-Detector distance.
    geometry['detectorOffset']=0  #Additive factor for the Crystal-Detector distance.
    geometry['detRot']=0#[°] rotation of detector. 0° mean it is perpendicular to incoming beam, positive number more suitble for vonHamos, -1° calculate the ideal von Hamos rotation
    geometry['ThBragg0']=-1; #[rad] Incidence angle of the central ray on the crystal. if set to -1, then it is calculated based on Bragg law.

    ## Detector. Those parameters does not influnece the simulation, only its evaluation
    geometry['detectorLength']=28
    geometry['detectorWidth']=-1; #-1 means automatic, otherwise [mm]
    geometry['detectorPxSize']=13e-3 #-1 means automatic, otherwise [mm]
    geometry['evaluation_width']=1  #[mm] Width of spectra selected for evaluation of spectral resolution


### Source
    source['EcentralRay']=8000 #Central energy of spectrometer. [eV]
    source['EmaxBandwidth']=1000 #Energy bandwidth which will be used to test the setup [eV].
    source['size']=0 # [mm] Uncertainity in the source position (i.e. source is cube with given size)

### This is end of user defining variables, follow imortatn code

    #internal variables:
    simulation['show_progress']=1
    simulation['collectLostBeams']=False

    ## simulation settings (configured by mmmxrt_spectrometer)
    source['secondBeamRatio']=0 #ratio - how much of second monoergetic beam is added.
    source['secondBeamEOffset']=10#eV
    source['rOffsetRatio']=0.0 #ratio of rayes whose origin is offset
    source['rOffset']=[0 ,0, 0] #offset of part of the beam given by previous value
    source['continuum']=False
    source['continuumMarks']=False#add a marks with
    source['continuumMarks_array']=[]
    source['continuumAdd']=False#add a little bit of continuum to the simuled x-ray spectrum
    source['continuumAddedRatio']=0.3#fraction of rays that will have that added continuum
    source['useBeamSpectrum']=False
    source['beamSpectrum']=''#array containing the spectrum

    source['divergenceXcut']=1#this makes the beam elliptical - use just to improve the efficiency of the simulation, might make the efficiency calculation wrong
    source['divergenceRing']=np.array([]) #Divergence will be ring-like with angular radius given by its positive value [rad]
    source['divergenceGrating']=-1
    source['divergenceMatrix']=[]
    source['divergenceGaussian']=False
    source['divergenceRectangular']=False
    source['divergenceAutomatic']=False
    source['divergenceX']=0
    source['divergenceY']=0
    source['divergenceFWHM']=-1

    source['do2DAngularResolutionTest']=False
    source['AngularGridRad']=0 # rad
    source['showspatial']=False
    source['show2Dspatial']=False
    source['showrealspatial']=False
    source['doAngularResolutionTest']=False


    #undocumented features
    crystal['variableD2']=False #if True, the 2d spacing is linearly variable (useful for ML), goverened by following parameter.
    crystal['d2Variation']= 0.0 #[Å/mm]
    crystal['gap']= 0 #mm ..horizontal gap in the crystal. Special feauture for SAXS mirror


    if not os.path.exists(simulation['out_data_directory']):
        os.mkdir(simulation['out_data_directory'])

    parameters={}
    parameters['source']=source
    parameters['geometry']=geometry
    parameters['simulation']=simulation
    parameters['crystal']=crystal

    return parameters


def load(p):
    """ Loads results and parameters saved by previous run of spectrometer()"""
    dira=p['simulation']['out_data_directory']
    name=p['simulation']['name']
    rrrs=pickle.load(open( dira+ "mmpxrt_results_"+name+"", "rb" ) )
    p=  pickle.load(open( dira+ "mmpxrt_parameters_"+name, "rb" ) )
    return rrrs,p



def phiToAngle(phi,tda,U,N):
    """ Calculates the angle alpha(phi), as described in the paper.

    Parameters
    ----------
        L : double[3]
            Vector of incident ray.

        phi : double
            angle defining where on circle around incident beam I am.

        tda :
            tan of desired angle from incident beam (aka radius of circle)

        U :
            ??
        N :
            ??
    Returns
    -------
        angle : alpha
    """
    axTh=np.array([1 ,np.sin(phi)*tda ,np.cos(phi)*tda])
    #axThv has an angle Theta from vector ax
    m=U.dot(axTh)
    angle=np.arccos(np.dot(N,m/np.linalg.norm(m)))
    #angle - angle between found m and angle of incidence
    return angle

def rotation_matrix(A,B):
# https://math.stackexchange.com/questions/180418/calculate-rotation-matrix-to-align-vector-a-to-vector-b-in-3d

    f=A
    t=B
    v = np.cross(f, t)
    u = v/np.linalg.norm(v)
    c = np.dot(f, t)
    h = (1 - c)/(1 - c**2)

    vx, vy, vz = v
    rot =np.array([[c + h*vx**2, h*vx*vy - vz, h*vx*vz + vy],
          [h*vx*vy+vz, c+h*vy**2, h*vy*vz-vx],
          [h*vx*vz - vy, h*vy*vz + vx, c+h*vz**2]])


    return(rot)


def getRightCrystalliteLorentz(L,N, Theta, Mozaicity,numerical_mossaic_phimap_width,numerical_mossaic_phimap_numpoints):
    """Finding the reflecting crystallite based on Lorentzian distribution.

    This functions selects any random crystallite which has the exact bragg
    angle theta with respect to direction of incidence, and its deviation from crystal
    surface is given by the lorentzian probability mosaic distribution.

    Parameters
    ----------
    L : double[3]
        Vector of incident ray.
    N : double[3]
        Normal vector of the crystal surface.
    Theta : double
        Bragg angle.
    Mozaicity : double
        Mosaicity of the crystal = crystallite angular spread [rad].

    Returns
    -------
    C : double[3]:
        Normal vector of the found reflecting crystallite.
    inte : double
        The probability integrated over all phis.
    """
    debug=False

#preparation
    Lnorm=L/np.linalg.norm(L)
    ax=np.array([1, 0, 0])
    divangle=np.pi/2-Theta#how much from L should I search the angle

    U=rotation_matrix(ax,Lnorm)

    N=N/np.linalg.norm(N)
    tda=np.tan(divangle)

## making rough angle map
# the set of all possible solutions of crystallites with ThBragg excatly
# correct with respect to incident beam makes a 'circle' around incident
# beam phi is shows a position on this circle.

# here I am checking what is the angle between crystallites on such circle
# and cyrstal normal, and already getting the probability according to
# Lorentzian distribution

#assuming Lorentzian distribution with FWHM = m
#gamma = HWHM

    gamma=Mozaicity/2
    pigamma=gamma*np.pi
    iis=np.arange(36)
    phis=iis*10/180*np.pi
    angles=np.zeros(36)
    for ii in iis:
        phi=phis[ii]
        angles[ii]=phiToAngle(phi,tda,U,N)
    b= np.argmin(angles)
    phibest=b*10
# ... and this is the phi, where alpha is closest to the crystal normal
    # this tells me where is the highest chance of being refleted, since assuming m<<ThetaBragg

# making finer angle map
    iis=np.arange(36)
    phis=(phibest+(iis-14)/2)/180*np.pi
    angles=np.zeros(36)
    for ii in iis:
        phi=phis[ii]
        angles[ii]=phiToAngle(phi,tda,U,N)
        #phis[ii]=phi
    b=np.argmin(angles)
    phibest2=phis[b]
# ... and this is the finer estimate of minimal angle phi

# making finest map, well centerd about peak, with size given by mozaicity
    numpoints=14 #orig
    numpoints=50 #orig
    numpoints=numerical_mossaic_phimap_numpoints
    FACTOR=10 #ORIGINAL SOLUTION
    FACTOR=30 #test
    FACTOR=numerical_mossaic_phimap_width #test
    iis=np.arange(2*numpoints)
    lorentzs=np.zeros(2*numpoints)
    angles=np.zeros(2*numpoints)
    spread=Mozaicity*FACTOR
    phis=(phibest2+ ((iis-numpoints)/numpoints*spread))
    for ii in iis:
        phi=phis[ii]
        angles[ii]=phiToAngle(phi,tda,U,N)
        phis[ii]=phi
        lorentzs[ii]=1/(pigamma*(1+((angles[ii])/gamma)**2))

    debug=0
    if (debug):
        phisg=phis/np.pi*180
#        plt.plot(phisg,angles/np.linalg.norm(angles),label='angle')
 #       plt.plot(phisg,lorentzs/np.linalg.norm(lorentzs),label='p(lorentz)')
        plt.plot(phisg,lorentzs,label='p(lorentz)')
        yl=plt.ylim()
        print(yl)
        plt.ylim(0,yl[1])
        plt.legend()
        plt.grid()

## find a good phi in the range, weighted by lorentzs (rejection sampling)
    phimin=phis[1]
    phiw=phis[np.size(phis)-1]-phis[1]

    inte=np.sum(lorentzs)*phiw/28;

    lorentzs=lorentzs/np.max(lorentzs)
    c=0
    C=None
    phi=-1
    while c<1000:
      phi=np.random.rand()*phiw+phimin
      y=np.random.rand()
      prob=np.interp(phi,phis,lorentzs)
      if prob>y: # done, send transformed phi
          axTh=np.array([1, np.sin(phi)*tda, np.cos(phi)*tda])
          m=U.dot(axTh)
          C=m
      #    print(c)
          break
      c=c+1

#if (debug),
#    phia=phi/pi*180
#    plot([phia phia],[0,1],'k-')
#end

    if phi==-1: #this never happened :)
        print('Lorentz failed')
        return np.nan

    return [C,inte]


def plane_line_intersect(n,V0,P0,P1):
    #from https://stackoverflow.com/questions/5666222/3d-line-plane-intersection
    # n: normal vector of the Plane
    # V0: any point that belongs to the Plane
    # P0: end point 1 of the segment P0P1
    # P1:  end point 2 of the segment P0P1
    w = P0 - V0
    u = P1-P0
    N = -np.dot(n,w)
    D = np.dot(n,u)
    sI = N / D
    I = P0+ sI*u
    return I

def plane_floor_line_intersect(P0,P1):
    #from https://stackoverflow.com/questions/5666222/3d-line-plane-intersection
    # n=[0,0,1]: normal vector of the Plane
    # V0=[0,0,0] any point that belongs to the Plane
    # P0: end point 1 of the segment P0P1
    # P1:  end point 2 of the segment P0P1
    w = P0
    u = P1-P0
    N = -1*P0[3]
    D = u[3]
    sI = N / D
    I = P0+ sI*u
    return I

def merge_rrr(rra,rrb):
    if rra==None:
        return rrb
    rrc={}
    rrc['E0s']=np.concatenate((rra['E0s'],rrb['E0s']))
    rrc['aois']=np.concatenate((rra['aois'],rrb['aois']))
    rrc['colores']=np.concatenate((rra['colores'],rrb['colores']))
    rrc['numrays']=rra['numrays']+rrb['numrays']
    rrc['effcnt']=rra['effcnt']+rrb['effcnt']
    rrc['effdet']=rra['effdet']+rrb['effdet']
    rrc['rayres']=np.concatenate((rra['rayres'],rrb['rayres']))
    return rrc

def update_progress(progress,maxi,style=0,barLength = 30):
    # https://stackoverflow.com/questions/3160699/python-progress-bar
     # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress >= maxi:
        progress = maxi
        status = "Done"
    block = int(round(barLength*progress/maxi))
    if style:
        yes="😋"
        no="😶"
    else:
        yes="*"
        no="-"
    text = "\r [{0}] {1:2.0f}/{2} {3}".format( yes*block + no*(barLength-block), progress,maxi, status)
    sys.stdout.write(text)
    sys.stdout.flush()


def update_progresses(progresses,maxi):
    # https://stackoverflow.com/questions/3160699/python-progress-bar
    barLength = 30 # Modify this to change the length of the progress bar
    status = ""
#    if progress >= maxi:
 #       progress = maxi
  #      status = "Done"
    text="\r"
    if np.mean(progresses) ==-2: #deactivating this
        text = text+" Done.                                         "
    else:
        for i,pr in enumerate(progresses):
            progress=pr
            if pr==-1:
                text = text+" done "
            else:
                block = int(round(barLength*progress/maxi))
                text = text+ "{:5.0f} ".format(progress)
    #text=text+"\r"
    sys.stdout.write(text)
    sys.stdout.flush()

def sphere_ray_intersect(sphere_centre, sphere_radius, ray_start,ray_direction):
    #"return: The ray t value of the first intersection point of the
    #ray with self, or None if no intersection occurs"""
    #taken from https://github.com/phire/Python-Ray-tracer/blob/master/sphere.py#L10
    hit = None
    q = sphere_centre - ray_start
    vDotQ = np.dot(ray_direction, q)
    squareDiffs = np.dot(q, q) - sphere_radius*sphere_radius
    discrim = vDotQ * vDotQ - squareDiffs
    if discrim >= 0:
        root = np.sqrt(discrim)
        t0 = (vDotQ - root)
        t1 = (vDotQ + root)
        if t0 < t1:
            hit = (t0, t1)
        else:
            hit = (t0, t1)
    p1 = ray_start+ray_direction*t0
    p2 = ray_start+ray_direction*t0
    return p2


def torus_ray_intersectElementwise(crystalRvSq,crystalRSq,crystalRv,crystalR,crystalCenterX,deepinCrystal, ray_start,ray_direction,crystalLength):
## FIND INTERSECTION OF RAY WITH CRYSTAL PLANE  (hlaving the interval, each call took 44ms)
    ##first, find "tF" : 't' of intersection with horizontal plane
    r0=ray_start
    v0=ray_direction
    tF=-1.*r0[2]/v0[2];
    #second, assume the intersection would be +-crystalLength/2 from this point
    mint=tF-crystalLength/2
    maxt=tF+crystalLength/2
    r00=r0[0]
    r01=r0[1]
    r02=r0[2]
    v00=v0[0]
    v01=v0[1]
    v02=v0[2]
    while ((maxt-mint)>1e-5):##this is the precision threshold in ~[mm]
       #1e-5 = 10nm .. should be sufficient
       t=mint+(maxt-mint)/2
       #r=r0+t*v0
       R0=r00+t*v00
       R1=r01+t*v01
       R2=r02+t*v02
       sqrt=(crystalRvSq-((R0-crystalCenterX)*(R0-crystalCenterX)))
       if sqrt<0:
           parzH=50 #too far from the crystal
       else:
           parzH=-1* math.sqrt(sqrt)  + crystalRv
       parzV=-1* math.sqrt(crystalRSq-(R1*R1)) + crystalR
       parz=parzH+parzV-deepinCrystal
       parz=min(parz,50)
       if (parz>R2):
           maxt=t
       else:
          mint=t
    r=np.array([R0,R1,R2])
    return r

def torus_ray_intersect(crystalRvSq,crystalRSq,crystalRv,crystalR,crystalCenterX,deepinCrystal, ray_start,ray_direction,crystalLength):
## FIND INTERSECTION OF RAY WITH CRYSTAL PLANE  (something like golden ratio, 12ms per run)
    #first, find "tF" : 't' of intersection with horizontal plane
    r0=ray_start
    v0=ray_direction
    tF=1.*r0[2]/v0[2]
    debug=0
    if debug:
        print(r0)
        print(v0)
    #second, assume the intersection would be +-crystalLength/2 from this point
    mint=tF-crystalLength/2
    maxt=tF+crystalLength/2
    r00=r0[0]
    r01=r0[1]
    r02=r0[2]
    v00=v0[0]
    v01=v0[1]
    v02=v0[2]
    t=tF
    maxIter=30
    precision=1e-5 #this means precision of 10μm, seems ok for tested applications
    i=0
    maxZ=100#maximal 'height' of crystal from floor. hard limit
    while (True):
       #r=r0+t*v0
       i=i+1
       R0=r00+t*v00
       R1=r01+t*v01
       R2=r02+t*v02
       if debug:
           print(i)
           print("X {:.0f}, Y {:.1f}, Z {:.0f}, t={:.0f}  ".format(R0,R1,R2,t))
       sqrt=(crystalRvSq-((R0-crystalCenterX)*(R0-crystalCenterX)))
       if sqrt<0:
           parzH=maxZ #too far from the crystal
       else:
           parzH=-1* math.sqrt(sqrt)  + crystalRv #how high is the crystal above the floor based on the radius along length
       if crystalRSq-(R1*R1)<0:#the intersection would be too far,
           if debug:
               print('step back, t={:.0f}, R1={:.0f}'.format(t,R1))
           t=0.8*t
           continue
           #return([0.,0.,0.])
       parzV=-1* math.sqrt(crystalRSq-(R1*R1)) + crystalR
       parz=parzH+parzV-deepinCrystal
       parz=min(parz,maxZ)
       if (abs(parz-R2)<precision): ##this is the precision threshold in ~[mm]
           if debug:
               print('well done, i={:.0f}'.format(i))
           break
       #otherwise, go to such t that I will be vertically at "parz"

       t=(parz-r02)/v02
       if debug:
           print("GO: parz {:.0f}, R2 {:.1f}, t={:.0f}  ".format(parz,R2,t))

       if i>maxIter:
           print('too much iterations in torus_rays_intersect')
           return([0.,0.,0.])
    r=np.array([R0,R1,R2])
    return r

def torus_ray_intersectVector(crystalRvSq,crystalRSq,crystalRv,crystalR,crystalCenterX,deepinCrystal, ray_start,ray_direction,crystalLength):
## FIND INTERSECTION OF RAY WITH CRYSTAL PLANE  (halving of interval, each call took about 70ms)
    #first, find "tF" : 't' of intersection with horizontal plane
    r0=ray_start
    v0=ray_direction
    tF=-1.*r0[2]/v0[2];
    #second, assume the intersection would be +-crystalLength/2 from this point
    mint=tF-crystalLength
    maxt=tF+crystalLength
    ia=0
    debug=0
    if debug:
        print('torus ray intersect')
        print(v0)
        print(mint)
        print(maxt)

    if np.abs(mint)<np.abs(maxt):
        mint=0
    else:
        maxt=0
    maxZ=100
    while ((maxt-mint)>1e-5):##this is the precision threshold in ~[mm]
       ia=ia+1
       #1e-5 = 10nm .. should be sufficient
       t=mint+(maxt-mint)/2
       r=r0+t*v0
       #parabola:      parz=(r(1)**2/a+r(2)**2/b )*c
       #if (geomTorus),
       #parzH=-1* (crystalRvSq-((r[0]-crystalCenterX)**2)**(1/2))  + crystalRv
  #     print("{:2.0f} {:2.0f} {:2.0f} {:2.0f}  ".format(crystalRvSq,r[0],crystalCenterX,crystalRv))
     #  pdb.set_trace()
       sqrt=(crystalRvSq-((r[0]-crystalCenterX)*(r[0]-crystalCenterX)))
       if sqrt<0:
           parzH=maxZ #too far from the crystal
       else:
           parzH=-1* math.sqrt(sqrt)  + crystalRv
       if crystalRSq-(r[1]*r[1])>0:
           parzV=-1* math.sqrt(crystalRSq-(r[1]*r[1])) + crystalR
       else:
           parzV=200
       parz=parzH+parzV-deepinCrystal
       parz=min(parz,maxZ)
       if (parz>r[2]):
           maxt=t
       else:
          mint=t
       if debug*0:
          print(t)
    if debug:
      print('done')
      print(r)
    return r

#@nb.njit(fastmath=True)
def mnorm(l):
    s = 0.
    for i in range(np.shape(l)[0]):
        s += l[i]**2
    return math.sqrt(s)


### Core

def spectrometer(p):
    """ This function makes the two raytracing tests of cyrstal spectrometer.

    Params:
        p : Dictionary of dictionaries of parameters.

    Returns:
        spectrorrr : Dictionary of rrr of both runs.
    """
    p['source']['continuumAdd']=True
    p['source']['continuumAddedRatio']=0.

    if p['source']['divergenceFWHM']<0:
        p['source']['divergenceAutomatic']=True
    p['simulation']['collectLostBeams']=False

    if p['simulation']['numraysE']>0:
        p['simulation']['numraysB']=round(10**(p['simulation']['numraysE']))
        p['simulation']['numraysM']=round(10**(p['simulation']['numraysE']-1))

    windowY=30

    p=geometry(p)
    sim=p['simulation']
    s=p['source']
    sg=p['sg']
    nump=sim['num_processes'];


    ## First run: broadband
    start = time.time()
    print( 'MMPXRT spectrometer ({:2.0f} cores)'.format(nump))

    print( 'Going to raytrace (broadband)')
    s['continuum']=True
    sg['numrays']=p['simulation']['numraysB']
    #s['rOffset']=[0,0,0]leave rOffset to be set by user
    sg['windowX']=10
    sg['windowY']=10

    if nump>1:
        sg['numrays']=int(np.round(sg['numrays']/nump))
        broadrrr = raytrace_multiprocess(p,nump)
    else:
        broadrrr = raytrace(p,None,None)

    end = time.time()

    ## Second run: Monochromatic
    print( '\nGoing to raytrace (monochromatic)')
    s['continuum']=False
    p['source']['continuumMarks']=False
    s['secondBeamRatio']=0
    s['showrealspatial']=True
    s['rOffsetRatio']=0.2
    s['useBeamSpectrum']=0
    rOff=0.1
    s['rOffset']=[np.sin(sg['ThBragg'])*rOff, 0,np.cos(sg['ThBragg'])*rOff]
    sg['numrays']=p['simulation']['numraysM']
    if nump>1:
        sg['numrays']=int(np.round(sg['numrays']/nump))
        monorrr = raytrace_multiprocess(p,nump)
    else:
        monorrr = raytrace(p,None,None)

    print("\n\n Spectrometer took: "+str(np.round(end-start))+" s");

    spectrorrr={}
    spectrorrr['elapsedTime']=end-start
    spectrorrr['mono']=monorrr
    spectrorrr['broad']=broadrrr

    fn=p['simulation']['out_data_directory']  +'mmpxrt_results_' +p['simulation']['name']
    pickle.dump( spectrorrr, open( fn, "wb" ) )
    fn=p['simulation']['out_data_directory']  +'mmpxrt_parameters_' +p['simulation']['name']
    pickle.dump( p, open( fn, "wb" ) )

    return spectrorrr


def spectrometer_imager(p):
    """ This function makes the two raytracing tests of cyrstal spectrometer.

    Params:
        p : Dictionary of dictionaries of parameters.

    Returns:
        spectrorrr : Dictionary of rrr of both runs.
    """
    p['source']['continuumAdd']=True
    p['source']['continuumMarks']=False
    p['source']['continuumAddedRatio']=0.

    if p['source']['divergenceFWHM']<0:
        p['source']['divergenceAutomatic']=True
    p['simulation']['collectLostBeams']=False

    if p['simulation']['numraysE']>0:
        p['simulation']['numraysB']=round(10**(p['simulation']['numraysE']))
        p['simulation']['numraysM']=round(10**(p['simulation']['numraysE']-1))

    windowY=30
    p=geometry(p)
    sim=p['simulation']
    s=p['source']
    sg=p['sg']
    nump=sim['num_processes'];


    ## First run: broadband
    start = time.time()
    print( 'MMPXRT spectrometer ({:2.0f} cores)'.format(nump))

    print( 'Going to raytrace (broadband)')
    s['continuum']=True
    sg['numrays']=p['simulation']['numraysB']
    sg['windowX']=10
    sg['windowY']=10
    s['showrealspatial']=0
    s['show2Dspatial']=True

    if nump>1:
        sg['numrays']=int(np.round(sg['numrays']/nump))
        broadrrr = raytrace_multiprocess(p,nump)
    else:
        broadrrr = raytrace(p,None,None)

    end = time.time()

    ## Second run: Monochromatic
    print( '\nGoing to raytrace (monochromatic)')
    s['continuum']=False
    s['secondBeamRatio']=0
    #s['showrealspatial']=True
    s['show2Dspatial']=True
    s['useBeamSpectrum']=0
    sg['numrays']=p['simulation']['numraysM']
    if nump>1:
        sg['numrays']=int(np.round(sg['numrays']/nump))
        monorrr = raytrace_multiprocess(p,nump)
    else:
        monorrr = raytrace(p,None,None)

    print("\n\n Spectrometer took: "+str(np.round(end-start))+" s");

    spectrorrr={}
    spectrorrr['elapsedTime']=end-start
    spectrorrr['mono']=monorrr
    spectrorrr['broad']=broadrrr

    fn=p['simulation']['out_data_directory']  +'mmpxrt_results_' +p['simulation']['name']
    pickle.dump( spectrorrr, open( fn, "wb" ) )
    fn=p['simulation']['out_data_directory']  +'mmpxrt_parameters_' +p['simulation']['name']
    pickle.dump( p, open( fn, "wb" ) )

    return spectrorrr



###############################################
def geometry(p):
    g=p['geometry']
    c=p['crystal']
    s=p['source']

    ## Finding an ideal setup in von Hamos Geometry
    if g['ThBragg0']>0:
        ThBragg=g['ThBragg0']
    else:
        ThBragg=np.arcsin(12398/p['source']['EcentralRay']/p['crystal']['d2'])
    crystalCenterX = c['radius_w'] / np.tan(ThBragg)
    Edist=crystalCenterX/np.cos(ThBragg)
    Edist=Edist*p['geometry']['defocusation']
    Edist_dect=Edist+p['geometry']['detectorOffset']

    if (p['geometry']['detRot']==-1): #van Hamos setting
        p['geometry']['detRot']=90-ThBragg/np.pi*180
    detRot=p['geometry']['detRot']


#    if exist('crystalROver'), #undocumented feature :)
     #   crystalR=crystalROver
    #end

    ## Using custom geometry if defined
    if (g['CrystalSource']>0):
        Edist=g['CrystalSource']
    if (g['CrystalDetector']>0):
        Edist_dect=g['CrystalDetector']

    ## writing geomtery in "E" variables
    Esource=np.array([0, 0, 0])
    Ecrystal=np.array([Edist,0,0])
    EcrystalAngle=ThBragg#between crystal and X-axis
    tempAngle=ThBragg
    Edetector=np.array([Edist+np.cos(2*tempAngle)*Edist_dect,0,np.sin(2*tempAngle)*Edist_dect])
    EdetectorAngle=ThBragg*2 #angle between detector and Z axis - settting to be perpendicular to the beam

    EdetectorAngle=EdetectorAngle + detRot/180*np.pi

    ## Transform into "S" variables & "S" cooridnate system (where crystal is lying along the XY plane)
    R = np.array([[np.cos(-1*EcrystalAngle), 0, -np.sin(-1*EcrystalAngle)] , [0, 1, 0] , [np.sin(-1*EcrystalAngle),  0, np.cos(-1*EcrystalAngle)]])
    Ri=np.linalg.inv(R)
    TransMatrix=R
    ScrystalTemp=Ecrystal.dot(Ri)
    O = np.array([0, 0, -1*ScrystalTemp[2]])
    Rotation=R
    Translation=O
    sg={}
    sg['Edist']=Edist
    sg['Edist_dect']=Edist_dect
    sg['Ssource']=Esource.dot(Ri)+O
    sg['Scrystal']=Ecrystal.dot(Ri)+O
    sg['Sdetector']=Edetector.dot(Ri)+O
    sg['SdetectorAngle']=EdetectorAngle-EcrystalAngle
    sg['ThBragg']=ThBragg

    ## Automatic Divergence: getting the observation angle where I see crystal
    if s['divergenceAutomatic']:
       safety_factor=1.2
       s['divergenceY']= np.arctan(c['width']/2/Edist) * safety_factor*2
       L2=c['length']/2
       x=(Edist**2 + (L2)**2 - 2*Edist*L2 * np.cos(ThBragg))**0.5
       s['divergenceX']= np.arcsin(np.sin(ThBragg)/x*L2) * safety_factor *2
       s['divergenceRectangular']=True


    ## Rewrite into old structures
    crystalCenterX=sg['Scrystal'][0]


    detX=sg['Scrystal'][0]
    sg['detn']=np.array([-1*np.cos(sg['SdetectorAngle']), 0, -1*np.sin(sg['SdetectorAngle'])])

    if (c['thickness']==-1):  #defining the depth distribution
        if (c['penetrationDepth']==-1):
            #finding the penetrationdepth
            tabl=ascii.read(c['mosaicCrystalTransmission'])
            xh=tabl['col1']
            transh=tabl['col2']
            #clength=700e-3 #mm - thickness of the table
            clength=c['mosaicCrystalTransmission_thickness']
            muh=-1*clength/np.log(transh);  #absorption coefficient as a function of energy (xh)

            muh_at_reference = np.interp(c['mosaicCrystal_penetration_depth_reference_energy'],xh,muh)
            #mue=muh/1.05*696e-3;        # original non-flexible way
            mue=muh/muh_at_reference*c['mosaicCrystal_penetration_depth_reference'] #absorption coefficient scaled to the mosaic reference

            mu=np.interp(s['EcentralRay'],xh,mue) #interpolating mue to current central energy
            mu_e=mu*np.sin(ThBragg)/2 #effective mu (i.e. perpendicular to the surface)
            mu_e=mu_e*c['penetrationDepthMultiplier']
            c['penetrationDepth']=mu_e
        else:
            c['penetrationDepth']=c['penetrationDepth']*c['penetrationDepthMultiplier']

    p['sg']=sg
    return p

#@profile
def raytrace(p,q,progress):
    """Core of the mmpxrt crystal raytracing code.

    Written by Michal Smid, 2016-19, IoP ASCR, HZDR

    Parameters:
        p : dict
            Dictionary of dictionaries of input parameters.
        q : multiprocess.queue
            Queue where to put results, can be None if running on single processor.

    Returns:
        raytraceres : double[numrays,3,3]
            trajectories of found rays

            raytraceres(i,a,r):

            `i` is the index of the ray:  1..numrays

            `a` refers to point: 0-source, 1-reflection at crystal, 2-intersection with detector

            `r` is the coordinate 0-x, 1-y. 2-z

    """
    #extracting variables
    g=p['geometry']
    c=p['crystal']
    s=p['source']
    sim=p['simulation']
    sg=p['sg']

    showProgress=sim['show_progress']
    numrays=np.int(sg['numrays'])
    progressmod=np.int(min(sim['progressmod'],np.round(numrays/600)))
    if progressmod==0:
        progressmod=1

    piH=np.pi/2
    crystalMozaicity=c['mosaicity']/2/180*np.pi#half spread..the crystallites are (uniformly) distributed between -Moz...+Moz [rad]
    #initrT=[0 0 sourceZ 1]
    initrT=sg['Ssource']
    crystalRvSq=c['radius_l']**2
    crystalRSq=c['radius_w']**2
    crystalR=c['radius_w']
    crystalRv=c['radius_l']
    EmaxBand=s['EmaxBandwidth']
    collectLostBeams=sim['collectLostBeams']

    #rayres--trajectories of rays (rayi, [init, reflection, detection],[x y z])
    rayres=np.full((numrays,3,3),np.nan);

    if collectLostBeams:
        lostbeams=np.zeros((numrays,3),float)
    #colors of beam, artifically added, 0-no, 1-r, 2-g,3-b
    colores=np.zeros(numrays,float)
    aois=np.zeros(numrays,float)
    lostReason=np.zeros(10,float)
    E0s=np.zeros(numrays,float)
    #1 using crystaldistribution & ray penetrate deeper then
    #crystalMaxThickness
    #2  not hit the crystal
    #3  AOI not within rcw (monocrystal)
    #4  Mozaicity: no suitable crystallite
    i=0
    lbi=1
    throughi=0
    effcnt=0
    effdet=0
    bDxH=s['divergenceX']/2
    bDyH=s['divergenceY']/2
    rOffsetRatio=s['rOffsetRatio']
    crystalCenterX=sg['Scrystal'][0]
    crystalWidth=c['width']
    crystalDistribution=c['penetrationDepth']
    d2=c['d2']
    rcwh=c['rockingCurveFWHM']/2
    crystalLength=c['length']
    crystalMinX=crystalCenterX-c['length']/2
    crystalMaxX=crystalCenterX+c['length']/2
    crystalliteRockingcurveWidth=c['crystalliteRockingcurveWidth']
    ThBragg=sg['ThBragg'];
    EcontAdd=s['EcentralRay']-s['EmaxBandwidth']/2
    divRing=s['divergenceRing']
    numerical_mossaic_phimap_width=sim['numerical_mossaic_phimap_width']
    numerical_mossaic_phimap_numpoints=sim['numerical_mossaic_phimap_numpoints']
    intersect_halving=sim['numerical_intersect_halving']
    spatialoffset=False
    totati=0
    totgol=0
    rOffset=np.linalg.norm(p['source']['rOffset'])
    #finding the total optimal probability
    N=[0,0,1]
    L=[np.cos(ThBragg),0,np.sin(ThBragg)]
    if crystalMozaicity>0:
        a=getRightCrystalliteLorentz(L,N,ThBragg,crystalMozaicity,numerical_mossaic_phimap_width,numerical_mossaic_phimap_numpoints)
        peak_integrated_reflectivity=a[1]

    #print(progressmod)
    #for iii=1:numrays,   # THE MAIN CYCLE
    iii=0
    while True:
        iii=iii+1
#        print("{:.0f}     - {:.0f}".format(iii,i))
        if iii>1000 and i==0:
            break
        effbeam=0  #this determines which beam is used for efficiency calculations

        if progress != None:
            progress.value=i
        else:
            if showProgress and np.mod(i,progressmod)==0:
                update_progress(i,numrays)


## DEFINE RAY
        r0=initrT
        if s['size']>0:
            off=(np.random.rand(3)-0.5)*s['size']
            r0=r0+off

## ANGULAR PROPERTIES
        if (s['do2DAngularResolutionTest']):#Do the test for SAXS
        #preset       AngularGridRad=6e-3#rad

            #Random:   dThY=AngularGridRad*(floor(random.random(1)*5)-2)
        #       dThX=AngularGridRad*(floor(random.random(1)*5)-2)
        #ordered
               dThX=(mod(iii,3)-1)
               dThY=(floor( mod(iii,9)/3)-1)
               dThX=s['AngularGridRad']*dThX
               dThY=s['AngularGridRad']*dThY

        else :
#taken out on 21.10.2020            if (s['doAngularResolutionTest']):
#               dThX=0
               #AngularTest=6e-3#rad
               #AngularTest=s['AngularGridRad']
               #if (random.random()<0.5):
                   #dThY=-1*AngularTest
               #else:
                   #dThY=AngularTest
         #   else : #Divergent beam
                if (s['divergenceGaussian']):
                    sigma=s['divergenceFWHM']/2.355
                    rad=normrnd(0,sigma)
                    phi=random.random()*2*np.pi
                    dThX=np.sin(phi)*rad*s['divergenceXcut']
                    dThY=np.cos(phi)*rad
                elif (s['divergenceRectangular']):
                    dThX=random.random()*s['divergenceX']-bDxH
                    dThY=random.random()*s['divergenceY']-bDyH
                    if (s['doAngularResolutionTest']):
                        dThY=np.abs(dThY)
                elif (s['divergenceMatrix']!=[]):
                    rect=s['divergenceMatrix'][0]
                    rotation=s['divergenceMatrix'][1]
                    saxs_spline=s['divergenceMatrix'][2]
                    #saxs=saxs/np.max(saxs)
#                    sx=np.shape(saxs)[0]
 #                   sy=np.shape(saxs)[1]
                    minThX=rect[0]
                    wideThX=rect[1]
                    minThY=rect[2]
                    wideThY=rect[3]
                    #from scipy.interpolate import RectBivariateSpline
                    #interp_spline = RectBivariateSpline(y, x, Z)
                    while True:
#                        rx=np.random.random_integers(0,sx-1)
 #                       ry=np.random.random_integers(0,sy-1)
                        rx=np.random.random()*wideThX+minThX
                        ry=np.random.random()*wideThY+minThY

                        val=saxs_spline(rx,ry)
                        if np.random.rand()<val:
                            break
#                    print('a')
 #                   print([rx,ry])
                    if rotation!=0:
                        r=(rx**2 + ry**2)**0.5
                        phi=np.arctan2(rx,ry)
                        nphi=phi+rotation
                        rx=r*np.sin(nphi)
                        ry=r*np.cos(nphi)
                    dThX=rx
                    dThY=ry
  #                  print('b')
   #                 print([dThX,dThY])
                elif np.size(divRing)>0 :
                    if s['divergenceGrating']>0 :  #grating
                        if np.size(divRing)>1:
                            dri=np.int(np.floor(random.random()*np.size(divRing)))
                            drr=divRing[dri]
                        else:
                            drr=divRing
                        phi=s['divergenceGrating']/180*np.pi
                        dThX=np.sin(phi)*drr
                        dThY=np.cos(phi)*drr
                    else:   #rings
                        if np.size(np.shape(divRing))==2: #assuming there is a spectrum
                            minE=divRing[0,0]
                            maxE=divRing[0,np.shape(divRing)[1]-1]
                            Er=0
                            while True:
                                Er=np.random.random()*(maxE-minE)+minE
                                pEr=np.interp(Er,divRing[0,:],divRing[1,:])
                                if random.random()<pEr:
                                    break
                            drr=Er
                        else: #just sharp rings
                            if np.size(divRing)>1:
                                dri=np.int(np.floor(random.random()*np.size(divRing)))
                                drr=divRing[dri]
                            else:
                                drr=divRing
                        phi=random.random()*2*np.pi
                        dThX=np.sin(phi)*drr
                        dThY=np.cos(phi)*drr
                else:#default: sharp circular divergence profile
                    bDy=s['divergenceFWHM']  #rad
                    bDx=s['divergenceFWHM']*s['divergenceXcut']
                    dThX=random.random()*bDx-bDx/2
                    dThY=random.random()*bDy-bDy/2
                    while (dThX**2+dThY**2)**0.5>s['divergenceFWHM']/2:
                        dThX=random.random()*bDx-bDx/2
                        dThY=random.random()*bDy-bDy/2

        v0=np.array([np.cos(ThBragg-dThX), np.sin(dThY), -1*np.sin(ThBragg-dThX)])
        if v0[0]<0:
            continue

## POSITION OF THE SOURCE
        if (s['showrealspatial']):
            spatialoffset=False
            effbeam=1
            if(random.random()<rOffsetRatio):
                r0=r0 + s['rOffset']
                spatialoffset=True
                effbeam=0
        else:
            if (s['show2Dspatial']):
                rr=random.random()
                spatialoffset=False
                if(rr<0.333):
                   r0=r0 + np.array([np.sin(ThBragg)*rOffset, 0,np.cos(ThBragg)*rOffset])
                else:
                   if(rr<0.666):
                       r0=r0 + np.array([0, rOffset, 0])
            else:
               spatialoffset=False

## SPECTRUM OF THE SOURCE
        if (s['useBeamSpectrum']):
                beamSpectrum=s['beamSpectrum']
                minE=beamSpectrum[0,0]
                maxE=beamSpectrum[0,np.shape(beamSpectrum)[1]-1]
                Er=0
                while True:
                    Er=np.random.random()*(maxE-minE)+minE
                    pEr=np.interp(Er,beamSpectrum[0,:],beamSpectrum[1,:]);
                    if random.random()<pEr:
                        break
                E0=Er
#                E0=8980
                contAddNow=1
        elif s['continuumMarks']:
            if random.random()<0.0: #1000 eV broad continuum around centralRay
                E0=random.random()*800-400 +s['EcentralRay']
            else:
                marknum=np.size(p['source']['continuumMarks_array'])
                markind=np.random.randint(marknum)
                E0=p['source']['continuumMarks_array'][markind]
                contAddNow=1

        elif (s['continuum']):
                E0=np.random.rand()*EmaxBand+EcontAdd
                contAddNow=1

        else:        #default - mono or dichromatic
            if spatialoffset or (random.random()>s['secondBeamRatio']):
                E0=s['EcentralRay']#energy of the photon
            else:
                E0=s['EcentralRay']+s['secondBeamEOffset']

            if (s['continuumAdd']) and (random.random()<s['continuumAddedRatio']):
                E0=random.random()*1000-500 +s['EcentralRay']
                contAddNow=1
                effbeam=0
            else:
                contAddNow=0
                effbeam=1

        if (effbeam):
            effcnt=effcnt+1

## FIND HOW DEEP IN THE CRYSTAL THE RAY WILL REFLECT

        res=10
        if c['thickness']==0:
            deepinCrystal=0
        else:
            if c['thickness']==-1:#use crystalDistritubtion
                deepinCrystal=c['maxThickness']+1
                while (deepinCrystal>c['maxThickness']):
                    deepinCrystal=np.random.exponential(crystalDistribution)
            else:
                deepinCrystal=random.random()*crystalThickness

## FIND INTERSECTION OF RAY WITH CRYSTAL PLANE
        #print(deepinCrystal*1e3)
        if intersect_halving:
            r=torus_ray_intersectVector(crystalRvSq,crystalRSq,crystalRv,crystalR,crystalCenterX,deepinCrystal, r0,v0,crystalLength)
        else:
            r=torus_ray_intersect(crystalRvSq,crystalRSq,crystalRv,crystalR,crystalCenterX,deepinCrystal, r0,v0,crystalLength)

## AM I ON THE CRYSTAL?
        if (r[0]<crystalMinX) or (r[0]>crystalMaxX) or (abs(r[1])>crystalWidth/2):#outofcrystal
            if (collectLostBeams):
                lostbeams[lbi,:]=rrockingCurveFWHM
            lbi=lbi+1
            lostReason[2]=lostReason[2]+1
            continue
        if c['gap']> 0:
            if (abs(r[1])<c['gap']/2):
                if (collectLostBeams):
                    lostbeams[lbi,:]=rrockingCurveFWHM
                lbi=lbi+1
                lostReason[2]=lostReason[2]+1
                continue

#GET NORMAL ANGLE AT CRYSTAL:
           #von Hamos
#           if (geomVonHamos):
#                dzdx=0
#                dzdy=1*r(2)/(crystalR**2-r(2)**2)**(1/2)
#             if (geomFlat),
#                dzdx=0
#                dzdy=0
#            if (geomRowland),
##                dzdx=1*(r(1)-crystalCenterX)/(crystalR**2-(r(1)-crystalCenterX)**2)**(1/2)
##                dzdy=0
#            if (geomTorus),
        dzdx=1*(r[0]-crystalCenterX)/(crystalRv**2-(r[0]-crystalCenterX)**2)**(1/2)
        dzdy=1*r[1]/(crystalR**2-r[1]**2)**(1/2)

        N=np.array([-1*dzdx, -1*dzdy, 1])#target normal vector at intersection
        N=N/mnorm(N)
        #L=-1*v0(1:3)#assuming v0 is already normalized
        L=-1/mnorm(v0)*v0#assumption was wrong, renormalize
        aoi=piH-np.arccos(np.dot(L,N))#angle of incidence
        aois[i]=aoi

## INTERACTION WITH CRYSTAL
        if c['variableD2']:
            dX=r[0]-crystalCenterX
            d2Change=dX*d2Variation #Å
            d2loc= d2+d2Change
            braggTheta=np.arcsin(12398/E0/d2loc)
        else:
            braggTheta=np.arcsin(12398/E0/d2)
        ## Reflect from non-mosaic crystal
            if (crystalMozaicity==0):

                  if abs(aoi-braggTheta)<(rcwh):
                     R=2*(np.dot(N,L)*N)-L#vector of reflected ray
                  else:
                    colores[i]=0
                    if (collectLostBeams):
                        lostbeams[lbi,:]=r
                    lbi=lbi+1
                    lostReason[3]=lostReason[3]+1
                    continue
            else:  ## play with MOZAICITY ISSUES
                A=getRightCrystalliteLorentz(L,N,braggTheta,crystalMozaicity,numerical_mossaic_phimap_width,numerical_mossaic_phimap_numpoints)
                Nc=A[0]
                inte=A[1]
                probability=inte/peak_integrated_reflectivity; #probability that some suitable crystallite is here.
#                if np.abs(aoi-braggTheta)<crystalMozaicity:
                if np.random.rand()<probability:
                    #i.e. I have found good crystallite
                    #I assume the AOI is exactly as I need
                    #Nc=getRightCrystalliteLorentz(L,N,braggTheta,crystalMozaicity)
                    if np.isnan(Nc).any():#there is no suitable crystallite ... this does not happen with the new "getRightCrystalliteLorentz"
                        colores[i]=0
                        if (collectLostBeams):
                            lostbeams[lbi,:]=[r, 0]
                        lbi=lbi+1
                        lostReason[4]=lostReason[4]+1
                        continue
                    Nc=Nc/np.linalg.norm(Nc)
                    if c['crystalliteRockingcurveWidth']>0:#randomizing the crystallite angle little bit
                        #too lazy to calculate a precise random angle and then
                        #rotation of the normal. Just randomizing the point
                        #crystalliteRockingcurveWidth [rad]
            #            randOffset=random.random(3,1)*crystalliteRockingcurveWidth/2#since Nc is unit vector, adding this will somehow rotate it by the angle
                        #better way - rotation around Y and Z axis
                        rotY=(random.random()*crystalliteRockingcurveWidth)-crystalliteRockingcurveWidth/2
                        rotX=(random.random()*crystalliteRockingcurveWidth)-crystalliteRockingcurveWidth/2
        #                rotX=rotY
                        Ry = np.matrix([[np.cos(rotY) ,0 ,np.sin(rotY)],[0, 1, 0],[  -1*np.sin(rotY) , 0 ,np.cos(rotY)]])
        #                Rz = [np.cos(rotZ) -1*np.sin(rotZ) 0  np.sin(rotZ)  np.cos(rotZ) 00 0 1]
                        Rx = np.matrix([[1, 0, 0],[ 0, np.cos(rotX), -1*np.sin(rotX)] , [0, np.sin(rotX) , np.cos(rotX)]])
                        Nc=Ry.dot(Rx).dot(Nc)
        #                Nc=Nc+randOffset
                        Nc=(Nc)/np.linalg.norm(Nc)#renormalizing
                        Nc=np.squeeze(np.asarray(Nc))
                    R=2*(np.dot(Nc,L)*Nc)-L#vector of reflected ray
                    colores[i]=1
                else: #loosing the beam due to too far from optimal angle
                    R=np.nan
                    colores[i]=0
                    if collectLostBeams:
                        lostbeams[lbi,:]=[r, 0]
                    lbi=lbi+1
                    lostReason[5]=lostReason[5]+1
                    continue

        #COLORING
        if (E0==s['EcentralRay'])or (s['useBeamSpectrum']):
           colores[i]=1
        else:
           colores[i]=2
        if (s['continuumAdd'] and (contAddNow)or(s['continuum'])):
           colores[i]=4

        E0s[i]=E0
        if s['showspatial']:
            if v0[1]>0:
                colores[i]=3
        if s['showrealspatial']:
           if spatialoffset:
               colores[i]=3

            ## INTERSECTION WITH DETECTOR
            #finding the place
            #now: r = intersection with crystal
            # R = vector of reflected ray

        det=plane_line_intersect(sg['detn'],sg['Sdetector'],r,r+100*R)
        rayres[i,2,:]=det

        if effbeam:
            effdet=effdet+1

        if i==numrays-1:
            break
            #storing values
        rayres[i,0,:]=r0#  Initial ray position
        rayres[i,1,:]=r### Intersection of crystal & ray
        i=i+1

        if np.mod(i,sim['outputdump'])==0:
            print('Dumping the data')
            print('')
 #           fn=p['simulation']['out_data_directory']  +'mmpxrt_dump_' +p['simulation']['name'] + '_rays=' +i
#            pickle.dump( rayres, open( fn, "wb" ) )
            fn=p['simulation']['out_data_directory']  +'mmpxrt_results_' +p['simulation']['name']
            pickle.dump( rayres, open( fn, "wb" ) )
            fn=p['simulation']['out_data_directory']  +'mmpxrt_parameters_' +p['simulation']['name']
            pickle.dump( p, open( fn, "wb" ) )

    if progress != None:
        progress.value=-1
    else:
        if showProgress :
            update_progress(numrays,numrays)
    detrays=i
    ratio=i/lbi

    raytraceres={}
    raytraceres['effdet']=effdet
    raytraceres['effcnt']=effcnt
    raytraceres['rayres']=rayres
    raytraceres['aois']=aois
    raytraceres['E0s']=E0s
    raytraceres['numrays']=numrays
    raytraceres['colores']=colores
    raytraceres['lostReason']=lostReason
    #print(lostReason)
#    print("TOTGOL" +str(totgol))
    if q!=None:
        q.put(raytraceres)
    #rrr=np.append(rrr,2)
    #rrr=merge_rrr(rrr,raytraceres)
#    print ("raytrace done" )

    return raytraceres


def raytrace_multiprocess(p,num_threads):
    """Runs the raytrace on multiple processors."""
    starttime = time.time()
    processes = []
    rrr=None
    q = multiprocessing.Queue()
    prs=[]
    print ("Starting "+str(num_threads)+ " process, each going to do "+str(p['sg']['numrays'])+" rays")
    for i in range(0,num_threads):
        #https://medium.com/@urban_institute/using-multiprocessing-to-make-python-code-faster-23ea5ef996ba
        p['simulation']['show_progress']=(i==num_threads-1)
#        print (" starting process # "+str(i))
        progress= multiprocessing.Value('i',0)
        prs.append(progress)
        pr = multiprocessing.Process(target=raytrace,args=(p,q,progress))
        processes.append(pr)
        pr.start()


    got=0
    progs=np.zeros(num_threads)
    while got<num_threads:

        for i in np.arange(num_threads):
            progress=prs[i]
            progs[i]=progress.value
        #print(progs)
        update_progresses(progs,10)
        time.sleep(3)
        #update_progress(progress.value,10)
        if q.qsize()>0:
#            print (" getting results no."+str(got))
            rrr=merge_rrr(rrr,q.get())
            got=got+1

    progs=progs*0-1
    update_progresses(progs,10)
    for process in processes:
        process.join()

    return rrr






### Evaluation & visualization

def spectrometer_evaluate(p,spectrorrr):
    """ Gets the most useful data from previous spectreometer raytracing.

    This function should be called after spectrometer(). It adds an `evalu` dictionary
    to `p` with some of the numeral parameters, and prints out a beautiful summary image.

    Params:
        p : Dictionary of dictionaries of parameters.
        spectrorrr : result of spectrometer().

    """
    so=p['source']
    c=p['crystal']
    sg=p['sg']
    broad_rrr=spectrorrr['broad']
    mono_rrr=spectrorrr['mono']

    elapsedTime=spectrorrr['elapsedTime']
    evaluateCont(p,broad_rrr)
    ev=p['evalu']

    fig= plt.figure(figsize=(19.20,12.08))
    #ax=plt.subplot(2,4,1)
    ax = fig.add_subplot(241)
    drawSideView(p,broad_rrr,ax)
    plt.title('Geomtery (side)')


    ax = fig.add_subplot(242)
    showDispersion(p,broad_rrr,ax,True)
    plt.title('Dispersion')


    ax = fig.add_subplot(245)
    drawDetectorStripes(p,broad_rrr,ax,0)
    plt.title('Detector image')

    # verified numbers:
    nl='\n'
    #nl='\\\\'
    s=' \t'

    # geometry recap
    ii=r''
    headerfont='\mathbf'
    headerfont='\mathfrak'
    headerfont='\mathcal'

    ii=ii+ '$\mathrm{\mathbb{\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/Mmpxrt \/\/v.'+ p['simulation']['version'] +' }}$'+ nl
    ii=ii+ '$\mathbf{'+ p['simulation']['name'] +' }$'+ nl
    ii=ii +p['simulation']['comment']+ nl
    now = datetime.now()
    dt_string = now.strftime("%d.%m.%Y, %H:%M")
    ii=ii +'run on '+ dt_string + nl+nl
    ii=ii +'number of rays:  {:2.0g} + {:2.0e}'.format(broad_rrr['numrays'], mono_rrr['numrays']) + nl
    if (elapsedTime>300):
        ii=ii +'time:  {:2.0f} min., {:2.0f} r/s'.format(elapsedTime/60,(broad_rrr['numrays']+mono_rrr['numrays'])/elapsedTime) + nl
    else:
        ii=ii +'time:  {:2.0f} s,  {:2.0f} r/s'.format(elapsedTime,(broad_rrr['numrays']+mono_rrr['numrays'])/elapsedTime) + nl


    ii=ii +nl+'$'+headerfont+'{\/\/Geometry}$' +nl
    ######################################
    ii=ii+ '$d_{{{{SC}}}}$:  {:2.2f}'.format(sg['Edist'])+ ' mm'+ nl
    ii=ii+ '$d_{{{{CD}}}}$:  {:2.2f}'.format(sg['Edist_dect'])+ ' mm' +nl
    ii=ii +'$\\theta_{{{{Bragg}}}}$ :  {:2.2f}'.format(sg['ThBragg']/np.pi*180) +'$^\\circ$' +nl
    ii=ii +'magnification:   {:2.2f}'.format(sg['Edist_dect']/sg['Edist'])+ '' +nl
    ii=ii +'crystal size:   {:2.0f} X {:2.0f} mm'.format(c['length'],c['width'])+ '' +nl
    ii=ii +'crystal radii:   {:2.2e} X {:2.2e} mm'.format(c['radius_l'],c['radius_w'])+ '' +nl


    ii=ii+ nl+ "$"+headerfont+'{\/\/Energy\/\/range}$'+ nl
    ######################################
    ii=ii +'central E:  {:2.0f}'.format(so['EcentralRay'])+  ' eV '+ nl
    ii=ii +'E range max.:  {:2.0f}'.format(ev['Erangemax'])+ ' eV ' +nl
    ii=ii+ '  i.e. reflecting rays in range:  {:2.0f}'.format(ev['Erangemaxmin'])+ ' - {:2.0f}'.format(ev['Erangemaxmax']) +' eV '+ nl
    ii=ii +'E range fwhm:  {:2.0f}'.format(ev['ErangeFWHM']) +' eV '+ nl
    ii=ii+ 'E range on detector:  {:2.0f}'.format(ev['ErangeDetected'])+ ' eV '+ nl

    ii=ii+ nl
    ii=ii +'horizontal spread fwhm:  {:2.2f}'.format(ev['horizontalSpreadFWHM'])+ ' mm'+ nl

    q=ev['dispersionQuadratic'];
    ii=ii +'dispersion: E[eV] = ${:2.5f}d^2 + {:2.2f}d + {:2.0f} $'.format(q[0],q[1],q[2])+ nl
    eV_per_px=q[1]*p['geometry']['detectorPxSize']
##################
    evaluateMono(p,mono_rrr)

    ax = fig.add_subplot(246)
    drawPSF(p,mono_rrr,ax)
    plt.title('Point spread function')



    ax = fig.add_subplot(243)
    plotTopViewAOI(p,mono_rrr,ax)
    plt.title('AOI on crystal [mrad]')



    dispersionLinearCentral=p['evalu']['dispersionLinearCentral']
    EresolutionR=p['evalu']['verticalSpreadRMS']*dispersionLinearCentral
    EresolutionF=p['evalu']['verticalSpreadFWHM']*dispersionLinearCentral
    EresolutionFnarrow=p['evalu']['verticalSpreadFWHMNarrow']*dispersionLinearCentral



    ii=ii+ nl +'$'+headerfont+'{\/\/Energy\/\/resolution}$' +nl
    ######################################
    ii=ii+ 'vertical spread from rms:  {:2.3f}'.format(p['evalu']['verticalSpreadRMS'])+ ' mm ' +nl
    ii=ii+ '  - energy resolution:  {:2.3f}'.format(EresolutionR)+ ' eV'+ nl
    ii=ii+ 'vertical spread from fwhm:  {:2.3f}'.format(p['evalu']['verticalSpreadFWHM']) +' mm '+ nl
    ii=ii+ '  - energy resolution:  {:2.3f}'.format( EresolutionF) +' eV'+ nl

    if p['geometry']['evaluation_width']>0:
        ii=ii+ 'vert. spr. narrow (fwhm) :  {:2.3f}'.format( p['evalu']['verticalSpreadFWHMNarrow']) +' mm '+ nl
        ii=ii +'  - energy resolution:  {:2.3f}'.format( EresolutionFnarrow)+ ' eV' +nl
    ii=ii +'dispersion per px:  {:2.1f}'.format(eV_per_px)+ ' eV/px' +nl

    rOff=np.linalg.norm(so['rOffset'])
    SpectSpatialMagnification=p['evalu']['SpatialOffset']/rOff #- = mm/mm
    SpectSpatialBluring=np.abs(p['evalu']['SpatialOffset']/rOff*dispersionLinearCentral) #eV/mm


    ii=ii+nl+ '$'+headerfont+'{\/\/Source\/\/size\/\/broadening}$'+ nl
    ######################################
    ii=ii+ 'magnification in spectral direction:  {:2.2f}'.format( SpectSpatialMagnification)+ ' '+ nl
    ii=ii +'source size broadening:  {:2.2f}'.format( SpectSpatialBluring)+ ' eV/mm ' +nl

    efficiency=p['evalu']['efficiency']
    ii=ii +nl+ 'efficiency:   {:2.2e}'.format(efficiency) +' = {:2.2e}'.format(efficiency*4*np.pi)  +' sr'+ nl
    ii=ii +'rays reflected:  {:2.2e} %'.format(p['evalu']['reflected_ratio']*100) +nl
    #i=ii +'$\mathcal{Caligraphic ccc}$' +nl
    #ii=ii +'$\mathit{Italic italic}$' +nl
   # ii=ii +'$\mathtt{True type}$' +nl
  #  ii=ii +'$\mathrm{Roman rom}$' +nl
 #   ii=ii +'$\mathfrak{Fraktur}$' +nl
#    ii=ii +'$\mathbf{Fraktur}$' +nl



    # print info
    from matplotlib import rc
    #rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
    ## for Palatino and other serif fonts use:
#    rc('font',**{'family':'serif','serif':['Palatino']})
#    rc('text', usetex=True)

    ax = fig.add_subplot(244)
    t=plt.text(-0.05,1,ii,transform=ax.transAxes,fontsize=12,verticalalignment='top')
    ax.axis('off')
    ax.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)



    ax = fig.add_subplot(247, projection='3d')
    plotoneview(p,broad_rrr,100,ax)
    plt.title('3D view')

    plt.savefig('mmpxrt_' +p['simulation']['name']+'.png' , bbox_inches ='tight',dpi=118)
    fn=p['simulation']['out_data_directory']  +'mmpxrt_parameters_' +p['simulation']['name']
    pickle.dump( p, open( fn, "wb" ) )
#    plt.close(fig)
    return fig, ax




def spectrometer_evaluate_noncentral_PSFs(p,spectrorrr):
    """
    """
    ####
    so=p['source']
    broad_rrr=spectrorrr['broad']

    fig= plt.figure(figsize=(19.20,12.08))
    ##################

    E0s=broad_rrr['E0s']
    rayres=broad_rrr['rayres']
    marks=so['continuumMarks_array']
    colores=broad_rrr['colores']
    spectrorrr

    yax=np.arange(-p['simulation']['PSFWindowY'],p['simulation']['PSFWindowY'],p['simulation']['PSFStepY'])
    yax=yax[:-1]
    profs=np.zeros((np.size(marks),np.size(yax)))

    for mi,mark in enumerate(marks):
        ax = fig.add_subplot(2,4,mi+1)
        plt.title('{:.0f} eV'.format(mark))
        sel=(E0s==mark)
    #    sel=(E0s>0)
        sel_rrr={}
        #sel_rrr['effdet']=effdet
        #sel_rrr['effcnt']=effcnt
        sel_rrr['rayres']=rayres[sel,:,:]
        #sel_rrr['aois']=aois
        sel_rrr['E0s']=E0s[sel]
        #sel_rrr['numrays']=numrays
        sel_rrr['colores']=colores[sel]*0+1

        [cntrsY,su2]=drawPSF(p,sel_rrr,ax,vertical_central=0)
        profs[mi,:]=su2

    # %
    #fig.add_subplot(2,4,8)
    plt.subplot2grid((2, 4), (1, 1), colspan=3)
    for mi,mark in enumerate(marks):
        prof=profs[mi,:]
        prof=prof/np.max(prof)
        plt.plot(yax*1e3,prof+mi*0.,label='{:.0f} eV'.format(mark))
    plt.title('Vertical profile of PSFs')
    plt.legend()
    plt.ylim(0,1)
    plt.xlabel('relative position [μm]')
    plt.grid()

    plt.savefig('mmpxrt_' +p['simulation']['name']+'noncentral_PSFs.png' , bbox_inches ='tight',dpi=118)
    return fig, ax

def evaluateCont(p,rrr):
    ## generationg pos* and calculation Erangemax
    sg=p['sg']
    detn=sg['detn']
    Sdetector=sg['Sdetector']
    colores=rrr['colores']
    rayres=rrr['rayres']
    E0s=rrr['E0s']
    numrays=np.size(colores)

  #  posR=np.full((numrays,2),np.nan);
    #posG=np.full((numrays,2),np.nan);
    #posB=np.full((numrays,2),np.nan);
    pos4=np.full((numrays,2),np.nan)
    posCont=np.full((numrays,2),np.nan)
    posCont2=np.full((numrays,2),np.nan)

    detHorz=(np.abs(detn[2])>np.abs(detn[0]))
    po=np.array([0.,0.],float)

#crude Erangemax estimation:
    Erangemaxmin=np.min(E0s)
    Erangemaxmax=np.max(E0s)
    ErangemaxCrude=Erangemaxmax-Erangemaxmin


    dEs=[10,20,50,100,200,500]
    ex=ErangemaxCrude/8
    ci=np.argmin(np.abs((dEs-ex)))
    dE=dEs[ci]
    Erangemaxmin=1e9#energy range as photons on detector
    Erangemaxmax=0

    for i in np.arange(numrays):
          absPos=rayres[i,2,:]
       #projection
          po[0]=absPos[1]#y in 3D becomes x in 2D
          po[1]=((absPos[0]-Sdetector[0])**2 + (absPos[2]-Sdetector[2])**2) ** (1/2)#distance from detector center
          if detHorz:
              if (absPos[0]-Sdetector[0])<0:#see if it was 'front' or 'behind' the detector
                  po[1]=po[1]*-1
          else:
              if (absPos[2]-Sdetector[2])<0:
                  po[1]=po[1]*-1
          #po() is position on detector
          ee=E0s[i]
          if (ee<Erangemaxmin):
              Erangemaxmin=ee
          if (ee>Erangemaxmax):
              Erangemaxmax=ee

          if colores[i]==4:
            pos4[i,:]=po
            if np.mod(ee,2*dE)<dE:
                posCont2[i,:]=po
            else:
                posCont[i,:]=po
   #       else:
#              if colores[i]==1:
 #                 posR[i,:]=po
  #            else:
    #              if colores[i]==2:
   #                   posG[i,:]=po
  #                else:
 #                   if colores[i]==3:
#                        posB[i,:]=po

    Erangemax=Erangemaxmax-Erangemaxmin

    ## horiz FWHM through RMS
    spH=0
    scnt=0
    meanCx=np.nanmean([pos4[:,0], pos4[:,0]])
    for i in np.arange(np.shape(pos4)[0]):
        if not(np.isnan(pos4[i,0])):
            spH=spH+(pos4[i,0]-meanCx)**2
            scnt=scnt+1
    spH=(spH/scnt)**(1/2)# std.dev
    spH=spH*2.3548#FWHM jedné poloviny spektra (continuum)[mm]
    evalu={}

    evalu['horizontalSpreadFWHM']=spH
    evalu['broad_pos4']=pos4
    evalu['broad_posCont']=posCont
    evalu['broad_posCont2']=posCont2
    evalu['Erangemax']=Erangemax
    evalu['Erangemaxmax']=Erangemaxmax
    evalu['Erangemaxmin']=Erangemaxmin
    evalu['Erangemax']=Erangemax
    evalu['broad_dE']=dE
    p['evalu']=evalu
    ## first do the dispersion
    showDispersion(p,rrr,None,False)

## energy range as FWHM of continuum signal
    Ebin=Erangemax/np.size(E0s)*80
    Ebin=max(Ebin,5)
    Ex=np.arange(Erangemaxmin-Ebin,Erangemaxmax+Ebin,Ebin)

    h=np.histogram(E0s,Ex)
    h=h[0]
    hm=np.max(h)/2
    dat2=np.copy(h)
    dat2[dat2<=hm]=0
    dat2[dat2>hm]=1

    if False:
        plt.plot(Ex,np.append(h,0))
        plt.plot(Ex,np.append(dat2,0)*80*100)
    Ex2=np.concatenate((dat2,np.array([0])))*Ex
    Ex2[Ex2==0]=np.nan
    ErangeFWHM=np.nanmax(Ex2)-np.nanmin(Ex2)
    evalu['ErangeFWHM']=ErangeFWHM

###########################################################
def evaluateMono(p,rrr):
    sg=p['sg']
    c=p['crystal']
    detn=sg['detn']
    Sdetector=sg['Sdetector']
    colores=rrr['colores']
    rayres=rrr['rayres']
    E0s=rrr['E0s']
    numrays=np.size(colores)
    ## generationg pos* and calculation Erangemax
    posR=np.full((numrays,2),np.nan)
    posG=np.full((numrays,2),np.nan)
    posB=np.full((numrays,2),np.nan)
    pos4=np.full((numrays,2),np.nan)
    detHorz=(np.abs(detn[2])>np.abs(detn[0]))
    po=np.array([0,0],float)
    for i in np.arange(numrays):
          absPos=rayres[i,2,:]
       #projection
          po[0]=absPos[1]#y in 3D becomes x in 2D
          po[1]=((absPos[0]-Sdetector[0])**2 + (absPos[2]-Sdetector[2])**2) ** (1/2)
          if detHorz:
              if (absPos[0]-Sdetector[0])<0:#see if it was 'front' or 'behind' the detector
                  po[1]=po[1]*-1
          else:
              if (absPos[2]-Sdetector[2])<0:
                  po[1]=po[1]*-1
          #po() is position on detector

          if colores[i]==1:
              posR[i,:]=po
          else:
              if colores[i]==2:
                  posG[i,:]=po
              else:
                if colores[i]==3:
                    posB[i,:]=po
                else:
                    if colores[i]==4:
                        pos4[i,:]=po


    ## Vertical FWHM through RMS
    meanCy=np.nanmean([posR[:,1]])
    sp=0
    scnt=0
    for i in np.arange(np.shape(posR)[0]):
        if not(np.isnan(posR[i,1])):
            sp=sp+(posR[i,1]-meanCy)**2
            scnt=scnt+1
    sp=(sp/scnt)**(1/2)# std.dev
    sp=sp*2.3548#FWHM jedné poloviny spektra (continuum)[mm]
    p['evalu']['verticalSpreadRMS']=sp


    ## Horizontal FWHM through RMS
    meanCx=np.nanmean([posR[:,0]])
    sp=0
    scnt=0
    for i in np.arange(np.shape(posR)[0]):
        if not(np.isnan(posR[i,0])):
            sp=sp+(posR[i,0]-meanCx)**2
            scnt=scnt+1
    sp=(sp/scnt)**(1/2)# std.dev
    sp=sp*2.3548#FWHM jedné poloviny spektra (continuum)[mm]
    p['evalu']['PSF_horizontalSpreadRMS']=sp

    ## Vertical FWHM through histogram
    vals=posR[:,1]
    if np.nansum(vals)==0:
        p['evalu']['reflected_ratio']=0
        p['evalu']['efficiency']=0
        p['evalu']['verticalSelectPSF']=0
        p['evalu']['verticalSpreadFWHMNarrow']=0
        p['evalu']['verticalSpreadFWHM']=0
        p['evalu']['SpatialOffset']=0
        p['evalu']['PSF_horizontalSpreadRMS']=0
        return

    if 0: #outdated,  done in drawPSF
        rang=(np.nanmax(vals)-np.nanmin(vals))
        lene=np.size(vals)-np.sum(np.isnan(vals))
        Ebin=rang/lene*380
        #if PSFStepY>-1:
            #Ebin=PSFStepY
        print(Ebin)
        Ex=np.arange(np.nanmin(vals)-Ebin,rang+np.nanmax(vals),Ebin)
        h=np.histogram(vals,Ex)[0]

        hm=np.max(h)/2
        dat2=h
        dat2[dat2<=hm]=0
        dat2[dat2>hm]=1
        Ex2=Ex*np.append(dat2,0)
        Ex2[Ex2==0]=np.nan
        if (True):
            h2=np.append(h,0)
            plt.figure()
            plt.plot(Ex,h2)
            plt.plot(Ex2,np.append(dat2,0)*hm)
            plt.figure()
        verticalSpreadFWHM=np.nanmax(Ex2)-np.nanmin(Ex2)
    else:
        verticalSpreadFWHM=0

    ## Horizontal FWHM through histogram
    vals=posR[:,0]

    rang=(np.nanmax(vals)-np.nanmin(vals))
    lene=np.size(vals)-np.sum(np.isnan(vals))
    Ebin=rang/lene*80
    Ex=np.arange(np.nanmin(vals)-Ebin,rang+np.nanmax(vals),Ebin)
    h=np.histogram(vals,Ex)[0]

    hm=np.max(h)/2 #half-max
    dat2=h
    dat2[dat2<=hm]=0
    dat2[dat2>hm]=1
    if (False):
        plt.plot(Ex,h)
        plt.plot(Ex,dat2*hm)
    Ex2=Ex*np.append(dat2,0)
    Ex2[Ex2==0]=np.nan
    PSF_horizontalSpreadFWHM=np.nanmax(Ex2)-np.nanmin(Ex2)
    p['evalu']['PSF_horizontalSpreadFWHM']=PSF_horizontalSpreadFWHM


    ## Vertical FWHM through histogram- narrow Y range
    evalSelectY=p['geometry']['evaluation_width']
    verticalSpreadFWHMnarrow=np.nan
    verticalSelectPSF=np.nan

    if evalSelectY>0:
        aa=np.array(posR[:,0])
        selnonnan=(~np.isnan(aa));
        selnonnan[selnonnan]=(np.abs(posR[selnonnan,0])<evalSelectY/2)
        #selnonnan=selnonnan*0+1
        sel=selnonnan
        #sel=np.logical_and((np.abs(posR[:,0])<evalSelectY/2))

        vals=posR[sel,1]
        rangee=(np.nanmax(vals)-np.nanmin(vals))
        lena=np.size(vals)-np.sum(np.isnan(vals))
        Ebin=rangee/lena*80

        Ebin=max(p['geometry']['detectorPxSize'],Ebin)

        #if PSFStepY>-1:
            #Ebin=PSFStepY
        if np.size(vals)>1:
            Ex=np.arange(np.nanmin(vals)-Ebin,rangee+np.nanmax(vals),Ebin)
            h=np.histogram(vals,Ex)[0]

            hm=np.max(h)/2
            dat2=np.copy(h)
            dat2[dat2<=hm]=0
            dat2[dat2>hm]=1
            if (False):
                plt.plot(Ex,h,'k')
                plt.plot(Ex,dat2*hm,'k')
            Ex2=Ex*np.append(dat2,0)
            Ex2[Ex2==0]=np.nan
            verticalSelectPSF=np.matrix((Ex,np.append(np.nan,h)))
            verticalSpreadFWHMnarrow=np.nanmax(Ex2)-np.nanmin(Ex2)

    ## source size broadening (aka 2D resolution)
    if np.logical_and(np.nansum(np.abs([posB[:,1]]))>0, np.nansum(np.abs([posR[:,1]]))>0):
        meanOffy=np.nanmean([posB[:,1]])
        meanCy=np.nanmean([posR[:,1]])
        SpatialOffset=np.abs(meanOffy-meanCy)#mm
    else:
        SpatialOffset=np.nan


    ## efficiency - this is a section corresponding to the equations in the paper
    if c['mosaicity']==0:
        c['crystalPeakReflectivity']=c['integrated_reflectivity']/c['rockingCurveFWHM']

    reflectedratio=rrr['effdet']/rrr['effcnt']
    if (not p['source']['divergenceGaussian']):
        if (p['source']['divergenceRectangular']):
            #coveredangle=(beamDivergenceX/2)*beamDivergenceY/2#this works probably just for small angles
            coveredangle=4*np.arcsin(np.sin(p['source']['divergenceX']/2)*np.sin(p['source']['divergenceY']/2))#from Wiki: https://en.wikipedia.org/wiki/Solid_angle
        else:
            coveredangle=np.pi*(p['source']['divergenceFWHM']/2)**2#this works probably just for small angles

        #those 3 rows are the equaiton in paper.
        coveredratio=coveredangle/(4*np.pi)

        efficiency=reflectedratio*coveredratio
        efficiency=efficiency*c['crystalPeakReflectivity']
        debug=1
        if debug:
            print("covered ratio: {:.1e}".format(coveredratio))
            print("reflected ratio: {:.1e}".format(reflectedratio))
            print("efficiency: {:.1e}".format(efficiency))
    else:
        efficiency=-1

    #crystal thickness ratio    :
    #this part assumes the integrated reflectivity was given for inifite thick crystal,
    #and calculates how much down it goes down with given crystal thickness

    #probability of ray reflection in given crystal thickness comapred to infinite crystal
       #prob_refl_thin =  (1-np.exp(-p['crystal']['maxThickness']/p['crystal']['penetrationDepth']))
       #prob_refl_ratio = 1/prob_refl_thin

    p['evalu']['reflected_ratio']=reflectedratio
    p['evalu']['efficiency']=efficiency
    p['evalu']['verticalSelectPSF']=verticalSelectPSF
    p['evalu']['verticalSpreadFWHMNarrow']=verticalSpreadFWHMnarrow
    p['evalu']['verticalSpreadFWHM']=verticalSpreadFWHM
    p['evalu']['SpatialOffset']=SpatialOffset


################################################################
def drawPSF(p,rrr,ax,vertical_central=1):
    colores=rrr['colores']
    rayres=rrr['rayres']
    E0s=rrr['E0s']
    ev=p['evalu']
    Sdetector=p['sg']['Sdetector']

    numrays=np.size(colores)
    posCont=np.full((numrays,2),np.nan)
    posR=np.full((numrays,2),np.nan)
    posG=np.full((numrays,2),np.nan)
    posB=np.full((numrays,2),np.nan)
    posCont=np.full((numrays,2),np.nan)
    posAll=np.full((numrays,2),np.nan)
    po=np.array([0.,0.],float)
    detn=p['sg']['detn']
    detHorz=(np.abs(detn[2])>np.abs(detn[0]))
    for i in np.arange(np.shape(rayres)[0]):
          absPos=rayres[i,2,:]
       #projection
          po[0]=absPos[1]#y in 3D becomes x in 2D
          po[1]=((absPos[0]-Sdetector[0])**2 + (absPos[2]-Sdetector[2])**2) ** (1/2)#distance from detector center
#          posAll[i,:]=[absPos[1], absPos[0]]
          if detHorz:
              if (absPos[0]-Sdetector[0])<0:#see if it was 'front' or 'behind' the detector
                  po[1]=po[1]*-1
          else:
              if (absPos[2]-Sdetector[2])<0:
                  po[1]=po[1]*-1
          posAll[i,:]=po
          if colores[i]==1:
              posR[i,:]=po
          else:
              if colores[i]==2:
                  posG[i,:]=po
              else:
                  if colores[i]==3:
                      posB[i,:]=po
          if colores[i]==4:
            posCont[i,:]=po

    if (np.nansum(np.nansum(posR))==0):
        return

    ## get the optimal ranges

    pC=posR
    xs=np.abs(pC[:,0])
    ys=np.abs(pC[:,1])
    xs2=xs[np.logical_not(np.isnan(xs))]
    ys2=ys[np.logical_not(np.isnan(ys))]
    windowX=np.quantile(xs2,0.95)*1.1
    windowY=np.quantile(ys2,0.95)*1.1

    cnt=np.shape(posCont)[0]
    stepX=windowX/cnt*600 #all this is in mm
    stepY=windowY/cnt*600

    stepY=min(stepY, windowY/5)
    stepX=min(stepX, windowX/5)
    stepX=max(p['geometry']['detectorPxSize'],stepX)
    stepY=max(p['geometry']['detectorPxSize'],stepY)
    stepX=max(windowX/40,stepX)
    stepY=max(windowY/40,stepY)
    windowX=max(windowX,5*stepX)
    if p['simulation']['PSFWindowY']>-1:
        windowY=p['simulation']['PSFWindowY']
    if p['simulation']['PSFStepY']>-1:
        stepY=p['simulation']['PSFStepY']
    if p['simulation']['PSFStepX']>-1:
        stepX=p['simulation']['PSFStepX']
    if p['simulation']['PSFWindowX']>-1:
        windowX=p['simulation']['PSFWindowX']

    if windowY<=(stepY*4):
        windowY=stepY*5
    ## plt.plotting
    if vertical_central:
        vertical_mean=0
    else:
        vertical_mean=np.nanmean(pC[:,1])
    cntrsY=np.arange(-1*windowY,windowY,stepY)
    cntrsY=cntrsY+vertical_mean
    cntrsX=np.arange(-1*windowX,windowX,stepX)

    edX=cntrsX+stepX/2
    edY=cntrsY+stepY/2
    #cntrs=[cntrsX,cntrsY]
    eds=[edX,edY]
    nR = np.histogram2d(posR[:,0],posR[:,1],eds)[0]
    nR[0,0]=0
    nR[np.shape(nR)[0]-1,np.shape(nR)[1]-1]=0
    nR[0,np.shape(nR)[1]-1]=0
    nR[np.shape(nR)[0]-1,0]=0
    nR2=np.transpose(nR)
    plt.imshow(nR2,extent=(-1000*windowX,1000*windowX,1000*(-windowY+vertical_mean),1000*(windowY+vertical_mean)),aspect='auto',origin='lower')

# %% get profiles & FWHM
    su2=np.sum(nR,0)
    su2y=np.sum(nR,1)
    su2[0]=0
    su2[np.size(su2)-1]=0
    su2y[0]=0
    su2y[np.size(su2y)-1]=0


    profile=np.append(np.nan,su2)
    hm=np.nanmax(profile)/2
    dat2=profile*1.0
    dat2[dat2<=hm]=np.nan
    dat2[dat2>hm]=1
#    Ex2=cntrsY*np.append(dat2,0)
    if 0:
        plt.figure()
        plt.plot(cntrsY,profile)
        plt.plot(cntrsY,dat2*hm)
#        plt.plot(Ex2,np.append(dat2,0)*hm)
        plt.figure()
    verticalSpreadFWHM=(np.nansum(dat2)+0.5)*stepY
    p['evalu']['verticalSpreadFWHM']=verticalSpreadFWHM
    #print(verticalSpreadFWHM)

# %%  draw profiles

    su2m=su2/np.max(su2)*0.5*windowX-windowX
    su2y=su2y/np.max(su2y)*0.5*windowY-windowY+vertical_mean
    print(windowY)
    dat3=dat2*0.25*windowX-windowX
    print(dat3)

    plt.plot(np.append(np.nan,su2m)*1e3,(cntrsY)*1000,'w',linewidth=1) #vertical
    plt.plot(dat3*1e3,cntrsY*1e3,'w',linewidth=1)

    plt.plot(cntrsX*1e3,np.append(np.nan,(su2y)*1e3),'w',linewidth=1) #horizontal



# %%


    #selected profile
    evalSelectY=p['geometry']['evaluation_width']
    if evalSelectY>0:
        es2=evalSelectY/2*1e3
        wy=windowY*1e3*1.1

        if np.size(p['evalu']['verticalSelectPSF'])>1:
            vyy=np.squeeze(np.asarray(p['evalu']['verticalSelectPSF'][1,:]))
            vyy=(vyy/np.nanmax(vyy)*0.5*windowX-windowX)*1e3
            plt.plot(vyy,np.squeeze(np.asarray(p['evalu']['verticalSelectPSF'][0,:]))*1e3,'r',linewidth=1)
            plt.plot([es2,es2,-1*es2,-1*es2],[wy,-1*wy,-1*wy,wy],'r',linewidth=1)

        plt.xlabel('y [$\mathrm{{\mu}m}$]')
        plt.ylabel('d [$\mathrm{{\mu}m}$]')
        ax.yaxis.set_label_coords(-0.12,0.5)
        #colorbar
        plt.xlim(-1*windowX*1e3,windowX*1e3)
        plt.ylim(-1*windowY*1e3,windowY*1e3)

    return [cntrsY,su2]

def drawDetectorStripes(p,rrr,ax,realscale):
    colores=rrr['colores']
    rayres=rrr['rayres']
    E0s=rrr['E0s']
    ev=p['evalu']
    Sdetector=p['sg']['Sdetector']

    numrays=np.size(colores)

    dE=ev['broad_dE']
    posCont2=ev['broad_posCont2']
    posCont=ev['broad_posCont']
    pC=ev['broad_pos4']

    ## get the optimal ranges
    #pC=np.concatenate((posCont,posCont2))
    xs=np.abs(pC[:,0])
    ys=np.abs(pC[:,1])

    xs2=xs[np.logical_not(np.isnan(xs))]
    ys2=ys[np.logical_not(np.isnan(ys))]
    windowX=np.quantile(xs2,0.95)*1.1
    if p['geometry']['detectorWidth']>0:
        windowX=p['geometry']['detectorWidth']/2
    windowY=np.quantile(ys2,0.95)*1.1
    windowY=p['geometry']['detectorLength']/2
    cnt=np.shape(posCont)[0]
    stepX=windowX/cnt*4000
    stepY=windowY/cnt*4000
    stepY=min(stepY, windowY/5)
    stepX=min(stepX, windowX/5)
    stepX=max(stepX,p['geometry']['detectorPxSize'])
    stepY=max(stepY,p['geometry']['detectorPxSize'])
    stepX=max(windowX/50,stepX)
    stepY=max(windowY/50,stepY)
    stepY=min(windowY/3,stepY)
    stepX=min(windowX/3,stepX)

    if p['simulation']['DetectorStepY']>-1:
        stepY=p['simulation']['DetectorStepY']
    if p['simulation']['DetectorStepX']>-1:
        stepX=p['simulation']['DetectorStepX']


    cntrsX=np.arange(-1*windowX,windowX,stepX)
    cntrsY=np.arange(-1*windowY,windowY,stepY)

    edX=cntrsX+stepX/2
    edY=cntrsY+stepY/2
    eds=[edX,edY]
    nCon =np.histogram2d(posCont[:,0],posCont[:,1],eds)
    nCont=nCon[0]

    nCon2 =np.histogram2d(posCont2[:,0],posCont2[:,1],eds)
    nCont2=nCon2[0]

    nCont=np.array(1.*nCont)/np.max(np.max(nCont))*1.
    nCont2=np.array(1.*nCont2)/np.max(np.max(nCont2))*1.
    nS=nCont+nCont2

    #boosting
    Threshold=0.
    if Threshold>0:
        BoostRegion=(nS<Threshold)
        blue=(nS/Threshold)
        blue[blue>1]=0
        blue=blue*0.4
        nCont[BoostRegion]=nCont[BoostRegion]*6
        nCont2[BoostRegion]=nCont2[BoostRegion]*6
    else:
        blue=nS*0


    img=np.zeros((np.shape(nCont)[0],np.shape(nCont)[1],3),float)
    img[:,:,0]=nCont*1
    img[:,:,1]=nCont2*1
    img[:,:,2]=blue
    img=np.transpose(img,(1,0,2))

    nR = np.histogram2d(posCont[:,0],posCont[:,1],eds)[0]
    nR=np.transpose(nR)
#    plt.imshow(nR,extent=(-1*windowX,windowX,-1*windowY,windowY),aspect='auto',origin='lower')
    aspe='auto'
    #if realscale:
        #aspe='equal'
    plt.imshow(img,extent=(-1*windowX,windowX,-1*windowY,windowY),aspect=aspe,origin='lower')

    t=plt.text(0.02,0.93,'stripe width: '+ str(dE)+ ' eV',transform=ax.transAxes,color='white')

    plt.xlabel('y [mm]')
    plt.ylabel('d [mm]')
    ax.yaxis.set_label_coords(-0.10,0.5)

    plt.plot([0, 0], [-600, 600],'-',linewidth=1,color=[0.5 ,0.5 ,0.5])
    plt.plot([-1, 1 ], [0, 0],'-',linewidth=1,color=[0.5 ,0.5, 0.5])

    if np.size(p['simulation']['DetectorXlim'])>0:
        plt.xlim(p['simulation']['DetectorXlim'])
    else:
        plt.xlim(-1*windowX,windowX)
    plt.ylim(-1*windowY,windowY)

    if not realscale:

        ## drawing the profiles
        windowY=np.quantile(ys2,0.99)*1.1
        stepY=min(windowY/3,stepY)
        cntrsY=np.arange(-1*windowY,windowY,stepY)

        hhs=np.histogram(posCont2[:,1],cntrsY)
        hh=hhs[0]
        hh=hh/np.max(hh)*windowX*0.7-windowX
        plt.plot(np.append(np.nan, hh),cntrsY,'y',linewidth=1)

        hhs=np.histogram(pC[:,1],cntrsY)
    #todo    save('detspect','spec','-ascii')
        hh=hhs[0]
        envelope=np.append(hh,np.nan);
        envelopes=envelope/np.nanmax(envelope)*windowX*0.7-windowX
        plt.plot(envelopes,cntrsY,'w')
        envel=np.matrix((cntrsY,envelope))
        p['evalu']['envelope']=envel


def drawDetectorAll(p,rrr,ax,realscale):
    colores=rrr['colores']
    rayres=rrr['rayres']
    E0s=rrr['E0s']
    Sdetector=p['sg']['Sdetector']

    numrays=np.size(colores)
    posCont=np.full((numrays,2),np.nan)
    posR=np.full((numrays,2),np.nan)
    posG=np.full((numrays,2),np.nan)
    posB=np.full((numrays,2),np.nan)
    posCont=np.full((numrays,2),np.nan)
    posAll=np.full((numrays,2),np.nan)
    po=np.array([0.,0.],float)
    detn=p['sg']['detn']
    detHorz=(np.abs(detn[2])>np.abs(detn[0]))
    for i in np.arange(np.shape(rayres)[0]):
          absPos=rayres[i,2,:]
       #projection
          po[0]=absPos[1]#y in 3D becomes x in 2D
          po[1]=((absPos[0]-Sdetector[0])**2 + (absPos[2]-Sdetector[2])**2) ** (1/2)#distance from detector center
#          posAll[i,:]=[absPos[1], absPos[0]]
          if detHorz:
              if (absPos[0]-Sdetector[0])<0:#see if it was 'front' or 'behind' the detector
                  po[1]=po[1]*-1
          else:
              if (absPos[2]-Sdetector[2])<0:
                  po[1]=po[1]*-1
          posAll[i,:]=po
          if colores[i]==1:
              posR[i,:]=po
          else:
              if colores[i]==2:
                  posG[i,:]=po
              else:
                  if colores[i]==3:
                      posB[i,:]=po
          if colores[i]==4:
            posCont[i,:]=po

#    if (np.nansum(np.nansum(posR))==0):
 #       return
    ## get the optimal ranges
    pC=posAll
    xs=np.abs(pC[:,0])
    ys=np.abs(pC[:,1])

    stepX=p['geometry']['detectorPxSize']
    stepY=p['geometry']['detectorPxSize']
    windowY=p['geometry']['detectorWidth']
    windowX=p['geometry']['detectorLength']

    ## plt.plotting
    cntrsX=np.arange(-1*windowX,windowX,stepX)
    cntrsY=np.arange(-1*windowY,windowY,stepY)

    edX=cntrsX+stepX/2
    edY=cntrsY+stepY/2
    #cntrs=[cntrsX,cntrsY]
    eds=[edX,edY]
    nC = np.histogram2d(pC[:,0],pC[:,1],eds)[0]
    nC[0,0]=0
    nC[np.shape(nC)[0]-1,np.shape(nC)[1]-1]=0
    nC[0,np.shape(nC)[1]-1]=0
    nC[np.shape(nC)[0]-1,0]=0
    nR2=np.transpose(nC)
    plt.imshow(nR2,extent=(-1000*windowX,1000*windowX,-1000*windowY,1000*windowY),aspect='auto',origin='lower')

    ## profiles

    su2=np.sum(nC,0)
    su2y=np.sum(nC,1)
    su2[0]=0
    su2[np.size(su2)-1]=0
    su2y[0]=0
    su2y[np.size(su2y)-1]=0

    su2=su2/np.max(su2)*0.5*windowX-windowX
    su2y=su2y/np.max(su2y)*0.5*windowY-windowY

    plt.plot(np.append(np.nan,su2)*1e3,cntrsY*1000,'w',linewidth=1)
    plt.plot(cntrsX*1e3,np.append(np.nan,su2y*1e3),'w',linewidth=1)

    #selected profile
    evalSelectY=p['geometry']['evaluation_width']
    es2=evalSelectY/2*1e3
    wy=windowY*1e3*1.1
    plt.plot([es2,es2,-1*es2,-1*es2],[wy,-1*wy,-1*wy,wy],'r',linewidth=1)

    plt.xlabel('y [$\mathrm{{\mu}m}$]')
    plt.ylabel('d [$\mathrm{{\mu}m}$]')
    ax.yaxis.set_label_coords(-0.12,0.5)
    #colorbar
    plt.xlim(-1*windowX*1e3,windowX*1e3)
    plt.ylim(-1*windowY*1e3,windowY*1e3)


def showDispersion(p,rrr,ax,plotnow):
    from numpy.polynomial import polynomial as P
    dispersionVertical=0
    pos4=p['evalu']['broad_pos4']
    detectorLength=p['geometry']['detectorLength']
    E0s=rrr['E0s']
    if dispersionVertical:
        Xs=[pos4[:,0],pos4[:,0]]
        minX=np.min([pos4[:,0],pos4[:,0]])
        maxX=np.max([pos4[:,0],pos4[:,0]])
        E0sb=[E0s,E0s]
    else:
        Xs=pos4[:,1]
        minX=np.min(pos4[:,1])
        maxX=np.max(pos4[:,1])
        E0sb=E0s
    selnan=np.logical_not(np.isnan(Xs))

    q=np.polyfit(Xs[selnan],E0sb[selnan],2)

    step=(maxX-minX)/500
    xval=np.arange(minX,maxX,step)
    fitval=np.polyval(q,xval)
    centralval=xval*q[1]+np.polyval(q,0)
    dispersionQuadratic=q
    dispersionQuadratic[1]=np.abs(dispersionQuadratic[1])
    p['evalu']['dispersionLinearCentral']=np.abs(q[1])
    detEdge=np.polyval(q,[-detectorLength/2, detectorLength/2])
    p['evalu']['ErangeDetected']=np.abs(detEdge[1]-detEdge[0])
    p['evalu']['dispersionQuadratic']=dispersionQuadratic;
    if  plotnow:
        sh=0.9
        shc=[sh,sh,sh]

        plt.xlabel('d [mm]')
        plt.ylabel('energy [keV]')
        ax.yaxis.set_label_coords(-0.12,0.5)

        plt.plot(Xs,E0sb/1000,'.',markersize=1,color=[0.3, 0.6,0.99],label='raytracing')
        plt.plot(xval,fitval/1000,color=[1, 0.4 ,0.2],label='quadratic fit',linewidth=3)
        plt.plot(xval,centralval/1000,color=[0.0,0.3,0.0],linewidth=1,label='tangent at d=0')

        er=[np.min(E0sb),np.max(detEdge)]
        sh=0.7
        shc=[sh,sh,sh]

        xl=plt.xlim()
        yl=plt.ylim()

        plt.plot([xl[0],detectorLength/2], [detEdge[1]/1000,detEdge[1]/1000],color=shc,linewidth=3,label='detector')
        plt.plot([xl[0],detectorLength/2], [detEdge[0]/1000,detEdge[0]/1000],color=shc,linewidth=3)

        plt.plot(([detectorLength/2,detectorLength/2,-1*detectorLength/2,-1*detectorLength/2,]),([0,detEdge[1]/1000,detEdge[1]/1000,0]),color=shc,linewidth=3)

        plt.legend()
        plt.grid()
#        plt.ylim(np.min(E0sb), np.max(E0sb))
        plt.ylim(yl)
        plt.xlim(xl)


def plotoneview(p,rrr,maxrays,ax):
    sg=p['sg']
    colores=rrr['colores']
    rayres=rrr['rayres']
    if ax==None:
        fig = plt.figure()
        fig= plt.figure(figsize=(14,10))
        ax = fig.add_subplot(111, projection='3d')
    #ax.view_init(elev=20., azim=-80.) #close to side view
    #ax.view_init(elev=20., azim=-140.)
    ax.view_init(elev=20., azim=-160.)
    lw=0.5
    maxrays=min(maxrays,np.size(colores))
    for i in np.arange(maxrays):
        c=colores[i];
        if (c==1):
            col='-'
            co='*'
            co2=[0.7, 0.3,0.2]
        else  :
            if (c==2):
                col='-'
                co='*'
                co2=[0.2, 0.7,0.1]
            else :
             col='-'
             co='.'
             co2=[0.3, 0.6,0.99]

        plt.plot(rayres[i,:,0],rayres[i,:,1],rayres[i,:,2],col,linewidth=lw,color=co2)
        plt.plot([rayres[i,2,0]],[rayres[i,2,1]],[rayres[i,2,2]],co,linewidth=lw,color=co2)
        plt.plot([rayres[i,1,0]],[rayres[i,1,1]],[rayres[i,1,2]],co,linewidth=lw,color=co2)
#    %% lost beams
#    maxrays=numrays;
#    maxrays=min(300,maxrays);
#    maxrays=min(length(lostbeams),maxrays);
#    for i=1:maxrays,
#         plot3(lostbeams(i,1),lostbeams(i,2),lostbeams(i,3),'*','Color',[0.5 0.5 0.5],'lineWidth',1);
#    end;
#
#    %%
#    cc=crystalWidth/2;
    plt.plot([rayres[1,0,0]],[rayres[1,0,1]],[rayres[1,0,2]],'*',color='red');

    drawCrystal(p)
#draw Detector
    detX=sg['Sdetector'][0];
    detY=sg['Sdetector'][1];
    detZ=sg['Sdetector'][2];
    detdx=np.sin(sg['SdetectorAngle'])*p['geometry']['detectorLength']/2
    detdz=np.cos(sg['SdetectorAngle'])*p['geometry']['detectorLength']/2
    windowX=p['geometry']['detectorWidth']/2
    if (windowX==-1):
        windowX=p['sg']['windowY']
    plt.plot([detX],[detY],[detZ],'k*');
    plt.plot([detX+detdx, detX+detdx, detX-detdx,detX-detdx, detX+detdx ],[detY-windowX,detY+windowX,detY+windowX,detY-windowX,detY-windowX,],         [detZ-detdz,detZ-detdz,detZ+detdz,detZ+detdz,detZ-detdz],'k-',linewidth=2);
#
#     plot3(Ssource(1),Ssource(2),Ssource(3),'k*');
#     central ray
    CR=np.matrix((sg['Ssource'],sg['Scrystal'],sg['Sdetector']));
    a=np.squeeze(np.array(CR[:,0]))
    b=np.squeeze(np.array(CR[:,1]))
    c=np.squeeze(np.array(CR[:,2]))
    plt.plot(a,b,c,'r',linewidth=1)

    plt.xlabel('x [mm]')
    plt.ylabel('y [mm]')
#    plt.zlabel('z [mm]');
    ax.set_zlabel('z [mm]')
    return ax

def drawCrystal(p):
    #fig= plt.figure(figsize=(14,10))
    #ax = fig.add_subplot(111, projection='3d')
    step=0.1
    c=p['crystal']
    sg=p['sg']
    crystalCenterX=sg['Scrystal'][0]
    crystalWidth=c['width']
    cc=crystalWidth/2;
    crystalMinX=crystalCenterX-c['length']/2
    crystalMaxX=crystalCenterX+c['length']/2
    crystalR=c['radius_w']
    crystalRv=c['radius_l']
    xis=np.arange(crystalMinX,crystalMaxX, step=step)
    zs=np.zeros(np.size(xis))
    zs2=np.zeros(np.size(xis))

    for xi in np.arange(np.size(xis)):
        r=[xis[xi], cc]
        parzH=-1*(crystalRv**2-(r[0]-crystalCenterX)**2)**(1/2)+crystalRv
        parzV=-1*(crystalR**2-(r[1])**2)**(1/2)+crystalR
        parz=parzH+parzV
        zs[xi]=parz

        r=[xis[xi], 0]
        parzH=-1*(crystalRv**2-(r[0]-crystalCenterX)**2)**(1/2)+crystalRv
        parzV=-1*(crystalR**2-(r[1])**2)**(1/2)+crystalR
        parz=parzH+parzV
        zs2[xi]=parz

    plt.plot(xis,xis*0+cc,zs,'k-')
    plt.plot(xis,xis*0-cc,zs,'k-')
    plt.plot(xis,xis*0,zs2,'k-')

    yis=np.arange(-1*cc,cc+1, step=step)
    zs=np.zeros(np.size(yis))
    zs2=np.zeros(np.size(yis))
    zs3=np.zeros(np.size(yis))
    for yi in np.arange(np.size(yis)):
        r=[crystalMinX,yis[yi]]
        parzH=-1*(crystalRv**2-(r[0]-crystalCenterX)**2)**(1/2)+crystalRv
        parzV=-1*(crystalR**2-(r[1])**2)**(1/2)+crystalR
        parz=parzH+parzV
        zs[yi]=parz

        r=[crystalMaxX,yis[yi]]
        parzH=-1*(crystalRv**2-(r[0]-crystalCenterX)**2)**(1/2)+crystalRv
        parz=parzH+parzV
        zs2[yi]=parz

        r=[crystalCenterX,yis[yi]]
        parzH=-1*(crystalRv**2-(r[0]-crystalCenterX)**2)**(1/2)+crystalRv
        parz=parzH+parzV
        zs3[yi]=parz

    plt.plot(yis*0+crystalMinX,yis,zs,'k-')
    plt.plot(yis*0+crystalMaxX,yis,zs2,'k-')
    #plt.plot(yis*0+crystalCenterX,yis,zs3,'k-')

def drawSideView(p,broad_rrr,ax):
    oneViewRays=50
    windowX=100
    maxrays=300
    windowY=p['geometry']['detectorLength']/2
    sg=p['sg']
    colores=broad_rrr['colores']
    rayres=broad_rrr['rayres']
    maxrays=min(maxrays,np.size(colores))
    for i in np.arange(maxrays):
        c=colores[i];
        if (c==1):
            col='-';
            co='*';
            co2=[0.7, 0.3,0.2];
        else  :
            if (c==2):
                col='-';
                co='*';
                co2=[0.2, 0.7,0.1];
            else :
             col='-';
             co='.';
             co2=[0.3, 0.6,0.99];

        plt.plot(rayres[i,:,0],rayres[i,:,2],col,linewidth=1,color=co2)
        plt.plot([rayres[i,2,0]],[rayres[i,2,2]],co,linewidth=1,color=co2)
        plt.plot([rayres[i,1,0]],[rayres[i,1,2]],co,linewidth=1,color=co2)

#drawCrystal(p)
    c=p['crystal']
    crystalCenterX=sg['Scrystal'][0]
    crystalWidth=c['width']
    cc=crystalWidth/2;
    crystalMinX=crystalCenterX-c['length']/2
    crystalMaxX=crystalCenterX+c['length']/2
    crystalR=c['radius_w']
    crystalRv=c['radius_l']
    xis=np.arange(crystalMinX,crystalMaxX)
    zs=np.zeros(np.size(xis))
    zs2=np.zeros(np.size(xis))

    for xi in np.arange(np.size(xis)):
        r=[xis[xi], cc]
        parzH=-1*(crystalRv**2-(r[0]-crystalCenterX)**2)**(1/2)+crystalRv
        parzV=-1*(crystalR**2-(r[1])**2)**(1/2)+crystalR
        parz=parzH+parzV
        zs[xi]=parz

        r=[xis[xi], 0]
        parzH=-1*(crystalRv**2-(r[0]-crystalCenterX)**2)**(1/2)+crystalRv
        parzV=-1*(crystalR**2-(r[1])**2)**(1/2)+crystalR
        parz=parzH+parzV
        zs2[xi]=parz

    plt.plot(xis,zs,'k-')
    plt.plot(xis,zs2,'k-')

    yis=np.arange(-1*cc,cc+1)
    zs=np.zeros(np.size(yis))
    zs2=np.zeros(np.size(yis))
    zs3=np.zeros(np.size(yis))
    for yi in np.arange(np.size(yis)):
        r=[crystalMinX,yis[yi]]
        parzH=-1*(crystalRv**2-(r[0]-crystalCenterX)**2)**(1/2)+crystalRv
        parzV=-1*(crystalR**2-(r[1])**2)**(1/2)+crystalR
        parz=parzH+parzV
        zs[yi]=parz

        r=[crystalMaxX,yis[yi]]
        parzH=-1*(crystalRv**2-(r[0]-crystalCenterX)**2)**(1/2)+crystalRv
        parz=parzH+parzV
        zs2[yi]=parz

        r=[crystalCenterX,yis[yi]]
        parzH=-1*(crystalRv**2-(r[0]-crystalCenterX)**2)**(1/2)+crystalRv
        parz=parzH+parzV
        zs3[yi]=parz

    plt.plot(yis*0+crystalMinX,zs,'k-')
    plt.plot(yis*0+crystalMaxX,zs2,'k-')
    plt.plot(yis*0+crystalCenterX,zs3,'k')


#draw Detector
    detX=sg['Sdetector'][0];
    detY=sg['Sdetector'][1];
    detZ=sg['Sdetector'][2];
    #plt.plot([detX],[detZ],'k*');

    detdx=np.sin(sg['SdetectorAngle'])*p['geometry']['detectorLength']/2;
    detdz=np.cos(sg['SdetectorAngle'])*p['geometry']['detectorLength']/2;
    plt.plot([detX+detdx, detX+detdx, detX-detdx,detX-detdx, detX+detdx ],[detZ-detdz,detZ-detdz,detZ+detdz,detZ+detdz,detZ-detdz],'k-',linewidth=2);
    plt.ylabel('z [mm]')
    plt.xlabel('x [mm]')
    plt.grid()
#central ray
    CR=np.matrix((sg['Ssource'],sg['Scrystal'],sg['Sdetector']));
    plt.plot(CR[:,0],CR[:,2],'r',linewidth=1);

    return ax

def plotTopViewAOI(p,rrr,ax):
    colores=rrr['colores']
    c=p['crystal']
    sg=p['sg']
    rayres=rrr['rayres']
    E0s=rrr['E0s']
    ev=p['evalu']
    Sdetector=p['sg']['Sdetector']

    maxray=3500
    aois=rrr['aois']
    ThBragg=p['sg']['ThBragg']
    ##
    if (c['variableD2']):
        rs=rayres[:,1,0]#x position of intersections with crystal
        dXs=rs-crystalCenterX
        d2Changes=dXs*d2Variation #Å
        d2loc= d2+d2Changes
        braggThetas=np.arcsin(12398/E0/d2loc)
        cr=(aois-braggThetas)##difference from Th0 in rad
    else:
        cr=(aois-ThBragg)##difference from Th0 in rad
    cr[colores==0]=np.nan
    cr[colores==3]=np.nan

    colorscaleHW=np.nanmax(np.abs(cr)) #half width of the color scale in rad
    r=np.arange(1,min(maxray,np.size(colores)))
    plt.scatter(rayres[r,1,0],rayres[r,1,1],s=10,c=cr[r]*1e3)
    plt.colorbar()

    xl=plt.xlim()
    #plot crystal
    crystalCenterX=sg['Scrystal'][0]
    crystalWidth=c['width']
    crystalDistribution=c['penetrationDepth']
    crystalminX=crystalCenterX-c['length']/2
    crystalmaxX=crystalCenterX+c['length']/2


    cc=crystalWidth/2
    plt.plot([crystalminX, crystalminX ,crystalmaxX ,crystalmaxX, crystalminX],[-1*cc, cc, cc ,-1*cc ,-1*cc],'k-')
    plt.plot([crystalminX, crystalmaxX, crystalmaxX, crystalmaxX, crystalminX],[-1*cc ,cc, cc ,-1*cc ,cc],'k-')

    ## plotting 'rocking curve'
    Xs=rayres[:,1,0]
    sel=np.logical_not(np.isnan(Xs))
    Xs2=(Xs[sel])
    xh=np.histogram(Xs2,bins=50)
    eds=xh[1][0:np.size(xh[1])-1]
    cens=eds+((eds[1]-eds[0])/2)
    rc=xh[0]/np.max(xh[0])
    rc=(rc-1)*cc
    plt.plot(cens,rc,color=[0.8,0.4,0.4],linewidth=3)
#    plt.plot(cens,rc,color=[0.6,1,1],linewidth=3)


    #plt.plot(crystalCenterX,0,'k*')
    plt.xlabel('x [mm]')
    plt.ylabel('y [mm]')
    ax.yaxis.set_label_coords(-0.13,0.5)


    plt.clim(-1000*colorscaleHW ,colorscaleHW*1e3)
    plt.xlim(xl)
    plt.grid()

