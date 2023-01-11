import datetime
from kabaret.app.ui.gui.widgets.flow.flow_view import QtWidgets, QtCore, QtGui
from kabaret.app import resources


FILE_CELL_MARGIN = 2
FILE_ICON_MARGIN = 2
PIXMAP_BY_STATUS = {
    'Available': resources.get_pixmap('icons.libreflow', 'checked-symbol-colored'),
    'Requested': resources.get_pixmap('icons.libreflow', 'waiting')
}
NODE_SIZE = 20
GRAPH_WIDTH_RATIO = 1.0
LINK_WIDTH = 3.0
LINK_RADIUS = 5.0


class QFileListDelegate(QtWidgets.QStyledItemDelegate):
    """
    Defines a delegate responsible for displaying file list entries.
    """

    def __init__(self, parent=None):
        super(QFileListDelegate, self).__init__(parent)

        self.font = QtGui.QFont()
        self.metrics = QtGui.QFontMetrics(self.font)
    
    def paint(self, painter, option, index):
        data = index.data(QtCore.Qt.UserRole)

        # Define draw areas
        orig_brush = painter.brush()
        orig_pen = painter.pen()
        rect_text = option.rect

        if option.state & QtWidgets.QStyle.State_Selected:
            painter.setBrush(QtGui.QColor('#004444'))
            painter.setPen(QtGui.QColor('#004444'))
            painter.drawRect(rect_text)
        
        rect_icon = QtCore.QRect(
            rect_text.left() + FILE_ICON_MARGIN,
            rect_text.top() + FILE_ICON_MARGIN,
            rect_text.height() - 2*FILE_ICON_MARGIN,
            rect_text.height() - 2*FILE_ICON_MARGIN
        )
        pixmap = resources.get_pixmap(*data.icon)
        pixmap = pixmap.scaled(
            rect_icon.size(),
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation
        )
        painter.drawPixmap(rect_icon, pixmap)

        if data.is_ref:
            rect_ref = QtCore.QRect(rect_icon.topLeft(), QtCore.QSize(15, 15))
            rect_ref.moveLeft(rect_icon.right() + 6*FILE_ICON_MARGIN)
            rect_ref.moveCenter(QtCore.QPoint(rect_ref.x(), option.rect.center().y()))
            pixmap = resources.get_pixmap('icons.gui', 'ref')
            pixmap = pixmap.scaled(
                rect_ref.size(),
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation
            )
            painter.drawPixmap(rect_ref, pixmap)

            rect_icon.setRight(rect_icon.right() + rect_ref.width())

        rect_text.setLeft(rect_icon.right() + 4*FILE_ICON_MARGIN)
        
        painter.setBrush(orig_brush)
        painter.setPen(orig_pen)
        painter.drawText(
            rect_text,
            QtCore.Qt.AlignVCenter,
            data.label
        )


