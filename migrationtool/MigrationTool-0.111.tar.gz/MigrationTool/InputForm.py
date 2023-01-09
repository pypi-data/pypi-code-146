import tkinter as tk
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
import Definition
import Parser
class InputForm(object): 
    hddProject = Definition.Project
    def __init__(self, project: Definition.Project):
        self.hddProject = project
        root=tk.Tk()
        
        # setting the windows size
        root.geometry("600x400")
          
        # declaring string variable
        # for storing name and password
        project_description=tk.StringVar()
        landing_name=tk.StringVar()
        storage_name=tk.StringVar()
        transformation_name=tk.StringVar()
        qem_server_name=tk.StringVar()
        storage_connection_name=tk.StringVar()
        source_connection_name=tk.StringVar()
        space_name=tk.StringVar()
        host=tk.StringVar()
        api_version=tk.StringVar()
        bearer_token=tk.StringVar()
        project_name=tk.StringVar()
        json_path=tk.StringVar()
        varblbl=tk.IntVar()
          
        # defining a function that will
        # get the name and password and
        # print them on the screen
        def selection():
            self.hddProject.manual=True
            self.hddProject.online=False
            self.hddProject.input_path = simpledialog.askstring("input string","Please enter txt file path")
            root.destroy()
        def submit():
         
            self.hddProject.online=True
            self.hddProject.manual=False
            self.hddProject.project_description=project_description.get()
            self.hddProject.landing_name=landing_name.get()
            self.hddProject.storage_name=storage_name.get()
            self.hddProject.transformation_name=transformation_name.get()
            self.hddProject.qem_server_name=qem_server_name.get()
            self.hddProject.storage_connection_name=storage_connection_name.get()
            self.hddProject.source_connection_name=source_connection_name.get()
            self.hddProject.space_name=space_name.get()
            self.hddProject.host=host.get()
            self.hddProject.api_version=api_version.get()
            self.hddProject.bearer_token=bearer_token.get()
            self.hddProject.project_name=project_name.get()
            self.hddProject.json_path=json_path.get()
            print("The name is : " + self.hddProject.project_description)
            #print("The password is : " + password)
             
            project_description.set("")
            landing_name.set("")
            storage_name.set("")
            transformation_name.set("")
            qem_server_name.set("")
            storage_connection_name.set("")
            source_connection_name.set("")
            space_name.set("")
            host.set("")
            api_version.set("")
            bearer_token.set("")
            project_name.set("")
            json_path.set("")
            root.destroy()


        r1=Radiobutton(root, text="Use txt file",padx = 5, variable=varblbl, value=1, command=selection).place(x=300,y=10)  
        r2=Radiobutton(root, text="Use Online Form",padx = 5, variable=varblbl, value=2).place(x=150,y=10)

        r1_label = tk.Label(root, text = '', font=('calibre',10, 'bold'))
        r2_label = tk.Label(root, text = '', font=('calibre',10, 'bold'))

        project_description_label = tk.Label(root, text = 'project_description', font=('calibre',10, 'bold'))
        project_description_entry = tk.Entry(root,textvariable = project_description, font=('calibre',10,'normal'))
          
        landing_name_label = tk.Label(root, text = 'landing_name', font = ('calibre',10,'bold'))
        landing_name_entry=tk.Entry(root, textvariable = landing_name, font = ('calibre',10,'normal'))#, show = '*')
          

        storage_name_label = tk.Label(root, text = 'storage_name', font = ('calibre',10,'bold'))
        storage_name_entry=tk.Entry(root, textvariable = storage_name, font = ('calibre',10,'normal'))

        transformation_name_label = tk.Label(root, text = 'transformation_name', font = ('calibre',10,'bold'))
        transformation_name_entry=tk.Entry(root, textvariable = transformation_name, font = ('calibre',10,'normal'))

        qem_server_name_label = tk.Label(root, text = 'qem_server_name', font = ('calibre',10,'bold'))
        qem_server_name_entry=tk.Entry(root, textvariable = qem_server_name, font = ('calibre',10,'normal'))

        storage_connection_name_label = tk.Label(root, text = 'storage_connection_name', font = ('calibre',10,'bold'))
        storage_connection_name_entry=tk.Entry(root, textvariable = storage_connection_name, font = ('calibre',10,'normal'))

        source_connection_name_label = tk.Label(root, text = 'source_connection_name', font = ('calibre',10,'bold'))
        source_connection_name_entry=tk.Entry(root, textvariable = source_connection_name, font = ('calibre',10,'normal'))

        space_name_label = tk.Label(root, text = 'space_name', font = ('calibre',10,'bold'))
        space_name_entry=tk.Entry(root, textvariable = space_name, font = ('calibre',10,'normal'))

        host_label = tk.Label(root, text = 'host', font = ('calibre',10,'bold'))
        host_entry=tk.Entry(root, textvariable = host, font = ('calibre',10,'normal'))

        api_version_label = tk.Label(root, text = 'api_version', font = ('calibre',10,'bold'))
        api_version_entry=tk.Entry(root, textvariable = api_version, font = ('calibre',10,'normal'))

        bearer_token_label = tk.Label(root, text = 'bearer_token', font = ('calibre',10,'bold'))
        bearer_token_entry=tk.Entry(root, textvariable = bearer_token, font = ('calibre',10,'normal'))

        project_name_label = tk.Label(root, text = 'project_name', font = ('calibre',10,'bold'))
        project_name_entry=tk.Entry(root, textvariable = project_name, font = ('calibre',10,'normal'))

        json_path_label = tk.Label(root, text = 'json_path', font = ('calibre',10,'bold'))
        json_path_entry=tk.Entry(root, textvariable = json_path, font = ('calibre',10,'normal'))
        
        # creating a button using the widget
        # Button that will call the submit function
        sub_btn=tk.Button(root,text = 'Submit', command = submit)
          
        # placing the label and entry in
        # the required position using grid
        # method

        r1_label.grid(row=2,column=0)
        r2_label.grid(row=3,column=0)
        project_description_label.grid(row=4,column=0)
        project_description_entry.grid(row=4,column=1)
        
        landing_name_label.grid(row=5,column=0)
        landing_name_entry.grid(row=5,column=1)

        storage_name_label.grid(row=6,column=0)
        storage_name_entry.grid(row=6,column=1)

        transformation_name_label.grid(row=7,column=0)
        transformation_name_entry.grid(row=7,column=1)

        qem_server_name_label.grid(row=8,column=0)
        qem_server_name_entry.grid(row=8,column=1)

        storage_connection_name_label.grid(row=9,column=0)
        storage_connection_name_entry.grid(row=9,column=1)

        source_connection_name_label.grid(row=10,column=0)
        source_connection_name_entry.grid(row=10,column=1)

        space_name_label.grid(row=11,column=0)
        space_name_entry.grid(row=11,column=1)

        host_label.grid(row=12,column=0)
        host_entry.grid(row=12,column=1)

        api_version_label.grid(row=13,column=0)
        api_version_entry.grid(row=13,column=1)

        bearer_token_label.grid(row=14,column=0)
        bearer_token_entry.grid(row=14,column=1)

        project_name_label.grid(row=15,column=0)
        project_name_entry.grid(row=15,column=1)

        json_path_label.grid(row=16,column=0)
        json_path_entry.grid(row=16,column=1)
        
        
        
        
        sub_btn.grid(row=17,column=1)
          
        # performing an infinite loop
        # for the window to display
        root.mainloop()
        #def get_input():
        #    messagebox.showinfo("Success","Welcome to our tutorial")
        #    s = simpledialog.askstring("input string","Please enter  your name")
        #    #s1 = simpledialog.askfloat("input float","Please enter  your name")
        #    #print(s)
        #    #print(s1)
        #def selection1():
        #    messagebox.showinfo("you selected manual txt file input")
        #    s = simpledialog.askstring("input string","Please enter the path of the txt file")
        #
        #    #print(selected)
        #def selection2():
        #     messagebox.showinfo("you selected online form input")
        #     
        #root = Tk()
        #root.title('input')
        #root.iconbitmap('C:/Users/EWX/OneDrive - QlikTech Inc/Pictures/useravatar.ico')
        #Label(text="Do You want to insert the input online ?", font=('Aerial 11')).pack()
        #radio1 = tk.IntVar()
        #radio1.set(0)
        #r1=Radiobutton(root, text="No",variable=radio1, padx = 0, value=1).pack(anchor=W)
        #r2=Radiobutton(root, text="YeS",variable=radio1, padx = 0, value=2).pack(anchor=W)
        ##radiobutton=Radio1.get()
        ##print(Radio1)
        ##print(radiobutton)
        #
        ##r1=Radiobutton(root, text="Yes",padx = 0,variable=radio1 , value=1, command=selection1)
        ##r1.pack(anchor=N)
        ##print(radio1.get())
        ##r2=Radiobutton(root, text="No",padx = 0,variable=radio1 , value=2)
        ##r2.pack(anchor=N)
        ##print(radio1.get())
        ##print(r1)
        ##print(r2)
        

        #button=Button(root, text="popup", command=get_input)
        #button.pack()
        #root.geometry("500x500")
        #root.mainloop()

        return 


