from os import path
import numpy as np
from wolfhece.textpillow import PRIORITY_FONTSIZE, PRIORITY_WIDTH
import wx
from wx.dataview import *
from wx.core import BoxSizer, FlexGridSizer, TreeItemId
from OpenGL.GL  import *
from shapely.geometry import LineString, MultiLineString,Point,MultiPoint,Polygon,JOIN_STYLE
from shapely.ops import nearest_points,substring
import pygltflib
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import struct
import pyvista as pv

from .PyTranslate import _
from .CpGrid import CpGrid
from .PyVertex import wolfvertex,getIfromRGB,getRGBfromI
from .PyParams import Wolf_Param
from .laz_viewer import myviewer
from .wolf_texture import Text_Image_Texture,Text_Infos
from .drawing_obj import Element_To_Draw


class Triangulation(Element_To_Draw):
    def __init__(self,fn='', idx='', plotted=True, parentgui=None, pts=[],tri=[]) -> None:

        super().__init__(idx, plotted, parentgui)

        self.filename = ''
        self.tri= tri
        self.pts = pts

        self.nb_tri = len(tri)
        self.nb_pts = len(pts)
        
        if fn !='':
            self.filename=fn
            self.read(fn)
        pass
    
    def as_polydata(self) -> pv.PolyData:
        
        return pv.PolyData(np.asarray(self.pts),np.column_stack([[3]*self.nb_tri,self.tri]), self.nb_tri)

    def from_polydata(self,poly:pv.PolyData):
        
        self.pts = np.asarray(poly.points.copy())
        self.tri = list(poly.faces.reshape([int(len(poly.faces)/4),4])[:,1:4])

        self.nb_pts = len(self.pts)
        self.nb_tri = len(self.tri)
    
    def crop_surface(self,other):
        other:Triangulation
        
        mypoly = self.as_polydata()
        mycrop = other.as_polydata()
        
        res = mypoly.crop_surface(other)

    
    def import_from_gltf(self, fn=''):

        if fn =='':
            dlg=wx.FileDialog(None,_('Choose filename'),wildcard='binary gltf2 (*.glb)|*.glb|gltf2 (*.gltf)|*.gltf|All (*.*)|*.*',style=wx.FD_OPEN)
            ret=dlg.ShowModal()
            if ret==wx.ID_CANCEL:
                dlg.Destroy()
                return
            
            fn=dlg.GetPath()
            dlg.Destroy()
            
        gltf = pygltflib.GLTF2().load(fn)

        # get the first mesh in the current scene
        mesh = gltf.meshes[gltf.scenes[gltf.scene].nodes[0]]

        # get the vertices for each primitive in the mesh
        for primitive in mesh.primitives:

            # get the binary data for this mesh primitive from the buffer
            accessor = gltf.accessors[primitive.attributes.POSITION]

            bufferView = gltf.bufferViews[accessor.bufferView]
            buffer = gltf.buffers[bufferView.buffer]
            data = gltf.get_data_from_buffer_uri(buffer.uri)

            # pull each vertex from the binary buffer and convert it into a tuple of python floats
            points = np.zeros([accessor.count, 3], order='F', dtype=np.float64)
            for i in range(accessor.count):
                index = bufferView.byteOffset + accessor.byteOffset + i * 12  # the location in the buffer of this vertex
                d = data[index:index + 12]  # the vertex data
                v = struct.unpack("<fff", d)  # convert from base64 to three floats

                points[i, :] = [v[0], -v[2], v[1]]

            accessor = gltf.accessors[primitive.indices]

            bufferView = gltf.bufferViews[accessor.bufferView]
            buffer = gltf.buffers[bufferView.buffer]
            data = gltf.get_data_from_buffer_uri(buffer.uri)

            triangles = []
            if accessor.componentType==pygltflib.UNSIGNED_SHORT:
                size=6
                format='<HHH'
            elif accessor.componentType==pygltflib.UNSIGNED_INT:
                size=12
                format='<LLL'

            for i in range(int(accessor.count)):
                index = bufferView.byteOffset + accessor.byteOffset + i*size  # the location in the buffer of this vertex
                d = data[index:index+size]  # the vertex data
                v = struct.unpack(format, d)   # convert from base64 to three floats
                triangles.append(list(v))

        self.pts = list(points)
        self.tri = triangles
        
        self.nb_pts = len(points)
        self.nb_tri = len(triangles)
        
    def export_to_gltf(self,fn=''):

        triangles = self.tri
        points = np.column_stack([self.pts[:,0],self.pts[:,2],-self.pts[:,1]]).astype(np.float32)

        triangles_binary_blob = triangles.flatten().tobytes()
        points_binary_blob = points.tobytes()
        
        gltf = pygltflib.GLTF2(
            scene=0,
            scenes=[pygltflib.Scene(nodes=[0])],
            nodes=[pygltflib.Node(mesh=0)],
            meshes=[
                pygltflib.Mesh(
                    primitives=[
                        pygltflib.Primitive(
                            attributes=pygltflib.Attributes(POSITION=1), indices=0
                        )
                    ]
                )
            ],
            accessors=[
                pygltflib.Accessor(
                    bufferView=0,
                    componentType=pygltflib.UNSIGNED_INT,
                    count=self.nb_tri,
                    type=pygltflib.SCALAR,
                    max=[int(triangles.max())],
                    min=[int(triangles.min())],
                ),
                pygltflib.Accessor(
                    bufferView=1,
                    componentType=pygltflib.FLOAT,
                    count=len(points),
                    type=pygltflib.VEC3,
                    max=points.max(axis=0).tolist(),
                    min=points.min(axis=0).tolist(),
                ),
            ],
            bufferViews=[
                pygltflib.BufferView(
                    buffer=0,
                    byteLength=len(triangles_binary_blob),
                    target=pygltflib.ELEMENT_ARRAY_BUFFER,
                ),
                pygltflib.BufferView(
                    buffer=0,
                    byteOffset=len(triangles_binary_blob),
                    byteLength=len(points_binary_blob),
                    target=pygltflib.ARRAY_BUFFER,
                ),
            ],
            buffers=[
                pygltflib.Buffer(
                    byteLength=len(triangles_binary_blob) + len(points_binary_blob)
                )
            ],
        )
        gltf.set_binary_blob(triangles_binary_blob + points_binary_blob)
        
        if fn =='':
            dlg=wx.FileDialog(None,_('Choose filename'),wildcard='binary gltf2 (*.glb)|*.glb|gltf2 (*.gltf)|*.gltf|All (*.*)|*.*',style=wx.FD_SAVE)
            ret=dlg.ShowModal()
            if ret==wx.ID_CANCEL:
                dlg.Destroy()
                return
            
            fn=dlg.GetPath()
            dlg.Destroy()
        
        gltf.save(fn)    
        return fn
    
    def saveas(self,fn=''):
        
        if self.filename=='' and fn=='':
            return
        
        if fn!='':
            self.filename=fn
            
        with open(self.filename,'wb') as f:
            f.write(self.nb_pts.to_bytes(4,'little'))
            self.pts.tofile(f,"")
            f.write(self.nb_tri.to_bytes(4,'little'))
            self.tri.tofile(f,"")

    def read(self,fn):
        with open(fn,'rb') as f:
            self.nb_pts = int.from_bytes(f.read(4),'little')
            buf = np.frombuffer(f.read(8 * self.nb_pts * 3), dtype=np.float64)
            self.pts = np.array(buf.copy(), dtype=np.float64).reshape([self.nb_pts,3])
            
            self.nb_tri = int.from_bytes(f.read(4),'little')
            buf = np.frombuffer(f.read(4 * self.nb_tri * 3), dtype=np.int32)
            self.tri = np.array(buf.copy(), dtype=np.int32).reshape([self.nb_tri,3])

            self.find_minmax(True)
            
    def plot(self, sx=None, sy=None, xmin=None, ymin=None, xmax=None, ymax=None, size=None):
        glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)    

        for curtri in self.tri:
            glBegin(GL_LINE_STRIP)

            glColor3ub(int(0),int(0),int(0))

            glVertex2d(self.pts[curtri[0]][0], self.pts[curtri[0]][1])
            glVertex2d(self.pts[curtri[1]][0], self.pts[curtri[1]][1])
            glVertex2d(self.pts[curtri[2]][0], self.pts[curtri[2]][1])
            glVertex2d(self.pts[curtri[0]][0], self.pts[curtri[0]][1])

            glEnd()
        
        glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)   
    
    def find_minmax(self,force):
        if force:
            if self.nb_pts>0:
                self.minx=np.min(self.pts[:,0])
                self.miny=np.min(self.pts[:,1])
                self.maxx=np.max(self.pts[:,0])
                self.maxy=np.max(self.pts[:,1])
    
    def import_dxf(self,fn):
        import ezdxf
        
        if not path.exists(fn):
            wx.LogWarning(_('File not found !') + ' ' + fn)
            return
        
        # Lecture du fichier dxf et identification du modelspace
        doc = ezdxf.readfile(fn)
        msp = doc.modelspace()        
        
        # Liste de stockage des coordonnées des faces 3D
        xyz = []

        # Bouclage sur les éléments du DXF
        for e in msp:
            if e.dxftype() == "3DFACE":
                # récupération des coordonnées  
                # --> on suppose que ce sont des triangles (!! une face3D peut être un quadrangle !! on oublie donc la 4ème coord)
                xyz += [e[0],e[1],e[2]]
                
        # On souhaite obtenir une triangulation du type :
        #   - liste de coordonnées des sommets des triangles
        #   - par triangle, liste de 3 indices, un pour chaque sommet 
        #
        # Actuellement, les coordonnées sont multipliées car chaque face a été extraite indépendamment
        # On commence donc par identifier les coordonnées uniques, par tuple
        # return_inverse permet de constituer la liste d'indices efficacement
        #
        xyz_u,indices = np.unique(np.array(xyz),return_inverse=True,axis=0)
        triangles = indices.reshape([int(len(indices)/3),3])    
        
        self.tri = triangles.astype(np.int32)
        self.pts = xyz_u
        self.nb_pts = len(self.pts)
        self.nb_tri = len(self.tri)
