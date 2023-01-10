import wezel
from wezel.utils import scipy


def all(parent): 
    parent.action(GaussianFilter, text="Gaussian Filter")
    parent.separator()
    parent.action(UniformFilter, text="Uniform Filter")
    parent.action(MinimumFilter, text="Minimum Filter")
    parent.action(MaximumFilter, text="Maximum Filter")
    parent.action(RankFilter, text="Rank Filter")
    parent.action(PercentileFilter, text="Percentile Filter")
    parent.action(MedianFilter, text="Median Filter")
    parent.separator()
    parent.action(PrewittFilter, text="Prewitt Filter")
    parent.action(SobelFilter, text="Sobel Filter")
    parent.action(LaplaceFilter, text="Laplace Filter")
    parent.action(GaussianLaplaceFilter, text="Gaussian Laplace Filter")
    parent.action(GaussianGradientMagnitudeFilter, text="Gaussian Gradient Magnitude Filter")
    parent.separator()
    parent.action(FourierGaussianFilter, text="Fourier Gaussian Filter")
    parent.action(FourierUniformFilter, text="Fourier Uniform Filter")
    parent.action(FourierEllipsoidFilter, text="Fourier Ellipsoid Filter")



class FourierEllipsoidFilter(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Default settings
        size = 2.0

        # Get user input
        cancel, f = app.dialog.input(
            {"label":"size (of ellipsoid kernel)", "type":"float", "value":size, "minimum": 1.0},
            title = 'Select Fourier Ellipsoid Filter settings')
        if cancel: 
            return

        # update defaults
        size = f[0]['value']

        # Filter series
        series = app.selected('Series')
        for sery in series:
            resized = scipy.fourier_ellipsoid(
                sery, size,
            )
            app.display(resized)
        app.refresh()


class FourierUniformFilter(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Default settings
        size = 2.0

        # Get user input
        cancel, f = app.dialog.input(
            {"label":"size (of uniform kernel)", "type":"float", "value":size, "minimum": 1.0},
            title = 'Select Fourier Uniform Filter settings')
        if cancel: 
            return

        # update defaults
        size = f[0]['value']

        # Filter series
        series = app.selected('Series')
        for sery in series:
            resized = scipy.fourier_uniform(
                sery, size,
            )
            app.display(resized)
        app.refresh()


class FourierGaussianFilter(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Default settings
        sigma = 2.0

        # Get user input
        cancel, f = app.dialog.input(
            {"label":"sigma (standard deviation for Gaussian kernel)", "type":"float", "value":sigma, "minimum": 1.0},
            title = 'Select Fourier Gaussian Filter settings')
        if cancel: 
            return

        # update defaults
        sigma = f[0]['value']

        # Filter series
        series = app.selected('Series')
        for sery in series:
            resized = scipy.fourier_gaussian(
                sery, sigma,
            )
            app.display(resized)
        app.refresh()


class GaussianGradientMagnitudeFilter(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Default settings
        modes = ['reflect', 'constant', 'nearest', 'mirror', 'wrap']
        sigma = 2.0
        mode = 0
        cval = 0.0

        # Get user input
        cancel, f = app.dialog.input(
            {"label":"sigma (standard deviation for Gaussian kernel)", "type":"float", "value":sigma, "minimum": 1.0},
            {"label":"mode (of extension at border)", "type":"dropdownlist", "list": modes, "value": mode},
            {"label":"cval (value past edges in constant mode)", "type":"float", "value":cval},
            title = 'Select Gaussian Gradient Magnitude Filter settings')
        if cancel: 
            return

        # update defaults
        sigma = f[0]['value']
        mode = f[1]['value']
        cval = f[2]['value']

        # Filter series
        series = app.selected('Series')
        for sery in series:
            resized = scipy.gaussian_gradient_magnitude(
                sery, sigma,
                mode = modes[mode],
                cval = cval,
            )
            app.display(resized)
        app.refresh()


class GaussianLaplaceFilter(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Default settings
        modes = ['reflect', 'constant', 'nearest', 'mirror', 'wrap']
        sigma = 2.0
        mode = 1
        cval = 0.0

        # Get user input
        cancel, f = app.dialog.input(
            {"label":"sigma (standard deviation for Gaussian kernel)", "type":"float", "value":sigma, "minimum": 1.0},
            {"label":"mode (of extension at border)", "type":"dropdownlist", "list": modes, "value": mode},
            {"label":"cval (value past edges in constant mode)", "type":"float", "value":cval},
            title = 'Select Gaussian Laplace Filter settings')
        if cancel: 
            return

        # update defaults
        sigma = f[0]['value']
        mode = f[1]['value']
        cval = f[2]['value']

        # Filter series
        series = app.selected('Series')
        for sery in series:
            resized = scipy.gaussian_laplace(
                sery, sigma,
                mode = modes[mode],
                cval = cval,
            )
            app.display(resized)
        app.refresh()


class LaplaceFilter(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Default settings
        modes = ['reflect', 'constant', 'nearest', 'mirror', 'wrap']
        mode = 1
        cval = 0.0

        # Get user input
        cancel, f = app.dialog.input(
            {"label":"mode (of extension at border)", "type":"dropdownlist", "list": modes, "value": mode},
            {"label":"cval (value past edges in constant mode)", "type":"float", "value":cval},
            title = 'Select Laplace Filter settings')
        if cancel: 
            return

        # update defaults
        mode = f[0]['value']
        cval = f[1]['value']

        # Filter series
        series = app.selected('Series')
        for sery in series:
            resized = scipy.laplace(
                sery,
                mode = modes[mode],
                cval = cval,
            )
            app.display(resized)
        app.refresh()


class SobelFilter(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Default settings
        modes = ['reflect', 'constant', 'nearest', 'mirror', 'wrap']
        axis = 0
        mode = 1
        cval = 0.0

        # Get user input
        cancel, f = app.dialog.input(
            {"label":"axis", "type":"dropdownlist", "list":['Horizontal', 'Vertical'], "value":axis},
            {"label":"mode (of extension at border)", "type":"dropdownlist", "list": modes, "value": mode},
            {"label":"cval (value past edges in constant mode)", "type":"float", "value":cval},
            title = 'Select Sobel Filter settings')
        if cancel: 
            return

        # update defaults
        axis = f[0]['value']
        mode = f[1]['value']
        cval = f[2]['value']

        # Filter series
        series = app.selected('Series')
        for sery in series:
            resized = scipy.sobel_filter(
                sery,
                axis = axis,
                mode = modes[mode],
                cval = cval,
            )
            app.display(resized)
        app.refresh()


class PrewittFilter(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Default settings
        modes = ['reflect', 'constant', 'nearest', 'mirror', 'wrap']
        axis = 0
        mode = 1
        cval = 0.0

        # Get user input
        cancel, f = app.dialog.input(
            {"label":"axis", "type":"dropdownlist", "list":['Horizontal', 'Vertical'], "value":axis},
            {"label":"mode (of extension at border)", "type":"dropdownlist", "list": modes, "value": mode},
            {"label":"cval (value past edges in constant mode)", "type":"float", "value":cval},
            title = 'Select Prewitt Filter settings')
        if cancel: 
            return

        # update defaults
        axis = f[0]['value']
        mode = f[1]['value']
        cval = f[2]['value']

        # Filter series
        series = app.selected('Series')
        for sery in series:
            resized = scipy.prewitt_filter(
                sery,
                axis = axis,
                mode = modes[mode],
                cval = cval,
            )
            app.display(resized)
        app.refresh()


class MedianFilter(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Default settings
        modes = ['reflect', 'constant', 'nearest', 'mirror', 'wrap']
        size = 3
        mode = 1
        cval = 0.0
        hshift = 0
        vshift = 0

        # Get user input & check if valid
        valid = False
        while not valid:
            # Get input
            cancel, f = app.dialog.input(
                {"label":"size (of the median filter)", "type":"integer", "value":size, "minimum": 1},
                {"label":"mode (of extension at border)", "type":"dropdownlist", "list": modes, "value": mode},
                {"label":"cval (value past edges in constant mode)", "type":"float", "value":cval},
                {"label":"horizontal shift (positive = to the left)", "type":"integer", "value":hshift},
                {"label":"vertical shift (positive = downwards)", "type":"integer", "value":vshift},
                title = 'Select Median Filter settings')
            if cancel: 
                return
            # update defaults
            size = f[0]['value']
            mode = f[1]['value']
            cval = f[2]['value']
            hshift = f[3]['value']
            vshift = f[4]['value']
            # check validity
            valid = (abs(hshift) < size/2.0) and (abs(vshift) < size/2.0)
            if not valid:
                msg = 'Invalid shift value: shifts must be less than half of the size'
                app.dialog.information(msg, 'Invalid input value')

        # Filter series
        series = app.selected('Series')
        for sery in series:
            resized = scipy.median_filter(
                sery,
                size = size,
                mode = modes[mode],
                cval = cval,
                origin = [hshift, vshift],
            )
            app.display(resized)
        app.refresh()


class PercentileFilter(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Default settings
        modes = ['reflect', 'constant', 'nearest', 'mirror', 'wrap']
        percentile = 50
        size = 3
        mode = 1
        cval = 0.0
        hshift = 0
        vshift = 0

        # Get user input & check if valid
        valid = False
        while not valid:
            # Get input
            cancel, f = app.dialog.input(
                {"label":"percentile", "type":"float", "value":percentile, 'minimum':0, 'maximum':100},
                {"label":"size (of the percentile filter)", "type":"integer", "value":size, "minimum": 1},
                {"label":"mode (of extension at border)", "type":"dropdownlist", "list": modes, "value": mode},
                {"label":"cval (value past edges in constant mode)", "type":"float", "value":cval},
                {"label":"horizontal shift (positive = to the left)", "type":"integer", "value":hshift},
                {"label":"vertical shift (positive = downwards)", "type":"integer", "value":vshift},
                title = 'Select Percentile Filter settings')
            if cancel: 
                return
            # update defaults
            percentile = f[0]['value']
            size = f[1]['value']
            mode = f[2]['value']
            cval = f[3]['value']
            hshift = f[4]['value']
            vshift = f[5]['value']
            # check validity
            valid = (abs(hshift) < size/2.0) and (abs(vshift) < size/2.0)
            if not valid:
                msg = 'Invalid shift value: shifts must be less than half of the size'
                app.dialog.information(msg, 'Invalid input value')

        # Filter series
        series = app.selected('Series')
        for sery in series:
            resized = scipy.percentile_filter(
                sery, percentile,
                size = size,
                mode = modes[mode],
                cval = cval,
                origin = [hshift, vshift],
            )
            app.display(resized)
        app.refresh()


class RankFilter(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Default settings
        modes = ['reflect', 'constant', 'nearest', 'mirror', 'wrap']
        rank = 10
        size = 3
        mode = 1
        cval = 0.0
        hshift = 0
        vshift = 0

        # Get user input & check if valid
        valid = False
        while not valid:
            # Get input
            cancel, f = app.dialog.input(
                {"label":"rank", "type":"integer", "value":rank},
                {"label":"size (of the rank filter)", "type":"integer", "value":size, "minimum": 1},
                {"label":"mode (of extension at border)", "type":"dropdownlist", "list": modes, "value": mode},
                {"label":"cval (value past edges in constant mode)", "type":"float", "value":cval},
                {"label":"horizontal shift (positive = to the left)", "type":"integer", "value":hshift},
                {"label":"vertical shift (positive = downwards)", "type":"integer", "value":vshift},
                title = 'Select Rank Filter settings')
            if cancel: 
                return
            # update defaults
            rank = f[0]['value']
            size = f[1]['value']
            mode = f[2]['value']
            cval = f[3]['value']
            hshift = f[4]['value']
            vshift = f[5]['value']
            # check validity
            valid = (abs(hshift) < size/2.0) and (abs(vshift) < size/2.0)
            if not valid:
                msg = 'Invalid shift value: shifts must be less than half of the size'
                app.dialog.information(msg, 'Invalid input value')

        # Filter series
        series = app.selected('Series')
        for sery in series:
            resized = scipy.rank_filter(
                sery, rank,
                size = size,
                mode = modes[mode],
                cval = cval,
                origin = [hshift, vshift],
            )
            app.display(resized)
        app.refresh()


class MaximumFilter(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Default settings
        modes = ['reflect', 'constant', 'nearest', 'mirror', 'wrap']
        size = 3
        mode = 1
        cval = 0.0
        hshift = 0
        vshift = 0

        # Get user input & check if valid
        valid = False
        while not valid:
            # Get input
            cancel, f = app.dialog.input(
                {"label":"size (of the maximum filter)", "type":"integer", "value":size, "minimum": 1},
                {"label":"mode (of extension at border)", "type":"dropdownlist", "list": modes, "value": mode},
                {"label":"cval (value past edges in constant mode)", "type":"float", "value":cval},
                {"label":"horizontal shift (positive = to the left)", "type":"integer", "value":hshift},
                {"label":"vertical shift (positive = downwards)", "type":"integer", "value":vshift},
                title = 'Select Maximum Filter settings')
            if cancel: 
                return
            # update defaults
            size = f[0]['value']
            mode = f[1]['value']
            cval = f[2]['value']
            hshift = f[3]['value']
            vshift = f[4]['value']
            # check validity
            valid = (abs(hshift) < size/2.0) and (abs(vshift) < size/2.0)
            if not valid:
                msg = 'Invalid shift value: shifts must be less than half of the size'
                app.dialog.information(msg, 'Invalid input value')

        # Filter series
        series = app.selected('Series')
        for sery in series:
            resized = scipy.maximum_filter(
                sery, 
                size = size,
                mode = modes[mode],
                cval = cval,
                origin = [hshift, vshift],
            )
            app.display(resized)
        app.refresh()


class MinimumFilter(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Default settings
        modes = ['reflect', 'constant', 'nearest', 'mirror', 'wrap']
        size = 3
        mode = 1
        cval = 0.0
        hshift = 0
        vshift = 0

        # Get user input & check if valid
        valid = False
        while not valid:
            # Get input
            cancel, f = app.dialog.input(
                {"label":"size (of the minimum filter)", "type":"integer", "value":size, "minimum": 1},
                {"label":"mode (of extension at border)", "type":"dropdownlist", "list": modes, "value": mode},
                {"label":"cval (value past edges in constant mode)", "type":"float", "value":cval},
                {"label":"horizontal shift (positive = to the left)", "type":"integer", "value":hshift},
                {"label":"vertical shift (positive = downwards)", "type":"integer", "value":vshift},
                title = 'Select Minimum Filter settings')
            if cancel: 
                return
            # update defaults
            size = f[0]['value']
            mode = f[1]['value']
            cval = f[2]['value']
            hshift = f[3]['value']
            vshift = f[4]['value']
            # check validity
            valid = (abs(hshift) < size/2.0) and (abs(vshift) < size/2.0)
            if not valid:
                msg = 'Invalid shift value: shifts must be less than half of the size'
                app.dialog.information(msg, 'Invalid input value')

        # Filter series
        series = app.selected('Series')
        for sery in series:
            resized = scipy.minimum_filter(
                sery, 
                size = size,
                mode = modes[mode],
                cval = cval,
                origin = [hshift, vshift],
            )
            app.display(resized)
        app.refresh()


class UniformFilter(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Default settings
        modes = ['reflect', 'constant', 'nearest', 'mirror', 'wrap']
        size = 3
        mode = 1
        cval = 0.0
        hshift = 0
        vshift = 0

        # Get user input & check if valid
        valid = False
        while not valid:
            # Get input
            cancel, f = app.dialog.input(
                {"label":"size (of the uniform filter)", "type":"integer", "value":size, "minimum": 1},
                {"label":"mode (of extension at border)", "type":"dropdownlist", "list": modes, "value": mode},
                {"label":"cval (value past edges in constant mode)", "type":"float", "value":cval},
                {"label":"horizontal shift (positive = to the left)", "type":"integer", "value":hshift},
                {"label":"vertical shift (positive = downwards)", "type":"integer", "value":vshift},
                title = 'Select Uniform Filter settings')
            if cancel: 
                return
            # update defaults
            size = f[0]['value']
            mode = f[1]['value']
            cval = f[2]['value']
            hshift = f[3]['value']
            vshift = f[4]['value']
            # check validity
            valid = (abs(hshift) < size/2.0) and (abs(vshift) < size/2.0)
            if not valid:
                msg = 'Invalid shift value: shifts must be less than half of the size'
                app.dialog.information(msg, 'Invalid input value')

        # Filter series
        series = app.selected('Series')
        for sery in series:
            resized = scipy.uniform_filter(
                sery, 
                size = size,
                mode = modes[mode],
                cval = cval,
                origin = [hshift, vshift],
            )
            app.display(resized)
        app.refresh()


class GaussianFilter(wezel.Action): 

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):

        # Get user input
        modes = ['reflect', 'constant', 'nearest', 'mirror', 'wrap']
        cancel, f = app.dialog.input(
            {"label":"sigma (standard deviation for Gaussian kernel)", "type":"float", "value":2.0, "minimum": 1.0},
            {"label":"order (0 = Gaussian, n = nth derivative of Gaussian)", "type":"integer", "value":0, "minimum": 0},
            {"label":"mode (of extension at border)", "type":"dropdownlist", "list": modes, "value": 1},
            {"label":"cval (value past edges in constant mode)", "type":"float", "value":0.0},
            {"label":"truncate (at this many standard deviations)", "type":"float", "value":4.0, "minimum": 1.0},
            title = 'Select Gaussian Filter settings')
        if cancel: 
            return

        # Filter series
        series = app.selected('Series')
        for sery in series:
            resized = scipy.gaussian_filter(
                sery, f[0]['value'],
                order = f[1]['value'],
                mode = modes[f[2]['value']],
                cval = f[3]['value'],
                truncate = f[4]['value'],
            )
            app.display(resized)
        app.refresh()

