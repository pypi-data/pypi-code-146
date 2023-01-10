
class Element_To_Draw:
    
    def __init__(self, idx= '', plotted=True, parentgui = None) -> None:
        
        self.idx = idx
        self.xmin=0.
        self.ymin=0.
        self.xmax=0.
        self.ymax=0.

        self.plotted = plotted
        self.plotting = False
        self.parentGUI = parentgui
        
    def check_plot(self):
        self.plotted = True

    def uncheck_plot(self, unload=True):
        self.plotted = False
    
    def plot(self, sx=None, sy=None, xmin=None, ymin=None, xmax=None, ymax=None, size=None):
        if self.plotted:
            
            self.plotting = True        
            
            # do something in OpenGL...
            
            self.plotting = False

    def find_minmax(self,update=False):
        pass
