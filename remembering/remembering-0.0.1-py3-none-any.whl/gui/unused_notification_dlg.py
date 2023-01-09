from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

WINDOW_FLAGS = (
        QtCore.Qt.Dialog
        | QtCore.Qt.WindowStaysOnTopHint
        | QtCore.Qt.FramelessWindowHint
        | QtCore.Qt.WindowDoesNotAcceptFocus
        | QtCore.Qt.BypassWindowManagerHint
)

SHOWN_TIMER_TIME_INT = 10000
IMAGE_GOAL_WIDTH_INT = 70
IMAGE_GOAL_HEIGHT_INT = 70


class NotificationDlg(QtWidgets.QFrame):
    breathe_signal = QtCore.Signal()
    close_signal = QtCore.Signal()

    def __init__(self):
        super().__init__(None, WINDOW_FLAGS)

        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        self.setLineWidth(2)

        hbox_l2 = QtWidgets.QHBoxLayout()
        self.setLayout(hbox_l2)

        self._image_qll = QtWidgets.QLabel()
        hbox_l2.addWidget(self._image_qll)

        image_filename_str = "bikkhu-hands.png"
        self._image_qll.setPixmap(
            QtGui.QPixmap(mc.mc_global.get_user_images_path(image_filename_str))
        )
        self._image_qll.setScaledContents(True)
        self.resize_image()

        vbox_l3 = QtWidgets.QVBoxLayout()
        hbox_l2.addLayout(vbox_l3)

        self._prep_qll = QtWidgets.QLabel(
            self.tr("Please slow down and prepare for your breathing break. Please adjust your posture")
        )
        self._prep_qll.setWordWrap(True)
        vbox_l3.addWidget(self._prep_qll)

        hbox_l4 = QtWidgets.QHBoxLayout()
        vbox_l3.addLayout(hbox_l4)

        hbox_l4.addStretch(1)

        self.close_qpb = QtWidgets.QPushButton(self.tr("Close"))
        self.close_qpb.setFlat(True)
        self.close_qpb.setFont(mc.mc_global.get_font_small())
        self.close_qpb.clicked.connect(self.on_close_button_clicked)
        hbox_l4.addWidget(self.close_qpb)

        self.breathe_qpb = QtWidgets.QPushButton(self.tr("Show Dialog"))
        # self._breathe_qpb.setFlat(True)
        self.breathe_qpb.setFont(mc.mc_global.get_font_small())
        self.breathe_qpb.clicked.connect(self.on_breathe_button_clicked)
        hbox_l4.addWidget(self.breathe_qpb)

        if self._intro_dlg_bool:
            self.close_qpb.setDisabled(True)
            self.breathe_qpb.setDisabled(True)

        # Set position - done right before show to get the right size hint and to avoid flickering
        screen_qrect = QtWidgets.QApplication.desktop().availableGeometry()
        xpos_int = screen_qrect.right() - self.sizeHint().width() - 30
        ypos_int = screen_qrect.bottom() - self.sizeHint().height() - 30
        self.move(xpos_int, ypos_int)

        self.show()  # -done after all the widgets have been added so that the right size is set
        self.raise_()
        self.showNormal()

        self._shown_qtimer = None
        if not self._intro_dlg_bool:
            self.start_shown_timer()

    def start_shown_timer(self):
        self._shown_qtimer = QtCore.QTimer(self)  # -please remember to send "self" to the timer
        self._shown_qtimer.setSingleShot(True)
        self._shown_qtimer.timeout.connect(self.shown_timer_timeout)
        self._shown_qtimer.start(SHOWN_TIMER_TIME_INT)

    def shown_timer_timeout(self):
        self.breathe_signal.emit()
        self.close()

    # overridden
    def mousePressEvent(self, i_qmouseevent):
        if self._intro_dlg_bool:
            return
        self.on_close_button_clicked()

    def on_breathe_button_clicked(self):
        self.exit()  # -closing first to avoid collision between dialogs
        self.breathe_signal.emit()

    def on_close_button_clicked(self):
        self.exit()
        self.close_signal.emit()

    def exit(self):
        self.close()
        self._shown_qtimer.stop()

    def resize_image(self):
        if self._image_qll.pixmap() is None:
            return
        old_width_int = self._image_qll.pixmap().width()
        old_height_int = self._image_qll.pixmap().height()
        if old_width_int == 0:
            return
        width_relation_float = old_width_int / IMAGE_GOAL_WIDTH_INT
        height_relation_float = old_height_int / IMAGE_GOAL_HEIGHT_INT

        if width_relation_float > height_relation_float:
            scaled_width_int = IMAGE_GOAL_WIDTH_INT
            scaled_height_int = (scaled_width_int / old_width_int) * old_height_int
        else:
            scaled_height_int = IMAGE_GOAL_HEIGHT_INT
            scaled_width_int = (scaled_height_int / old_height_int) * old_width_int

        self._image_qll.setFixedWidth(scaled_width_int)
        self._image_qll.setFixedHeight(scaled_height_int)
