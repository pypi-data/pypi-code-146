import timeit
import random
import numpy as np
from PyQt5.QtCore import pyqtSignal

from wezel import widgets, canvas
from wezel.canvas.utils import colormap_to_LUT

class SeriesCanvas(canvas.Canvas):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._model = SeriesCanvasModel()

    def slotMaskChanged(self):
        if self._model._regions == []:
            self._model.addRegion()
            clr = self.maskItem.color()
            self._model.setColor(clr)
            if self.toolBar is not None:
                self.toolBar.newRegion()
        self.saveMask()
        if self.toolBar is not None:
            self.toolBar.maskChanged()


    def setArray(self, array, uid, center, width, colormap):
        self._model.setArray(
            uid, 
            center, 
            width, 
            colormap,
        )
        super().setImage(
            array, 
            self._model.center(), 
            self._model.width(), 
            self._model.colormap(),
        )

    def changeArray(self, array, uid, center, width, colormap):

        # Save current mask
        bin = self.maskItem.bin()
        if bin is not None:
            if self._model._regions == []:
                self.addRegion()
                if self.toolBar is not None:
                    self.toolBar.newRegion()
        self._model.setMask(bin)

        # update toolbar and display
        self._model.setArray(
            uid,
            center,
            width,
            colormap)
        if self.toolBar is not None:
            self.toolBar.setArray(
                array,
                self._model.center(), 
                self._model.width(), 
                self._model.colormap())
        super().setImage(
            array, 
            self._model.center(), 
            self._model.width(), 
            self._model.colormap())

        # get new mask
        mask = self._model.mask()
        self.setMask(mask, color=self._model.color())


    def removeCurrentRegion(self):
        currentIndex = self.currentIndex()
        self._model._regions.remove(self._model._currentRegion)
        if self._model._regions == []:
            self._model._currentRegion = None
            self.setMask(None)
        else:
            if currentIndex >= len(self._model._regions)-1:
                currentIndex = -1
            self._model._currentRegion = self._model._regions[currentIndex]
            self.setMask(self._model.mask(), color=self._model.color())
        if self.toolBar is not None:
            self.toolBar.newRegion()
        #self.newRegion.emit()

    def currentIndex(self):
        if self._model._regions == []:
            return -1
        current = self._model._currentRegion
        return self._model._regions.index(current)

    def addRegion(self):
        if self._model._regions != []: 
            self.saveMask()
        self._model.addRegion()
        self.setMask(None, color=self._model.color())
        if self.toolBar is not None:
            self.toolBar.newRegion()
        #self.newRegion.emit()

    def saveMask(self):
        self._model.setMask(self.maskItem.bin())

    def setCurrentRegion(self, index):
        self.saveMask()
        self._model._currentRegion = self._model._regions[index]
        self.setMask(self._model.mask(), color=self._model.color())
        if self.toolBar is not None:
            self.toolBar.newRegion()
        #self.newRegion.emit()

    def setCurrentRegionName(self, name):
        self._model._currentRegion['name'] = name

    def loadRegion(self):
        self._model.loadRegion()
        self.setMask(self._model.mask(), color=self._model.color())

    def setColormap(self, cmap=None):
        super().setColormap(cmap)
        self._model._cmap[self._model._currentImage] = cmap
        self._model._lut[self._model._currentImage] = self.imageItem._lut

    def setWindow(self, center=None, width=None):
        super().setWindow(center, width)
        self._model.setWindow(self.center(), self.width())

    def regionNames(self):
        return self._model.regionNames()

    def mask(self):
        return self._model.mask()




