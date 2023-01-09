import threading
import tkinter as tk
from tkinter import ttk
from tkinter import IntVar, Radiobutton, font
from ipra.Utility.StringUtility import GetStringSingletion
from ipra.Utility.tkinterUtility import *
from ipra.Utility.ConfigUtility import GetConfigSingletion


class LoadingPolicyTopLevel(tk.Toplevel):
    def __init__(self,xPos,yPos, totalSize):
        tk.Toplevel.__init__(self)
        self.geometry(f'+{int(xPos/2 + xPos)}+{int(yPos/2 + yPos)}')
        self.config_obj = GetConfigSingletion()
        self.stringVar = GetStringSingletion()

        self.title(self.stringVar.importPolicy.get())
        self.iconbitmap('C:\IPRA\RESOURCE\hexicon.ico')

        self.geometry("300x100")

        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        self.columnconfigure(0,weight=1)
        
        self.progressValue = 0
        self.progressBar = ttk.Progressbar(
            self,
            orient='horizontal',
            mode='determinate',
            maximum = totalSize,
            #time 2 is scrap and build
        )

        self.progressBar.grid(column=0, row=0, padx=5,pady=5,sticky='we')
        self.progressBar.grid_propagate(False)


        self.statusLable = tk.Label(self,text=self.stringVar.importPolicy.get(),font=font.Font(size=15))
        self.statusLable.grid(column=0,row=1,sticky='we')
        self.statusLable.grid_propagate(False)

        self.tkraise()

    def setStatusLableText(self,textStringVar):
        self.statusLable.after(10,self.statusLable.config(text=textStringVar))

    def setStatusProgresValueByValue(self,value):
        try:
            self.progressValue = self.progressValue+value
            self.buildHeaderThread = threading.Thread(target = self.__updateProgress,args=[self.progressValue])
            self.buildHeaderThread.start()
            #self.progressBar.after(10,self.__updateProgress(self.progressValue))

        except Exception as ex:
            print(str(ex))

    def updateDisplay(self,policy,progress):
        print(policy+" "+str(progress))
        #self.setStatusLableText(policy)
        self.setStatusProgresValueByValue(progress)

    def __updateProgress(self, value):
        self.progressBar["value"] = value