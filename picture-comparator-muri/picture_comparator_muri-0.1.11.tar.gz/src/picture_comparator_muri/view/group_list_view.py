from random import randint
from typing import Union, Optional, Iterable

from PySide6.QtCore import QModelIndex, QPersistentModelIndex, QSize, Qt, QRect, QPoint, Signal, QEvent
from PySide6.QtGui import QPainter, QResizeEvent, QMouseEvent, QPainterPath, QColor, QIcon
from PySide6.QtWidgets import QListView, QStyleOptionViewItem, QStyledItemDelegate

from picture_comparator_muri.model.display_settings import DisplaySettings
from picture_comparator_muri.model.group_selection_model import GroupSelectionModel
from picture_comparator_muri.model.image_group import ImageGroup
from picture_comparator_muri.model.image_info import ImageInfo
from picture_comparator_muri.model.utils import ThresholdFind
from picture_comparator_muri.model.watched_list import WatchedListModel
from picture_comparator_muri.resources.resources import Resources


class GroupListDelegate(QStyledItemDelegate):
    identical_groups_colors = [
        QColor.fromRgb(217, 143, 221), QColor.fromRgb(254, 254, 254), QColor.fromRgb(69, 192, 113),
        QColor.fromRgb(230, 197, 96), QColor.fromRgb(243, 79, 81), QColor.fromRgb(52, 159, 189),
        QColor.fromRgb(216, 234, 88), QColor.fromRgb(88, 234, 213), QColor.fromRgb(85, 40, 103),
        QColor.fromRgb(134, 100, 72)
    ]
    link_icon = QIcon.fromTheme('emblem-symbolic-link').pixmap(20, 20)

    def __init__(self):
        super().__init__()
        self._image_group: Optional[ImageGroup]
        self._threshold = ThresholdFind(True)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem,
              index: Union[QModelIndex, QPersistentModelIndex]) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        image: ImageInfo = index.model().data(index, Qt.DisplayRole)
        # Adjust thumbnail size if scroll bar is to be showed
        qimg = image.qimage(option.rect.size())
        painter.drawImage(option.rect, qimg)
        if image.is_link:
            link_position_x = option.rect.x() + option.rect.width() - self.link_icon.width() - 5
            link_position_y = option.rect.y() + 5
            painter.drawPixmap(link_position_x, link_position_y, self.link_icon)
        if image.selected:  # option.state & QStyle.State_Selected doesn't work correctly
            brush = option.palette.highlight()
            color = brush.color()
            color.setAlphaF(.6)
            brush.setColor(color)
            painter.fillRect(option.rect, color)
        if image.identical_group is not None:
            path = QPainterPath()
            path.addEllipse(QPoint(option.rect.x() + 10, option.rect.y() + 10), 7, 7)
            painter.pen().setWidth(2)
            painter.strokePath(path, painter.pen())
            while image.identical_group >= len(self.identical_groups_colors):
                # Unlikely to happen, so we just pick a random color
                self.identical_groups_colors.append(QColor.fromRgb(randint(0, 255), randint(0, 255), randint(0, 255)))
            painter.fillPath(path, self.identical_groups_colors[image.identical_group])
        if image.marked_for_deletion:
            icon_height = option.rect.height() // 2
            scaled = Resources.delete_marker.scaledToHeight(icon_height)
            rect = QRect(option.rect.x() + (option.rect.width() - scaled.width()) / 2,
                         option.rect.y() + (option.rect.height() - scaled.height()) / 2,
                         scaled.width(), scaled.height())
            painter.drawImage(rect, scaled)

    def _group_fits(self, height: int, limit: int, spacing: int, images: Iterable) -> bool:
        """Checks whether images should take height of widget or make a space for a scrollbar.
        @height: image height without spacing or """
        result = self._threshold.get(height)
        if result is None:
            width = 0
            for image in images:
                width += 2 * spacing
                width += image.scaled_width(height)
                result = width <= limit
                self._threshold.register(height, result)
        return result

    def sizeHint(self, option: QStyleOptionViewItem, index: Union[QModelIndex, QPersistentModelIndex]) -> QSize:
        widget: QListView = option.widget
        image: ImageInfo = index.model().data(index, Qt.DisplayRole)
        height = option.widget.height() - widget.spacing() * 2
        # Adjust thumbnail size if scroll bar is to be showed
        if not self._group_fits(height, widget.width(), widget.spacing(), widget.model().elements):
            height -= widget.horizontalScrollBar().height()
        width = image.scaled_width(height)
        size = QSize(width, height)
        return size

    def clear_cache(self):
        self._threshold.clear()


class GroupListView(QListView):
    ImageHoverChanged = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._last_hovered = ''
        model = WatchedListModel()
        selection_model = GroupSelectionModel()
        selection_model.setModel(model)
        self.setModel(model)
        self.setSelectionModel(selection_model)
        self.setItemDelegate(GroupListDelegate())
        self.setMouseTracking(True)

    def model(self) -> WatchedListModel:
        return super().model()

    def itemDelegate(self) -> GroupListDelegate:
        return super().itemDelegate()

    def set_display_settings(self, display_settings: DisplaySettings):
        if isinstance(self.selectionModel(), GroupSelectionModel):
            self.selectionModel().display_settings = display_settings

    def resizeEvent(self, e: QResizeEvent) -> None:
        super().resizeEvent(e)
        self.itemDelegate().clear_cache()
        self.model().update_view()  # Trick Qt into thinking model was changes, so positions of items are updated

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.selectionModel().press_started()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.selectionModel().press_ended()
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        index = self.indexAt(e.pos())
        if index.isValid():
            image = self.model().elements[index.row()]
            path = image.path if image else ''
        else:
            path = ''
        if self._last_hovered != path:
            self._last_hovered = path
            self.ImageHoverChanged.emit(path)

        super().mouseMoveEvent(e)

    def leaveEvent(self, event: QEvent) -> None:
        if self._last_hovered:
            self._last_hovered = ''
            self.ImageHoverChanged.emit('')