class SeriesCanvasModel:
    def __init__(self):
        self._series = None
        self._center = {}
        self._width = {}
        self._lut = {}
        self._cmap = {}
        self._regions = []
        self._currentRegion = None # dict
        self._currentImage = None # uid

    def center(self):
        return self._center[self._currentImage]

    def width(self):
        return self._width[self._currentImage]

    def lut(self):
        return self._lut[self._currentImage]

    def colormap(self):
        return self._cmap[self._currentImage]

    def setWindow(self, center, width):
        self._center[self._currentImage] = center
        self._width[self._currentImage] = width

    def setArray(self, uid, center, width, colormap):
        self._currentImage = uid
        if uid in self._center.keys():
            return
        self._center[uid] = center
        self._width[uid] = width
        self._lut[uid] = colormap_to_LUT(colormap)
        self._cmap[uid] = colormap

    def color(self):
        if self._currentRegion is None:
            return 0
        return self._currentRegion['color']

    def mask(self):
        if self._currentRegion is None:
            return
        if self._currentImage in self._currentRegion:
            return self._currentRegion[self._currentImage]

    def setMask(self, bin):
        if bin is None:
            return
        if self._currentRegion is None:
            return
        self._currentRegion[self._currentImage] = bin
        
    def setColor(self, RGB):
        if self._currentRegion is None:
            return
        self._currentRegion['color'] = RGB

    def regionNames(self):
        return [r['name'] for r in self._regions]

    def regionColors(self):
        return [r['color'] for r in self._regions]

    def addRegion(self):
        # Find unique name
        newName = "New Region"
        allNames = self.regionNames()
        count = 0
        while newName in allNames:
            count += 1 
            newName = 'New Region [' + str(count).zfill(3) + ']'
        # Add new region
        newRegion = {'name': newName, 'color': self.newColor()}
        self._regions.append(newRegion)
        self._currentRegion = newRegion

    def newColor(self):
        # Find unique color
        allColors = self.regionColors()
        colorIndex = 0
        color = self.colorFromIndex(colorIndex)
        while color in allColors:
            colorIndex += 1
            color = self.colorFromIndex(colorIndex)
        return color

    def colorFromIndex(self, color):
        # RGB color of the region
        if color == 0:
            return [255, 0, 0]
        if color == 1:
            return [0, 255, 0]
        if color == 2:
            return [0, 0, 255]
        if color == 3:
            return [0, 255, 255]
        if color == 4:
            return [255, 0, 255]
        if color == 5:
            return [255, 255, 0]
        if color == 6:
            return [0, 128, 255]
        if color == 7:
            return [255, 0, 128]
        if color == 8:
            return [128, 255, 0]
        return [
            random.randint(0,255), 
            random.randint(0,255), 
            random.randint(0,255)]


    def saveRegions(self):
        #start = timeit.default_timer()
        series = self._series
        if not series.exists():
            return
        images = series.instances()
        for region in self._regions:
            if len(region.keys()) > 2:
                roi_series = series.new_sibling(SeriesDescription=region['name'])
                for cnt, image in enumerate(images):
                    series.status.progress(cnt+1, len(images), 'Saving region '+ region['name'])
                    uid = image.SOPInstanceUID
                    if uid in region:
                        array = region[uid].astype(np.float32)
                        mask = image.copy_to(roi_series)
                        mask.set_array(array)
                        mask.WindowCenter = 0.5
                        mask.WindowWidth = 1.0
        series.status.hide()
        #print(timeit.default_timer()-start)


    def loadRegion(self):
        # Build list of series for all series in the same study
        seriesList = self._series.parent().children()
        seriesLabels = [series.instance().SeriesDescription for series in seriesList]
        # Ask the user to select series to import as regions
        input = widgets.UserInput(
            {"label":"Series:", "type":"listview", "list": seriesLabels}, 
            title = "Please select regions to load")
        if input.cancel:
            return
        seriesList = [seriesList[i] for i in input.values[0]["value"]]
        seriesLabels = [seriesLabels[i] for i in input.values[0]["value"]]
        suffix = ' mapped to ' + self._series.instance().SeriesDescription
        # Overlay each of the selected series on the displayed series
        for s, series in enumerate(seriesList):
            # Create overlay
            region, images = series.map_mask_to(self._series)
            # Add new region
            newRegion = {'name': seriesLabels[s] + suffix, 'color': self.newColor()}
            if isinstance(region, list): # If self._series has multiple slice groups
                for r, reg in enumerate(region):
                    for i, image in np.ndenumerate(images[r]):
                        if image is not None:
                            newRegion[image.SOPInstanceUID] = reg[:,:,i[0]] != 0
            else:
                for i, image in np.ndenumerate(images):
                    if image is not None:
                        newRegion[image.SOPInstanceUID] = region[:,:,i[0]] != 0
            self._regions.append(newRegion)
            self._currentRegion = newRegion