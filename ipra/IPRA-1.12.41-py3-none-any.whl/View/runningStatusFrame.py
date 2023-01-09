import tkinter as tk
from tkinter import ttk
import configparser

from ipra.Utility.StringUtility import GetStringSingletion
from tkinter import font
from ipra.Utility.ConfigUtility import GetConfigSingletion

class RunningStatusFrame(tk.Frame):
    STATUS_EXCEPTION = 0
    STATUS_SCRAP_COMPLETE = 1
    STATUS_REPORT_COMPLETE = 2
    
    def __init__(self,masterFrame,col_idx,company):
        super().__init__(masterFrame)
        self.currentCompnany = company
        
        self.grid_propagate(0)
        self.grid(row=0,column=col_idx,sticky='nwes',padx=5, pady=5)
        #row 0 = list box, row 1 = running status
        tk.Frame.rowconfigure(self,0,weight=1)
        tk.Frame.rowconfigure(self,1,weight=15)
        tk.Frame.rowconfigure(self,2,weight=1)
        tk.Frame.rowconfigure(self,3,weight=1)
        tk.Frame.columnconfigure(self,0,weight=1)
        
        #create check box 
        self.defaultCheck = False

        self.stringDisplay = GetStringSingletion()
        try:
            self.config_obj = GetConfigSingletion()
            defaultValue = self.config_obj.ReadConfig('default_download_report',company[0])
            if defaultValue == 'True':
                self.defaultCheck = True
        except Exception as e:
            self.defaultCheck = False
            
            
        self.chkValue = tk.BooleanVar() 
        self.chkValue.set(self.defaultCheck)
        self.chkText = self.stringDisplay.downloadReport.get().format(self.stringDisplay.CompanyFullName(company[0]),font=('Arial bold',15))
        self.chkbox = tk.Checkbutton(self, text=self.chkText, var=self.chkValue ,font=('Arial bold',12)) 
        self.chkbox.grid(column=0,row=0,columnspan=2,sticky='w')
        self.chkbox.grid_propagate(False)

        #create list box
        self.listbox = tk.Listbox(self,listvariable=tk.StringVar(value=company),font=("Arial", 12))
        self.listbox.grid(column=0,row=1,sticky='nwes')

        # link a scrollbar to a list
        scrollbar = tk.Scrollbar(
            self,
            orient='vertical',
            command=self.listbox.yview
        )

        self.listbox['yscrollcommand'] = scrollbar.set

        scrollbar.grid(
            column=1,
            row=1,
            sticky='ns')
        
        #create Progress bar
        self.progressValue = 0
        self.progressBar = ttk.Progressbar(
            self,
            orient='horizontal',
            mode='determinate',
            maximum= (len(company)-1) * 2
            #time 2 is scrap and build
        )
        # place the progressbar
        self.progressBar.grid(column=0, row=2, columnspan=2, padx=5,pady=5,sticky='we')
        self.progressBar.grid_propagate(False)
        
        self.policyList = company
        self.policyStatus = [-1] * len(company)

        self.statusLable = tk.Label(self,text=self.stringDisplay.waitingExe.get(),font=font.Font(size=15))
        self.statusLable.grid(column=0,row=3,columnspan=2,sticky='nwes')
        self.statusLable.grid_propagate(False)

    def setStatusLableText(self,textStringVar):
        self.statusLable.after(10,self.statusLable.config(text=textStringVar))

    def setStatusProgresValueByValue(self,value):
        self.progressValue = self.progressValue+value
        self.progressBar["value"] = self.progressValue
        
    def resetProgress(self):
        self.progressValue = 0
        self.progressBar["value"] = self.progressValue
        self.setStatusLableText(self.stringDisplay.waitingExe.get())
    
    def getDownloadReportIndicator(self):
        return self.chkValue.get()
        
    def setListItemColor(self,policy,status):
        index = self.policyList.index(policy)
        if not self.policyStatus[index] == self.STATUS_EXCEPTION:
            self.policyStatus[index] = status
            if status == self.STATUS_EXCEPTION:
                self.listbox.itemconfig(index, {'bg':'red','fg':'white'})
            elif status == self.STATUS_SCRAP_COMPLETE:
                self.listbox.itemconfig(index, {'bg':'lightblue'})
            else:
                self.listbox.itemconfig(index, {'bg':'lightgreen'})
            pass
        else:
            pass
    
    def setListItemCursor(self,policy):
        index = self.policyList.index(policy)
        self.listbox.selection_set(index)
        pass

    def updateLangauge(self):
        self.chkbox.after(10,
        self.chkbox.config(text=self.stringDisplay.downloadReport.get().format(self.stringDisplay.CompanyFullName(self.currentCompnany[0]))))
    