class vectorproperties:
    
    used:bool
    
    color:int
    width:int
    style:int
    alpha:int
    closed=bool
    filled:bool
    legendvisible:bool
    transparent:bool
    flash:bool

    legendtext:str
    legendrelpos:int
    legendx:float
    legendy:float

    legendbold:bool
    legenditalic:bool
    legendunderlined:bool
    legendfontname=str
    legendfontsize:int
    legendcolor:int

    extrude:bool = False

    myprops:Wolf_Param = None

    def __init__(self,lines=[],parent=None) -> None:
        self.parent:vector
        self.parent=parent
        
        if len(lines)>0:
            line1=lines[0].split(',')
            line2=lines[1].split(',')

            self.color=int(line1[0])
            self.width=int(line1[1])
            self.style=int(line1[2])
            self.closed=line1[3]=='#TRUE#'
            self.filled=line1[4]=='#TRUE#'
            self.legendvisible=line1[5]=='#TRUE#'
            self.transparent=line1[6]=='#TRUE#'
            self.alpha=int(line1[7])
            self.flash=line1[8]=='#TRUE#'

            self.legendtext=line2[0]
            self.legendrelpos=int(line2[1])
            self.legendx=float(line2[2])
            self.legendy=float(line2[3])
            self.legendbold=line2[4]=='#TRUE#'
            self.legenditalic=line2[5]=='#TRUE#'
            self.legendfontname=str(line2[6])
            self.legendfontsize=int(line2[7])
            self.legendcolor=int(line2[8])
            self.legendunderlined=line2[9]=='#TRUE#'

            self.used=lines[2]=='#TRUE#'
        else:
            self.color=0
            self.width=1
            self.style=1
            self.closed=False
            self.filled=False
            self.legendvisible=False
            self.transparent=False
            self.alpha=0
            self.flash=False

            self.legendtext=''
            self.legendrelpos=5
            self.legendx=0.
            self.legendy=0.
            self.legendbold=False
            self.legenditalic=False
            self.legendfontname='Arial'
            self.legendfontsize=10
            self.legendcolor=0
            self.legendunderlined=False

            self.used=True
        
        self.init_extra()

    def init_extra(self):

        self.legendlength = 100
        self.legendheight = 100
        self.legendpriority = 2
        self.legendorientation = 0
        
    def get_extra(self):

        extras = [self.legendlength,
                  self.legendheight,
                  self.legendpriority,
                  self.legendorientation]
        
        return extras

    def set_extra(self,linesextra:list):
        
        if len(linesextra)>0:
            self.legendlength = float(linesextra[0])
            self.legendheight = float(linesextra[1])
            self.legendpriority = float(linesextra[2])
            self.legendorientation = float(linesextra[3])
        

    def saveextra(self,f):
        
        extras = self.get_extra()
                
        f.write(self.parent.myname+'\n')
        f.write('{}\n'.format(len(extras)))
        for curextra in extras:
            f.write('{}'.format(curextra)+'\n') 

    def save(self,f):
        line1 = str(self.color) + ',' + str(self.width)+','+ str(self.style)

        added = ',#TRUE#' if self.closed else ',#FALSE#'
        line1+=added
        added = ',#TRUE#' if self.filled else ',#FALSE#'
        line1+=added
        added = ',#TRUE#' if self.legendvisible else ',#FALSE#'
        line1+=added
        added = ',#TRUE#' if self.transparent else ',#FALSE#'
        line1+=added
        line1+=','+str(self.alpha)
        added = ',#TRUE#' if self.flash else ',#FALSE#'
        line1+=added
        
        f.write(line1+'\n')

        line1 = self.legendtext + ',' + str(self.legendrelpos)+','+ str(self.legendx)+','+ str(self.legendy)
        added = ',#TRUE#' if self.legendbold else ',#FALSE#'
        line1+=added
        added = ',#TRUE#' if self.legenditalic else ',#FALSE#'
        line1+=added
        line1+= ','+self.legendfontname + ',' + str(self.legendfontsize)+ ',' + str(self.legendcolor)
        added = ',#TRUE#' if self.legendunderlined else ',#FALSE#'
        line1+=added
                
        f.write(line1+'\n')
        
        added = '#TRUE#' if self.used else '#FALSE#'
        f.write(added+'\n')
            
    def fill_property_default(self):
        
        curdict=self.myprops.myparams_default
        
        if 'Draw' in curdict.keys():
            keysactive = curdict['Draw'].keys()
            if 'Color' in keysactive:
                self.color = getIfromRGB(curdict['Draw']['Color']['value'])
            if 'Width' in keysactive:
                self.width = int(curdict['Draw']['Width']['value'])
            if 'Style' in keysactive:
                self.style = int(curdict['Draw']['Style']['value'])
            if 'Closed' in keysactive:
                self.closed = bool(curdict['Draw']['Closed']['value'])
            if 'Filled' in keysactive:
                self.filled = bool(curdict['Draw']['Filled']['value'])
            if 'Transparent' in keysactive:
                self.transparent = bool(curdict['Draw']['Transparent']['value'])
            if 'Alpha' in keysactive:
                self.alpha = int(curdict['Draw']['Alpha']['value'])
            if 'Flash' in keysactive:
                self.flash = bool(curdict['Draw']['Flash']['value'])

        if 'Legend' in curdict.keys():
            keysactive = curdict['Legend'].keys()
            if 'Underlined' in keysactive:
                self.legendunderlined = bool(curdict['Legend']['Underlined']['value'])
            if 'Bold' in keysactive:
                self.legendbold = bool(curdict['Legend']['Bold']['value'])
            if 'Font name' in keysactive:
                self.legendfontname = str(curdict['Legend']['Font name']['value'])
            if 'Font size' in keysactive:
                self.legendfontsize = int(curdict['Legend']['Font size']['value'])
            if 'Color' in keysactive:
                self.legendcolor = getIfromRGB(curdict['Legend']['Color']['value'])
            if 'Italic' in keysactive:
                self.legenditalic = bool(curdict['Legend']['Italic']['value'])
            if 'relative Position' in keysactive:
                self.legendrelpos = int(curdict['Legend']['relative Position']['value'])
            if 'Text' in keysactive:
                self.legendtext = str(curdict['Legend']['Text']['value'])
            if 'Visible' in keysactive:
                self.legendvisible = bool(curdict['Legend']['Visible']['value'])
            if 'X' in keysactive:
                self.legendx = float(curdict['Legend']['X']['value'])
            if 'Y' in keysactive:
                self.legendy = float(curdict['Legend']['Y']['value'])

            if 'Length' in keysactive:
                self.legendlength = float(curdict['Legend']['Length']['value'])
            if 'Height' in keysactive:
                self.legendheight = float(curdict['Legend']['Height']['value'])
            if 'Priority' in keysactive:
                self.legendpriority = int(curdict['Legend']['Priority']['value'])
            if 'Orientation' in keysactive:
                self.legendorientation = float(curdict['Legend']['Orientation']['value'])

    def fill_property(self):
        
        curdict=self.myprops.myparams
        self.fill_property_default()
        
        if 'Draw' in curdict.keys():
            keysactive = curdict['Draw'].keys()
            if 'Color' in keysactive:
                self.color = getIfromRGB(curdict['Draw']['Color']['value'].replace('(','').replace(')','').split(', '))
            if 'Width' in keysactive:
                self.width = int(curdict['Draw']['Width']['value'])
            if 'Style' in keysactive:
                self.style = int(curdict['Draw']['Style']['value'])
            if 'Closed' in keysactive:
                self.closed = bool(curdict['Draw']['Closed']['value'])
            if 'Filled' in keysactive:
                self.filled = bool(curdict['Draw']['Filled']['value'])
            if 'Transparent' in keysactive:
                self.transparent = bool(curdict['Draw']['Transparent']['value'])
            if 'Alpha' in keysactive:
                self.alpha = int(curdict['Draw']['Alpha']['value'])
            if 'Flash' in keysactive:
                self.flash = bool(curdict['Draw']['Flash']['value'])

        if 'Legend' in curdict.keys():
            keysactive = curdict['Legend'].keys()
            if 'Underlined' in keysactive:
                self.legendunderlined = bool(curdict['Legend']['Underlined']['value'])
            if 'Bold' in keysactive:
                self.legendbold = bool(curdict['Legend']['Bold']['value'])
            if 'Font name' in keysactive:
                self.legendfontname = str(curdict['Legend']['Font name']['value'])
            if 'Font size' in keysactive:
                self.legendfontsize = int(curdict['Legend']['Font size']['value'])
            if 'Color' in keysactive:
                self.legendcolor = getIfromRGB(curdict['Legend']['Color']['value'].replace('(','').replace(')','').split(', '))
            if 'Italic' in keysactive:
                self.legenditalic = bool(curdict['Legend']['Italic']['value'])
            if 'relative Position' in keysactive:
                self.legendrelpos = int(curdict['Legend']['relative Position']['value'])
            if 'Text' in keysactive:
                self.legendtext = str(curdict['Legend']['Text']['value'])
            if 'Visible' in keysactive:
                self.legendvisible = bool(curdict['Legend']['Visible']['value'])
            if 'X' in keysactive:
                self.legendx = float(curdict['Legend']['X']['value'])
            if 'Y' in keysactive:
                self.legendy = float(curdict['Legend']['Y']['value'])

            if 'Length' in keysactive:
                self.legendlength = float(curdict['Legend']['Length']['value'])
            if 'Height' in keysactive:
                self.legendheight = float(curdict['Legend']['Height']['value'])
            if 'Priority' in keysactive:
                self.legendpriority = int(curdict['Legend']['Priority']['value'])
            if 'Orientation' in keysactive:
                self.legendorientation = float(curdict['Legend']['Orientation']['value'])
                
        if self.legendvisible:
            self.parent.textimage = Text_Image_Texture(self.legendtext,
                                                self.parent.parentzone.parent.parentGUI,
                                                self.get_textfont(),
                                                self.parent,
                                                self.legendx,
                                                self.legendy)
        else: 
            self.parent.textimage=None

    def get_textfont(self):
        
        r,g,b = getRGBfromI(self.legendcolor)
        return Text_Infos(self.legendpriority,
                          (np.cos(self.legendorientation/180*np.pi),np.sin(self.legendorientation/180*np.pi)),
                          self.legendfontname.lower()+'.ttf',
                          self.legendfontsize,
                          colour=(r,g,b,255),
                          dimsreal=(self.legendlength,self.legendheight))
                
    def defaultprop(self):
        if self.myprops is None:
            self.myprops=Wolf_Param(title='Vector Properties',to_read=False)
            self.myprops.callbackdestroy = self.destroyprop
            self.myprops.callback=self.fill_property
            self.myprops.saveme.Disable()
            self.myprops.loadme.Disable()
            self.myprops.reloadme.Disable()

        self.myprops.addparam('Draw','Color',(0,0,0),'Color','Drawing color',whichdict='Default')
        self.myprops.addparam('Draw','Width',1,'Integer','Drawing width',whichdict='Default')
        self.myprops.addparam('Draw','Style',1,'Integer','Drawing style',whichdict='Default')
        self.myprops.addparam('Draw','Closed',False,'Logical','',whichdict='Default')
        self.myprops.addparam('Draw','Filled',False,'Logical','',whichdict='Default')
        self.myprops.addparam('Draw','Transparent',False,'Logical','',whichdict='Default')
        self.myprops.addparam('Draw','Alpha',0,'Integer','Transparent intensity',whichdict='Default')
        self.myprops.addparam('Draw','Flash',False,'Logical','',whichdict='Default')

        self.myprops.addparam('Legend','Visible',False,'Logical','',whichdict='Default')
        self.myprops.addparam('Legend','Text','','String','',whichdict='Default')
        self.myprops.addparam('Legend','relative Position',5,'Integer','',whichdict='Default')
        self.myprops.addparam('Legend','X',0,'Float','',whichdict='Default')
        self.myprops.addparam('Legend','Y',0,'Float','',whichdict='Default')
        self.myprops.addparam('Legend','Bold',False,'Logical','',whichdict='Default')
        self.myprops.addparam('Legend','Italic',False,'Logical','',whichdict='Default')
        self.myprops.addparam('Legend','Font name','Arial','String','',whichdict='Default')
        self.myprops.addparam('Legend','Font size',10,'Integer','',whichdict='Default')
        self.myprops.addparam('Legend','Color',(0,0,0),'Color','',whichdict='Default')
        self.myprops.addparam('Legend','Underlined',False,'Logical','',whichdict='Default')
        self.myprops.addparam('Legend','Length',0,'Float','',whichdict='Default')
        self.myprops.addparam('Legend','Height',0,'Float','',whichdict='Default')
        self.myprops.addparam('Legend','Priority',2,'Integer','',whichdict='Default')
        self.myprops.addparam('Legend','Orientation',0,'Float','',whichdict='Default')

    def destroyprop(self):
        self.myprops=None

    def show(self):
        self.defaultprop()

        self.myprops.addparam('Draw','Color',getRGBfromI(self.color),'Color','Drawing color')
        self.myprops.addparam('Draw','Width',self.width,'Integer','Drawing width')
        self.myprops.addparam('Draw','Style',self.style,'Integer','Drawing style')
        self.myprops.addparam('Draw','Closed',self.closed,'Logical','')
        self.myprops.addparam('Draw','Filled',self.filled,'Logical','')
        self.myprops.addparam('Draw','Transparent',self.transparent,'Logical','')
        self.myprops.addparam('Draw','Alpha',self.alpha,'Integer','Transparent intensity')
        self.myprops.addparam('Draw','Flash',self.flash,'Logical','')

        self.myprops.addparam('Legend','Visible',self.legendvisible,'Logical','')
        self.myprops.addparam('Legend','Text',self.legendtext,'String','')
        self.myprops.addparam('Legend','relative Position',self.legendrelpos,'Integer','')
        self.myprops.addparam('Legend','X',self.legendx,'Float','')
        self.myprops.addparam('Legend','Y',self.legendy,'Float','')
        self.myprops.addparam('Legend','Bold',self.legendbold,'Logical','')
        self.myprops.addparam('Legend','Italic',self.legenditalic,'Logical','')
        self.myprops.addparam('Legend','Font name',self.legendfontname,'String','')
        self.myprops.addparam('Legend','Font size',self.legendfontsize,'Integer','')
        self.myprops.addparam('Legend','Color',getRGBfromI(self.legendcolor),'Color','')
        self.myprops.addparam('Legend','Underlined',self.legendunderlined,'Logical','')

        self.myprops.addparam('Legend','Length',self.legendlength,'Float','')
        self.myprops.addparam('Legend','Height',self.legendheight,'Float','')
        self.myprops.addparam('Legend','Priority',self.legendpriority,'Integer','')
        self.myprops.addparam('Legend','Orientation',self.legendorientation,'Float','')

        self.myprops.Populate()
        self.myprops.Show()

