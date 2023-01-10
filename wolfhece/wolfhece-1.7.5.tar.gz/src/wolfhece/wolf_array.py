import os
import sys
from matplotlib.axis import Axis
import numpy as np
import numpy.ma as ma
import math as m
from OpenGL.GL import *
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.path as mpltPath
import re
import wx
from scipy.interpolate import interp2d, griddata
from scipy.ndimage import laplace, label
import pygltflib
import struct
from shapely.geometry import Point, LineString, MultiLineString
from shapely.ops import linemerge, substring
from os.path import dirname,basename,join

from .PyTranslate import _
from .GraphNotebook import PlotPanel
from .CpGrid import CpGrid

try:
    from .libs import wolfogl
except:
    msg=_('Error importing wolfogl.pyd')
    msg+=_('   Python version : ' + sys.version)
    msg+=_('   If your Python version is not 3.7.x or 3.9.x, you need to compile an adapted library with compile_wcython.py in wolfhece library path')
    msg+=_('   See comments in compile_wcython.py or launch *python compile_wcython.py build_ext --inplace* in :')
    msg+='      ' + os.path.dirname(__file__)
    
    raise Exception(msg)

from .xyz_file import XYZFile
from .PyPalette import wolfpalette
from .PyVertexvectors import Zones, vector, wolfvertex, zone, Triangulation
from .PyVertex import cloud_vertices

WOLF_ARRAY_HILLSHAPE = -1
WOLF_ARRAY_FULL_SINGLE = 1
WOLF_ARRAY_FULL_DOUBLE = 2
WOLF_ARRAY_SYM_DOUBLE = 8
WOLF_ARRAY_FULL_LOGICAL = 4
WOLF_ARRAY_CSR_DOUBLE = 5
WOLF_ARRAY_FULL_INTEGER = 6
WOLF_ARRAY_FULL_SINGLE_3D = 7
WOLF_ARRAY_FULL_INTEGER8 = 8

WOLF_ARRAY_MB_SINGLE = 3
WOLF_ARRAY_MB_INTEGER = 9

WOLF_ARRAY_FULL_INTEGER16 = 11
WOLF_ARRAY_MNAP_INTEGER = 20

WOLF_ARRAY_MB = [WOLF_ARRAY_MB_SINGLE, WOLF_ARRAY_MB_INTEGER, WOLF_ARRAY_MNAP_INTEGER]


def getkeyblock(i, addone=True):
    if addone:
        return 'block' + str(i + 1)
    else:
        return 'block' + str(i)


class header_wolf():

    def __init__(self) -> None:
        self.origx = 0.0
        self.origy = 0.0
        self.origz = 0.0

        self.translx = 0.0
        self.transly = 0.0
        self.translz = 0.0

        self.dx = 0.0
        self.dy = 0.0
        self.dz = 0.0

        self.nbx = 0
        self.nby = 0
        self.nbz = 0

        self.nb_blocks = 0
        self.head_blocks = {}

    def get_bounds(self, abs=True):
        if abs:
            return ([self.origx + self.translx, self.origx + self.translx + float(self.nbx) * self.dx],
                    [self.origy + self.transly, self.origy + self.transly + float(self.nby) * self.dy])
        else:
            return ([self.origx, self.origx + float(self.nbx) * self.dx],
                    [self.origy, self.origy + float(self.nby) * self.dy])

    def get_bounds_ij(self, abs=True):

        mybounds = self.get_bounds(abs)

        return (
        [self.get_ij_from_xy(mybounds[0][0], mybounds[1][0]), self.get_ij_from_xy(mybounds[0][1], mybounds[0][0])],
        [self.get_ij_from_xy(mybounds[0][0], mybounds[1][1]), self.get_ij_from_xy(mybounds[0][1], mybounds[1][1])])

    def get_ij_from_xy(self, x, y, abs=True):

        locx = np.float64(x) - self.origx
        locy = np.float64(y) - self.origy
        if abs:
            locx = locx - self.translx
            locy = locy - self.transly

        i = np.int32(locx / self.dx)
        j = np.int32(locy / self.dy)

        return i, j  # ATTENTION, Indices en numérotation Python --> WOLF ajouter +1

    def find_intersection(self, other, ij=False):

        mybounds = self.get_bounds()
        otherbounds = other.get_bounds()

        if otherbounds[0][0] > mybounds[0][1]:
            return None
        elif otherbounds[1][0] > mybounds[1][1]:
            return None
        elif otherbounds[0][1] < mybounds[0][0]:
            return None
        elif otherbounds[1][1] < mybounds[0][1]:
            return None
        else:
            ox = max(mybounds[0][0], otherbounds[0][0])
            oy = max(mybounds[1][0], otherbounds[1][0])
            ex = min(mybounds[0][1], otherbounds[0][1])
            ey = min(mybounds[1][1], otherbounds[1][1])
            if ij:
                i1, j1 = self.get_ij_from_xy(ox, oy)
                i2, j2 = self.get_ij_from_xy(ex, ey)

                i3, j3 = other.get_ij_from_xy(ox, oy)
                i4, j4 = other.get_ij_from_xy(ex, ey)
                return ([[i1, i2], [j1, j2]],
                        [[i3, i4], [j3, j4]])
            else:
                return ([ox, ex], [oy, ey])

    def find_union(self, other):

        mybounds = self.get_bounds()
        otherbounds = other.get_bounds()

        ox = min(mybounds[0][0], otherbounds[0][0])
        oy = min(mybounds[1][0], otherbounds[1][0])
        ex = max(mybounds[0][1], otherbounds[0][1])
        ey = max(mybounds[1][1], otherbounds[1][1])

        return ([ox, ex], [oy, ey])


    def write_txt_header(self,filename,wolftype,forceupdate=False):
        """
        Ecriture du header dans un fichier texte
        
        filename : chemin d'accès et nom de fichier avec '.txt' qui ne sera pas ajouté automatiquement
        wolftype : type de la matrice WOLF_ARRAY_*
        
        """
        if not os.path.exists(filename) or forceupdate:
            with open(filename,'w') as f:
            
                """ Ecriture de l'en-tête de Wolf array """
                f.write('NbX :\t{0}\n'.format(str(self.nbx)))
                f.write('NbY :\t{0}\n'.format(str(self.nby)))
                f.write('OrigX :\t{0}\n'.format(str(self.origx)))
                f.write('OrigY :\t{0}\n'.format(str(self.origy)))
                f.write('DX :\t{0}\n'.format(str(self.dx)))
                f.write('DY :\t{0}\n'.format(str(self.dy)))
                f.write('TypeEnregistrement :\t{0}\n'.format(str(wolftype)))
                f.write('TranslX :\t{0}\n'.format(str(self.translx)))
                f.write('TranslY :\t{0}\n'.format(str(self.transly)))
                if wolftype == WOLF_ARRAY_FULL_SINGLE_3D:
                    f.write('NbZ :\t{0}\n'.format(str(self.nbz)))
                    f.write('OrigZ :\t{0}\n'.format(str(self.origz)))
                    f.write('DZ :\t{0}\n'.format(str(self.dz)))
                    f.write('TranslZ :\t{0}\n'.format(str(self.translz)))

                if wolftype in WOLF_ARRAY_MB:
                    f.write('Nb Blocs :\t{0}\n'.format(str(self.nb_blocks)))
                    for i in range(self.nb_blocks):
                        curhead = self.head_blocks[getkeyblock(i)]
                        f.write('NbX :\t{0}\n'.format(str(curhead.nbx)))
                        f.write('NbY :\t{0}\n'.format(str(curhead.nby)))
                        f.write('OrigX :\t{0}\n'.format(str(curhead.origx)))
                        f.write('OrigY :\t{0}\n'.format(str(curhead.origy)))
                        f.write('DX :\t{0}\n'.format(str(curhead.dx)))
                        f.write('DY :\t{0}\n'.format(str(curhead.dy)))


