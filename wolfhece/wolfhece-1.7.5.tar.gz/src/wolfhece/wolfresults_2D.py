from ast import If
import sys
import wx
from os.path import dirname, exists
from math import floor

import numpy.ma as ma
import numpy as np
import matplotlib.path as mpltPath
from OpenGL.GL import *

from .PyPalette import wolfpalette
from .PyTranslate import _
from .gpuview import GRID_N, Rectangle, VectorField
from .pyshields import get_d_cr,get_d_cr_susp,izbach_d_cr
from .pyviews import WolfViews


try:
    from .libs import wolfpy
except Exception as ex:
    # This convoluted error handling is here to catch an issue
    # which was difficult to track down: wolfpy was there
    # but its DLL were not available.
    
    from importlib.util import find_spec
    s = find_spec('wolfhece.libs.wolfpy')
    from pathlib import Path

    # Not too sure about this find_spec. If the root
    # directory is not the good one, the import search may
    # end up in the site packages, loading the wrong wolfpy.

    base = Path(__file__).parent.parts
    package = Path(s.origin).parent.parts
    is_submodule = (len(base) <= len(package)) and all(i==j for i, j in zip(base, package))

    if is_submodule:
        msg = _("wolfpy was found but we were not able to load it. It may be an issue with its DLL dependencies")
        msg += _("The actual error was: {}").format(str(ex))
    else:
        msg=_('Error importing wolfpy.pyd')
        msg+=_('   Python version : ' + sys.version)
        msg+=_('   If your Python version is not 3.7.x or 3.9.x, you need to compile an adapted library with compile_wcython.py in wolfhece library path')
        msg+=_('   See comments in compile_wcython.py or launch *python compile_wcython.py build_ext --inplace* in :')
        msg+='      ' + dirname(__file__)
        
    raise Exception(msg)

from .wolf_array import WolfArray, getkeyblock, header_wolf, WolfArrayMB
from .mesh2d import wolf2dprev
from .PyVertexvectors import vector

CHOICES_VIEW_2D = {_('Water depth [m]'):'waterdepth', 
                  _('Water level [m]'):'waterlevel', 
                  _('Bottom level [m]'):'topography', 
                  _('Discharge X [m2s-1]'):'qx', 
                  _('Discharge Y [m2s-1]'):'qy', 
                  _('Discharge norm [m2s-1]'):'qnorm', 
                  _('Velocity X [ms-1]'):'ux', 
                  _('Velocity Y [ms-1]'):'uy', 
                  _('Velocity norm [ms-1]'):'unorm', 
                  _('Head [m]'):'head', 
                  _('Froude [-]'):'froude',
                  _('Discharge vector field'):'vector_field_q',
                  _('Velocity vector field'):'vector_field_u',
                  _('Critical grain diameter - Shields'):'critical_diameter_shields',
                  _('Critical grain diameter - Izbach'):'critical_diameter_izbach',
                  _('Critical grain diameter - Suspension 50%'):'critical_diameter_suspension_50',
                  _('Critical grain diameter - Suspension 100%'):'critical_diameter_suspension_100',
                  _('WL + Q'):'wl_q',
                  _('WD + U'):'wd_u',
                  _('Top + WL + Q'):'t_wl_q',
                  _('Top + WD + Q'):'t_wd_q',
                  _('Top + WD + U'):'t_wd_u'
                    } 

