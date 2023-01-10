import os
import wezel
import dbdicom as db


def all(parent):

    parent.action(Open, shortcut='Ctrl+O')
    parent.action(Read)
    parent.action(Save, shortcut='Ctrl+S')
    parent.action(Restore, shortcut='Ctrl+R')
    parent.action(Close, shortcut='Ctrl+C')
    parent.separator()
    parent.action(OpenSubFolders, text='Open subfolders')
    parent.separator()
    parent.action(ExportAsDicom, text='Export as .dcm')
    parent.action(ExportAsCsv, text='Export as .csv')
    parent.action(ExportAsPng, text='Export as .png')
    parent.action(ExportAsNifti, text='Export as .nii')
    

class Open(wezel.Action):

    def run(self, app):
        """
        Open a DICOM folder and update display.
        """
        app.status.message("Opening DICOM folder..")
        path = app.dialog.directory("Select a DICOM folder")
        if path == '':
            app.status.message('') 
            return
        app.status.cursorToHourglass()
        app.close()
        app.open(path)
        app.status.hide()
        app.status.cursorToNormal()
        


class Close(wezel.Action):
    """
    Close wezel.
    """ 
    def enable(self, app): 
        if app.folder is None:
            return False
        return app.folder.manager.is_open()

    def run(self, app):
        closed = app.folder.close()
        if closed: 
            app.close()


class Read(wezel.Action):

    def enable(self, app): 
        if app.folder is None:
            return False  
        return app.folder.manager.is_open()

    def run(self, app):
        """
        Read the open DICOM folder.
        """
        app.status.cursorToHourglass()
        app.central.closeAllSubWindows()
        app.folder.scan()
        app.status.cursorToNormal() 
        app.refresh()


class Restore(wezel.Action):

    def enable(self, app):
        if app.folder is None:
            return False
        return app.folder.manager.is_open()

    def run(self, app):
        """
        Restore the open DICOM folder.
        """
        app.folder.restore()
        app.refresh()


class Save(wezel.Action):

    def enable(self, app):
        if app.folder is None:
            return False  
        return app.folder.manager.is_open()

    def run(self, app):
        """
        Saves the open DICOM folder.
        """
        app.folder.save()


class OpenSubFolders(wezel.Action):

    def run(self, app):
        """
        Open a DICOM folder and update display.
        """
        app.status.message("Opening DICOM folder..")
        path = app.dialog.directory("Select the top folder..")
        if path == '':
            app.status.message('') 
            return
        subfolders = next(os.walk(path))[1]
        subfolders = [os.path.join(path, f) for f in subfolders]
        app.close()
        app.status.cursorToHourglass()
        for i, path in enumerate(subfolders):
            msg = 'Reading folder ' + str(i+1) + ' of ' + str(len(subfolders))
            #app.open(path)
            app.status.message(msg)
            folder = db.database(path=path, 
                status = app.status, 
                dialog = app.dialog)
            folder.save()
        app.status.cursorToNormal()
        app.status.hide()
        app.folder = folder
        app.display(app.folder)


class ExportAsDicom(wezel.Action):
    """Export selected series"""

    def enable(self, app):
        return app.nr_selected(3) != 0

    def run(self, app):

        series = app.get_selected(3)
        if series == []:
            app.dialog.information("Please select at least one series")
            return
        path = app.dialog.directory("Where do you want to export the data?")
        for i, s in enumerate(series):
            app.status.progress(i, len(series), 'Exporting data..')
            s.export_as_dicom(path)
        app.status.hide()

class ExportAsCsv(wezel.Action):
    """Export selected series"""

    def enable(self, app):
        return app.nr_selected(3) != 0

    def run(self, app):
        series = app.get_selected(3)
        if series == []:
            app.dialog.information("Please select at least one series")
            return
        path = app.dialog.directory("Where do you want to export the data?")
        for i, s in enumerate(series):
            app.status.message('Exporting series ' + str(i))
            s.export_as_csv(path)
        app.status.hide()

class ExportAsPng(wezel.Action):
    """Export selected series"""

    def enable(self, app):
        return app.nr_selected(3) != 0

    def run(self, app):
        series = app.get_selected(3)
        if series == []:
            app.dialog.information("Please select at least one series")
            return
        path = app.dialog.directory("Where do you want to export the data?")
        for i, s in enumerate(series):
            app.status.message('Exporting series ' + str(i))
            s.export_as_png(path)
        app.status.hide()

class ExportAsNifti(wezel.Action):
    """Export selected series"""

    def enable(self, app):
        return app.nr_selected(3) != 0

    def run(self, app):
        series = app.get_selected(3)
        if series == []:
            app.dialog.information("Please select at least one series")
            return
        path = app.dialog.directory("Where do you want to export the data?")
        for i, s in enumerate(series):
            app.status.message('Exporting series ' + str(i))
            s.export_as_nifti(path)
        app.status.hide()