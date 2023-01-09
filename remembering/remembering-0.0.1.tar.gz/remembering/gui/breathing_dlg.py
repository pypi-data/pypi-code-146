import logging

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

import remembering.gui.mc_global

TIME_NOT_SET_FT = 0.0

MIN_SCALE_FT = 0.7
HISTORY_IB_MAX = 4.0
HISTORY_OB_MAX = 7.0
TIME_LINE_IB_DURATION_INT = 8000
TIME_LINE_OB_DURATION_INT = 16000
TIME_LINE_IB_FRAME_RANGE_INT = 1000
TIME_LINE_OB_FRAME_RANGE_INT = 2000

WINDOW_FLAGS = (
        QtCore.Qt.Dialog
        | QtCore.Qt.WindowStaysOnTopHint
        | QtCore.Qt.FramelessWindowHint
        | QtCore.Qt.WindowDoesNotAcceptFocus
        | QtCore.Qt.BypassWindowManagerHint
)

VIEW_WIDTH_INT = 330
VIEW_HEIGHT_INT = 180
BR_WIDTH_FT = 50.0
BR_HEIGHT_FT = 50.0


class BreathingDlg(QtWidgets.QGraphicsView):
    close_signal = QtCore.Signal()
    ib_signal = QtCore.Signal()
    ob_signal = QtCore.Signal()

    # Also contains the graphics scene
    def __init__(self, i_can_be_closed: bool = True):
        super().__init__()
        # i_ib_phrase: str, i_ob_phrase: str,
        self.ib_phrase_str = ""
        self.ob_phrase_str = ""

        self._can_be_closed_bool = i_can_be_closed
        self._hover_active_bool = False
        self._keyboard_active_bool = True
        self._cursor_qtimer = None
        self._cursor_move_active_bool = False
        self.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        self.setLineWidth(0)
        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)
        self._start_time_ft = TIME_NOT_SET_FT
        self._ib_length_ft_list = []
        self._ob_length_ft_list = []

        self.setWindowFlags(WINDOW_FLAGS)

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setFixedWidth(VIEW_WIDTH_INT)
        self.setFixedHeight(VIEW_HEIGHT_INT)
        t_brush = QtGui.QBrush(QtGui.QColor(remembering.gui.mc_global.MC_WHITE_COLOR_STR))
        self.setBackgroundBrush(t_brush)
        self.setRenderHints(
            QtGui.QPainter.Antialiasing |
            QtGui.QPainter.SmoothPixmapTransform
        )
        self.setAlignment(QtCore.Qt.AlignCenter)

        self._graphics_scene = QtWidgets.QGraphicsScene()
        self.setScene(self._graphics_scene)

        # Custom dynamic breathing graphic (may be possible to change this in the future)
        self._breathing_gi = BreathingGraphicsObject()
        self._graphics_scene.addItem(self._breathing_gi)
        self._breathing_gi.update_pos_and_origin_point(VIEW_WIDTH_INT, VIEW_HEIGHT_INT)
        self._breathing_gi.hover_signal.connect(self._breathing_gi_hover)
        # -Please note that for breathing in we use a static sized rectangle (instead of the one
        # the user sees),
        # this is the reason for using "hover" instead of "enter above"
        self._breathing_gi.leave_signal.connect(self._breathing_gi_leave)

        # Text
        self.text_gi = TextGraphicsItem()
        self.text_gi.setAcceptHoverEvents(
            False)  # -so that the underlying item will not be disturbed
        help_text_str = "Hover over the green box breathing in and outside the green box " \
                        "breathing out"
        self.text_gi.setHtml(remembering.gui.mc_global.get_html(help_text_str, 11))
        self.text_gi.setTextWidth(200)
        self.text_gi.update_pos_and_origin_point(VIEW_WIDTH_INT, VIEW_HEIGHT_INT)
        self.text_gi.setDefaultTextColor(
            QtGui.QColor(remembering.gui.mc_global.MC_DARKER_GREEN_COLOR_STR))
        self._graphics_scene.addItem(self.text_gi)

        self._peak_scale_ft = 1

        # self._breathing_graphicsview_l3 = CustomGraphicsView()
        self.ib_signal.connect(self._start_breathing_in)
        self.ob_signal.connect(self._start_breathing_out)

        # Set position - done after show to get the right size hint
        screen_qrect = QtGui.QGuiApplication.primaryScreen().availableGeometry()
        self._xpos_int = screen_qrect.left() + (screen_qrect.width() - VIEW_WIDTH_INT) // 2
        self._ypos_int = screen_qrect.bottom() - VIEW_HEIGHT_INT - 60
        # -self.sizeHint().height() gives only 52 here, unknown why, so we use VIEW_HEIGHT_INT
        # instead
        logging.debug("screen_qrect.bottom() = " + str(screen_qrect.bottom()))
        logging.debug("self.sizeHint().height() = " + str(self.sizeHint().height()))
        self.move(self._xpos_int, self._ypos_int)

        # Animation
        self._ib_qtimeline = QtCore.QTimeLine(duration=TIME_LINE_IB_DURATION_INT)
        self._ib_qtimeline.setFrameRange(1, TIME_LINE_IB_FRAME_RANGE_INT)
        self._ib_qtimeline.setEasingCurve(QtCore.QEasingCurve.Linear)
        self._ib_qtimeline.frameChanged.connect(
            self.frame_change_breathing_in
        )
        self._ob_qtimeline = QtCore.QTimeLine(duration=TIME_LINE_OB_DURATION_INT)
        self._ob_qtimeline.setFrameRange(1, TIME_LINE_OB_FRAME_RANGE_INT)
        self._ob_qtimeline.setEasingCurve(QtCore.QEasingCurve.Linear)
        self._ob_qtimeline.frameChanged.connect(
            self.frame_change_breathing_out
        )

        self.show()  # -done after all the widget have been added so that the right size is set
        self.raise_()
        self.activateWindow()
        self.showNormal()

    def set_io_phrases(self, i_ib: str, i_ob: str):
        self.ib_phrase_str = i_ib
        self.ob_phrase_str = i_ob

    def close_dialog(self):
        self.close_signal.emit()
        self.close()

    # overridden
    def mouseReleaseEvent(self, i_qmouseevent):
        if self._can_be_closed_bool:
            self.close_dialog()

    # overridden
    def leaveEvent(self, i_qevent):
        if self._can_be_closed_bool:
            self.close_dialog()

    def _start_breathing_in(self):
        self.text_gi.setHtml(remembering.gui.mc_global.get_html(self.ib_phrase_str))

        self._ob_qtimeline.stop()
        self._ib_qtimeline.start()

    def _start_breathing_out(self):
        self.text_gi.setHtml(remembering.gui.mc_global.get_html(self.ob_phrase_str))

        self._ib_qtimeline.stop()
        self._ob_qtimeline.start()

    # overridden
    def keyPressEvent(self, i_qkeyevent) -> None:
        if not self._keyboard_active_bool:
            return
        if i_qkeyevent.key() == QtCore.Qt.Key_Shift:
            logging.info("shift key pressed")
            self._start_breathing_in()

    # overridden
    def keyReleaseEvent(self, i_qkeyevent) -> None:
        if not self._keyboard_active_bool:
            return
        if i_qkeyevent.key() == QtCore.Qt.Key_Shift:
            logging.info("shift key released")
            self._start_breathing_out()

    def _breathing_gi_hover(self):
        if remembering.gui.mc_global.breathing_state == \
                remembering.gui.mc_global.BreathingState.breathing_in:
            return

        hover_rectangle_qsize = QtCore.QSizeF(BR_WIDTH_FT, BR_HEIGHT_FT)
        # noinspection PyCallByClass
        pos_pointf = QtWidgets.QGraphicsItem.mapFromItem(
            self._breathing_gi,
            self._breathing_gi,
            self._breathing_gi.x() + (
                        self._breathing_gi.boundingRect().width() - hover_rectangle_qsize.width(

            )) / 2,
            self._breathing_gi.y() + (
                        self._breathing_gi.boundingRect().height() -
                        hover_rectangle_qsize.height()) / 2
        )
        # -widget coords
        hover_rectangle_coords_qrect = QtCore.QRectF(pos_pointf, hover_rectangle_qsize)

        cursor = QtGui.QCursor()  # -screen coords
        cursor_pos_widget_coords_qp = self.mapFromGlobal(cursor.pos())  # -widget coords

        logging.debug("cursor.pos() = " + str(cursor.pos()))
        logging.debug("cursor_pos_widget_coords_qp = " + str(cursor_pos_widget_coords_qp))
        logging.debug("hover_rectangle_coords_qrect = " + str(hover_rectangle_coords_qrect))

        if hover_rectangle_coords_qrect.contains(cursor_pos_widget_coords_qp):
            remembering.gui.mc_global.breathing_state = \
                remembering.gui.mc_global.BreathingState.breathing_in
            self.ib_signal.emit()
            self.text_gi.update_pos_and_origin_point(VIEW_WIDTH_INT, VIEW_HEIGHT_INT)
            self._breathing_gi.update_pos_and_origin_point(VIEW_WIDTH_INT, VIEW_HEIGHT_INT)

    def _breathing_gi_leave(self):
        if remembering.gui.mc_global.breathing_state != \
                remembering.gui.mc_global.BreathingState.breathing_in:
            return
        remembering.gui.mc_global.breathing_state = \
            remembering.gui.mc_global.BreathingState.breathing_out

        self._peak_scale_ft = self._breathing_gi.scale()
        self.ob_signal.emit()
        self.text_gi.update_pos_and_origin_point(VIEW_WIDTH_INT, VIEW_HEIGHT_INT)
        self._breathing_gi.update_pos_and_origin_point(VIEW_WIDTH_INT, VIEW_HEIGHT_INT)

    def frame_change_breathing_in(self, i_frame_nr_int: int) -> None:
        phrase = "Breathing in i know i am breathing in"
        new_scale_int_ft = 1 + 0.001 * i_frame_nr_int
        self.text_gi.setScale(new_scale_int_ft)
        self._breathing_gi.setScale(new_scale_int_ft)

    def frame_change_breathing_out(self, i_frame_nr_int: int) -> None:
        phrase = "Breathing out i know i am breathing out"
        new_scale_int_ft = self._peak_scale_ft - 0.0005 * i_frame_nr_int
        if new_scale_int_ft < MIN_SCALE_FT:
            new_scale_int_ft = MIN_SCALE_FT
        self.text_gi.setScale(new_scale_int_ft)
        self._breathing_gi.setScale(new_scale_int_ft)


