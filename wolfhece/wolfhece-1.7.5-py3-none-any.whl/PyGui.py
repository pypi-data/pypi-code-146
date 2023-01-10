from os import path,scandir
import wx
from wx.lib.busy import BusyInfo

from .apps.splashscreen import WolfLauncher
from .wolf_array import WOLF_ARRAY_FULL_LOGICAL, WOLF_ARRAY_MB_SINGLE, WolfArray,getkeyblock, WolfArray_Sim2D
from .PyTranslate import _
from .PyDraw import WolfMapViewer,imagetexture
from .PyParams import Wolf_Param
from .PyVertexvectors import Grid
from .RatingCurve import SPWMIGaugingStations,SPWDCENNGaugingStations
from .PyGuiHydrology import GuiHydrology
from .Results2DGPU import wolfres2DGPU
from .hydrology.Catchment import Catchment
from .hydrology.forcedexchanges import forced_exchanges
from .mesh2d.wolf2dprev import *
from .hydrometry.kiwis import hydrometry,URL_SPW

class GenMapManager(wx.Frame):
    allviews:WolfMapViewer

    def __init__(self,splash=True, *args, **kw):
        if splash:
            MySplash = WolfLauncher()        
        super().__init__(*args, **kw)
        self.mylogs = wx.LogWindow(None,_('Informations'))     
        self.mylogs.PassMessages(False) # évite que les messages ne soit affichés en popup en plus de la fenêtre de Logs

    def add_grid(self):
        mygrid=Grid(1000.)
        self.allviews.add_object('vector',newobj=mygrid,ToCheck=False,id='Grid')

    def add_WMS(self):
        xmin=0
        xmax=0
        ymin=0
        ymax=0
        orthos={'IMAGERIE':{'1971':'ORTHO_1971','1994-2000':'ORTHO_1994_2000',
                        '2006-2007':'ORTHO_2006_2007',
                        '2009-2010':'ORTHO_2009_2010',
                        '2012-2013':'ORTHO_2012_2013',
                        '2015':'ORTHO_2015','2016':'ORTHO_2016','2017':'ORTHO_2017',
                        '2018':'ORTHO_2018','2019':'ORTHO_2019','2020':'ORTHO_2020',
                        '2021':'ORTHO_2021'}}
        for idx,(k,item) in enumerate(orthos.items()):
            for kdx,(m,subitem) in enumerate(item.items()):
                self.allviews.add_object(which='wmsback',
                            newobj=imagetexture('PPNC',m,k,subitem,
                            self.allviews,xmin,xmax,ymin,ymax,-99999,1024),
                            ToCheck=False,id='PPNC '+m)
        self.allviews.add_object(which='wmsback',
                    newobj=imagetexture('PPNC','Orthos France','OI.OrthoimageCoverage.HR','',
                    self.allviews,xmin,xmax,ymin,ymax,-99999,1024,France=True,epsg='EPSG:27563'),
                    ToCheck=False,id='Orthos France')

        forelist={'EAU':{'Aqualim':'RES_LIMNI_DGARNE','Alea':'ALEA_INOND','Lidaxes':'LIDAXES','Juillet 2021':'ZONES_INONDEES','Juillet 2021 IDW':'ZONES_INONDEES$IDW'},
                    'LIMITES':{'Secteurs Statistiques':'LIMITES_QS_STATBEL'},
                    'INSPIRE':{'Limites administratives':'AU_wms'},
                    'PLAN_REGLEMENT':{'Plan Percellaire':'CADMAP_2021_PARCELLES'}}
        
        for idx,(k,item) in enumerate(forelist.items()):
            for kdx,(m,subitem) in enumerate(item.items()):
                self.allviews.add_object(which='wmsfore',
                            newobj=imagetexture('PPNC',m,k,subitem,
                            self.allviews,xmin,xmax,ymin,ymax,-99999,1024),
                            ToCheck=False,id=m)        

class MapManager(GenMapManager):
    def __init__(self,*args, **kw):
        super().__init__(*args, **kw)
        self.allviews=WolfMapViewer(None,'Wolf - main data manager')
        self.add_grid()
        self.add_WMS()

        if exists('spw/stations.csv'):
            self.SPWhydrometry=hydrometry(dir='spw')
        else:
            self.SPWhydrometry=hydrometry(URL_SPW)
        self.allviews.add_object(which='other',newobj=self.SPWhydrometry,ToCheck=False,id='SPW hydrometry')


