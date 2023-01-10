import pandas as pd

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton,
    )
from PyQt5.QtGui import QIcon

from wezel import widgets, icons


class SeriesSliders(QWidget):
    """Widget with sliders to navigate through a DICOM series."""

    valueChanged = pyqtSignal(object)

    def __init__(self, series=None, image=None, dimensions=[]):  
        super().__init__()
        self._blockSignals = False
        if dimensions == []:
            self.sliderTags = ["SliceLocation","AcquisitionTime"]
        else: 
            self.sliderTags = dimensions
        self._setWidgets()
        self._setLayout()
        if series is not None:
            self.setData(series, image)

    def _setWidgets(self):

        self.slidersButton = QPushButton()
        self.slidersButton.setToolTip("Display Multiple Sliders")
        self.slidersButton.setCheckable(True)
        self.slidersButton.setIcon(QIcon(icons.slider_icon))
        self.slidersButton.clicked.connect(self._slidersButtonClicked)  

        self.instanceSlider = widgets.LabelSlider("", range(1))
        self.instanceSlider.valueChanged.connect(self._mainSliderValueChanged)

        self.sliders = [self.instanceSlider]

    def _setLayout(self):

        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignLeft  | Qt.AlignVCenter)
        self.layout.setSpacing(2)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.slidersButton)
        self.layout.addWidget(self.instanceSlider)

        self.setStyleSheet("background-color: white")
        self.setLayout(self.layout)

    def blockSignals(self, block):
        self._blockSignals = block

    def setData(self, series=None, image=None, blockSignals=False):
        restore = self._blockSignals
        self._blockSignals = blockSignals
        self.series = series
        self._readDataFrame()
        self._setSliderValueLists()
        if image is None:
            if self.series is not None:
                image = self.series.instance()
        self.setImage(image)  
        self._blockSignals = restore          

    def setSeries(self, series): 
        self.series = series
        self._readDataFrame()
        self._setSliderValueLists()
        image = self.series.instance()
        self.setImage(image)

    def setImage(self, image): 
        self.blockSignals(True) 
        self.image = image
        self._setSliderValues()
        self._sliderValueChanged()
        self.blockSignals(False) 


    def _readDataFrame(self):
        """Read the dataframe for the series.
        
        Drop tags that are not present in every instance. 
        Drop tags that appear only once.
        """
        # Add all default tags in the registry and get values
        tags = self.sliderTags.copy()  
        if self.series is None:
            self.dataFrame = pd.DataFrame([], index=[], columns=tags)
            return
        # If all required tags are in the register,
        # then just extract the register for the series;
        # else read the data from disk.
        columns = list(self.series.manager.columns)
        tags = list(set(tags + columns))
        # if set(tags) == set(columns): # integrated in dbdicom read_dataframe
        #     self.dataFrame = self.series.register()
        # else: 
        #     self.dataFrame = self.series.read_dataframe(tags)  
        self.dataFrame = self.series.read_dataframe(tags)  
        self.dataFrame.sort_values("InstanceNumber", inplace=True)
        #self.dataFrame.dropna(axis=1, inplace=True)  
        #self.dataFrame.reset_index()
        # remove tags with one unique value  
        for tag in self.sliderTags:        
            if tag in self.dataFrame: 
                values = self.dataFrame[tag].unique().tolist()
                if len(values) == 1:
                    self.dataFrame.drop(tag, axis=1, inplace=True)
        # update list of slider Tags
        for tag in self.sliderTags.copy():
            if tag not in self.dataFrame:
                self.sliderTags.remove(tag)


    def _setSliderValueLists(self):
        for slider in self._activeSliders:
            values = self.dataFrame[slider.label].unique().tolist()
            values.sort()
            slider.setValues(values)


    def _slidersButtonClicked(self):
        """Show or hide the other sliders that can be added."""

        if self.slidersButton.isChecked(): 
            # Build Checkbox sliders
            #self.slidersButton.setStyleSheet("background-color: red")
            for tag in self.sliderTags:
                tagValues = self.dataFrame[tag].unique().tolist()
                try:
                    tagValues.sort()
                except:
                    pass
                slider = widgets.CheckBoxSlider(tag, tagValues)
                slider.valueChanged.connect(self._sliderValueChanged)
                slider.stateChanged.connect(self._sliderStateChanged)
                self.layout.addWidget(slider)
                self.sliders.append(slider)
        else: 
            # Delete CheckBox sliders
            for slider in self.sliders[1:]:
                slider.deleteLater()
            self.sliders = self.sliders[:1]
            self.sliders[0].show()

    def _sliderStateChanged(self):

        if self.image is None:
            self._sliderValueChanged()
        else:
            self._setActiveSliderValues()
            self._setMainSliderValue()

    def _setSliderValues(self):
        
        if self.image is None: 
            return
        self._setActiveSliderValues()
        self._setMainSliderValue()

    def move(self, slider='first', direction=1, key='up'):
        """
        Move the sliders by one step forwards or backwards.

        Arguments
        ---------
        Specify either slider + direction, or key.

        slider : either first or second slider
        direction : either +1 (forwards) or -1 (backwards)
        key: arrow (left, right, up or down)
        """
        # Translate keyboard arrow hits to slider movement
        self._blockSignals = True
        if key is not None:
            if key == 'left':
                slider = 'first'
                direction = -1
            elif key == 'right':
                slider = 'first'
                direction = 1
            elif key == 'up':
                slider = 'second'
                direction = 1
            elif key == 'down':
                slider = 'second'
                direction = -1
        active = self._activeSliders
        if self.sliders[0].isHidden():
            if slider == 'first':
                sldr = active[0]
                index = sldr.index() + direction
                if sldr.setIndex(index):
                    self._sliderValueChanged()
            else:
                if len(active) > 1:
                    sldr = active[1]
                else:
                    sldr = active[0]
                index = sldr.index() + direction
                if sldr.setIndex(index):
                    self._sliderValueChanged()

        else: # main slider is visible

            if slider == 'first':
                sldr = self.sliders[0]
                index = sldr.index() + direction
                if sldr.setIndex(index):
                    self._mainSliderValueChanged()
            else: 
                if len(active) > 0:
                    sldr = active[0]
                    index = sldr.index() + direction
                    if sldr.setIndex(index):
                        self._sliderValueChanged()
                else:
                    sldr = self.sliders[0]
                    index = sldr.index() + direction
                    if sldr.setIndex(index):
                        self._mainSliderValueChanged()
        self._blockSignals = False


    def _setActiveSliderValues(self):

        if self.image is None: 
            return
        find = self.dataFrame.SOPInstanceUID == self.image.uid
        row = self.dataFrame.loc[find]
        for slider in self._activeSliders:
            value = row[slider.label].values[0]
            slider.setValue(value)

    def _setMainSliderValue(self):

        if self.image is None: 
            return
        imageUIDs = self._getAllSelectedImages()
        if len(imageUIDs) <= 1:
            self.sliders[0].hide()
        else:
            index = imageUIDs.index(self.image.uid)
            self.sliders[0].setValue(index)
            self.sliders[0].show()

    def _mainSliderValueChanged(self):  
        """Change the selected image"""

        imageUIDs = self._getAllSelectedImages()
        if imageUIDs == []:
            self.image = None
            self.sliders[0].hide()
        elif len(imageUIDs) == 1:
            self.image = self.series.instance(imageUIDs[0])
            self.sliders[0].hide()
        else:
            index = self.sliders[0].value()
            self.image = self.series.instance(imageUIDs[index])
        if not self._blockSignals:
            self.valueChanged.emit(self.image)

    def _sliderValueChanged(self):  
        """Change the selected image"""

        imageUIDs = self._getAllSelectedImages()
        if imageUIDs == []: 
            self.image = None
            self.sliders[0].hide()
        elif len(imageUIDs) == 1:
            self.image = self.series.instance(imageUIDs[0])
            self.sliders[0].hide()
        else:
            self.sliders[0].setValues(range(len(imageUIDs)))
            index = self.sliders[0].value()
            self.image = self.series.instance(imageUIDs[index])
            self.sliders[0].show()
        if not self._blockSignals:
            self.valueChanged.emit(self.image)


    def _getAllSelectedImages(self):
        """Get the list of all image files selected by the optional sliders"""

        selection = pd.Series( 
            index = self.dataFrame.index, 
            data = self.dataFrame.shape[0] * [True]
        )
        for slider in self._activeSliders:
            sliderSelection = self.dataFrame[slider.label] == slider.value()
            selection = selection & sliderSelection
        if not selection.any():
            return []
        else:
            return self.dataFrame.SOPInstanceUID[selection].values.tolist()

    @property
    def _activeSliders(self):
        """Create a list of all active sliders"""

        activeSliders = []
        for slider in self.sliders[1:]:
            if slider.checkBox.isChecked():
                activeSliders.append(slider)
        return activeSliders
    

