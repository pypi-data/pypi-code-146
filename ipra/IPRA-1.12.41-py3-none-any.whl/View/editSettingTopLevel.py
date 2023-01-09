import tkinter as tk
from tkinter import IntVar, Radiobutton, font
from tkinter.constants import DISABLED
from ipra.Logger.logger import Logger

from ipra.Utility.StringUtility import GetStringSingletion
from ipra.Utility.tkinterUtility import *
from ipra.Utility.ConfigUtility import GetConfigSingletion

class EditSettingTopLevel(tk.Toplevel):
    def __init__(self,xPos,yPos):
        tk.Toplevel.__init__(self)
        
        self.logger = Logger()
        self.geometry(f'+{xPos}+{yPos}')
        self.config_obj = GetConfigSingletion()
        self.stringVar = GetStringSingletion()

        self.title(self.stringVar.editSetting.get())
        self.iconbitmap('C:\IPRA\RESOURCE\hexicon.ico')
        # sets the geometry of toplevel
        self.geometry("550x250")
        
        tk.Frame.rowconfigure(self,0,weight=1)
        tk.Frame.columnconfigure(self,0,weight=1)
        
        mainFrame = tk.Frame(master=self,background='#808080')
        mainFrame.grid(row=0,column=0,sticky='nsew')
        mainFrame.grid_propagate(False)


        #Log Path related
        logPathLable = tk.Label(mainFrame,text=self.stringVar.logPath.get(),font=("Arial", 15),background='#808080')

        logPathLable.grid(column=0,row=0,sticky='ns',padx=5,pady=5)
        logPathLable.grid_propagate(False)

        self.logPath = tk.StringVar(mainFrame,value=self.config_obj.ReadConfig('logger_path','loggerpath'))
        self.logPathTextField = tk.Entry(mainFrame,font=("Arial", 10),width=30,textvariable=self.logPath,state=DISABLED)
        self.logPathTextField.grid(column=1,row=0,sticky='nwse',padx=5,pady=5)
        self.logPathTextField.grid_propagate(False)
        
        setlogPathButton = tk.Button(mainFrame,text=self.stringVar.selectPath.get(),command=self.__selectLogDirectory,font=font.Font(size=15))
        setlogPathButton.grid(column=2,row=0, sticky='nsew',padx=5, pady=5)
        #Log Path related

        #Output Path related
        outputPathLable = tk.Label(mainFrame,text=self.stringVar.outputPath.get(),font=("Arial", 15),background='#808080')

        outputPathLable.grid(column=0,row=1,sticky='ns',padx=5,pady=5)
        outputPathLable.grid_propagate(False)

        self.outputPath = tk.StringVar(mainFrame,value=self.config_obj.ReadConfig('report_path','outputPath'))
        self.outputPathTextField = tk.Entry(mainFrame,font=("Arial", 10),width=30,textvariable=self.outputPath,state=DISABLED)
        self.outputPathTextField.grid(column=1,row=1,sticky='nwse',padx=5,pady=5)
        self.outputPathTextField.grid_propagate(False)
        
        setOutputPathButton = tk.Button(mainFrame,text=self.stringVar.selectPath.get(),command=self.__selectOutPutDirectory,font=font.Font(size=15))
        setOutputPathButton.grid(column=2,row=1, sticky='nsew',padx=5, pady=5)
        #Output Path related
        
        #Input Path related
        inputPathLable = tk.Label(mainFrame,text=self.stringVar.inputPath.get(),font=("Arial", 15),background='#808080')
        inputPathLable.grid(column=0,row=2,sticky='ns',padx=5,pady=5)
        inputPathLable.grid_propagate(False)

        self.inputPath = tk.StringVar(mainFrame,value='')
        self.inputPathTextField = tk.Entry(mainFrame,font=("Arial", 10),width=30,textvariable=self.inputPath,state=DISABLED)
        self.inputPathTextField.grid(column=1,row=2,sticky='nwse',padx=5,pady=5)
        self.inputPathTextField.grid_propagate(False)
        
        returnButton = tk.Button(mainFrame,text=self.stringVar.selectPath.get(),command=self.__selectInputPutDirectory,font=font.Font(size=15))
        returnButton.grid(column=2,row=2, sticky='nsew',padx=5, pady=5)
        #Input Path related

        #radio Button section for Language selection
        self.languageSelect = IntVar()
        if self.config_obj.ReadConfig('language','display') == 'zh':
            self.languageSelect.set(1)
        else:
            self.languageSelect.set(2)


        R1 = Radiobutton(mainFrame, text=self.stringVar.zhHK.get(), variable=self.languageSelect, value=1,font=font.Font(size=15))
        R1.grid(column=0,row=3,sticky='nsew',padx=5,pady=5)
        R1.grid_propagate(False)
        R2 = Radiobutton(mainFrame, text=self.stringVar.english.get(), variable=self.languageSelect, value=2,font=font.Font(size=15))
        R2.grid(column=1,row=3,sticky='nsew',padx=5,pady=5)
        R2.grid_propagate(False)
        #radio Button section for Language selection

        returnButton = tk.Button(mainFrame,text=self.stringVar.saveAndReturn.get(),command=self.__confirmReturn,font=font.Font(size=15))
        returnButton.grid(column=0,row=4, sticky='nsew',padx=5, pady=5)

        self.isUpdateRequired = False
        self.tkraise()
        
    def show(self):
        self.wait_window()
        return self.isUpdateRequired
    
    def __confirmReturn(self):
        self.config_obj.WriteConfig('report_path','outputPath',self.outputPath.get())
        self.config_obj.WriteConfig('report_path','inputPath',self.inputPath.get())
        self.config_obj.WriteConfig('logger_path','loggerpath',self.logPath.get())
        
        if self.languageSelect.get() == 1:
            self.config_obj.WriteConfig('language','display','zh')
        else:
            self.config_obj.WriteConfig('language','display','en')

        self.isUpdateRequired = True
        self.destroy()
        return
    
    def __selectOutPutDirectory(self):
        self.outputPath.set(selectPath())
        self.tkraise()
        return

    def __selectInputPutDirectory(self):
        self.inputPath.set(selectPath()+'/')
        self.tkraise()
        return

    def __selectLogDirectory(self):
        self.logPath.set(selectPath())
        self.logPath.set(self.logPath.get()+'/')
        self.logger.setLogPath(self.logPath.get())
        self.tkraise()
        return