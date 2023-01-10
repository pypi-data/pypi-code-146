"""
This is a minimal wxPython SplashScreen
"""

from os.path import dirname, join, exists
import wx
import time
from   wx.adv import SplashScreen as SplashScreen,SPLASH_CENTRE_ON_SCREEN,SPLASH_TIMEOUT,Sound

class WolfLauncher(SplashScreen):
    """
    Wolf Splashcreen
    """    
    
    done = False
    
    def __init__(self, parent=None):

        if self.done:
            return

        mydir=dirname(__file__)
        mybitmap = wx.Bitmap(name=join(mydir,".\\WolfPython.png"), type=wx.BITMAP_TYPE_PNG)
        
        mask = wx.Mask(mybitmap, wx.Colour(255,0,204))
        mybitmap.SetMask(mask)
        splash = SPLASH_CENTRE_ON_SCREEN | SPLASH_TIMEOUT
        duration = 2000 # milliseconds

        # Call the constructor with the above arguments
        # in exactly the following order.
        super(WolfLauncher, self).__init__(bitmap=mybitmap,
                                            splashStyle=splash,
                                            milliseconds=duration,
                                            parent=None,
                                            id=-1,
                                            pos=wx.DefaultPosition,
                                            size=wx.DefaultSize,
                                            style=wx.STAY_ON_TOP |
                                                    wx.BORDER_NONE)

        self.Bind(wx.EVT_CLOSE, self.OnExit)
        self.CenterOnScreen(wx.BOTH)
        self.Show()
        
        soundfile=['son6.wav']
        if exists(join(mydir,'../sounds/'+soundfile[0])):
            time.sleep(1)
            mysound = Sound(join(mydir,'../sounds/'+soundfile[0]))
            mysound.Play()
            
        self.done = True

    def OnExit(self, event):
        # The program will freeze without this line.
        event.Skip()  # Make sure the default handler runs too...
        self.Hide()
