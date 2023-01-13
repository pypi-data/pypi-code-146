from PySide6.QtCore import QSortFilterProxyModel, Slot
from scroller.ImageModel import ImageModel

class ImageProxy(QSortFilterProxyModel):
    """
    A proxy model that filters the images based on their proxy ID.
    """
    def __init__(self, source, proxyID):
        """
        Initializes the ImageProxy object.

        Args:
            source (ImageModel): The source model.
            proxyID (int): The proxy ID of the images to filter.
        """
        super().__init__()
        self.setSourceModel(source)
        self.proxyID = proxyID

    def filterAcceptsRow(self, source_row, source_parent):
        """
        Determines whether the image at the given row and parent should be included in the proxy model.

        Args:
            source_row (int): The row of the image in the source model.
            source_parent (QModelIndex): The parent of the image in the source model.

        Returns:
            bool: True if the image should be included in the proxy model, False otherwise.
        """
        return (
            self.sourceModel()
            .index(source_row, 0, source_parent)
            .data(ImageModel.proxyID)
            == self.proxyID
        )

    @Slot(int)
    def generateImages(self, count: int):
        """
        Generates images in the source model and filters them based on the proxy ID.

        Args:
            count (int): The number of images to generate.
        """
        self.sourceModel().generateImages(count=count, proxyID=self.proxyID)

    @Slot(result=int)
    def getProxyID(self):
        """
        Returns the proxy ID of the images in the proxy model.

        Returns:
            int: The proxy ID of the images.
        """
        return self.proxyID
