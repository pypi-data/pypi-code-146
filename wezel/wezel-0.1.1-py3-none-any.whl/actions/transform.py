import wezel
from wezel.utils import skimage, scipy


def all(parent): 
    parent.action(FourierShift, text="Shift image")
    parent.separator()
    parent.action(Zoom, text="Resample images")
    parent.action(Resample3Disotropic, text="Resample 3D volume (isotropic)")
    parent.action(Resample3D, text="Resample 3D volume")
    parent.separator()
    parent.action(ResliceAxial, text='Reslice (axial)')
    parent.action(ResliceCoronal, text='Reslice (coronal)')
    parent.action(ResliceSagittal, text='Reslice (sagittal)')
    parent.separator()
    parent.action(OverlayOn, text='Overlay on..')
    parent.action(CoregisterTo, text='Coregister to..')
    parent.separator()
    parent.action(CoregisterSeries, text='Align time series')
    parent.action(MDRegConstant2D, text='Align time series (mdreg 2D - constant)')
    parent.action(MDRegConstant3D, text='Align time series (mdreg 3D - constant)')



class FourierShift(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Default settings
        hshift = 64
        vshift = 64

        # Get user input
        cancel, f = app.dialog.input(
            {"label":"horizontal shift", "type":"float", "value":hshift},
            {"label":"vertical shift", "type":"float", "value":vshift},
            title = 'Select Sobel Filter settings')
        if cancel: 
            return

        # update defaults
        hshift = f[0]['value']
        vshift = f[1]['value']

        # Filter series
        series = app.selected('Series')
        for sery in series:
            resized = scipy.fourier_shift(
                sery, [hshift, vshift],
            )
            app.display(resized)
        app.refresh()


class Zoom(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Get user input
        cancel, f = app.dialog.input(
            {"type":"float", "label":"Resize with factor..", "value":2.0, "minimum": 0},
            title='Select parameter ranges')
        if cancel: 
            return
        factor = f[0]['value']

        # Resize series
        series = app.selected('Series')
        for sery in series:
            resized = scipy.zoom(sery, factor)
            app.display(resized)
        app.refresh()


class OverlayOn(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        for series in app.selected('Series'):
            seriesList = series.parent().children()
            seriesLabels = [s.instance().SeriesDescription for s in seriesList]
            input = wezel.widgets.UserInput(
                {"label":"Overlay on which series?", "type":"dropdownlist", "list": seriesLabels, 'value':0}, 
                title = "Please select underlay series")
            if input.cancel:
                return
            underlay = seriesList[input.values[0]["value"]]
            mapped = series.map_to(underlay)
            app.display(mapped)
        app.refresh()


class Resample3D(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        for series in app.selected('Series'):
            input = wezel.widgets.UserInput(
                {"label":"New voxel size in mm (height)", "type":"float", 'value':1.0, 'minimum':0.01}, 
                {"label":"New voxel size in mm (width)", "type":"float", 'value':1.0, 'minimum':0.01},
                {"label":"New voxel size in mm (depth)", "type":"float", 'value':1.0, 'minimum':0.01},
                title = "Please select new voxel size")
            if input.cancel:
                return
            voxel_size = [
                input.values[0]["value"], 
                input.values[1]["value"], 
                input.values[2]["value"]]
            resliced = scipy.resample(series, voxel_size=voxel_size)
            app.display(resliced)
        app.refresh()


class Resample3Disotropic(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        for series in app.selected('Series'):
            input = wezel.widgets.UserInput(
                {"label":"New voxel size (mm)", "type":"float", 'value':1.0, 'minimum':0.01}, 
                title = "Please select new voxel size")
            if input.cancel:
                return
            voxel_size = [
                input.values[0]["value"], 
                input.values[0]["value"], 
                input.values[0]["value"]]
            resliced = scipy.resample(series, voxel_size=voxel_size)
            app.display(resliced)
        app.refresh()


class ResliceAxial(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        for series in app.selected('Series'):
            resliced = scipy.reslice(series, orientation='axial')
            app.display(resliced)
        app.refresh()


class ResliceCoronal(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        for series in app.selected('Series'):
            resliced = scipy.reslice(series, orientation='coronal')
            app.display(resliced)
        app.refresh()


class ResliceSagittal(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        for series in app.selected('Series'):
            resliced = scipy.reslice(series, orientation='sagittal')
            app.display(resliced)
        app.refresh()


class CoregisterTo(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        for series in app.selected('Series'):
            seriesList = series.parent().children()
            seriesLabels = [s.instance().SeriesDescription for s in seriesList]
            input = wezel.widgets.UserInput(
                {"label":"Coregister to which fixed series?", "type":"dropdownlist", "list": seriesLabels, 'value':0},
                {"label":"Attachment (smaller = smoother)", "type":"float", 'value':0.1, 'minimum':0.0}, 
                title = "Please select fixed series")
            if input.cancel:
                return
            fixed = seriesList[input.values[0]["value"]]
            coregistered = skimage.coregister(series, fixed, attachment=input.values[1]["value"])
            app.display(coregistered)
        app.refresh()


class CoregisterSeries(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        input = wezel.widgets.UserInput(
            {"label":"Attachment (smaller = smoother)", "type":"float", 'value':0.1, 'minimum':0.0}, 
            title = "Please select coregistration settings")
        if input.cancel:
            return
        for series in app.selected('Series'):
            coregistered = skimage.coregister_series(series, attachment=input.values[0]["value"])
            app.display(coregistered)
        app.refresh()


class MDRegConstant2D(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        input = wezel.widgets.UserInput(
            {"label":"Attachment (smaller = smoother)", "type":"float", 'value':0.1, 'minimum':0.0}, 
            {"label":"Stop when improvement is less than (pixelsizes):", "type":"float", 'value':1.0, 'minimum':0},
            {"label":"Maximum number of iterations", "type":"integer", 'value':10, 'minimum':1}, 
            title = "Please select coregistration settings")
        if input.cancel:
            return
        for series in app.selected('Series'):
            coregistered = skimage.mdreg_constant_2d(series, 
                attachment = input.values[0]["value"],
                max_improvement = input.values[1]["value"],
                max_iter = input.values[2]["value"])
            app.display(coregistered)
        app.refresh()


class MDRegConstant3D(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        input = wezel.widgets.UserInput(
            {"label":"Attachment (smaller = smoother)", "type":"float", 'value':0.1, 'minimum':0.0}, 
            {"label":"Stop when improvement is less than (pixelsizes):", "type":"float", 'value':1.0, 'minimum':0},
            {"label":"Maximum number of iterations", "type":"integer", 'value':10, 'minimum':1}, 
            title = "Please select coregistration settings")
        if input.cancel:
            return
        for series in app.selected('Series'):
            coregistered = skimage.mdreg_constant_3d(series, 
                attachment = input.values[0]["value"],
                max_improvement = input.values[1]["value"],
                max_iter = input.values[2]["value"])
            app.display(coregistered)
        app.refresh()