class vector:

    myname:str
    nbvertices:int
    myvertices:list
    myprop:vectorproperties
    minx:float
    miny:float
    maxx:float
    maxy:float

    mytree:TreeListCtrl
    myitem:TreeItemId

    def __init__(self,lines:list=[],is2D=True,name='',parentzone=None) -> None:
            
        self.is2D = is2D
        self.closed=False
        
        self.parentzone:Zones
        self.parentzone=parentzone
        self.minx=-99999.
        self.miny=-99999.
        self.maxx=-99999.
        self.maxy=-99999.
        
        self.mylimits = None
        
        self.textimage=None
                
        self.length2D=None
        self.length3D=None
        self._lengthparts2D=None
        self._lengthparts3D=None
                
        if type(lines)==list:
            if len(lines)>0:
                self.myname=lines[0]
                self.nbvertices=int(lines[1])
                self.myvertices=[]

                if is2D:
                    for i in range(self.nbvertices):
                        try:
                            curx,cury=lines[2+i].split()
                        except:
                            curx,cury=lines[2+i].split(',')
                        curvert = wolfvertex(float(curx),float(cury))
                        self.myvertices.append(curvert)
                else:
                    for i in range(self.nbvertices):
                        try:
                            curx,cury,curz=lines[2+i].split()
                        except:
                            curx,cury,curz=lines[2+i].split(',')
                        curvert = wolfvertex(float(curx),float(cury),float(curz))
                        self.myvertices.append(curvert)

                self.myprop=vectorproperties(lines[self.nbvertices+2:],parent=self)

        if name!='':
            self.myname=name
            self.nbvertices=0
            self.myvertices=[]
            self.myprop=vectorproperties(parent=self)
        
        self.linestring = None
        
        # Utile surtout pour les sections en travers
        self.zdatum = 0.
        self.add_zdatum=False
        self.sdatum = 0.
        self.add_sdatum=False

    def save(self,f):
        f.write(self.myname+'\n')
        f.write(str(self.nbvertices)+'\n')

        force3D=False
        if self.parentzone is not None:
            force3D = self.parentzone.parent.force3D

        if self.is2D and not force3D:
            for curvert in self.myvertices:
                f.write(f'{curvert.x},{curvert.y}'+'\n')
        else:
            for curvert in self.myvertices:
                f.write(f'{curvert.x},{curvert.y},{curvert.z}'+'\n')
                
        self.myprop.save(f)

    def reverse(self):
        self.myvertices.reverse()
       
    def get_values_on_vertices(self,curarray):
        
        if not curarray.plotted:            
            return                                
                        
        for curpt in self.myvertices:
            curpt.z = curarray.get_value(curpt.x,curpt.y)
                            
    def get_values_linked(self,linked_arrays:list,linked_labels:list,refine=True):
        
        exit=True
        for curarray,curlabel in zip(linked_arrays,linked_labels):
            if curarray.plotted:            
                exit=False
                
        if exit:
            return
                
        if refine:
            myzone=zone(name='linked_arrays - fine step')
            myls = self.asshapely_ls()
            length = myls.length
            
            
            for curarray,curlabel in zip(linked_arrays,linked_labels):
                if curarray.plotted:       
                    
                    myvec=vector(name=curlabel,parentzone=myzone) 
                    myzone.add_vector(myvec)    

                    ds = min(curarray.dx,curarray.dy)
                    nb = int(np.ceil(length/ds*2))
                    
                    alls = np.linspace(0,int(length),nb)
                    
                    pts = [myls.interpolate(curs) for curs in alls]
                    
                    allz = [curarray.get_value(curpt.x,curpt.y) for curpt in pts]
                    
                    for curpt,curz in zip(pts,allz):
                        myvec.add_vertex(wolfvertex(curpt.x,curpt.y,curz))
        else:                        
            myzone=zone(name='linked_arrays')
            for curarray,curlabel in zip(linked_arrays,linked_labels):
                if curarray.plotted:       
                    
                    myvec=vector(name=curlabel,parentzone=myzone) 
                    myzone.add_vector(myvec)        

                    for curpt in self.myvertices:
                        myvec.add_vertex(wolfvertex(curpt.x,curpt.y,curarray.get_value(curpt.x,curpt.y)))
                                                    
        return myzone

    def plot_linked(self,fig,ax,linked_arrays,linked_labels):
        
        colors=['red','blue','green']

        exit=True
        for curarray,curlabel in zip(linked_arrays,linked_labels):
            if curarray.plotted:            
                exit=False
                
        if exit:
            return
        
        k=0

        myls = self.asshapely_ls()
        length = myls.length
        tol=length/10.
        ax.set_xlim(0-tol,length+tol)

        zmin=99999.
        zmax=-99999.
        
        for curarray,curlabel in zip(linked_arrays,linked_labels):
            if curarray.plotted:            

                ds = min(curarray.dx,curarray.dy)
                nb = int(np.ceil(length/ds*2))
                
                alls = np.linspace(0,int(length),nb)
                
                pts = [myls.interpolate(curs) for curs in alls]
                
                allz = [curarray.get_value(curpt.x,curpt.y) for curpt in pts]
                
                zmaxloc=np.max(allz)
                zminloc=np.min(allz)
                
                zmax=max(zmax,zmaxloc)
                zmin=min(zmin,zminloc)
                
                if np.max(allz)>-99999:
                    ax.plot(alls,allz,
                            color=colors[np.mod(k,3)],
                            lw=2.0,
                            label=curlabel)
                k+=1
        
        ax.set_ylim(zmin,zmax)
        fig.canvas.draw()

    def plot_mpl(self,show=False,forceaspect=True,fig:Figure=None,ax:Axes=None,labels:dict={}):
        # plot
        
        x,y=self.get_sz()
                
        xmin=x[0]
        xmax=x[-1]
        ymin=np.min(y)
        ymax=np.max(y)
        
        if ax is None:
            redraw=False
            fig = plt.figure()
            ax=fig.add_subplot(111)
        else:
            redraw=True
            ax.cla()

        if 'title' in labels.keys():
            ax.set_title(labels['title'])
        if 'xlabel' in labels.keys():
            ax.set_xlabel(labels['xlabel'])
        if 'ylabel' in labels.keys():
            ax.set_ylabel(labels['ylabel'])

        if ymax>-99999.:
        
            dy=ymax-ymin
            ymin-=dy/4.
            ymax+=dy/4.        
                
            ax.plot(x,y,color='black',
                    lw=2.0,
                    label=self.myname)
                    
            ax.legend()
            
            tol=(xmax-xmin)/10.
            ax.set_xlim(xmin-tol,xmax+tol)
            ax.set_ylim(ymin,ymax)
            
            if forceaspect:
                aspect=1.0*(ymax-ymin)/(xmax-xmin)*(ax.get_xlim()[1] - ax.get_xlim()[0]) / (ax.get_ylim()[1] - ax.get_ylim()[0])
                ax.set_aspect(aspect)
                
        if show:
            fig.show()     
            
        if redraw:
            fig.canvas.draw()
            
        return fig,ax
            
    def isinside(self,x,y):
        if self.nbvertices==0:
            return False
        
        poly = self.asshapely_pol()
        inside2 = poly.contains(Point([x,y]))        
        return inside2
            
    def asshapely_pol(self):
        coords=self.asnparray()
        return Polygon(coords)

    def asshapely_ls(self):
        coords=self.asnparray3d()
        return LineString(coords)

    def asshapely_mp(self):
        multi=self.asnparray3d()
        return MultiPoint(multi)

    def asnparray(self):
        return np.asarray(list([vert.x,vert.y] for vert in self.myvertices))

    def asnparray3d(self):
        xyz= np.asarray(list([vert.x,vert.y,vert.z] for vert in self.myvertices))
        
        if self.add_zdatum:
            xyz[:,2]+=self.zdatum
        return xyz

    def prepare_shapely(self):
        self.linestring = self.asshapely_ls()
        
    def projectontrace(self,trace):
        
        # trace:vector
        tracels:LineString
        tracels = trace.asshapely_ls()
        
        xyz = self.asnparray3d()
        all_s = [tracels.project(Point(cur[0],cur[1])) for cur in xyz]
        
        newvec = vector(name=_('Projection on ')+trace.myname)
        for s,(x,y,z) in zip(all_s,xyz):
            newvec.add_vertex(wolfvertex(s,z))
            
        return newvec

    def parallel_offset(self,distance=5.,side='left'):
        '''
        The distance parameter must be a positive float value.

        The side parameter may be ‘left’ or ‘right’. Left and right are determined by following the direction of the given geometric points of the LineString. 
        Right hand offsets are returned in the reverse direction of the original LineString or LineRing, while left side offsets flow in the same direction.
        '''        
        
        if self.nbvertices<2:
            return None
        
        myls = self.asshapely_ls()
        
        mypar = myls.parallel_offset(distance=abs(distance),side=side,join_style=JOIN_STYLE.round)
        
        if mypar.geom_type=='MultiLineString':
            return None
        
        
        if len(mypar.coords) >0:
            if side=='right':
                #On souhaite garder une même orientation pour les vecteurs
                mypar = substring(mypar, 1., 0., normalized=True)

            newvec = vector(name='par'+str(distance))
            
            for x,y in mypar.coords:
                xy = Point(x,y)
                curs = mypar.project(xy,True)
                curz = myls.interpolate(curs,True).z
                
                newvert = wolfvertex(x,y,curz)
                newvec.add_vertex(newvert)
            
            return newvec
        else:
            return None
        
    def intersection(self,vec2 = None,eval_dist=False,norm=False):
        ls1 = self.asshapely_ls() if self.linestring is None else self.linestring
        ls2 = vec2.asshapely_ls() if vec2.linestring is None else vec2.linestring
        
        myinter = ls1.intersection(ls2)
        
        if eval_dist:
            mydists = ls1.project(myinter,normalized=norm)
            return ls1.intersection(ls2),mydists
        else:
            return ls1.intersection(ls2)

    def reset(self):
        self.nbvertices=0
        self.myvertices=[]
        self.linestring=None
    
    def add_vertex(self,addedvert):
        if type(addedvert) is list:
            for curvert in addedvert:
                self.add_vertex(curvert)
        else:
            self.myvertices.append(addedvert)
            self.nbvertices+=1

    def count(self):
        self.nbvertices=len(self.myvertices)

    def close_force(self):
        cond = self.myvertices[-1] is not self.myvertices[0] and (self.myvertices[-1].x!=self.myvertices[0].x and self.myvertices[-1].y!=self.myvertices[0].y)
        if not self.is2D :
            cond = cond and self.myvertices[-1].z!=self.myvertices[0].z
        if cond:
            self.add_vertex(self.myvertices[0])
            self.closed=True                

    def nblines(self):
        return self.nbvertices+5

    def verify_s_ascending(self):
        
        s,z=self.get_sz(cumul=False)
        
        correction=False
        where=[]
        
        for i in range(self.nbvertices-1):
            if s[i]>s[i+1]:
                
                correction=True
                where.append(i+1)
                
                x=self.myvertices[i].x
                y=self.myvertices[i].y
                
                self.myvertices[i].x=self.myvertices[i+1].x
                self.myvertices[i].y=self.myvertices[i+1].y

                self.myvertices[i+1].x=x
                self.myvertices[i+1].y=y
                
        return correction,where

    def find_nearest_vert(self,x,y):
        
        xy=Point(x,y)
        mynp = self.asnparray()
        mp = MultiPoint(mynp)
        near = np.asarray(nearest_points(mp,xy)[0].coords)
        return self.myvertices[np.asarray(np.argwhere(mynp==near[0])[0,0])]

    def insert_nearest_vert(self,x,y):
        
        xy=Point(x,y)
        mynp = self.asnparray()
        mp = MultiPoint(mynp)
        ls = LineString(mynp)
        
        nearmp = nearest_points(mp,xy) #point le plus proche sur base du nuage
        nearls = nearest_points(ls,xy) #point le plus proche sur base de la ligne
        
        smp = ls.project(nearmp[0]) #distance le long de la ligne du sommet le plus proche
        sls = ls.project(nearls[0]) #distance le long de la ligne du point le plus proche au sens géométrique (perpendiculaire au segment) 
        
        indexmp= np.argwhere(mynp==nearmp[0])[0,0] #index du vertex
        
        if indexmp==0 and self.closed:
            #le vecteur est fermé
            #il faut donc chercher à savoir si le point est après le premier point ou avant le dernier (qui possèdent les mêmes coords)
            if sls<=ls.length and sls >=ls.project(Point([self.myvertices[-2].x,self.myvertices[-2].y])):
                smp=ls.length
                indexmp=self.nbvertices-1
            else:
                indexmp=1
        else:
            if sls >= smp:
                #le point projeté sur la droite est au-delà du vertex le plus proche
                #on ajoute donc le point après
                indexmp+=1

        myvert=wolfvertex(x,y)
        self.myvertices.insert(indexmp,myvert)
        self.nbvertices+=1

        return self.myvertices[indexmp]
    
    def find_minmax(self):
        if len(self.myvertices)>0:
            self.minx=min(vert.x for vert in self.myvertices)
            self.miny=min(vert.y for vert in self.myvertices)
            self.maxx=max(vert.x for vert in self.myvertices)
            self.maxy=max(vert.y for vert in self.myvertices)

    def plot(self):

        if self.myprop.used:
            
            if self.myprop.filled:
                glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)         
            else:   
                glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)       
                
            rgb=getRGBfromI(self.myprop.color)
                        
            if self.myprop.transparent:
                glEnable(GL_BLEND)
                glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA)
            else:
                glDisable(GL_BLEND)
            
            glLineWidth(float(self.myprop.width))
            #glPointSize(float(self.myprop.width))

            if self.myprop.filled:
                glBegin(GL_POLYGON)
            else:   
                glBegin(GL_LINE_STRIP)

            if self.myprop.transparent:
                glColor4ub(int(rgb[0]),int(rgb[1]),int(rgb[2]),int(self.myprop.alpha))
            else:
                glColor3ub(int(rgb[0]),int(rgb[1]),int(rgb[2]))

            for curvertex in self.myvertices:
                glVertex2d(curvertex.x, curvertex.y)

            if self.myprop.closed and (self.myvertices[0].x != self.myvertices[-1].x or self.myvertices[0].y != self.myvertices[-1].y):
                curvertex = self.myvertices[0]
                glVertex2d(curvertex.x, curvertex.y)

            glEnd()
            
            glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
            glDisable(GL_BLEND)        
            
            if self.myprop.legendvisible:
                self.textimage.paint()        

    def add2tree(self,tree:TreeListCtrl,root):
        self.mytree=tree
        self.myitem=tree.AppendItem(root, self.myname,data=self)
        if self.myprop.used:
            tree.CheckItem(self.myitem)

    def unuse(self):
        self.myprop.used=False
        self.mytree.UncheckItem(self.myitem)

    def use(self):
        self.myprop.used=True
        self.mytree.CheckItem(self.myitem)

    def fillgrid(self,gridto:CpGrid):
        curv:wolfvertex

        gridto.SetColLabelValue(0,'X')
        gridto.SetColLabelValue(1,'Y')
        gridto.SetColLabelValue(2,'Z')
        gridto.SetColLabelValue(3,'value')
        gridto.SetColLabelValue(4,'s curvi')
        
        nb=gridto.GetNumberRows()
        if len(self.myvertices)-nb>0:
            gridto.AppendRows(len(self.myvertices)-nb)
        k=0
        for curv in self.myvertices:
           gridto.SetCellValue(k,0,str(curv.x))
           gridto.SetCellValue(k,1,str(curv.y))
           gridto.SetCellValue(k,2,str(curv.z))
           k+=1

    def updatefromgrid(self,gridfrom:CpGrid):
        curv:wolfvertex
       
        nbl=gridfrom.GetNumberRows()       
        k=0
        while k<nbl:
            x=gridfrom.GetCellValue(k,0)
            y=gridfrom.GetCellValue(k,1)
            z=gridfrom.GetCellValue(k,2)
            if z=='':
                z=0.
            if x!='':
                if k<self.nbvertices:
                    self.myvertices[k].x=float(x)
                    self.myvertices[k].y=float(y)
                    self.myvertices[k].z=float(z)
                else:
                    newvert=wolfvertex(float(x),float(y),float(z))
                    self.add_vertex(newvert)
                k+=1
            else:
                break

        while k<self.nbvertices:
            self.myvertices.pop(k)
            self.nbvertices-=1
            
        if self.linestring is not None:
            self.prepare_shapely()

    def get_s3d(self):
        s3d=np.zeros[self.nbvertices]
        for k in range(1,self.nbvertices+1):
            s3d[k]=s3d[k-1]+self.myvertices[k-1].dist3D(self.myvertices[k])

    def get_sz(self,cumul=True):
            
        z = np.asarray([self.myvertices[i].z for i in range(self.nbvertices)])
        
        nb = len(z)
        s = np.zeros(nb)
                
        if cumul:
            x1 = self.myvertices[0].x
            y1 = self.myvertices[0].y
            for i in range(nb-1):
                x2 = self.myvertices[i+1].x
                y2 = self.myvertices[i+1].y
                
                length = np.sqrt((x2-x1)**2.+(y2-y1)**2.)
                s[i+1] = s[i]+length
                
                x1=x2
                y1=y2
        else:
            for i in range(nb):
                s[i] = self.myvertices[0].dist2D(self.myvertices[i])
                            
        return s,z

    def update_lengths(self):      
        self._lengthparts2D=np.zeros(self.nbvertices-1)
        self._lengthparts3D=np.zeros(self.nbvertices-1)
        
        for k in range(self.nbvertices-1):
            self._lengthparts2D[k] = self.myvertices[k].dist2D(self.myvertices[k+1])
            self._lengthparts3D[k] = self.myvertices[k].dist3D(self.myvertices[k+1])
            
        if self.closed and self.myvertices[0]!=self.myvertices[-1]:
            self._lengthparts2D[-1] = self.myvertices[-2].dist2D(self.myvertices[-1])
            self._lengthparts3D[-1] = self.myvertices[-2].dist3D(self.myvertices[-1])

        self.length2D = np.sum(self._lengthparts2D)
        self.length3D = np.sum(self._lengthparts3D)
        
    def get_segment(self,s,is3D,adim=True,frombegin=True):
        if is3D:
            length = self.length3D
            lengthparts = self._lengthparts3D
        else:
            length = self.length2D
            lengthparts = self._lengthparts2D
        
        if length is None:
            self.update_lengths()
            if is3D:
                length = self.length3D
                lengthparts = self._lengthparts3D
            else:
                length = self.length2D
                lengthparts = self._lengthparts2D
            
        cums = np.cumsum(lengthparts)

        if adim:
            cums = cums.copy()/length
            cums[-1]=1.
            lengthparts = lengthparts.copy()/length
            if s>1.:
                s=1.
            if s<0.:
                s=0.
        else:        
            if s>length:
                s=length
            if s<0.:
                s=0.
        
        if frombegin:
            k=0
            while s>cums[k]:
                k+=1
        else:
            k=self.nbvertices-2
            if k>0:
                while s<cums[k] and k>0:
                    k-=1                
                if (k==0 and s<cums[0]) or s==cums[self.nbvertices-2]:
                    pass
                else:
                    k+=1
                
        if k==len(cums):
            k=len(cums)

        return k,cums[k],lengthparts
    
    def split(self,ds):
        
        newvec = vector(name=self.myname+'_split',parentzone=self.parentzone)

        self.update_lengths()
        
        locds = ds/self.length3D
        
        dist3d = np.concatenate([np.arange(0.,1.,locds),np.cumsum(self._lengthparts3D)/self.length3D])
        dist3d = np.unique(dist3d)
        
        for curs in dist3d:
            newvec.add_vertex(self.interpolate(curs,is3D=True,adim=True))
            
        curzone:zone
        curzone=self.parentzone
        curzone.add_vector(newvec)
        
        try:
            curzone.parent.fill_structure()
        except:
            pass
    
    def interpolate(self,s,is3D=True,adim=True,frombegin=True):
        
        k,cums,lengthparts=self.get_segment(s,is3D,adim,frombegin)
                
        pond = (cums-s)/lengthparts[k]
        
        return wolfvertex(self.myvertices[k].x*pond+self.myvertices[k+1].x*(1.-pond),
                          self.myvertices[k].y*pond+self.myvertices[k+1].y*(1.-pond),
                          self.myvertices[k].z*pond+self.myvertices[k+1].z*(1.-pond))
        
    def substring(self,s1,s2,is3D=True,adim=True,eps=1.e-2):
        
        if s1==s2:
            s2+=eps

        k1,cums1,lengthparts1=self.get_segment(s1,is3D,adim,True)
        k2,cums2,lengthparts2=self.get_segment(s2,is3D,adim,False)
                
        pond1 = max((cums1-s1)/lengthparts1[k1],0.)
        pond2 = min((cums2-s2)/lengthparts2[k2],1.)
        
        v1= wolfvertex(self.myvertices[k1].x*pond1+self.myvertices[k1+1].x*(1.-pond1),
                       self.myvertices[k1].y*pond1+self.myvertices[k1+1].y*(1.-pond1),
                       self.myvertices[k1].z*pond1+self.myvertices[k1+1].z*(1.-pond1))
        
        v2= wolfvertex(self.myvertices[k2].x*pond2+self.myvertices[k2+1].x*(1.-pond2),
                       self.myvertices[k2].y*pond2+self.myvertices[k2+1].y*(1.-pond2),
                       self.myvertices[k2].z*pond2+self.myvertices[k2+1].z*(1.-pond2))
        
        newvec = vector(name='substr')
        
        newvec.add_vertex(v1)
        
        if s1<=s2:
            if is3D:
                for k in range(k1+1,k2+1):
                    if self.myvertices[k].dist3D(newvec.myvertices[-1])!=0.:
                        newvec.add_vertex(self.myvertices[k])
            else:
                for k in range(k1+1,k2+1):
                    if self.myvertices[k].dist2D(newvec.myvertices[-1])!=0.:
                        newvec.add_vertex(self.myvertices[k])
        else:            
            if is3D:
                for k in range(k1+1,k2+1,-1):
                    if self.myvertices[k].dist3D(newvec.myvertices[-1])!=0.:
                        newvec.add_vertex(self.myvertices[k])
            else:
                for k in range(k1+1,k2+1,-1):
                    if self.myvertices[k].dist2D(newvec.myvertices[-1])!=0.:
                        newvec.add_vertex(self.myvertices[k])

        if [v2.x,v2.y,v2.z] != [newvec.myvertices[-1].x,newvec.myvertices[-1].y,newvec.myvertices[-1].z]:
            newvec.add_vertex(v2)
            
        # if newvec.nbvertices==0:
        #     a=1
        # if newvec.nbvertices==1:
        #     a=1
        # newvec.update_lengths()
        # if np.min(newvec._lengthparts2D)==0.:
        #     a=1
        return newvec

