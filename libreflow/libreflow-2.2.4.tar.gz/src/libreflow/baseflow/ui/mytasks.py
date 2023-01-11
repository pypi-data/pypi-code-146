import os
import datetime
import pprint
import time
import webbrowser
from kabaret.app.ui.gui.widgets.flow.flow_view import (
    CustomPageWidget,
    QtWidgets,
    QtCore,
    QtGui,
)
from kabaret.app.ui.gui.widgets.flow.flow_field import ObjectActionMenuManager
from kabaret.app import resources
from kabaret.app.ui.gui.icons import flow as _

from libreflow.baseflow.runners import CHOICES_ICONS

from ...resources.icons import gui as _


class LabelIcon(QtWidgets.QLabel):

    def __init__(self, icon=None):
        QtWidgets.QLabel.__init__(self, '')
        if icon:
            self.setIcon(icon)
    
    def setIcon(self, icon):
        icon = QtGui.QIcon(resources.get_icon(icon))
        pixmap = icon.pixmap(QtCore.QSize(16, 16))
        self.setPixmap(pixmap)
        self.setAlignment(QtCore.Qt.AlignVCenter)


class FilterCheckableComboBox(QtWidgets.QComboBox):

    # Subclass Delegate to increase item height
    class Delegate(QtWidgets.QStyledItemDelegate):
        # def paint(self, painter, option, index):
        #     super().paint(painter, option, index)

        #     painter.save()
        #     painter.drawRoundedRect(option.rect, 10, 10)
        #     painter.drawText(option.rect, QtCore.Qt.TextWordWrap, index.data())
        #     painter.restore()

        def sizeHint(self, option, index):
            size = super().sizeHint(option, index)
            size.setHeight(20)
            return size

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make the combo editable to set a custom text, but readonly
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        # Make the lineedit the same color as QPushButton
        self.setStyleSheet(
            '''QComboBox {
                background: #3e4041;
            }'''
        )

        # Use custom delegate
        self.setItemDelegate(FilterCheckableComboBox.Delegate())

        # Update the text when an item is toggled
        self.model().dataChanged.connect(self.updateText)
        self.model().itemChanged.connect(self.handleItemChanged)

        # Hide and show popup when clicking the line edit
        self.lineEdit().installEventFilter(self)
        self.closeOnLineEditClick = False

        # Prevent popup from closing when clicking on an item
        self.view().viewport().installEventFilter(self)

        # Disable right-click
        self.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)

        self.previousData = []
        self.defaultPreset = []

    def resizeEvent(self, event):
        # Recompute text to elide as needed
        self.updateText()
        super().resizeEvent(event)

    def wheelEvent(self, *args, **kwargs):
        pass

    def eventFilter(self, object, event):
        if object == self.lineEdit():
            if event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self.closeOnLineEditClick:
                        self.hidePopup()
                    else:
                        self.showPopup()
                    return True
                return False

        if object == self.view().viewport():
            if event.type() == QtCore.QEvent.MouseButtonRelease:
                index = self.view().indexAt(event.pos())
                item = self.model().item(index.row())

                if item.checkState() == QtCore.Qt.Checked:
                    item.setCheckState(QtCore.Qt.Unchecked)
                    if item.text() == 'Default':
                        for i in range(self.model().rowCount()):
                            if self.model().item(i).text() == 'Default':
                                continue
                            if self.model().item(i).text() == 'DONE':
                                self.model().item(i).setCheckState(QtCore.Qt.Unchecked)
                                continue
                            if self.model().item(i).checkState() == QtCore.Qt.Checked:
                                self.model().item(i).setCheckState(QtCore.Qt.Unchecked)
                else:
                    item.setCheckState(QtCore.Qt.Checked)
                return True
        return False

    def handleItemChanged(self, item):
        if item.checkState() == QtCore.Qt.Checked:
            if item.text() == 'Default':
                for i in range(self.model().rowCount()):
                    if self.model().item(i).text() == 'Default':
                        continue
                    if self.model().item(i).text() == 'DONE':
                        self.model().item(i).setCheckState(QtCore.Qt.Unchecked)
                        continue
                    if self.model().item(i).checkState() == QtCore.Qt.Unchecked:
                        self.model().item(i).setCheckState(QtCore.Qt.Checked)
        if self.currentData() != self.defaultPreset:
            for i in range(self.model().rowCount()):
                if self.model().item(i).text() == 'Default':
                    self.model().item(i).setCheckState(QtCore.Qt.Unchecked)

    def showPopup(self):
        super().showPopup()
        # When the popup is displayed, a click on the lineedit should close it
        self.closeOnLineEditClick = True

    def hidePopup(self):
        super().hidePopup()
        # Used to prevent immediate reopening when clicking on the lineEdit
        self.startTimer(100)
        # Refresh the display text when closing
        self.updateText()
        # Check if there are any changes
        newRes = self.currentData()
        if self.previousData != newRes:
            self.previousData = newRes
            self.parent().page_widget.update_presets(filter_data=self.previousData)
            self.parent().page_widget.list.refresh(force_update=True)

    def timerEvent(self, event):
        # After timeout, kill timer, and reenable click on line edit
        self.killTimer(event.timerId())
        self.closeOnLineEditClick = False

    def updateText(self):
        texts = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == QtCore.Qt.Checked:
                if self.model().item(i).text() == 'Default':
                    continue
                texts.append(self.model().item(i).text())
        text = ", ".join(texts)

        # Compute elided text (with "...")
        metrics = QtGui.QFontMetrics(self.lineEdit().font())
        elidedText = metrics.elidedText(text, QtCore.Qt.ElideRight, self.lineEdit().width())
        if '…' in elidedText:
            elidedText = 'Status (' + str(len(texts)) + ')'
        self.lineEdit().setText(elidedText)

    def addItem(self, text, data=None):
        item = QtGui.QStandardItem()
        item.setText(text)
        if data is None:
            item.setData(text)
        else:
            item.setData(data)
        item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
        item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
        self.model().appendRow(item)

    def addItems(self, texts, datalist=None):
        for i, text in enumerate(texts):
            try:
                data = datalist[i]
            except (TypeError, IndexError):
                data = None
            self.addItem(text, data)

    def setDefaultPreset(self):
        preset = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).text() == 'Default' or self.model().item(i).text() == 'DONE':
                continue
            preset.append(self.model().item(i).data())
        self.defaultPreset = preset

    def setChecked(self, texts, state):
        for i, text in enumerate(texts):
            for row in range(self.model().rowCount()):
                if self.model().item(row).text() == text:
                    if state == True:
                        self.model().item(row).setCheckState(QtCore.Qt.Checked)
                    else:
                        self.model().item(row).setCheckState(QtCore.Qt.Unchecked)

    def currentData(self):
        # Return the list of selected items data
        res = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).text() == 'Default':
                continue
            if self.model().item(i).checkState() == QtCore.Qt.Checked:
                res.append(self.model().item(i).data())
        if res == self.defaultPreset:
            self.model().item(0).setCheckState(QtCore.Qt.Checked)
        return res