class GPU2DModel(GenMapManager):

    mydir:str
    files_results_array:dict
    mybed:WolfArray

    def __init__(self,dir:str='', *args, **kw):
        super(GPU2DModel, self).__init__(*args, **kw)
        
        self.allviews=WolfMapViewer(None,'Wolf GPU 2D')
        self.add_grid()
        self.add_WMS()

        if dir=='':
            idir=wx.DirDialog(None,"Choose Directory")
            if idir.ShowModal() == wx.ID_CANCEL:
                return
            self.mydir =idir.GetPath()
        else:
            self.mydir=path.normpath(dir)

        ext=['.top','.frott','.cls_pos','.cls_Z','.hbin','.zbin','.srcq']
        for myext in ext:
            if path.exists(self.mydir+'//simul'+myext):
                self.allviews.add_object(which='array',filename=self.mydir+'//simul'+myext,id=myext,ToCheck=False)
        
        self.mybed=WolfArray(self.mydir +'//simul.top')
        self.result = wolfres2DGPU(self.mydir,self.mybed,parent=self)
        self.allviews.add_object(which='array',newobj=self.result,id='res1',ToCheck=False)

        """self.files_results_array={}
        self.files_results_array['H']=[]
        idx=101
        while path.exists(self.mydir+'//out'+str(idx)+'r.bin'):
            self.files_results_array['H'].append(['out'+str(idx)+'r.bin','step '+str(idx)])
            idx+=1

        for curfile in self.files_results_array['H']:
            curext=curfile[0]
            curidx=curfile[1]
            self.allviews.add_object(which='array',filename=self.mydir+'//'+curext,id=curidx,ToCheck=False)
        """

        self.allviews.findminmax(True)        
        self.allviews.Autoscale(False)
    
class HydrologyModel(GenMapManager):

    mydir:str
    mydircharact:str
    mydirwhole:str
    files_hydrology_array:dict
    files_hydrology_vectors:dict
    mainparams:Wolf_Param
    basinparams:Wolf_Param
    SPWstations:SPWMIGaugingStations
    DCENNstations:SPWDCENNGaugingStations
    mycatchment:Catchment
    myexchanges:forced_exchanges

    def __init__(self,dir:str='', splash=True, *args, **kw):
        super(HydrologyModel, self).__init__(splash=splash, *args, **kw)

        self.SPWstations=SPWMIGaugingStations()
        self.DCENNstations=SPWDCENNGaugingStations()

        if dir=='':
            idir=wx.DirDialog(None,"Choose Directory")
            if idir.ShowModal() == wx.ID_CANCEL:
                return
            self.mydir =idir.GetPath()
        else:
            self.mydir=path.normpath(dir)
            
        self.mydircharact=path.join(self.mydir,'Characteristic_maps\\Drainage_basin')
        self.mydirwhole=path.join(self.mydir,'Whole_basin\\')
        
        self.mycatchment = Catchment('Mysim',self.mydir,False,True)
        self.myexchanges = forced_exchanges(self.mydir)

        self.allviews=GuiHydrology(title='Model : '+self.mydir)

        self.files_hydrology_array={'Characteristic_maps':[
            ('.b','Raw elevation [m]'),
            ('corr.b','Corrected elevation [m]'),
            #('diff.b','Corrections (corr-raw) [m]'),
            ('.nap','Mask [-]'),
            ('.sub','SubBasin index [-]'),
            ('.cnv','Accumulation [km²]'),
            ('.time','Total time [s]'),
            ('.coeff','RunOff coeff [-]'),
            ('.slope','Slope [-]'),
            ('.reachs','Reach index [-]'),
            ('.strahler','Strahler index [-]'),
            ('.reachlevel','Reach accumulation [-]'),
            ('.landuse1','Woodlands [m²]'),
            ('.landuse2','Pastures [m²]'),
            ('.landuse3','Cultivated [m²]'),
            ('.landuse4','Pavements [m²]'),
            ('.landuse5','Water [m²]'),
            ('.landuse6','River [m²]'),
            ('.landuse_limited_area','LandUse Verif'),
            ('.principal_landuse_cropped','Principal landuse [-]'),
            ('_encode.sub','Coded index SubB [-]')]}

        self.files_hydrology_vectors={'Characteristic_maps':[('.delimit.vec','Watershed')],
                                      'Whole_basin':[('Rain_basin_geom.vec','Rain geom'),
                                                     ('Evap_basin_geom.vec','Evapotranspiration geom')]}   

        for curfile in self.files_hydrology_array['Characteristic_maps']:
            curext=curfile[0]
            curidx=curfile[1]
            self.allviews.add_object(which='array',filename=self.mydircharact+curext,id=curidx,ToCheck=False)

        for curfile in self.files_hydrology_vectors['Characteristic_maps']:
            curext=curfile[0]
            curidx=curfile[1]
            self.allviews.add_object(which='vector',filename=self.mydircharact+curext,id=curidx,ToCheck=False)
        
        for curfile in self.files_hydrology_vectors['Whole_basin']:
            curext=curfile[0]
            curidx=curfile[1]
            if path.exists(self.mydirwhole+curext):
                self.allviews.add_object(which='vector',filename=self.mydirwhole+curext,id=curidx,ToCheck=False)
                
        self.allviews.add_object(which='vector',newobj=self.myexchanges.mysegs,id='Forced exchanges',ToCheck=False)
        self.allviews.add_object(which='cloud',newobj=self.mycatchment.subBasinCloud,id='Local outlets',ToCheck=False)
        self.allviews.add_object(which='cloud',newobj=self.myexchanges.mycloudup,id='Up nodes',ToCheck=False)
        self.allviews.add_object(which='cloud',newobj=self.myexchanges.myclouddown,id='Down nodes',ToCheck=False)
        
        self.allviews.add_object(which='other',newobj=self.SPWstations,ToCheck=False,id='SPW-MI stations')
        self.allviews.add_object(which='other',newobj=self.DCENNstations,ToCheck=False,id='SPW-DCENN stations')

        self.add_grid()
        self.add_WMS()

        self.allviews.findminmax(True)        
        self.allviews.Autoscale(False)

        #Fichiers de paramètres
        self.mainparams=Wolf_Param(self.allviews,filename=self.mydir+'\\Main_model.param',title="Model parameters",DestroyAtClosing=False)
        self.basinparams=Wolf_Param(self.allviews,filename=self.mydircharact+'.param',title="Basin parameters",DestroyAtClosing=False)
        self.mainparams.Hide()
        self.basinparams.Hide() 

