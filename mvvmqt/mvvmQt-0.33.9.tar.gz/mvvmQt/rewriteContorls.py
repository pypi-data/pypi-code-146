from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel

class Widget(QWidget):
    def showType(self, isFull):
        if isFull:
            return super().showFullScreen()
        else:
            return super().show()

class Window(QMainWindow, Widget):
    pass

class Label(QLabel):
    def setTextOrPixmap(self, data):
        if type(data) == str:
            self.setText(data)
        else:
            self.setPixmap(data)