class zone:

    myname:str
    nbvectors:int
    myvectors:list
    minx:float
    miny:float
    maxx:float
    maxy:float
    selected_vectors:list
    mytree:TreeListCtrl
    myitem:TreeItemId
    active_vector:vector

    def __init__(self,lines=[],name='',parent=None,is2D=True) -> None:
        
        self.idgllist = -99999
        self.active_vector=None
        self.parent=parent

        if len(lines)>0:
            self.myname=lines[0]
            self.nbvectors=int(lines[1])
            self.myvectors=[]
            curstart=2
            for i in range(self.nbvectors):
                curvec=vector(lines[curstart:],parentzone=self,is2D=is2D)
                curstart+=curvec.nblines()
                self.myvectors.append(curvec)

        if name!='':
            self.myname=name
            self.nbvectors=0
            self.myvectors=[]
        
        self.selected_vectors=[]
        self.multils = None
        self.used = True

        pass

    def save(self,f):
        f.write(self.myname+'\n')
        f.write(str(self.nbvectors)+'\n')
        for curvect in self.myvectors:
            curvect.save(f)

    def saveextra(self,f):
        f.write(self.myname+'\n')
        curvect:vector
        for curvect in self.myvectors:
            curvect.myprop.saveextra(f)

    def add_vector(self,addedvect,index=-99999):
        
        if index==-99999 or index >self.nbvectors:
            self.myvectors.append(addedvect)
        else:
            self.myvectors.insert(index,addedvect)
        self.nbvectors+=1
        
        if self.nbvectors==1:
            self.active_vector = addedvect

    def count(self):
        self.nbvectors=len(self.myvectors)

    def nblines(self):
        nb=2
        for curvec in self.myvectors:
            nb+=curvec.nblines()
        
        return nb

    def find_minmax(self,update=False):
        if update:
            for vect in self.myvectors:
                vect.find_minmax()

        if self.nbvectors==0:
            self.minx=-99999.
            self.miny=-99999.
            self.maxx=-99999.
            self.maxy=-99999.
        else:
            minsx=np.asarray([vect.minx for vect in self.myvectors])
            minsy=np.asarray([vect.miny for vect in self.myvectors])
            maxsx=np.asarray([vect.maxx for vect in self.myvectors])
            maxsy=np.asarray([vect.maxy for vect in self.myvectors])
            
            if len(minsx)>1:
                self.minx=np.min(minsx[np.where(minsx!=-99999.)])
                self.maxx=np.max(maxsx[np.where(maxsx!=-99999.)])
                self.miny=np.min(minsy[np.where(minsy!=-99999.)])
                self.maxy=np.max(maxsy[np.where(maxsy!=-99999.)])
            else:
                self.minx=minsx[0]
                self.maxx=maxsx[0]
                self.miny=minsy[0]
                self.maxy=maxsy[0]
            
    def plot(self,prep=False):
        
        if prep:
            if self.idgllist==-99999:
                self.idgllist = glGenLists(1)
            
            glNewList(self.idgllist,GL_COMPILE)
            for curvect in self.myvectors:
                curvect.plot()        
            glEndList()
        else:
            if self.idgllist!=-99999:
                glCallList(self.idgllist)
            else:
                for curvect in self.myvectors:
                    curvect.plot()

    def select_vectors_from_point(self,x:float,y:float,inside=True):
        curvect:vector
        self.selected_vectors.clear()
        
        if inside:
            for curvect in self.myvectors:
                if curvect.isinside(x,y):
                    self.selected_vectors.append((curvect,99999.))
        else:
            distmin=99999.
            for curvect in self.myvectors:
                nvert:wolfvertex
                nvert= curvect.find_nearest_vert(x,y)
                dist=np.sqrt((nvert.x-x)**2.+(nvert.y-y)**2.)
                if dist<distmin:
                    distmin=dist
                    vectmin=curvect
            
            self.selected_vectors.append((vectmin,distmin))
                    
    def add2tree(self,tree:TreeListCtrl,root):
        self.mytree=tree
        self.myitem=tree.AppendItem(root, self.myname,data=self)
                
        for curvect in self.myvectors:
            curvect.add2tree(tree,self.myitem)

        if self.used:
            tree.CheckItem(self.myitem)
        else:
            tree.UncheckItem(self.myitem)
            
    def unuse(self):
        for curvect in self.myvectors:
            curvect.unuse()
        self.used=False
        self.mytree.UncheckItem(self.myitem)

    def use(self):
        for curvect in self.myvectors:
            curvect.use()
        self.used=True
        self.mytree.CheckItem(self.myitem)

    def asshapely_ls(self):
        mylines=[]
        curvect:vector
        for curvect in self.myvectors:
            mylines.append(curvect.asshapely_ls())
        return MultiLineString(mylines)

    def prepare_shapely(self):
        self.multils = self.asshapely_ls()

    def get_selected_vectors(self,all=False):
        if all:
            mylist=[]
            if len(self.selected_vectors)>0:
                mylist.append(self.selected_vectors)
            return mylist
        else:
            if len(self.selected_vectors)>0:
                return self.selected_vectors[0]
                
        return None

    def add_parallel(self,distance):
        
        if distance>0.:
            mypl = self.active_vector.parallel_offset(distance,'right')
        elif distance<0.:
            mypl = self.active_vector.parallel_offset(distance,'left')
        else:
            mypl = vector(name=self.active_vector.myname+"_duplicate")
            mypl.myvertices = [wolfvertex(cur.x,cur.y,cur.z) for cur in self.active_vector.myvertices]
            mypl.nbvertices = self.active_vector.nbvertices
                    
        if mypl is None:
            return
        
        mypl.parentzone = self
        self.add_vector(mypl)

    def parallel_active(self,distance):
        
        if self.nbvectors>1:
            self.myvectors = [curv for curv in self.myvectors if curv ==self.active_vector]
            self.nbvectors = 1
            
        mypl = self.active_vector.parallel_offset(distance,'left')
        mypr = self.active_vector.parallel_offset(distance,'right')
        
        if mypl is None or mypr is None:
            return
        
        self.add_vector(mypl,0)
        self.add_vector(mypr,2)
        
    def create_polygon_from_parallel(self,ds,howmanypoly=1):
        
        vecleft:vector
        vecright:vector
        veccenter:vector
        vecleft = self.myvectors[0]
        veccenter = self.myvectors[1]
        vecright = self.myvectors[2]
        
        #Shapely LineString
        lsl = vecleft.asshapely_ls()
        lsr = vecright.asshapely_ls()
        lsc = veccenter.asshapely_ls()

        #Number of points
        nb = int(np.ceil(lsc.length / ds))
        #Adimensional distances along center vector
        sloc = np.linspace(0.,1.,nb,endpoint=True)
        #Points along center vector
        ptsc = [lsc.interpolate(curs,True) for curs in sloc]
        #Real distances along left, right and center vector
        sl = [lsl.project(curs) for curs in ptsc]
        sr = [lsr.project(curs) for curs in ptsc]
        sc = [lsc.project(curs) for curs in ptsc]

        if howmanypoly==1:
            #un seul polygone sur base des // gauche et droite
            zonepoly = zone(name='polygons_'+self.myname,parent=self.parent)
                        
            self.parent.add_zone(zonepoly)
                        
            for i in range(len(sl)-1):
                
                #mean distance along center will be stored as Z value of each vertex
                smean =(sc[i]+sc[i+1])/2.
                curvec=vector(name='poly'+str(i+1),parentzone=zonepoly)
                #Substring for Left and Right
                sublsl=substring(lsl,sl[i],sl[i+1])            
                sublsr=substring(lsr,sr[i],sr[i+1])            
                
                #Test if the substring result is Point or LineString
                if sublsl.geom_type=='Point':
                    curvec.add_vertex(wolfvertex(sublsl.x,sublsl.y,smean))
                elif sublsl.geom_type=='LineString':
                    xy=np.asarray(sublsl.coords)
                    for (x,y) in xy:
                        curvec.add_vertex(wolfvertex(x,y,smean))

                if sublsr.geom_type=='Point':
                    curvec.add_vertex(wolfvertex(sublsr.x,sublsr.y,smean))
                elif sublsr.geom_type=='LineString':
                    xy=np.asarray(sublsr.coords)
                    xy=np.flipud(xy)
                    for (x,y) in xy:
                        curvec.add_vertex(wolfvertex(x,y,smean))
                
                #force to close the polygon
                curvec.close_force()
                #add vector to zone
                zonepoly.add_vector(curvec)
                
            #force to update minmax in the zone --> mandatory to plot
            zonepoly.find_minmax(True)
        else:
            #deux polygones sur base des // gauche et droite
            zonepolyleft = zone(name='polygons_left_'+self.myname,parent=self.parent)
            zonepolyright = zone(name='polygons_right_'+self.myname,parent=self.parent)
            self.parent.add_zone(zonepolyleft)
            self.parent.add_zone(zonepolyright)
                        
            for i in range(len(sl)-1):
                
                smean =(sc[i]+sc[i+1])/2.
                curvecleft=vector(name='poly'+str(i+1),parentzone=zonepolyleft)
                curvecright=vector(name='poly'+str(i+1),parentzone=zonepolyright)
                
                sublsl=substring(lsl,sl[i],sl[i+1])            
                sublsr=substring(lsr,sr[i],sr[i+1])            
                sublsc=substring(lsc,sc[i],sc[i+1])            
                
                #left poly
                if sublsl.geom_type=='Point':
                    curvecleft.add_vertex(wolfvertex(sublsl.x,sublsl.y,smean))
                elif sublsl.geom_type=='LineString':
                    xy=np.asarray(sublsl.coords)
                    for (x,y) in xy:
                        curvecleft.add_vertex(wolfvertex(x,y,smean))

                if sublsc.geom_type=='Point':
                    curvecleft.add_vertex(wolfvertex(sublsc.x,sublsc.y,smean))
                elif sublsc.geom_type=='LineString':
                    xy=np.asarray(sublsc.coords)
                    xy=np.flipud(xy)
                    for (x,y) in xy:
                        curvecleft.add_vertex(wolfvertex(x,y,smean))

                #right poly
                if sublsc.geom_type=='Point':
                    curvecright.add_vertex(wolfvertex(sublsc.x,sublsc.y,smean))
                elif sublsc.geom_type=='LineString':
                    xy=np.asarray(sublsc.coords)
                    for (x,y) in xy:
                        curvecright.add_vertex(wolfvertex(x,y,smean))

                if sublsr.geom_type=='Point':
                    curvecright.add_vertex(wolfvertex(sublsr.x,sublsr.y,smean))
                elif sublsr.geom_type=='LineString':
                    xy=np.asarray(sublsr.coords)
                    xy=np.flipud(xy)
                    for (x,y) in xy:
                        curvecright.add_vertex(wolfvertex(x,y,smean))
                
                curvecleft.close_force()
                curvecright.close_force()
                
                zonepolyleft.add_vector(curvecleft)
                zonepolyright.add_vector(curvecright)
                
            
            zonepolyleft.find_minmax(True)
            zonepolyright.find_minmax(True)
                    
        self.parent.fill_structure()

    def plot_linked_poly(self,fig,ax,linked_arrays,linked_labels,linestyle='-'):
        
        colors=['red','blue','green','darkviolet','fuchsia','lime']

        exit=True
        for curarray,curlabel in zip(linked_arrays,linked_labels):
            if curarray.plotted:            
                exit=False
                
        if exit:
            return
        
        k=0

        zmin=99999.
        zmax=-99999.
        
        srefs=np.asarray([curpol.myvertices[0].z for curpol in self.myvectors])
        
        for curarray,curlabel in zip(linked_arrays,linked_labels):
            if curarray.plotted:            

                vals= [curarray.get_values_insidepoly(curpol) for curpol in self.myvectors]
                
                values = np.asarray([cur[0] for cur in vals],dtype=object)
                valel  = np.asarray([cur[1] for cur in vals],dtype=object)
                
                zmaxloc=np.asarray([np.max(curval) for curval in values])
                zminloc=np.asarray([np.min(curval) for curval in values])
                
                zmax=max(zmax,np.max(zmaxloc))
                zmin=min(zmin,np.min(zminloc[np.where(zminloc>-99999.)]))
                
                if zmax>-99999:
                    
                    zloc = np.asarray([np.median(curpoly) for curpoly in values])
                    
                    ax.plot(srefs[np.where(zloc!=-99999.)],zloc[np.where(zloc!=-99999.)],
                            color=colors[np.mod(k,3)],
                            lw=2.0,
                            linestyle=linestyle,
                            label=curlabel+'_median')

                    zloc = np.asarray([np.min(curpoly) for curpoly in values])

                    ax.plot(srefs[np.where(zloc!=-99999.)],zloc[np.where(zloc!=-99999.)],
                            color=colors[np.mod(k,3)],alpha=.3,
                            lw=2.0,
                            linestyle=linestyle,
                            label=curlabel+'_min')

                    zloc = np.asarray([np.max(curpoly) for curpoly in values])

                    ax.plot(srefs[np.where(zloc!=-99999.)],zloc[np.where(zloc!=-99999.)],
                            color=colors[np.mod(k,3)],alpha=.3,
                            lw=2.0,
                            linestyle=linestyle,
                            label=curlabel+'_max')
                
                if valel[0] is not None:
                    zmaxloc=np.asarray([np.max(curval) for curval in valel])
                    zminloc=np.asarray([np.min(curval) for curval in valel])
                    
                    zmax=max(zmax,np.max(zmaxloc))
                    zmin=min(zmin,np.min(zminloc[np.where(zminloc>-99999.)]))
                    
                    if zmax>-99999:
                        
                        zloc = np.asarray([np.median(curpoly) for curpoly in valel])
                        
                        ax.plot(srefs[np.where(zloc!=-99999.)],zloc[np.where(zloc!=-99999.)],
                                color='black',
                                lw=2.0,
                                linestyle=linestyle,
                                label=curlabel+'_top_median')

                        # zloc = np.asarray([np.min(curpoly) for curpoly in valel])

                        # ax.plot(srefs[np.where(zloc!=-99999.)],zloc[np.where(zloc!=-99999.)],
                        #         color='black',alpha=.3,
                        #         lw=2.0,
                        #         linestyle=linestyle,
                        #         label=curlabel+'_top_min')

                        # zloc = np.asarray([np.max(curpoly) for curpoly in valel])

                        # ax.plot(srefs[np.where(zloc!=-99999.)],zloc[np.where(zloc!=-99999.)],
                        #         color='black',alpha=.3,
                        #         lw=2.0,
                        #         linestyle=linestyle,
                        #         label=curlabel+'_top_max')
                    
                k+=1
        
        ax.set_ylim(zmin,zmax)
        fig.canvas.draw()

