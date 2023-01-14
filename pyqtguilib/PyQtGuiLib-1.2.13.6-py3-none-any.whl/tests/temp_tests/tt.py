from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QLineEdit,
    QPushButton,
    Signal
)

'''
    测试用例的标准模板,该代码用于复制
'''
import time
import sys
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QPlainTextEdit,QTextEdit

class Test(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.resize(600,600)

        self.btn = QPushButton("输出",self)
        self.btn.clicked.connect(self.test)

        self.line = QTextEdit(self)
        self.line.move(50,50)

    def write(self,text):
        self.line.append(text)

    def test(self):
        sys.stderr = self
        print("123",file=sys.stderr,end="")
        print("456",file=sys.stderr,end="")
        print("789",file=sys.stderr,end="")
        print("147",file=sys.stderr,end="")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Test()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())