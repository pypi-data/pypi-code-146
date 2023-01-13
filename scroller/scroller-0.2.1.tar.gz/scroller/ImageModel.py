from ctypes.wintypes import VARIANT_BOOL
import random
import importlib
import os
from PIL import Image
from PySide6.QtCore import QAbstractListModel, QModelIndex, QSettings, QStandardPaths, Qt, QUrl, Slot
from scroller.ManagedThreadPool import ManagedThreadPool
from scroller.Generator import Generator

class ImageModel(QAbstractListModel):
    """
    Custom model class for displaying a list of images in a QtQuick view
    """
    url = Qt.UserRole + 1
    proxyID = Qt.UserRole + 2
    ratio = Qt.UserRole + 3
    type = Qt.UserRole + 4

    def __init__(self, parent=None):
        """
        Initialize the ImageModel class
        """
        super().__init__(parent)
        self.imageData = []
        self.proxies = {}
        self.imageList = []
        self.toGenerateList = []

        self.threadPool = ManagedThreadPool()
        self.threadPool.setMaxThreadCount(10)

    @Slot(QUrl)
    def startup(self, folder: QUrl):
        """
        Set the folder containing the images to be displayed
        """
        self.setFolder(folder)

    def data(self, index, role=Qt.DisplayRole):
        """
        Return the data for the given role at the given index
        """
        row = index.row()
        if index.isValid() and 0 <= row < self.rowCount():
            if role == ImageModel.url:
                return self.imageData[row]["url"]
            elif role == ImageModel.proxyID:
                return self.imageData[row]["proxyID"]
            elif role == ImageModel.ratio:
                return self.imageData[row]["ratio"]
            elif role == ImageModel.type:
                return self.imageData[row]["type"]

    def rowCount(self, index=QModelIndex()):
        """
        Return the number of rows in the model
        """
        return len(self.imageData)

    def roleNames(self):
        """
        Return the role names for the model
        """
        return {
            ImageModel.url: b"url",
            ImageModel.proxyID: b"proxyID",
            ImageModel.ratio: b"ratio",
            ImageModel.type: b"type",
        }

    @Slot(int, result="QVariant")
    def get(self, row):
        """
        Return the image data for the given row
        """
        try:
            return self.imageData[row]
        except IndexError:
            return VARIANT_BOOL()

    def setFolder(self, folder: QUrl):
        """
        Set the folder containing the images to be displayed
        """
        folder = folder.toLocalFile() if folder.toLocalFile() else folder.toString()
        self.beginRemoveRows(QModelIndex(), 0, self.rowCount() - 1)
        self.imageData = []
        self.endRemoveRows()

        self.imageList = [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith((".jpg", ".jpeg", ".png", ".gif"))]
        random.shuffle(self.imageList)
        self.toGenerateList = self.imageList

        self.threadPool.cancelAll()

        for proxy in self.proxies.values():
            self.generateImages(count=10, proxyID=proxy.getProxyID())

    @Slot(result=QUrl)
    @Slot(bool, result=str)
    def getFolder(self, local: bool = False):
        """
        Return the current folder path
        """
        folder = QSettings().value(
                "folder",
                QStandardPaths.standardLocations(QStandardPaths.PicturesLocation)[0],
            )
        return folder if local else QUrl.fromLocalFile(folder)

    @Slot(list, result=list)
    def generateImageData(self, generationList: list, proxyID: int):
        """
        Generate image data for the given list of image paths
        """
        data = []
        for path in generationList:
            _, ext = os.path.splitext(path)
            ext = ext.lower()
            if ext in (".jpg", ".jpeg", "png"):
                type_ = "image"
            elif ext == ".gif":
                type_ = "gif"
            else:
                continue

            try:
                with Image.open(path) as img:
                    ratio = img.size[0] / img.size[1]
            except PermissionError:  # file is not readable
                continue
            data.append(
                {
                    "url": QUrl.fromLocalFile(path),
                    "ratio": ratio,
                    "proxyID": proxyID,
                    "type": type_,
                }
            )
        return data

    @Slot(result=bool)
    @Slot(int, result=bool)
    @Slot(int, int, result=bool)
    def generateImages(self, count: int = 1, proxyID: int = 0):
        """
        Generate images for the model
        """
        if count > len(self.toGenerateList):
            random.shuffle(self.imageList)
            self.toGenerateList = self.imageList
        
        self.toGenerateList, generationList = (
            self.toGenerateList[count:],
            self.toGenerateList[:count],
        )

        thread = Generator(self.generateImageData, generationList, proxyID)
        thread.signals.dataGenerated.connect(self._onDataGenerated)
        thread.signals.error.connect(self._onError)
        self.threadPool.start(thread)
        return True

    def _onDataGenerated(self, data):
        """
        Slot called when image data has been generated by a worker thread
        """
        index = self.rowCount()
        self.beginInsertRows(QModelIndex(), index, index + len(data) - 1)
        self.imageData.extend(data)
        self.endInsertRows()

    def _onError(self, error):
        """
        Slot called when an error occurs in a worker thread
        """
        print(f"An error occurred with the thread: {error}")

    @Slot(int, result=QAbstractListModel)
    def requestProxy(self, proxyID: int):
        """
        Return a new proxy object for the given proxy ID
        """
        importlib.import_module("scroller.ImageProxy")
        from scroller.ImageProxy import ImageProxy
        self.proxies[proxyID] = ImageProxy(self, proxyID)
        return self.proxies[proxyID]

    @Slot(int)
    def removeProxy(self, proxyID: int):
        """
        Slot called when a proxy object is deleted
        """
        self.proxies.pop(proxyID, None)
