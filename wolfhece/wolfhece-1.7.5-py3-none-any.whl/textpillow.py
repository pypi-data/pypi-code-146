from queue import PriorityQueue
from PIL import Image,ImageDraw,ImageFont
import numpy as np

PRIORITY_WIDTH=0
PRIORITY_HEIGHT=1
PRIORITY_FONTSIZE=2

class Text_Infos():
    
    def __init__(self, priority=PRIORITY_WIDTH, orientationbase=(1,0), 
                 fontname="arial.ttf", fontsize=10, colour=(0,0,0,255),
                 dimspix=(100,100),dimsreal=(0,0)) -> None:
                
        self.lengthpix = dimspix[0]
        self.heightpix = dimspix[1]

        self.lengthreal = dimsreal[0]
        self.heightreal = dimsreal[1]

        self.scalex = 1
        self.scaley = 1
        
        self.orientationbase = orientationbase
        
        self.priority = priority
        
        self.fontname = fontname
        self.fontsize = fontsize
        self.colour = colour
                            
    def setsize_pixels(self,w,h):
        
        self.lengthpix = w
        self.heightpix = h

    def setsize_real(self,wh=(0,0),scales=(0,0)):
        """Evalue la taille en pixel sur base de la taille réelle

        Args:
            w (float): largeur dans le système réel
            h (float): hauteur dans le système réel
            scales (tuple, optional): Facteur d'échelle selon x et y. Defaults to (0,0)
            
            Le facteur d'céhelle est évalué comme le rapport entre la taille en pixel et la taille réelle. 
            Exemple : 0.5 --> 2x plus petit en pixels qu'en réel. 
        """        
        if self.priority == PRIORITY_FONTSIZE:
            return

        if scales != (0,0):
            self.scalex=scales[0]
            self.scaley=scales[1]
        
        if wh!=(0,0):
            self.lengthreal=wh[0]
            self.heightreal=wh[1]

        self.lengthpix = self.lengthreal*self.scalex
        self.heightpix = self.heightreal*self.scaley
    
    def findsize(self,text:str):
        """Trouve la taille en pixel sur base du texte et de la taille de police en cours

        Args:
            text (str): Texte à utiliser
        """        
        
        font=ImageFont.truetype(self.fontname,self.fontsize)
        left,top,right,bottom = font.getbbox(text)
        
        self.lengthpix = right-left
        self.heightpix = bottom-top   
        
    def adapt_fontsize(self,text):
        
        old = self.fontsize
        
        if self.priority == PRIORITY_FONTSIZE:
            return not old==self.fontsize
        
        w = self.lengthpix
        h = self.heightpix
        
        self.findsize(text)
        
        scalex=1
        scaley=1
        if w!=0:
            scalex = self.lengthpix / w
        if h!=0:
            scaley = self.heightpix / h
        
        if self.priority == PRIORITY_WIDTH:
            self.fontsize = int(self.fontsize/scalex)
        elif self.priority == PRIORITY_HEIGHT:             
            self.fontsize = int(self.fontsize/scaley)

        self.fontsize=min(self.fontsize,200)

        self.findsize(text)
        
        return abs(old-self.fontsize)>3
        
    def findscale(self,dx,dy,w,h):
        
        self.scalex = w/dx
        self.scaley = h/dy

    def setscale(self,sx=1,sy=1):
        
        self.scalex = sx
        self.scaley = sy

        if self.scalex == 0:
            self.scalex=1.
        if self.scaley == 0:
            self.scaley=1.

    def getcorners(self, xcenter, ycenter):
        
        orientx = self.orientationbase
        orienty = (-orientx[1], orientx[0])
        
        if self.scalex == 0:
            self.scalex=1.
        if self.scaley == 0:
            self.scaley=1.
        
        l2scale = self.lengthpix/self.scalex/2
        h2scale = self.heightpix/self.scaley/2
        
        x1 = xcenter - orienty[0]*h2scale - orientx[0]*l2scale
        x2 = xcenter - orienty[0]*h2scale + orientx[0]*l2scale
        x3 = xcenter + orienty[0]*h2scale + orientx[0]*l2scale
        x4 = xcenter + orienty[0]*h2scale - orientx[0]*l2scale

        y1 = ycenter - orienty[1]*h2scale - orientx[1]*l2scale
        y2 = ycenter - orienty[1]*h2scale + orientx[1]*l2scale
        y3 = ycenter + orienty[1]*h2scale + orientx[1]*l2scale
        y4 = ycenter + orienty[1]*h2scale - orientx[1]*l2scale
        
        x=[x1,x2,x3,x4]
        y=[y1,y2,y3,y4]
        
        return x,y
    
    def getminmax(self, xcenter, ycenter):
        
        x,y = self.getcorners(xcenter,ycenter)
        return np.min(x),np.max(x),np.min(y),np.max(y)
        
class Text_Image():

    def __init__(self,text,proptext:Text_Infos) -> None:
        
        self.text=text
        self.width=proptext.lengthpix
        self.height=proptext.heightpix
        self.fontname=proptext.fontname
        self.color=proptext.colour

        self.font10=ImageFont.truetype(self.fontname,10)

        self.priority=proptext.priority

        self.image=None
        
        if proptext.priority == PRIORITY_FONTSIZE:
            self.cur_sizefont=proptext.fontsize
        else:
            self.cur_sizefont=10

        self.create_image()

    def create_image(self):

        if self.priority == PRIORITY_WIDTH:
            left,top,right,bottom = self.font10.getbbox(self.text)
            scale = self.width/(right-left)
            self.cur_sizefont = int(10*scale)
        elif self.priority == PRIORITY_HEIGHT:
            left,top,right,bottom = self.font10.getbbox(self.text)
            scale = self.height/(bottom-top)
            self.cur_sizefont = int(10*scale)
        elif self.priority == PRIORITY_FONTSIZE:
            scale = 1
        
        self.curfont=ImageFont.truetype(self.fontname,size=self.cur_sizefont)

        self.imagemask = self.curfont.getmask(self.text) #, mode="L")
        left,top,right,bottom = self.curfont.getbbox(self.text)
        
        self.image = Image.new('RGBA',self.imagemask.size,(255,255,255,0))
        drawer = ImageDraw.Draw(self.image)
        drawer.text((0,-top),text=self.text,font=self.curfont,fill=self.color,)

if __name__=='__main__':

    myprop = Text_Infos(PRIORITY_WIDTH,fontname="sanserif.ttf",colour=(50,255,60,255))
    myprop.lengthpix=300    

    myprop.adapt_fontsize('test')

    myprop = Text_Infos(PRIORITY_WIDTH,fontname="arial.ttf",colour=(50,255,60,255))
    myprop.lengthpix=300    
    mytest = Text_Image("Test",myprop)
    mytest.image.show()

    myprop = Text_Infos(PRIORITY_HEIGHT,fontname="arial.ttf",colour=(50,255,60,255))
    myprop.heightpix=300
    mytest = Text_Image("Test", myprop)
    mytest.image.show()

    myprop = Text_Infos(PRIORITY_WIDTH,fontname="arial.ttf",colour=(50,255,60,255))
    myprop.setsize_real(300,200,(1,1))
    mytest = Text_Image("Test",myprop)
    mytest.image.show()

    myprop = Text_Infos(PRIORITY_WIDTH,fontname="arial.ttf",colour=(50,255,60,255))
    myprop.setsize_real(300,200,(.5,.5))
    mytest = Text_Image("Test",myprop)
    mytest.image.show()