class NewArray(wx.Dialog):
    def __init__(self, parent):
        super(NewArray, self).__init__(parent, title=_('New array'), size=(300, 300),
                                       style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL | wx.OK)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        glsizer = self.CreateSeparatedButtonSizer(wx.OK)

        gSizer1 = wx.GridSizer(6, 2, 0, 0)

        glsizer.Insert(0, gSizer1)

        self.m_staticText9 = wx.StaticText(self, wx.ID_ANY, u"dX", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText9.Wrap(-1)

        gSizer1.Add(self.m_staticText9, 0, wx.ALL, 5)

        self.dx = wx.TextCtrl(self, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, style=wx.TE_CENTER)
        gSizer1.Add(self.dx, 0, wx.ALL, 5)

        self.m_staticText10 = wx.StaticText(self, wx.ID_ANY, u"dY", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText10.Wrap(-1)

        gSizer1.Add(self.m_staticText10, 0, wx.ALL, 5)

        self.dy = wx.TextCtrl(self, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, style=wx.TE_CENTER)
        gSizer1.Add(self.dy, 0, wx.ALL, 5)

        self.m_staticText11 = wx.StaticText(self, wx.ID_ANY, u"NbX", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText11.Wrap(-1)

        gSizer1.Add(self.m_staticText11, 0, wx.ALL, 5)

        self.nbx = wx.TextCtrl(self, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, style=wx.TE_CENTER)
        gSizer1.Add(self.nbx, 0, wx.ALL, 5)

        self.m_staticText12 = wx.StaticText(self, wx.ID_ANY, u"NbY", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText12.Wrap(-1)

        gSizer1.Add(self.m_staticText12, 0, wx.ALL, 5)

        self.nby = wx.TextCtrl(self, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, style=wx.TE_CENTER)
        gSizer1.Add(self.nby, 0, wx.ALL, 5)

        self.m_staticText13 = wx.StaticText(self, wx.ID_ANY, u"OrigX", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText13.Wrap(-1)

        gSizer1.Add(self.m_staticText13, 0, wx.ALL, 5)

        self.ox = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, style=wx.TE_CENTER)
        gSizer1.Add(self.ox, 0, wx.ALL, 5)

        self.m_staticText14 = wx.StaticText(self, wx.ID_ANY, u"OrigY", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText14.Wrap(-1)

        gSizer1.Add(self.m_staticText14, 0, wx.ALL, 5)

        self.oy = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, style=wx.TE_CENTER)
        gSizer1.Add(self.oy, 0, wx.ALL, 5)

        # self.OK = wx.Button( self, wx.ID_ANY, u"Validate", wx.DefaultPosition, wx.DefaultSize, 0 )
        # gSizer1.Add( self.OK, 0, wx.ALL, 5 )

        self.nbx.SetFocus()
        self.nbx.SelectAll()
        self.SetSizer(glsizer)
        self.Layout()

        self.Centre(wx.BOTH)


class CropDialog(wx.Dialog):
    def __init__(self, parent):
        super(CropDialog, self).__init__(parent, title=_('Cropping array'), size=(300, 300),
                                         style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL | wx.OK)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        glsizer = self.CreateSeparatedButtonSizer(wx.OK)

        gSizer1 = wx.GridSizer(6, 2, 0, 0)

        glsizer.Insert(0, gSizer1)

        self.m_staticText9 = wx.StaticText(self, wx.ID_ANY, u"dX", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText9.Wrap(-1)

        gSizer1.Add(self.m_staticText9, 0, wx.ALL, 5)

        self.dx = wx.TextCtrl(self, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, style=wx.TE_CENTER)
        gSizer1.Add(self.dx, 0, wx.ALL, 5)

        self.m_staticText10 = wx.StaticText(self, wx.ID_ANY, u"dY", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText10.Wrap(-1)

        gSizer1.Add(self.m_staticText10, 0, wx.ALL, 5)

        self.dy = wx.TextCtrl(self, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, style=wx.TE_CENTER)
        gSizer1.Add(self.dy, 0, wx.ALL, 5)

        self.m_staticText11 = wx.StaticText(self, wx.ID_ANY, u"OrigX - lower left corner", wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.m_staticText11.Wrap(-1)

        gSizer1.Add(self.m_staticText11, 0, wx.ALL, 5)

        self.ox = wx.TextCtrl(self, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, style=wx.TE_CENTER)
        gSizer1.Add(self.ox, 0, wx.ALL, 5)

        self.m_staticText12 = wx.StaticText(self, wx.ID_ANY, u"OrigY - lower left corner", wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.m_staticText12.Wrap(-1)

        gSizer1.Add(self.m_staticText12, 0, wx.ALL, 5)

        self.oy = wx.TextCtrl(self, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, style=wx.TE_CENTER)
        gSizer1.Add(self.oy, 0, wx.ALL, 5)

        self.m_staticText13 = wx.StaticText(self, wx.ID_ANY, u"EndX - upper right corner", wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.m_staticText13.Wrap(-1)

        gSizer1.Add(self.m_staticText13, 0, wx.ALL, 5)

        self.ex = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, style=wx.TE_CENTER)
        gSizer1.Add(self.ex, 0, wx.ALL, 5)

        self.m_staticText14 = wx.StaticText(self, wx.ID_ANY, u"EndY - upper right corner", wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.m_staticText14.Wrap(-1)

        gSizer1.Add(self.m_staticText14, 0, wx.ALL, 5)

        self.ey = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, style=wx.TE_CENTER)
        gSizer1.Add(self.ey, 0, wx.ALL, 5)

        # self.OK = wx.Button( self, wx.ID_ANY, u"Validate", wx.DefaultPosition, wx.DefaultSize, 0 )
        # gSizer1.Add( self.OK, 0, wx.ALL, 5 )

        self.ox.SetFocus()
        self.ox.SelectAll()
        self.SetSizer(glsizer)
        self.Layout()

        self.Centre(wx.BOTH)

    def get_header(self):
        myhead = header_wolf()
        myhead.origx = float(self.ox.Value)
        myhead.origy = float(self.oy.Value)
        myhead.dx = float(self.dx.Value)
        myhead.dy = float(self.dy.Value)
        myhead.nbx = int((float(self.ex.Value) - myhead.origx) / myhead.dx)
        myhead.nby = int((float(self.ey.Value) - myhead.origy) / myhead.dy)

        return myhead


class Ops_Array(wx.Frame):

    def __init__(self, wxparent, parentarray, parentGUI):

        super(Ops_Array, self).__init__(wxparent, title=_('Operations'), size=(370, 450),
                                        style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.active_vector = None
        self.active_zone = None
        self.myzones = Zones(parent=self)
        self.myzonetmp = zone(name='tmp')
        self.vectmp = vector(name='tmp')
        self.fnsave = ''

        self.myzonetmp.add_vector(self.vectmp)
        self.myzones.add_zone(self.myzonetmp)

        self.parentarray = parentarray
        self.parentGUI = parentGUI


        # GUI
        self.Bind(wx.EVT_CLOSE, self.onclose)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        # GUI Notebook
        self.array_ops = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)
        
        #  panel Selection
        self.selection = wx.Panel(self.array_ops, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.array_ops.AddPage(self.selection, _("Selection"), True)

        #  panel Operations
        self.operation = wx.Panel(self.array_ops, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.array_ops.AddPage(self.operation, _("Operations"), False)

        #  panel Mask
        self.mask = wx.Panel(self.array_ops, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.array_ops.AddPage(self.mask, _("Mask"), False)

        #  panel Interpolation
        self.Interpolation = wx.Panel(self.array_ops, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.array_ops.AddPage(self.Interpolation, _("Interpolation"), False)

        #  panel Tools
        self.tools = wx.Panel(self.array_ops, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.array_ops.AddPage(self.tools, _("Tools"), False)

        #  panel PALETTE de couleurs
        self.Palette = PlotPanel(self.array_ops, wx.ID_ANY, toolbar=False)
        self.palgrid = CpGrid(self.Palette, wx.ID_ANY, style=wx.WANTS_CHARS | wx.TE_CENTER)
        self.palapply = wx.Button(self.Palette, wx.ID_ANY, _("Apply"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.palgrid.CreateGrid(16, 4)
        self.palauto = wx.CheckBox(self.Palette, wx.ID_ANY, _("Automatic"), wx.DefaultPosition, wx.DefaultSize,
                                   style=wx.CHK_CHECKED)
        self.palalpha = wx.CheckBox(self.Palette, wx.ID_ANY, _("Opacity"), wx.DefaultPosition, wx.DefaultSize,
                                    style=wx.CHK_CHECKED)
        self.palshader = wx.CheckBox(self.Palette, wx.ID_ANY, _("Hillshade"), wx.DefaultPosition, wx.DefaultSize,
                                     style=wx.CHK_CHECKED)
        self.palalphaslider = wx.Slider(self.Palette, wx.ID_ANY, 100, 0, 100, wx.DefaultPosition, wx.DefaultSize,
                                        wx.SL_HORIZONTAL, name='palslider')

        self.palalphahillshade = wx.Slider(self.Palette, wx.ID_ANY, 100, 0, 100, wx.DefaultPosition, wx.DefaultSize,
                                           wx.SL_HORIZONTAL, name='palalphaslider')
        self.palazimuthhillshade = wx.Slider(self.Palette, wx.ID_ANY, 315, 0, 360, wx.DefaultPosition, wx.DefaultSize,
                                             wx.SL_HORIZONTAL, name='palazimuthslider')
        self.palaltitudehillshade = wx.Slider(self.Palette, wx.ID_ANY, 0, 0, 90, wx.DefaultPosition, wx.DefaultSize,
                                              wx.SL_HORIZONTAL, name='palaltitudeslider')

        self.palsave = wx.Button(self.Palette, wx.ID_ANY, _("Save to file"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.palload = wx.Button(self.Palette, wx.ID_ANY, _("Load from file"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.palimage = wx.Button(self.Palette, wx.ID_ANY, _("Create image"), wx.DefaultPosition, wx.DefaultSize, 0)

        if self.parentarray.mypal.automatic:
            self.palauto.SetValue(1)
        else:
            self.palauto.SetValue(0)

        self.palalpha.SetValue(1)

        self.palchoosecolor = wx.Button(self.Palette, wx.ID_ANY, _("Choose color for current value"),
                                        wx.DefaultPosition, wx.DefaultSize)

        self.Palette.sizerfig.Add(self.palgrid, 1, wx.EXPAND)
        self.Palette.sizer.Add(self.palauto, 1, wx.EXPAND)
        self.Palette.sizer.Add(self.palalpha, 1, wx.EXPAND)
        self.Palette.sizer.Add(self.palalphaslider, 1, wx.EXPAND)
        self.Palette.sizer.Add(self.palshader, 1, wx.EXPAND)

        self.Palette.sizer.Add(self.palalphahillshade, 1, wx.EXPAND)
        self.Palette.sizer.Add(self.palazimuthhillshade, 1, wx.EXPAND)
        self.Palette.sizer.Add(self.palaltitudehillshade, 1, wx.EXPAND)

        self.Palette.sizer.Add(self.palchoosecolor, 1, wx.EXPAND)
        self.Palette.sizer.Add(self.palapply, 1, wx.EXPAND)
        self.Palette.sizer.Add(self.palload, 1, wx.EXPAND)
        self.Palette.sizer.Add(self.palsave, 1, wx.EXPAND)
        self.Palette.sizer.Add(self.palimage, 1, wx.EXPAND)

        self.array_ops.AddPage(self.Palette, _("Palette"), False)

        # HISTOGRAMMES
        self.histo = PlotPanel(self.array_ops, wx.ID_ANY, toolbar=True)
        self.histoupdate = wx.Button(self.histo, wx.ID_ANY, _("All data..."), wx.DefaultPosition, wx.DefaultSize, 0)
        self.histoupdatezoom = wx.Button(self.histo, wx.ID_ANY, _("On zoom..."), wx.DefaultPosition, wx.DefaultSize, 0)
        self.histoupdateerase = wx.Button(self.histo, wx.ID_ANY, _("Erase"), wx.DefaultPosition, wx.DefaultSize, 0)

        self.histo.sizer.Add(self.histoupdate, 0, wx.EXPAND)
        self.histo.sizer.Add(self.histoupdatezoom, 0, wx.EXPAND)
        self.histo.sizer.Add(self.histoupdateerase, 0, wx.EXPAND)

        self.array_ops.AddPage(self.histo, _("Histogram"), False)

        # LINKS
        self.links = wx.Panel(self.array_ops, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.array_ops.AddPage(self.links, _("Links"), False)

        # Interpolation
        gSizer1 = wx.GridSizer(0, 2, 0, 0)

        self.interp2D = wx.Button(self.Interpolation, wx.ID_ANY, _("2D Interpolation on selection"), wx.DefaultPosition,
                                  wx.DefaultSize, 0)
        gSizer1.Add(self.interp2D, 0, wx.EXPAND)
        self.interp2D.Bind(wx.EVT_BUTTON, self.interpolation2D)

        self.m_button7 = wx.Button(self.Interpolation, wx.ID_ANY, _("Volume/Surface evaluation"), wx.DefaultPosition,
                                   wx.DefaultSize, 0)
        gSizer1.Add(self.m_button7, 0, wx.EXPAND)
        self.m_button7.Bind(wx.EVT_BUTTON, self.volumesurface)

        self.m_button8 = wx.Button(self.Interpolation, wx.ID_ANY, _("Interpolation on active zone \n polygons"),
                                   wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer1.Add(self.m_button8, 0, wx.EXPAND)
        self.m_button8.Bind(wx.EVT_BUTTON, self.interp2Dpolygons)

        self.m_button9 = wx.Button(self.Interpolation, wx.ID_ANY, _("Interpolation on active zone \n 3D polylines"),
                                   wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer1.Add(self.m_button9, 0, wx.EXPAND)
        self.m_button9.Bind(wx.EVT_BUTTON, self.interp2Dpolylines)

        self.m_button10 = wx.Button(self.Interpolation, wx.ID_ANY, _("Interpolation on active vector \n polygon"),
                                    wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer1.Add(self.m_button10, 0, wx.EXPAND)
        self.m_button10.Bind(wx.EVT_BUTTON, self.interp2Dpolygon)

        self.m_button11 = wx.Button(self.Interpolation, wx.ID_ANY, _("Interpolation on active vector \n 3D polyline"),
                                    wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer1.Add(self.m_button11, 0, wx.EXPAND)
        self.m_button11.Bind(wx.EVT_BUTTON, self.interp2Dpolyline)

        self.Interpolation.SetSizer(gSizer1)
        self.Interpolation.Layout()
        gSizer1.Fit(self.Interpolation)
        
        # Tools
        # gSizer1 = wx.GridSizer(0, 2, 0, 0)

        # self.interp2D = wx.Button(self.Interpolation, wx.ID_ANY, _("2D Interpolation on selection"), wx.DefaultPosition,
        #                           wx.DefaultSize, 0)
        # gSizer1.Add(self.interp2D, 0, wx.EXPAND)
        # self.interp2D.Bind(wx.EVT_BUTTON, self.interpolation2D)

        # self.m_button7 = wx.Button(self.Interpolation, wx.ID_ANY, _("Volume/Surface evaluation"), wx.DefaultPosition,
        #                            wx.DefaultSize, 0)
        # gSizer1.Add(self.m_button7, 0, wx.EXPAND)
        # self.m_button7.Bind(wx.EVT_BUTTON, self.volumesurface)

        # self.m_button8 = wx.Button(self.Interpolation, wx.ID_ANY, _("Interpolation on active zone \n polygons"),
        #                            wx.DefaultPosition, wx.DefaultSize, 0)
        # gSizer1.Add(self.m_button8, 0, wx.EXPAND)
        # self.m_button8.Bind(wx.EVT_BUTTON, self.interp2Dpolygons)

        # self.m_button9 = wx.Button(self.Interpolation, wx.ID_ANY, _("Interpolation on active zone \n 3D polylines"),
        #                            wx.DefaultPosition, wx.DefaultSize, 0)
        # gSizer1.Add(self.m_button9, 0, wx.EXPAND)
        # self.m_button9.Bind(wx.EVT_BUTTON, self.interp2Dpolylines)

        # self.m_button10 = wx.Button(self.Interpolation, wx.ID_ANY, _("Interpolation on active vector \n polygon"),
        #                             wx.DefaultPosition, wx.DefaultSize, 0)
        # gSizer1.Add(self.m_button10, 0, wx.EXPAND)
        # self.m_button10.Bind(wx.EVT_BUTTON, self.interp2Dpolygon)

        # self.m_button11 = wx.Button(self.Interpolation, wx.ID_ANY, _("Interpolation on active vector \n 3D polyline"),
        #                             wx.DefaultPosition, wx.DefaultSize, 0)
        # gSizer1.Add(self.m_button11, 0, wx.EXPAND)
        # self.m_button11.Bind(wx.EVT_BUTTON, self.interp2Dpolyline)

        # self.Interpolation.SetSizer(gSizer1)
        # self.Interpolation.Layout()
        # gSizer1.Fit(self.Interpolation)        

        # Selection

        bSizer15 = wx.BoxSizer(wx.VERTICAL)

        bSizer21 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer16 = wx.BoxSizer(wx.VERTICAL)

        selectmethodChoices = [_("by clicks"), _("inside active vector"), _("inside active zone"),
                               _("inside temporary vector"), _("under active vector"), _("under active zone"),
                               _("under temporary vector")]
        self.selectmethod = wx.RadioBox(self.selection, wx.ID_ANY, _("How to select nodes?"), wx.DefaultPosition,
                                        wx.DefaultSize, selectmethodChoices, 1, wx.RA_SPECIFY_COLS)
        self.selectmethod.SetSelection(0)
        self.selectmethod.SetToolTip(_("Selection mode"))

        bSizer16.Add(self.selectmethod, 0, wx.ALL, 5)
        
        self.selectrestricttomask = wx.CheckBox(self.selection,wx.ID_ANY,_('Use mask to restrict'))
        self.selectrestricttomask.SetValue(True)
        self.selectrestricttomask.SetToolTip(_('If checked, the selection will be restricted by the mask data'))
        
        bSizer16.Add(self.selectrestricttomask, 0, wx.ALL, 5)

        self.LaunchSelection = wx.Button(self.selection, wx.ID_ANY,
                                         _("Action !"), wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        self.LaunchSelection.SetBackgroundColour((0,128,64,255))
        self.LaunchSelection.SetDefault()
        # self.LaunchSelection.SetForegroundColour((255,255,255,255))
        font = wx.Font(12, wx.FONTFAMILY_DECORATIVE, 0, 90, underline = False,faceName ="")
        self.LaunchSelection.SetFont(font)
        
        bSizer16.Add(self.LaunchSelection, 0, wx.EXPAND)
        self.AllSelection = wx.Button(self.selection, wx.ID_ANY,
                                      _("Select all nodes"), wx.DefaultPosition,
                                      wx.DefaultSize, 0)
        bSizer16.Add(self.AllSelection, 0, wx.EXPAND)
        self.MoveSelection = wx.Button(self.selection, wx.ID_ANY,
                                       _("Move current selection to..."), wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        bSizer16.Add(self.MoveSelection, 0, wx.EXPAND)
        self.ResetSelection = wx.Button(self.selection, wx.ID_ANY,
                                        _("Reset"), wx.DefaultPosition,
                                        wx.DefaultSize, 0)
        bSizer16.Add(self.ResetSelection, 0, wx.EXPAND)
        self.ResetAllSelection = wx.Button(self.selection, wx.ID_ANY,
                                           _("Reset All"), wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        bSizer16.Add(self.ResetAllSelection, 0, wx.EXPAND)

        bSizer21.Add(bSizer16, 1, wx.EXPAND, 5)

        bSizer17 = wx.BoxSizer(wx.VERTICAL)

        self.m_button2 = wx.Button(self.selection, wx.ID_ANY, _("Manage vectors"), wx.DefaultPosition, wx.DefaultSize,
                                   0)
        bSizer17.Add(self.m_button2, 0, wx.EXPAND)

        self.active_vector_id = wx.StaticText(self.selection, wx.ID_ANY, _("Active vector"), wx.DefaultPosition,
                                              wx.DefaultSize, 0)
        self.active_vector_id.Wrap(-1)

        bSizer17.Add(self.active_vector_id, 0, wx.EXPAND)

        self.CurActiveparent = wx.StaticText(self.selection, wx.ID_ANY, _("Active parent"), wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.CurActiveparent.Wrap(-1)

        bSizer17.Add(self.CurActiveparent, 0, wx.EXPAND)

        self.loadvec = wx.Button(self.selection, wx.ID_ANY, _("Read from file..."), wx.DefaultPosition, wx.DefaultSize,
                                 0)
        bSizer17.Add(self.loadvec, 0, wx.EXPAND)

        self.saveas = wx.Button(self.selection, wx.ID_ANY, _("Save as..."), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer17.Add(self.saveas, 0, wx.EXPAND)

        self.save = wx.Button(self.selection, wx.ID_ANY, _("Save"), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer17.Add(self.save, 0, wx.EXPAND)

        bSizer21.Add(bSizer17, 1, wx.EXPAND, 5)

        bSizer15.Add(bSizer21, 1, wx.EXPAND, 5)

        bSizer22 = wx.BoxSizer(wx.HORIZONTAL)

        self.nbselect = wx.StaticText(self.selection, wx.ID_ANY, _("nb"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.nbselect.Wrap(-1)

        bSizer22.Add(self.nbselect, 1, wx.EXPAND, 10)

        self.minx = wx.StaticText(self.selection, wx.ID_ANY, _("xmin"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.minx.Wrap(-1)

        self.minx.SetToolTip(_("X Mininum"))

        bSizer22.Add(self.minx, 1, wx.EXPAND, 10)

        self.maxx = wx.StaticText(self.selection, wx.ID_ANY, _("xmax"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.maxx.Wrap(-1)

        self.maxx.SetToolTip(_("X Maximum"))

        bSizer22.Add(self.maxx, 1, wx.EXPAND, 10)

        self.miny = wx.StaticText(self.selection, wx.ID_ANY, _("ymin"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.miny.Wrap(-1)

        self.miny.SetToolTip(_("Y Minimum"))

        bSizer22.Add(self.miny, 1, wx.EXPAND, 10)

        self.maxy = wx.StaticText(self.selection, wx.ID_ANY, _("ymax"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.maxy.Wrap(-1)

        self.maxy.SetToolTip(_("Y Maximum"))

        bSizer22.Add(self.maxy, 1, wx.EXPAND, 10)

        bSizer15.Add(bSizer22, 0, wx.EXPAND, 5)

        self.selection.SetSizer(bSizer15)
        self.selection.Layout()
        bSizer15.Fit(self.selection)

        # Mask
        sizermask = wx.BoxSizer(wx.VERTICAL)
        self.mask.SetSizer(sizermask)

        unmaskall = wx.Button(self.mask, wx.ID_ANY, _("Unmask all"), wx.DefaultPosition, wx.DefaultSize, 0)
        sizermask.Add(unmaskall, 1, wx.EXPAND)
        unmaskall.Bind(wx.EVT_BUTTON, self.Unmaskall)

        unmasksel = wx.Button(self.mask, wx.ID_ANY, _("Unmask selection"), wx.DefaultPosition, wx.DefaultSize, 0)
        sizermask.Add(unmasksel, 1, wx.EXPAND)
        unmasksel.Bind(wx.EVT_BUTTON, self.Unmasksel)

        invertmask = wx.Button(self.mask, wx.ID_ANY, _("Invert mask"), wx.DefaultPosition, wx.DefaultSize, 0)
        sizermask.Add(invertmask, 1, wx.EXPAND)
        invertmask.Bind(wx.EVT_BUTTON, self.InvertMask)

        self.mask.Layout()
        sizermask.Fit(self.mask)

        # Operations
        sizeropgen = wx.BoxSizer(wx.VERTICAL)
        sepopcond = wx.BoxSizer(wx.HORIZONTAL)
        sizerop = wx.BoxSizer(wx.VERTICAL)
        sizercond = wx.BoxSizer(wx.VERTICAL)
        # bSizer26 = wx.BoxSizer( wx.VERTICAL )

        # bSizer14.Add( bSizer26, 1, wx.EXPAND, 5 )
        sepopcond.Add(sizercond, 1, wx.EXPAND)
        sepopcond.Add(sizerop, 1, wx.EXPAND)
        sizeropgen.Add(sepopcond, 1, wx.EXPAND)

        operationChoices = [u"+", u"-", u"*", u"/", _("replace")]
        self.choiceop = wx.RadioBox(self.operation, wx.ID_ANY,
                                    _("Operation"), wx.DefaultPosition,
                                    wx.DefaultSize, operationChoices, 1, wx.RA_SPECIFY_COLS)
        self.choiceop.SetSelection(4)
        sizerop.Add(self.choiceop, 1, wx.EXPAND)

        self.opvalue = wx.TextCtrl(self.operation, wx.ID_ANY, u"1",
                                   wx.DefaultPosition, wx.DefaultSize, style=wx.TE_CENTER)
        sizerop.Add(self.opvalue, 0, wx.EXPAND)

        conditionChoices = [u"<", u"<=", u"=", u">=", u">", u"isNaN"]
        self.condition = wx.RadioBox(self.operation, wx.ID_ANY, _("Condition"), wx.DefaultPosition, wx.DefaultSize,
                                     conditionChoices, 1, wx.RA_SPECIFY_COLS)
        self.condition.SetSelection(2)
        sizercond.Add(self.condition, 1, wx.EXPAND)

        self.condvalue = wx.TextCtrl(self.operation, wx.ID_ANY, u"0",
                                     wx.DefaultPosition, wx.DefaultSize, style=wx.TE_CENTER)
        sizercond.Add(self.condvalue, 0, wx.EXPAND)

        self.ApplyOp = wx.Button(self.operation, wx.ID_ANY, _("Apply math operator"), wx.DefaultPosition,
                                 wx.DefaultSize, 0)
        sizeropgen.Add(self.ApplyOp, 1, wx.EXPAND)

        self.SelectOp = wx.Button(self.operation, wx.ID_ANY, _("Apply selection condition"), wx.DefaultPosition,
                                  wx.DefaultSize, 0)
        sizeropgen.Add(self.SelectOp, 1, wx.EXPAND)

        maskdata = wx.Button(self.operation, wx.ID_ANY, _("Apply on mask"), wx.DefaultPosition, wx.DefaultSize, 0)
        sizeropgen.Add(maskdata, 1, wx.EXPAND)
        maskdata.Bind(wx.EVT_BUTTON, self.Onmask)

        self.operation.SetSizer(sizeropgen)
        self.operation.Layout()
        sizeropgen.Fit(self.operation)

        gensizer = wx.BoxSizer(wx.VERTICAL)
        gensizer.Add(self.array_ops, 1, wx.EXPAND | wx.ALL)

        self.SetSizer(gensizer)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.LaunchSelection.Bind(wx.EVT_BUTTON, self.OnLaunchSelect)
        self.AllSelection.Bind(wx.EVT_BUTTON, self.OnAllSelect)
        self.MoveSelection.Bind(wx.EVT_BUTTON, self.OnMoveSelect)
        self.ResetSelection.Bind(wx.EVT_BUTTON, self.OnResetSelect)
        self.ResetAllSelection.Bind(wx.EVT_BUTTON, self.OnResetAllSelect)
        self.m_button2.Bind(wx.EVT_BUTTON, self.OnManageVectors)
        self.loadvec.Bind(wx.EVT_BUTTON, self.OnLoadvec)
        self.saveas.Bind(wx.EVT_BUTTON, self.OnSaveasvec)
        self.save.Bind(wx.EVT_BUTTON, self.OnSavevec)
        self.ApplyOp.Bind(wx.EVT_BUTTON, self.OnApplyOpMath)
        self.SelectOp.Bind(wx.EVT_BUTTON, self.OnApplyOpSelect)
        self.palapply.Bind(wx.EVT_BUTTON, self.Onupdatepal)
        self.palsave.Bind(wx.EVT_BUTTON, self.Onsavepal)
        self.palload.Bind(wx.EVT_BUTTON, self.Onloadpal)
        self.palimage.Bind(wx.EVT_BUTTON, self.Onpalimage)
        self.palchoosecolor.Bind(wx.EVT_BUTTON, self.OnClickColorPal)
        self.histoupdate.Bind(wx.EVT_BUTTON, self.OnClickHistoUpdate)
        self.histoupdatezoom.Bind(wx.EVT_BUTTON, self.OnClickHistoUpdate)
        self.histoupdateerase.Bind(wx.EVT_BUTTON, self.OnClickHistoUpdate)

    def interpolation2D(self, event: wx.MouseEvent):
        self.parentarray.interpolation2D()

    def Unmaskall(self, event: wx.MouseEvent):
        """
        Enlève le masque des tous les éléments 
        @author Pierre Archambeau
        """
        curarray: WolfArray
        curarray = self.parentarray
        curarray.mask_reset()
        curarray = self.parentarray
        curarray.updatepalette()
        curarray.delete_lists()
        
    def Unmasksel(self,event:wx.MouseEvent):
        """
        Enlève le masque des éléments sélectionnés
        @author Pierre Archambeau
        """
        curarray: WolfArray
        curarray = self.parentarray
        
        if len(curarray.mngselection.myselection) == 0:
            return
        else:
            destxy = curarray.mngselection.myselection

        destij = np.asarray([list(curarray.get_ij_from_xy(x, y)) for x, y in destxy])

        curarray.array.mask[destij[:, 0], destij[:, 1]] = False

        curarray.updatepalette()
        curarray.delete_lists()

    def InvertMask(self, event: wx.MouseEvent):

        curarray: WolfArray
        curarray = self.parentarray
        curarray.mask_invert()
        curarray = self.parentarray
        curarray.updatepalette()
        curarray.delete_lists()

    def interp2Dpolygons(self, event: wx.MouseEvent):

        choices = ["nearest", "linear", "cubic"]
        dlg = wx.SingleChoiceDialog(None, "Pick an interpolate method", "Choices", choices)
        ret = dlg.ShowModal()
        if ret == wx.ID_CANCEL:
            dlg.Destroy()
            return

        method = dlg.GetStringSelection()
        dlg.Destroy()

        actzone = self.active_zone
        curarray: WolfArray
        curarray = self.parentarray

        for curvec in actzone:
            curvec: vector
            self._interp2Dpolygon(curvec, method)

        curarray.updatepalette()
        curarray.delete_lists()

    def interp2Dpolygon(self, event: wx.MouseEvent):

        choices = ["nearest", "linear", "cubic"]
        dlg = wx.SingleChoiceDialog(None, "Pick an interpolate method", "Choices", choices)
        ret = dlg.ShowModal()
        if ret == wx.ID_CANCEL:
            dlg.Destroy()
            return

        method = dlg.GetStringSelection()
        dlg.Destroy()

        actzone = self.active_zone
        curarray: WolfArray
        curarray = self.parentarray

        self._interp2Dpolygon(self.active_vector, method)

        curarray.updatepalette()
        curarray.delete_lists()

    def _interp2Dpolygon(self, vect: vector, method):
        curarray: WolfArray
        curarray = self.parentarray

        if len(curarray.mngselection.myselection) == 0:
            destxy = curarray.get_xy_inside_polygon(vect)
        else:
            destxy = curarray.mngselection.myselection

        destij = np.asarray([list(curarray.get_ij_from_xy(x, y)) for x, y in destxy])

        xyz = vect.asnparray3d()

        newvalues = griddata(xyz[:, :2], xyz[:, 2], destxy, method=method, fill_value=-99999.)

        locmask = np.where(newvalues != -99999.)
        curarray.array.data[destij[locmask][:, 0], destij[locmask][:, 1]] = newvalues[locmask]

    def interp2Dpolylines(self, event: wx.MouseEvent):

        actzone = self.active_zone
        curarray: WolfArray
        curarray = self.parentarray

        for curvec in actzone:
            curvec: vector
            self._interp2Dpolyline(curvec)

        curarray.updatepalette()
        curarray.delete_lists()

    def interp2Dpolyline(self, event: wx.MouseEvent):

        curarray: WolfArray
        curarray = self.parentarray

        self._interp2Dpolyline(self.active_vector)

        curarray.updatepalette()
        curarray.delete_lists()

    def _interp2Dpolyline(self, vect: vector, usemask=True):

        curarray: WolfArray
        curarray = self.parentarray

        vecls = vect.asshapely_ls()
        if len(curarray.mngselection.myselection) == 0:
            allij = curarray.get_ij_under_polyline(vect, usemask)
            allxy = [curarray.get_xy_from_ij(cur[0], cur[1]) for cur in allij]
        else:
            allxy = curarray.mngselection.myselection
            allij = np.asarray([curarray.get_ij_from_xy(x,y) for x,y in allxy])

        newz = np.asarray([vecls.interpolate(vecls.project(Point(x, y))).z for x, y in allxy])
        curarray.array.data[allij[:, 0], allij[:, 1]] = newz

    def volumesurface(self, event):

        if self.parentGUI.linked:
            array1 = self.parentGUI.linkedList[0].active_array
            array2 = self.parentGUI.linkedList[1].active_array

            if array1 is self.parentarray:
                array2.mngselection.myselection = array1.mngselection.myselection.copy()
            if array2 is self.parentarray:
                array1.mngselection.myselection = array2.mngselection.myselection.copy()

            if len(self.parentarray.mngselection.myselection) == 0 or self.parentarray.mngselection.myselection == 'all':
                myarray = array1
                axs = myarray.volume_estimation()
                myarray = array2
                axs = myarray.volume_estimation(axs)
            else:
                myarray = array1.mngselection.get_newarray()
                axs = myarray.volume_estimation()
                myarray = array2.mngselection.get_newarray()
                axs = myarray.volume_estimation(axs)
        else:
            if len(self.parentarray.mngselection.myselection) == 0 or self.parentarray.mngselection.myselection == 'all':
                myarray = self.parentarray
            else:
                myarray = self.parentarray.mngselection.get_newarray()
            myarray.volume_estimation()

        plt.show()

    def OnAllSelect(self, event):
        self.parentarray.mngselection.myselection = 'all'
        self.parentarray.myops.nbselect.SetLabelText('All')

    def OnMoveSelect(self, event):
        dlg = wx.TextEntryDialog(self, 'Choose id', 'id?')
        ret = dlg.ShowModal()
        idtxt = dlg.GetValue()
        self.parentarray.mngselection.selections[idtxt] = {}
        curdict = self.parentarray.mngselection.selections[idtxt]

        curdict['select'] = self.parentarray.mngselection.myselection
        curdict['idgllist'] = 0
        self.parentarray.mngselection.myselection = []
        self.parentarray.mngselection.update_nb_nodes_sections()

        dlg = wx.ColourDialog(self)
        ret = dlg.ShowModal()
        color = dlg.GetColourData()
        curdict['color'] = color

    def OnResetSelect(self, event):
        self.parentarray.mngselection.myselection = []
        self.nbselect.SetLabelText('0')
        self.minx.SetLabelText('0')
        self.miny.SetLabelText('0')
        self.maxx.SetLabelText('0')
        self.maxy.SetLabelText('0')

    def OnResetAllSelect(self, event):
        self.OnResetSelect(0)
        self.parentarray.mngselection.selections = {}

    def OnApplyOpSelect(self, event):
        curcond = self.condition.GetSelection()

        curcondvalue = float(self.condvalue.GetValue())

        self.parentarray.mngselection.condition_select(curcond, curcondvalue)

    def OnApplyOpMath(self, event):

        curop = self.choiceop.GetSelection()
        curcond = self.condition.GetSelection()

        curopvalue = float(self.opvalue.GetValue())
        curcondvalue = float(self.condvalue.GetValue())

        self.parentarray.mngselection.treat_select(curop, curcond, curopvalue, curcondvalue)
        pass

    def Onmask(self, event):

        curop = self.choiceop.GetSelection()
        curcond = self.condition.GetSelection()

        curopvalue = float(self.opvalue.GetValue())
        curcondvalue = float(self.condvalue.GetValue())

        self.parentarray.mngselection.mask_condition(curop, curcond, curopvalue, curcondvalue)
        pass

    def OnManageVectors(self, event):
        if self.parentGUI.linked:
            if self.parentGUI.link_shareopsvect:
                if self.myzones.parentGUI in self.parentGUI.linkedList:
                    self.myzones.showstructure(self.myzones.parent, self.myzones.parentGUI)
                    return

        self.myzones.showstructure(self, self.parentGUI)

    def OnLoadvec(self, event):
        dlg = wx.FileDialog(None, 'Select file',
                            wildcard='Vec file (*.vec)|*.vec|Vecz file (*.vecz)|*.vecz|Dxf file (*.dxf)|*.dxf|All (*.*)|*.*', style=wx.FD_OPEN)

        ret = dlg.ShowModal()
        if ret == wx.ID_CANCEL:
            dlg.Destroy()
            return

        self.fnsave = dlg.GetPath()
        dlg.Destroy()
        self.myzones = Zones(self.fnsave, parent=self)

        if self.parentGUI is not None:
            if self.parentGUI.linked:
                if not self.parentGUI.linkedList is None:
                    for curFrame in self.parentGUI.linkedList:
                        if curFrame.link_shareopsvect:
                            curFrame.active_array.myops.myzones = self.myzones
                            curFrame.active_array.myops.fnsave = self.fnsave

    def OnSaveasvec(self, event):

        dlg = wx.FileDialog(None, 'Select file', wildcard='Vec file (*.vec)|*.vec|Vecz file (*.vecz)|*.vecz|All (*.*)|*.*', style=wx.FD_SAVE)

        ret = dlg.ShowModal()
        if ret == wx.ID_CANCEL:
            dlg.Destroy()
            return

        self.fnsave = dlg.GetPath()
        dlg.Destroy()
        
        self.myzones.saveas(self.fnsave)

        if self.parentGUI is not None:
            if self.parentGUI.linked:
                if not self.parentGUI.linkedList is None:
                    for curFrame in self.parentGUI.linkedList:
                        if curFrame.link_shareopsvect:
                            curFrame.active_array.myops.fnsave = self.fnsave

    def OnSavevec(self, event):

        if self.fnsave == '':
            return

        self.myzones.saveas(self.fnsave)

    def select_node_by_node(self):
        if self.parentGUI is not None:
            self.parentGUI.action = 'select node by node'
            self.parentGUI.active_array = self.parentarray

    def select_zone_inside_manager(self):

        if self.active_zone is None:
            wx.MessageBox('Please select an active zone !')
            return

        for curvec in self.active_zone.myvectors:
            self._select_vector_inside_manager(curvec)

    def select_vector_inside_manager(self):
        if self.active_vector is None:
            wx.MessageBox('Please select an active vector !')
            return

        self._select_vector_inside_manager(self.active_vector)

    def _select_vector_inside_manager(self, vect: vector):

        if len(vect.myvertices) > 2:
            self.parentarray.mngselection.select_insidepoly(vect)

        elif self.parentGUI is not None:
            if len(vect.myvertices) < 3:
                wx.MessageBox('Please add points to vector by clicks !')

            self.parentGUI.action = 'select by vector inside'
            self.parentGUI.active_array = self.parentarray
            self.Active_vector(vect)

            firstvert = wolfvertex(0., 0.)
            self.vectmp.add_vertex(firstvert)

    def select_zone_under_manager(self):

        if self.active_zone is None:
            wx.MessageBox('Please select an active zone !')
            return

        for curvec in self.active_zone.myvectors:
            self._select_vector_under_manager(curvec)

    def select_vector_under_manager(self):
        if self.active_vector is None:
            wx.MessageBox('Please select an active vector !')
            return

        self._select_vector_under_manager(self.active_vector)

    def _select_vector_under_manager(self, vect: vector):

        if len(vect.myvertices) > 1:
            self.parentarray.mngselection.select_underpoly(vect)

        elif self.parentGUI is not None:
            if len(vect.myvertices) < 2:
                wx.MessageBox('Please add points to vector by clicks !')

            self.parentGUI.action = 'select by vector under'
            self.parentGUI.active_array = self.parentarray
            self.Active_vector(vect)

            firstvert = wolfvertex(0., 0.)
            self.vectmp.add_vertex(firstvert)

    def select_vector_inside_tmp(self):
        if self.parentGUI is not None:
            self.parentGUI.action = 'select by tmp vector inside'
            self.vectmp.reset()
            self.Active_vector(self.vectmp)
            self.parentGUI.active_array = self.parentarray

            firstvert = wolfvertex(0., 0.)
            self.vectmp.add_vertex(firstvert)

    def select_vector_under_tmp(self):
        if self.parentGUI is not None:
            self.parentGUI.action = 'select by tmp vector under'
            self.vectmp.reset()
            self.Active_vector(self.vectmp)
            self.parentGUI.active_array = self.parentarray

            firstvert = wolfvertex(0., 0.)
            self.vectmp.add_vertex(firstvert)

    def OnLaunchSelect(self, event):
        id = self.selectmethod.GetSelection()

        if id == 0:
            wx.LogMessage(_('Node selection by individual clicks'))
            wx.LogMessage(_(''))
            wx.LogMessage(_('   Clicks on the desired nodes...'))
            wx.LogMessage(_(''))
            self.select_node_by_node()
        elif id == 1:
            wx.LogMessage(_('Node selection inside active vector (manager)'))
            self.select_vector_inside_manager()
        elif id == 2:
            wx.LogMessage(_('Node selection inside active zone (manager)'))
            self.select_zone_inside_manager()
        elif id == 3:
            wx.LogMessage(_('Node selection inside temporary vector'))
            wx.LogMessage(_(''))
            wx.LogMessage(_('   Choose vector by clicks...'))
            wx.LogMessage(_(''))
            self.select_vector_inside_tmp()
        elif id == 4:
            wx.LogMessage(_('Node selection under active vector (manager)'))
            self.select_vector_under_manager()
        elif id == 5:
            wx.LogMessage(_('Node selection under active zone (manager)'))
            self.select_zone_under_manager()
        elif id == 6:
            wx.LogMessage(_('Node selection under temporary vector'))
            wx.LogMessage(_(''))
            wx.LogMessage(_('   Choose vector by clicks...'))
            wx.LogMessage(_(''))
            self.select_vector_under_tmp()

    def onclose(self, event):
        self.Hide()

    def Active_vector(self, vect: vector, copyall=True):
        if vect is None:
            return
        self.active_vector = vect
        self.active_vector_id.SetLabelText(vect.myname)

        if vect.parentzone is not None:
            self.active_zone = vect.parentzone

        if self.parentGUI is not None and copyall:
            self.parentGUI.Active_vector(vect)

    def Active_zone(self, zone):
        self.active_zone = zone
        if self.parentGUI is not None:
            self.parentGUI.Active_zone(zone)

    def update_palette(self):
        self.Palette.add_ax()
        fig, ax = self.Palette.get_fig_ax()
        self.parentarray.mypal.plot(fig, ax)
        fig.canvas.draw()
        self.parentarray.mypal.fillgrid(self.palgrid)

    def Onsavepal(self, event):
        myarray: WolfArray
        myarray = self.parentarray
        myarray.mypal.savefile()

    def Onloadpal(self, event):
        myarray: WolfArray
        myarray = self.parentarray
        myarray.mypal.readfile()
        myarray.updatepalette(0)
        myarray.delete_lists()
        self.update_palette()

    def Onpalimage(self, event):
        myarray: WolfArray
        myarray = self.parentarray
        myarray.mypal.export_image()

    def Onupdatepal(self, event):
        curarray: WolfArray
        curarray = self.parentarray

        auto = self.palauto.IsChecked()

        oldalpha = curarray.alpha
        if self.palalpha.IsChecked():
            curarray.alpha = 1.
        else:
            curarray.alpha = float(self.palalphaslider.GetValue()) / 100.

        ret = curarray.mypal.updatefromgrid(self.palgrid)
        if curarray.mypal.automatic != auto or curarray.alpha != oldalpha or ret:
            curarray.mypal.automatic = auto
            curarray.updatepalette(0)
            curarray.delete_lists()

        shadehill = self.palshader.IsChecked()
        if not curarray.shading and shadehill:
            curarray.shading = True

        azim = float(self.palazimuthhillshade.GetValue())
        alti = float(self.palaltitudehillshade.GetValue())

        if curarray.azimuthhill != azim:
            curarray.azimuthhill = azim
            curarray.shading = True

        if curarray.altitudehill != alti:
            curarray.altitudehill = alti
            curarray.shading = True

        alpha = float(self.palalphahillshade.GetValue()) / 100.
        if curarray.shaded.alpha != alpha:
            curarray.shaded.alpha = alpha
            curarray.shading = True

    def OnClickHistoUpdate(self, event: wx.Event):

        itemlabel = event.GetEventObject().GetLabel()
        fig, ax = self.histo.get_fig_ax()

        if itemlabel == self.histoupdateerase.LabelText:
            ax.clear()
            fig.canvas.draw()
            return

        myarray: WolfArray
        myarray = self.parentarray

        onzoom = []
        if itemlabel == self.histoupdatezoom.LabelText:
            if self.parentGUI is not None:
                onzoom = [self.parentGUI.xmin, self.parentGUI.xmax, self.parentGUI.ymin, self.parentGUI.ymax]

        partarray = myarray.get_working_array(onzoom).flatten(order='F')  # .sort(axis=-1)

        ax: Axis
        ax.hist(partarray, 200, density=True)

        fig.canvas.draw()

    def OnClickColorPal(self, event):

        gridto = self.palgrid
        k = gridto.GetGridCursorRow()
        r = int(gridto.GetCellValue(k, 1))
        g = int(gridto.GetCellValue(k, 2))
        b = int(gridto.GetCellValue(k, 3))

        curcol = wx.ColourData()
        curcol.SetChooseFull(True)
        curcol.SetColour(wx.Colour(r, g, b))

        dlg = wx.ColourDialog(None, curcol)
        ret = dlg.ShowModal()

        if ret == wx.ID_CANCEL:
            return

        curcol = dlg.GetColourData()
        rgb = curcol.GetColour()

        k = gridto.GetGridCursorRow()
        gridto.SetCellValue(k, 1, str(rgb.red))
        gridto.SetCellValue(k, 2, str(rgb.green))
        gridto.SetCellValue(k, 3, str(rgb.blue))


class SelectionData():
    myselection: list
    selections: dict

    def __init__(self, parent) -> None:
        self.parent: WolfArray
        self.parent = parent

        self.dx = parent.dx
        self.dy = parent.dy

        self.myselection = []
        self.selections = {}
        self.update_plot_selection = False
        self.hideselection = False
        self.numlist_select = 0

    def plot_selection(self):

        if self.myselection != 'all':
            if len(self.myselection) > 0:
                self.numlist_select = self._plot_selection(self.myselection, (1., 0., 0.), self.numlist_select)

        if len(self.selections) > 0:
            for cur in self.selections.values():
                if cur['select'] != 'all':
                    col = cur['color'].GetColour()
                    cur['idgllist'] = self._plot_selection(cur['select'],
                                                           (float(col[0]) / 255., float(col[1]) / 255.,
                                                            float(col[2]) / 255.),
                                                           cur['idgllist'])

    def _plot_selection(self, curlist, color, loclist=0):

        if self.update_plot_selection:
            if loclist != 0:
                glDeleteLists(loclist, 1)

            loclist = glGenLists(1)
            glNewList(loclist, GL_COMPILE)

            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            glBegin(GL_QUADS)
            for cursel in curlist:
                x1 = cursel[0] - self.dx / 2.
                x2 = cursel[0] + self.dx / 2.
                y1 = cursel[1] - self.dy / 2.
                y2 = cursel[1] + self.dy / 2.
                glColor3f(color[0], color[1], color[2])
                glVertex2f(x1, y1)
                glVertex2f(x2, y1)
                glVertex2f(x2, y2)
                glVertex2f(x1, y2)
            glEnd()

            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            for cursel in curlist:
                glBegin(GL_LINE_STRIP)
                x1 = cursel[0] - self.dx / 2.
                x2 = cursel[0] + self.dx / 2.
                y1 = cursel[1] - self.dy / 2.
                y2 = cursel[1] + self.dy / 2.
                glColor3f(0., 1., 0.)
                glVertex2f(x1, y1)
                glVertex2f(x2, y1)
                glVertex2f(x2, y2)
                glVertex2f(x1, y2)
                glVertex2f(x1, y1)
                glEnd()

            glEndList()
            self.update_plot_selection = False
        else:
            if loclist != 0:
                glCallList(loclist)

        return loclist

    def add_node_to_selection(self, x, y, verif=True):
        '''Ajout d'une coordonnée à la sélection'''
        # on repasse par les i,j car les coordonnées transférées peuvent venir d'un click souris
        # le but est de ne conserver que les coordonnées des CG de mailles
        i, j = self.parent.get_ij_from_xy(x, y)
        self.add_node_to_selectionij(i, j, verif)

    def add_nodes_to_selection(self, xy, verif=True):
        '''Ajout d'une liste de coordonnées à la sélection'''
        # on repasse par les i,j car les coordonnées transférées peuvent venir d'un click souris
        # le but est de ne conserver que les coordonnées des CG de mailles
        ij = [self.parent.get_ij_from_xy(x, y) for x, y in xy]
        self.add_nodes_to_selectionij(ij, verif)

    def add_node_to_selectionij(self, i, j, verif=True):
        '''Ajout d'un couple d'indices à la sélection'''
        x1, y1 = self.parent.get_xy_from_ij(i, j)

        if verif:
            try:
                ret = self.myselection.index((x1, y1))
            except:
                ret = -1
            if ret >= 0:
                self.myselection.pop(ret)
            else:
                self.myselection.append((x1, y1))
        else:
            self.myselection.append((x1, y1))

    def add_nodes_to_selectionij(self, ij, verif=True):
        '''Ajout d'une liste de couples d'indices à la sélection'''
        if len(ij)==0:
            wx.LogDebug(_('Nothing to do in add_nodes_to_selectionij !'))
            return

        nbini = len(self.myselection)

        xy = [self.parent.get_xy_from_ij(i, j) for i, j in ij]

        self.myselection += xy

        if nbini != 0:
            if verif:
                # trouve les éléments uniques dans la liste de tuples (--> axis=0) et retourne également le comptage
                selunique, counts = np.unique(self.myselection, return_counts=True, axis=0)

                # les éléments énumérés plus d'une fois doivent être enlevés
                #  on trie par ordre décroissant
                locsort = sorted(zip(counts.tolist(), selunique.tolist()), reverse=True)
                counts = [x[0] for x in locsort]
                sel = [tuple(x[1]) for x in locsort]

                # on recherche le premier 1
                idx = counts.index(1)
                # on ne conserve que la portion de liste utile
                self.myselection = sel[idx:]
            else:
                self.myselection = np.unique(self.myselection, axis=0)

    def select_insidepoly(self, myvect: vector):

        nbini = len(self.myselection)

        myvect.find_minmax()
        mypoints,_ = self.parent.get_xy_infootprint_vect(myvect)
        path = mpltPath.Path(myvect.asnparray())
        inside = path.contains_points(mypoints)

        if self.parent.myops.selectrestricttomask.IsChecked():
            self.hideselection=True            

        self.add_nodes_to_selection(mypoints[np.where(inside)], verif=nbini != 0)
        if self.parent.myops.selectrestricttomask.IsChecked():
            self.condition_select('Mask',0)

        self.hideselection=False
        self.update_nb_nodes_sections()

    def select_underpoly(self, myvect: vector):

        nbini = len(self.myselection)

        myvect.find_minmax()
        mypoints = self.parent.get_ij_under_polyline(myvect)

        self.add_nodes_to_selectionij(mypoints, verif=nbini != 0)

        if self.parent.myops.selectrestricttomask.IsChecked():
            self.condition_select('Mask',0)

        self.update_nb_nodes_sections()

    def update_nb_nodes_sections(self):
        
        if self.myselection=='all':
            nb = self.parent.nbnotnull
        else:
            nb = len(self.myselection)
        
        if nb > 10000:
            if not self.hideselection:
                self.update_plot_selection = False  # on met par défaut à False car OpenGL va demander une MAJ de l'affichage le temps que l'utilisateur réponde
                dlg = wx.MessageDialog(None,
                                       'Large selection !!' + str(nb) + '\n Would you like to plot the selected cells?',
                                       style=wx.YES_NO)
                ret = dlg.ShowModal()
                if ret == wx.ID_YES:
                    self.update_plot_selection = True
                else:
                    self.update_plot_selection = False
                    self.hideselection = True
                dlg.Destroy()
        else:
            self.update_plot_selection = True

        self.parent.myops.nbselect.SetLabelText(str(nb))
        if nb>0:
            self.parent.myops.minx.SetLabelText(str(np.min(np.asarray(self.myselection)[:, 0])))
            self.parent.myops.miny.SetLabelText(str(np.min(np.asarray(self.myselection)[:, 1])))
            self.parent.myops.maxx.SetLabelText(str(np.max(np.asarray(self.myselection)[:, 0])))
            self.parent.myops.maxy.SetLabelText(str(np.max(np.asarray(self.myselection)[:, 1])))

    def condition_select(self, cond, condval, condval2=0, usemask=False):
        array = self.parent.array
        nbini = len(self.myselection)

        if usemask :
            mask=np.logical_not(array.mask)
            if nbini == 0:
                if cond == 0 or cond=='<':
                    # <
                    ij = np.argwhere((array < condval) & mask)
                elif cond == 1 or cond=='<=':
                    # <=
                    ij = np.argwhere((array <= condval) & mask)
                elif cond == 2 or cond=='==':
                    # ==
                    ij = np.argwhere((array == condval) & mask)
                elif cond == 3 or cond=='>=':
                    # >=
                    ij = np.argwhere((array >= condval) & mask)
                elif cond == 4 or cond=='>':
                    # >
                    ij = np.argwhere((array > condval) & mask)
                elif cond == 5 or cond=='NaN':
                    # NaN
                    ij = np.argwhere((np.isnan(array)) & mask)
                elif cond == 6 or cond=='>=<=':
                    # interval with equality
                    ij = np.argwhere(((array>=condval) & (array<=condval2)) & mask)
                elif cond == 7 or cond=='><':
                    # interval without equality
                    ij = np.argwhere(((array>condval) & (array<condval2)) & mask)
                elif cond == 8 or cond=='<>':
                    # interval without equality
                    ij = np.argwhere(((array<condval) | (array>condval2)) & mask)

                self.add_nodes_to_selectionij(ij, nbini != 0)
            else:
                sel = np.asarray(self.myselection)
                ijall = np.asarray(self.parent.get_ij_from_xy(sel[:, 0], sel[:, 1])).transpose()
                if cond == 0 or cond=='<':
                    # <
                    ij = np.argwhere((array[ijall[:, 0], ijall[:, 1]] < condval) & (mask[ijall[:, 0], ijall[:, 1]]))
                elif cond == 1 or cond=='<=':
                    # <=
                    ij = np.argwhere((array[ijall[:, 0], ijall[:, 1]] <= condval) & (mask[ijall[:, 0], ijall[:, 1]]))
                elif cond == 2 or cond=='==':
                    # ==
                    ij = np.argwhere((array[ijall[:, 0], ijall[:, 1]] == condval) & (mask[ijall[:, 0], ijall[:, 1]]))
                elif cond == 3 or cond=='>=':
                    # >=
                    ij = np.argwhere((array[ijall[:, 0], ijall[:, 1]] >= condval) & (mask[ijall[:, 0], ijall[:, 1]]))
                elif cond == 4 or cond=='>':
                    # >
                    ij = np.argwhere((array[ijall[:, 0], ijall[:, 1]] > condval) & (mask[ijall[:, 0], ijall[:, 1]]))
                elif cond == 5 or cond=='NaN':
                    # NaN
                    ij = np.argwhere((np.isnan(array[ijall[:, 0], ijall[:, 1]])) & (mask[ijall[:, 0], ijall[:, 1]]))           
                elif cond == 6 or cond=='>=<=':
                    # interval with equality
                    ij = np.argwhere(((array[ijall[:, 0], ijall[:, 1]]>=condval) & (array[ijall[:, 0], ijall[:, 1]]<=condval2)) & (mask[ijall[:, 0], ijall[:, 1]]))
                elif cond == 7 or cond=='><':
                    # interval without equality
                    ij = np.argwhere(((array[ijall[:, 0], ijall[:, 1]]>condval) & (array[ijall[:, 0], ijall[:, 1]]<condval2)) & (mask[ijall[:, 0], ijall[:, 1]]))
                elif cond == 8 or cond=='<>':
                    # interval without equality
                    ij = np.argwhere(((array[ijall[:, 0], ijall[:, 1]]<condval) | (array[ijall[:, 0], ijall[:, 1]]>condval2)) & (mask[ijall[:, 0], ijall[:, 1]]))

                ij = ij.flatten()
                self.add_nodes_to_selectionij(ijall[ij], nbini != 0)
        else:
            if nbini == 0:
                if cond == 0 or cond=='<':
                    # <
                    ij = np.argwhere(array < condval)
                elif cond == 1 or cond=='<=':
                    # <=
                    ij = np.argwhere(array <= condval)
                elif cond == 2 or cond=='==':
                    # ==
                    ij = np.argwhere(array == condval)
                elif cond == 3 or cond=='>=':
                    # >=
                    ij = np.argwhere(array >= condval)
                elif cond == 4 or cond=='>':
                    # >
                    ij = np.argwhere(array > condval)
                elif cond == 5 or cond=='NaN':
                    # NaN
                    ij = np.argwhere(np.isnan(array))
                elif cond == 6 or cond=='>=<=':
                    # interval with equality
                    ij = np.argwhere((array>=condval) & (array<=condval2))
                elif cond == 7 or cond=='><':
                    # interval without equality
                    ij = np.argwhere((array>condval) & (array<condval2))
                elif cond == 8 or cond=='<>':
                    # interval without equality
                    ij = np.argwhere((array<condval) | (array>condval2))
                elif cond == -1 or cond=='Mask':
                    # Mask
                    ij = np.argwhere(array.mask)
                elif cond == -2 or cond=='NotMask':
                    # Mask
                    ij = np.argwhere(np.logical_not(array.mask))

                self.add_nodes_to_selectionij(ij, nbini != 0)
            else:
                sel = np.asarray(self.myselection)
                ijall = np.asarray(self.parent.get_ij_from_xy(sel[:, 0], sel[:, 1])).transpose()

                if cond == 0 or cond=='<':
                    # <
                    ij = np.argwhere(array[ijall[:, 0], ijall[:, 1]] < condval)
                elif cond == 1 or cond=='<=':
                    # <=
                    ij = np.argwhere(array[ijall[:, 0], ijall[:, 1]] <= condval)
                elif cond == 2 or cond=='==':
                    # ==
                    ij = np.argwhere(array[ijall[:, 0], ijall[:, 1]] == condval)
                elif cond == 3 or cond=='>=':
                    # >=
                    ij = np.argwhere(array[ijall[:, 0], ijall[:, 1]] >= condval)
                elif cond == 4 or cond=='>':
                    # >
                    ij = np.argwhere(array[ijall[:, 0], ijall[:, 1]] > condval)
                elif cond == 5 or cond=='NaN':
                    # NaN
                    ij = np.argwhere(np.isnan(array[ijall[:, 0], ijall[:, 1]]))
                elif cond == 6 or cond=='>=<=':
                    # interval with equality
                    ij = np.argwhere((array[ijall[:, 0], ijall[:, 1]]>=condval) & (array[ijall[:, 0], ijall[:, 1]]<=condval2))
                elif cond == 7 or cond=='><':
                    # interval without equality
                    ij = np.argwhere((array[ijall[:, 0], ijall[:, 1]]>condval) & (array[ijall[:, 0], ijall[:, 1]]<condval2))
                elif cond == 8 or cond=='<>':
                    # interval without equality
                    ij = np.argwhere((array[ijall[:, 0], ijall[:, 1]]<condval) | (array[ijall[:, 0], ijall[:, 1]]>condval2) )
                elif cond == -1 or cond=='Mask':
                    # Mask
                    ij = np.argwhere(array.mask[ijall[:, 0], ijall[:, 1]])
                elif cond == -2 or cond=='NotMask':
                    # Mask
                    ij = np.argwhere(np.logical_not(array.mask[ijall[:, 0], ijall[:, 1]]))

                ij = ij.flatten()
                self.add_nodes_to_selectionij(ijall[ij], nbini != 0)

        self.update_nb_nodes_sections()

    def treat_select(self, op, cond, opval, condval):
        # operationChoices = [ u"+", u"-", u"*", u"/", u"replace'" ]
        # conditionChoices = [ u"<", u"<=", u"=", u">=", u">",u"isNaN" ]
        def test(val, cond, condval):
            if cond == 0:
                return val < condval
            elif cond == 1:
                return val <= condval
            elif cond == 2:
                return val == condval
            elif cond == 3:
                return val >= condval
            elif cond == 4:
                return val > condval
            elif cond == 5:
                return np.isnan(val)

        array = self.parent.array
        if self.myselection == 'all':
            if op == 0:
                if cond == 0:
                    # <
                    ind = np.argwhere(np.logical_and(array < condval, np.logical_not(array.mask)))
                    array[ind[:, 0], ind[:, 1]] += opval
                elif cond == 1:
                    # <=
                    ind = np.argwhere(np.logical_and(array <= condval, np.logical_not(array.mask)))
                    array[ind[:, 0], ind[:, 1]] += opval
                elif cond == 2:
                    # ==
                    ind = np.argwhere(np.logical_and(array == condval, np.logical_not(array.mask)))
                    array[ind[:, 0], ind[:, 1]] += opval
                elif cond == 3:
                    # >=
                    ind = np.argwhere(np.logical_and(array >= condval, np.logical_not(array.mask)))
                    array[ind[:, 0], ind[:, 1]] += opval
                elif cond == 4:
                    # >
                    ind = np.argwhere(np.logical_and(array > condval, np.logical_not(array.mask)))
                    array[ind[:, 0], ind[:, 1]] += opval
                elif cond == 5:
                    # NaN
                    ind = np.argwhere(np.logical_and(np.isnan(array), np.logical_not(array.mask)))
                    array[ind[:, 0], ind[:, 1]] = opval
            elif op == 1:
                if cond == 0:
                    # <
                    ind = np.argwhere(np.logical_and(array < condval, np.logical_not(array.mask)))
                    array[ind[:, 0], ind[:, 1]] -= opval
                elif cond == 1:
                    # <=
                    ind = np.argwhere(np.logical_and(array <= condval, np.logical_not(array.mask)))
                    array[ind[:, 0], ind[:, 1]] -= opval
                elif cond == 2:
                    # ==
                    ind = np.argwhere(np.logical_and(array == condval, np.logical_not(array.mask)))
                    array[ind[:, 0], ind[:, 1]] -= opval
                elif cond == 3:
                    # >=
                    ind = np.argwhere(np.logical_and(array >= condval, np.logical_not(array.mask)))
                    array[ind[:, 0], ind[:, 1]] -= opval
                elif cond == 4:
                    # >
                    ind = np.argwhere(np.logical_and(array > condval, np.logical_not(array.mask)))
                    array[ind[:, 0], ind[:, 1]] -= opval
                elif cond == 5:
                    # NaN
                    ind = np.argwhere(np.logical_and(np.isnan(array), np.logical_not(array.mask)))
                    array[ind[:, 0], ind[:, 1]] = opval
            elif op == 2:
                if cond == 0:
                    # <
                    ind = np.argwhere(np.logical_and(array < condval, np.logical_not(array.mask)))
                    array[ind[:, 0], ind[:, 1]] *= opval
                elif cond == 1:
                    # <=
                    ind = np.argwhere(np.logical_and(array <= condval, np.logical_not(array.mask)))
                    array[ind[:, 0], ind[:, 1]] *= opval
                elif cond == 2:
                    # ==
                    ind = np.argwhere(np.logical_and(array == condval, np.logical_not(array.mask)))
                    array[ind[:, 0], ind[:, 1]] *= opval
                elif cond == 3:
                    # >=
                    ind = np.argwhere(np.logical_and(array >= condval, np.logical_not(array.mask)))
                    array[ind[:, 0], ind[:, 1]] *= opval
                elif cond == 4:
                    # >
                    ind = np.argwhere(np.logical_and(array > condval, np.logical_not(array.mask)))
                    array[ind[:, 0], ind[:, 1]] *= opval
                elif cond == 5:
                    # NaN
                    ind = np.argwhere(np.logical_and(np.isnan(array), np.logical_not(array.mask)))
                    array[ind[:, 0], ind[:, 1]] = opval
            elif op == 3 and opval != 0.:
                if cond == 0:
                    # <
                    ind = np.argwhere(np.logical_and(array < condval, np.logical_not(array.mask)))
                    array[ind[:, 0], ind[:, 1]] /= opval
                elif cond == 1:
                    # <=
                    ind = np.argwhere(np.logical_and(array <= condval, np.logical_not(array.mask)))
                    array[ind[:, 0], ind[:, 1]] /= opval
                elif cond == 2:
                    # ==
                    ind = np.argwhere(np.logical_and(array == condval, np.logical_not(array.mask)))
                    array[ind[:, 0], ind[:, 1]] /= opval
                elif cond == 3:
                    # >=
                    ind = np.argwhere(np.logical_and(array >= condval, np.logical_not(array.mask)))
                    array[ind[:, 0], ind[:, 1]] /= opval
                elif cond == 4:
                    # >
                    ind = np.argwhere(np.logical_and(array > condval, np.logical_not(array.mask)))
                    array[ind[:, 0], ind[:, 1]] /= opval
                elif cond == 5:
                    # NaN
                    ind = np.argwhere(np.logical_and(np.isnan(array), np.logical_not(array.mask)))
                    array[ind[:, 0], ind[:, 1]] = 0
            elif op == 4:
                if cond == 0:
                    # <
                    ind = np.argwhere(np.logical_and(array < condval, np.logical_not(array.mask)))
                    array[ind[:, 0], ind[:, 1]] = opval
                elif cond == 1:
                    # <=
                    ind = np.argwhere(np.logical_and(array <= condval, np.logical_not(array.mask)))
                    array[ind[:, 0], ind[:, 1]] = opval
                elif cond == 2:
                    # ==
                    ind = np.argwhere(np.logical_and(array == condval, np.logical_not(array.mask)))
                    array[ind[:, 0], ind[:, 1]] = opval
                elif cond == 3:
                    # >=
                    ind = np.argwhere(np.logical_and(array >= condval, np.logical_not(array.mask)))
                    array[ind[:, 0], ind[:, 1]] = opval
                elif cond == 4:
                    # >
                    ind = np.argwhere(np.logical_and(array > condval, np.logical_not(array.mask)))
                    array[ind[:, 0], ind[:, 1]] = opval
                elif cond == 5:
                    # NaN
                    ind = np.argwhere(np.logical_and(np.isnan(array), np.logical_not(array.mask)))
                    array[ind[:, 0], ind[:, 1]] = opval
        else:
            ij = [self.parent.get_ij_from_xy(cur[0], cur[1]) for cur in self.myselection]

            if op == 0:
                for i, j in ij:
                    if test(array.data[i, j], cond, condval):
                        array.data[i, j] += opval
            elif op == 1:
                for i, j in ij:
                    if test(array.data[i, j], cond, condval):
                        array.data[i, j] -= opval
            elif op == 2:
                for i, j in ij:
                    if test(array.data[i, j], cond, condval):
                        array.data[i, j] *= opval
            elif op == 3 and opval != 0.:
                for i, j in ij:
                    if test(array.data[i, j], cond, condval):
                        array.data[i, j] /= opval
            elif op == 4:
                for i, j in ij:
                    if test(array.data[i, j], cond, condval):
                        array.data[i, j] = opval

        self.parent.mask_data(self.parent.nullvalue)
        self.parent.updatepalette()
        self.parent.delete_lists()

    def mask_condition(self, op, cond, opval, condval):
        # operationChoices = [ u"+", u"-", u"*", u"/", u"replace'" ]
        # conditionChoices = [ u"<", u"<=", u"=", u">=", u">",u"isNaN" ]
        def test(val, cond, condval):
            if cond == 0:
                return val < condval
            elif cond == 1:
                return val <= condval
            elif cond == 2:
                return val == condval
            elif cond == 3:
                return val >= condval
            elif cond == 4:
                return val > condval
            elif cond == 5:
                return np.isnan(val)

        array = self.parent.array
        if self.myselection == 'all':
            if cond == 0:
                # <
                ind = np.argwhere(np.logical_and(array < condval, np.logical_not(array.mask)))
            elif cond == 1:
                # <=
                ind = np.argwhere(np.logical_and(array <= condval, np.logical_not(array.mask)))
            elif cond == 2:
                # ==
                ind = np.argwhere(np.logical_and(array == condval, np.logical_not(array.mask)))
            elif cond == 3:
                # >=
                ind = np.argwhere(np.logical_and(array >= condval, np.logical_not(array.mask)))
            elif cond == 4:
                # >
                ind = np.argwhere(np.logical_and(array > condval, np.logical_not(array.mask)))
            elif cond == 5:
                # NaN
                ind = np.argwhere(np.logical_and(np.isnan(array), np.logical_not(array.mask)))

            array.mask[ind[:, 0], ind[:, 1]] = True

        else:
            ij = [self.parent.get_ij_from_xy(cur[0], cur[1]) for cur in self.myselection]

            for i, j in ij:
                if test(array.data[i, j], cond, condval):
                    array.mask[i, j] = True

        self.parent.nbnotnull = array.count()
        self.parent.updatepalette()
        self.parent.delete_lists()

    def get_values_sel(self):

        if self.myselection == 'all':
            return -99999
        else:
            sel = np.asarray(self.myselection)
            if len(sel) == 1:
                ijall = np.asarray(self.parent.get_ij_from_xy(sel[0, 0], sel[0, 1])).transpose()
                z = self.parent.array[ijall[0], ijall[1]]
            else:
                ijall = np.asarray(self.parent.get_ij_from_xy(sel[:, 0], sel[:, 1])).transpose()
                z = self.parent.array[ijall[:, 0], ijall[:, 1]].flatten()

        return z

    def get_header(self):
        array: WolfArray

        array = self.parent
        sel = np.asarray(self.myselection)

        myhead = header_wolf()

        myhead.dx = array.dx
        myhead.dy = array.dy
        myhead.translx = 0.  # array.translx
        myhead.transly = 0.  # array.transly

        myhead.origx = np.amin(sel[:, 0]) - array.dx / 2.
        myhead.origy = np.amin(sel[:, 1]) - array.dy / 2.

        ex = np.amax(sel[:, 0]) + array.dx / 2.
        ey = np.amax(sel[:, 1]) + array.dy / 2.

        myhead.nbx = int((ex - myhead.origx) / array.dx)
        myhead.nby = int((ey - myhead.origy) / array.dy)

        return myhead

    def get_newarray(self):

        newarray = WolfArray()
        newarray.init_from_header(self.get_header())

        sel = np.asarray(self.myselection)
        if len(sel) == 1:
            ijall = np.asarray(self.parent.get_ij_from_xy(sel[0, 0], sel[0, 1])).transpose()
            z = self.parent.array[ijall[0], ijall[1]]
        else:
            ijall = np.asarray(self.parent.get_ij_from_xy(sel[:, 0], sel[:, 1])).transpose()
            z = self.parent.array[ijall[:, 0], ijall[:, 1]].flatten()

        newarray.array[:, :] = -99999.
        newarray.nullvalue = -99999.

        newarray.set_values_sel(sel, z)

        return newarray


# Objet Wolf Array en simple précision
class WolfArray(header_wolf):
    """ Classe pour l'importation de WOLF arrays"""
    array: ma.masked_array
    mygrid: dict
    idx: str

    myops: Ops_Array

    def __init__(self, fname=None, mold=None, masknull=True, crop=None,
                 whichtype=WOLF_ARRAY_FULL_SINGLE, preload=True,
                 create=False, parentgui=None,nullvalue=0.,srcheader=None):
        super().__init__()

        self.parentGUI = parentgui
        self.idx = ''
        self.flipupd=False
        self.array = None
        
        self.linkedvec = None

        self.filename = ""
        self.nbdims = 2
        self.isblock = False
        self.blockindex = 0
        self.wolftype = whichtype

        self.preload = preload
        self.loaded = False
        self.masknull = masknull

        self.rgb = None
        self.mypal = None
        self.alpha = 1.
        self.shading = False

        self.azimuthhill = 315.
        self.altitudehill = 0.

        if self.wolftype != WOLF_ARRAY_HILLSHAPE and parentgui is not None:
            self.shaded = WolfArray(whichtype=WOLF_ARRAY_HILLSHAPE)
            self.shaded.mypal.defaultgray()
            self.shaded.mypal.automatic = False

        self.nullvalue = nullvalue
        self.nbnotnull = 99999
        self.nbnotnullzoom = 99999
        self.nbtoplot = 0

        self.gridsize = 100
        self.gridmaxscales = -1

        self.plotted = False
        self.plotting = False

        self.mypal = wolfpalette(None, "Palette of colors")
        self.mypal.default16()
        self.mypal.automatic = True
        self.mygrid = {}

        self.cropini = crop
        
        if type(srcheader) is header_wolf:
            header=srcheader
            self.origx = header.origx
            self.origy = header.origy
            self.origz = header.origz

            self.translx = header.translx
            self.transly = header.transly
            self.translz = header.translz

            self.dx = header.dx
            self.dy = header.dy
            self.dz = header.dz

            self.nbx = header.nbx
            self.nby = header.nby
            self.nbz = header.nbz

            self.nb_blocks = header.nb_blocks
            self.head_blocks = header.head_blocks.copy()

        """ Constructeur d'un WOLF array """
        if fname is not None:
            self.filename = fname
            self.read_all()
            if masknull and self.preload:
                self.mask_data(self.nullvalue)

        elif mold is not None:
            self.nbdims = mold.nbdims
            self.nbx = mold.nbx
            self.nby = mold.nby
            self.nbz = mold.nbz
            self.dx = mold.dx
            self.dy = mold.dy
            self.dz = mold.dz
            self.origx = mold.origx
            self.origy = mold.origy
            self.origz = mold.origz
            self.translx = mold.translx
            self.transly = mold.transly
            self.translz = mold.translz
            self.array = ma.copy(mold.array)
            # return

        elif create:
            new = NewArray(None)
            ret = new.ShowModal()
            if ret == wx.ID_CANCEL:
                return
            else:
                self.init_from_new(new)

        self.add_ops_sel()
        
    def loadnap_and_apply(self):
        
        file_name, file_extension = os.path.splitext(self.filename)
        fnnap = file_name + '.napbin'
        if os.path.exists(fnnap):
            locnap = WolfArray(fnnap)
            
            self.array.data[np.where(locnap.array.mask)] = self.nullvalue
            self.mask_data(self.nullvalue)
            
            self.reset_plot()
    
    def filter_inundation(self,eps):

        self.array[np.where(self.array<eps)] = 0.
        if self.linkedvec is not None:
            self.mask_outsidepoly(self.linkedvec)
            
        self.reset_plot()

    def export_geotif(self,outdir='',extent = ''):
        from osgeo import gdal, osr, gdalconst
        
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(31370)

        filename = join(outdir,self.idx)+extent+'.tif'
                
        arr=self.array
        if arr.dtype == np.float32:
            arr_type = gdal.GDT_Float32
        else:
            arr_type = gdal.GDT_Int32

        driver: gdal.Driver
        out_ds: gdal.Dataset
        band: gdal.Band
        driver = gdal.GetDriverByName("GTiff")
        out_ds = driver.Create(filename, arr.shape[0], arr.shape[1], 1, arr_type)
        out_ds.SetProjection(srs.ExportToWkt())
        out_ds.SetGeoTransform([self.origx+self.translx,
                                self.dx,
                                0.,
                                self.origy+self.transly,
                                0.,
                                self.dy])
        band = out_ds.GetRasterBand(1)
        band.SetNoDataValue(0.)
        band.WriteArray(arr.transpose())
        band.FlushCache()
        band.ComputeStatistics(False)        
    
    def add_ops_sel(self):

        if self.parentGUI is not None:
            self.myops = Ops_Array(None, self, self.parentGUI)
            self.myops.Hide()

            self.mngselection = SelectionData(self)

        else:
            self.myops = None
            self.mngselection = None

    def change_gui(self, newparentgui):
        if self.parentGUI is None:
            self.parentGUI = newparentgui
            self.add_ops_sel()
        else:
            self.parentGUI = newparentgui
            self.myops.parentGUI = newparentgui

    def compare_cloud(self,mycloud:cloud_vertices):
        
        xyz_cloud = mycloud.get_xyz()
        zarray = np.array([self.get_value(curxy[0],curxy[1]) for curxy in xyz_cloud])
        
        nbout = np.count_nonzero(zarray==-99999)
        
        z_cloud = xyz_cloud[zarray!=-99999][:,2]
        xy_cloud = xyz_cloud[zarray!=-99999][:,:2]
        zarray = zarray[zarray!=-99999]
        
        zall = np.concatenate([z_cloud,zarray])
        zmin = np.min(zall)
        zmax = np.max(zall)
        
        diffz = zarray-z_cloud
        cmap = plt.cm.get_cmap('RdYlBu')
        mindiff = np.min(diffz)
        maxdiff = np.max(diffz)

        fig,ax = plt.subplots(2,1)
        ax[0].set_title(_('Comparison Z - ') + str(nbout) + _(' outside points on ') + str(len(xyz_cloud)))
        sc0 = ax[0].scatter(z_cloud,zarray,s=10,c=diffz,cmap = cmap, vmin=mindiff, vmax=maxdiff)
        ax[0].set_xlabel(_('Scatter values'))
        ax[0].set_ylabel(_('Array values'))
        ax[0].set_xlim([zmin,zmax])
        ax[0].set_ylim([zmin,zmax])       
        ax[0].plot([zmin,zmax],[zmin,zmax])
        ax[0].axis('equal')

        sc1 = ax[1].scatter(xy_cloud[:,0],xy_cloud[:,1],s=10,c=diffz,cmap = cmap, vmin=mindiff, vmax=maxdiff)
        fig.colorbar(sc1)
        ax[1].axis('equal')
        
        plt.show()
        
    def compare_tri(self,mytri:Triangulation):
        
        xyz_cloud = mytri.pts
        zarray = np.array([self.get_value(curxy[0],curxy[1]) for curxy in xyz_cloud])
        
        nbout = np.count_nonzero(zarray==-99999)
        
        z_cloud = xyz_cloud[zarray!=-99999][:,2]
        xy_cloud = xyz_cloud[zarray!=-99999][:,:2]
        zarray = zarray[zarray!=-99999]
        
        zall = np.concatenate([z_cloud,zarray])
        zmin = np.min(zall)
        zmax = np.max(zall)
        
        diffz = zarray-z_cloud
        cmap = plt.cm.get_cmap('RdYlBu')
        mindiff = np.min(diffz)
        maxdiff = np.max(diffz)

        fig,ax = plt.subplots(2,1)
        ax[0].set_title(_('Comparison Z - ') + str(nbout) + _(' outside points on ') + str(len(xyz_cloud)))
        sc0 = ax[0].scatter(z_cloud,zarray,s=10,c=diffz,cmap = cmap, vmin=mindiff, vmax=maxdiff)
        ax[0].set_xlabel(_('Scatter values'))
        ax[0].set_ylabel(_('Array values'))
        ax[0].set_xlim([zmin,zmax])
        ax[0].set_ylim([zmin,zmax])       
        ax[0].plot([zmin,zmax],[zmin,zmax])
        ax[0].axis('equal')

        sc1 = ax[1].scatter(xy_cloud[:,0],xy_cloud[:,1],s=10,c=diffz,cmap = cmap, vmin=mindiff, vmax=maxdiff)
        fig.colorbar(sc1)
        ax[1].axis('equal')
        
        plt.show()
    
    def interpolate_on_cloud(self, xy, z, method='linear'):
        '''
        See : https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.griddata.html

            method == nearest, linear or cubic

        '''

        if self.mngselection.myselection == [] or self.mngselection.myselection == 'all':

            decalx = self.origx + self.translx
            decaly = self.origy + self.transly
            x = np.arange(self.dx / 2. + decalx, float(self.nbx) * self.dx + self.dx / 2 + decalx, self.dx)
            y = np.arange(self.dy / 2. + decaly, float(self.nby) * self.dy + self.dy / 2 + decaly, self.dy)
            grid_x, grid_y = np.meshgrid(x, y, sparse=True, indexing='xy')

            newvalues = griddata(xy, z, (grid_x, grid_y), method=method, fill_value=-99999.).transpose()
            self.array.data[np.where(newvalues != -99999.)] = newvalues[np.where(newvalues != -99999.)]

        else:
            ij = np.asarray([self.get_ij_from_xy(x, y) for x, y in self.mngselection.myselection])
            newvalues = griddata(xy, z, self.mngselection.myselection, method=method, fill_value=-99999.)

            ij = ij[np.where(newvalues != -99999.)]
            newvalues = newvalues[np.where(newvalues != -99999.)]
            self.array.data[ij[:, 0], ij[:, 1]] = newvalues

        self.reset_plot()

    def interpolate_on_triangulation(self, coords, triangles, grid_x=None, grid_y = None):
        import matplotlib.tri as mtri
        '''
        See : https://matplotlib.org/stable/gallery/images_contours_and_fields/triinterp_demo.html

            method == linear

        '''
        
        if (self.mngselection is not None) and (grid_x is not None and grid_y is not None):
            if self.mngselection.myselection != [] and self.mngselection.myselection != 'all':
                ij = np.asarray([self.get_ij_from_xy(x, y) for x, y in self.mngselection.myselection])
                
                # Opérateur d'interpolation linéaire
                triang = mtri.Triangulation(coords[:,0],coords[:,1],triangles)
                interplin = mtri.LinearTriInterpolator(triang, coords[:,2])            # Interpolation et récupération dans le numpy.array de l'objet Wolf
                newvalues = np.ma.masked_array([interplin(x, y) for x, y in self.mngselection.myselection])

                ij = ij[np.where(~newvalues.mask)]
                # newvalues = newvalues.data[np.where(~newvalues.mask)]
                self.array.data[ij[:, 0], ij[:, 1]] = newvalues.data[np.where(~newvalues.mask)]

                self.reset_plot()
                return

        if grid_x is None and grid_y is None:           
            decalx = self.origx + self.translx
            decaly = self.origy + self.transly
            x = np.arange(self.dx / 2. + decalx, float(self.nbx) * self.dx + self.dx / 2 + decalx, self.dx)
            y = np.arange(self.dy / 2. + decaly, float(self.nby) * self.dy + self.dy / 2 + decaly, self.dy)
            grid_x, grid_y = np.meshgrid(x, y, indexing='ij')
        
        # Opérateur d'interpolation linéaire
        triang = mtri.Triangulation(coords[:,0],coords[:,1],triangles)
        interplin = mtri.LinearTriInterpolator(triang, coords[:,2])
        # Interpolation et récupération dans le numpy.array de l'objet Wolf
        newvalues = interplin(grid_x,grid_y).astype(np.float32)

        self.array.data[~newvalues.mask] = newvalues[~newvalues.mask]
        
        self.reset_plot()

    def import_from_gltf(self, fn='', fnpos='', interp_method = 'matplotlib'):
        
        """
        interp_method == 'matplotlib' or 'griddata'
        """

        if fn == '' or fnpos == '':
            wx.LogMessage(_('Retry !! -- Bad files'))
            return

        if self.parentGUI is not None:
            if self.parentGUI.link_params is None:
                self.parentGUI.link_params = {}

            self.parentGUI.link_params['gltf file'] = fn
            self.parentGUI.link_params['gltf pos'] = fnpos

        mytri = Triangulation()
        mytri.import_from_gltf(fn)
        
        with open(fnpos, 'r') as f:
            mylines = f.read().splitlines()

            ox = float(mylines[0])
            oy = float(mylines[1])

            nbx = int(mylines[2])
            nby = int(mylines[3])

            i1 = int(mylines[4])
            j1 = int(mylines[5])
            i2 = int(mylines[6])
            j2 = int(mylines[7])

            xmin = float(mylines[8])
            xmax = float(mylines[9])
            ymin = float(mylines[10])
            ymax = float(mylines[11])

        x = np.arange(self.dx / 2. + ox, float(nbx) * self.dx + self.dx / 2 + ox, self.dx)
        y = np.arange(self.dy / 2. + oy, float(nby) * self.dy + self.dy / 2 + oy, self.dy)

        if interp_method =='matplotlib':
            grid_x, grid_y = np.meshgrid(x, y, indexing='ij')
            self.interpolate_on_triangulation(np.asarray(mytri.pts),mytri.tri, grid_x, grid_y)
        else:            
            grid_x, grid_y = np.meshgrid(x, y, sparse=True, indexing='xy')
            newvalues = griddata(np.asarray(mytri.pts)[:,0:2], np.asarray(mytri.pts)[:,2], (grid_x, grid_y), method='linear')
            locmask = np.logical_and(np.logical_not(self.array.mask[i1:i2, j1:j2]),
                                    np.logical_not(np.isnan(newvalues.transpose())))
            self.array.data[i1:i2, j1:j2][locmask] = newvalues.transpose()[locmask]

        self.reset_plot()

    def export_to_gltf(self, bounds=None, fn=''):

        mytri = self.get_triangulation(bounds)
        mytri.export_to_gltf(fn)


        if bounds is None:
            ox = self.origx + self.translx
            oy = self.origy + self.transly
            nbx = self.nbx
            nby = self.nby
            i1 = 0
            i2 = self.nbx
            j1 = 0
            j2 = self.nby
            bounds = [[ox,ox+float(nbx)*self.dx],[oy,oy+float(nby)*self.dy]]

        else:
            ox = max(self.origx, bounds[0][0])
            oy = max(self.origy, bounds[1][0])

            i1, j1 = self.get_ij_from_xy(ox, oy)
            i2, j2 = self.get_ij_from_xy(bounds[0][1], bounds[1][1])

            i1 = max(i1, 0)
            j1 = max(j1, 0)
            i2 = min(i2 + 1, self.nbx)
            j2 = min(j2 + 1, self.nby)

            nbx = i2 - i1
            nby = j2 - j1

        with open(fn + '.pos', 'w') as f:
            f.write(str(ox) + '\n')
            f.write(str(oy) + '\n')
            f.write(str(nbx) + '\n')
            f.write(str(nby) + '\n')
            f.write(str(i1) + '\n')
            f.write(str(j1) + '\n')
            f.write(str(i2) + '\n')
            f.write(str(j2) + '\n')
            f.write(str(bounds[0][0]) + '\n')
            f.write(str(bounds[0][1]) + '\n')
            f.write(str(bounds[1][0]) + '\n')
            f.write(str(bounds[1][1]))
            
    def get_triangulation(self, bounds=None):

        if bounds is None:
            ox = self.origx + self.translx
            oy = self.origy + self.transly
            nbx = self.nbx
            nby = self.nby
            i1 = 0
            i2 = self.nbx
            j1 = 0
            j2 = self.nby
            
            bounds = [[ox,ox+float(nbx)*self.dx],[oy,oy+float(nby)*self.dy]]

        else:
            ox = max(self.origx, bounds[0][0])
            oy = max(self.origy, bounds[1][0])

            i1, j1 = self.get_ij_from_xy(ox, oy)
            i2, j2 = self.get_ij_from_xy(bounds[0][1], bounds[1][1])

            i1 = max(i1, 0)
            j1 = max(j1, 0)
            i2 = min(i2 + 1, self.nbx)
            j2 = min(j2 + 1, self.nby)

            nbx = i2 - i1
            nby = j2 - j1

        refx = ox
        refy = oy

        x = np.arange(self.dx / 2. + refx, float(nbx) * self.dx + self.dx / 2 + refx, self.dx)
        y = np.arange(self.dy / 2. + refy, float(nby) * self.dy + self.dy / 2 + refy, self.dy)

        zmin = np.min(self.array[i1:i2, j1:j2])

        points = np.asarray(
            [[xx, yy, self.get_value(xx + ox - refx, yy + oy - refy, nullvalue=zmin)] for xx in x for yy in y],
            dtype=np.float32)

        decal = 0
        triangles = []
        triangles.append([[i + decal, i + decal + 1, i + decal + nby] for i in range(nby - 1)])
        triangles.append([[i + decal + nby, i + decal + 1, i + decal + nby + 1] for i in range(nby - 1)])

        for k in range(1, nbx - 1):
            decal = k * nby
            triangles.append([[i + decal, i + decal + 1, i + decal + nby] for i in range(nby - 1)])
            triangles.append([[i + decal + nby, i + decal + 1, i + decal + nby + 1] for i in range(nby - 1)])
        triangles = np.asarray(triangles, dtype=np.uint32).reshape([(2 * nby - 2) * (nbx - 1), 3])

        mytri = Triangulation(pts = points, tri = triangles)        
        return mytri

    def hillshade(self, azimuth, angle_altitude):
        azimuth = 360.0 - azimuth

        x, y = np.gradient(self.array)
        slope = np.pi / 2. - np.arctan(np.sqrt(x * x + y * y))
        aspect = np.arctan2(-x, y)
        azimuthrad = azimuth * np.pi / 180.
        altituderad = angle_altitude * np.pi / 180.

        shaded = np.sin(altituderad) * np.sin(slope) + np.cos(altituderad) * np.cos(slope) * np.cos(
            (azimuthrad - np.pi / 2.) - aspect)
        shaded += 1.
        shaded *= .5

        self.shaded.set_header(self.get_header())
        self.shaded.array = shaded
        self.shading = False
        self.shaded.delete_lists()

    def get_gradient_norm(self):

        mygradient = WolfArray(mold=self)

        x, y = np.gradient(self.array, self.dx, self.dy)
        mygradient.array = ma.asarray(np.pi / 2. - np.arctan(np.sqrt(x * x + y * y)))
        mygradient.array.mask = self.array.mask

        return mygradient

    def get_laplace(self):
        mylap = WolfArray(mold=self)
        mylap.array = ma.asarray(laplace(self.array) / self.dx ** 2.)
        mylap.array.mask = self.array.mask

        return mylap

    def volume_estimation(self, axs=None):

        vect = self.array[np.logical_not(self.array.mask)].flatten()
        zmin = np.amin(vect)
        zmax = np.amax(vect)

        dlg = wx.TextEntryDialog(None, _("Desired Z max ?\n Current Z min :") + str(zmin), _("Z max?"), str(zmax))
        ret = dlg.ShowModal()

        if ret == wx.ID_CANCEL:
            dlg.Destroy()
            return

        zmax = float(dlg.GetValue())
        dlg.Destroy()

        dlg = wx.NumberEntryDialog(None, _("How many values?"), _("How many?"), _("How many ?"), 10, 0, 200)
        ret = dlg.ShowModal()

        if ret == wx.ID_CANCEL:
            dlg.Destroy()
            return

        nb = dlg.GetValue()
        dlg.Destroy()

        deltaz = (zmax - zmin) / nb
        curz = zmin
        nbgroupement = []
        longueur = []
        stockage = []
        z = []

        dlg = wx.MessageDialog(None, _("Would you like to calculate relationships on the basis of the largest area ? \n if Yes, no guarantee on the volume increase"), style = wx.YES_NO|wx.YES_DEFAULT)
        ret = dlg.ShowModal()
        if ret == wx.ID_YES:
            labeled= True
        dlg.Destroy()

        extensionmax = WolfArray(mold=self)
        extensionmax.array[:, :] = 0.

        if labeled:
            for i in range(nb + 1):
                wx.LogMessage(_('  Step ') +str(i))
                z.append(curz)

                if i == 0:
                    diff = self.array - (curz + 1.e-3)
                else:
                    diff = self.array - curz

                diff[diff > 0] = 0.
                diff.data[diff.mask] = 0.
                labeled_array, num_features = label(diff.data)
                labeled_array = ma.asarray(labeled_array)
                labeled_array.mask = self.array.mask
                groupement = labeled_array
                groupement[labeled_array.mask] = 0
                nbgroupement.append(num_features)
                for j in range(1, nbgroupement[i] + 1):
                    taille = (np.sum(groupement[groupement == j]) // j)
                    longueur.append([taille, j])
                longueur.sort(key=lambda x: x[0], reverse=True)

                jmax = longueur[0][1]
                nbmax = longueur[0][0]
                volume = -self.dx * self.dy * np.sum(diff[labeled_array == jmax])
                surface = self.dx * self.dy * nbmax
                stockage.append([volume, surface])
                curz += deltaz

                extensionmax.array[np.logical_and(labeled_array == jmax, extensionmax.array[:, :] == 0.)] = float(i + 1)
        else:
            for i in range(nb + 1):
                wx.LogMessage(_('  Step ') +str(i))
                z.append(curz)

                if i == 0:
                    diff = self.array - (curz + 1.e-3)
                else:
                    diff = self.array - curz

                diff[diff > 0] = 0.
                diff.data[diff.mask] = 0.
                volume = -self.dx * self.dy * np.sum(diff)
                surface = self.dx * self.dy * np.count_nonzero(diff<0.)
                stockage.append([volume, surface])
                curz += deltaz

                extensionmax.array[np.logical_and(diff[:,:]<0., extensionmax.array[:, :] == 0.)] = float(i + 1)
            
        dlg = wx.FileDialog(None, _('Choose filename'), wildcard='bin (*.bin)|*.bin|All (*.*)|*.*', style=wx.FD_SAVE)
        ret = dlg.ShowModal()
        if ret == wx.ID_CANCEL:
            dlg.Destroy()
            return

        fn = dlg.GetPath()
        dlg.Destroy()

        extensionmax.filename = fn
        extensionmax.write_all()

        if axs is None:
            fig, axs = plt.subplots(1, 2, tight_layout=True)
        axs[0].plot(z, [x[0] for x in stockage])
        axs[0].scatter(z, [x[0] for x in stockage])
        axs[0].set_xlabel(_("Elevation [m]"), size=15)
        axs[0].set_ylabel(_("Volume [m^3]"), size=15)
        axs[1].step(z, [x[1] for x in stockage], where='post')
        axs[1].scatter(z, [x[1] for x in stockage])
        axs[1].set_xlabel(_("Elevation [m]"), size=15)
        axs[1].set_ylabel(_("Surface [m^2]"), size=15)
        plt.suptitle(_("Retention capacity of the selected zone"), fontsize=20)

        with open(fn[:-4] + '_hvs.txt', 'w') as f:
            f.write('H [m]\tZ [m DNG]\tVolume [m^3]\tSurface [m^2]\n')
            for curz, (curv, curs) in zip(z, stockage):
                f.write('{}\t{}\t{}\t{}\n'.format(curz - zmin, curz, curv, curs))

        return axs

    def paste_all(self, fromarray):
        fromarray: WolfArray

        i1, j1 = self.get_ij_from_xy(fromarray.origx, fromarray.origy)
        i2, j2 = self.get_ij_from_xy(fromarray.origx + fromarray.nbx * fromarray.dx,
                                     fromarray.origy + fromarray.nby * fromarray.dy)

        i1 = max(0, i1)
        j1 = max(0, j1)
        i2 = min(self.nbx, i2)
        j2 = min(self.nby, j2)

        x1, y1 = self.get_xy_from_ij(i1, j1)
        x2, y2 = self.get_xy_from_ij(i2, j2)

        i3, j3 = self.get_ij_from_xy(x1, y1)
        i4, j4 = self.get_ij_from_xy(x2, y2)

        usefulij = np.where(np.logical_not(fromarray.array.mask[i3:i4, j3:j4]))
        usefulij[0][:] += i1
        usefulij[1][:] += j1
        self.array.data[usefulij] = fromarray.array.data[usefulij]

        self.mask_data(self.nullvalue)
        self.reset_plot()

    def set_values_sel(self, xy, z,update=True):

        sel = np.asarray(xy)

        if len(sel) == 1:
            ijall = np.asarray(self.get_ij_from_xy(sel[0, 0], sel[0, 1])).transpose()
            i = ijall[0]
            j = ijall[1]

            if i > 0 and i < self.nbx and j > 0 and j < self.nby:
                self.array[i, j] = z
        else:
            ijall = np.asarray(self.get_ij_from_xy(sel[:, 0], sel[:, 1])).transpose()

            useful = np.where(
                (ijall[:, 0] >= 0) & (ijall[:, 0] < self.nbx) & (ijall[:, 1] >= 0) & (ijall[:, 1] < self.nby))

            self.array[ijall[useful, 0], ijall[useful, 1]] = z[useful]

        self.mask_data(self.nullvalue)
        
        if update:
            self.reset_plot()

    def init_from_new(self, dlg: NewArray):
        self.dx = float(dlg.dx.Value)
        self.dy = float(dlg.dy.Value)
        self.nbx = int(dlg.nbx.Value)
        self.nby = int(dlg.nby.Value)
        self.origx = float(dlg.ox.Value)
        self.origy = float(dlg.oy.Value)

        self.array = ma.MaskedArray(np.ones((self.nbx, self.nby), order='F', dtype=np.float32))
        self.mask_reset()

    def init_from_header(self, myhead: header_wolf):
        self.dx = myhead.dx
        self.dy = myhead.dy
        self.nbx = myhead.nbx
        self.nby = myhead.nby
        self.origx = myhead.origx
        self.origy = myhead.origy
        self.translx = myhead.translx
        self.transly = myhead.transly

        self.array = ma.MaskedArray(np.ones((self.nbx, self.nby), order='F', dtype=np.float32))
        self.mask_reset()

    def interpolation2D(self):

        if '1' in self.mngselection.selections.keys():
            curlist = self.mngselection.selections['1']['select']
            cursel = self.mngselection.myselection
            if len(curlist) > 0:
                ij = [self.get_ij_from_xy(cur[0], cur[1]) for cur in curlist]
                z = [self.array.data[curij[0], curij[1]] for curij in ij]

                if cursel == 'all':
                    xall = np.linspace(self.origx + self.dx / 2., self.origx + (float(self.nbx) - .5) * self.dx,
                                       self.nbx)
                    yall = np.linspace(self.origy + self.dy / 2., self.origy + (float(self.nby) - .5) * self.dy,
                                       self.nby)
                    cursel = [(x, y) for x in xall for y in yall]

                z = griddata(curlist, z, cursel, fill_value=np.NaN)

                for cur, curz in zip(cursel, z):
                    if not np.isnan(curz):
                        i, j = self.get_ij_from_xy(cur[0], cur[1])
                        self.array.data[i, j] = curz

                self.reset_plot()

    def copy_mask(self, source, forcenullvalue= False):

        if forcenullvalue:
            self.array[np.where(source.array.mask)] = self.nullvalue

        self.array.mask = source.array.mask
        self.nbnotnull = source.nbnotnull

        if self.plotted:
            self.reset_plot()

    def copy_mask_log(self,mask):
        self.array.mask = mask
        self.nbnotnull = self.array.count()

        if self.plotted:
            self.reset_plot()

    def check_plot(self):
        self.plotted = True

        if not self.loaded and self.filename != '':
            self.read_data()
            if self.masknull:
                self.mask_data(0.)

        self.loaded = True

        if self.rgb is None:
            self.updatepalette(0)

    def uncheck_plot(self, unload=True, forceresetOGL=False):
        self.plotted = False

        if unload and self.filename != '':
            dlg = wx.MessageDialog(None,
                                   _('Do you want to unload data? \n If YES, the data will be reloaded from file once checekd \n If not saved, modifications will be lost !!'),
                                   style=wx.YES_NO)
            ret = dlg.ShowModal()
            if ret == wx.ID_YES:
                self.delete_lists()
                self.array = np.zeros([1])
                self.rgb = None
                self.loaded = False
                return

        if not forceresetOGL:
            dlg = wx.MessageDialog(None, _('Do you want to reset OpenGL lists?'), style=wx.YES_NO)
            ret = dlg.ShowModal()
            if ret == wx.ID_YES:
                self.delete_lists()
                self.rgb = None
        else:
            self.delete_lists()
            self.rgb = None

    def get_header(self, abs=True) -> header_wolf():
        curhead = header_wolf()

        curhead.origx = self.origx
        curhead.origy = self.origy
        curhead.origz = self.origz

        curhead.dx = self.dx
        curhead.dy = self.dy
        curhead.dz = self.dz

        curhead.nbx = self.nbx
        curhead.nby = self.nby
        curhead.nbz = self.nbz

        curhead.translx = self.translx
        curhead.transly = self.transly
        curhead.translz = self.translz

        curhead.nb_blocks = self.nb_blocks

        if abs:
            curhead.origx += curhead.translx
            curhead.origy += curhead.transly
            curhead.origz += curhead.translz

            curhead.translx = 0.
            curhead.transly = 0.
            curhead.translz = 0.
        return curhead

    def set_header(self, header: header_wolf):
        self.origx = header.origx
        self.origy = header.origy
        self.origz = header.origz

        self.translx = header.translx
        self.transly = header.transly
        self.translz = header.translz

        self.dx = header.dx
        self.dy = header.dy
        self.dz = header.dz

        self.nbx = header.nbx
        self.nby = header.nby
        self.nbz = header.nbz

        self.nb_blocks = header.nb_blocks
        self.head_blocks = header.head_blocks.copy()
        
        self.add_ops_sel()

    def __add__(self, other):
        """Surcharge de l'opérateur d'addition"""
        newArray = WolfArray()
        newArray.nbdims = self.nbdims
        newArray.nbx = self.nbx
        newArray.nby = self.nby
        newArray.dx = self.dx
        newArray.dy = self.dy
        newArray.origx = self.origx
        newArray.origy = self.origy
        newArray.translx = self.translx
        newArray.transly = self.transly

        if self.nbdims == 3:
            newArray.nbz = self.nbz
            newArray.dz = self.dz
            newArray.origz = self.origz
            newArray.translz = self.translz

        if type(other) == float:
            if other != 0.:
                newArray.array = np.ma.masked_array(self.array + other, self.array.mask)
        else:
            newArray.array = np.ma.masked_array(self.array + other.array, self.array.mask)
        return newArray

    def __mul__(self, other):
        """Surcharge de l'opérateur d'addition"""
        newArray = WolfArray()
        newArray.nbdims = self.nbdims
        newArray.nbx = self.nbx
        newArray.nby = self.nby
        newArray.dx = self.dx
        newArray.dy = self.dy
        newArray.origx = self.origx
        newArray.origy = self.origy
        newArray.translx = self.translx
        newArray.transly = self.transly

        if self.nbdims == 3:
            newArray.nbz = self.nbz
            newArray.dz = self.dz
            newArray.origz = self.origz
            newArray.translz = self.translz

        if type(other) == float:
            if other != 0.:
                newArray.array = np.ma.masked_array(self.array * other, self.array.mask)
        else:
            newArray.array = np.ma.masked_array(self.array * other.array, self.array.mask)
        return newArray

    def __sub__(self, other):
        """Surcharge de l'opérateur de soustraction"""
        newArray = WolfArray()
        newArray.nbdims = self.nbdims
        newArray.nbx = self.nbx
        newArray.nby = self.nby
        newArray.dx = self.dx
        newArray.dy = self.dy
        newArray.origx = self.origx
        newArray.origy = self.origy
        newArray.translx = self.translx
        newArray.transly = self.transly

        if self.nbdims == 3:
            newArray.nbz = self.nbz
            newArray.dz = self.dz
            newArray.origz = self.origz
            newArray.translz = self.translz

        if type(other) == float:
            if other != 0.:
                newArray.array = np.ma.masked_array(self.array - other, self.array.mask)
        else:
            newArray.array = np.ma.masked_array(self.array - other.array, self.array.mask)
        return newArray

    def __pow__(self, other):
        """Surcharge de l'opérateur puissance"""
        newArray = WolfArray()
        newArray.nbdims = self.nbdims
        newArray.nbx = self.nbx
        newArray.nby = self.nby
        newArray.dx = self.dx
        newArray.dy = self.dy
        newArray.origx = self.origx
        newArray.origy = self.origy
        newArray.translx = self.translx
        newArray.transly = self.transly

        if self.nbdims == 3:
            newArray.nbz = self.nbz
            newArray.dz = self.dz
            newArray.origz = self.origz
            newArray.translz = self.translz

        newArray.array = np.ma.masked_array(self.array ** other, self.array.mask)
        return newArray

    def __truediv__(self, other):
        """Surcharge de l'opérateur puissance"""
        newArray = WolfArray()
        newArray.nbdims = self.nbdims
        newArray.nbx = self.nbx
        newArray.nby = self.nby
        newArray.dx = self.dx
        newArray.dy = self.dy
        newArray.origx = self.origx
        newArray.origy = self.origy
        newArray.translx = self.translx
        newArray.transly = self.transly

        if self.nbdims == 3:
            newArray.nbz = self.nbz
            newArray.dz = self.dz
            newArray.origz = self.origz
            newArray.translz = self.translz

        if type(other) == float:
            if other != 0.:
                newArray.array = np.ma.masked_array(self.array / other, self.array.mask)
        else:
            newArray.array = np.ma.masked_array(np.where(other == 0., 0., self.array / other.array), self.array.mask)

        return newArray

    def mask_outsidepoly(self, myvect: vector):

        mask = self.array.mask
        mask[:,:] = True
        
        # trouve les indices dans le polygone
        myij = self.get_ij_inside_polygon(myvect,False)        
        # démasquage des mailles contenues
        mask[myij[:,0],myij[:,1]] = False
        # annulation des valeurs en dehors du polygone
        self.array.data[np.where(mask)] = self.nullvalue
        # recherche du nouveau masque, sinon les valeurs no_data à l'intérieur du polygone vont pollluer la matrice
        self.mask_data(self.nullvalue)

    def get_xy_infootprint_vect(self, myvect: vector) -> np.ndarray:
        
        myptsij = self.get_ij_infootprint_vect(myvect)
        mypts=np.asarray(myptsij.copy(),dtype=np.float64)
        mypts[:,0] = (mypts[:,0]+.5)*self.dx +self.origx +self.translx
        mypts[:,1] = (mypts[:,1]+.5)*self.dy +self.origy +self.transly
        
        return mypts,myptsij

    def get_ij_infootprint_vect(self, myvect: vector) -> np.ndarray:
        i1, j1 = self.get_ij_from_xy(myvect.minx, myvect.miny)
        i2, j2 = self.get_ij_from_xy(myvect.maxx, myvect.maxy) 
        i1 = max(i1,0)       
        j1 = max(j1,0)       
        i2 = min(i2,self.nbx-1)       
        j2 = min(j2,self.nby-1)       
        xv,yv = np.meshgrid(np.arange(i1,i2+1),np.arange(j1,j2+1))
        mypts = np.hstack((xv.flatten()[:,np.newaxis],yv.flatten()[:,np.newaxis]))
        
        return mypts

    def get_xy_inside_polygon(self, myvect: vector, usemask=True):
        '''
        Obtention des coordonnées contenues dans un polygone
         usemask = restreint les éléments aux éléments non masqués de la matrice
        '''

        myvect.find_minmax()
        mypointsxy,mypointsij = self.get_xy_infootprint_vect(myvect)
        myvert = myvect.asnparray()
        path = mpltPath.Path(myvert)
        inside = path.contains_points(mypointsxy)

        mypointsxy = mypointsxy[np.where(inside)]

        if usemask:
            mypointsij = mypointsij[np.where(inside)]
            mymask = np.logical_not(self.array.mask[mypointsij[:, 0], mypointsij[:, 1]])
            mypointsxy = mypointsxy[np.where(mymask)]

        return mypointsxy

    def convert_xy2ij(self,xy):
        return np.asarray((xy[:,0]-self.origx -self.translx)/self.dx-.5,dtype=np.int32), \
               np.asarray((xy[:,1]-self.origy -self.transly)/self.dy-.5,dtype=np.int32)
        
    def convert_ij2xy(self,xy):
        return np.asarray((xy[:,0]+.5)*self.dx+self.origx +self.translx ,dtype=np.float64), \
               np.asarray((xy[:,1]+.5)*self.dy+self.origy +self.transly ,dtype=np.float64)
        

    def get_ij_inside_polygon(self, myvect: vector, usemask=True):
        '''
        Obtention des indices contenues dans un polygone
         usemask = restreint les éléments aux éléments non masqués de la matrice
        '''

        myvect.find_minmax()
        mypointsij = self.get_ij_infootprint_vect(myvect)
        myvert = myvect.asnparray()
        i,j =self.convert_xy2ij(myvert)
        path = mpltPath.Path(np.column_stack([i,j]))
        inside = path.contains_points(mypointsij)

        mypointsij = mypointsij[np.where(inside)]

        if usemask:
            mymask = np.logical_not(self.array.mask[mypointsij[:, 0], mypointsij[:, 1]])
            mypointsij = mypointsij[np.where(mymask)]

        return mypointsij

    def get_values_insidepoly(self, myvect: vector, usemask=True, getxy=False):

        mypoints = self.get_xy_inside_polygon(myvect, usemask)
        myvalues = np.asarray([self.get_value(cur[0], cur[1]) for cur in mypoints])

        if getxy:
            return myvalues, mypoints
        else:
            return myvalues, None

    def get_ij_under_polyline(self, myvect: vector, usemask=True):
        '''
        Obtention des coordonnées sous un polygone
         usemask = restreint les éléments aux éléments non masqués de la matrice
        '''

        myls = myvect.asshapely_ls()
        length = myls.length

        ds = min(self.dx, self.dy)
        nb = int(np.ceil(length / ds * 2))

        alls = np.linspace(0, length, nb, endpoint=True)

        pts = [myls.interpolate(curs) for curs in alls]
        allij = np.asarray([self.get_ij_from_xy(curpt.x, curpt.y) for curpt in pts])

        allij = np.unique(allij, axis=0)

        if usemask:
            mymask = np.logical_not(self.array.mask[allij[:, 0], allij[:, 1]])
            allij = allij[np.where(mymask)]

        return allij

    def reset(self):
        if self.nbdims == 2:
            self.array[:, :] = 0.0
        elif self.nbdims == 3:
            self.array[:, :, :] = 0.0

    def allocate_ressources(self):
        if self.nbdims == 2:
            self.array = ma.ones([self.nbx, self.nby])
        elif self.nbdims == 3:
            self.array = ma.ones([self.nbx, self.nby, self.nbz])

    def read_all(self):
        """ Lecture d'un Wolf aray depuis le nom de fichier """
        if not os.path.exists(self.filename):
            wx.LogWarning(_('No data file : ')+self.filename)
            return
        
        self.read_txt_header()
        if self.preload:
            self.read_data()
            self.loaded = True
        return

    def write_all(self):
        """ Ecriture de tous les fichiers d'un Wolf array """
        self.write_txt_header()
        self.write_array()

    def rebin(self, factor, operation='mean'):
        """ Adaptation de la résolution"""
        operation = operation.lower()
        if not operation in ['sum', 'mean']:
            raise ValueError("Operation not supported.")

        self.nbx = int(self.nbx / factor)
        self.nby = int(self.nby / factor)
        self.dx = self.dx * float(factor)
        self.dy = self.dy * float(factor)
        new_shape = (self.nbx, self.nby)

        compression_pairs = [(d, c // d) for d, c in zip(new_shape,
                                                         self.array.shape)]
        flattened = [l for p in compression_pairs for l in p]
        self.array = self.array.reshape(flattened)
        for i in range(len(new_shape)):
            op = getattr(self.array, operation)
            self.array = np.float32(op(-1 * (i + 1)))

    def read_txt_header(self):
        """ Lecture du header .txt """
        if self.filename.endswith('.flt'):
            # Fichier .flt
            f = open(self.filename[:-4] + '.hdr', 'r')
            lines = f.read().splitlines()
            f.close()

            for curline in lines:
                if 'NCOLS' in curline.upper():
                    tmp = curline.split(' ')
                    self.nbx = int(tmp[-1])
                elif 'NROWS' in curline.upper():
                    tmp = curline.split(' ')
                    self.nby = int(tmp[-1])
                elif 'XLLCORNER' in curline.upper():
                    tmp = curline.split(' ')
                    self.origx = float(tmp[-1])
                elif 'YLLCORNER' in curline.upper():
                    tmp = curline.split(' ')
                    self.origy = float(tmp[-1])
                elif 'ULXMAP' in curline.upper():
                    tmp = curline.split(' ')
                    self.origx = float(tmp[-1])
                    self.flipupd=True
                elif 'ULYMAP' in curline.upper():
                    tmp = curline.split(' ')
                    self.origy = float(tmp[-1])
                    self.flipupd=True
                elif 'CELLSIZE' in curline.upper():
                    tmp = curline.split(' ')
                    self.dx = self.dy = float(tmp[-1])                    
                elif 'XDIM' in curline.upper():
                    tmp = curline.split(' ')
                    self.dx = float(tmp[-1])                    
                elif 'YDIM' in curline.upper():
                    tmp = curline.split(' ')
                    self.dy = float(tmp[-1])                    
                elif 'NODATA' in curline.upper():
                    tmp = curline.split(' ')
                    self.nullvalue = float(tmp[-1])  
                    
            if self.flipupd:
                self.origy -= self.dy*float(self.nby)
                              
        else:
            if not os.path.exists(self.filename + '.txt'):
                wx.LogMessage(_('File {os.path.curdir} does not exist -- Retry!'))
                return

            with open(self.filename + '.txt', 'r') as f:
                lines = f.read().splitlines()

            tmp = lines[0].split(':')
            self.nbx = int(tmp[1])
            tmp = lines[1].split(':')
            self.nby = int(tmp[1])
            tmp = lines[2].split(':')
            self.origx = float(tmp[1])
            tmp = lines[3].split(':')
            self.origy = float(tmp[1])
            tmp = lines[4].split(':')
            self.dx = float(tmp[1])
            tmp = lines[5].split(':')
            self.dy = float(tmp[1])
            tmp = lines[6].split(':')
            self.wolftype = int(tmp[1])
            tmp = lines[7].split(':')
            self.translx = float(tmp[1])
            tmp = lines[8].split(':')
            self.transly = float(tmp[1])

            decal = 9
            if self.wolftype == WOLF_ARRAY_FULL_SINGLE_3D:
                self.nbdims = 3
                tmp = lines[9].split(':')
                self.nbz = int(tmp[1])
                tmp = lines[10].split(':')
                self.origz = float(tmp[1])
                tmp = lines[11].split(':')
                self.dz = float(tmp[1])
                tmp = lines[12].split(':')
                self.translz = float(tmp[1])
                decal = 13

            if self.wolftype in WOLF_ARRAY_MB:
                tmp = lines[decal].split(':')
                self.nb_blocks = int(tmp[1])

                decal += 1
                for i in range(self.nb_blocks):
                    curhead = header_wolf()
                    tmp = lines[decal].split(':')
                    curhead.nbx = int(tmp[1])
                    tmp = lines[decal + 1].split(':')
                    curhead.nby = int(tmp[1])
                    tmp = lines[decal + 2].split(':')
                    curhead.origx = float(tmp[1])
                    tmp = lines[decal + 3].split(':')
                    curhead.origy = float(tmp[1])
                    tmp = lines[decal + 4].split(':')
                    curhead.dx = float(tmp[1])
                    tmp = lines[decal + 5].split(':')
                    curhead.dy = float(tmp[1])
                    decal += 6

                    curhead.translx = self.translx + self.origx
                    curhead.transly = self.transly + self.origy

                    self.head_blocks[getkeyblock(i)] = curhead

    def write_txt_header(self):
        """ Ecriture de l'en-tête de Wolf array """
        f = open(self.filename + '.txt', 'w')
        f.write('NbX :\t{0}\n'.format(str(self.nbx)))
        f.write('NbY :\t{0}\n'.format(str(self.nby)))
        f.write('OrigX :\t{0}\n'.format(str(self.origx)))
        f.write('OrigY :\t{0}\n'.format(str(self.origy)))
        f.write('DX :\t{0}\n'.format(str(self.dx)))
        f.write('DY :\t{0}\n'.format(str(self.dy)))
        f.write('TypeEnregistrement :\t{0}\n'.format(str(self.wolftype)))
        f.write('TranslX :\t{0}\n'.format(str(self.translx)))
        f.write('TranslY :\t{0}\n'.format(str(self.transly)))
        if self.wolftype == WOLF_ARRAY_FULL_SINGLE_3D:
            f.write('NbZ :\t{0}\n'.format(str(self.nbz)))
            f.write('OrigZ :\t{0}\n'.format(str(self.origz)))
            f.write('DZ :\t{0}\n'.format(str(self.dz)))
            f.write('TranslZ :\t{0}\n'.format(str(self.translz)))

        if self.wolftype in WOLF_ARRAY_MB:
            f.write('Nb Blocs :\t{0}\n'.format(str(self.nb_blocks)))
            for i in range(self.nb_blocks):
                curhead = self.head_blocks[getkeyblock(i)]
                f.write('NbX :\t{0}\n'.format(str(curhead.nbx)))
                f.write('NbY :\t{0}\n'.format(str(curhead.nby)))
                f.write('OrigX :\t{0}\n'.format(str(curhead.origx)))
                f.write('OrigY :\t{0}\n'.format(str(curhead.origy)))
                f.write('DX :\t{0}\n'.format(str(curhead.dx)))
                f.write('DY :\t{0}\n'.format(str(curhead.dy)))

        f.close()

    def read_data(self):
        if not os.path.exists(self.filename):
            wx.LogWarning(_('No data file : ')+self.filename)
            return
        
        if self.cropini is None:
            with open(self.filename, 'rb') as f:
                self._read_binary_data(f)
                
        else:
            if type(self.cropini) is np.ndarray:
                pass
            elif type(self.cropini) is list:
                pass
            else:
                newcrop = CropDialog(None)

                badvalues = True
                while badvalues:
                    badvalues = False

                    ret = newcrop.ShowModal()
                    if ret == wx.ID_CANCEL:
                        newcrop.Destroy()
                        return
                    else:
                        self.cropini = [[float(newcrop.ox.Value), float(newcrop.ex.Value)],
                                        [float(newcrop.oy.Value), float(newcrop.ey.Value)]]
                        tmpdx = float(newcrop.dx.Value)
                        tmpdy = float(newcrop.dy.Value)

                    if self.dx != tmpdx or self.dy != tmpdy:
                        if tmpdx / self.dx != tmpdy / self.dy:
                            badvalues = True

                newcrop.Destroy()

            with open(self.filename, 'rb') as f:
                if self.wolftype == 1 or self.wolftype == 7:

                    imin, jmin = self.get_ij_from_xy(self.cropini[0][0], self.cropini[1][0])
                    imax, jmax = self.get_ij_from_xy(self.cropini[0][1], self.cropini[1][1])

                    imin = int(imin)
                    jmin = int(jmin)
                    imax = int(imax)
                    jmax = int(jmax)

                    oldnbx = self.nbx
                    oldnby = self.nby

                    self.nbx = imax - imin
                    self.nby = jmax - jmin
                    self.origx, self.origy = self.get_xy_from_ij(imin, jmin)
                    self.origx -= self.dx / 2.
                    self.origy -= self.dy / 2.

                    locarray = np.zeros([self.nbx, self.nby])

                    # on boucle sur les 'j'
                    nbi = imax - imin
                    if self.filename.endswith('.flt'):
                        f.seek(((oldnby - jmax) * oldnbx + imin) * 4)
                    else:
                        f.seek((imin + jmin * oldnbx) * 4)

                    for j in range(jmin, jmax):
                        locarray[0:imax - imin, j - jmin] = np.frombuffer(f.read(4 * nbi), dtype=np.float32)
                        f.seek((oldnbx - nbi) * 4, 1)

                    self.array = ma.masked_array(locarray, dtype=np.float32)

            if self.filename.endswith('.flt'):
                # fichier .flt --> miroir "horizontal"
                self.array = np.fliplr(self.array)

            if self.dx != tmpdx:
                self.rebin(tmpdx / self.dx)

        self.loaded = True

    def _read_binary_data(self, f, seek=0):

        if seek > 0:
            f.seek(0)

        if self.wolftype == WOLF_ARRAY_FULL_SINGLE or self.wolftype == WOLF_ARRAY_FULL_SINGLE_3D:
            locarray = np.frombuffer(f.read(self.nbx * self.nby * 4), dtype=np.float32)
            self.array = ma.masked_array(locarray.copy(), dtype=np.float32)
        elif self.wolftype == WOLF_ARRAY_FULL_LOGICAL:
            locarray = np.frombuffer(f.read(self.nbx * self.nby * 2), dtype=np.int16)
            self.array = ma.masked_array(locarray.copy(), dtype=np.int16)
        elif self.wolftype == WOLF_ARRAY_FULL_DOUBLE:
            locarray = np.frombuffer(f.read(self.nbx * self.nby * 8), dtype=np.float64)
            self.array = ma.masked_array(locarray.copy(), dtype=np.float64)
        elif self.wolftype == WOLF_ARRAY_FULL_INTEGER:
            locarray = np.frombuffer(f.read(self.nbx * self.nby * 4), dtype=np.int32)
            self.array = ma.masked_array(locarray.copy(), dtype=np.int32)
        elif self.wolftype == WOLF_ARRAY_FULL_INTEGER16:
            locarray = np.frombuffer(f.read(self.nbx * self.nby * 2), dtype=np.int16)
            self.array = ma.masked_array(locarray.copy(), dtype=np.int16)

        if self.nbdims == 2:
            self.array = self.array.reshape(self.nbx, self.nby, order='F')
            if self.flipupd:
                self.array=np.fliplr(self.array)
            
        elif self.nbdims == 3:
            self.array = self.array.reshape(self.nbx, self.nby, self.nbz, order='F')

    def write_array(self):
        """ Ecriture du tableau en binaire """
        self.array.data.transpose().tofile(self.filename, "")

    def write_xyz(self, fname):
        """ Ecriture d un fichier xyz avec toutes les données du Wolf Array """
        my_file = XYZFile(fname)
        my_file.fill_from_wolf_array(self)
        my_file.write_to_file()

    def get_xyz(self, which='all'):
        x1, y1 = self.get_xy_from_ij(0, 0)
        x2, y2 = self.get_xy_from_ij(self.nbx, self.nby, aswolf=True)
        xloc = np.linspace(x1, x2, self.nbx)
        yloc = np.linspace(y1, y2, self.nby)
        xy = np.meshgrid(xloc, yloc, indexing='xy')

        xyz = np.column_stack([xy[0].flatten(), xy[1].flatten(), self.array.flatten()])

        filter = np.invert(ma.getmaskarray(self.array).flatten())

        return xyz[filter]

    def set_general_frame_from_xyz(self, fname, dx, dy):
        """ Lecture d'un fichier xyz et initialisation des données de base """
        my_file = XYZFile(fname)
        my_file.read_from_file()
        (xlim, ylim) = my_file.get_extent()

        self.dx = dx
        self.dy = dy
        self.origx = m.floor(xlim[0]) - 5.0 * self.dx
        self.origy = m.floor(ylim[0]) - 5.0 * self.dy
        self.nbx = int((m.floor(xlim[1]) - m.ceil(xlim[0])) / self.dx) + 10
        self.nby = int((m.floor(ylim[1]) - m.ceil(ylim[0])) / self.dy) + 10

        self.array = np.ma.zeros((self.nbx, self.nby))
        return my_file

    def fillin_from_xyz(self, xyz):

        self.array.data[self.get_ij_from_xy(xyz[:, 0], xyz[:, 1])] = np.float32(xyz[:, 2])

    def mask_reset(self):
        if self.nbdims == 2:
            self.array.mask = np.zeros((self.nbx, self.nby))
            self.nbnotnull = self.nbx * self.nby
        elif self.nbdims == 3:
            self.array.mask = np.zeros((self.nbx, self.nby, self.nbz))
            self.nbnotnull = self.nbx * self.nby * self.nbz

    def mask_data(self, value):
        self.array.mask = self.array.data == value
        self.nbnotnull = self.array.count()

    def mask_lower(self, value):
        self.array.mask = self.array.data < value
        self.nbnotnull = self.array.count()

    def mask_lowerequal(self, value):
        self.array.mask = self.array.data <= value
        self.nbnotnull = self.array.count()
                
    def reset_plot(self,whichpal=0):
        self.delete_lists()
        self.nbnotnull = self.array.count()
        self.updatepalette(whichpal)

    def mask_allexceptdata(self, value):
        self.array.mask = self.array.data != value
        self.nbnotnull = self.array.count()

    def mask_invert(self):
        self.array.mask = np.logical_not(self.array.mask)
        self.nbnotnull = self.array.count()

    def meshgrid(self, mode='gc'):
        x_start = self.translx + self.origx
        y_start = self.transly + self.origy
        if mode == 'gc':
            x_discr = np.linspace(x_start + self.dx / 2, x_start + self.nbx * self.dx - self.dx / 2, self.nbx)
            y_discr = np.linspace(y_start + self.dy / 2, y_start + self.nby * self.dy - self.dy / 2, self.nby)
        elif mode == 'borders':
            x_discr = np.linspace(x_start, x_start + self.nbx * self.dx, self.nbx + 1)
            y_discr = np.linspace(y_start, y_start + self.nby * self.dy, self.nby + 1)

        y, x = np.meshgrid(y_discr, x_discr)
        return x, y

    def crop(self, i_start, j_start, nbx, nby, k_start=1, nbz=1):
        newWolfArray = WolfArray()
        newWolfArray.nbx = nbx
        newWolfArray.nby = nby
        newWolfArray.dx = self.dx
        newWolfArray.dy = self.dy
        newWolfArray.origx = self.origx + i_start * self.dx
        newWolfArray.origy = self.origy + j_start * self.dy
        newWolfArray.translx = self.translx
        newWolfArray.transly = self.transly

        if self.nbdims == 3:
            newWolfArray.nbz = nbz
            newWolfArray.dz = self.dz
            newWolfArray.origz = self.origz + k_start * self.dz
            newWolfArray.translz = self.translz

            newWolfArray.array = self.array[i_start:i_start + nbx, j_start:j_start + nby, k_start:k_start + nbz]
        elif self.nbdims == 2:
            newWolfArray.array = self.array[i_start:i_start + nbx, j_start:j_start + nby]

        return newWolfArray

    def extremum(self, which='min'):
        if which == 'min':
            my_extr = np.amin(self.array)
        else:
            my_extr = np.amax(self.array)

        return my_extr

    def get_bounds(self, abs=True):
        if abs:
            return ([self.origx + self.translx, self.origx + self.translx + float(self.nbx) * self.dx],
                    [self.origy + self.transly, self.origy + self.transly + float(self.nby) * self.dy])
        else:
            return ([self.origx, self.origx + float(self.nbx) * self.dx],
                    [self.origy, self.origy + float(self.nby) * self.dy])

    def find_intersection(self, other, ij=False):

        mybounds = self.get_bounds()
        otherbounds = other.get_bounds()

        if otherbounds[0][0] > mybounds[0][1]:
            return None
        elif otherbounds[1][0] > mybounds[1][1]:
            return None
        elif otherbounds[0][1] < mybounds[0][0]:
            return None
        elif otherbounds[1][1] < mybounds[0][1]:
            return None
        else:
            ox = max(mybounds[0][0], otherbounds[0][0])
            oy = max(mybounds[1][0], otherbounds[1][0])
            ex = min(mybounds[0][1], otherbounds[0][1])
            ey = min(mybounds[1][1], otherbounds[1][1])
            if ij:
                i1, j1 = self.get_ij_from_xy(ox, oy)
                i2, j2 = self.get_ij_from_xy(ex, ey)

                i3, j3 = other.get_ij_from_xy(ox, oy)
                i4, j4 = other.get_ij_from_xy(ex, ey)
                return ([[i1, i2], [j1, j2]],
                        [[i3, i4], [j3, j4]])
            else:
                return ([ox, ex], [oy, ey])

    def find_union(self, other):

        mybounds = self.get_bounds()
        otherbounds = other.get_bounds()

        ox = min(mybounds[0][0], otherbounds[0][0])
        oy = min(mybounds[1][0], otherbounds[1][0])
        ex = max(mybounds[0][1], otherbounds[0][1])
        ey = max(mybounds[1][1], otherbounds[1][1])

        return ([ox, ex], [oy, ey])

    def get_ij_from_xy(self, x, y, z=0., scale=1., aswolf=False, abs=True):

        locx = np.float64(x) - self.origx
        locy = np.float64(y) - self.origy
        locz = np.float64(z) - self.origz
        if abs:
            locx = locx - self.translx
            locy = locy - self.transly
            locz = locz - self.translz

        i = np.int32(locx / (self.dx * scale))
        j = np.int32(locy / (self.dy * scale))

        if aswolf:
            i += 1
            j += 1

        if self.nbdims == 3:
            k = np.int32(locz / (self.dz * scale))
            if aswolf:
                k += 1
            return i, j, k  # ATTENTION, Indices en numérotation Python --> WOLF ajouter +1
        elif self.nbdims == 2:
            return i, j  # ATTENTION, Indices en numérotation Python --> WOLF ajouter +1

    def get_xy_from_ij(self, i, j, k=0, scale=1., aswolf=False, abs=True):

        i = np.int32(i)
        j = np.int32(j)

        if aswolf:
            i += -1
            j += -1

        if abs:
            x = (np.float64(i) + .5) * (self.dx * scale) + self.origx + self.translx
            y = (np.float64(j) + .5) * (self.dy * scale) + self.origy + self.transly
        else:
            x = (np.float64(i) + .5) * (self.dx * scale) + self.origx
            y = (np.float64(j) + .5) * (self.dy * scale) + self.origy

        if self.nbdims == 3:
            k = np.int32(k)
            if aswolf:
                k += -1

            if abs:
                z = (np.float64(k) - .5) * (self.dz * scale) + self.origz + self.translz
            else:
                z = (np.float64(k) - .5) * (self.dz * scale) + self.origz

            return x, y, z

        elif self.nbdims == 2:
            return x, y

    def get_xy_from_ij_array(self, ij:np.ndarray):

        xy = np.zeros(ij.shape)
        xy[:,0] = (np.float64(ij[:,0]) + .5) * self.dx + self.origx + self.translx
        xy[:,1] = (np.float64(ij[:,1]) + .5) * self.dy + self.origy + self.transly

        return xy

    def get_value(self, x, y, z=0., nullvalue=-99999):

        if self.nbdims == 2:
            i, j = self.get_ij_from_xy(x, y)
            if i >= 0 and i < self.nbx and j >= 0 and j < self.nby:
                if self.array.mask[i, j]:
                    value = nullvalue
                else:
                    value = self.array[i, j]
            else:
                value = nullvalue
        elif self.nbdims == 3:
            i, j, k = self.get_ij_from_xy(x, y, z)
            if i >= 0 and i < self.nbx and j >= 0 and j < self.nby and k >= 0 and k < self.nbz:

                if self.array.mask[i, j, k]:
                    value = nullvalue
                else:
                    value = self.array[i, j, k]
            else:
                value = nullvalue

        return float(value)

    def get_xlim(self, window_x, window_y):
        a_x = window_x / (self.nbx * self.dx)
        a_y = window_y / (self.nby * self.dy)
        if a_x < a_y:
            # C'est la mise à l'échelle selon x qui compte
            return (self.origx + self.translx, self.origx + self.translx + self.nbx * self.dx)
        else:
            # C'est la mise à l'échelle selon y qui compte
            l = (self.nby * self.dy) / window_y * window_x
            return (self.origx + self.translx + self.nbx * self.dx * 0.5 - l * 0.5,
                    self.origx + self.translx + self.nbx * self.dx * 0.5 + l * 0.5)

    def get_ylim(self, window_x, window_y):
        a_x = window_x / (self.nbx * self.dx)
        a_y = window_y / (self.nby * self.dy)
        if a_x < a_y:
            # C'est la mise à l'échelle selon x qui compte
            l = (self.nbx * self.dx) / window_x * window_y
            return (self.origy + self.transly + self.nby * self.dy * 0.5 - l * 0.5,
                    self.origy + self.transly + self.nby * self.dy * 0.5 + l * 0.5)
        else:
            # C'est la mise à l'échelle selon y qui compte
            return (self.origy + self.transly, self.origy + self.transly + self.nby * self.dy)

    def get_working_array(self, onzoom=[]):
        if onzoom != []:
            istart, jstart = self.get_ij_from_xy(onzoom[0], onzoom[2])
            iend, jend = self.get_ij_from_xy(onzoom[1], onzoom[3])

            istart = 0 if istart < 0 else istart
            jstart = 0 if jstart < 0 else jstart
            iend = self.nbx if iend > self.nbx else iend
            jend = self.nby if jend > self.nby else jend

            partarray = self.array[istart:iend, jstart:jend]
            self.nbnotnullzoom = partarray.count()
            return partarray[partarray.mask == False]
        else:
            return self.array[self.array.mask == False]

    def updatepalette(self, which=0, onzoom=[]):

        if self.array is None:
            return

        if self.mypal.automatic:
            if onzoom != []:
                self.mypal.isopop(self.get_working_array(onzoom), self.nbnotnullzoom)
            else:
                self.mypal.isopop(self.get_working_array(), self.nbnotnull)

        self.rgb = self.mypal.get_rgba(self.array)
        self.rgb[self.array.mask] = [1., 1., 1., 1.]

        if self.myops is not None:
            self.myops.update_palette()

    def plot(self, sx=None, sy=None, xmin=None, ymin=None, xmax=None, ymax=None):

        if not self.plotted:
            return

        self.plotting = True

        if self.plotted and sx is None:
            sx = self.sx
            sy = self.sy
            xmin = self.xmin
            xmax = self.xmax
            ymin = self.ymin
            ymax = self.ymax
        else:
            self.sx = sx
            self.sy = sy
            self.xmin = xmin
            self.xmax = xmax
            self.ymin = ymin
            self.ymax = ymax

        nbpix = min(sx * self.dx, sy * self.dy)
        if nbpix >= 1.:
            # si une maille est tracée sur au moins 2 pixels
            curscale = 1
        elif math.ceil(1. / nbpix) <= 3:
            curscale = math.ceil(math.ceil(1. / nbpix))
        else:
            curscale = math.ceil(math.ceil(1. / nbpix) / 3) * 3

        curscale = max(curscale, 1)
        cursize = curscale  # 2.**curscale
        curnbx = max(math.ceil(float(self.nbx) / (self.gridsize * cursize)), 1)
        curnby = max(math.ceil(float(self.nby) / (self.gridsize * cursize)), 1)

        if not cursize in self.mygrid.keys():
            self.mygrid[cursize] = {}
            curlist = self.mygrid[cursize]
            curlist['nbx'] = curnbx
            curlist['nby'] = curnby
            numlist = glGenLists(curnbx * curnby)
            curlist['firstlist'] = numlist
            wx.LogMessage(_('OpenGL lists - allocation') + ' - ' +_('first list')+str(numlist) )
            curlist['mylists'] = np.linspace(numlist, numlist + curnbx * curnby - 1, num=curnbx * curnby,
                                             dtype=np.integer).reshape((curnbx, curnby), order='F')
            curlist['done'] = np.zeros((curnbx, curnby), dtype=np.integer, order='F')

        if (curnbx == 1 and curnby == 1):
            if (self.gridmaxscales == -1):
                self.gridmaxscales = curscale
            elif curscale > self.gridmaxscales:
                curscale = self.gridmaxscales
                cursize = curscale
                curnbx = max(math.ceil(float(self.nbx) / (self.gridsize * cursize)), 1)
                curnby = max(math.ceil(float(self.nby) / (self.gridsize * cursize)), 1)

        istart, jstart = self.get_ij_from_xy(xmin, ymin, scale=cursize * float(self.gridsize))
        iend, jend = self.get_ij_from_xy(xmax, ymax, scale=cursize * float(self.gridsize))

        istart = max(0, istart)
        jstart = max(0, jstart)
        iend = min(curnbx - 1, iend)
        jend = min(curnby - 1, jend)

        if self.wolftype != WOLF_ARRAY_HILLSHAPE and self.shading:
            self.hillshade(self.azimuthhill, self.altitudehill)
            self.shaded.updatepalette(0)
            if self.parentGUI is not None:
                if not self.idx + '_hillshade' in self.parentGUI.added['arrays'].keys():
                    self.parentGUI.add_object('array', newobj=self.shaded, ToCheck=True, id=self.idx + '_hillshade')

        try:
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            for j in range(jstart, jend + 1):
                for i in range(istart, iend + 1):
                    self.fillonecellgrid(cursize, i, j)
                    try:
                        mylistdone = self.mygrid[cursize]['done'][i, j]
                        if mylistdone == 1:
                            mylist = self.mygrid[cursize]['mylists'][i, j]
                            if mylist > 0:
                                glCallList(self.mygrid[cursize]['mylists'][i, j])
                    except:
                        pass

            glDisable(GL_BLEND)
        except:
            pass
        self.plotting = False

        if self.mngselection is not None:
            self.mngselection.plot_selection()

        if self.myops is not None:
            self.myops.myzones.plot()

    def delete_lists(self):
        for idx, cursize in enumerate(self.mygrid):
            curlist = self.mygrid[cursize]
            nbx = curlist['nbx']
            nby = curlist['nby']
            first = curlist['firstlist']
            glDeleteLists(first, nbx * nby)
            wx.LogDebug(str(first)+'  '+str(nbx * nby))

        self.mygrid = {}
        self.gridmaxscales = -1

    def plot_matplotlib(self):

        self.mask_data(0.)
        self.updatepalette(0)

        fig = plt.figure()

        ax = fig.add_subplot(111)
        plt.imshow(self.array.transpose(), origin='lower', cmap=self.mypal,
                   extent=(self.origx, self.origx + self.dx * self.nbx, self.origy, self.origy + self.dy * self.nby))
        ax.set_aspect('equal')

        plt.show()

    def fillonecellgrid(self, curscale, loci, locj, force=False):

        cursize = curscale  # 2**curscale

        if not cursize in self.mygrid.keys():
            return

        curlist = self.mygrid[cursize]
        exists = curlist['done'][loci, locj]

        if exists == 0 or force:
            wx.LogDebug('Computing OpenGL List for '+str(loci)+';' +str(locj) + ' on scale factor '+str(curscale))

            ox = self.origx + self.translx
            oy = self.origy + self.transly
            dx = self.dx
            dy = self.dy

            numlist = int(curlist['mylists'][loci, locj])
            wx.LogDebug(str(numlist))

            try:
                glNewList(numlist, GL_COMPILE)
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

                step = self.gridsize * cursize
                jstart = max(locj * step, 0)
                jend = min(jstart + step, self.nby)
                istart = max(loci * step, 0)
                iend = min(istart + step, self.nbx)

                try:
                    if self.wolftype != WOLF_ARRAY_FULL_SINGLE:
                        if self.nbnotnull != self.nbx * self.nby:
                            if self.nbnotnull > 0:
                                wolfogl.addme(self.array.astype(dtype=np.float32), self.rgb, ox, oy, dx, dy, jstart,
                                              jend, istart, iend, cursize, self.nullvalue, self.alpha)
                        elif self.nbnotnull > 0:
                            wolfogl.addmeall(self.array.astype(dtype=np.float32), self.rgb, ox, oy, dx, dy, jstart,
                                             jend, istart, iend, cursize, self.nullvalue, self.alpha)
                    else:
                        if self.nbnotnull != self.nbx * self.nby:
                            if self.nbnotnull > 0:
                                wolfogl.addme(self.array, self.rgb, ox, oy, dx, dy, jstart, jend, istart, iend, cursize,
                                              self.nullvalue, self.alpha)
                        else:
                            wolfogl.addmeall(self.array, self.rgb, ox, oy, dx, dy, jstart, jend, istart, iend, cursize,
                                             self.nullvalue, self.alpha)
                except:
                    pass
                glEndList()
            except:
                raise NameError(
                    'Opengl in WolfArray_fillonecellgrid -- maybe a conflict with an existing opengl32.dll file - please rename the opengl32.dll in the libs directory and retry')

            curlist['done'][loci, locj] = 1

    def suxsuy_contour(self, filename='',abs=False):

        # Calcul des bords libres SUX, SUY
        indicesX=[]
        indicesY=[]
        
        locls=[]

        dx = self.dx
        dy = self.dy
        
        translx = self.origx 
        transly = self.origy 
        if abs:
            translx += self.translx
            transly += self.transly
        
        for i in range(self.nbx-1):
            for j in range(self.nby-1):
                x1 = float(i+1) * dx + translx
                y1 = float(j+1) * dy + transly
                if self.array.mask[i, j] ^ self.array.mask[i + 1, j]:
                    indicesX.append([i+2, j+1]) # +2, +1 pour être en accord avec le standard de numérotation Fortran
                    locls.append(LineString([[x1,y1-dy],[x1,y1]]))
                    
                if self.array.mask[i, j] ^ self.array.mask[i, j +1]:
                    indicesY.append([i+1,j+2]) # +1, +2 pour être en accord avec le standard de numérotation Fortran
                    locls.append(LineString([[x1-dx,y1],[x1,y1]]))

        interior=False
        contour = linemerge(locls)
        
        if contour.geom_type == 'LineString':
            # All is fine - only one vector
            xy = np.asarray(contour.coords)
            nb = len(xy)
            contourgen = vector(name='external border')
            for x,y in xy:
                contourgen.add_vertex(wolfvertex(x,y))

        elif contour.geom_type == 'MultiLineString':
            interior=True
            # Multiple vectors --> combine
            contour:MultiLineString
            lenghts=[mygeom.length  for mygeom in contour.geoms]
            ind = np.argmax(lenghts)
            
            xyall=[np.column_stack([np.asarray(mygeom.coords),np.zeros(len(mygeom.coords))]) for mygeom in contour.geoms]
            
            xy = xyall[ind]
            
            for i in range(len(xyall)):
                if i!=ind:
                    xy=np.concatenate([xy, 
                                      np.asarray([xyall[i][0,0],xyall[i][0,1],1.]).reshape([1,3]), 
                                      xyall[i][1:], 
                                      np.asarray([xy[0,0],xy[0,1],1.]).reshape([1,3])])
                        
            nb = len(xy)
            contourgen = vector(name='external border')
            for x,y,z in xy:
                contourgen.add_vertex(wolfvertex(x,y,z))
                contourgen.myvertices[-1].in_use = z != 0.
        
        if filename != '':
            with open(filename+'.sux','w') as f:
                # f.write('{}\n'.format(len(self.indicesX)))
                np.savetxt(f,np.asarray(indicesX), delimiter=',', fmt='%u,%u')

            with open(filename + '.suy', 'w') as f:
                # f.write('{}\n'.format(len(self.indicesY)))
                np.savetxt(f, np.asarray(indicesY), delimiter=',', fmt='%u,%u')
                
            with open(filename + '.xy', 'w') as f:
                f.write('{}\n'.format(nb))
                xy[:,0]-=translx-self.origx
                xy[:,1]-=transly-self.origy
                np.savetxt(f, xy[:,:2], delimiter='\t')
                
        return indicesX,indicesY,contourgen,interior

class WolfArrayMB(WolfArray):
    myblocks: dict
    
    def __init__(self, fname=None, mold=None, masknull=True, crop=None, whichtype=WOLF_ARRAY_MB_SINGLE, preload=True,
                 create=False, parentgui=None, nullvalue=0, srcheader=None):
        self.myblocks = {}
        super().__init__(fname, mold, masknull, crop, whichtype, preload, create, parentgui, nullvalue, srcheader)
        self.wolftype = WOLF_ARRAY_MB_SINGLE

    def check_plot(self):
        self.plotted = True
        self.mimic_plotdata()

        if not self.loaded and self.filename != '':
            self.read_data()
            if self.masknull:
                self.mask_data(0.)
            if self.rgb is None:
                self.rgb = np.ones((self.nbx, self.nby, 4), order='F', dtype=np.integer)
            self.updatepalette(0)
            self.loaded = True

    def uncheck_plot(self, unload=True):
        self.plotted = False
        self.mimic_plotdata()

        if unload:
            force = False
            dlg = wx.MessageDialog(None, _('Do you want to reset OpenGL lists?'), style=wx.YES_NO)
            ret = dlg.ShowModal()
            if ret == wx.ID_YES:
                force = True

            for curblock in self.myblocks.values():
                curblock.uncheck_plot(unload, force)
                self.rgb = None
            self.myblocks = {}
            self.loaded = False

    def mask_data(self, value):
        self.nbnotnull = 0
        for i in range(self.nb_blocks):
            curblock = self.myblocks[getkeyblock(i)]
            curarray = curblock.array
            curarray.mask = curarray.data == value

            nbnotnull = curarray.count()
            curblock.nbnotnull = nbnotnull
            self.nbnotnull += nbnotnull

    def read_data(self):

        with open(self.filename, 'rb') as f:
            for i in range(self.nb_blocks):
                curblock = WolfArray(whichtype=WOLF_ARRAY_FULL_SINGLE)
                curblock.isblock = True
                curblock.blockindex = i
                curblock.set_header(self.head_blocks[getkeyblock(i)])
                curblock._read_binary_data(f)
                self.myblocks[getkeyblock(i)] = curblock

    def write_array(self):
        """ Ecriture du tableau en binaire """
        with open(self.filename, 'wb') as f:
            for i in range(self.nb_blocks):
                curarray = self.myblocks[getkeyblock(i)]
                f.write(curarray.array.data.transpose().tobytes())

    def get_ij_from_xy(self, x, y, z=0, scale=1, aswolf=False, abs=True, which_block=1):
        return self.myblocks[getkeyblock(which_block, False)].get_ij_from_xy(x, y, z, scale, aswolf, abs)

    def get_values_as_wolf(self, i, j, which_block=1):

        keyblock = getkeyblock(which_block, False)
        curblock = self.myblocks[keyblock]

        nbx = curblock.nbx
        nby = curblock.nby

        if (i > 0 and i <= nbx and j > 0 and j <= nby):
            h = curblock.array[i - 1, j - 1]

        return h

    def get_value(self, x, y, abs=True):

        h = np.NaN
        for curblock in self.myblocks.values():
            curblock: WolfArray
            nbx = curblock.nbx
            nby = curblock.nby

            i, j = curblock.get_ij_from_xy(x, y, abs=abs)

            if (i > 0 and i <= nbx and j > 0 and j <= nby):
                h = curblock.array[i, j]
                if not curblock.array.mask[i, j]:
                    break

        return h

    def get_xy_from_ij(self, i, j, which_block, aswolf=False, abs=True):
        x, y = self.myblocks[getkeyblock(which_block, False)].get_xy_from_ij(i, j, aswolf=aswolf, abs=abs)
        return x, y

    def get_blockij_from_xy(self, x, y, abs=True):

        exists = False
        k = 1
        for curblock in self.myblocks.values():
            curblock: WolfArray
            nbx = curblock.nbx
            nby = curblock.nby

            i, j = curblock.get_ij_from_xy(x, y, abs=abs)

            if (i > 0 and i <= nbx and j > 0 and j <= nby):
                if not curblock.array.mask[i, j]:
                    exists = True
                    break
            k += 1

        if exists:
            return i, j, k
        else:
            return -1, -1, -1

    def link_palette(self):
        for curblock in self.myblocks.values():
            curblock.mypal = self.mypal

    def updatepalette(self, which=0, onzoom=[]):

        if len(self.myblocks) == 0:
            return

        if onzoom != []:
            allarrays = []
            for curblock in self.myblocks.values():
                istart, jstart = curblock.get_ij_from_xy(onzoom[0], onzoom[2])
                iend, jend = curblock.get_ij_from_xy(onzoom[1], onzoom[3])

                istart = 0 if istart < 0 else istart
                jstart = 0 if jstart < 0 else jstart
                iend = curblock.nbx if iend > curblock.nbx else iend
                jend = curblock.nby if jend > curblock.nby else jend

                partarray = curblock.array[istart:iend, jstart:jend]
                partarray = partarray[partarray.mask == False]
                if len(partarray) > 0:
                    allarrays.append(partarray.flatten())

            allarrays = np.concatenate(allarrays)
            self.mypal.isopop(allarrays, allarrays.count())
        else:
            allarrays = np.concatenate(
                [curblock.array[curblock.array.mask == False].flatten() for curblock in self.myblocks.values()])
            self.mypal.isopop(allarrays, self.nbnotnull)

        self.link_palette()
        for curblock in self.myblocks.values():
            curblock.rgb = self.mypal.get_rgba(curblock.array)

    def delete_lists(self):
        for curblock in self.myblocks.values():
            curblock.delete_lists()

    def mimic_plotdata(self):
        for curblock in self.myblocks.values():
            curblock: WolfArray
            curblock.plotted = self.plotted
            curblock.plotting = self.plotting

    def plot(self, sx=None, sy=None, xmin=None, ymin=None, xmax=None, ymax=None):

        self.plotting = True
        self.mimic_plotdata()

        for curblock in self.myblocks.values():
            curblock.plot(sx, sy, xmin, ymin, xmax, ymax)

        self.plotting = False
        self.mimic_plotdata()

    def fillonecellgrid(self, curscale, loci, locj, force=False):
        for curblock in self.myblocks.values():
            curblock.fillonecellgrid(curscale, loci, locj, force)


class WolfArrayMNAP(WolfArrayMB):
    contour: Zones

    def __init__(self, fname=None, mold=None, masknull=True, crop=None):
        super().__init__(fname, mold, masknull, crop)

        self.contour = Zones()

    def read_data(self):
        with open(self.filename + '.mnap') as f:
            lines = f.read().splitlines()

            self.nb_blocks = abs(int(lines[0]))
            self.contour = Zones()

            decal = 1
            for i in range(self.nb_blocks):
                curkey = getkeyblock(i)
                curarray = WolfArray()
                self.myblocks[curkey] = curarray

                curarray.wolftype = WOLF_ARRAY_FULL_INTEGER8
                curarray.isblock = True
                curarray.blockindex = i

                tmp = re.sub('\\s+', ' ', lines[decal].strip()).split(' ')
                curarray.dx = float(tmp[0])
                curarray.dy = float(tmp[1])

                tmp = re.sub('\\s+', ' ', lines[decal + 1].strip()).split(' ')
                curarray.origx = float(tmp[0]) - self.origx

                tmp = re.sub('\\s+', ' ', lines[decal + 2].strip()).split(' ')
                curarray.origy = float(tmp[0]) - self.origy

                tmp = re.sub('\\s+', ' ', lines[decal + 3].strip()).split(' ')
                curarray.nbx = int(tmp[0])
                curarray.nby = int(tmp[1])

                decal += 4
                myarray = []

                for j in range(curarray.nby):
                    newline = [np.int32(curval) for curval in re.sub('\\s+', ' ', lines[decal].strip()).split()]
                    while len(newline) != curarray.nbx:
                        decal += 1
                        newline = np.concatenate([newline, [np.int32(curval) for curval in
                                                            re.sub('\\s+', ' ', lines[decal].strip()).split()]])
                    myarray.append(newline)
                    decal += 1

                curarray.array = np.flipud(np.ma.asarray(myarray, order='F')).transpose()

                curzone = zone(name=curkey)
                contourblock = vector(name='contour')

                curzone.add_vector(contourblock)
                self.contour.add_zone(curzone)

                nbvert = int(lines[decal])
                for j in range(nbvert):
                    decal += 1
                    xy = re.sub('\\s+', ' ', lines[decal].strip()).split(' ')
                    myvert = wolfvertex(float(xy[0]), float(xy[1]))
                    contourblock.add_vertex(myvert)
                decal += 1
                curarray.translx = self.translx + self.origx
                curarray.transly = self.transly + self.origy

    def read_txt_header(self):

        with open(self.filename + '.trl') as f:
            lines = f.read().splitlines()
            self.translx = float(lines[1])
            self.transly = float(lines[2])

        with open(self.filename + '.par') as f:
            lines = f.read().splitlines()
            self.dx = float(lines[7])
            self.dy = float(lines[8])
            self.nbx = int(lines[9])
            self.nby = int(lines[10])
            self.origx = float(lines[11])
            self.origy = float(lines[12])

        self.wolftype = WOLF_ARRAY_MNAP_INTEGER
        
        
class WolfArray_Sim2D(WolfArray):
    """
    Surcharge de WolfArray pour les matrices fines de simulation
    Objectif :
        - reporter la matrice de mask depuis une source
    """
    
    def __init__(self, fname=None, mold=None, masknull=True, crop=None, whichtype=WOLF_ARRAY_FULL_SINGLE, preload=True, create=False, parentgui=None, nullvalue=0, srcheader=None,masksrc=None):
        self.masksrc=masksrc

        super().__init__(fname, mold, masknull, crop, whichtype, preload, create, parentgui, nullvalue, srcheader)
                
    def check_plot(self):
        self.plotted = True

        if not self.loaded and self.filename != '':
            self.read_data()
            
            if self.array is None:
                #problème à la lecture
                self.plotted=False
                return
            
            if self.masksrc is not None:
                    self.array.mask = self.masksrc

        self.loaded = True

        if self.rgb is None:
            self.updatepalette(0)
            
    def read_all(self):
        if self.filename[-4:]=='zbin':
            fileold = self.filename

            self.filename = fileold[:-4]+'top'
            
            if not os.path.exists(self.filename):
                return
            
            self.read_txt_header()
            self.filename = fileold
            self.read_data()
        else:
            return super().read_all()
    
    def read_data(self):
        
        if self.filename[-4:]=='zbin':
            fileold = self.filename

            self.filename = fileold[:-4]+'top'

            if not os.path.exists(self.filename):
                return
            
            self.read_data()
            toparray = self.array.copy()            

            self.filename = fileold[:-4]+'hbin'
            self.read_data()
            harray = self.array.copy()            
            
            self.array = toparray+harray
            self.array.mask = self.masksrc
            
            self.filename = fileold
        else:
            return super().read_data()
    
    def write_all(self):
        return super().write_all()
    
    def write_array(self):
        if self.filename[-4:]=='zbin':
            fileold = self.filename

            self.filename = fileold[:-4]+'top'
            if not os.path.exists(self.filename):
                self.filename = fileold
                return

            zarray = self.array.copy()            
            self.read_data()
            toparray = self.array.copy()            
            
            self.array = zarray-toparray
            self.array[np.where(self.array<0.)]=0.
                        
            self.filename = fileold[:-4]+'hbin'
            self.write_array()

            self.filename = fileold
        
        else:
            return super().write_array()        
