from typing import Union, Optional, Dict

from PySide6.QtCore import QModelIndex, QPersistentModelIndex, Qt, QSize
from PySide6.QtGui import QPainter, QImage
from PySide6.QtWidgets import QGridLayout, QScrollArea, QListView, QAbstractItemDelegate, QStyleOptionViewItem, QStyle, \
    QWidget, QAbstractItemView

from picture_comparator_muri.model.image_group import ImageGroup
from picture_comparator_muri.model.watched_list import WatchedList, WatchedListModel


class MatchesView:  # TODO; Think what to do with it, after stack view is added
    def __init__(self):
        super().__init__()


class ListMatchDelegate(QAbstractItemDelegate):
    img_size = 120
    padding = 5

    def __init__(self):
        super().__init__()
        self._cache: Dict = {}

    def _get_group_bitmap(self, image_group: ImageGroup):
        pixmap = self._cache.get(image_group)
        if not pixmap:
            thumbs = []
            width = self.padding * (len(image_group) + 1)
            max_height = 0
            for image in image_group:
                qimg = QImage(image.path)
                if qimg.width() > qimg.height():
                    qimg = qimg.scaledToWidth(self.img_size)
                else:
                    qimg = qimg.scaledToHeight(self.img_size)
                thumbs.append(qimg)
                width += qimg.width()
                max_height = max(max_height, qimg.height())
            pixmap = QImage(width, max_height + 2 * self.padding, QImage.Format_ARGB32)
            pixmap.fill(0x00000000)
            painter = QPainter(pixmap)
            x = self.padding
            for qimg in thumbs:
                painter.drawImage(x, self.padding, qimg)
                painter.drawRect(x, self.padding, qimg.width(), qimg.height())
                x += qimg.width() + self.padding
            self._cache[image_group] = pixmap
        return pixmap

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: Union[QModelIndex, QPersistentModelIndex]) -> None:
        image_group: ImageGroup = index.model().data(index, Qt.DisplayRole)
        pixmap = self._get_group_bitmap(image_group)
        painter.drawImage(option.rect.x(), option.rect.y(), pixmap)
        if option.state & QStyle.State_Selected:
            brush = option.palette.highlight()
            color = brush.color()
            color.setAlphaF(.6)
            brush.setColor(color)
            painter.fillRect(option.rect, color)

    def sizeHint(self, option: QStyleOptionViewItem, index: Union[QModelIndex, QPersistentModelIndex]) -> QSize:
        image_group: ImageGroup = index.model().data(index, Qt.DisplayRole)
        pixmap = self._get_group_bitmap(image_group)
        return pixmap.size()


class MatchesListView(QListView):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setModel(WatchedListModel())
        self.setItemDelegate(ListMatchDelegate())
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

    def model(self) -> WatchedListModel:  # Override type hint
        return super().model()

    def set_groups(self, groups: WatchedList):
        self.model().set_list(groups)


class MatchesStackView(QScrollArea, MatchesView):  # TODO; Think what to do with it, after stack view is added
    layout_class = QGridLayout

    def __init__(self):
        super().__init__()
        # self.layout.addWidget(QLabel('This is stack view'))