class Zones(wx.Frame):

    idx:str
    tx:float
    ty:float
    minx:float
    miny:float
    maxx:float
    maxy:float

    nbzones:int

    myzones:list
    treelist:TreeListCtrl
    xls:CpGrid

    def __init__(self,myfile='',ox:float=0.,oy:float=0.,tx:float=0.,ty:float=0.,parent=None,is2D=True):
        self.loaded=True
        self.active_vector = None
        self.active_zone = None
        self.last_active = None
        self.force3D=False
        self.is2D=is2D

        self.filename=myfile

        try:
            super(Zones, self).__init__(None, size=(300, 400))
            self.Bind(wx.EVT_CLOSE,self.OnClose)
        except:
            pass
        
        self.parent = parent
        self.parentGUI = parent
        self.init_struct=True

        self.minx=ox
        self.miny=oy
        self.tx=tx
        self.ty=ty
        self.myzones=[]
        self.nbzones=0
        
        if myfile!='':
            
            if myfile.endswith('.dxf'):
                self.is2D=False
                self.import_dxf(myfile)
            else:
                if myfile.endswith('.vecz'):
                    self.is2D=False
                
                f = open(myfile, 'r')
                lines = f.read().splitlines()
                f.close()

                try:
                    tx,ty=lines[0].split()
                except:
                    tx,ty=lines[0].split(',')
                
                self.tx=float(tx)
                self.ty=float(ty)
                self.nbzones=int(lines[1])

                curstart=2
                for i in range(self.nbzones):
                    curzone=zone(lines[curstart:],parent=self,is2D=self.is2D)
                    self.myzones.append(curzone)
                    curstart+=curzone.nblines()

            self.find_minmax(True)

    def import_dxf(self, fn, imported_elts=['POLYLINE','LWPOLYLINE','LINE']):
        import ezdxf
        
        if not path.exists(fn):
            wx.LogWarning(_('File not found !') + ' ' + fn)
            return
        
        # Lecture du fichier dxf et identification du modelspace
        doc = ezdxf.readfile(fn)
        msp = doc.modelspace()  
        layers = doc.layers   

        used_layers = {}
        # Bouclage sur les éléments du DXF pour identifier les layers utiles et ensuite créer les zones adhoc
        for e in msp:
            if doc.layers.get(e.dxf.layer).dxf.plot==1:
                if e.dxftype() == "POLYLINE":
                    if e.dxf.layer not in used_layers.keys():
                        curlayer = used_layers[e.dxf.layer]={}                    
                    else:
                        curlayer = used_layers[e.dxf.layer]    
                    curlayer[e.dxftype().lower()]=0
                    
                elif e.dxftype() == "LWPOLYLINE":
                    if e.dxf.layer not in used_layers.keys():
                        curlayer = used_layers[e.dxf.layer]={}                    
                    else:
                        curlayer = used_layers[e.dxf.layer]    
                    curlayer[e.dxftype().lower()]=0
                
                elif e.dxftype() == "LINE": # dans ce cas spécifique, ce sont a priori les lignes composant les croix sur les points levés
                    if e.dxf.layer not in used_layers.keys():
                        curlayer = used_layers[e.dxf.layer]={}                    
                    else:
                        curlayer = used_layers[e.dxf.layer]        
                    curlayer[e.dxftype().lower()]=0
            else:
                pass
        
        # Création des zones
        for curlayer in used_layers.keys():
            for curtype in used_layers[curlayer].keys():
                curzone = used_layers[curlayer][curtype] = zone(name = '{} - {}'.format(curlayer,curtype),is2D=self.is2D,parent=self)
                self.add_zone(curzone)

        # Nouveau bouclage sur les éléments du DXF pour remplissage
        nbid=0
        for e in msp:
            if doc.layers.get(e.dxf.layer).dxf.plot==1:
                
                if e.dxftype() == "POLYLINE":
                    nbid+=1
                    # récupération des coordonnées  
                    verts = [cur.dxf.location.xyz for cur in e.vertices]
                    
                    curzone = used_layers[e.dxf.layer][e.dxftype().lower()]
                    
                    curpoly = vector(is2D=False,name=e.dxf.handle,parentzone=curzone)
                    curzone.add_vector(curpoly)
                    
                    for cur in verts:
                        myvert = wolfvertex(cur[0],cur[1],cur[2])
                        curpoly.add_vertex(myvert)
                        
                elif e.dxftype() == "LWPOLYLINE":
                    nbid+=1
                    # récupération des coordonnées  
                    verts = np.array(e.lwpoints.values)
                    verts = verts.reshape([int(len(verts)/5),5])[:,:2]
                    verts = np.column_stack([verts,[e.dxf.elevation]*len(verts)])
                    
                    curzone = used_layers[e.dxf.layer][e.dxftype().lower()]
                                    
                    curpoly = vector(is2D=False,name=e.dxf.handle,parentzone=curzone)
                    curzone.add_vector(curpoly)
                    for cur in verts:
                        myvert = wolfvertex(cur[0],cur[1],cur[2])
                        curpoly.add_vertex(myvert)

                elif e.dxftype() == "LINE": 
                    nbid+=1
                                    
                    curzone = used_layers[e.dxf.layer][e.dxftype().lower()]
                                    
                    curpoly = vector(is2D=False,name=e.dxf.handle,parentzone=curzone)
                    curzone.add_vector(curpoly)
                    
                    # récupération des coordonnées  
                    myvert = wolfvertex(e.dxf.start[0],e.dxf.start[1],e.dxf.start[2])
                    curpoly.add_vertex(myvert)
                    myvert = wolfvertex(e.dxf.end[0],e.dxf.end[1],e.dxf.end[2])
                    curpoly.add_vertex(myvert)
                    
        try :
            wx.LogMessage(_('Number of imported elements : ')+str(nbid))    
        except:
            pass        
            
                
    def find_nearest_vector(self,x,y):
        
        xy=Point(x,y)

        distmin=99999.
        minvec=None
        curzone:zone
        for curzone in self.myzones:
            curvect:vector
            for curvect in curzone.myvectors:
                mynp = curvect.asnparray()
                mp = MultiPoint(mynp)
                near = nearest_points(mp,xy)[0]
                dist = xy.distance(near)
                if dist < distmin:
                    minvec=curvect
                    distmin=dist
        
        return minvec

    def reset_listogl(self):
        for curzone in self.myzones:
            curzone:zone
            if curzone.idgllist!=-99999:
                glDeleteLists(curzone.idgllist,1)
                curzone.idgllist=-99999

    def prep_listogl(self):
        for curzone in self.myzones:
            curzone.plot(True)
        
    def check_plot(self):
        self.plotted = True

    def uncheck_plot(self,unload=True):
        self.plotted = False
    
    def saveas(self,filename=''):
        if filename!='':
            self.filename=filename
            
        if self.filename.endswith('.vecz'):
            self.force3D=True
        
        with open(self.filename, 'w') as f:
            f.write(f'{self.tx} {self.ty}'+'\n')
            f.write(str(self.nbzones)+'\n')
            for curzone in self.myzones:
                curzone.save(f)

        with open(self.filename + '.extra', 'w') as f:
            for curzone in self.myzones:
                curzone.saveextra(f)

    def OnClose(self,e):
        self.Hide()
        pass

    def add_zone(self,addedzone):
        self.myzones.append(addedzone)
        self.nbzones+=1

    def find_minmax(self,update=False):
        
        if update:
            for zone in self.myzones:
                zone.find_minmax(update)

        if len(self.myzones)>0:
            
            minsx=np.asarray([zone.minx for zone in self.myzones])
            minsy=np.asarray([zone.miny for zone in self.myzones])
            maxsx=np.asarray([zone.maxx for zone in self.myzones])
            maxsy=np.asarray([zone.maxy for zone in self.myzones])
            
            if len(minsx)>1:
                self.minx=np.min(minsx[np.where(minsx!=-99999.)])
                self.maxx=np.max(maxsx[np.where(maxsx!=-99999.)])
                self.miny=np.min(minsy[np.where(minsy!=-99999.)])
                self.maxy=np.max(maxsy[np.where(maxsy!=-99999.)])
            else:
                self.minx=minsx[0]
                self.maxx=maxsx[0]
                self.miny=minsy[0]
                self.maxy=maxsy[0]
        else:
            self.minx=0.
            self.miny=0.
            self.maxx=1.
            self.maxy=1.
            
    def plot(self):
        for curzone in self.myzones:
            curzone.plot()

    def select_vectors_from_point(self,x:float,y:float,inside=True):
        curzone:zone
        xmin=1e30
        for curzone in self.myzones:
            xmin = curzone.select_vectors_from_point(x,y,inside)

    def showstructure(self,parent,parentGUI=None):

        self.parent = parent
        self.parentGUI = parent
        if parentGUI is not None:
            self.parentGUI = parentGUI

        if self.init_struct:
            box = BoxSizer(orient=wx.HORIZONTAL)
            
            boxleft = BoxSizer(orient=wx.VERTICAL)
            boxright = BoxSizer(orient=wx.VERTICAL)

            boxadd = BoxSizer(orient=wx.VERTICAL)
            boxdelete = BoxSizer(orient=wx.VERTICAL)
            boxupdown = BoxSizer(orient=wx.HORIZONTAL)
            boxupdownv = BoxSizer(orient=wx.VERTICAL)
            boxupdownz = BoxSizer(orient=wx.VERTICAL)
            
            self.xls=CpGrid(self,-1,wx.WANTS_CHARS)
            self.xls.CreateGrid(10,5)

            self.addrows = wx.Button(self,label=_('Add rows'))
            self.addrows.Bind(wx.EVT_BUTTON,self.Onaddrows)

            self.updatevertices = wx.Button(self,label=_('Update coordinates'))
            self.updatevertices.Bind(wx.EVT_BUTTON,self.Onupdatevertices)

            self.capturevertices = wx.Button(self,label=_('Add'))
            self.capturevertices.Bind(wx.EVT_BUTTON,self.Oncapture)

            self.modifyvertices = wx.Button(self,label=_('Modify'))
            self.modifyvertices.Bind(wx.EVT_BUTTON,self.Onmodify)

            self.dynapar = wx.Button(self,label=_('Add and parallel'))
            self.dynapar.Bind(wx.EVT_BUTTON,self.OncaptureandDynapar)

            self.createapar = wx.Button(self,label=_('Create parallel'))
            self.createapar.Bind(wx.EVT_BUTTON,self.OnAddPar)

            self.sascending = wx.Button(self,label=_('Verify s ascending order'))
            self.sascending.Bind(wx.EVT_BUTTON,self.Onsascending)

            self.insertvertices = wx.Button(self,label=_('Insert'))
            self.insertvertices.Bind(wx.EVT_BUTTON,self.Oninsert)

            self.splitvertices = wx.Button(self,label=_('Split'))
            self.splitvertices.Bind(wx.EVT_BUTTON,self.Onsplit)

            self.interpxyz = wx.Button(self,label=_('Interpolate coords'))
            self.interpxyz.Bind(wx.EVT_BUTTON,self.Oninterpvec)
            
            self.evaluates = wx.Button(self,label=_('Evaluate s'))
            self.evaluates.Bind(wx.EVT_BUTTON,self.Onevaluates)
            
            self.zoomonactive = wx.Button(self,label=_('Zoom on'))
            self.zoomonactive.Bind(wx.EVT_BUTTON,self.Onzoom)            
            
            self.saveimages = wx.Button(self,label=_('Save images from active zone'))
            self.saveimages.Bind(wx.EVT_BUTTON,self.Onsaveimages)

            self.binfrom3 = wx.Button(self,label=_('Create bin from 3 vectors'))
            self.binfrom3.Bind(wx.EVT_BUTTON,self.Oncreatebin)

            self.trifromall = wx.Button(self,label=_('Create tri from all vectors'))
            self.trifromall.Bind(wx.EVT_BUTTON,self.Oncreatemultibin)

            self.polyfrompar = wx.Button(self,label=_('Create polygons from parallels'))
            self.polyfrompar.Bind(wx.EVT_BUTTON,self.Oncreatepolygons)


            boxright.Add(self.xls,1,wx.EXPAND)
            boxright.Add(self.addrows,0,wx.EXPAND)
            boxright.Add(self.capturevertices,0,wx.EXPAND)
            boxright.Add(self.dynapar,0,wx.EXPAND)
            boxright.Add(self.createapar,0,wx.EXPAND)
            boxright.Add(self.modifyvertices,0,wx.EXPAND)
            boxright.Add(self.insertvertices,0,wx.EXPAND)
            boxright.Add(self.splitvertices,0,wx.EXPAND)
            boxright.Add(self.zoomonactive,0,wx.EXPAND)
            boxright.Add(self.sascending,0,wx.EXPAND)
            boxright.Add(self.evaluates,0,wx.EXPAND)
            boxright.Add(self.interpxyz,0,wx.EXPAND)
            boxright.Add(self.updatevertices,0,wx.EXPAND)


            from .wolf_array import Ops_Array            
            if isinstance(self.parent,Ops_Array):        
                self.butgetval = wx.Button(self,label=_('Get values (self array)'))
                self.butgetval.Bind(wx.EVT_BUTTON,self.Ongetvalues)            
                boxright.Add(self.butgetval,0,wx.EXPAND)
        
            self.butgetvallinked = wx.Button(self,label=_('Get values (all arrays)'))
            self.butgetvallinked.Bind(wx.EVT_BUTTON,self.Ongetvalueslinked)            
            self.butgetrefvallinked = wx.Button(self,label=_('Get values (all arrays and remeshing)'))
            self.butgetrefvallinked.Bind(wx.EVT_BUTTON,self.Ongetvalueslinkedandref)            

            boxright.Add(self.butgetvallinked,0,wx.EXPAND)
            boxright.Add(self.butgetrefvallinked,0,wx.EXPAND)

            self.treelist = TreeListCtrl(self,style=TL_CHECKBOX|wx.TR_FULL_ROW_HIGHLIGHT|wx.TR_EDIT_LABELS)
            self.treelist.AppendColumn('Zones')
            self.treelist.Bind(EVT_TREELIST_ITEM_CHECKED, self.OnCheckItem)
            self.treelist.Bind(EVT_TREELIST_ITEM_ACTIVATED, self.OnActivateItem)
            self.treelist.Bind(EVT_TREELIST_ITEM_CONTEXT_MENU,self.OnRDown)

            self.treelist.Bind(wx.EVT_CHAR,self.OnEditLabel)

            self.labelactvect = wx.StaticText( self, wx.ID_ANY, _("None"), style=wx.ALIGN_CENTER_HORIZONTAL )
            self.labelactvect.Wrap( -1 )
            self.labelactvect.SetToolTip(_('Name of the active vector'))
            self.labelactzone = wx.StaticText( self, wx.ID_ANY, _("None"), style=wx.ALIGN_CENTER_HORIZONTAL )
            self.labelactzone.Wrap( -1 )
            self.labelactzone.SetToolTip(_('Name of the active zone'))

            self.addzone = wx.Button(self,label=_('Add zone'))
            self.addvector = wx.Button(self,label=_('Add vector'))
            self.deletezone = wx.Button(self,label=_('Delete zone'))
            self.findactivevector = wx.Button(self,label=_('Find in whole zones'))
            self.findactivevectorcurz = wx.Button(self,label=_('Find in active zone'))
            self.deletevector = wx.Button(self,label=_('Delete vector'))
            
            self.upvector = wx.Button(self,label=_('Up vector'))
            self.downvector = wx.Button(self,label=_('Down vector'))
            self.upzone = wx.Button(self,label=_('Up zone'))
            self.downzone = wx.Button(self,label=_('Down zone'))
            # self.interpolate = wx.Button(self,label=_('Interpolate vector'))

            self.addzone.Bind(wx.EVT_BUTTON,self.OnClickadd_zone)
            self.addvector.Bind(wx.EVT_BUTTON,self.OnClickadd_vector)
            self.deletezone.Bind(wx.EVT_BUTTON,self.OnClickdelete_zone)
            self.deletevector.Bind(wx.EVT_BUTTON,self.OnClickdelete_vector)
            self.upvector.Bind(wx.EVT_BUTTON,self.OnClickup_vector)
            self.downvector.Bind(wx.EVT_BUTTON,self.OnClickdown_vector)

            self.upzone.Bind(wx.EVT_BUTTON,self.OnClickup_zone)
            self.downzone.Bind(wx.EVT_BUTTON,self.OnClickdown_zone)
            
            # self.interpolate.Bind(wx.EVT_BUTTON,self.OnClickInterpolate)
            self.findactivevector.Bind(wx.EVT_BUTTON,self.OnClickfindactivate_vector)
            self.findactivevectorcurz.Bind(wx.EVT_BUTTON,self.OnClickfindactivate_vector2)

            boxadd.Add(self.labelactvect,1,wx.EXPAND)
            boxadd.Add(self.labelactzone,1,wx.EXPAND)
            boxadd.Add(self.addzone,1,wx.EXPAND)
            boxadd.Add(self.addvector,1,wx.EXPAND)
            boxadd.Add(self.findactivevector,1,wx.EXPAND)
            boxadd.Add(self.findactivevectorcurz,1,wx.EXPAND)
            boxdelete.Add(self.deletezone,1,wx.EXPAND)
            boxdelete.Add(self.deletevector,1,wx.EXPAND)
            boxdelete.Add(boxupdown,1,wx.EXPAND)
            
            boxupdown.Add(boxupdownz,1,wx.EXPAND)
            boxupdown.Add(boxupdownv,1,wx.EXPAND)
            
            boxupdownv.Add(self.upvector,1,wx.EXPAND)
            boxupdownv.Add(self.downvector,1,wx.EXPAND)
            boxupdownz.Add(self.upzone,1,wx.EXPAND)
            boxupdownz.Add(self.downzone,1,wx.EXPAND)            
            
            # boxdelete.Add(self.interpolate,1,wx.EXPAND)
            boxdelete.Add(self.saveimages,1,wx.EXPAND)
            boxdelete.Add(self.binfrom3,1,wx.EXPAND)
            boxdelete.Add(self.trifromall,1,wx.EXPAND)
            boxdelete.Add(self.polyfrompar,1,wx.EXPAND)

            boxleft.Add(self.treelist,1,wx.EXPAND)
            boxleft.Add(boxadd,0,wx.EXPAND)
            boxleft.Add(boxdelete,0,wx.EXPAND)

            box.Add(boxleft,1,wx.EXPAND)
            box.Add(boxright,1,wx.EXPAND)

            self.fill_structure()

            self.treelist.SetSize(200,500)
            self.SetSize(400,700)

            self.SetSizer(box)
            
            self.init_struct=False
            
        self.Show()
    
    def fill_structure(self):
        self.treelist.DeleteAllItems()

        root = self.treelist.GetRootItem()
        mynode=self.treelist.AppendItem(root, 'All zones',data=self)
        self.treelist.CheckItem(mynode)
        
        curzone:zone
        for curzone in self.myzones:
            curzone.add2tree(self.treelist,mynode)
            
        self.treelist.Expand(mynode)
        
    def expand_tree(self,objzone=None):
        root = self.treelist.GetRootItem()
        
        curchild = self.treelist.GetFirstChild(root)
        curzone=self.treelist.GetItemData(curchild)
        
        while curchild is not None:
            if curzone is objzone:
                self.treelist.Expand(curchild)
                break
            else:
                curchild=self.treelist.GetNextItem(curchild)        
                curzone=self.treelist.GetItemData(curchild)

    def Oncapture(self,event):
        if self.verify_activevec():
            return
                
        self.parentGUI.action='capture vertices'
        firstvert=wolfvertex(0.,0.)
        self.active_vector.add_vertex(firstvert)
        self.parentGUI.mimicme()
        
    def OnAddPar(self,event:wx.MouseEvent):
        if self.verify_activevec():
            return

        dlg = wx.TextEntryDialog(None,_('Normal distance ? \nd > 0 is right \n d < 0 is left'),value='0.0')
        ret=dlg.ShowModal()
        dist=dlg.GetValue()
        dlg.Destroy()
        try:
            dist = float(dist)
        except:
            wx.LogWarning(_('Bad value -- Retry !'))
            return
        
        self.active_zone.add_parallel(dist)
        self.fill_structure()
        self.find_minmax(True)
        self.expand_tree(self.active_zone)
            
    def OncaptureandDynapar(self,event):
        if self.verify_activevec():
            return
                
        self.parentGUI.action='dynamic parallel'
        
        firstvert=wolfvertex(0.,0.)
        self.active_vector.add_vertex(firstvert)
            
        self.parentGUI.mimicme()

    def Onsascending(self,e):
        correct,wherec= self.active_vector.verify_s_ascending()
        self.xls_active_vector()
        
        if self.parentGUI is not None:
            if correct:
                msg=_('Modification on indices :\n')
                for curi in wherec:
                    msg+= str(curi)+'<-->'+str(curi+1)+'\n'
                dlg=wx.MessageDialog(None,msg)
                dlg.ShowModal()
    
    def Onmodify(self,event):
        self.parentGUI.action='modify vertices'
        self.parentGUI.mimicme()
        
        self.active_zone.idgllist=-99999

    def Onzoom(self,event):
        self.parentGUI.zoomon_activevector()

    def Ongetvalues(self,e:wx.EVT_BUTTON):
        from .wolf_array import Ops_Array
        
        if isinstance(self.parent,Ops_Array):        
            self.active_vector.get_values_on_vertices(self.parent.parentarray)
            self.active_vector.fillgrid(self.xls)
        else:
            curarray = self.parentGUI.active_array
            if curarray is not None:
                self.active_vector.get_values_on_vertices(curarray)
                self.active_vector.fillgrid(self.xls)
            else:
                wx.LogMessage(_('Please actived the desired array'))

    def Ongetvalueslinked(self,e:wx.EVT_BUTTON):
        
        linked,labels=self.parentGUI.get_linked_arrays()
        
        if len(linked)>0:
            newzone:zone
            newzone=self.active_vector.get_values_linked(linked,labels,False)
            
            self.add_zone(newzone)
            newzone.parent=self
            
            self.fill_structure()
            
    def Ongetvalueslinkedandref(self,e:wx.EVT_BUTTON):
        linked,labels=self.parentGUI.get_linked_arrays()
        
        if len(linked)>0:
            newzone:zone
            newzone=self.active_vector.get_values_linked(linked,labels)
            
            self.add_zone(newzone)
            newzone.parent=self
            
            self.fill_structure()

    def Onsaveimages(self,event):
        self.save_images_fromvec()  
        
    def Oncreatepolygons(self,event):
        curz = self.active_zone
        
        if curz.nbvectors!=3:
            raise NameError(_('The active zone must contain 3 vectors and only 3'))
        
        dlg=wx.NumberEntryDialog(None,_('What is the desired longitudinal size [cm] ?'),'ds','ds size',500,1,10000)
        ret=dlg.ShowModal()
        if ret==wx.ID_CANCEL:
            dlg.Destroy()
            return
        
        ds=float(dlg.GetValue())/100.
        dlg.Destroy()
        
        dlg=wx.NumberEntryDialog(None,_('How many polygons ? \n\n 1 = one large polygon from left to right\n 2 = two polygons - one left and one right'),'Number','Polygons',1,1,2)
        ret=dlg.ShowModal()
        if ret==wx.ID_CANCEL:
            dlg.Destroy()
            return

        nb=int(dlg.GetValue())
        dlg.Destroy()

        self.active_zone.create_polygon_from_parallel(ds,nb)

    def Oncreatebin(self,event):
        
        curz = self.active_zone
        
        if curz.nbvectors!=3:
            raise NameError(_('The active zone must contain 3 vectors and only 3'))
        
        dlg=wx.MessageDialog(None,_('Would you like to copy the center elevations to the parallel sides ?'),style=wx.YES_NO)
        ret=dlg.ShowModal()
        if ret==wx.ID_YES:
            left:LineString
            center:LineString
            right:LineString
            
            left = curz.myvectors[0].asshapely_ls()
            center = curz.myvectors[1].asshapely_ls()
            right = curz.myvectors[2].asshapely_ls()

            for idx,coord in enumerate(left.coords):
                xy = Point(coord[0],coord[1])
                curs = left.project(xy,True)
                curz.myvectors[0].myvertices[idx].z=center.interpolate(curs,True).z

            for idx,coord in enumerate(right.coords):
                xy = Point(coord[0],coord[1])
                curs = right.project(xy,True)
                curz.myvectors[2].myvertices[idx].z=center.interpolate(curs,True).z
        
        dlg.Destroy()

        left:LineString
        center:LineString
        right:LineString
        
        left = curz.myvectors[0].asshapely_ls()
        center = curz.myvectors[1].asshapely_ls()
        right = curz.myvectors[2].asshapely_ls()
               
        dlg=wx.NumberEntryDialog(None,_('What is the desired lateral size [cm] ?'),'ds','ds size',500,1,10000.)
        ret=dlg.ShowModal()
        if ret==wx.ID_CANCEL:
            dlg.Destroy()
            return
        
        addedz=float(dlg.GetValue())/100.
        dlg.Destroy()

        dlg=wx.NumberEntryDialog(None,_('How many points along center polyline ?')+'\n'+
                                    _('Length size is {} meters').format(center.length),'nb','dl size',100,1,10000.)
        ret=dlg.ShowModal()
        if ret==wx.ID_CANCEL:
            dlg.Destroy()
            return
        
        nb=int(dlg.GetValue())
        dlg.Destroy()
            
        s = np.linspace(0.,1.,num=nb,endpoint=True)                
        points=np.zeros((5*nb,3),dtype=np.float32)
        
        decal=0
        for curs in s:

            ptl=left.interpolate(curs,True)
            ptc=center.interpolate(curs,True)
            ptr=right.interpolate(curs,True)
 
            points[0+decal,:] = np.asarray([ptl.coords[0][0],ptl.coords[0][1],ptl.coords[0][2]])
            points[1+decal,:] = np.asarray([ptl.coords[0][0],ptl.coords[0][1],ptl.coords[0][2]])
            points[2+decal,:] = np.asarray([ptc.coords[0][0],ptc.coords[0][1],ptc.coords[0][2]])
            points[3+decal,:] = np.asarray([ptr.coords[0][0],ptr.coords[0][1],ptr.coords[0][2]])
            points[4+decal,:] = np.asarray([ptr.coords[0][0],ptr.coords[0][1],ptr.coords[0][2]])
            
            points[0+decal,2] += addedz
            points[4+decal,2] += addedz
            
            decal+=5
                            
        decal=0
        triangles=[]
        
        nbpts=5
        triangles.append([[i+decal,i+decal+1,i+decal+nbpts] for i in range(nbpts-1)])
        triangles.append([[i+decal+nbpts,i+decal+1,i+decal+nbpts+1] for i in range(nbpts-1)])

        for k in range(1,nb-1):
            decal=k*nbpts
            triangles.append([ [i+decal,i+decal+1,i+decal+nbpts] for i in range(nbpts-1)])
            triangles.append([ [i+decal+nbpts,i+decal+1,i+decal+nbpts+1] for i in range(nbpts-1)])
        triangles=np.asarray(triangles,dtype=np.uint32).reshape([(2*nbpts-2)*(nb-1),3])

        mytri=Triangulation(pts=points,tri=triangles)
        mytri.find_minmax(True)
        fn=mytri.export_to_gltf()

        dlg=wx.MessageDialog(None,_('Would you like to add triangulation to parent gui ?'),style=wx.YES_NO)
        ret=dlg.ShowModal()
        if ret==wx.ID_YES:
            
            self.parentGUI.add_object('triangulation',newobj=mytri)

        dlg.Destroy()

    def Oncreatemultibin(self,event):
        
        myzone = self.active_zone
        myls = []
        for curv in myzone.myvectors:
            myls.append(curv.asshapely_ls())        
               
        dlg=wx.NumberEntryDialog(None,_('How many points along polylines ?')+'\n'+
                                    _('Length size is {} meters').format(myls[0].length),'nb','dl size',100,1,10000.)
        ret=dlg.ShowModal()
        if ret==wx.ID_CANCEL:
            dlg.Destroy()
            return
        
        nb=int(dlg.GetValue())
        dlg.Destroy()
            
        s = np.linspace(0.,1.,num=nb,endpoint=True)                
        points=np.zeros((nb*myzone.nbvectors,3),dtype=np.float64)
        
        decal=0
        for curs in s:

            pt = [curls.interpolate(curs,True) for curls in myls]
 
            for k in range(myzone.nbvectors):
                xyz=pt[k].coords[0]
                points[k+decal,:] = np.asarray([xyz[0],xyz[1],xyz[2]])
                        
            decal+=myzone.nbvectors
                            
        decal=0
        triangles=[]
        
        nbpts=myzone.nbvectors
        triangles.append([[i+decal,i+decal+1,i+decal+nbpts] for i in range(nbpts-1)])
        triangles.append([[i+decal+nbpts,i+decal+1,i+decal+nbpts+1] for i in range(nbpts-1)])

        for k in range(1,nb-1):
            decal=k*nbpts
            triangles.append([ [i+decal,i+decal+1,i+decal+nbpts] for i in range(nbpts-1)])
            triangles.append([ [i+decal+nbpts,i+decal+1,i+decal+nbpts+1] for i in range(nbpts-1)])
        triangles=np.asarray(triangles,dtype=np.uint32).reshape([(2*nbpts-2)*(nb-1),3])

        mytri=Triangulation(pts=points,tri=triangles)
        mytri.find_minmax(True)

        self.parentGUI.add_object('triangulation',newobj=mytri)

    def save_images_fromvec(self,dir=''):
        if dir=='':
            dlg = wx.DirDialog(None,"Choose directory to store images",style=wx.FD_SAVE)
            ret=dlg.ShowModal()
            
            if ret==wx.ID_CANCEL:
                return
            
            dir = dlg.GetPath()
        
        for curzone in self.myzones:        
            for curvec in curzone.myvectors:
                curvec:vector
                if curvec.nbvertices>1:                
                    oldwidth=curvec.myprop.width
                    curvec.myprop.width=4
                    myname = curvec.myname

                    self.Activate_vector(curvec)
                    
                    if self.parentGUI.linked:
                        for curview in self.parentGUI.linkedList:
                            title = curview.GetTitle()
                            curview.zoomon_activevector()           
                            fn = path.join(dir,title + '_' + myname+'.png')
                            curview.save_canvasogl(fn)
                    else:
                        self.parentGUI.zoomon_activevector()           
                        fn = path.join(dir,myname+'.png')
                        self.parentGUI.save_canvasogl(fn)
                        
                        fn = path.join(dir,'palette_v_' + myname+'.png')
                        self.parentGUI.active_array.mypal.export_image(fn,'v')
                        fn = path.join(dir,'palette_h_' + myname+'.png')
                        self.parentGUI.active_array.mypal.export_image(fn,'h')
                        
                    curvec.myprop.width = oldwidth
            
    def Oninsert(self,event):
        self.parentGUI.action='insert vertices'
        self.parentGUI.mimicme()
        
        self.active_zone.idgllist=-99999
        
    def Onsplit(self,event:wx.MouseEvent):
        
        dlg=wx.NumberEntryDialog(None,_('What is the desired longitudinal size [cm] ?'),'ds','ds size',100,1,100000.)
        ret=dlg.ShowModal()
        if ret==wx.ID_CANCEL:
            dlg.Destroy()
            return
        
        ds=float(dlg.GetValue())/100.
        dlg.Destroy()

        self.active_vector.split(ds)
        
    def Onevaluates(self,event:wx.MouseEvent):
        
        curv:vector
        curv = self.active_vector
        curv.update_lengths()
        
        dlg = wx.SingleChoiceDialog(None, "Which mode?", "How to evaluate lengths?", ['2D','3D'])
        ret=dlg.ShowModal()
        if ret==wx.ID_CANCEL:
            dlg.Destroy()
            return
        
        method=dlg.GetStringSelection()
        dlg.Destroy()
        
        self.xls.SetCellValue(0,4,'0.0')
        s=0.
        if method=='2D':
            for k in range(curv.nbvertices-1):
                s+=curv._lengthparts2D[k]
                self.xls.SetCellValue(k+1,4,str(s))
        else:
            for k in range(curv.nbvertices-1):
                s+=curv._lengthparts3D[k]
                self.xls.SetCellValue(k+1,4,str(s))

    def Oninterpvec(self,event:wx.MouseEvent):

        curv:vector
        curv = self.active_vector
        
        s=[]
        z=[]
        
        for k in range(curv.nbvertices):
            zgrid = self.xls.GetCellValue(k,2)
            sgrid = self.xls.GetCellValue(k,4)
            if zgrid!='' and float(zgrid)!=-99999.:
                z.append(float(zgrid))
                s.append(float(sgrid))

        if len(z)==0:
            return
                    
        f = interp1d(s,z)

        for k in range(curv.nbvertices):
            zgrid = self.xls.GetCellValue(k,2)
            sgrid = self.xls.GetCellValue(k,4)
            if zgrid=='' or float(zgrid)==-99999.:
                z = f(float(sgrid))
                self.xls.SetCellValue(k,2,str(z))

    def Onupdatevertices(self,event):
        if self.verify_activevec():
            return
        
        self.active_vector.updatefromgrid(self.xls)
        self.find_minmax(True)

    def Onaddrows(self,event):
        nbrows=None
        dlg=wx.TextEntryDialog(None,_('How many rows?'),value='1')
        while nbrows is None:
            rc = dlg.ShowModal()
            if rc == wx.ID_OK:
                nbrows = int(dlg.GetValue())
                self.xls.AppendRows(nbrows)
            else:
                return        

    def OnClickadd_zone(self,event):
        curname=None
        dlg=wx.TextEntryDialog(None,_('Choose a name for the new zone'),value='New_Zone')
        while curname is None:
            rc = dlg.ShowModal()
            if rc == wx.ID_OK:
                curname = str(dlg.GetValue())
                newzone = zone(name=curname,parent=self)
                self.add_zone(newzone)
                self.fill_structure()
                self.active_zone = newzone
            else:
                return
        
    def OnClickadd_vector(self,event):
        curname=None
        dlg=wx.TextEntryDialog(None,_('Choose a name for the new vector'),value='New_Vector')
        while curname is None:
            rc = dlg.ShowModal()
            if rc == wx.ID_OK:
                curname = str(dlg.GetValue())
                newvec = vector(name=curname,parentzone=self.active_zone)
                self.active_zone.add_vector(newvec)
                self.fill_structure()
                self.Activate_vector(newvec)                
            else:
                return

    def OnClickdelete_zone(self,event):
        curname=self.active_zone.myname
        r = wx.MessageDialog(
            None,
            _('The zone {n} will be deleted. Continue?').format(n=curname),
            style=wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION
        ).ShowModal()

        if r != wx.ID_YES:
            return

        self.myzones.pop(int(self.myzones.index(self.active_zone)))
        self.nbzones-=1
        self.fill_structure()
        self.find_minmax(True)

    def OnClickfindactivate_vector(self,event):
        if self.parentGUI is not None:
            
            dlg=wx.MessageDialog(None,"Search only closed polyline?",style=wx.YES_NO)
            ret=dlg.ShowModal()
            if ret==wx.YES:
                self.parentGUI.action = 'select active vector inside'
            else:
                self.parentGUI.action = 'select active vector all'
            self.parentGUI.active_zones=self

    def OnClickfindactivate_vector2(self,event):
        if self.parentGUI is not None:
            dlg=wx.MessageDialog(None,"Search only closed polyline?",style=wx.YES_NO)
            ret=dlg.ShowModal()
            if ret==wx.YES:
                self.parentGUI.action = 'select active vector2 inside'
            else:
                self.parentGUI.action = 'select active vector2 all'

            self.parentGUI.active_zone=self.active_zone
            self.parentGUI.active_zones=self
            
    def get_selected_vectors(self,all=False):
        curzone:zone
        if all:
            mylist=[]
            for curzone in self.myzones:
                ret = curzone.get_selected_vectors(all)
                if ret is not None:                    
                    mylist.append(ret)
            return mylist
        else:
            distmin=99999.
            vecmin = None
            for curzone in self.myzones:
                ret = curzone.get_selected_vectors()
                if ret is not None:                    
                    if ret[1]<distmin:
                        distmin= ret[1]
                        vecmin = ret[0]
                
            return vecmin

    def verify_activevec(self):
        msg=''
        if self.active_vector is None:
            msg+=_('Active vector is None\n')            
            msg+=_('\n')
            msg+=_('Retry !\n')
            wx.MessageBox(msg)
            return True
         
        return False

    def OnClickdelete_vector(self,event):
        if self.verify_activevec():
            return
        
        curname=self.active_vector.myname
        r = wx.MessageDialog(
            None,
            _('The vector {n} will be deleted. Continue?').format(n=curname),
            style=wx.YES_NO | wx.ICON_QUESTION
        ).ShowModal()

        if r != wx.ID_YES:
            return

        actzone =self.active_zone
        actzone.myvectors.pop(int(actzone.myvectors.index(self.active_vector)))
        actzone.nbvectors-=1
        self.fill_structure()
        self.find_minmax(True)
        
    def OnClickup_vector(self,event):
        
        for idx,curv in enumerate(self.active_zone.myvectors):
            
            if curv == self.active_vector:
                if idx==0:
                    return
                self.active_zone.myvectors.pop(idx)
                self.active_zone.myvectors.insert(idx-1,curv)
                
                self.fill_structure()
                
                break

    def OnClickdown_vector(self,event):
        for idx,curv in enumerate(self.active_zone.myvectors):
            
            if curv == self.active_vector:
                if idx==self.active_zone.nbvectors:
                    return
                self.active_zone.myvectors.pop(idx)
                self.active_zone.myvectors.insert(idx+1,curv)
                
                self.fill_structure()
                
                break

    def OnClickup_zone(self,event):
        
        for idx,curz in enumerate(self.myzones):
            
            if curz == self.active_zone:
                if idx==0:
                    return
                self.myzones.pop(idx)
                self.myzones.insert(idx-1,curz)
                
                self.fill_structure()
                
                break

    def OnClickdown_zone(self,event):
        for idx,curz in enumerate(self.myzones):
            
            if curz == self.active_zone:
                if idx==self.nbzones:
                    return
                self.myzones.pop(idx)
                self.myzones.insert(idx+1,curz)
                
                self.fill_structure()
                
                break

    def unuse(self):
        for curzone in self.myzones:
            curzone.unuse()

    def use(self):
        for curzone in self.myzones:
            curzone.use()

    def OnCheckItem(self,event):

        myitem=event.GetItem()
        check = self.treelist.GetCheckedState(myitem)
        myitemdata=self.treelist.GetItemData(myitem)
        if check:
            myitemdata.use()
        else:
            myitemdata.unuse()

    def OnRDown(self,event):
        if self.verify_activevec():
            return
                
        self.active_vector.myprop.show()

    def OnActivateItem(self,event:TreeListEvent):
        myitem=event.GetItem()
        myitemdata=self.treelist.GetItemData(myitem)
        
        if isinstance(myitemdata,vector):
            self.Activate_vector(myitemdata)         
        elif isinstance(myitemdata,zone):
            self.Activate_zone(myitemdata)
            
        self.last_active = myitemdata
        
    def Activate_vector(self,object:vector):
        self.active_vector = object
        self.xls_active_vector()
        
        if object.parentzone is not None:
            self.active_zone = object.parentzone
            object.parentzone.active_vector = object

        if self.parent is not None:
            self.parent.Active_vector(self.active_vector)

        self.labelactvect.SetLabel(self.active_vector.myname)
        self.labelactzone.SetLabel(self.active_zone.myname)
        self.Layout()

    def Activate_zone(self,object:zone):
        self.active_zone = object
        if object.active_vector is not None:
            self.active_vector = object.active_vector
        elif object.nbvectors>0:
            self.Activate_vector(object.myvectors[0])
    
        self.labelactvect.SetLabel(self.active_vector.myname)
        self.labelactzone.SetLabel(self.active_zone.myname)

    def xls_active_vector(self):
        self.xls.ClearGrid()
        self.active_vector.fillgrid(self.xls)        

    def OnEditLabel(self,event):
        key=event.GetKeyCode()

        if key==wx.WXK_F2:
            if self.last_active is not None:        
                curname=None
                dlg=wx.TextEntryDialog(None,_('Choose a new name'),value=self.last_active.myname)
                while curname is None:
                    rc = dlg.ShowModal()
                    if rc == wx.ID_OK:
                        curname = str(dlg.GetValue())
                        self.last_active.myname = curname
                        self.fill_structure()
                    else:
                        return

    def add_interpolators(self,myinterpolators):
        myinterpolators:Interpolators
        curinterp:Interpolator
        
        zonesinterp=Zones(parent=self.parent)

        id=0
        points=[]
        triangles=[]
        decal=0
        for curinterp in myinterpolators.myinterp:
            id+=1
            
            myzone = zone(name='Interpolator'+str(id),parent=zonesinterp,is2D=False)
            myzone.used=False
            zonesinterp.add_zone(myzone)
            curinterp.add_triangles_to_zone(myzone)

            nbpts,pts,tr=curinterp.get_triangles()
                        
            points.append(pts)
            triangles.append(tr+decal)
            decal+=nbpts

        curinterp.export_gltf(np.concatenate(points),np.concatenate(triangles))

        try:
            self.fill_structure()
        except:
            pass
        
        return zonesinterp

