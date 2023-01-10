import sys
import threading
from tkinter import *

from QualityCompare import main

inputs = {
    'projectPath': {'type': 'text', 'label': 'Project directory', 'default_value': 'C:/...'},
    'ifcPath': {'type': 'text', 'label': 'IFC directory', 'default_value': None},
    'pcdPath': {'type': 'text', 'label': 'PCD directory', 'default_value': None},
    'outputPath': {'type': 'text', 'label': 'Output directory', 'default_value': None},

    'saveMeshes': {'type': 'bool', 'label': 'Save meshes', 'default_value': True},
    'saveMeshPcd': {'type': 'bool', 'label': 'Save mesh PCD', 'default_value': True},
    'saveCroppedPcd': {'type': 'bool', 'label': 'Save cropped PCD', 'default_value': True},
    'saveFilteredPcd': {'type': 'bool', 'label': 'Save filtered PCD', 'default_value': True},
    'saveCSV': {'type': 'bool', 'label': 'Save CSV', 'default_value': True},
    'saveExcel': {'type': 'bool', 'label': 'Save excel', 'default_value': True},
    'saveColloredBIM': {'type': 'bool', 'label': 'Save colored BIM', 'default_value': True},
    'saveColloredPcd': {'type': 'bool', 'label': 'Save colored PCD', 'default_value': True},

    'resolution': {'type': 'num', 'label': 'Resolution', 'default_value': 0.025},
}

# #AVANCED
# key = [('Wall', ["IfcWall", "IfcWindow","IfcDoor"]), ('Column', ["IfcColumn"] ), ('Beam', ["IfcBeam"]), ('Slab', ["IfcSlab","IfcCovering"]), ('Roof', ['IfcRoof']), ('Clutter', [])]
# tempPath = None

# t30 = 0.015 #LOA30 Treshold
# t20 = 0.05 #LOA20 Treshold
# t10 = 0.1 #LOA10 Treshold
# t00 =1 #Total distance treshold
# abs = True # use absolute values for percentages

# distanceTreshold = 0.1 #distance trechold for filtering
# searchRadius=0.1 #Seach radius treshold for normal matching
# dotTreshold = 0.8 #treshhold for normal matching

# p10 = 0.68 #cumulative percentage treshold LOA10
# p20 = 0.68 #cumulative percentage treshold LOA20
# p30 = 0.68 #cumulative percentage treshold LOA30

class Redirect():
    def __init__(self, widget, autoscroll=True):
        self.widget = widget
        self.autoscroll = autoscroll

    def write(self, text):
        self.widget.insert('end', text)
        if self.autoscroll:
            self.widget.see("end")

class Gui(Tk):
    def __init__(self):
        super().__init__()

        self.title("SCAN2BIM - QualityCompare")

        self.user_inputs = {}

        self.current_values = {}

        for i, key in enumerate(inputs.keys()):
            input = inputs[key]
            # adding a label to the root window
            lbl = Label(self, text = input['label'])
            lbl.grid(column = 0, row = i, padx=10, pady=10, sticky=W)

            if input['type'] == 'text' or input['type'] == 'num':
                # adding Entry Field
                txt_val = Entry(self, width=70)
                txt_val.grid(column= 1, row=i, padx=10, pady=10, sticky=E)
                if input['default_value'] is not None:
                    txt_val.insert(0, f"{input['default_value']}")
                self.user_inputs[key] = txt_val
            elif input['type'] == 'bool':
                # adding Boolean Checkbox
                var = BooleanVar()
                bool_val = Checkbutton(self, variable=var)
                bool_val.grid(column= 1, row=i, padx=10, pady=10)
                if input['default_value'] == True:
                    bool_val.select()
                self.user_inputs[key] = var

        output_lbl = Label(self, text = 'Output:')
        output_lbl.grid(column = 0, row = i+1, padx=10, pady=10, sticky=W)
        frame = Frame(self)
        frame.grid(column=0, row=i+2, columnspan=2, rowspan=2, padx=10)
        self.text = Text(frame, height=10)
        # self.text = Text(frame, height=10, state='disabled')
        self.text.pack(side='left', fill='both', expand=True)
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side='right', fill='y')
        self.text['yscrollcommand'] = scrollbar.set
        scrollbar['command'] = self.text.yview

        self.old_stdout = sys.stdout

        # self.stop = Button(self, text='Exit', width=20, height=2, bg='#ff0000', command=self.exit)
        # self.stop.grid(column= 0, row=i+4, padx=10, pady=10, sticky=W)

        self.submit = Button(self, text='Compare', width=20, height=2, bg='#6afc62', command=self.compare)
        self.submit.grid(column= 1, row=i+4, padx=10, pady=10, sticky=E)

    def update_current_values(self):
        for key, value in self.user_inputs.items():
            if inputs[key]['type'] == 'num':
                self.current_values[key] = float(value.get())
            else:
                self.current_values[key] = value.get()

    def compare(self):
        self.submit["state"] = DISABLED
        # self.stop["state"] = NORMAL
        self.update_current_values()
        self.thread = threading.Thread(target=main, args=[self.current_values])
        self.thread.daemon = True
        self.thread.start()

    # def exit(self):
    #     sys.exit()

if __name__ == "__main__":
    gui = Gui()
    sys.stdout = Redirect(gui.text)
    gui.mainloop()
    sys.stdout = gui.old_stdout