class FilesUploadComboBox(QtWidgets.QComboBox):

    # Subclass Delegate to increase item height
    class Delegate(QtWidgets.QStyledItemDelegate):
        def sizeHint(self, option, index):
            size = super().sizeHint(option, index)
            return size

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make the combo editable to set a custom text, but readonly
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        # Make the lineedit the same color as QPushButton
        self.setStyleSheet(
            '''QComboBox {
                background: #3e4041;
            }'''
        )

        # Use custom delegate
        self.setItemDelegate(FilesUploadComboBox.Delegate())

        # Update the text when an item is toggled
        self.model().dataChanged.connect(self.updateText)
        # self.model().itemChanged.connect(self.handleItemChanged)

        # Hide and show popup when clicking the line edit
        self.lineEdit().installEventFilter(self)
        self.closeOnLineEditClick = False

        # Prevent popup from closing when clicking on an item
        self.view().viewport().installEventFilter(self)

        # Disable right-click
        self.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)

        self.setAcceptDrops(True)

        self.primary_files_names = []
        self.previousData = []

        self.addItem('- Add files', checkable=False)
        self.addItem('- Clear selection', checkable=False)
        self.setCurrentIndex(-1)

        self.add_primary_files()

        self.currentIndexChanged.connect(self._on_files_index_changed)

    def resizeEvent(self, event):
        # Recompute text to elide as needed
        self.updateText()
        super().resizeEvent(event)

    def wheelEvent(self, *args, **kwargs):
        pass

    def eventFilter(self, object, event):
        if object == self.lineEdit():
            if event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    if self.closeOnLineEditClick:
                        self.hidePopup()
                    else:
                        self.showPopup()
                    return True
        return False

    def showPopup(self):
        super().showPopup()
        # When the popup is displayed, a click on the lineedit should close it
        self.closeOnLineEditClick = True

    def hidePopup(self):
        super().hidePopup()
        # Used to prevent immediate reopening when clicking on the lineEdit
        self.startTimer(100)
        # Refresh the display text when closing
        self.updateText()
        # Check if there are any changes
        newRes = self.currentData()
        if self.previousData != newRes:
            self.previousData = newRes

    def timerEvent(self, event):
        # After timeout, kill timer, and reenable click on line edit
        self.killTimer(event.timerId())
        self.closeOnLineEditClick = False

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.add_files(links)
        else:
            event.ignore()

    def updateText(self):
        texts = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == QtCore.Qt.Checked:
                texts.append(self.model().item(i).text())
        text = ", ".join(texts)

        # Compute elided text (with "...")
        metrics = QtGui.QFontMetrics(self.lineEdit().font())
        elidedText = metrics.elidedText(text, QtCore.Qt.ElideRight, self.lineEdit().width())
        if '…' in elidedText:
            elidedText = str(len(texts)) + ' Files'
        self.lineEdit().setText(elidedText)

    def addItem(self, text, data=None, checkable=True):
        item = QtGui.QStandardItem()
        item.setText(text)
        if data is None:
            item.setData(text)
        else:
            item.setData(data)
        if checkable:
            item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
            item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
        self.model().appendRow(item)

    def addItems(self, texts, datalist=None):
        for i, text in enumerate(texts):
            try:
                data = datalist[i]
            except (TypeError, IndexError):
                data = None
            self.addItem(text, data)

    def setChecked(self, texts, state):
        for i, text in enumerate(texts):
            for row in range(self.model().rowCount()):
                if self.model().item(row).text() == text:
                    if state == True:
                        self.model().item(row).setCheckState(QtCore.Qt.Checked)
                    else:
                        self.model().item(row).setCheckState(QtCore.Qt.Unchecked)

    def currentData(self):
        # Return the list of selected items data
        res = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == QtCore.Qt.Checked:
                res.append(self.model().item(i).data())
        return res

    def add_primary_files(self):
        files_list = self.parent().task_item.files_list
        for i in range(files_list.topLevelItemCount()):
            f = files_list.topLevelItem(i)
            check = self.parent().page_widget.is_uploadable(f.file_name)
            if check:
                r = self.parent().page_widget.session.cmds.Flow.call(
                    f.file_oid, 'get_head_revision', ['Available'], {}
                )
                self.addItem(f.file_name, r.get_path())
                self.primary_files_names.append(f.file_name)

    def add_files(self, paths):
        for path in paths:
            exist = False
            for i in range(self.model().rowCount()):
                if self.model().item(i).data() == path:
                    self.model().item(i).setCheckState(QtCore.Qt.Checked)
                    exist = True
                    break
            if not exist:
                filename = os.path.split(path)[1]
                self.addItem(filename, path)
                index = self.findText(filename, QtCore.Qt.MatchFixedString)
                self.model().item(index).setCheckState(QtCore.Qt.Checked)

    def _on_files_index_changed(self, index):
        if index == 0:
            dialog = QtWidgets.QFileDialog()
            dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)

            if dialog.exec_():
                paths = dialog.selectedFiles()
                self.add_files(paths)
            else:
                self.setCurrentIndex(-1)
                self.updateText()

        if index == 1:
            self.setCurrentIndex(-1)
            for i in range(self.model().rowCount()):
                if self.model().item(i).checkState() == QtCore.Qt.Checked:
                    self.model().item(i).setCheckState(QtCore.Qt.Unchecked)