class Grid(Zones):

    def __init__(self, size:float=1000.,ox:float=0.,oy:float=0.,ex:float=1000.,ey:float=1000., parent=None):
        super().__init__(ox=ox, oy=oy, parent=parent)

        mygrid=zone(name='mygrid',parent=self)
        self.add_zone(mygrid)
        mygridx=vector(name='mygridx')
        mygridy=vector(name='mygridy')
        contour=vector(name='contour')
        mygrid.add_vector(mygridx)
        mygrid.add_vector(mygridy)
        mygrid.add_vector(contour)
        self.creategrid(size,ox,oy,ex,ey)

    def creategrid(self,size:float=100.,ox:float=0.,oy:float=0.,ex:float=1000.,ey:float=1000.):

        mygridx=self.myzones[0].myvectors[0]
        mygridy=self.myzones[0].myvectors[1]
        contour=self.myzones[0].myvectors[2]
        mygridx.reset()
        mygridy.reset()
        contour.reset()

        locox=int(ox/size)*size
        locoy=int(oy/size)*size
        locex=(np.ceil(ex/size))*size
        locey=(np.ceil(ey/size))*size

        nbx=int(np.ceil((locex-locox)/size))
        nby=int(np.ceil((locey-locoy)/size))

        dx=locex-locox
        dy=locey-locoy

        #grillage vertical        
        xloc=locox
        yloc=locoy
        for i in range(nbx):
            newvert=wolfvertex(xloc,yloc)
            mygridx.add_vertex(newvert)
            
            yloc+=dy
            newvert=wolfvertex(xloc,yloc)
            mygridx.add_vertex(newvert)
            
            xloc+=size
            dy=-dy

        #grillage horizontal        
        xloc=locox
        yloc=locoy
        for i in range(nby):
            newvert=wolfvertex(xloc,yloc)
            mygridy.add_vertex(newvert)
            
            xloc+=dx
            newvert=wolfvertex(xloc,yloc)
            mygridy.add_vertex(newvert)
            
            yloc+=size
            dx=-dx

        newvert=wolfvertex(locox,locoy)
        contour.add_vertex(newvert)
        newvert=wolfvertex(locex,locoy)
        contour.add_vertex(newvert)
        newvert=wolfvertex(locex,locey)
        contour.add_vertex(newvert)
        newvert=wolfvertex(locox,locey)
        contour.add_vertex(newvert)

        self.find_minmax(True)
                
