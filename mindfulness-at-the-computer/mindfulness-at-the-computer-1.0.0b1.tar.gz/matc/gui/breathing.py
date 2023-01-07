"""
Contains breathing dialog/window as well as breathing visualizations/graphics

"""
import enum
import logging
import math
import random
import typing

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

import matc.constants
import matc.shared
import matc.state

WINDOW_FLAGS = (QtCore.Qt.Dialog | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
"""
Other flags:
* QtCore.Qt.WindowDoesNotAcceptFocus - With this it seems we don't capture keyboard events
* QtCore.Qt.BypassWindowManagerHint - With this we won't see a placement in the activity panel
"""
DLG_WIDTH = 570
DLG_HEIGHT = 290
DLG_CORNER_RADIUS = 40
DLG_BOTTOM_MARGINAL = 50

CLOSE_DIALOG_DURATION = 2500
CLOSE_DIALOG_RANGE = 250

TIME_LINE_IB_DURATION = 8000
TIME_LINE_OB_DURATION = 16000
TIME_LINE_DOT_DURATION = 1000
TIME_LINE_IB_FRAME_RANGE = 1000
TIME_LINE_OB_FRAME_RANGE = 2000
TIME_LINE_DOT_FRAME_RANGE = 255

USE_SETTINGS_BV = -1

HELP_TEXTS = [
    "You can press and hold the shift key while breathing in and letting it be while breathing out",
    "Please practice natural breathing and accept your breathing as it is (do not force it to be "
    "longer)",
    "Your breath is a bridge between your mind and body",
    "Please be aware of your posture and practice breathing with the stomach",
    "Let your breathing come first, and only afterward interact with the breathing dialog",
]


class CursorPosition(enum.Enum):
    """
    It's also possible that the cursor is inside the graphics item but outside of the initial area,
    but we don't need to send a signal for this, so it's not covered here
    """
    inside = enum.auto()  # -inside the initial/starting/minimum area of the graphics item
    outside = enum.auto()  # -outside the breathing graphics item


class BrState(enum.Enum):
    inactive = enum.auto()
    breathing_in = enum.auto()
    breathing_out = enum.auto()


class BreathingGraphicsView(QtWidgets.QGraphicsView):
    """
    GraphicsView for the breathing dialog. Contains the graphics scene. Which in turn contains this:
    * Breathing dots
    * Help text
    * Breathing visualizations --- there are different types, and the settings determine which
    one is used
    * Breathing phrases

    GraphicsView documentation: https://doc.qt.io/qt-6/qgraphicsview.html#details

    Abbreviations:
    * bv: breathing visualization
    * gi: graphics item
    * go: graphics object

    Different ways this is accessed:
    * Breathing dialog --- Created in MainObject.__init__ but only displayed later
    * Showing the breathing graphics view inside the breathing dialog..
      * ..after the intro dialog is closed:
        1. MainObject.on_intro_dialog_closed
        2. MainObject._open_br_dlg -> BreathingGraphicsView.open_dlg
        3. BreathingGraphicsView.initiate_gv
      * ..after the user chooses a new breathing phrase in systray sub-menu
        1. MainObject.on_tray_br_phrase_triggered
        2. MainObject._open_br_dlg -> BreathingGraphicsView.open_dlg
        3. BreathingGraphicsView.initiate_gv
      * ..after the user clicks on the systray notification message_title
        1. MainObject.on_tray_icon_message_clicked
        2. MainObject._open_br_dlg -> BreathingGraphicsView.open_dlg
        3. BreathingGraphicsView.initiate_gv
      * ..after the user chooses to open the breathing dialog from the systray menu
        1. MainObject.on_tray_open_breathing_dialog_triggered
        2. MainObject._open_br_dlg -> BreathingGraphicsView.open_dlg
        3. BreathingGraphicsView.initiate_gv
      * ..when starting the application
        1. main.main
        2. MainObject._open_br_dlg -> BreathingGraphicsView.open_dlg
        3. BreathingGraphicsView.initiate_gv
      * ..when testing (dialog shown only for a fraction of a second):
        1. test_main.test_breathing_dlg
        2. MainObject._open_br_dlg -> BreathingGraphicsView.open_dlg
        3. BreathingGraphicsView.initiate_gv
    * Showing the breathing graphics view inside the intro dialog
      1. intro_dlg
      2. BreathingGraphicsView.initiate_gv
    * Generating a preview bitmap for the settings dialog
      1. this.get_preview_pixmap
      2. BreathingGraphicsView.initiate_gv

    Instances of BreathingGraphicsView is created..
    * ..in the MainObject __init__ function
      * Please note: This is done only once (the dialog hidden/shown to "close"/"open")
    * ..in the intro dialog
    * ..in the settings dialog (for the pixmaps)

    Explanation of how coordinates work:
    https://forum.qt.io/topic/106003/how-to-seamlessly-place-item-into-scene-at-specific-location
    -adding-qgraphicsitem-to-scene-always-places-it-at-0-0/2

    """
    close_signal = QtCore.Signal()
    first_breathing_gi_signal = QtCore.Signal()

    def __init__(self, i_is_closeable: bool = True) -> None:
        """
        :param i_is_closeable: Used by the intro dialog
        """
        super().__init__()
        self.is_first_time_shown = True
        self.active_bv_go = None
        self.breathing_state = BrState.inactive
        self.is_closeable = i_is_closeable

        # Window setup..
        self.setWindowFlags(WINDOW_FLAGS)
        self.setWindowTitle(f"Breathing Dialog - {matc.constants.APPLICATION_PRETTY_NAME}")
        self.setWindowIcon(QtGui.QIcon(matc.shared.get_app_icon_path()))
        self.setStyleSheet(f"background-color: {matc.shared.BLACK_COLOR};")
        self.setFrameStyle(QtWidgets.QFrame.NoFrame)
        self.setFixedWidth(DLG_WIDTH)
        self.setFixedHeight(DLG_HEIGHT)
        self.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # ..rounding corners
        painter_path_mask = QtGui.QPainterPath()
        painter_path_mask.addRoundedRect(self.rect(), DLG_CORNER_RADIUS, DLG_CORNER_RADIUS)
        polygon_mask = painter_path_mask.toFillPolygon().toPolygon()
        # -.toPolygon converts from QPolygonF to QPolygon
        region_mask = QtGui.QRegion(polygon_mask)
        self.setMask(region_mask)
        # ..close dialog fade out animation
        self.close_dialog_qtimeline = QtCore.QTimeLine(duration=CLOSE_DIALOG_DURATION)
        self.close_dialog_qtimeline.setFrameRange(1, CLOSE_DIALOG_RANGE)
        self.close_dialog_qtimeline.setEasingCurve(QtCore.QEasingCurve.Linear)
        self.close_dialog_qtimeline.frameChanged.connect(self.on_close_dialog_frame_changed)
        self.close_dialog_qtimeline.finished.connect(self.on_close_dialog_qtimeline_finished)
        # Graphics and layout setup..
        # ..graphics scene
        self._graphics_scene = QtWidgets.QGraphicsScene()
        self._graphics_scene.setSceneRect(QtCore.QRectF(0, 0, DLG_WIDTH, DLG_HEIGHT))
        self.setScene(self._graphics_scene)
        # ..dots
        self.br_dots_gi_list = []
        self.dot_qtimeline = QtCore.QTimeLine(duration=TIME_LINE_DOT_DURATION)
        self.dot_qtimeline.setFrameRange(1, TIME_LINE_DOT_FRAME_RANGE)
        self.dot_qtimeline.setEasingCurve(QtCore.QEasingCurve.InOutQuad)
        self.dot_qtimeline.frameChanged.connect(self.on_dot_frame_change)
        # ..help text
        self.help_text_gi = GraphicsTextItem()
        self._graphics_scene.addItem(self.help_text_gi)
        # ..breathing phrase
        self.phrase = None
        self.br_text_gi = GraphicsTextItem()
        self._graphics_scene.addItem(self.br_text_gi)
        # ..central line
        self.central_line_gi = CentralLineQgi()
        self.central_line_gi.hide()
        self._graphics_scene.addItem(self.central_line_gi)
        # Animation time for the custom dynamic breathing graphics
        self.ib_qtimeline = QtCore.QTimeLine(duration=TIME_LINE_IB_DURATION)
        self.ib_qtimeline.setFrameRange(1, TIME_LINE_IB_FRAME_RANGE)
        self.ib_qtimeline.setEasingCurve(QtCore.QEasingCurve.Linear)
        self.ib_qtimeline.frameChanged.connect(self.on_frame_change_breathing_in)
        self.ob_qtimeline = QtCore.QTimeLine(duration=TIME_LINE_OB_DURATION)
        self.ob_qtimeline.setFrameRange(1, TIME_LINE_OB_FRAME_RANGE)
        self.ob_qtimeline.setEasingCurve(QtCore.QEasingCurve.Linear)
        self.ob_qtimeline.frameChanged.connect(self.on_frame_change_breathing_out)

    def sizeHint(self) -> QtCore.QSize:
        size_ = QtCore.QSize(DLG_WIDTH, DLG_HEIGHT)
        return size_

    def close_dlg(self):
        """
        The dialog is hidden when "closed"
        """
        # self.showNormal()  # -for MacOS. showNormal is used here rather than showMinimized to
        # avoid animation
        self.close_dialog_qtimeline.stop()
        self.ib_qtimeline.stop()
        self.ob_qtimeline.stop()
        self.hide()
        self.close_signal.emit()

    def show(self):
        raise Exception(
            "Call not supported, please call the function in super class instead, or use initiate")

    def open_dlg(self, i_phrase: typing.Optional[matc.state.BreathingPhrase] = None):
        screen_qrect = QtGui.QGuiApplication.primaryScreen().availableGeometry()
        _xpos_int = screen_qrect.left() + (screen_qrect.width() - DLG_WIDTH) // 2
        _ypos_int = screen_qrect.bottom() - DLG_HEIGHT - DLG_BOTTOM_MARGINAL
        self.move(_xpos_int, _ypos_int)
        self.close_dlg()
        self.showNormal()
        self.initiate_gv(USE_SETTINGS_BV, i_phrase)  # -continuing the setup

    def initiate_gv(self, i_br_vis: int,
            i_phrase: typing.Optional[matc.state.BreathingPhrase] = None):
        """
        If the user opens the breathing dialog, this function is called from show_breathing_dlg. It
        is also called when generating preview images for the settings dialog, and when showing the
        (interactive) breathing dialog inside the intro dialog

        TODO: Rewrite this function header documentation
        """

        super().show()
        self.setWindowOpacity(1)
        self.breathing_state = BrState.inactive
        self.phrase = i_phrase

        move_mouse_cursor: bool = matc.state.settings[matc.state.SK_MOVE_MOUSE_CURSOR]
        if move_mouse_cursor and not self.is_first_time_shown and i_br_vis == USE_SETTINGS_BV:
            screen_point = self.mapToGlobal(QtCore.QPoint(DLG_WIDTH - 75, DLG_HEIGHT // 2 + 20))
            screen = QtGui.QGuiApplication.primaryScreen()
            mouse_cursor = QtGui.QCursor()
            mouse_cursor.setPos(screen, screen_point)
            # https://doc.qt.io/qt-5/qcursor.html#setPos-1

        for br_dot in self.br_dots_gi_list:
            self._graphics_scene.removeItem(br_dot)
        self.br_dots_gi_list.clear()

        ####################################################################################

        if i_br_vis == USE_SETTINGS_BV:
            self.br_vis_id: int = matc.state.settings[matc.state.SK_BREATHING_VISUALIZATION]
            # -important that this setting is read here and stored, because we want to maintain
            # the behaviour if the user should happen to change the settings while the breathing
            # dialog is visible
        else:  # -when called from the intro dialog
            self.br_vis_id = i_br_vis

        if self.active_bv_go:
            self._graphics_scene.removeItem(self.active_bv_go)
            del self.active_bv_go
            self.active_bv_go = None

        if self.br_vis_id == matc.shared.BrVis.bar.value:
            self.active_bv_go = BreathingBarQgo()
            self.active_bv_go.position_signal.connect(self._breathing_gi_mouse_pos_changed)
        elif self.br_vis_id == matc.shared.BrVis.circle.value:
            self.active_bv_go = BreathingCircleQgo()
            self.active_bv_go.position_signal.connect(self._breathing_gi_mouse_pos_changed)
        elif self.br_vis_id == matc.shared.BrVis.line.value:
            self.active_bv_go = BreathingLineQgo()
        elif self.br_vis_id == matc.shared.BrVis.columns.value:
            self.active_bv_go = BreathingColumnRootQgo()
        else:
            raise Exception("Case not covered")
        self._graphics_scene.addItem(self.active_bv_go)
        self.active_bv_go.show()
        # self.active_bv_go.update_pos_and_origin_point()
        self.active_bv_go.setPos(QtCore.QPointF(DLG_WIDTH / 2, DLG_HEIGHT / 2))

        help_text_x = DLG_WIDTH / 2 - self.help_text_gi.boundingRect().width() / 2
        help_text_pointf = QtCore.QPointF(help_text_x, 10)
        self.help_text_gi.setPos(help_text_pointf)
        self.help_text_gi.show()

        if self.is_first_time_shown:
            help_text_str = self.active_bv_go.get_first_time_help_text()
        else:
            help_text_str = random.choice(HELP_TEXTS)
        self.help_text_gi.set_text(help_text_str)

        self.br_text_gi.setHtml(self._get_ib_ob_html())
        text_pointf = QtCore.QPointF(
            DLG_WIDTH / 2 - self.br_text_gi.boundingRect().width() / 2,
            DLG_HEIGHT - self.br_text_gi.boundingRect().height() - 10
        )
        if self.br_vis_id == matc.shared.BrVis.line.value:
            text_pointf.setY(DLG_HEIGHT / 2 - self.br_text_gi.boundingRect().height() / 2)
            self.central_line_gi.show()
        elif self.br_vis_id == matc.shared.BrVis.columns.value:
            self.central_line_gi.show()
        else:
            self.central_line_gi.hide()
        self.br_text_gi.setPos(text_pointf)

        self.is_first_time_shown = False

    @staticmethod
    def get_preview_pixmap(i_br_vis_item: matc.shared.BrVis) -> QtGui.QPixmap:
        br_gv = BreathingGraphicsView()
        br_gv.initiate_gv(i_br_vis_item.value)

        if i_br_vis_item == matc.shared.BrVis.columns:
            br_gv.active_bv_go.add_ib_column()
            br_gv.active_bv_go.change_size_br_in(300)
            br_gv.active_bv_go.add_ob_column()
            br_gv.active_bv_go.change_size_br_out(400)

            br_gv.active_bv_go.add_ib_column()
            br_gv.active_bv_go.change_size_br_in(350)
            br_gv.active_bv_go.add_ob_column()
            br_gv.active_bv_go.change_size_br_out(450)

            br_gv.active_bv_go.add_ib_column()
            br_gv.active_bv_go.change_size_br_in(150)

        br_pixmap = br_gv.grab()
        br_new_size = QtCore.QSize(br_pixmap.width() // 2, br_pixmap.height() // 2)
        br_resized_pixmap = br_pixmap.scaled(br_new_size)
        # del br_gv  # -freeing up memory just in case
        return br_resized_pixmap

    def on_close_dialog_qtimeline_finished(self):
        self.close_dlg()

    def on_close_dialog_frame_changed(self, i_frame_nr: int):
        opacity = 1.0 - i_frame_nr / CLOSE_DIALOG_RANGE
        self.setWindowOpacity(opacity)
        self.update()

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        super().mousePressEvent(event)
        event.accept()
        if self.is_closeable:
            self.close_dlg()

    def leaveEvent(self, i_qevent) -> None:
        if self.is_closeable:
            self.close_dialog_qtimeline.start()

    def enterEvent(self, i_qevent) -> None:
        self.setWindowOpacity(1)
        self.close_dialog_qtimeline.stop()

    def mouseMoveEvent(self, i_mouse_event: QtGui.QMouseEvent) -> None:
        """
        Only used by the "Columns" and "Line" visualizations. The others handle breathing in/out
        in their own
        hoverMoveEvent methods.

        :param i_mouse_event:
        """
        vis_te = (matc.shared.BrVis.columns.value,
                  matc.shared.BrVis.line.value)
        if self.br_vis_id in vis_te:
            if i_mouse_event.position().y() < DLG_HEIGHT // 2:
                self.start_breathing_in()
            else:
                self.start_breathing_out()

        super().mouseMoveEvent(i_mouse_event)  # <- SEGFAULT

    def _get_ib_ob_html(self, i_ib_focus: bool = False, i_ob_focus: bool = False) -> str:
        margin = 0
        if self.br_vis_id == matc.shared.BrVis.line.value:
            margin = 8
        ib_text = "Breathing in"
        ob_text = "Breathing out"
        if self.phrase:
            ib_text = self.phrase.in_breath
            ob_text = self.phrase.out_breath
        ib_html = matc.shared.get_html(i_text=ib_text, i_focus=i_ib_focus, i_margin=margin)
        ob_html = matc.shared.get_html(i_text=ob_text, i_focus=i_ob_focus, i_margin=margin)
        return ib_html + ob_html

    def start_breathing_in(self) -> None:
        if self.breathing_state == BrState.breathing_in:
            return
        self.breathing_state = BrState.breathing_in
        # Dots
        self.on_dot_frame_change(TIME_LINE_DOT_FRAME_RANGE)
        br_dots_gi = DotQgo(len(self.br_dots_gi_list))
        self.br_dots_gi_list.append(br_dots_gi)
        self._graphics_scene.addItem(br_dots_gi)
        for br_dot in self.br_dots_gi_list:
            br_dot.update_pos(len(self.br_dots_gi_list))
        if len(self.br_dots_gi_list) == 1:
            self.first_breathing_gi_signal.emit()
        self.dot_qtimeline.stop()
        self.dot_qtimeline.start()

        self.help_text_gi.hide()
        self.br_text_gi.setHtml(self._get_ib_ob_html(i_ib_focus=True))

        self.ob_qtimeline.stop()
        self.ib_qtimeline.start()
        self.active_bv_go.add_ib_column()

    def start_breathing_out(self) -> None:
        if self.breathing_state != BrState.breathing_in:
            return
        self.breathing_state = BrState.breathing_out

        self.br_text_gi.setHtml(self._get_ib_ob_html(i_ob_focus=True))

        self.ib_qtimeline.stop()
        self.ob_qtimeline.start()
        self.active_bv_go.add_ob_column()

    def keyPressEvent(self, i_qkeyevent) -> None:
        if i_qkeyevent.key() == QtCore.Qt.Key_Shift:
            logging.debug("shift key pressed")
            self.start_breathing_in()
        elif i_qkeyevent.key() == QtCore.Qt.Key_Return:
            logging.debug("return key pressed")
            self.close_dlg()

    def keyReleaseEvent(self, i_qkeyevent) -> None:
        if i_qkeyevent.key() == QtCore.Qt.Key_Shift:
            logging.debug("shift key released")
            self.start_breathing_out()

    def _breathing_gi_mouse_pos_changed(self, i_pos_type: int) -> None:
        """
        Only used by the breathing visualizations "cirlce" and "bar"
        """
        if i_pos_type == CursorPosition.inside.value:
            self.start_breathing_in()
        elif i_pos_type == CursorPosition.outside.value:
            self.start_breathing_out()

    def on_frame_change_breathing_in(self, i_frame_nr: int) -> None:
        self.active_bv_go.change_size_br_in(i_frame_nr)

    def on_frame_change_breathing_out(self, i_frame_nr: int) -> None:
        self.active_bv_go.change_size_br_out(i_frame_nr)

    def on_dot_frame_change(self, i_frame_nr: int) -> None:
        if len(self.br_dots_gi_list) <= 0:
            return
        last_dot_gi: DotQgo = self.br_dots_gi_list[-1]
        last_dot_gi.color.setAlpha(i_frame_nr)
        last_dot_gi.update()


class GraphicsTextItem(QtWidgets.QGraphicsTextItem):
    def __init__(self) -> None:
        super().__init__()
        self.setDefaultTextColor(QtGui.QColor(matc.shared.DARKER_GREEN_COLOR))
        self.setTextWidth(DLG_WIDTH - 20)

    def set_text(self, i_text: str):
        html_string = matc.shared.get_html(i_text)
        self.setHtml(html_string)


class DotQgo(QtWidgets.QGraphicsObject):
    DOT_RADIUS_FT = 6
    DOT_SPACING = 3
    TOP_MARGIN = 12

    def __init__(self, i_number: int):
        super().__init__()
        self.number = i_number  # -starts at 0
        self.draw_rectf = QtCore.QRectF(
            -self.DOT_RADIUS_FT, -self.DOT_RADIUS_FT,
            2 * self.DOT_RADIUS_FT, 2 * self.DOT_RADIUS_FT
        )
        self.setAcceptHoverEvents(False)
        self.color = QtGui.QColor(matc.shared.DARKER_GREEN_COLOR)
        self.color.setAlpha(0)

    def boundingRect(self):
        bounding_rect = QtCore.QRectF(-DLG_WIDTH / 2, -DLG_HEIGHT / 2, DLG_WIDTH, DLG_HEIGHT)
        return bounding_rect

    # Overridden
    def paint(self, i_qpainter: QtGui.QPainter, i_qstyleoptiongraphicsitem, widget=None) -> None:
        t_brush = QtGui.QBrush(self.color)
        i_qpainter.setBrush(t_brush)
        pen = QtGui.QPen()
        pen.setWidth(0)
        i_qpainter.setPen(pen)
        i_qpainter.drawEllipse(self.draw_rectf)

    def update_pos(self, i_total_nr: int) -> None:
        pixel_difference: int = 2 * self.DOT_RADIUS_FT + self.DOT_SPACING
        x_delta = (self.number - (i_total_nr - 1) / 2) * pixel_difference
        x: float = DLG_WIDTH / 2 + x_delta
        y: float = self.TOP_MARGIN + self.DOT_RADIUS_FT
        self.setPos(QtCore.QPointF(x, y))


class BreathingQgo(QtWidgets.QGraphicsObject):
    """
    Abstract base class for the different breathing visualizations used:
    * BreathingBarQgo - this handles hover events
    * BreathingCircleQgo - this handles hover events
    * BreathingColumn - Only used to display
    * BreathingColumnRoot - this holds several BreathingColumn objects
    * BreathingLineQgo - doesn't handle hover events. Only used to display

    > The QGraphicsObject class provides a base class for all graphics items that require
    signals, slots and properties.
    https://doc.qt.io/qt-5/qgraphicsobject.html

    Please note: *If* we need to change the boundingRect rectangle, we have to call
    updateGeometry, otherwise we may
    get an intermittent segmentation fault.
    """
    position_signal = QtCore.Signal(int)

    def change_size_br_in(self, i_frame_nr: int):
        pass

    def change_size_br_out(self, i_frame_nr: int):
        pass

    def add_ib_column(self):
        pass

    def add_ob_column(self):
        pass

    def paint(self, i_qpainter: QtGui.QPainter, i_qstyleoptiongraphicsitem, widget=None) -> None:
        raise NotImplementedError

    def __init__(self):
        super().__init__()
        self.draw_rectf = QtCore.QRectF(0, 0, 0, 0)
        self.setAcceptHoverEvents(True)

    def get_first_time_help_text(self) -> str:
        raise NotImplementedError

    def boundingRect(self):
        bounding_rect = QtCore.QRectF(-DLG_WIDTH / 2, -DLG_HEIGHT / 2, DLG_WIDTH, DLG_HEIGHT)
        return bounding_rect
        # return self.draw_rectf  # <- SEGFAULT <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    def hoverLeaveEvent(self, i_qgraphicsscenehoverevent) -> None:
        pass
        # Please note that this function is entered in case the user hovers over something
        #  on top of this graphics item
        # self.position_signal.emit(CursorPosition.outside.value)

    def hoverMoveEvent(self,
            i_qgraphicsscenehoverevent: QtWidgets.QGraphicsSceneHoverEvent) -> None:
        pass


class BreathingColumnRootQgo(BreathingQgo):
    """
    Holds multiple BreathingColumnQgo objects.

    Previously it seems that we had to store references to each of the BreathingColumns in Python
    to avoid
    intermittent segmentation fault errors.
    """

    def __init__(self):
        super().__init__()
        self.counter = 0

    def get_first_time_help_text(self) -> str:
        return "Hover over the upper half breathing in, and over the lower half breathing out"

    # Overridden
    def paint(self, i_qpainter: QtGui.QPainter, i_qstyleoptiongraphicsitem, widget=None) -> None:
        pass

    def add_ib_column(self):
        new_child_go = BreathingColumnQgo(self.counter, i_is_ib=True)
        new_child_go.hide()  # -do not show until change_size_br_[in/out]
        self.counter += 1
        # self.co_refs.append(new_child_go)
        new_child_go.setParentItem(self)

    def add_ob_column(self):
        new_child_go = BreathingColumnQgo(self.counter, i_is_ib=False)
        new_child_go.hide()
        self.counter += 1
        new_child_go.setParentItem(self)

    def update_pos(self) -> None:
        """
        Updates the position of the root item. This will also move the leaf items
        """
        x: float = DLG_WIDTH / 2
        if len(self.childItems()) > 0:
            last_child_go = self.childItems()[-1]
            x = DLG_WIDTH / 2 - last_child_go.x() / 2
        self.setX(x)

    def change_size_br_in(self, i_frame_nr: int):
        nr_of_items = len(self.childItems())
        if nr_of_items < 1:
            return
        last_child_go = self.childItems()[-1]
        last_child_go.show()
        new_height_ft = 0.1 * i_frame_nr
        old_height_ft = last_child_go.draw_rectf.height()
        if new_height_ft < old_height_ft:
            new_height_ft = old_height_ft
        last_child_go.draw_rectf.setHeight(new_height_ft)
        last_child_go.update_pos()
        last_child_go.update()  # -paint function called

        self.update_pos()

    def change_size_br_out(self, i_frame_nr: int):
        nr_of_items = len(self.childItems())
        if nr_of_items < 1:
            return
        last_child_go = self.childItems()[-1]
        last_child_go.show()
        new_height_ft = 0.1 * i_frame_nr
        old_height_ft = last_child_go.draw_rectf.height()
        if new_height_ft < old_height_ft:
            new_height_ft = old_height_ft
        last_child_go.draw_rectf.setHeight(new_height_ft)
        last_child_go.update_pos()
        last_child_go.update()  # -paint function called

    """
    With the code below we sometimes got a memeory error:
    
    RuntimeError: Internal C++ object (BreathingColumnRootQgo) already deleted.
    
    def __del__(self):
        # Cleanup to avoid memory leaks
        logging.debug("BreathingColumnRootQgo destructor - dereferencing and deleting child items")
        for child_item in self.childItems():
            child_item.setParentItem(None)
            del child_item
    """


class BreathingColumnQgo(BreathingQgo):
    COL_WIDTH = 50
    SPACING = 5

    def __init__(self, i_number: int, i_is_ib: bool = True):
        super().__init__()
        self.draw_rectf = QtCore.QRectF(-self.COL_WIDTH / 2, 0, self.COL_WIDTH, 0)
        self.number = i_number
        self.is_ib: bool = i_is_ib  # In-breath: True; Out-breath: False

    def get_first_time_help_text(self) -> str:
        raise Exception("Should not be possible to get here")

    def update_pos(self) -> None:
        x: float = (self.number // 2) * (self.SPACING + self.COL_WIDTH)
        if self.is_ib:
            y: float = - self.draw_rectf.height()
        else:
            y: float = 0
        self.setPos(QtCore.QPointF(x, y))

    # Overridden
    def paint(self, i_qpainter: QtGui.QPainter, i_qstyleoptiongraphicsitem, widget=None) -> None:
        if self.is_ib:
            color_ = QtGui.QColor(matc.shared.LIGHT_GREEN_COLOR)
        else:
            color_ = QtGui.QColor(matc.shared.DARK_GREEN_COLOR)
        t_brush = QtGui.QBrush(color_)
        i_qpainter.setBrush(t_brush)
        i_qpainter.drawRect(self.draw_rectf)


class BreathingXScaleQgo(BreathingQgo):
    def paint(self, i_qpainter: QtGui.QPainter, i_qstyleoptiongraphicsitem, widget=None) -> None:
        raise NotImplementedError

    def get_first_time_help_text(self) -> str:
        raise NotImplementedError

    def change_size_br_in(self, i_frame_nr: int):
        new_scale_x = 1 + 0.001 * i_frame_nr
        tranform_scale_x = QtGui.QTransform()
        tranform_scale_x = tranform_scale_x.scale(new_scale_x, 1)
        self.setTransform(tranform_scale_x)
        self.peak_scale = new_scale_x

    def change_size_br_out(self, i_frame_nr: int):
        new_scale_x = self.peak_scale - 0.0007 * i_frame_nr
        if new_scale_x < 1:
            new_scale_x = 1
        tranform_scale_x = QtGui.QTransform()
        tranform_scale_x = tranform_scale_x.scale(new_scale_x, 1)
        self.setTransform(tranform_scale_x)


class BreathingBarQgo(BreathingXScaleQgo):
    WIDTH = 140.0  # -minimum and starting value
    HEIGHT = 50.0
    CORNER_RADIUS = 5

    def __init__(self):
        super().__init__()
        self.draw_rectf = QtCore.QRectF(-self.WIDTH / 2, -self.HEIGHT / 2, self.WIDTH, self.HEIGHT)
        self.setTransformOriginPoint(0, 0)
        self.peak_scale: float = 1.0

    def get_first_time_help_text(self) -> str:
        return "Hover over the green area breathing in, and outside the green area breathing out"

    # Overridden
    def paint(self, i_qpainter: QtGui.QPainter, i_qstyleoptiongraphicsitem, widget=None) -> None:
        t_brush = QtGui.QBrush(QtGui.QColor(matc.shared.LIGHT_GREEN_COLOR))
        i_qpainter.setBrush(t_brush)
        i_qpainter.drawRoundedRect(self.draw_rectf, self.CORNER_RADIUS, self.CORNER_RADIUS)

    # Overridden
    def hoverMoveEvent(self,
            i_qgraphicsscenehoverevent: QtWidgets.QGraphicsSceneHoverEvent) -> None:
        """
        This will be called when the mouse cursor is within the boundingrect.

        .pos() from the event object is in item coords.
        """

        mouse_pos_item_coords_transformed = i_qgraphicsscenehoverevent.pos()
        mouse_pos_item_coords_original = self.transform().map(mouse_pos_item_coords_transformed)
        if self.draw_rectf.contains(mouse_pos_item_coords_original):
            self.position_signal.emit(CursorPosition.inside.value)
        elif not self.draw_rectf.contains(mouse_pos_item_coords_transformed):
            self.position_signal.emit(CursorPosition.outside.value)


class BreathingLineQgo(BreathingXScaleQgo):
    WIDTH = 120.0  # -minimum and starting value
    HEIGHT = 3

    def __init__(self):
        super().__init__()
        self.draw_rectf = QtCore.QRectF(-self.WIDTH / 2, -self.HEIGHT / 2, self.WIDTH, self.HEIGHT)
        self.setTransformOriginPoint(0, 0)
        self.peak_scale: float = 1.0

        color = QtGui.QColor(matc.shared.WHITE_COLOR)
        self.brush = QtGui.QBrush(color)
        self.pen = QtGui.QPen(color)

    def get_first_time_help_text(self) -> str:
        return "Hover over the upper half breathing in, and over the lower half breathing out"

    # Overridden
    def paint(self, i_qpainter: QtGui.QPainter, i_qstyleoptiongraphicsitem, widget=None) -> None:
        i_qpainter.setPen(self.pen)
        i_qpainter.setBrush(self.brush)
        i_qpainter.drawRect(self.draw_rectf)


class BreathingCircleQgo(BreathingQgo):
    """
    breathing in: ignoring the state of the circle, instead using the same starting state
    breathing out: using the state of the circle
    """
    CIRCLE_RADIUS_FT = 45.0  # -minimum and starting value

    def __init__(self):
        super().__init__()
        self.draw_rectf = QtCore.QRectF(
            -self.CIRCLE_RADIUS_FT, -self.CIRCLE_RADIUS_FT,
            2 * self.CIRCLE_RADIUS_FT, 2 * self.CIRCLE_RADIUS_FT
        )
        self.setTransformOriginPoint(0, 0)
        self.peak_scale: float = 1.0

    def get_first_time_help_text(self) -> str:
        return "Hover over the green area breathing in, and outside the green area breathing out"

    def change_size_br_in(self, i_frame_nr: int):
        new_scale = 1 + 0.001 * i_frame_nr
        self.setScale(new_scale)
        self.peak_scale = new_scale

    def change_size_br_out(self, i_frame_nr: int):
        new_scale = self.peak_scale - 0.0007 * i_frame_nr
        if new_scale < 1:
            new_scale = 1
        self.setScale(new_scale)

    # Overridden
    def paint(self, i_qpainter: QtGui.QPainter, i_qstyleoptiongraphicsitem, widget=None) -> None:
        # i_qpainter.fillRect(self.draw_rectf, t_brush)
        t_brush = QtGui.QBrush(QtGui.QColor(matc.shared.LIGHT_GREEN_COLOR))
        i_qpainter.setBrush(t_brush)
        i_qpainter.drawEllipse(self.draw_rectf)

    # Overridden
    def hoverMoveEvent(self,
            i_qgraphicsscenehoverevent: QtWidgets.QGraphicsSceneHoverEvent) -> None:
        ppos_scaled = i_qgraphicsscenehoverevent.pos()
        distance_from_center_scaled: float = math.dist([0, 0], [ppos_scaled.x(), ppos_scaled.y()])

        # logging.debug(f"{pposy=}")
        ppos_x_original = ppos_scaled.x() * self.scale()
        ppos_y_original = ppos_scaled.y() * self.scale()
        distance_from_center_original: float = math.dist([0, 0], [ppos_x_original, ppos_y_original])
        # logging.debug(f"{distance_from_center=}")

        if distance_from_center_original < self.CIRCLE_RADIUS_FT:
            self.position_signal.emit(CursorPosition.inside.value)
        elif distance_from_center_scaled > self.CIRCLE_RADIUS_FT:
            # self.draw_rectf.width() // 2
            # self.CIRCLE_RADIUS_FT
            self.position_signal.emit(CursorPosition.outside.value)


class CentralLineQgi(QtWidgets.QGraphicsItem):
    """
    Used with the columns and line visualizations.

    Please note: We have to implement boundingRect() and paint(), when subclassing QGraphicsItem
    (or QGraphicsObject)
    otherwise we will get a SIGSEGV error.

    > To write your own graphics item, you first create a subclass of QGraphicsItem, and then
    start by implementing its
    > two pure virtual public functions: boundingRect(), which returns an estimate of the area
    painted by the item, and
    > paint(), which implements the actual painting.

    https://doc.qt.io/qt-6/qgraphicsitem.html#details
    """

    def __init__(self):
        super().__init__()
        line_height = 3
        y = (DLG_HEIGHT - line_height) // 2
        self.draw_rectf = QtCore.QRectF(0, y, DLG_WIDTH, line_height)

        color = QtGui.QColor(matc.shared.DARK_GREEN_COLOR)
        self.brush = QtGui.QBrush(color)
        self.pen = QtGui.QPen(color)

    def boundingRect(self):
        return self.draw_rectf

    # Overridden
    def paint(self, i_qpainter: QtGui.QPainter, i_qstyleoptiongraphicsitem, widget=None) -> None:
        i_qpainter.setPen(self.pen)
        i_qpainter.setBrush(self.brush)
        i_qpainter.drawRect(self.draw_rectf)


if __name__ == "__main__":  # pragma no cover
    import sys

    matc_qapplication = QtWidgets.QApplication(sys.argv)
    bgv = BreathingGraphicsView()
    bgv.setWindowFlags(WINDOW_FLAGS)
    bgv.open_dlg()
    matc_qapplication.exec()