class QFileHistoryDelegate(QtWidgets.QStyledItemDelegate):
    """
    Defines a delegate responsible for displaying file revision data.
    """

    def __init__(self, parent=None):
        super(QFileHistoryDelegate, self).__init__(parent)

        self.font = QtGui.QFont()
        self.metrics = QtGui.QFontMetrics(self.font)
    
    def paint(self, painter, option, index):
        orig_brush = painter.brush()
        orig_pen = painter.pen()
        data, max_link, max_color, weights = index.data(QtCore.Qt.UserRole)

        if option.state & QtWidgets.QStyle.State_Selected:
            painter.setBrush(QtGui.QColor('#004444'))
            painter.setPen(QtGui.QColor('#004444'))
            painter.drawRect(option.rect)
            # if index.column() == 1:
            #     print(index.row())
            #     print(weights)
            #     print(weights[index.row()])
        
        painter.setBrush(orig_brush)
        painter.setPen(orig_pen)

        if weights is None:
            weights = (0.45, {}, {})
        
        if index.column() == 0:
            painter.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform)
            color = QtGui.QColor('#aaaaaa')

            node_center = QtCore.QPoint(option.rect.right() - 10, option.rect.center().y())
            input_link, output_links, cross_links = data.links
            input_color, output_colors, cross_colors = data.colors
            
            remaining_width = node_center.x() - 2 * NODE_SIZE - option.rect.left()
            remaining_width *= GRAPH_WIDTH_RATIO
            right = node_center.x() - NODE_SIZE
            offset = 1.5 * painter.pen().width()

            if max_link > 0:
                step = remaining_width / max_link
            else:
                step = 1
            
            if data.working_copy:
                node_center.setX(right - max_link * step)

            if input_link >= 0:
                color.setHsvF(90.0 * input_color / (float(max_color) * 360.0) + 160.0/360.0, 0.75, weights[0])
                painter.setBrush(color)
                painter.setPen(QtGui.QPen(color, LINK_WIDTH))
                
                if input_link == 0:
                    p = QtCore.QPoint(node_center.x(), option.rect.bottom() - 1)
                    painter.drawLine(p, node_center)
                else:
                    x = right - input_link * step
                    
                    c1 = QtCore.QPoint(x + LINK_RADIUS, node_center.y())
                    c2 = QtCore.QPoint(x, node_center.y() + LINK_RADIUS)
                    ep = QtCore.QPoint(x, option.rect.bottom() - 1)
                    p = QtGui.QPainterPath()
                    p.moveTo(node_center)
                    p.cubicTo(c1, c2, ep)

                    painter.setBrush(QtCore.Qt.NoBrush)
                    painter.drawPath(p)
                    painter.setBrush(QtCore.Qt.SolidPattern)
            
            for i in range(len(output_links)):
                output_link = output_links[i]
                if output_link < 0:
                    continue
                
                output_color = output_colors[i]
                color.setHsvF(90.0 * output_color / (float(max_color) * 360.0) + 160.0/360.0, 0.75, weights[1].get(output_link, 0.45))
                painter.setBrush(color)
                painter.setPen(QtGui.QPen(color, LINK_WIDTH))

                if output_link == 0:
                    p = QtCore.QPoint(node_center.x(), option.rect.top())
                    painter.drawLine(node_center, p)
                else:
                    x = right - output_link * step
                    c1 = QtCore.QPoint(x + LINK_RADIUS, node_center.y())
                    c2 = QtCore.QPoint(x, node_center.y() - LINK_RADIUS)
                    ep = QtCore.QPoint(x, option.rect.top())
                    p = QtGui.QPainterPath()
                    p.moveTo(node_center)
                    p.cubicTo(c1, c2, ep)

                    painter.setBrush(QtCore.Qt.NoBrush)
                    painter.drawPath(p)
                    painter.setBrush(QtCore.Qt.SolidPattern)

            for i in range(len(cross_links)):
                cross_link = cross_links[i]
                if cross_link < 0:
                    continue

                cross_color = cross_colors[i]
                color.setHsvF(90.0 * cross_color / (float(max_color) * 360.0) + 160.0/360.0, 0.75, weights[2].get(cross_link, 0.45))
                painter.setBrush(color)
                painter.setPen(QtGui.QPen(color, LINK_WIDTH))
                
                x = int(cross_link > 0) * (right - cross_link * step) + int(cross_link == 0) * (option.rect.right() - 10)

                painter.drawLine(QtCore.QPoint(x, option.rect.bottom() - 1), QtCore.QPoint(x, option.rect.top()))
            
            painter.setBrush(QtGui.QColor('#777777'))
            painter.setPen(QtGui.QPen(QtGui.QColor('#777777'), 3))

            pixmap = resources.get_pixmap('icons.history', data.status)
            pixmap_rect = QtCore.QRect(node_center.x() - 0.5 * NODE_SIZE, node_center.y() - 0.5 * NODE_SIZE, NODE_SIZE, NODE_SIZE)

            painter.setBackground(QtGui.QColor('#777777'))
            painter.setBackgroundMode(QtCore.Qt.OpaqueMode)
            painter.drawPixmap(pixmap_rect, pixmap, pixmap.rect())
            painter.setBackgroundMode(QtCore.Qt.TransparentMode)

            painter.setBrush(orig_brush)
            painter.setPen(orig_pen)
        else:
            draw_rect = option.rect
            alignment = QtCore.Qt.AlignHCenter

            if index.column() == 1:
                painter.setBrush(QtGui.QColor(data.status_color))
                painter.setPen(QtGui.QColor(data.status_color))
                text = data.name
            elif index.column() == 2:
                text = data.user
            elif index.column() == 3:
                text = data.comment
                alignment = QtCore.Qt.AlignLeft
                draw_rect.setLeft(draw_rect.left() + 10)
            elif index.column() == 4:
                text = datetime.datetime.fromtimestamp(data.date).strftime('%y-%m-%d %H:%M')
            
            painter.drawText(
                draw_rect,
                QtCore.Qt.AlignVCenter | alignment,
                text
            )
            painter.setBrush(orig_brush)
            painter.setPen(orig_pen)


class QFileStatutesDelegate(QtWidgets.QStyledItemDelegate):
    """
    Defines a delegate responsible for displaying file revision synchronisation statutes.
    """

    def __init__(self, parent=None):
        super(QFileStatutesDelegate, self).__init__(parent)

        self.font = QtGui.QFont()
        self.metrics = QtGui.QFontMetrics(self.font)
    
    def paint(self, painter, option, index):
        data = index.data(QtCore.Qt.UserRole)
        draw_rect = option.rect
        orig_brush = painter.brush()
        orig_pen = painter.pen()

        if option.state & QtWidgets.QStyle.State_Selected:
            painter.setBrush(QtGui.QColor('#004444'))
            painter.setPen(QtGui.QColor('#004444'))
            painter.drawRect(draw_rect)
        
        painter.setBrush(orig_brush)
        painter.setPen(orig_pen)

        if index.column() == 0:
            painter.setBrush(QtGui.QColor(data.status_color))
            painter.setPen(QtGui.QColor(data.status_color))
            painter.drawText(
                draw_rect,
                QtCore.Qt.AlignCenter,
                data.name
            )
            painter.setBrush(orig_brush)
            painter.setPen(orig_pen)
        else:
            pixmap = PIXMAP_BY_STATUS.get(data.sync_status(index.column() - 1))

            if pixmap is not None:
                pixmap = pixmap.scaled(
                    draw_rect.size() - QtCore.QSize(4, 4),
                    QtCore.Qt.KeepAspectRatio,
                    QtCore.Qt.SmoothTransformation)
                x = draw_rect.center().x() - round(0.5 * pixmap.rect().width())
                y = draw_rect.center().y() - round(0.5 * pixmap.rect().height())
                
                painter.drawPixmap(
                    QtCore.QRect(x, y, pixmap.rect().width(), pixmap.rect().height()),
                    pixmap
                )