class Interpolator():
    '''
    Objet d'interpolation sur sections en travers
    
        - self.interpolants est une liste de listes
        - chaque élément de self.interpolants est également une liste de listes
        - chaque liste de self.interpolants[k] contient les wolfvertex de la section discrétisée
    
    '''
    
    def __init__(self,vec1:vector,vec2:vector,supports:list,ds=1.) -> None:
        
        self.interpolants=[]
        
        sect1={}
        sect2={}
        
        #Linestrings shapely des sections 1 et 2
        #ATTENTION, SHAPELY est une librairie géométrique 2D --> des outils spécifiques ont été programmés pour faire l'interpolation 3D
        s1=sect1['ls']=vec1.asshapely_ls()
        s2=sect2['ls']=vec2.asshapely_ls()
        
        nb = 0
        supls={}

        eps=5.e-2

        for curvec in supports:
            #linestring du support courant
            #distances des intersections des sections sur le support           
            myls:LineString
            myls=curvec.asshapely_ls()
            
            #intersections du vecteur support avec les sections
            i1=myls.intersects(s1)
            if not i1:
                pt=Point(s1.xy[0][0],s1.xy[1][0])
                pt1=myls.interpolate(myls.project(pt))
                length = pt1.distance(pt)
                i1 = length<eps

                if i1:
                    vec1.myvertices[0].x=pt1.xy[0][0]
                    vec1.myvertices[0].y=pt1.xy[1][0]
                    s1=vec1.asshapely_ls()

                if not i1:
                    pt=Point(s1.xy[0][-1],s1.xy[1][-1])
                    pt1=myls.interpolate(myls.project(pt))
                    length = pt1.distance(pt)
                    i1 = length<eps
                    if i1:
                        vec1.myvertices[-1].x=pt1.xy[0][-1]
                        vec1.myvertices[-1].y=pt1.xy[1][-1]
                        s1=vec1.asshapely_ls()

            i2=myls.intersects(s2)
            if not i2:
                pt=Point(s2.xy[0][0],s2.xy[1][0])
                pt2=myls.interpolate(myls.project(pt))
                length = pt2.distance(Point(s2.xy[0][0],s2.xy[1][0]))
                i2 = length<eps

                if i2:
                    vec2.myvertices[0].x=pt2.xy[0][0]
                    vec2.myvertices[0].y=pt2.xy[1][0]
                    s2=vec2.asshapely_ls()

                if not i2:
                    pt=Point(s2.xy[0][-1],s2.xy[1][-1])
                    pt2=myls.interpolate(myls.project(pt))
                    length = pt2.distance(pt)
                    i2 = length<eps
                    if i2:
                        vec2.myvertices[-1].x=pt2.xy[0][-1]
                        vec2.myvertices[-1].y=pt2.xy[1][-1]
                        s2=vec2.asshapely_ls()

            if i1 and i2:
                supls[nb]={}
                supls[nb]['ls']=myls
                supls[nb]['vec']=curvec    
                nb+=1

        #bouclage sur les vecteurs supports pour trouver les intersections avec les sections
        #  - trouver la portion utile entre intersections des supports
        #  - trouver les distances sur les sections de ces intersections
        for k in range(nb):
            #linestring du support courant
            #distances des intersections des sections sur le support           
            myls:LineString
            myls=supls[k]['ls']
            
            #intersections du vecteur support avec les sections
            
            #section amont
            i1=myls.intersection(s1)
            if i1.geom_type=='MultiPoint':
                i1=i1.geoms[0]
            
            #section aval
            i2=myls.intersection(s2)
            if i2.geom_type=='MultiPoint':
                i2=i2.geoms[0]

            #Les distances, sur les sections, sont calculées en projetant l'intersection du vecteur support et des sections
            sect1[k]=s1.project(i1)
            sect2[k]=s2.project(i2)

            #Les distances, sur le support, sont calculées en projetant l'intersection du vecteur support et des sections
            supls[k][1]=myls.project(i1)
            if supls[k][1]==-1.:
                #problème de précision de calcul
                if myls.distance(Point(s1.xy[0][0],s1.xy[1][0]))<eps:
                    supls[k][1]=myls.project(Point(s1.xy[0][0],s1.xy[1][0]))
                    sect1[k]=s1.project(Point(s1.xy[0][0],s1.xy[1][0]))
                elif myls.distance(Point(s1.xy[0][-1],s1.xy[1][-1]))<eps:
                    supls[k][1]=myls.project(Point(s1.xy[0][-1],s1.xy[1][-1]))
                    sect1[k]=s1.project(Point(s1.xy[0][-1],s1.xy[1][-1]))

            supls[k][2]=myls.project(i2)
            if supls[k][2]==-1.:
                #problème de précision de calcul
                if myls.distance(Point(s2.xy[0][0],s2.xy[1][0]))<eps:
                    supls[k][2]=myls.project(Point(s2.xy[0][0],s2.xy[1][0]))
                    sect2[k]=s2.project(Point(s2.xy[0][0],s2.xy[1][0]))
                elif myls.distance(Point(s2.xy[0][-1],s2.xy[1][-1]))<eps:
                    supls[k][2]=myls.project(Point(s2.xy[0][-1],s2.xy[1][-1]))
                    sect2[k]=s2.project(Point(s2.xy[0][-1],s2.xy[1][-1]))
                        
            #on ne conserve que la fraction utile entre intersections
            supls[k]['vec']=supls[k]['vec'].substring(supls[k][1],supls[k][2],False,False)

        #bouclage sur les intervalles --> nb_supports-1
        for k in range(nb-1):
            interpolant=[]
            self.interpolants.append(interpolant)

            cursupl:vector
            cursupr:vector
            curvec1:vector
            curvec2:vector

            #morceaux de sections entre intersections avec le support
            curvec1=sect1['sub'+str(k)]=vec1.substring(sect1[k],sect1[k+1],is3D=False,adim=False)
            curvec2=sect2['sub'+str(k)]=vec2.substring(sect2[k],sect2[k+1],is3D=False,adim=False)
            
            #pointeurrs vers les morceaux des supports
            cursupl = supls[k]['vec']
            cursupr = supls[k+1]['vec']

            #MAJ des longueurs 2D et 3D
            cursupl.update_lengths()
            cursupr.update_lengths()
            curvec1.update_lengths()
            curvec2.update_lengths()
                
            #Trouve la liste des distances à traiter pour le maillage
            nbi = np.ceil(max(curvec1.length3D,curvec2.length3D)/ds)
            locds = 1./float(nbi)
            dist3d = np.concatenate([np.arange(0.,1.,locds),np.cumsum(curvec1._lengthparts3D)/curvec1.length3D,np.cumsum(curvec2._lengthparts3D)/curvec2.length3D])
            dist3d = np.unique(dist3d)
            
            #nombre de points à traiter sur les supports
            # on divise la longueur 3D des supports par la taille souhaitée et on arrondi à l'entier supérieur
            nbi = int(np.ceil(max(cursupl.length3D,cursupr.length3D)/ds))
            # nouvelle distance de calcul
            locds = 1./float(nbi)
                    
            sloc=0.
            pt1l = curvec1.interpolate(0.,True,True)
            pt2l = curvec2.interpolate(0.,True,True)
            pt1r = curvec1.interpolate(1.,True,True)
            pt2r = curvec2.interpolate(1.,True,True)
            
            s1dr = vector(name='sectiondroite1')
            s2dr = vector(name='sectiondroite2')
            s1dr.add_vertex([pt1l,pt1r])
            s2dr.add_vertex([pt2l,pt2r])
            
            s1dr = s1dr.asshapely_ls()
            s2dr = s2dr.asshapely_ls()
            
            # if np.isnan(pt1l.x):
            #     a=1
            # if np.isnan(pt2l.x):
            #     a=1
            # if np.isnan(pt1r.x):
            #     a=1
            # if np.isnan(pt2r.x):
            #     a=1
            
            for curalong in range(nbi+1):
                print(str(curalong))
                
                #interpolation 3D sur les 2 supports                
                l1 = cursupl.interpolate(sloc,True,True)
                l2 = cursupr.interpolate(sloc,True,True)
                
                curvec=vector(name='loc')
                curvec.add_vertex([l1,l2])
                val = []

                if l1.z!=0.:
                    if pt1l.z==0.:
                        alpha1l=0.
                    else:
                        alpha1l = l1.z/pt1l.z
                    if pt2l.z==0.:
                        alpha2l=0.
                    else:
                        alpha2l = l1.z/pt2l.z
                else:
                    alpha1l = 0.
                    alpha2l = 0.
                if l2.z!=0.:
                    if pt1r.z==0.:
                        alpha1r = 0.
                    else:
                        alpha1r = l2.z/pt1r.z
                    
                    if pt2r.z==0.:
                        alpha2r = 0.
                    else:
                        alpha2r = l2.z/pt2r.z
                else:
                    alpha1r=0.
                    alpha2r=0.

                for curdist in dist3d:
                    
                    #interpolation 3D dans les 2 sections                   
                    cur1 = curvec1.interpolate(curdist,True,True)
                    cur2 = curvec2.interpolate(curdist,True,True)

                    alpha1 = alpha1l*(1.-curdist)+alpha1r*curdist
                    alpha2 = alpha2l*(1.-curdist)+alpha2r*curdist

                    sr1 = s1dr.project(Point(cur1.x,cur1.y)) 
                    sr2 = s2dr.project(Point(cur2.x,cur2.y))
                    pr1 = s1dr.interpolate(sr1) 
                    pr2 = s2dr.interpolate(sr2)
                    sr1/=s1dr.length
                    sr2/=s2dr.length
                    
                    dx1 = cur1.x-pr1.x 
                    dy1 = cur1.y-pr1.y 
                    dx2 = cur2.x-pr2.x 
                    dy2 = cur2.y-pr2.y 
                    dx = dx1*(1.-sloc)+dx2*sloc
                    dy = dy1*(1.-sloc)+dy2*sloc
                    s = sr1*(1.-sloc)+sr2*sloc
                    
                    # dist2d1 = cur1.dist2D(curvec1.myvertices[0])/curvec1.myvertices[0].dist2D(curvec1.myvertices[-1]) #curvec1.length2D
                    # dist2d2 = cur2.dist2D(curvec2.myvertices[0])/curvec2.myvertices[0].dist2D(curvec2.myvertices[-1]) #curvec2.length2D
                    # dist2d  = dist2d1*(1.-sloc) + dist2d2*sloc
                    # pt = curvec.interpolate(dist2d,False,True)
                    pt = curvec.interpolate(s,False,True)

                    # xloc = cur1.x + sloc * (cur2.x-cur1.x)
                    # yloc = cur1.y + sloc * (cur2.y-cur1.y)
                    zloc = cur1.z*alpha1 + sloc * (cur2.z*alpha2-cur1.z*alpha1)
                    
                    val.append(wolfvertex(pt.x+dx,pt.y+dy,zloc))
                    # val.append(wolfvertex(xloc,yloc,zloc))

                interpolant.append(val)
                
                sloc+=locds
                sloc=min(sloc,1.)

    def get_xyz_for_viewer(self,nbsub=10):
        
        pts=self.interpolants
        
        nb=0
        for curpt in pts:
            for curl in curpt:
                nb+=(len(curpt)-1)*(len(curl)-1)*3+(len(curl)-1)+(len(curpt))

        pond=np.arange(0.,1.,1./float(nbsub))
        xyz=np.ones([(nb-1)*nbsub,4],order='F')
        start=0
        for curpt in pts:           
            for k in range(len(curpt)-1):
                curl=curpt[k]
                nextl=curpt[k+1]
                for i in range(len(curl)-1):
                    v1=curl[i].getcoords()
                    v2=curl[i+1].getcoords()
                    v3=nextl[i].getcoords()
                    
                    xyz[start:start+nbsub,:3]=[v1+(v2-v1)*curpond for curpond in pond] 
                    start+=nbsub
                    xyz[start:start+nbsub,:3]= [v2+(v3-v2)*curpond for curpond in pond] 
                    start+=nbsub
                    xyz[start:start+nbsub,:3]= [v3+(v1-v3)*curpond for curpond in pond]
                    start+=nbsub
            
            curl=curpt[-1]
            for i in range(len(curl)-1):
                v1=curl[i].getcoords()
                v2=curl[i+1].getcoords()               
                xyz[start:start+nbsub,:3]=[v1+(v2-v1)*curpond for curpond in pond] 
                start+=nbsub
            for k in range(len(curpt)-1):
                curl=curpt[k]
                nextl=curpt[k+1]
                v1=curl[-1].getcoords()
                v3=nextl[-1].getcoords()                
                xyz[start:start+nbsub,:3]=[v1+(v3-v1)*curpond for curpond in pond] 
                start+=nbsub   
                
        return xyz

    def add_triangles_to_zone(self,myzone:zone):
        
        nb=0
        npt=1
        for curpt in self.interpolants:
            for k in range(len(curpt)-1):
                curl=curpt[k]
                nextl=curpt[k+1]
                for i in range(len(curl)-1):
                    curvec = vector(name='tr'+'_'+str(npt)+'_'+str(k)+'_'+str(i),parentzone=myzone)                
                    curvec.add_vertex([curl[i],curl[i+1],nextl[i]])
                    curvec.close_force()
                    curvec.myprop.used=False
                    myzone.add_vector(curvec)
                    
                    curvec = vector(name='tr'+'_'+str(npt)+'_'+str(k+1)+'_'+str(i),parentzone=myzone)                
                    curvec.add_vertex([nextl[i],curl[i+1],nextl[i+1]])
                    curvec.close_force()
                    curvec.myprop.used=False
                    myzone.add_vector(curvec)
                
            npt+=1
            nb+=(len(curpt)-1)*(len(curl)-1)*3+(len(curl)-1)+(len(curpt))

    def get_triangles(self,forgltf=True):
        
        points=[]
        triangles=[]
        nbpts=0
        nbtr=0
        for curpt in self.interpolants:

            nb_points_perline = len(curpt[0])
            nbsect=len(curpt)
            if forgltf:
                pointsloc=[[pt.x,pt.z,-pt.y] for curl in curpt for pt in curl]
            else:
                pointsloc=[[pt.x,pt.y,pt.z] for curl in curpt for pt in curl]

            trianglesloc=[[[k+decal*nb_points_perline+nbpts,
                        k+1+decal*nb_points_perline+nbpts,
                        nb_points_perline+k+decal*nb_points_perline+nbpts],

                        [nb_points_perline+k+decal*nb_points_perline+nbpts,
                        k+1+decal*nb_points_perline+nbpts,
                        nb_points_perline+k+decal*nb_points_perline+1+nbpts]]                      
                            for decal in range(len(curpt)-1) for k in range(nb_points_perline-1)]

            nbpts+=nb_points_perline*nbsect
            nbloc=(nb_points_perline-1)*(nbsect-1)*2
            nbtr+=nbloc

            points.append(pointsloc)
            triangles.append(np.asarray(trianglesloc).reshape([nbloc,3]))
                

        points=np.asarray(np.concatenate(points),dtype=np.float32)
        triangles=np.asarray(np.concatenate(triangles),dtype=np.uint32)
        
        
        if len(np.argwhere(np.isnan(points)==True))>0:
            a=1

        return nbpts,points,triangles

    def get_points(self,forgltf=False):
        
        points=[]
        nbpts=0
        for curpt in self.interpolants:

            nb_points_perline = len(curpt[0])
            nbsect=len(curpt)
            if forgltf:
                pointsloc=[[pt.x,pt.z,-pt.y] for curl in curpt for pt in curl]
            else:
                pointsloc=[[pt.x,pt.y,pt.z] for curl in curpt for pt in curl]

            nbpts+=nb_points_perline*nbsect
            points.append(pointsloc)
        
        if forgltf:
            points=np.asarray(np.concatenate(points),dtype=np.float32)
        else:
            points=np.asarray(np.concatenate(points))

        return nbpts,points

    def export_gltf(self,points=None,triangles=None):

        if points is None and triangles is None:
            points,triangles= self.get_triangles()
        
        triangles_binary_blob = triangles.flatten().tobytes()
        points_binary_blob = points.tobytes()
        
        gltf = pygltflib.GLTF2(
            scene=0,
            scenes=[pygltflib.Scene(nodes=[0])],
            nodes=[pygltflib.Node(mesh=0)],
            meshes=[
                pygltflib.Mesh(
                    primitives=[
                        pygltflib.Primitive(
                            attributes=pygltflib.Attributes(POSITION=1), indices=0
                        )
                    ]
                )
            ],
            accessors=[
                pygltflib.Accessor(
                    bufferView=0,
                    componentType=pygltflib.UNSIGNED_INT,
                    count=triangles.size,
                    type=pygltflib.SCALAR,
                    max=[int(triangles.max())],
                    min=[int(triangles.min())],
                ),
                pygltflib.Accessor(
                    bufferView=1,
                    componentType=pygltflib.FLOAT,
                    count=len(points),
                    type=pygltflib.VEC3,
                    max=points.max(axis=0).tolist(),
                    min=points.min(axis=0).tolist(),
                ),
            ],
            bufferViews=[
                pygltflib.BufferView(
                    buffer=0,
                    byteLength=len(triangles_binary_blob),
                    target=pygltflib.ELEMENT_ARRAY_BUFFER,
                ),
                pygltflib.BufferView(
                    buffer=0,
                    byteOffset=len(triangles_binary_blob),
                    byteLength=len(points_binary_blob),
                    target=pygltflib.ARRAY_BUFFER,
                ),
            ],
            buffers=[
                pygltflib.Buffer(
                    byteLength=len(triangles_binary_blob) + len(points_binary_blob)
                )
            ],
        )
        gltf.set_binary_blob(triangles_binary_blob + points_binary_blob)
        
        dlg=wx.FileDialog(None,_('Choose filename'),wildcard='binary gltf2 (*.glb)|*.glb|gltf2 (*.gltf)|*.gltf|All (*.*)|*.*',style=wx.FD_SAVE)
        ret=dlg.ShowModal()
        if ret==wx.ID_CANCEL:
            dlg.Destroy()
            return
        
        fn=dlg.GetPath()
        dlg.Destroy()
        
        gltf.save(fn)    

    def get_xy_z_for_griddata(self):
        
        xy = np.asarray([[curvertex.x,curvertex.y] for curpt in self.interpolants for curl in curpt for curvertex in curl])
        z = np.asarray([curvertex.z for curpt in self.interpolants for curl in curpt for curvertex in curl])
        
        # if len(np.argwhere(np.isnan(z)))>0:
        #     test=1
        # if len(np.argwhere(np.isneginf(z)))>0:
        #     test=1
        # if len(np.argwhere(np.isposinf(z)))>0:
        #     test=1
        return xy,z
                                               
