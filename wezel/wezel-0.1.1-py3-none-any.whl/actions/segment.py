import numpy as np
import wezel
from wezel.utils import dbimage, skimage, scipy


def all(parent):   
    parent.action(ThresholdAbsolute, text="Threshold (absolute values)")
    parent.action(ThresholdRelative, text="Threshold (relative values)")
    parent.action(CannyFilter, text="Canny Edge Detection")
    parent.separator()
    parent.action(BinaryFillHoles, text="Fill holes")
    parent.action(Label, text="Label structures")
    parent.separator() 
    parent.action(Watershed2DLabels, text="Watershed 2D (from labels)")
    #parent.action(Watershed3DLabels, text="Watershed 2D (from labels)")
    parent.action(Watershed2D, text="Watershed 2D (no labels)")
    parent.action(Watershed3D, text="Watershed 3D (no labels)")


class ThresholdAbsolute(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Get user input
        cancel, f = app.dialog.input(
            {"label":"low threshold (signal units)", "type":"float", "value": 0},
            {"label":"high threshold (signal units)", "type":"float", "value": 100},
            title = 'Select Thresholding settings')
        if cancel: 
            return

        # Filter series
        series = app.selected('Series')
        for sery in series:
            filtered = dbimage.threshold(
                sery, 
                low_threshold = f[0]['value'],
                high_threshold = f[1]['value'],
                method = 'absolute',
            )
            app.display(filtered)
        app.refresh()


class ThresholdRelative(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Get user input
        cancel, f = app.dialog.input(
            {"label":"low threshold (%)", "type":"float", "value": 25.0, "minimum": 0.0, 'maximum':100.0},
            {"label":"high threshold (%)", "type":"float", "value": 75.0, "minimum": 0.0, 'maximum':100.0},
            {"label":"thresholding method", "type":"dropdownlist", "list": ['Range', 'Percentile'], "value": 1},
            title = 'Select Thresholding settings')
        if cancel: 
            return
        if f[2]['value'] == 1:
            method = 'quantiles'
        else:
            method = 'range'

        # Filter series
        series = app.selected('Series')
        for sery in series:
            filtered = dbimage.threshold(
                sery, 
                low_threshold = f[0]['value']/100,
                high_threshold = f[1]['value']/100,
                method = method,
            )
            app.display(filtered)
        app.refresh()


class Watershed3D(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Calculate watershed
        series = app.selected('Series')
        for sery in series:

            desc = sery.SeriesDescription
            siblings = sery.siblings()
            sibling_desc = [s.SeriesDescription for s in siblings]

            # Get user input
            cancel, f = app.dialog.input(
                {   "label": "Number of labels: ", 
                    "type": "integer", 
                    "value": 250,
                    'minimum': 0,
                },
                {   "label": "Mask: ", 
                    "type": "dropdownlist", 
                    "list": ['Entire image'] + sibling_desc, 
                    "value": 0,
                },
                {   'label': 'Compactness: ',
                    'type': 'float',
                    'value': 0.0, 
                },
                {   'label': 'Include watershed line?',
                    'type': 'dropdownlist',
                    'list': ['Yes', 'No'],
                    'value': 1,
                },
                title = 'Select settings for watershed segmentation of ' + desc)
            if cancel: 
                return
            if f[1]['value'] == 0:
                mask = None
            else:
                mask = siblings[f[1]['value']-1]

            filtered = skimage.watershed_3d(
                sery, 
                markers = f[0]['value'],
                mask = mask,
                compactness = f[2]['value'],
                watershed_line = f[3]['value'] == 0,
            )
            app.display(filtered)

        app.refresh()


class Watershed2D(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Get user input
        cancel, f = app.dialog.input(
            {   "label": "Number of labels: ", 
                "type": "integer", 
                "value": 250,
                'minimum': 0,
            },
            {   'label': 'Compactness: ',
                'type': 'float',
                'value': 0.0, 
            },
            {   'label': 'Include watershed line?',
                'type': 'dropdownlist',
                'list': ['Yes', 'No'],
                'value': 1,
            },
            title = 'Select settings for watershed segmentation')
        if cancel: 
            return

        # Calculate watershed
        series = app.selected('Series')
        for sery in series:
            filtered = skimage.watershed_2d(
                sery, 
                markers = f[0]['value'],
                compactness = f[1]['value'],
                watershed_line = f[2]['value'] == 0,
            )
            app.display(filtered)

        app.refresh()


class Watershed2DLabels(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Filter series
        series = app.selected('Series')
        for sery in series:

            # Get user input
            desc = sery.SeriesDescription
            siblings = sery.siblings()
            sibling_desc = [s.SeriesDescription for s in siblings]
            cancel, f = app.dialog.input(
                {   "label": "Labels: ", 
                    "type": "dropdownlist", 
                    "list": ['use local minima'] + sibling_desc, 
                    "value": 0,
                },
                {   'label': 'Compactness: ',
                    'type': 'float',
                    'value': 0.0, 
                },
                {   'label': 'Include watershed line?',
                    'type': 'dropdownlist',
                    'list': ['Yes', 'No'],
                    'value': 1,
                },
                title = 'Select settings for watershed segmentation of ' + desc)
            if cancel: 
                return
            if f[0]['value'] == 0:
                markers = None
            else:
                markers = siblings[f[0]['value']-1]

             # Calculate watershed
            filtered = skimage.watershed_2d_labels(
                sery, 
                markers = markers,
                compactness = f[1]['value'],
                watershed_line = f[2]['value'] == 0,
            )
            app.display(filtered)

        app.refresh()


class Label(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Get user input
        cancel, f = app.dialog.input(
            {   "label": "Size of the structuring element", 
                "type": "dropdownlist", 
                "list": [
                        '3 pixels (plus)', 
                        '3 pixels (square)', 
                        '5 pixels (diamond)', 
                        '5 pixels (fat plus)',
                        '5 pixels (square)',
                        ], 
                "value": 0,
            },
            title = 'Select settings for image labelling.')
        if cancel: 
            return

        # update defaults
        if f[0]['value'] == 0:
            structure = np.array([   
                [0,1,0],
                [1,1,1],
                [0,1,0]])
        if f[0]['value'] == 1:
            structure = np.array([   
                [1,1,1],
                [1,1,1],
                [1,1,1]])
        elif f[0]['value'] == 2:
            structure = np.array([   
                [0,0,1,0,0],
                [0,1,1,1,0],
                [1,1,1,1,1],
                [0,1,1,1,0],
                [0,0,1,0,0]])
        elif f[0]['value'] == 3:
            structure = np.array([   
                [0,1,1,1,0],
                [1,1,1,1,1],
                [1,1,1,1,1],
                [1,1,1,1,1],
                [0,1,1,1,0]])
        elif f[0]['value'] == 4:
            structure = np.array([   
                [1,1,1,1,1],
                [1,1,1,1,1],
                [1,1,1,1,1],
                [1,1,1,1,1],
                [1,1,1,1,1]])
        
        # Filter series
        series = app.selected('Series')
        for sery in series:
            filtered = scipy.label(
                sery, 
                structure=structure
            )
            app.display(filtered)
        app.refresh()


class BinaryFillHoles(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Get user input
        cancel, f = app.dialog.input(
            {   "label": "Size of the structuring element", 
                "type": "dropdownlist", 
                "list": ['1 pixel', '3 pixels', '5 pixels'], 
                "value": 0,
            },
            title = 'Select settings for filling holes.')
        if cancel: 
            return

        # update defaults
        if f[0]['value'] == 0:
            structure = None
        elif f[0]['value'] == 1:
            structure = np.array([   
                [0,1,0],
                [1,1,1],
                [0,1,0]])
        elif f[0]['value'] == 2:
            structure = np.array([   
                [0,0,1,0,0],
                [0,1,1,1,0],
                [1,1,1,1,1],
                [0,1,1,1,0],
                [0,0,1,0,0]])
        
        # Filter series
        series = app.selected('Series')
        for sery in series:
            filtered = scipy.binary_fill_holes(
                sery, 
                structure=structure
            )
            app.display(filtered)
        app.refresh()


class CannyFilter(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Default settings
        modes = ['reflect', 'constant', 'nearest', 'mirror', 'wrap']
        sigma = 1.0
        low_threshold = 25.
        high_threshold = 75.
        mode = 1
        cval = 0.0

        # Get user input
        cancel, f = app.dialog.input(
            {"label":"sigma (standard deviation for Gaussian kernel)", "type":"float", "value":sigma, "minimum": 1.0},
            {"label":"low threshold (%)", "type":"float", "value": low_threshold, "minimum": 0.0, 'maximum':100.0},
            {"label":"high threshold (%)", "type":"float", "value": high_threshold, "minimum": 0.0, 'maximum':100.0},
            {"label":"mode (of extension at border)", "type":"dropdownlist", "list": modes, "value": mode},
            {"label":"cval (value past edges in constant mode)", "type":"float", "value":cval},
            title = 'Select Canny Edge Filter settings')
        if cancel: 
            return

        # update defaults
        sigma = f[0]['value']
        low_threshold = f[1]['value']/100
        high_threshold = f[2]['value']/100
        mode = f[3]['value']
        cval = f[4]['value']

        # Filter series
        for sery in app.selected('Series'):
            filtered = skimage.canny(
                sery, 
                sigma = sigma,
                low_threshold = low_threshold,
                high_threshold = high_threshold,
                use_quantiles = True,
                mode = modes[mode],
                cval = cval,
            )
            app.display(filtered)
        app.refresh()

