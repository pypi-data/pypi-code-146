from email import policy
from ipra.Utility.StringUtility import *
from ipra.Controller.reportThreadController import ReportThreadController
from ipra.Controller.robotThreadController import RobotThreadController
from ipra.Controller.policyCollectionController import PolicyCollectionController
from ipra.Utility.ConfigUtility import GetConfigSingletion
from ipra.Utility.tkinterUtility import *
from ipra.Logger.logger import Logger
from ipra.View.runningStatusFrame import RunningStatusFrame
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from ipra.View.manualInputTopLevel import ManualInputTopLevel
from ipra.View.editSettingTopLevel import EditSettingTopLevel
import random

class MainApplication(tk.Tk):
    frame_running_state = None
    frame_instances_running_state = []
    __VERSION = "1.12.39"
    __DATE = "03-JAN-2022"
    __CHECKSUM = "AA847271DAD0F54D"

    supportSystem = None
    button_standard = None
    button_manual = None
    button_reset = None
    button_start = None
    button_report = None

    def __init__(self):
        tk.Tk.__init__(self)
        
        self.logger = Logger()
        self.configParser = GetConfigSingletion()
        self.stringValue = GetStringSingletion()

        self.logger.writeLogString('MAINFRAME','START IPRA {0}'.format(self.__VERSION))
        self.title("IPRA v{0}".format(self.__VERSION))
        self.geometry("600x700")
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(side="top", fill="both", expand=True)
        self.protocol("WM_DELETE_WINDOW", self.__closeMainFrame)
        self.__createMenuBar()
        
        tk.Frame.rowconfigure(self.main_frame,0,weight=1)
        tk.Frame.rowconfigure(self.main_frame,1,weight=10)
        tk.Frame.rowconfigure(self.main_frame,2,weight=1)
        tk.Frame.columnconfigure(self.main_frame,0,weight=1)

        #Open excel, work sheet etc. prepare all the policy no.
        frame_open_excel = tk.Frame(master=self.main_frame)
        frame_open_excel.grid(row=0,column=0,sticky='nsew')
        frame_open_excel.grid_propagate(0)

        #Display Policy no. and running status
        self.frame_running_state = tk.Frame(master=self.main_frame,background="#808080")
        self.frame_running_state.grid(row=1,column=0,sticky='nsew')
        self.frame_running_state.grid_propagate(0)
        
        #start/clean running state
        frame_exeRobot = tk.Frame(master=self.main_frame)
        frame_exeRobot.grid(row=2,column=0,sticky='nsew')
        frame_exeRobot.grid_propagate(0)

        self.policyController = PolicyCollectionController()
        self.robotThreadController = RobotThreadController()
        self.reportThreadController = ReportThreadController()
        
        self.__createFrameOpenExcel(frame_open_excel)
        self.__createFrameExeRobot(frame_exeRobot)

    def startFrame(self):
        self.mainloop()
    
    def __createMenuBar(self):
        self.menubar = Menu(self, background='#ff8000', foreground='black', activebackground='white', activeforeground='black')  

        self.edit = Menu(self.menubar, tearoff=0)  
        self.edit.add_command(label=self.stringValue.editSetting.get(), command=self.__editSetting)  
        self.menubar.add_cascade(label=self.stringValue.setting.get(), menu=self.edit)  

        self.help = Menu(self.menubar, tearoff=0)  
        self.help.add_command(label=self.stringValue.about.get(), command=self.__about)  
        self.menubar.add_cascade(label=self.stringValue.about.get(), menu=self.help)
        
        self.config(menu=self.menubar)
    
    def __about(self):
        aboutWindow = Toplevel(self)
        aboutWindow.geometry(f'+{self.winfo_rootx()}+{self.winfo_rooty()}')
        aboutWindow.iconbitmap('C:\IPRA\RESOURCE\hexicon.ico')
        aboutWindow.title(self.stringValue.about.get())
 
        # sets the geometry of toplevel
        aboutWindow.geometry("300x350")

        # A Label widget to show in toplevel
        self.version = Label(aboutWindow,text = self.stringValue.versionString.get().format(self.__VERSION))
        self.version.config(font=('Arial bold',13))
        self.version.pack(anchor=NW)

        self.date = Label(aboutWindow,text = self.stringValue.releaseDate.get().format(self.__DATE))
        self.date.config(font=('Arial bold',13))
        self.date.pack(anchor=NW)

        self.checksum = Label(aboutWindow,text = self.stringValue.checksum.get().format(self.__CHECKSUM))
        self.checksum.config(font=('Arial bold',13))
        self.checksum.pack(anchor=NW)


        Label(aboutWindow,text ="")
        self.supportSystem = Label(aboutWindow,text = self.stringValue.supportSystem.get(),font=font.Font(size=15))
        self.supportSystem.pack()
        
        listbox_widget = Listbox(aboutWindow,height=50)
        for entry in self.policyController.getPolicyCollection():
            listbox_widget.insert(END, entry[0])
        listbox_widget.pack()
    
    def __editSetting(self):
        editSettingDialog = EditSettingTopLevel(self.winfo_rootx(),self.winfo_rooty())
        if editSettingDialog.show():
            self.__updateDisplayLanguage()

        return
        
    def __createFrameOpenExcel(self,frame):
        Grid.rowconfigure(frame,0,weight=1)
        Grid.columnconfigure(frame,0,weight=1)
        #Grid.columnconfigure(frame,1,weight=1)

        self.button_standard = Button(frame, text=self.stringValue.importPolicy.get(), command=self.__openStandardFile,font=font.Font(size=15))
        #self.button_manual = Button(frame,text =self.stringValue.importManualPolicy.get(),command=self.__openManualInputDialog,font=font.Font(size=15))

        self.button_standard.grid(row=0,column=0, sticky='nsew',padx=5, pady=5)
        #self.button_manual.grid(row=0,column=1, sticky='nsew',padx=5, pady=5)
        return

    def __createFrameExeRobot(self,frame):
        Grid.rowconfigure(frame,0,weight=1)
        Grid.columnconfigure(frame,0,weight=1)
        Grid.columnconfigure(frame,1,weight=1)
        Grid.columnconfigure(frame,2,weight=1)

        self.button_reset = Button(frame, text =self.stringValue.clear.get(),command = self.__cleanFrameRunningState,font=font.Font(size=15))
        self.button_start = Button(frame,text =self.stringValue.startRobot.get(),command=self.__startRobot,font=font.Font(size=15))
        self.button_report = Button(frame,text =self.stringValue.exportReport.get(),command=self.__buildReport,font=font.Font(size=15))

        self.button_reset.grid(row=0,column=0, sticky='nsew',padx=5, pady=5)
        self.button_start.grid(row=0,column=1, sticky='nsew',padx=5, pady=5)
        self.button_report.grid(row=0,column=2, sticky='nsew',padx=5, pady=5)
        return

    def __openStandardFile(self):
        filePath = openFileAll()
        if filePath != None and filePath != '':
            readResult = self.policyController.getPolicyListFromFile(filePath)
            if readResult:
                self.__displaySearchPolicy()
            else:
                messagebox.showerror(self.stringValue.importError.get(), self.stringValue.formatError.get())
        return
    
    def __openManualInputDialog(self):
        manualInputDialog = ManualInputTopLevel(self.policyController.getSupportedList())
        manualList = manualInputDialog.show()
        self.policyController.policySwitchByList(manualList)
        self.__displaySearchPolicy()
        return

    def __displaySearchPolicy(self):
        column_idx = 0
        Grid.rowconfigure(self.frame_running_state,0,weight=10)
        for company in self.policyController.getPolicyCollection():
            if(len(company)>1):
                Grid.columnconfigure(self.frame_running_state,column_idx,weight=1)
                frameTemp = RunningStatusFrame(self.frame_running_state,column_idx,company)
                column_idx = column_idx + 1
                self.frame_instances_running_state.append(frameTemp)
            else:
                self.frame_instances_running_state.append(None)

    def __cleanFrameRunningState(self):
        #Clean and reset
        
        for frame in self.frame_instances_running_state:
            if frame != None:
                frame.destroy()
        #self.frame_running_state.destory()
        self.__resetFrameRunningState()
        self.frame_instances_running_state = []
        self.policyController.cleanAllPolicy()

    def __startRobot(self):
        self.robotThreadController.createRobotThread(self.policyController.getPolicyCollection(),self.frame_instances_running_state)

    def __buildReport(self):
        self.reportThreadController.createReportThread(self.policyController.getPolicyCollection(),self.frame_instances_running_state)

    def __closeMainFrame(self):
        #Shut down all frame and close all webdriver
        #Important to release all resources
        self.robotThreadController.destoryAllRobotThread()
        self.destroy()

        return

    def __resetFrameRunningState(self):
        self.frame_running_state = tk.Frame(master=self.main_frame,background="#808080")
        self.frame_running_state.grid(row=1,column=0,sticky='nsew')
        self.frame_running_state.grid_propagate(0)        

    def __updateDisplayLanguage(self):
        self.stringValue.SetString()

        self.__createMenuBar()

        self.button_standard.after(10,self.button_standard.config(text=self.stringValue.importPolicy.get()))

        self.button_reset.after(10,self.button_reset.config(text=self.stringValue.clear.get()))
        self.button_start.after(10,self.button_start.config(text=self.stringValue.startRobot.get()))
        self.button_report.after(10,self.button_report.config(text=self.stringValue.exportReport.get()))

        for policyFrame in self.frame_instances_running_state:
            if policyFrame != None:
                policyFrame.updateLangauge()



