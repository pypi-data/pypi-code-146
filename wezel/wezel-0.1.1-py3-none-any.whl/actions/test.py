import wezel
import time
import numpy as np
import os

def test_Function(start, end, signals):
  signals.log.emit("Calculation Started")
  for n in range(start, end):
    time.sleep(1)
    signals.log.emit("Message " + str(n))  
  return "Result of the calculation"


def test_Copy(series_list, signals):
    signals.log.emit("Copying {} series".format(len(series_list)))      
    for series in series_list:
        signals.log.emit('Copying {}'.format(series.label()))
        series.copy()  
    return "Copying complete"


def test_export(series, path,signals):
    signals.log.emit("Start exporting series")
    for s in series:
        signals.log.emit("Exporting {} series to {}".format(s.label(), path))
        s.export(path)
    return "Series export complete"   


def test_array_copy(start, end, signals):
    signals.log.emit("Copying arrays started")      
    for n in range(start, end):
        time.sleep(1)
        first_array=np.arange(n)
        second_array=np.copy(first_array)
        signals.log.emit("{} copied".format(first_array)) 
    return "Array copying complete"


def test_file_write(signals):
    try:
        if not os.path.exists("C:\\FileDemo\\"):
            os.makedirs("C:\\FileDemo\\")
            signals.log.emit("Directory created")
        with open('C:\\FileDemo\\myfile.txt', 'w+') as f:
            f.write('Create a new text file!')
        signals.log.emit("File created") 
        for n in range(10):
            time.sleep(1)
            with open("C:\\FileDemo\\myfile.txt", "a") as f:
                f.write("\n This text was added using Append.")
            signals.log.emit("Text appended to file")
        return "File operations finished"
    except FileNotFoundError:
        signals.log.emit("File myfile.txt does not exist")
        return "Terminated by error"

        

def all(parent):
    parent.action(Test_UserInput, text='Test UserInput')
    parent.action(Test_LoggingToGUI, text='Test Logging to GUI')
    parent.action(Test_ArrayCopy, text='Test Array Copy & Logging to GUI')
    parent.action(Test_FileWrite, text='Test Write to File & Logging to GUI')
    parent.action(Test_Copy, text='Test Copy Series & Logging to GUI')
    parent.action(Test_Export, text='Test Export Series & Logging to GUI')
    
    

class Test_FileWrite(wezel.Action):
    def run(self, app):
        window = wezel.widgets.LoggingWidget(test_file_write)
        app.addAsSubWindow(window, "Test File Write and Logging to GUI")


class Test_LoggingToGUI(wezel.Action):
    def run(self, app):
        window = wezel.widgets.LoggingWidget(test_Function, start=1,end=10)
        app.addAsSubWindow(window, "Test Logging to GUI")


class Test_UserInput(wezel.Action):
    def run(self, app): 
        filters = ["Gaussian", "Uniform", "Median", "Maximum", "Wiener"]
        flavours = ["Chocolate", "Vanilla", "Strawberry"]

        cancel, input = app.dialog.input(
            {"label":"Which filter?", "type":"listview", "list": filters},
            {"label":"Which filter?", "type":"dropdownlist", "list": filters, "value": 2},
            {"label":"Which flavour?", "type":"dropdownlist", "list": flavours},
            {"label":"Filter size in pixels", "type":"float"},
            {"label":"Type a string", "type":"string","value":"hello world!"},
            {"label":"Which flavour?", "type":"listview", "list":flavours},
            {"label":"An integer between 0 and 1000", "type":"integer", "value":20, "minimum": 0, "maximum": 1000}, 
            {"label":"An integer larger than -100", "type":"float", "value":20, "minimum": -100}, 
            {"label":"An integer less than 1000", "type":"integer", "value":30, "maximum": 1000},
            {"label":"Any integer", "type":"integer", "value":40},
            {"label":"Any integer", "type":"integer"},
            {"label":"Type a string", "type":"string","value":"hello world!"},
            title = "Can we have some input?")
        if not cancel: 
            for field in input:
                print(field["label"], ': ', field["value"])


class Test_Copy(wezel.Action):
    def enable(self, app):
        return app.nr_selected(3) != 0

    def run(self, app):
        series_list = app.get_selected(3)
        window = wezel.widgets.LoggingWidget(test_Copy, series_list=series_list)
        app.addAsSubWindow(window, "Test Logging to GUI while copying DICOM series")
       

class Test_ArrayCopy(wezel.Action):  
    def run(self, app):
        window = wezel.widgets.LoggingWidget(test_array_copy, start=10,end=20)
        app.addAsSubWindow(window, "Test Logging to GUI while copying numpy arrays")


class Test_Export(wezel.Action):
    """Export selected series"""

    def enable(self, app):
        return app.nr_selected(3) != 0

    def run(self, app):
        series = app.get_selected(3)
        path = app.dialog.directory("Where do you want to export the data?")
        window = wezel.widgets.LoggingWidget(test_export, series=series, path=path)
        app.addAsSubWindow(window, "Test Logging to GUI while copying numpy arrays")