class OneWolfResult:

    def __init__(self,fname = None,mold = None):
        self.waterdepth = WolfArray()
        self.top = WolfArray()
        self.qx = WolfArray()
        self.qy = WolfArray()
        self.rough_n = WolfArray()
        self.set_current('waterdepth')
        
        self.critShields = None
        self.critIzbach = None
        self.critSusp50 = None
        self.critSusp100 = None
                
    @property
    def current(self):
        return self._current

    def set_current(self,which):        
        self._which_current = which

        if which=='waterdepth':
            self._current=self.waterdepth
        elif which=='topography':
            self._current=self.top
        elif which=='qx':
            self._current=self.qx
        elif which=='qy':
            self._current=self.qy
        elif which=='qnorm':
            self._current=(self.qx**2.+self.qy**2.)**.5
        elif which=='unorm':
            self._current=(self.qx**2.+self.qy**2.)**.5/self.waterdepth
        elif which=='ux':
            self._current=self.qx/self.waterdepth
        elif which=='uy':
            self._current=self.qy/self.waterdepth
        elif which=='waterlevel':
            self._current=self.waterdepth+self.top
        elif which=='froude':
            self._current=(self.qx**2.+self.qy**2.)**.5/self.waterdepth/(self.waterdepth*9.81)**.5
        elif which=='head':
            self._current=(self.qx**2.+self.qy**2.)**.5/self.waterdepth/(2.*9.81)+self.waterdepth+self.top
        elif which=='vector_field_q':
            self._current=(self.qx**2.+self.qy**2.)**.5
            self._vec_field = VectorField(self.qx.array, self.qy.array, self.qx.get_bounds(), self.qx.dx, self.qy.dy)
        elif which=='vector_field_u':
            ux = self.qx/self.waterdepth
            uy = self.qy/self.waterdepth
            self._current=(ux**2.+uy**2.)**.5
            self._vec_field = VectorField(ux.array, uy.array, ux.get_bounds(), ux.dx, ux.dy)
            
        elif which =='wl_q':
            
            self._current = self.waterdepth+self.top            
            self._view = WolfViews()
            
            ux = self.qx/self.waterdepth
            uy = self.qy/self.waterdepth

            self._view.add_elemts([self._current, VectorField(ux.array, uy.array, self.qx.get_bounds(), self.qx.dx, self.qy.dy)])

        elif which =='wd_u':
            
            self._current = self.waterdepth            
            self._view = WolfViews()
            self._view.add_elemts([self._current, VectorField(self.qx.array, self.qy.array, self.qx.get_bounds(), self.qx.dx, self.qy.dy)])

        elif which =='t_wl_q':

            self._current = self.waterdepth+self.top
            self._view = WolfViews()
            
            self._view.add_elemts([self.top, self._current, VectorField(self.qx.array, self.qy.array, self.qx.get_bounds(), self.qx.dx, self.qy.dy)])

        elif which =='t_wd_q':

            self._current = self.waterdepth
            self.waterdepth.mypal.defaultblue_minmax(self.waterdepth.array)
            self._view = WolfViews()
            
            self._view.add_elemts([self.top, self._current, VectorField(self.qx.array, self.qy.array, self.qx.get_bounds(), self.qx.dx, self.qy.dy)])

        elif which =='t_wd_u':

            self._current = self.waterdepth
            self.waterdepth.mypal.defaultblue_minmax(self.waterdepth.array)
            self._view = WolfViews()
            
            ux = self.qx/self.waterdepth
            uy = self.qy/self.waterdepth
            
            self._view.add_elemts([self.top, self._current, VectorField(ux.array, uy.array, self.qx.get_bounds(), self.qx.dx, self.qy.dy)])
        
        elif which=='critical_diameter_shields':
            if self.critShields is None:
                self.critShields = self.get_critdiam(0)
            self._current = self.critShields
        elif which=='critical_diameter_izbach':
            if self.critIzbach is None:
                self.critIzbach = self.get_critdiam(1)
            self._current = self.critIzbach
        elif which=='critical_diameter_suspension_50':
            if self.critSusp50 is None:
                self.critSusp50 = self.get_critsusp(50)
            self._current = self.critSusp50
        elif which=='critical_diameter_suspension_100':
            if self.critSusp100 is None:
                self.critSusp100 = self.get_critsusp(100)
            self._current = self.critSusp100
            
    def update_pal(self,curpal:wolfpalette,graypal=None,bluepal=None):        
        which = self._which_current

        self._current.mypal = curpal
        self._current.rgb = curpal.get_rgba(self._current.array)
        self._current.rgb[self._current.array.mask] = [1., 1., 1., 1.]
        
        if which == 'wd_u':
            self._view.pals = [bluepal,curpal]
        elif which =='t_wl_q':
            self._view.pals = [graypal,curpal,None]
        elif which =='t_wd_q':
            self._view.pals = [graypal,bluepal,None]
        elif which =='t_wd_u':
            self._view.pals = [graypal,bluepal,None]
        
    def get_critdiam(self,which):

        with wx.lib.busy.BusyInfo(_('Computing critical diameters')):
            wait = wx.BusyCursor()
        
            ij = np.argwhere(self.waterdepth.array>0.)

            diamcrit = WolfArray(mold=self.waterdepth)
            qnorm = (self.qx**2.+self.qy**2.)**.5
            qnorm.array.mask=self.waterdepth.array.mask
                    
            if which==0:
                diam = np.asarray([get_d_cr(qnorm.array[i,j],self.waterdepth.array[i,j],1./self.rough_n.array[i,j])[which] for i,j in ij])
            else:
                diam = np.asarray([izbach_d_cr(qnorm.array[i,j],self.waterdepth.array[i,j]) for i,j in ij])

            diamcrit.array[ij[:,0],ij[:,1]] = diam

            del wait
            return diamcrit
                 
    def get_critsusp(self,which=50):
        
        with wx.lib.busy.BusyInfo(_('Computing critical diameters')):
            wait = wx.BusyCursor()
            ij = np.argwhere(self.waterdepth.array>0.)
            
            diamcrit = WolfArray(mold=self.waterdepth)
            qnorm = (self.qx**2.+self.qy**2.)**.5
            qnorm.array.mask=self.waterdepth.array.mask
                    
            diam = np.asarray([get_d_cr_susp(qnorm.array[i,j],self.waterdepth.array[i,j],1./self.rough_n.array[i,j],which=which) for i,j in ij])
            
            diamcrit.array[ij[:,0],ij[:,1]] = diam
            
            del wait
            return diamcrit
            
    def plot(self, sx=None, sy=None,xmin=None,ymin=None,xmax=None,ymax=None):
        if self._which_current in ['vector_field_q','vector_field_u']:
            self._vec_field.plot(sx, sy,xmin,ymin,xmax,ymax)
        elif self._which_current in ['wl_q','wd_u','t_wl_q','t_wd_q','t_wd_u']:
            self._view.plot(sx, sy,xmin,ymin,xmax,ymax)
        else:
            self._current.plot(sx, sy,xmin,ymin,xmax,ymax)
        
    def get_values_labels(self,i,j):        
        which = self._which_current
        
        labels = list(CHOICES_VIEW_2D.keys())
        val = list(CHOICES_VIEW_2D.values())
        
        mylab = [labels[val.index(which)]]
        myval = [self._current.array[i,j]]
    
        if which in ['wl_q','wd_u','t_wl_q','t_wd_q','t_wd_u']:

            mylab = [labels[val.index('topography')],
                     labels[val.index('waterdepth')],
                     labels[val.index('waterlevel')],
                     labels[val.index('qx')],
                     labels[val.index('qy')],
                     labels[val.index('qnorm')],
                     labels[val.index('ux')],
                     labels[val.index('uy')],
                     labels[val.index('unorm')],
                     labels[val.index('froude')]
                     ]

            top = self.top.array[i,j]            
            h  = self.waterdepth.array[i,j]            
            
            sl = h+top
            
            qx = self.qx.array[i,j]
            qy = self.qy.array[i,j]
            qnorm = (qx**2.+qy**2.)**.5
            
            ux = qx/h
            uy = qy/h
            
            unorm = (ux**2.+uy**2.)**.5
            
            fr = unorm/(9.81*h)**.5
            myval = [top,
                     h,
                     sl,
                     qx,
                     qy,
                     qnorm,
                     ux,
                     uy,
                     unorm,
                     fr]

        return myval,mylab
            