class Interpolators():
    
    def __init__(self,banks:Zones,cs,ds=1.) -> None:
        
        self.mybanks = [curv for curzone in banks.myzones for curv in curzone.myvectors]
        cs.set_zones()
        self.mycs = cs.myzones
        
        self.myinterp=[]
        
        zonecs:zone
        zonecs = self.mycs.myzones[0]
        
        if zonecs.myvectors[0].up is not None:
            
            cs1=cs.get_upstream()['cs']
            
            while cs1.down is not cs1:
                cs2=cs1.down
                myinterp=Interpolator(cs1,cs2,self.mybanks,ds)
                self.myinterp.append(myinterp)
                cs1=cs2
        else:
            for i in range(zonecs.nbvectors-1):
                cs1=zonecs.myvectors[i]
                cs2=zonecs.myvectors[i+1]
                myinterp=Interpolator(cs1,cs2,self.mybanks,ds)
                self.myinterp.append(myinterp)
        
        self.myzones= self.mycs.add_interpolators(self)

    def viewer_interpolator(self):

        xyz=[]
        for curinterp in self.myinterp:
            xyz.append(curinterp.get_xyz_for_viewer())

        xyz=np.concatenate(xyz)

        myviewer(xyz,0)
        
    def interp_on_array(self,myarray,method):
        
        xy=[]
        z=[]
        for curint in self.myinterp: 
            tmpxy,tmpz = curint.get_xy_z_for_griddata()
            xy.append(tmpxy)
            z.append(tmpz)
            
        xy = np.concatenate(xy)
        z = np.concatenate(z)
        
        myarray.interpolate_on_cloud(xy,z,method)
                                    
                
                
                
                
        