class Wolf2DModel(GenMapManager):

    mydir:str
    filenamegen:str
    files_others:dict
    files_fine_array:dict
    files_MB_array:dict
    files_vectors:dict
    mainparams:Wolf_Param

    SPWstations:SPWMIGaugingStations
    DCENNstations:SPWDCENNGaugingStations

    def __init__(self,dir:str='', *args, **kw):
        super(Wolf2DModel, self).__init__(*args, **kw)

        self.SPWstations=SPWMIGaugingStations()
        self.DCENNstations=SPWDCENNGaugingStations()
        
        if dir=='':
            idir=wx.DirDialog(None,"Choose Directory")
            if idir.ShowModal() == wx.ID_CANCEL:
                return
            self.mydir =idir.GetPath()
        else:
            self.mydir=path.normpath(dir)

        with BusyInfo(_('Opening 2D model')), wx.BusyCursor() as wait:
            self.filenamegen=''
            #recherche du nom générique --> sans extension
            for curfile in scandir(self.mydir):
                if curfile.is_file():
                    ext=path.splitext(curfile)
                    if len(ext[1])==0:
                        self.filenamegen = path.join(self.mydir,curfile.name)
                        break
                    
            self.allviews=WolfMapViewer(None,title='2D model : '+self.mydir,wolfparent=self)
            
            if self.filenamegen=='':
                return
            
            wx.LogMessage(_('Generic file is : ')+self.filenamegen)
            wx.LogMessage(_('Creating GUI'))
            
            self.files_others={'Generic file':[
                ('','First parametric file - historical'),
                ('.par','Parametric file - multiblocks')],
                            'Charachteristics':[
                ('.fil','Infiltration hydrographs [m³/s]'),
                ('.mnap','Resulting mesh [-]'),
                ('.trl','Translation to real world [m]')
                ]}
            
            self.files_vectors={'Block file':[
                ('.bloc','Blocks geometry')],
                                'Borders':[
                ('.sux','X borders'),
                ('.suy','Y borders')],
                                'Contour':[
                ('.xy','General perimeter')                     
            ]}

            self.files_MB_array={'Initial Conditions':[
                ('.topini','Bed elevation [m]',WOLF_ARRAY_MB_SINGLE),
                ('.hbinb','Water depth [m]',WOLF_ARRAY_MB_SINGLE),
                ('.qxbinb','Discharge X [m²/s]',WOLF_ARRAY_MB_SINGLE),
                ('.qybinb','Discharge Y [m²/s]',WOLF_ARRAY_MB_SINGLE),
                ('.frotini','Roughness coeff',WOLF_ARRAY_MB_SINGLE)
            ]}

            self.files_fine_array={'Characteristics':[
                ('.napbin','Mask [-]',WOLF_ARRAY_FULL_LOGICAL),
                ('.top','Bed Elevation [m]',WOLF_ARRAY_FULL_SINGLE),
                ('.topini_fine','Bed Elevation - computed [m]',WOLF_ARRAY_FULL_SINGLE),
                ('.frot','Roughness coefficient [law dependent]',WOLF_ARRAY_FULL_SINGLE),
                ('.inf','Infiltration zone [-]',WOLF_ARRAY_FULL_SINGLE),
                ('.hbin','Initial water depth [m]',WOLF_ARRAY_FULL_SINGLE),
                ('.qxbin','Initial discharge along X [m^2/s]',WOLF_ARRAY_FULL_SINGLE),
                ('.qybin','Initial discharge along Y [m^2/s]',WOLF_ARRAY_FULL_SINGLE)
            ]}
            
            self.fines_array=[]

            wx.LogMessage(_('Importing parameters'))
            self.myparam=prev_parameters_simul(self)
            self.myparam.read_file()

            wx.LogMessage(_('Reading mask'))
            self.mynap = self.read_fine_nap()
            
            wx.LogMessage(_('Reading sux-suy'))
            self.mysuxy = prev_suxsuy(self)
            self.mysuxy.read_file()
            
            wx.LogMessage(_('Reading xy'))
            self.xyfile = xy_file(self)
            self.xyzones = self.xyfile.myzones
            
            wx.LogMessage(_('Reading infiltration'))
            self.myinfil=prev_infiltration(self)
            self.myinfil.read_file()
            self.myinfil.read_array()

            wx.LogMessage(_('Reading blocks'))
            self.myblocfile=bloc_file(self)
            self.myblocfile.read_file()
            
            wx.LogMessage(_('Reading MNAP'))
            self.mymnap= WolfArrayMNAP(self.filenamegen)        
            self.mymnap.parentGUI=self        
            self.mymnap.add_ops_sel()
            
            # self.cont_sauv:Zones
            # self.filaire:Zones

            wx.LogMessage(_('Adding arrays to GUI'))
            #fine resolution
            self.napbin = WolfArray_Sim2D(fname=self.filenamegen+'.napbin', whichtype=WOLF_ARRAY_FULL_LOGICAL,preload=True,parentgui=self,srcheader=self.get_header())
            self.allviews.add_object(which='array',newobj=self.napbin,id='mask - fine',ToCheck=True)
            
            self.curmask = self.napbin.array.mask
            
            self.top = WolfArray_Sim2D(fname=self.filenamegen+'.top', whichtype=WOLF_ARRAY_FULL_SINGLE,preload=False,parentgui=self,masksrc=self.curmask,srcheader=self.get_header())
            self.allviews.add_object(which='array',newobj=self.top,id='bed elevation - fine',ToCheck=False)

            self.topinifine = WolfArray_Sim2D(fname=self.filenamegen+'.topini_fine', whichtype=WOLF_ARRAY_FULL_SINGLE,preload=False,parentgui=self,masksrc=self.curmask,srcheader=self.get_header())
            self.allviews.add_object(which='array',newobj=self.topinifine,id='bed elevation - computed',ToCheck=False)

            self.frot = WolfArray_Sim2D(fname=self.filenamegen+'.frot', whichtype=WOLF_ARRAY_FULL_SINGLE,preload=False,parentgui=self,masksrc=self.curmask,srcheader=self.get_header())
            self.allviews.add_object(which='array',newobj=self.frot,id='manning roughness - fine',ToCheck=False)

            self.inf = self.myinfil.myarray
            self.myinfil.myarray.parentGUI=self        
            self.myinfil.masksrc=self.curmask
            self.myinfil.myarray.add_ops_sel()        
            self.allviews.add_object(which='array',newobj=self.inf,id='infiltration',ToCheck=False)
            
            self.allviews.add_object(which='array',newobj=self.mymnap,id='mnap',ToCheck=False)

            self.hbin = WolfArray_Sim2D(fname=self.filenamegen+'.hbin', whichtype=WOLF_ARRAY_FULL_SINGLE,preload=False,parentgui=self,masksrc=self.curmask,srcheader=self.get_header())
            self.allviews.add_object(which='array',newobj=self.hbin,id='H - IC',ToCheck=False)

            self.qxbin = WolfArray_Sim2D(fname=self.filenamegen+'.qxbin', whichtype=WOLF_ARRAY_FULL_SINGLE,preload=False,parentgui=self,masksrc=self.curmask,srcheader=self.get_header())
            self.allviews.add_object(which='array',newobj=self.qxbin,id='QX - IC',ToCheck=False)

            self.qybin = WolfArray_Sim2D(fname=self.filenamegen+'.qybin', whichtype=WOLF_ARRAY_FULL_SINGLE,preload=False,parentgui=self,masksrc=self.curmask,srcheader=self.get_header())
            self.allviews.add_object(which='array',newobj=self.qybin,id='QY - IC',ToCheck=False)

            self.zbin = WolfArray_Sim2D(fname=self.filenamegen+'.zbin', whichtype=WOLF_ARRAY_FULL_SINGLE,preload=False,parentgui=self,masksrc=self.curmask,srcheader=self.get_header())
            self.allviews.add_object(which='array',newobj=self.zbin,id='Water level - IC',ToCheck=False)

            self.fines_array.append(self.napbin)
            self.fines_array.append(self.top)
            self.fines_array.append(self.frot)
            self.fines_array.append(self.inf)
            self.fines_array.append(self.hbin)
            self.fines_array.append(self.qxbin)
            self.fines_array.append(self.qybin)

            #MB resolution
            self.hbinb = WolfArrayMB(fname=self.filenamegen+'.hbinb', whichtype=WOLF_ARRAY_MB_SINGLE,preload=False,parentgui=self)
            self.hbinb.set_header(self.get_header_MB())        
            self.allviews.add_object(which='array',newobj=self.hbinb,id='H - IC - MB',ToCheck=False)

            self.qxbinb = WolfArrayMB(fname=self.filenamegen+'.qxbinb', whichtype=WOLF_ARRAY_MB_SINGLE,preload=False,parentgui=self)
            self.qxbinb.set_header(self.get_header_MB())        
            self.allviews.add_object(which='array',newobj=self.qxbinb,id='QX - IC - MB',ToCheck=False)

            self.qybinb = WolfArrayMB(fname=self.filenamegen+'.qybinb', whichtype=WOLF_ARRAY_MB_SINGLE,preload=False,parentgui=self)
            self.qybinb.set_header(self.get_header_MB())        
            self.allviews.add_object(which='array',newobj=self.qybinb,id='QY - IC - MB',ToCheck=False)

            self.topini = WolfArrayMB(fname=self.filenamegen+'.topini', whichtype=WOLF_ARRAY_MB_SINGLE,preload=False,parentgui=self)
            self.topini.set_header(self.get_header_MB())        
            self.allviews.add_object(which='array',newobj=self.topini,id='bed elevation - MB',ToCheck=False)
            
            wx.LogMessage(_('Adding vectors to GUI'))
            #vectors
            self.allviews.add_object(which='vector',newobj=self.xyzones,id='XY',ToCheck=True)
            self.allviews.add_object(which='vector',newobj=self.mysuxy.myborders,id='Borders',ToCheck=False)
            self.allviews.add_object(which='vector',newobj=self.myblocfile.my_vec_blocks,id='Blocks',ToCheck=False)
            
            self.allviews.add_object(which='other',newobj=self.SPWstations,ToCheck=False,id='SPW-MI stations')
            self.allviews.add_object(which='other',newobj=self.DCENNstations,ToCheck=False,id='SPW-DCENN stations')

            self.add_grid()
            self.add_WMS()

            wx.LogMessage(_('Zooming'))
            self.allviews.findminmax(True)        
            self.allviews.Autoscale(False)

            self.mysuxy.myborders.prep_listogl()
            self.myblocfile.my_vec_blocks.prep_listogl()

            #Fichiers de paramètres
            # self.mainparams=Wolf_Param(self.allviews,filename=self.mydir+'\\Main_model.param',title="Model parameters",DestroyAtClosing=False)
            # self.mainparams.Hide()
            
            wx.LogMessage(_('Adapting menu'))
            self.allviews.menu_sim2D()

            wx.LogMessage(_('Verifying files'))
            self.verify_files()
        
    def verify_files(self):
        """
        Vérification de la présence des en-têtes dans les différents fichiers
        """
        
        fhead = self.get_header()
        mbhead = self.get_header_MB()
        
        fine = self.files_fine_array['Characteristics']
        for curextent,text,wolftype in fine:
            fname = self.filenamegen + curextent
            if exists(fname):
                fname += '.txt'
                if not exists(fname):
                    fhead.write_txt_header(fname,wolftype)

        mb = self.files_MB_array['Initial Conditions']
        for curextent,text,wolftype in mb:
            fname = self.filenamegen + curextent
            if exists(fname):
                fname += '.txt'
                if not exists(fname):
                    mbhead.write_txt_header(fname,wolftype)
                
        fname = self.filenamegen + '.lst'
        if not exists(fname):
            with open(fname,'w') as f:
                f.write('0\n')
    
    def mimic_mask(self,source:WolfArray_Sim2D):
        
        wx.LogMessage(_('Copying mask to all arrays'))
        self.curmask = source.array.mask
        
        for curarray in self.fines_array:
            curarray:WolfArray_Sim2D
            if curarray is not source and curarray.loaded:
                curarray.copy_mask_log(self.curmask)
                
        wx.LogMessage(_('Updating mask array and .nap file'))
        self.napbin.array.data[np.where(np.logical_not(self.curmask))] = -1
        self.napbin.write_all()
        
    def extend_bed_elevation(self):
        
        dlg = wx.MessageDialog(self,_('Would you like to autocomplete elevation from external file?'),style=wx.YES_NO|wx.YES_DEFAULT)
        ret=dlg.ShowModal()
        dlg.Destroy()
        
        if ret == wx.ID_NO:
            wx.LogMessage(_('Nothing to do !')) 
            return
        
        if not self.top.loaded:
            self.top.check_plot()
            self.top.copy_mask_log(self.curmask)
            self.top.loaded=True    
        
        filterArray = "bin (*.bin)|*.bin|all (*.*)|*.*"
        fdlg = wx.FileDialog(self, "Choose file", wildcard=filterArray, style=wx.FD_OPEN)
        if fdlg.ShowModal() != wx.ID_OK:
            fdlg.Destroy()
            return
        
        filename = fdlg.GetPath()
        fdlg.Destroy()
        
        wx.LogMessage(_('Importing data from file'))    
        newtop = WolfArray(fname=filename,parentgui=self)
        
        wx.LogMessage(_('Finding nodes -- plotting disabled for speed'))    
        self.top.mngselection.hideselection = True
        self.top.mngselection.condition_select(2,0., usemask=True)
        
        if len(self.top.mngselection.myselection)>0:
            newtop.mngselection.myselection = self.top.mngselection.myselection
            newtop.mngselection.hideselection = True
            newtop.mngselection.update_nb_nodes_sections()

            wx.LogMessage(_('Copying values'))    
            z = newtop.mngselection.get_values_sel()
            wx.LogMessage(_('Pasting values'))    
            self.top.set_values_sel(self.top.mngselection.myselection, z, False)           

        self.top.mngselection.hideselection = False
        self.top.mngselection.myselection=[]
        self.top.copy_mask_log(self.curmask)        
        self.top.reset_plot()
        
        wx.LogMessage('')
        wx.LogMessage(_('Do not forget to save your changes to files !'))            
        wx.LogMessage('')
        
    def extend_freesurface_elevation(self,selection:list):
        
        wx.LogMessage(_('Loading necessary values'))    
        listarrays=[self.top,self.hbin,self.zbin]
        for curarray in listarrays:
            if not curarray.loaded:
                wx.LogMessage('  ' + curarray.idx)   
                curarray.check_plot()
                curarray.copy_mask_log(self.curmask)
                curarray.loaded=True    
                curarray.mngselection.hideselection = True

        wx.LogMessage(_('Hiding positive values'))            
        self.hbin.mngselection.myselection = selection.copy()
        self.hbin.mngselection.condition_select(4,0., usemask=True)
        nullvalues = self.hbin.mngselection.myselection.copy()
        
        nb = len(nullvalues)
        if nb==0:
            wx.LogMessage(_('Nothing to do -- exit !'))
            return                
            
        wx.LogMessage('  ' + str(len(nullvalues)) + _(' to interpolate'))     
        
        wx.LogMessage(_('Hiding null values'))            
        self.hbin.mngselection.myselection = selection.copy()
        self.hbin.mngselection.condition_select(2,0., usemask=True)
        nb = len(self.hbin.mngselection.myselection)

        wx.LogMessage('  ' + str(nb) + _(' source nodes'))           
        if nb<2:
            wx.LogMessage(_('Not enough source nodes -- exit !'))
            return                
        
        wx.LogMessage(_('Copying selection to zbin'))    
        self.zbin.mngselection.myselection = self.hbin.mngselection.myselection.copy()
        z = self.zbin.mngselection.get_values_sel()
        xy = np.asarray(self.zbin.mngselection.myselection)
        
        wx.LogMessage(_('Interpolating free surface'))    
        self.zbin.mngselection.myselection = nullvalues.copy()
        self.zbin.interpolate_on_cloud(xy,z,'nearest')
        
        wx.LogMessage(_('Filtering negative values'))    
        self.hbin.array = self.zbin.array - self.top.array
        self.hbin.array[np.where(self.hbin.array<0.)]=0.
        
        self.zbin.array = self.hbin.array+self.top.array
        
        wx.LogMessage(_('Refreshing mask and plot'))    
        for curarray in listarrays:
            curarray.copy_mask_log(self.curmask)
            curarray.mngselection.myselection=[]
            curarray.mngselection.hideselection=False
            curarray.reset_plot()
                
        wx.LogMessage('')
        wx.LogMessage(_('Do not forget to save your changes to files !'))            
        wx.LogMessage('')
                
    def extend_roughness(self,selection:list):
        
        # La sélection contient tous les points utiles
        sel=selection.copy()
        
        dlg = wx.TextEntryDialog(None,_('Which value should be replace by nearest one?'),_('Value'),value='0.04')
        ret = dlg.ShowModal()
        
        if ret == wx.ID_CANCEL:
            dlg.Destroy()
            return
        
        oldval = float(dlg.GetValue())
        eps = oldval/1000.
        dlg.Destroy()
        
        wx.LogMessage(_('Loading necessary values'))    
        listarrays=[self.frot]
        for curarray in listarrays:
            if not curarray.loaded:
                wx.LogMessage('  ' + curarray.idx)   
                curarray.check_plot()
                curarray.copy_mask_log(self.curmask)
                curarray.loaded=True    
                curarray.mngselection.hideselection = True

        wx.LogMessage(_('Selecting old values'))  
        self.frot.mngselection.hideselection = True          
        self.frot.mngselection.myselection = sel.copy()
        
        # On cherche les points à interpoler --> on resélectionne les mailles en dehors de l'intervalle
        # La double sélection supprime la maille de la zone déjà sélectionnée
        self.frot.mngselection.condition_select('<>',oldval-eps,oldval+eps, usemask=True)
        nullvalues = self.frot.mngselection.myselection.copy()
        
        nb = len(nullvalues)
        if nb==0:
            wx.LogMessage(_('Nothing to do -- exit !'))
            return                
            
        wx.LogMessage('  ' + str(len(nullvalues)) + _(' to interpolate'))     
        
        wx.LogMessage(_('Hiding old values'))            
        self.frot.mngselection.myselection = sel.copy()

        # On cherche les points depuis où interpoler --> on resélectionne les mailles dans l'intervalle
        # La double sélection supprime la maille de la zone déjà sélectionnée
        self.frot.mngselection.condition_select('>=<=',oldval-eps,oldval+eps, usemask=True)
        nb = len(self.frot.mngselection.myselection)

        wx.LogMessage('  ' + str(nb) + _(' source nodes'))           
        if nb<2:
            wx.LogMessage(_('Not enough source nodes -- exit !'))
            return                
        
        wx.LogMessage(_('Interpolating NN'))    
        # Récupération des z et xy des mailles actuellement sélectionnées
        z = self.frot.mngselection.get_values_sel()
        xy = np.asarray(self.frot.mngselection.myselection)
        # Recopiage des mailles à interpoler depuis le stockage temporaire
        self.frot.mngselection.myselection = nullvalues
        # Interpolation par voisin le plus proche
        self.frot.interpolate_on_cloud(xy,z,'nearest')
                
        wx.LogMessage(_('Refreshing mask and plot'))    
        for curarray in listarrays:
            curarray.copy_mask_log(self.curmask)
            curarray.mngselection.myselection=[]
            curarray.mngselection.hideselection = False
            curarray.mngselection.update_nb_nodes_sections()
            curarray.reset_plot()
                
        wx.LogMessage('')
        wx.LogMessage(_('Do not forget to save your changes to files !'))            
        wx.LogMessage('')

    def set_type_ic(self,which=2,dialog=True):
        
        if dialog:
            dlg = wx.SingleChoiceDialog(None,_('How do you want to read initial conditions ?'),_('Reading mode'),choices=[_('Text'),_('Binary mono-block'),_('Binary multi-blocks')])        
            ret = dlg.ShowModal()
            if ret == wx.ID_CANCEL:
                dlg.Destroy()
                return

            which = dlg.GetSelection()+1
            dlg.Destroy()
        
        if which<1 or which>3:
            return

        self.myparam.ntyperead = which
        self.myparam.write_file()


    def replace_external_contour(self,newvec:vector,interior):
        
        wx.LogMessage(_('Copying extrenal contour'))        
        
        wx.LogMessage(_('   ... in .bloc'))
        ext_zone:zone
        ext_zone = self.myblocfile.my_vec_blocks.myzones[0]
        ext_zone.myvectors[0] = newvec
        
        wx.LogMessage(_('   ... in xy --> Fortran will update this file after internal meshing process'))
        self.xyzones.myzones[0].myvectors[0] = newvec
        
        self.myblocfile.my_vec_blocks.reset_listogl()
        self.myblocfile.my_vec_blocks.prep_listogl()
        
        wx.LogMessage(_('Updating .bloc file'))
        self.myblocfile.interior=interior
        self.myblocfile.my_vec_blocks.find_minmax(True)
        self.myblocfile.update_nbmax()
        self.myblocfile.write_file()

    def write_bloc_file(self):
        
        wx.LogMessage(_('Updating .bloc file'))
        self.myblocfile.my_vec_blocks.find_minmax(True)
        self.myblocfile.write_file()
    
    def get_header_MB(self,abs=False):
        '''#> Renvoit un header avec les infos multi-blocs'''
        myheader:header_wolf
        myheader = self.mymnap.get_header(abs=abs)
        for curblock in self.mymnap.myblocks.values():
            myheader.head_blocks[getkeyblock(curblock.blockindex)] = curblock.get_header(abs=abs)
        return  myheader
        
    def get_header(self,abs=True):
        '''#> Renvoit un header de matrice "fine" non MB'''
        
        curhead = header_wolf()
        
        curhead.nbx = self.myparam.nxfin
        curhead.nby = self.myparam.nyfin
        
        curhead.dx = self.myparam.dxfin
        curhead.dy = self.myparam.dyfin
        
        curhead.origx = self.myparam.xminfin
        curhead.origy = self.myparam.yminfin
        
        curhead.translx = self.myparam.translx
        curhead.transly = self.myparam.transly
        
        return curhead
        # return self.mymnap.get_header(abs=abs)
                
    def read_fine_array(self,which=''):
        '''Lecture d'une matrice fine'''
        
        myarray =WolfArray()
        myarray.set_header(self.get_header())
        myarray.filename = self.filenamegen+which
        myarray.read_data()
        
        return myarray
    
    def read_MB_array(self,which=''):
        '''Lecture d'une matrice MB'''
        
        myarray =WolfArrayMB()
        myarray.set_header(self.get_header_MB())
        myarray.filename = self.filenamegen+which
        myarray.read_data()
        
        return myarray

    def read_fine_nap(self) -> np.ndarray:
        '''Lecture de la matrice nap sur le maillage fin'''
        nbx=self.myparam.nxfin
        nby=self.myparam.nyfin        
        
        with open(self.filenamegen +'.napbin', 'rb') as f:
            mynap = np.frombuffer(f.read(nbx*nby*2), dtype=np.int16).copy()
            mynap=np.abs(mynap)
        
        return mynap.reshape([nbx,nby], order='F')

    def transfer_ic(self,vector):
        
        dlg = wx.DirDialog(None,_('Choose directory containing destination model'),style=wx.DD_DIR_MUST_EXIST)
        ret = dlg.ShowModal()
        
        if ret==wx.ID_CANCEL:
            dlg.Destroy()
            return
        
        dstdir = dlg.GetPath()
        dlg.Destroy()
        
        wx.LogMessage(_('Reading destination model'))
        dstmodel = Wolf2DModel(dstdir,splash=False)
        
        wx.LogMessage(_('Reading data sources'))
        srcarrays=[self.top,self.hbin,self.qxbin,self.qybin]
        for loc in srcarrays:
            if not loc.loaded:
                loc.read_data()
                loc.copy_mask_log(self.curmask)

        wx.LogMessage(_('Reading data destination'))
        destarrays=[dstmodel.top,dstmodel.hbin,dstmodel.qxbin,dstmodel.qybin]
        for loc in destarrays:
            if not loc.loaded:
                loc.read_data()
                loc.copy_mask_log(dstmodel.curmask)
                
        wx.LogMessage(_('Copying data'))
        for src,dst in zip(srcarrays,destarrays):
            wx.LogMessage('  '+src.idx)
            
            vals,xy = src.get_values_insidepoly(vector,getxy=True)
            dst.set_values_sel(xy,vals)
            
        wx.LogMessage(_('Writing data on disk'))
        for loc in destarrays:
            loc.write_all()
            
        wx.LogMessage(_('Finished !'))
        
        pass
