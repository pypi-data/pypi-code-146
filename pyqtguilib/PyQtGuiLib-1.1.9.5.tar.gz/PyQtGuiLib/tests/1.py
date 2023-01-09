import sys
from PyQt5.QtWidgets import QWidget,QApplication,QPushButton,QHBoxLayout,QTableWidget


class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(800,500)

        # 水平布局
        self.hlay = QHBoxLayout(self)

        self.btn = QPushButton("添加QWidget")
        self.btn.clicked.connect(self.addWidget)

        self.hlay.addWidget(self.btn)

    # 添加QWidget
    def addWidget(self,widget):
        widget.setStyleSheet("background-color: rgb(85, 170, 127);")
        widget.show()
        self.hlay.addWidget(widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test()
    win.show()

    sys.exit(app.exec_())