class TextGraphicsItem(QtWidgets.QGraphicsTextItem):
    def __init__(self):
        super().__init__()

    def update_pos_and_origin_point(self, i_view_width: int, i_view_height: int):
        t_pointf = QtCore.QPointF(
            i_view_width / 2 - self.boundingRect().width() / 2,
            i_view_height / 2 - self.boundingRect().height() / 2
        )
        self.setPos(t_pointf)

        self.setTransformOriginPoint(self.boundingRect().center())


class BreathingGraphicsObject(QtWidgets.QGraphicsObject):
    hover_signal = QtCore.Signal()
    leave_signal = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.rectf = QtCore.QRectF(0.0, 0.0, BR_WIDTH_FT, BR_HEIGHT_FT)
        self.setAcceptHoverEvents(True)

    # Overridden
    def paint(self, i_qpainter, i_qstyleoptiongraphicsitem, widget=None):
        t_brush = QtGui.QBrush(QtGui.QColor(remembering.gui.mc_global.MC_LIGHT_GREEN_COLOR_STR))
        i_qpainter.fillRect(self.rectf, t_brush)

    # Overridden
    def boundingRect(self):
        return self.rectf

    # Overridden
    def hoverMoveEvent(self, i_qgraphicsscenehoverevent):
        self.hover_signal.emit()

    # Overridden
    def hoverLeaveEvent(self, i_qgraphicsscenehoverevent):
        # Please note that this function is entered in case the user hovers over something on top
        # of this graphics item
        logging.debug("hoverLeaveEvent")
        self.leave_signal.emit()

    def update_pos_and_origin_point(self, i_view_width: int, i_view_height: int):
        t_pointf = QtCore.QPointF(
            i_view_width / 2 - self.boundingRect().width() / 2,
            i_view_height / 2 - self.boundingRect().height() / 2
        )
        self.setPos(t_pointf)

        self.setTransformOriginPoint(self.boundingRect().center())