class NavigationButton(QtWidgets.QToolButton):

    def __init__(self, name, oid):
        super(NavigationButton, self).__init__()
        if ':' in name:
            self.name = name.split(':')[1]
        else:
            self.name = name
        self.oid = oid

        self.setProperty('tight_layout', True)
        self.setProperty('hide_arrow', True)
        self.setProperty('no_border', True)
        self.setProperty('square', True)
        self.setArrowType(QtCore.Qt.NoArrow)

        self.setText('/%s' % (self.name,))

        self.clicked.connect(self._goto)

    def _goto(self, b=None):
        self.parent().tasks_list.page_widget.page.goto(self.oid)


# class KitsuUser(QtWidgets.QWidget):

    #     def __init__(self, parent, full_name, color):
    #         super(KitsuUser, self).__init__()
    #         self.parent = parent
    #         self.full_name = full_name
    #         self.color = color

    #         self.build()

    #     def build(self):
    #         lo = QtWidgets.QHBoxLayout()
    #         lo.setMargin(0)

    #         self.user_icon = QtWidgets.QLabel()
    #         pm = resources.get_pixmap('icons.libreflow', 'circular-shape-silhouette')
    #         painter = QtGui.QPainter(pm)
    #         painter.save()
    #         font = QtGui.QFont()
    #         font.setPointSize(12)
    #         font.setWeight(QtGui.QFont.Bold)
    #         painter.setFont(font)
    #         painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
    #         painter.fillRect(pm.rect(), QtGui.QColor(self.color))
    #         painter.setPen(QtCore.Qt.white)
    #         painter.drawText(pm.rect(), QtCore.Qt.AlignCenter, ''.join([s[0] for s in self.full_name.split()]))
    #         painter.restore()
    #         self.user_icon.setPixmap(pm.scaled(23, 23, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
    #         self.user_icon.setAlignment(QtCore.Qt.AlignCenter)
            
    #         self.user_name = QtWidgets.QLabel(self.full_name)
    #         self.user_name.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

    #         lo.addWidget(self.user_icon)
    #         lo.addWidget(self.user_name)
    #         self.setLayout(lo)


class MyTasksFooter(QtWidgets.QWidget):

    def __init__(self, page_widget):
        super(MyTasksFooter, self).__init__(page_widget)
        self.page_widget = page_widget
        self.build()

    def build(self):
        self.left_text = QtWidgets.QLabel()
        self.left_text.setText(str(self.page_widget.list.get_count())+' Tasks')
        self.page_widget.list.get_count()
        self.shift_label = QtWidgets.QLabel('Press SHIFT to display entity description')

        hlo = QtWidgets.QHBoxLayout()
        hlo.addWidget(self.left_text)
        hlo.addStretch()
        hlo.addWidget(self.shift_label)
        hlo.setContentsMargins(0,10,0,5)
        self.setLayout(hlo)

    def refresh_count(self):
        self.left_text.setText(str(self.page_widget.list.get_count())+' Tasks')
        self.left_text.setStyleSheet('')


