from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import ( 
    QLabel, 
)

from wezel import icons

class ImageLabel(QLabel):

    def __init__(self):
        super().__init__()
        self.setScaledContents(True)
        self.setData(icons.wezel)
        
    def setData(self, file):
        self.im = QPixmap(file).scaledToWidth(512)
        self.setPixmap(self.im)


