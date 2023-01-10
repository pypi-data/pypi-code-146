import wx

from .drawing_obj import Element_To_Draw
from .wolf_array import WolfArray,WolfArrayMB
from .PyParams import Wolf_Param

class WolfViews(Element_To_Draw):
    
    def __init__(self, idx='', plotted=True, parentgui = None) -> None:
        
        super().__init__(idx, plotted, parentgui)
        
        self.view = []
        self.pals = []
        
    def read_from_file(self,fn):
        myproject = Wolf_Param(None, filename=fn, toShow=False)

        mykeys = ['cross_sections', 'vector', 'array']

        # with wx.lib.busy.BusyInfo(_('Opening project')):
        #     wait = wx.BusyCursor()

        #     if 'cross_sections' in myproject.myparams.keys():
        #         for curid, curname in zip(myproject.myparams['cross_sections'].keys(),
        #                                 myproject.myparams['cross_sections'].values()):
        #             if curid != 'format' and curid != 'dirlaz':
        #                 mycs = crosssections(curname['value'],
        #                                     format=myproject.myparams['cross_sections']['format']['value'],
        #                                     dirlaz=myproject.myparams['cross_sections']['dirlaz']['value'])

        #                 self.add_object('cross_sections', newobj=mycs, id=curid)

        #     if 'vector' in myproject.myparams.keys():
        #         for curid, curname in zip(myproject.myparams['vector'].keys(), myproject.myparams['vector'].values()):
        #             if exists(curname['value']):
        #                 myvec = Zones(curname['value'])
        #                 self.add_object('vector', newobj=myvec, id=curid)
        #             else:
        #                 wx.LogMessage(_('Bad parameter in project file - vector : ')+ curname['value'])

        #     if 'array' in myproject.myparams.keys():
        #         for curid, curname in zip(myproject.myparams['array'].keys(), myproject.myparams['array'].values()):
                    
        #             if exists(curname['value']):
        #                 curarray = WolfArray(curname['value'])
        #                 self.add_object('array', newobj=curarray, id=curid)
        #             else:
        #                 wx.LogMessage(_('Bad parameter in project file - array : ')+ curname['value'])


        #     if 'wolf2d' in myproject.myparams.keys():
        #         for curid, curname in zip(myproject.myparams['wolf2d'].keys(), myproject.myparams['wolf2d'].values()):
        #             if exists(curname['value']):
        #                 curwolf = Wolfresults_2D(curname['value'])
        #                 self.add_object('res2d', newobj=curwolf, id=curid)
        #             else:
        #                 wx.LogMessage(_('Bad parameter in project file - wolf2d : ')+ curname['value'])

        #         self.menu_wolf2d()

        #     if 'palette' in myproject.myparams.keys():
        #         self.project_pal = {}
        #         for curid, curname in zip(myproject.myparams['palette'].keys(), myproject.myparams['palette'].values()):
        #             if exists(curname['value']):
        #                 mypal = wolfpalette(None, '')
        #                 mypal.readfile(curname['value'])
        #                 mypal.automatic = False

        #                 self.project_pal[curid] = mypal
        #             else:
        #                 wx.LogMessage(_('Bad parameter in project file - palette : ')+ curname['value'])

        #     if 'palette-array' in myproject.myparams.keys():
        #         curarray: WolfArray
        #         if self.project_pal is not None:
        #             for curid, curname in zip(myproject.myparams['palette-array'].keys(),
        #                                     myproject.myparams['palette-array'].values()):
        #                 if curname['value'] in self.project_pal.keys():
        #                     curarray = self.getobj(curid)
        #                     if curarray is not None:
        #                         mypal:wolfpalette
        #                         mypal = self.project_pal[curname['value']]
        #                         curarray.mypal = mypal
        #                         if mypal.automatic:
        #                             curarray.myops.palauto.SetValue(1)
        #                         else:
        #                             curarray.myops.palauto.SetValue(0)
        #                         curarray.updatepalette(0)
        #                         curarray.delete_lists()
        #                     else:
        #                         wx.LogWarning(_('Bad parameter in project file - palette-array : ')+ curid)

        #     if 'cross_sections_link' in myproject.myparams.keys():
        #         if 'linkzones' in myproject.myparams['cross_sections_link'].keys():
        #             idx = myproject.myparams['cross_sections_link']['linkzones']['value']

        #             for curvect in self.added['vectors']:
        #                 myzones: Zones
        #                 myzones = self.added['vectors'][curvect]['values']
        #                 if myzones.idx == idx:
        #                     self.active_cs.link_external_zones(myzones)

        #             zonename = ''
        #             vecname = ''

        #             if 'sortzone' in myproject.myparams['cross_sections_link'].keys():
        #                 zonename = myproject.myparams['cross_sections_link']['sortzone']['value']
        #             if 'sortname' in myproject.myparams['cross_sections_link'].keys():
        #                 vecname = myproject.myparams['cross_sections_link']['sortname']['value']

        #             if zonename != '' and vecname != '':
        #                 names = [cur.myname for cur in myzones.myzones]
        #                 idx = names.index(zonename)
        #                 curzone = myzones.myzones[idx]
        #                 names = [cur.myname for cur in curzone.myvectors]
        #                 idx = names.index(vecname)
        #                 curvec = curzone.myvectors[idx]

        #                 if curvec is not None:
        #                     curvec: vector
        #                     self.active_cs.sort_along(curvec.asshapely_ls(), curvec.myname, False)
                            
        #     if 'vector_array_link' in myproject.myparams.keys():
        #         for curid, curname in zip(myproject.myparams['vector_array_link'].keys(), myproject.myparams['vector_array_link'].values()):
                    
        #             locvec = None
        #             locarray = None
        #             for curvec in self.myvectors:
        #                 if curvec.idx == curname['value'].lower():
        #                     locvec=curvec
        #                     break
                    
        #             for curarray in self.myarrays:
        #                 if curarray.idx == curid.lower():
        #                     locarray=curarray
        #                     break
                        
        #             if locvec is not None and locarray is not None:
                        
        #                 locarray.linkedvec = locvec.myzones[0].myvectors[0]
                        
        #             else:
                        
        #                 wx.LogWarning(_('Bad vec-array association in project file !'))
        #                 wx.LogWarning(curid)
        #                 wx.LogWarning(curname['value'])
        #     del wait
            
    def change_gui(self, newparentgui):
        self.parentGUI = newparentgui

        for cur in self.view:
            if isinstance(cur,WolfArray) or isinstance(cur,WolfArrayMB):
                cur.change_gui(newparentgui)
            else:
                cur.parentGUI = newparentgui
        
    def add_elemt(self,added_elemt,pal=None):
        self.view.append(added_elemt)
        self.pals.append(pal)
    
    def add_elemts(self,added_elemts:list,pals=None):
        self.view += added_elemts
        
        if pals is None:
            self.pals += [None]*len(added_elemts)
        else:
            self.pals += pals
                    
    def plot(self, sx=None, sy=None, xmin=None, ymin=None, xmax=None, ymax=None, size=None):

        if self.plotted:

            for cur,pal in zip(self.view,self.pals):
                oldplotted = cur.plotted
                cur.plotted=True
                
                if isinstance(cur,WolfArray):
                    if cur.rgb is None:
                        if pal is not None:
                            cur.rgb = pal.get_rgba(cur.array)
                        else:
                            cur.mypal.defaultgray_minmax(cur.array)
                            cur.rgb = cur.mypal.get_rgba(cur.array)
                
                cur.plot(sx,sy,xmin,ymin,xmax,ymax)
                cur.plotted = oldplotted

    def find_minmax(self):
        xmin = 1.e30
        ymin = 1.e30
        xmax = -1.e30
        ymax = -1.e30
        
        for cur in self.view:
            if isinstance(cur,WolfArray) or isinstance(cur,WolfArrayMB):
                x,y = cur.get_bounds()                
                xmin = min(x[0], xmin)
                xmax = max(x[1], xmax)
                ymin = min(y[0], ymin)
                ymax = max(y[1], ymax)
        
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
