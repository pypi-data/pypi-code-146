"""Form for one time pad"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QLabel, QFormLayout
from PySide6.QtWidgets import QLineEdit, QGridLayout, QTabWidget, QWidget

from kinneyotp import OTP

class Form(QDialog):
    """Main form"""

    def __init__(self, parent=None):
        """constructor"""
        super(Form, self).__init__(parent)
        self.parent = None
        self.main = self

        self.otp = OTP()

        width = 500
        height = 200

        length = 400

        self.setMinimumSize(width, height)
        self.setWindowTitle("One Time Pad")

        main_layout = QGridLayout(self)
        self.setLayout(main_layout)

        # create a tab widget
        tab = QTabWidget(self)

        # encode page
        encode_page = QWidget(self)
        layout = QFormLayout()
        encode_page.setLayout(layout)
        self.encode_text = QLineEdit()
        self.encode_text.setFixedWidth(length)
        self.encode_key = QLineEdit()
        self.encode_key.setFixedWidth(length)
        self.encoded = QLabel()
        self.encoded.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.encode_message = QLabel()
        layout.addRow('Text:', self.encode_text)
        layout.addRow('Key:', self.encode_key)
        layout.addRow('Encoded:', self.encoded)
        layout.addRow('', self.encode_message)
        self.encode_text.textChanged.connect(self.do_encode)
        self.encode_key.textChanged.connect(self.do_encode)

        # decode page
        decode_page = QWidget(self)
        layout = QFormLayout()
        decode_page.setLayout(layout)
        self.decode_text = QLineEdit()
        self.decode_text.setFixedWidth(length)
        self.decode_key = QLineEdit()
        self.decode_key.setFixedWidth(length)
        self.decoded = QLabel()
        self.decoded.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.decode_message = QLabel()
        layout.addRow('Text to decode:', self.decode_text)
        layout.addRow('Key:', self.decode_key)
        layout.addRow('Decoded:', self.decoded)
        layout.addRow('', self.decode_message)
        self.decode_text.textChanged.connect(self.do_decode)
        self.decode_key.textChanged.connect(self.do_decode)

        # settings page
        settings_page = QWidget(self)
        layout = QFormLayout()
        settings_page.setLayout(layout)
        self.alphabet = QLabel()
        self.alphabet.setText(self.otp.alphabet)
        self.alphabet.setFixedWidth(length)
        layout.addRow('Alphabet:', self.alphabet)

        # add pane to the tab widget
        tab.addTab(encode_page, 'Encode')
        tab.addTab(decode_page, 'Decode')
        tab.addTab(settings_page, 'Settings')

        main_layout.addWidget(tab, 0, 0, 2, 1)

    def do_encode(self):
        """Try to encode using text using the key."""
        text = self.encode_text.text()
        key = self.encode_key.text()
        encoded = ""
        msg = ""
        if len(text) == len(key):
            self.otp.key = key
            msg, encoded = self.otp.encode(text)
        else:
            msg = "The length of the text and key must be the same."
        self.encoded.setText(encoded)
        self.encode_message.setText(msg)

    def do_decode(self):
        """Try to decode using the text and the key."""
        text = self.decode_text.text()
        key = self.decode_key.text()
        decoded = ""
        msg = ""
        if len(text) == len(key):
            self.otp.key = key
            msg, decoded = self.otp.decode(text)
        else:
            msg = "The length of the text and key must be the same."
        self.decoded.setText(decoded)
        self.decode_message.setText(msg)

    # pylint: disable=unused-argument
    def closeEvent(self, event):
        """Override the close event so the user can just click the close window in corner."""
        self.accept()