class Wolfresults_2D(object):
    
    myblocks:dict
    myheaders:dict

    def __init__(self,fname = None,mold = None, eps=0.):
        self.filename=""
        self.filenamegen=self.filename
        
        self.myparams =None
        
        self.nb_blocks = 0
        self.loaded=True
        self.current_result = -1
        self.mypal = wolfpalette(None,'Colors')
        self.mypal.default16()
        self.mypal.automatic = True

        self.epsilon = eps
        
        self.nbnotnull=99999
        self.parentgui=None
        self.idx=None

        self.plotted=False
        self.plotting=False
        
        self._which_current_view = _('Water depth [m]')

        if fname is not None:
            #self.filename = fname.ljust(255)
            self.filename = fname
            self.filenamegen=self.filename
            
            with open(self.filename + '.trl') as f:
                trl=f.read().splitlines()
                self.translx=float(trl[1])
                self.transly=float(trl[2])

            wolfpy.r2d_init(self.filename.ljust(255).encode('ansi'))
            self.nb_blocks = wolfpy.r2d_nbblocks()
            self.myblocks={}
            self.myheaders={}
            for i in range(self.nb_blocks):
                curblock = OneWolfResult()
                self.myblocks[getkeyblock(i)] = curblock
                nbx,nby,dx,dy,ox,oy,tx,ty = wolfpy.r2d_hblock(i+1)
                
                curhead = self.myheaders[getkeyblock(i)]=header_wolf()
                curhead.nbx = nbx
                curhead.nby = nby
                curhead.origx = ox
                curhead.origy = oy
                curhead.dx = dx
                curhead.dy = dy
                curhead.translx = self.translx
                curhead.transly = self.transly
                
                self.myblocks[getkeyblock(i)].waterdepth.dx = dx
                self.myblocks[getkeyblock(i)].waterdepth.dy = dy
                self.myblocks[getkeyblock(i)].waterdepth.nbx = nbx
                self.myblocks[getkeyblock(i)].waterdepth.nby = nby
                self.myblocks[getkeyblock(i)].waterdepth.origx = ox
                self.myblocks[getkeyblock(i)].waterdepth.origy = oy
                self.myblocks[getkeyblock(i)].waterdepth.translx = self.translx
                self.myblocks[getkeyblock(i)].waterdepth.transly = self.transly

                self.myblocks[getkeyblock(i)].top.dx = dx
                self.myblocks[getkeyblock(i)].top.dy = dy
                self.myblocks[getkeyblock(i)].top.nbx = nbx
                self.myblocks[getkeyblock(i)].top.nby = nby
                self.myblocks[getkeyblock(i)].top.origx = ox
                self.myblocks[getkeyblock(i)].top.origy = oy
                self.myblocks[getkeyblock(i)].top.translx = self.translx
                self.myblocks[getkeyblock(i)].top.transly = self.transly
                
                self.myblocks[getkeyblock(i)].qx.dx = dx
                self.myblocks[getkeyblock(i)].qx.dy = dy
                self.myblocks[getkeyblock(i)].qx.nbx = nbx
                self.myblocks[getkeyblock(i)].qx.nby = nby
                self.myblocks[getkeyblock(i)].qx.origx = ox
                self.myblocks[getkeyblock(i)].qx.origy = oy
                self.myblocks[getkeyblock(i)].qx.translx = self.translx
                self.myblocks[getkeyblock(i)].qx.transly = self.transly

                self.myblocks[getkeyblock(i)].qy.dx = dx
                self.myblocks[getkeyblock(i)].qy.dy = dy
                self.myblocks[getkeyblock(i)].qy.nbx = nbx
                self.myblocks[getkeyblock(i)].qy.nby = nby
                self.myblocks[getkeyblock(i)].qy.origx = ox
                self.myblocks[getkeyblock(i)].qy.origy = oy
                self.myblocks[getkeyblock(i)].qy.translx = self.translx
                self.myblocks[getkeyblock(i)].qy.transly = self.transly

                self.myblocks[getkeyblock(i)].rough_n.dx = dx
                self.myblocks[getkeyblock(i)].rough_n.dy = dy
                self.myblocks[getkeyblock(i)].rough_n.nbx = nbx
                self.myblocks[getkeyblock(i)].rough_n.nby = nby
                self.myblocks[getkeyblock(i)].rough_n.origx = ox
                self.myblocks[getkeyblock(i)].rough_n.origy = oy
                self.myblocks[getkeyblock(i)].rough_n.translx = self.translx
                self.myblocks[getkeyblock(i)].rough_n.transly = self.transly

            self.allocate_ressources()
            self.read_topography()
            self.read_ini_mb()
            
            self.loaded_rough = False

        self.nbx = 1
        self.nby = 1

        ox=99999.
        oy=99999.
        ex=-99999.
        ey=-99999.
        for curblock in self.myblocks.values():
            curblock:OneWolfResult
            curhead=curblock.waterdepth.get_header(False)
            ox=min(ox,curhead.origx)
            oy=min(oy,curhead.origy)
            ex=max(ex,curhead.origx+float(curhead.nbx)*curhead.dx)
            ey=max(ey,curhead.origy+float(curhead.nby)*curhead.dy)
        self.dx = ex-ox
        self.dy = ey-oy
        self.origx = ox
        self.origy = oy

    def read_param_simul(self):
        self.myparams = wolf2dprev.prev_parameters_simul(self)
        self.myparams.read_file(self.filename)
    
    def get_currentview(self):    
        return self._which_current_view

    def set_currentview(self,which=None):    
                
        if which is None:
            which = self._which_current_view        
        
        if which in CHOICES_VIEW_2D.keys():
            self._which_current_view = which

            self.plotting=True
            self.mimic_plotdata()
            
            self.delete_lists() #on efface les listes OpenGL car on va remplacer l'objet, or il peut être nue combinaison de cartes de base

            if which in [_('Critical grain diameter - Shields'), 
                         _('Critical grain diameter - Izbach'), 
                         _('Critical grain diameter - Suspension 50%'),
                         _('Critical grain diameter - Suspension 100%')]:
                
                if not self.loaded_rough:
                    self.read_roughness_param()

            for curblock in self.myblocks.values():
                curblock:OneWolfResult
                curblock.set_current(CHOICES_VIEW_2D[which])                    
                    
            self.mypal.automatic = True
            self.reset_plot()
            
            self.plotting=False
            self.mimic_plotdata()                 

    def allocate_ressources(self):
        for i in range(self.nb_blocks):
            self.myblocks[getkeyblock(i)].waterdepth.allocate_ressources()
            self.myblocks[getkeyblock(i)].top.allocate_ressources()
            self.myblocks[getkeyblock(i)].qx.allocate_ressources()
            self.myblocks[getkeyblock(i)].qy.allocate_ressources()

    def read_topography(self):

        with open(self.filename.strip() + '.topini','rb') as f:
            for i in range(self.nb_blocks):
                nbx=self.myblocks[getkeyblock(i)].top.nbx
                nby=self.myblocks[getkeyblock(i)].top.nby
                nbbytes=nbx*nby*4
                self.myblocks[getkeyblock(i)].top.array = ma.masked_equal(np.frombuffer(f.read(nbbytes),dtype=np.float32),0.)
                self.myblocks[getkeyblock(i)].top.array = self.myblocks[getkeyblock(i)].top.array.reshape(nbx,nby,order='F')
    
    def read_ini_mb(self):

        if exists(self.filename.strip() + '.hbinb'):
            with open(self.filename.strip() + '.hbinb','rb') as f:
                for i in range(self.nb_blocks):
                    nbx=self.myblocks[getkeyblock(i)].waterdepth.nbx
                    nby=self.myblocks[getkeyblock(i)].waterdepth.nby
                    nbbytes=nbx*nby*4
                    self.myblocks[getkeyblock(i)].waterdepth.array = ma.masked_equal(np.frombuffer(f.read(nbbytes),dtype=np.float32),0.)
                    self.myblocks[getkeyblock(i)].waterdepth.array = self.myblocks[getkeyblock(i)].waterdepth.array.reshape(nbx,nby,order='F')

        if exists(self.filename.strip() + '.qxbinb'):
            with open(self.filename.strip() + '.qxbinb','rb') as f:
                for i in range(self.nb_blocks):
                    nbx=self.myblocks[getkeyblock(i)].qx.nbx
                    nby=self.myblocks[getkeyblock(i)].qx.nby
                    nbbytes=nbx*nby*4
                    self.myblocks[getkeyblock(i)].qx.array = ma.masked_equal(np.frombuffer(f.read(nbbytes),dtype=np.float32),0.)
                    self.myblocks[getkeyblock(i)].qx.array = self.myblocks[getkeyblock(i)].qx.array.reshape(nbx,nby,order='F')

        if exists(self.filename.strip() + '.qybinb'):
            with open(self.filename.strip() + '.qybinb','rb') as f:
                for i in range(self.nb_blocks):
                    nbx=self.myblocks[getkeyblock(i)].qy.nbx
                    nby=self.myblocks[getkeyblock(i)].qy.nby
                    nbbytes=nbx*nby*4
                    self.myblocks[getkeyblock(i)].qy.array = ma.masked_equal(np.frombuffer(f.read(nbbytes),dtype=np.float32),0.)
                    self.myblocks[getkeyblock(i)].qy.array = self.myblocks[getkeyblock(i)].qy.array.reshape(nbx,nby,order='F')

    def read_roughness_param(self):

        with open(self.filename.strip() + '.frotini','rb') as f:
            for i in range(self.nb_blocks):
                nbx=self.myblocks[getkeyblock(i)].rough_n.nbx
                nby=self.myblocks[getkeyblock(i)].rough_n.nby
                nbbytes=nbx*nby*4
                self.myblocks[getkeyblock(i)].rough_n.array = ma.masked_equal(np.frombuffer(f.read(nbbytes),dtype=np.float32),0.)
                self.myblocks[getkeyblock(i)].rough_n.array = self.myblocks[getkeyblock(i)].rough_n.array.reshape(nbx,nby,order='F')
        self.loaded_rough = True

    def get_nbresults(self):
        wolfpy.r2d_init(self.filename.ljust(255).encode('ansi'))
        return  wolfpy.r2d_getnbresults()
    
    def read_oneblockresult_withoutmask(self,which=-1,whichblock=-1):
        if whichblock!=-1:
            nbx = self.myblocks[getkeyblock(whichblock,False)].waterdepth.nbx
            nby = self.myblocks[getkeyblock(whichblock,False)].waterdepth.nby
            self.myblocks[getkeyblock(whichblock,False)].waterdepth.array, self.myblocks[getkeyblock(whichblock,False)].qx.array, self.myblocks[getkeyblock(whichblock,False)].qy.array = wolfpy.r2d_getresults(which,nbx,nby,whichblock)

    def read_oneblockresult(self,which=-1,whichblock=-1):
        if whichblock!=-1:
            
            self.read_oneblockresult_withoutmask(which,whichblock)
            self.myblocks[getkeyblock(whichblock,False)].waterdepth.array=ma.masked_equal(self.myblocks[getkeyblock(whichblock,False)].waterdepth.array,0.)
            
            if self.epsilon > 0.:
                self.myblocks[getkeyblock(whichblock,False)].waterdepth.mask_lowerequal(self.epsilon)
            
            self.myblocks[getkeyblock(whichblock,False)].qx.array=ma.masked_where(self.myblocks[getkeyblock(whichblock,False)].waterdepth.array.mask,self.myblocks[getkeyblock(whichblock,False)].qx.array)
            self.myblocks[getkeyblock(whichblock,False)].qy.array=ma.masked_where(self.myblocks[getkeyblock(whichblock,False)].waterdepth.array.mask,self.myblocks[getkeyblock(whichblock,False)].qy.array)

    def read_oneresult(self,which=-1):
        wolfpy.r2d_init(self.filename.ljust(255).encode('ansi'))
        for i in range(self.nb_blocks):
            self.read_oneblockresult(which,i+1)
            
        self.current_result = which
        self.loaded=True

    def get_values_as_wolf(self,i,j,which_block=1):
        h=-1
        qx=-1
        qy=-1
        vx=-1
        vy=-1
        vabs=-1
        fr=-1
        
        nbx = self.myblocks[getkeyblock(which_block,False)].waterdepth.nbx
        nby = self.myblocks[getkeyblock(which_block,False)].waterdepth.nby

        if(i>0 and i<=nbx and j>0 and j<=nby):
            h = self.myblocks[getkeyblock(which_block,False)].waterdepth.array[i-1,j-1]
            top = self.myblocks[getkeyblock(which_block,False)].top.array[i-1,j-1]
            qx = self.myblocks[getkeyblock(which_block,False)].qx.array[i-1,j-1]
            qy = self.myblocks[getkeyblock(which_block,False)].qy.array[i-1,j-1]
            if(h>0.):
                vx = qx/h
                vy = qy/h
                vabs=(vx**2.+vy**2.)**.5
                fr = vabs/(9.81*h)**.5
        
        return h,qx,qy,vx,vy,vabs,fr,h+top,top
    
    def get_header_block(self,which_block=1) -> header_wolf:
        return self.myheaders[getkeyblock(which_block,False)]
    
    def get_xy_infootprint_vect(self, myvect: vector,which_block=1) -> np.ndarray:

        """
        Returns:
            numpy array content les coordonnées xy des mailles dans l'empreinte du vecteur
        """
        
        myptsij = self.get_ij_infootprint_vect(myvect, which_block)
        mypts=np.asarray(myptsij.copy(),dtype=np.float64)
        
        lochead = self.get_header_block(which_block)

        mypts[:,0] = (mypts[:,0]+.5)*lochead.dx +lochead.origx +lochead.translx
        mypts[:,1] = (mypts[:,1]+.5)*lochead.dy +lochead.origy +lochead.transly
                
        return mypts,myptsij

    def get_ij_infootprint_vect(self, myvect: vector, which_block=1) -> np.ndarray:
        
        """
        Returns:
            numpy array content les indices ij des mailles dans l'empreinte du vecteur
        """
        
        lochead = self.get_header_block(which_block)
        nbx = lochead.nbx
        nby = lochead.nby
        
        i1, j1 = self.get_ij_from_xy(myvect.minx, myvect.miny, which_block)
        i2, j2 = self.get_ij_from_xy(myvect.maxx, myvect.maxy, which_block) 
        i1 = max(i1,0)       
        j1 = max(j1,0)       
        i2 = min(i2,nbx-1)       
        j2 = min(j2,nby-1)       
        xv,yv = np.meshgrid(np.arange(i1,i2+1),np.arange(j1,j2+1))
        mypts = np.hstack((xv.flatten()[:,np.newaxis],yv.flatten()[:,np.newaxis]))
        
        return mypts
    
    def get_xy_inside_polygon(self, myvect: vector, usemask=True):
        '''
        Obtention des coordonnées contenues dans un polygone
         usemask = restreint les éléments aux éléments non masqués de la matrice
        '''

        myvect.find_minmax()

        mypointsxy={}

        myvert = myvect.asnparray()
        path = mpltPath.Path(myvert)
        
        for curblock in range(self.nb_blocks):
            locpointsxy,locpointsij = self.get_xy_infootprint_vect(myvect,curblock+1)    
            inside = path.contains_points(locpointsxy)

            locpointsxy = locpointsxy[np.where(inside)]

            if usemask and len(locpointsxy)>0:
                locpointsij = locpointsij[np.where(inside)]
                mymask = np.logical_not(self.myblocks[getkeyblock(curblock)].current.array.mask[locpointsij[:, 0], locpointsij[:, 1]])
                locpointsxy = locpointsxy[np.where(mymask)]

            mypointsxy[getkeyblock(curblock)]=locpointsxy

        return mypointsxy
    
    def get_values_insidepoly(self,myvect:vector, usemask=True, agglo=True, getxy=False):
        
        myvalues={}
        myvaluesel={}
        mypoints = self.get_xy_inside_polygon(myvect, usemask)

        for curblock in range(self.nb_blocks):
            if len(mypoints[getkeyblock(curblock)])>0:
                locval = np.asarray([self.get_value(cur[0], cur[1], True) for cur in mypoints[getkeyblock(curblock)]])
                locel = np.asarray([self.get_value_elevation(cur[0],cur[1],True) for cur in mypoints[getkeyblock(curblock)]])

                locval=locval[np.where(locval!=-1)]
                locel=locel[np.where(locel!=-1)]
                
                myvalues[getkeyblock(curblock)]=locval
                myvaluesel[getkeyblock(curblock)]=locel
            else:
                myvalues[getkeyblock(curblock)]=np.asarray([])
                myvaluesel[getkeyblock(curblock)]=np.asarray([])
        
        if agglo:
            myvalues   = np.concatenate([cur for cur in myvalues.values()])
            myvaluesel = np.concatenate([cur for cur in myvaluesel.values()])
            mypoints   = np.concatenate([cur for cur in mypoints.values()])
        
        if self._which_current_view == _('Water level [m]'):
            if getxy:
                return myvalues,myvaluesel,mypoints
            else:
                return myvalues,myvaluesel
        else:
            if getxy:
                return myvalues,None,mypoints
            else:
                return myvalues,None

    def get_values_from_xy(self,x,y,abs=False):
        h=-1
        qx=-1
        qy=-1
        vx=-1
        vy=-1
        vabs=-1
        fr=-1
        
        exists=False
        for which_block in range(1,self.nb_blocks+1):
            nbx = self.myblocks[getkeyblock(which_block,False)].waterdepth.nbx
            nby = self.myblocks[getkeyblock(which_block,False)].waterdepth.nby
            i,j=self.get_ij_from_xy(x,y,which_block=which_block,abs=abs)

            if(i>0 and i<=nbx and j>0 and j<=nby):
                h = self.myblocks[getkeyblock(which_block,False)].waterdepth.array[i-1,j-1]
                top = self.myblocks[getkeyblock(which_block,False)].top.array[i-1,j-1]
                qx = self.myblocks[getkeyblock(which_block,False)].qx.array[i-1,j-1]
                qy = self.myblocks[getkeyblock(which_block,False)].qy.array[i-1,j-1]
                
                exists = top>0.
                
                if(h>0.):
                    vx = qx/h
                    vy = qy/h
                    vabs=(vx**2.+vy**2.)**.5
                    fr = vabs/(9.81*h)**.5
                    exists=True
                if exists:
                    break

        if exists:
            return (h,qx,qy,vx,vy,vabs,fr,h+top,top),(i,j,which_block)
        else:
            return (-1,-1,-1,-1,-1,-1,-1),('-','-','-')

    def get_value(self,x,y,abs=False):
        h=-1
        exists=False
        for which_block in range(1,self.nb_blocks+1):
            nbx = self.myblocks[getkeyblock(which_block,False)].waterdepth.nbx
            nby = self.myblocks[getkeyblock(which_block,False)].waterdepth.nby
            i,j=self.get_ij_from_xy(x,y,which_block=which_block,abs=False)

            if(i>0 and i<=nbx and j>0 and j<=nby):
                h = self.myblocks[getkeyblock(which_block,False)].waterdepth.array[i-1,j-1]
                val = self.myblocks[getkeyblock(which_block,False)].current.array[i-1,j-1]

                if h is not np.nan:
                    exists=np.abs(h)>0.
                    if exists:
                        break

        if exists:
            return val
        else:
            return -1

    def get_values_labels(self,x,y,abs=False):
        h=-1
        exists=False
        
        for which_block in range(1,self.nb_blocks+1):
            nbx = self.myblocks[getkeyblock(which_block,False)].waterdepth.nbx
            nby = self.myblocks[getkeyblock(which_block,False)].waterdepth.nby
            i,j=self.get_ij_from_xy(x,y,which_block=which_block,abs=False)

            if(i>0 and i<=nbx and j>0 and j<=nby):
                                
                h = self.myblocks[getkeyblock(which_block,False)].waterdepth.array[i-1,j-1]

                if h is not np.nan:
                    exists=np.abs(h)>0.
                    if exists:
                        break

        if exists:
            vals,labs = self.myblocks[getkeyblock(which_block,False)].get_values_labels(i-1,j-1)
            return vals,labs
        else:
            return -1

    def get_value_elevation(self,x,y,abs=False):
        h=-1
        exists=False
        for which_block in range(1,self.nb_blocks+1):
            nbx = self.myblocks[getkeyblock(which_block,False)].waterdepth.nbx
            nby = self.myblocks[getkeyblock(which_block,False)].waterdepth.nby
            i,j=self.get_ij_from_xy(x,y,which_block=which_block,abs=False)

            if(i>0 and i<=nbx and j>0 and j<=nby):
                h = self.myblocks[getkeyblock(which_block,False)].waterdepth.array[i-1,j-1]
                val = self.myblocks[getkeyblock(which_block,False)].top.array[i-1,j-1]

                if h is not np.nan:
                    exists=np.abs(h)>0.
                    if exists:
                        break

        if exists:
            return val
        else:
            return -1

    def get_xy_from_ij(self,i,j,which_block,abs=False):
        x,y = self.myblocks[getkeyblock(which_block,False)].waterdepth.get_xy_from_ij(i,j)
        if abs:
            return x+self.translx,y+self.transly
        else:
            return x,y

    def get_ij_from_xy(self,x,y,which_block,abs=False):
        locx=x
        locy=y
        if abs:
            locx=x-self.translx
            locy=y-self.transly
        
        i,j = self.myblocks[getkeyblock(which_block,False)].waterdepth.get_ij_from_xy(locx,locy)
        return i+1,j+1 # En indices WOLF

    def get_blockij_from_xy(self,x,y,abs=False):
        locx=x
        locy=y
        if abs:
            locx=x-self.translx
            locy=y-self.transly

        ret=self.get_values_from_xy(x,y,abs)
        
        return ret[1]

    # def extract_allsteps(x,y):
    #     myvalues=np.zeros()

    def check_plot(self):
        self.plotted = True
        self.mimic_plotdata()
        
        if not self.loaded and self.filename!='':
            self.read_oneresult(self.current_result)
            self.reset_plot()
    
    def uncheck_plot(self,unload=False):
        self.plotted = False
        self.mimic_plotdata()
            
    def link_palette(self):
        for curblock in self.myblocks.values():
            curblock:OneWolfResult
            curblock.update_pal(self.mypal,self.palgray,self.palblue)           
    
    def get_min_max(self,which):
        
        if which == 'topography':           
            min = np.min([np.min(curblock.top.array) for curblock in self.myblocks.values()])
            max = np.max([np.max(curblock.top.array) for curblock in self.myblocks.values()])
        elif which == 'waterdepth':           
            min = np.min([np.min(curblock.waterdepth.array) for curblock in self.myblocks.values()])
            max = np.max([np.max(curblock.waterdepth.array) for curblock in self.myblocks.values()])
        elif which == 'current':           
            min = np.min([np.min(curblock.current.array) for curblock in self.myblocks.values()])
            max = np.max([np.max(curblock.current.array) for curblock in self.myblocks.values()])
            
        return min,max
    
    def get_working_array(self,onzoom=[]):
        
        if onzoom!=[]:
            allarrays=[]
            for curblock in self.myblocks.values():
                curblock:OneWolfResult
                istart,jstart = curblock._current.get_ij_from_xy(onzoom[0],onzoom[2])
                iend,jend = curblock._current.get_ij_from_xy(onzoom[1],onzoom[3])
                
                istart= 0 if istart < 0 else istart
                jstart= 0 if jstart < 0 else jstart
                iend= curblock._current.nbx if iend > curblock._current.nbx else iend
                jend= curblock._current.nby if jend > curblock._current.nby else jend
                
                partarray=curblock._current.array[istart:iend,jstart:jend]
                partarray=partarray[partarray.mask==False]
                if len(partarray)>0:
                    allarrays.append(partarray.flatten())
            
            allarrays=np.concatenate(allarrays)
        else:
            allarrays = np.concatenate([curblock.current.array[curblock.current.array.mask==False].flatten() for curblock in self.myblocks.values()])
        
        self.nbnotnull = allarrays.count()
        
        return allarrays
    
    def updatepalette(self,which=0,onzoom=[]):
            
        self.palgray = wolfpalette()
        self.palblue = wolfpalette()
        
        self.palgray.defaultgray()
        self.palblue.defaultblue()
        
        self.palgray.values[0],self.palgray.values[-1] = self.get_min_max('topography')
        self.palblue.values[0],self.palblue.values[-1] = self.get_min_max('waterdepth')
        
        if self.mypal.automatic:
            self.mypal.default16()
            self.mypal.isopop(self.get_working_array(onzoom=onzoom),self.nbnotnull)
        
        self.link_palette()

    def delete_lists(self):
        for curblock in self.myblocks.values():
            curblock:OneWolfResult
            curblock._current.delete_lists()

    def mimic_plotdata(self): 
        for curblock in self.myblocks.values():
            curblock:OneWolfResult
            curblock._current.plotted = self.plotted
            curblock._current.plotting = self.plotting
            
    def plot(self, sx=None, sy=None,xmin=None,ymin=None,xmax=None,ymax=None):
        
        self.plotting=True
        self.mimic_plotdata()
        
        for curblock in self.myblocks.values():
            curblock:OneWolfResult
            curblock.plot(sx, sy,xmin,ymin,xmax,ymax)
        
        if self.myparams is not None:
            self.myparams.clfbx.myzones.plot()
            self.myparams.clfby.myzones.plot()
        
        self.plotting=False
        self.mimic_plotdata()
            
    def fillonecellgrid(self,curscale,loci,locj,force=False):
        for curblock in self.myblocks.values():
            curblock:OneWolfResult
            curblock._current.fillonecellgrid(curscale,loci,locj,force)    
            
    def set_current(self,which):

        for curblock in self.myblocks.values():
            curblock:OneWolfResult
            curblock.set_current(which)    
            
    def next_result(self):
        
        nb = self.get_nbresults()
        
        if self.current_result==-1:
            self.read_oneresult(-1)
        else:
            self.current_result+=1
            self.current_result = min(nb,self.current_result)
            self.read_oneresult(self.current_result)
            
            self.reset_plot()
    
    def reset_plot(self,whichpal=0):
        self.delete_lists()
        self.get_working_array()
        self.updatepalette(whichpal)
    
    def transfer_ic(self,myvector):
        
        dlg = wx.MessageDialog(None,_('You will transfer the node values covered by the active vector to an other model.') + '\n\n' + 'Continue ?', style = wx.YES_NO)
        ret = dlg.ShowModal()
        dlg.Destroy()
        if ret == wx.ID_NO:
            return
        
        dlg = wx.DirDialog(None,_('Please select the directory of the model'),style = wx.FD_OPEN)  
        ret = dlg.ShowModal()
        if ret == wx.ID_CANCEL:
            dlg.Destroy()
            return
        
        mydir = dlg.GetPath()
        
              
        pass