class EditStatusDialog(QtWidgets.QDialog):

    def __init__(self, task_item):
        super(EditStatusDialog, self).__init__(task_item)
        self.task_item = task_item
        self.page_widget = task_item.page_widget
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setStyleSheet('font-size: 11px;')
        self.setMaximumSize(600, 300)

        self.build()
    
    def build(self):
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(20,20,20,20)

        palette = self.palette()
        palette.setColor(QtGui.QPalette.Base, palette.color(QtGui.QPalette.Window))
        self.setPalette(palette)

        self.content_layout = QtWidgets.QGridLayout()
        self.content_layout.setAlignment(QtCore.Qt.AlignTop)
      
        self.content_layout.addWidget(LabelIcon(('icons.flow', 'input')), 0, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Target Status'), 0, 1, QtCore.Qt.AlignVCenter)
        self.target_status = QtWidgets.QComboBox()
        self.target_status.addItems(sorted(self.page_widget.get_task_statutes(False)))
        self.target_status.setCurrentText('Work In Progress')
        self.content_layout.addWidget(self.target_status, 0, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(('icons.flow', 'input')), 1, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Comment'), 1, 1, QtCore.Qt.AlignVCenter)
        self.comment = QtWidgets.QTextEdit('')
        self.content_layout.addWidget(self.comment, 1, 2, QtCore.Qt.AlignVCenter)

        self.content_layout.addWidget(LabelIcon(('icons.flow', 'input')), 2, 0, QtCore.Qt.AlignVCenter)
        self.content_layout.addWidget(QtWidgets.QLabel('Files'), 2, 1, QtCore.Qt.AlignVCenter)
        self.files = FilesUploadComboBox(self)
        self.content_layout.addWidget(self.files, 2, 2, QtCore.Qt.AlignVCenter)

        # Buttons
        self.button_layout = QtWidgets.QHBoxLayout()

        self.button_post = QtWidgets.QPushButton('Post')
        self.button_cancel = QtWidgets.QPushButton('Cancel')

        self.button_post.clicked.connect(self._on_post_button_clicked)
        self.button_cancel.clicked.connect(self._on_cancel_button_clicked)

        self.button_post.setAutoDefault(False)
        self.button_cancel.setAutoDefault(False)

        self.button_layout.addStretch()
        self.button_layout.addWidget(self.button_post)
        self.button_layout.addWidget(self.button_cancel)

        self.layout.addLayout(self.content_layout)
        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

    def sizeHint(self):
        return QtCore.QSize(475, 275)

    def _on_post_button_clicked(self):
        if len(self.files.currentData()) == 1:
            if self.files.currentText() in self.files.primary_files_names:
                self.page_widget.upload_preview(
                    self.page_widget.session.cmds.Flow.get_value(self.task_item.oid+'/entity_id'),
                    self.task_item.task_type,
                    self.target_status.currentText(),
                    self.files.currentData()[0],
                    self.comment.toPlainText()
                )
        else:
            self.page_widget.set_task_status(
                self.task_item.task_id,
                self.target_status.currentText(),
                self.comment.toPlainText(),
                self.files.currentData()
            )
        self.page_widget.list.refresh(True)

    def _on_cancel_button_clicked(self):
        self.close()


class TaskFile(QtWidgets.QTreeWidgetItem):

    def __init__(self, tree, file_oid):
        super(TaskFile, self).__init__(tree)
        self.tree = tree
        self.file_oid = file_oid
        self.page_widget = tree.page_widget

        self.refresh()
    
    def refresh(self):
        self.file_name = self.page_widget.session.cmds.Flow.get_value(self.file_oid+'/display_name')
        name, ext = os.path.splitext(self.file_name)
        icon = CHOICES_ICONS.get(
            ext[1:], ('icons.gui', 'text-file-1')
        ) 

        self.setIcon(0, self.get_icon(icon))
        self.setText(0, self.file_name)

        self.setExpanded(True)
    
    @staticmethod
    def get_icon(icon_ref):
        return QtGui.QIcon(resources.get_icon(icon_ref))


class TaskFiles(QtWidgets.QTreeWidget):

    def __init__(self, task_item):
        super(TaskFiles, self).__init__(task_item)
        self.task_item = task_item
        self.page_widget = task_item.page_widget

        self.action_manager = ObjectActionMenuManager(
            self.page_widget.session, self.page_widget.page.show_action_dialog, 'Flow.map'
        )

        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setStyleSheet('''
        QTreeView::item {
            height: 25px;
        }
        QTreeView::item:selected {
            background-color: #223e55;
            color: white;
        }'''
        )
        self.setRootIsDecorated(False)

        self.setHeaderLabel('Files')
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        
        self.refresh()

        self.header().setStretchLastSection(True)

        self.itemDoubleClicked.connect(self._on_item_double_clicked)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._on_context_menu)

    def refresh(self):
        self.blockSignals(True)
        self.clear()

        primary_files = sorted(self.page_widget.session.cmds.Flow.get_value(
            self.task_item.oid+'/primary_files'
        ))

        for oid in primary_files:
            TaskFile(self, oid)

        self.blockSignals(False)
    
    def _on_item_double_clicked(self, item):
        self.page_widget.page.show_action_dialog(self.page_widget.session.cmds.Flow.call(
            item.file_oid, 'activate_oid', [], {}
        ))

    def _on_context_menu(self, pos):
        item = self.itemAt(pos)

        if item is None:
            return

        self.action_menu = QtWidgets.QMenu()

        has_actions = self.action_manager.update_oid_menu(
            item.file_oid, self.action_menu, with_submenus=True
        )

        if has_actions:
            self.action_menu.exec_(self.viewport().mapToGlobal(pos))


class TaskItem(QtWidgets.QWidget):

    def __init__(self, tasks_list, oid):
        super(TaskItem, self).__init__()
        self.setObjectName('TaskItem')
        self.tasks_list = tasks_list
        self.page_widget = tasks_list.page_widget
        self.oid = oid

        self.task_oid = self.page_widget.session.cmds.Flow.get_value(self.oid+'/task_oid')
        
        self.op = QtWidgets.QGraphicsOpacityEffect(self)
        self.op.setOpacity(1.00)
        self.setGraphicsEffect(self.op)
        self.setAutoFillBackground(True)
        self.setStyleSheet('font-size: 12px;')
        self.setMinimumHeight(165)
        self.setMaximumHeight(200)

        self.build()
        self.refresh()

    def build(self):
        container = QtWidgets.QGridLayout()
        container.setMargin(10)

        # Left Layout
        left_lo = QtWidgets.QVBoxLayout()
        self.oid_lo = QtWidgets.QHBoxLayout()
        self.oid_lo.setSpacing(0)
        left_lo.addLayout(self.oid_lo)

        self.files_list = TaskFiles(self)
        left_lo.addWidget(self.files_list)

        # Right Layout
        ## Kitsu
        self.right_kitsu = QtWidgets.QWidget()
        self.kitsu_lo = QtWidgets.QVBoxLayout()
        self.kitsu_lo.setContentsMargins(0,0,0,0)
        kitsu_header = QtWidgets.QHBoxLayout()
        kitsu_header.setSpacing(0)

        self.type_label = QtWidgets.QLabel('')
        self.status_label = QtWidgets.QLabel('')
        self.redirect_task = QtWidgets.QPushButton(QtGui.QIcon(resources.get_icon(('icons.libreflow', 'kitsu'))), '')
        self.redirect_task.setIconSize(QtCore.QSize(13,13))
        self.redirect_task.setStyleSheet('padding: 2;')
        self.edit_status = QtWidgets.QPushButton(QtGui.QIcon(resources.get_icon(('icons.libreflow', 'edit-blank'))), '')
        self.edit_status.setIconSize(QtCore.QSize(13,13))
        self.edit_status.setStyleSheet('padding: 2;')
        self.edit_status.clicked.connect(self._on_edit_status_button_clicked)
        kitsu_header.addStretch()
        kitsu_header.addWidget(self.type_label)
        kitsu_header.addWidget(self.status_label)
        kitsu_header.addWidget(self.redirect_task)
        kitsu_header.addWidget(self.edit_status)

        self.kitsu_lo.addLayout(kitsu_header)

        self.kitsu_comments = QtWidgets.QTextBrowser()
        self.kitsu_comments.setOpenExternalLinks(True)
        self.kitsu_comments.setReadOnly(True)
        self.kitsu_comments.setPlaceholderText('No comment for this task.')

        self.kitsu_lo.addWidget(self.kitsu_comments)
        self.right_kitsu.setLayout(self.kitsu_lo)

        ## Entity Data
        self.right_entity = QtWidgets.QWidget()
        entity_lo = QtWidgets.QGridLayout()
        entity_lo.setContentsMargins(0,0,0,0)

        self.header_spacer = QtWidgets.QWidget()
        header_spacer_lo = QtWidgets.QVBoxLayout()
        header_spacer_lo.setContentsMargins(0,0,0,0)
        self.header_spacer.setLayout(header_spacer_lo)
        self.spacer = QtWidgets.QSpacerItem(0, 23, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        header_spacer_lo.addItem(self.spacer)

        self.shot_header = QtWidgets.QWidget()
        shot_header_lo = QtWidgets.QHBoxLayout()
        shot_header_lo.setContentsMargins(0,0,0,0)
        self.shot_header.setLayout(shot_header_lo)

        self.shot_icon = QtWidgets.QLabel()
        pm = resources.get_pixmap('icons.gui', 'film-strip-with-two-photograms')
        self.shot_icon.setPixmap(pm.scaled(23, 23, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.shot_icon.setAlignment(QtCore.Qt.AlignCenter)
        self.shot_frames = QtWidgets.QLabel('Frames duration')
        self.shot_frames.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        shot_header_lo.addWidget(self.shot_icon)
        shot_header_lo.addWidget(self.shot_frames)
        shot_header_lo.addStretch()
        entity_lo.addWidget(self.shot_header, 0, 0, QtCore.Qt.AlignTop)
        entity_lo.addWidget(self.header_spacer, 0, 0, QtCore.Qt.AlignTop)

        self.entity_description = QtWidgets.QTextEdit('')
        self.entity_description.setPlaceholderText('No description')
        self.entity_description.setReadOnly(True)
        # Set line spacing
        descBlockFmt = QtGui.QTextBlockFormat()
        descBlockFmt.setLineHeight(120, QtGui.QTextBlockFormat.ProportionalHeight)
        descTextCursor = self.entity_description.textCursor()
        descTextCursor.clearSelection()
        descTextCursor.select(QtGui.QTextCursor.Document)
        descTextCursor.mergeBlockFormat(descBlockFmt)

        entity_lo.addWidget(self.entity_description, 2, 0, QtCore.Qt.AlignTop)
        self.right_entity.setLayout(entity_lo)
        self.right_entity.hide()

        container.addLayout(left_lo, 0, 0)
        container.addWidget(self.right_kitsu, 0, 1)
        container.addWidget(self.right_entity, 0, 1)
        container.setColumnStretch(0, 3)
        container.setColumnStretch(1, 2)
        self.setLayout(container)

    def refresh(self):
        self.task_id = self.page_widget.session.cmds.Flow.get_value(self.oid+'/task_id')
        entity_type = self.page_widget.session.cmds.Flow.get_value(self.oid+'/entity_type')

        # Bookmark
        if self.page_widget.session.cmds.Flow.get_value(self.oid+'/is_bookmarked'):
            self.bookmark_button = QtWidgets.QToolButton()
            self.bookmark_button.setIcon(resources.get_icon(('icons.gui', 'star')))
            self.bookmark_button.setIconSize(QtCore.QSize(14, 14))
            self.bookmark_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            self.bookmark_button.clicked.connect(self._on_bookmark_button_clicked)
            self.oid_lo.addWidget(self.bookmark_button)

        # Navigation buttons
        project_oid = self.page_widget.get_project_oid()

        label_to_oid = self.page_widget.session.cmds.Flow.split_oid(self.task_oid, True, project_oid)
        for label, goto_oid in label_to_oid:
            nav_button = NavigationButton(label, goto_oid)
            self.oid_lo.addWidget(nav_button)
        self.oid_lo.addStretch()

        # Task Status
        self.task_type = self.page_widget.session.cmds.Flow.get_value(self.oid+'/task_type')
        status = self.page_widget.session.cmds.Flow.get_value(self.oid+'/task_status')
        self.type_label.setText(f'{self.task_type} -')
        self.status_label.setText(f'{status.upper()}')

        # Redirect Task
        task_link = self.create_task_link(entity_type)
        self.redirect_task.clicked.connect(lambda: self._on_redirect_task_button_clicked(task_link))

        # Comments
        comments = self.page_widget.get_task_comments(self.task_id)

        if comments:
            comment_html = '''
            <style>
                a:link {
                    color: #00BFFF;
                    background-color: transparent;
                    text-decoration: none;
                }
                .separator {
                    border-bottom: 1px solid white;
                    border-collapse: collapse;
                }
                .spacer {
                    margin-bottom: 10px;
                }
            </style>
            '''

            for i, c in enumerate(comments):
                date_object = datetime.datetime.strptime(c['created_at'], "%Y-%m-%dT%H:%M:%S")

                comment_html = comment_html + '''
                <table cellspacing=0 width=100%>
                <tr>
                    <td><span style='color: {color}; font-weight: bold;'>{status}</span> - {name}</td>
                    <td align=right>{date}</td>
                </tr>
                </table>
                '''.format(
                    color=c['task_status']['color'],
                    status=c['task_status']['short_name'].upper(),
                    name=c['person']['first_name'] + ' ' + c['person']['last_name'],
                    date=date_object.strftime('%d/%m'),
                )

                if c['text'] != '':
                    if '\n' in c['text']:
                        comment_lines = c['text'].split('\n')
                        for line in comment_lines:
                            comment_html = comment_html + '''<p>{text}</p>'''.format(text=line)
                    else:
                        comment_html = comment_html + '''<p>{text}</p>'''.format(text=c['text'])

                if c['previews'] != []:
                    revision_link = self.create_revision_link(entity_type, c['previews'][0]['id'])
                    comment_html = comment_html + '''<p><a href='{link}'>Revision</a></p>'''.format(link=revision_link)
                
                if i == 0:
                    self.status_label.setStyleSheet(f'color: {c["task_status"]["color"]}; font-weight: 700; padding-right: 1;')

                if i == len(comments)-1:
                    continue
                comment_html = comment_html + '''<table cellspacing=0 class="spacer" width=100%><tr><td class="separator"/></tr></table>'''

            self.kitsu_comments.setHtml(comment_html)

        if self.status_label.styleSheet() == '':
            status_data = self.page_widget.get_task_status(status)
            self.status_label.setStyleSheet(f'color: {status_data["color"]}; font-weight: 700; padding-right: 1;')

        if self.page_widget.session.cmds.Flow.get_value(self.oid+'/shot_frames'):
            self.header_spacer.hide()
            frames = self.page_widget.session.cmds.Flow.get_value(self.oid+'/shot_frames')
            project_fps = int(self.page_widget.get_project_fps())
            timecode = self.frames_to_timecode(frames, project_fps)
            self.shot_frames.setText(str(frames)+' frames ('+timecode+')')
        else:
            self.shot_header.hide()
        self.entity_description.setText(self.page_widget.session.cmds.Flow.get_value(self.oid+'/entity_description'))

    def frames_to_timecode(self, frames, fps):
        h = int(frames / 86400) 
        m = int(frames / 1440) % 60
        s = int((frames % 1440)/fps)
        f = frames % 1440 % fps
        return ( "%02d:%02d:%02d:%02d" % ( h, m, s, f))

    def create_task_link(self, entity_type):
        return '{server}/productions/{project}/{entity}/tasks/{task}'.format(
            server=self.page_widget.get_server_url(),
            project=self.page_widget.get_project_id(),
            entity=entity_type.lower(),
            task=self.task_id
        )

    def create_revision_link(self, entity_type, preview_id):
        return '{server}/productions/{project}/{entity}/tasks/{task}/previews/{preview}'.format(
            server=self.page_widget.get_server_url(),
            project=self.page_widget.get_project_id(),
            entity=entity_type.lower(),
            task=self.task_id,
            preview=preview_id
        )
    
    def _on_bookmark_button_clicked(self):
        is_bookmarked = self.page_widget.toggle_bookmark(self.task_oid)
        if is_bookmarked:
            self.bookmark_button.setIcon(resources.get_icon(('icons.gui', 'star')))
            self.bookmark_button.setIconSize(QtCore.QSize(12, 12))
        else:
            self.bookmark_button.setIcon(resources.get_icon(('icons.gui', 'star-1')))
            self.bookmark_button.setIconSize(QtCore.QSize(12, 12))

    def _on_redirect_task_button_clicked(self, link):
        webbrowser.open(link)
    
    def _on_edit_status_button_clicked(self):
        dialog = EditStatusDialog(self)
        dialog.exec()


class MyTasksList(QtWidgets.QScrollArea):

    def __init__(self, page_widget):
        super(MyTasksList, self).__init__()
        self.page_widget = page_widget
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.refresh()

    def refresh(self, force_update=False):
        if force_update:
            self.page_widget.footer.left_text.setText('Updating...')
            self.page_widget.footer.left_text.setStyleSheet('color: red; font-weight: 700;')
            for i in reversed(range(self.layout.count())):
                widget = self.layout.itemAt(i).widget()
                if widget is not None:
                    widget.op.setOpacity(0.50)

            QtWidgets.QApplication.processEvents()
            QtWidgets.QApplication.processEvents()

        tasks = self.page_widget.session.cmds.Flow.call(
            self.page_widget.oid, 'get_tasks', {force_update}, {}
        )

        container = QtWidgets.QWidget()
        container.setObjectName('ScrollAreaContainer')
        container.setStyleSheet('QWidget#ScrollAreaContainer {background-color: #2b2b2b;}')
        self.layout = QtWidgets.QVBoxLayout(container)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.setSpacing(10)
        
        for task in tasks:
            item = TaskItem(self, task.oid())
            self.layout.addWidget(item)

        self.layout.addStretch(1)
        self.layout.setMargin(10)
        self.setWidget(container)

        if force_update:
            self.page_widget.footer.refresh_count()

    def get_count(self):
        return self.layout.count() - 1

    def toggle_entity_data(self):
        for i in reversed(range(self.layout.count())):
            task = self.layout.itemAt(i).widget()
            if task is not None:
                if task.right_kitsu.isVisible():
                    task.right_kitsu.hide()
                    task.right_entity.show()
                else:
                    task.right_entity.hide()
                    task.right_kitsu.show()


class MyTasksHeader(QtWidgets.QWidget):

    def __init__(self, page_widget):
        super(MyTasksHeader, self).__init__(page_widget)
        self.page_widget = page_widget
        self.build_completed = False
        self.build()

    def build(self):
        self.refresh_icon = QtGui.QIcon(resources.get_icon(('icons.gui', 'refresh')))
        self.refresh_button = QtWidgets.QPushButton(self.refresh_icon, '')
        self.refresh_button.clicked.connect(self._on_refresh_button_clicked)
        self.refresh_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        
        self.filter_label = QtWidgets.QLabel('Filter by')
        self.filter_combobox = FilterCheckableComboBox()
        self.filter_combobox.addItem('Default')
        self.filter_combobox.addItems(sorted([task.upper() for task in self.page_widget.get_task_statutes(True)]))
        self.filter_combobox.setDefaultPreset()
        filter_value = self.page_widget.get_user_filter()
        if filter_value == []:
            self.filter_combobox.setChecked(['Default'], True)
        else:
            for statues in filter_value:
                self.filter_combobox.setChecked([statues], True)
        self.filter_combobox.previousData = self.filter_combobox.currentData()
        self.page_widget.update_presets(filter_data=self.filter_combobox.previousData)
        
        self.sort_label = QtWidgets.QLabel('Sort by')
        self.sort_combobox = QtWidgets.QComboBox()
        self.sort_combobox.addItems(['Entity name', 'Status', 'Latest update'])
        self.sort_combobox.currentTextChanged.connect(self._on_sort_combobox_changed)
        self.sort_combobox.setView(QtWidgets.QListView())
        self.sort_combobox.setStyleSheet(
            '''QComboBox QAbstractItemView::item {
                min-height: 20px;
            }'''
        )
        sort_value = self.page_widget.get_user_sorted()
        if sort_value == None:
            self.page_widget.update_presets(sort_data='Entity name')
        else:
            self.sort_combobox.setCurrentText(sort_value)

        self.kitsu_tasks = QtWidgets.QPushButton(QtGui.QIcon(resources.get_icon(('icons.libreflow', 'kitsu'))), 'My Tasks')
        self.kitsu_tasks.clicked.connect(self._on_kitsu_tasks_button_clicked)
        self.kitsu_tasks.setIconSize(QtCore.QSize(13,13))
        self.kitsu_tasks.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.fdt_button = QtWidgets.QPushButton('FDT')
        self.fdt_button.clicked.connect(self._on_fdt_button_clicked)
        self.fdt_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        hlo = QtWidgets.QHBoxLayout()
        hlo.addWidget(self.refresh_button)
        hlo.addWidget(self.filter_label)
        hlo.addWidget(self.filter_combobox)
        hlo.addWidget(self.sort_label)
        hlo.addWidget(self.sort_combobox)
        hlo.addStretch()
        hlo.addWidget(self.kitsu_tasks)
        hlo.addWidget(self.fdt_button)
        hlo.setContentsMargins(0,0,0,5)
        self.setLayout(hlo)
        self.build_completed = True

    def _on_sort_combobox_changed(self, value):
        if self.build_completed == False:
            return
        self.page_widget.update_presets(sort_data=value)
        self.page_widget.list.refresh(force_update=True)

    def _on_refresh_button_clicked(self):
        self.page_widget.list.refresh(force_update=True)

    def _on_kitsu_tasks_button_clicked(self):
        webbrowser.open(self.page_widget.get_server_url() + '/todos')

    def _on_fdt_button_clicked(self):
        webbrowser.open('https://fdt.lesfees.net/')


class MyTasksPageWidget(CustomPageWidget):

    def build(self):
        self.setStyleSheet('outline: 0;')

        self.header = MyTasksHeader(self)
        self.list = MyTasksList(self)
        self.footer = MyTasksFooter(self)

        vlo = QtWidgets.QVBoxLayout()
        vlo.addWidget(self.header)
        vlo.addWidget(self.list)
        vlo.addWidget(self.footer)
        vlo.setSpacing(0)
        vlo.setMargin(0)
        self.setLayout(vlo)

        self.key_press_start_time = -1
    
    def sizeHint(self):
        return QtCore.QSize(2000, 2000)

    def keyPressEvent(self, event):
        super(MyTasksPageWidget, self).keyPressEvent(event)

        if event.key() == QtCore.Qt.Key_Shift:
            self.list.toggle_entity_data()
            self.key_press_start_time =  time.time()

    def keyReleaseEvent(self, event):
        super(MyTasksPageWidget, self).keyReleaseEvent(event)
        key_press_time = time.time() - self.key_press_start_time

        if event.key() == QtCore.Qt.Key_Shift and key_press_time > 0.5:
            self.list.toggle_entity_data()

    def get_project_oid(self):
        return self.session.cmds.Flow.call(
            self.oid, 'get_project_oid', {}, {}
        )

    def get_project_id(self):
        return self.session.cmds.Flow.call(
            self.oid, 'get_project_id', {}, {}
        )

    def get_project_fps(self):
        return self.session.cmds.Flow.call(
            self.oid, 'get_project_fps', {}, {}
        )

    def get_user_filter(self):
        return self.session.cmds.Flow.get_value(self.oid+'/settings/task_statues_filter')

    def get_user_sorted(self):
        return self.session.cmds.Flow.get_value(self.oid+'/settings/task_sorted')

    def get_task_comments(self, task_id):
        return self.session.cmds.Flow.call(
            self.oid, 'get_task_comments', {task_id}, {}
        )

    def get_server_url(self):
        return self.session.cmds.Flow.call(
            self.oid, 'get_server_url', {}, {}
        )

    def is_uploadable(self, file_name):
        return self.session.cmds.Flow.call(
            self.oid, 'is_uploadable', [file_name], {}
        )

    def get_task_statutes(self, short_name):
        return self.session.cmds.Flow.call(
            self.oid, 'get_task_statutes', [short_name], {}
        )

    def get_task_status(self, task_status_name):
        return self.session.cmds.Flow.call(
            self.oid, 'get_task_status', [task_status_name], {}
        )

    def set_task_status(self, task_id, task_status_name, comment, files):
        return self.session.cmds.Flow.call(
            self.oid, 'set_task_status', [task_id, task_status_name, comment, files], {}
        )

    def upload_preview(self, entity_id, task_name, task_status_name, file_path, comment):
        return self.session.cmds.Flow.call(
            self.oid, 'upload_preview', [entity_id, task_name, task_status_name, file_path, comment], {}
        )

    def toggle_bookmark(self, oid):
        return self.session.cmds.Flow.call(
            self.oid, 'toggle_bookmark', [oid], {}
        )

    def update_presets(self, filter_data=None, sort_data=None):
        if filter_data:
            self.session.cmds.Flow.set_value(self.oid+'/settings/task_statues_filter', filter_data)
        if sort_data:
            self.session.cmds.Flow.set_value(self.oid+'/settings/task_sorted', sort_data)
        return self.session.cmds.Flow.call(
            self.oid+'/settings', 'update_presets', {}, {}
        )
