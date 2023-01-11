from kabaret.app.ui.gui.widgets.flow.flow_view import QtCore, QtGui, QtWidgets
from kabaret.app import resources

from libreflow.baseflow.runners import CHOICES_ICONS
from ....resources.icons import gui


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


class TargetInput(QtWidgets.QLineEdit):

    def __init__(self, widget, page):
        QtWidgets.QLineEdit.__init__(self)
        self.widget = widget
        self.page = page
        self.target_original = ''
    
        self.editingFinished.connect(self._on_target_finish_edit)
        self.setDragEnabled(True)

    def checkTarget(self):
        if self.text() == '':
            return
            
        self.blockSignals(True)
        if self.text() == self.target_original:
            if not self.property('error'):
                self.set_source_display()
            return self.blockSignals(False)

        self.target_original = self.text()
        task_name = self.page.check_new_target(self.text())
        if task_name is None:
            self.setProperty('error', True)
            self.setStyleSheet('''
                QLineEdit {
                    border-color: red;
                }
                QToolTip {
                    background-color: #ffaaaa;
                    color: black;
                    border-color: red;
                }
            ''')
            if self.text()[-1] == '/':
                error = '!!!\nERROR: The last character must not be a slash.'
            else:
                error = '!!!\nERROR: You need to specify a task entity.'
            self.setToolTip(error)
            self.widget.checkbox.setEnabled(False)
            self.widget.checkbox.setCheckState(QtCore.Qt.Unchecked)
            self.widget.statusicon.setIcon(self.widget.ICON_BY_STATUS['Warning'])
            return self.blockSignals(False)
        
        self.setProperty('error', False)
        self.setStyleSheet('')
        self.setToolTip('')
        self.widget.item.file_target.set(self.text())
        self.widget.item.task_name.set(task_name)
        self.widget.file_preset_name.clear()
        self.widget.file_preset_name.addItems(self.page.session.cmds.Flow.call(self.widget.oid, 'get_files_choices', {}, {}))
        self.set_source_display()
        self.blockSignals(False)

    def set_source_display(self):
        if self.text() == '':
            return

        split = self.text().split('/')
        indices = list(range(len(split) - 1, 2, -2))
        self.setText(' · '.join([split[i] for i in reversed(indices)]))

    def focusInEvent(self, event):
        if event.reason() != QtCore.Qt.PopupFocusReason:
            self.setText(self.target_original)
        super(TargetInput, self).focusInEvent(event)

    def dragEnterEvent(self, event):
        if self.page.session.cmds.Flow.can_handle_mime_formats(event.mimeData().formats()):
            event.acceptProposedAction()
        else:
            return super(TargetInput, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if self.page.session.cmds.Flow.can_handle_mime_formats(event.mimeData().formats()):
            event.acceptProposedAction()
        else:
            return super(TargetInput, self).dragMoveEvent(event)

    def dropEvent(self, event):
        self.setText(event.mimeData().text())
        self.checkTarget()
         
    def _on_target_finish_edit(self):
        self.checkTarget()


class FileItem(QtWidgets.QWidget):

    ICON_BY_STATUS = {
        'OK':   ('icons.libreflow', 'available'),
        'NEW':   ('icons.libreflow', 'available'),
        'Warning': ('icons.libreflow', 'warning'),
        'Unknown':   ('icons.libreflow', 'error')
    }

    def __init__(self, files_list, item):
        super(FileItem, self).__init__()
        self.setObjectName('FileItem')
        self.list = files_list
        self.page_widget = files_list.page_widget
        self.item = item
        self.oid = item.oid()
       
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet('''QWidget#FileItem {background-color: #3e4041;}''')
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._on_context_menu)

        self.build()
        self.refresh(True)

    def build(self):
        container = QtWidgets.QVBoxLayout()
        container.setMargin(10)

        header_lo = QtWidgets.QHBoxLayout()
        self.checkbox = QtWidgets.QCheckBox()
        self.checkbox.setEnabled(False)
        self.fileicon = LabelIcon()
        self.filename = QtWidgets.QLabel()
        self.arrow = QtWidgets.QLabel('➜')
        self.file_preset_name = QtWidgets.QComboBox()
        self.preset_edit = QtWidgets.QLineEdit()
        self.preset_edit.setObjectName('PresetComboBox')
        self.file_preset_name.setLineEdit(self.preset_edit)
        self.file_revision = QtWidgets.QLabel()
        self.statusicon = LabelIcon()

        header_lo.addWidget(self.checkbox)
        header_lo.addWidget(self.fileicon)
        header_lo.addWidget(self.filename)
        header_lo.addWidget(self.arrow)
        header_lo.addWidget(self.file_preset_name)
        header_lo.addStretch()
        header_lo.addWidget(self.file_revision)
        header_lo.addWidget(self.statusicon)

        settings_lo = QtWidgets.QHBoxLayout()
        target_label = QtWidgets.QLabel('Target')
        self.target_input = TargetInput(self, self.page_widget)
        comment_label = QtWidgets.QLabel('Comment')
        self.comment_input = QtWidgets.QLineEdit()
        self.comment_input.editingFinished.connect(self._on_comment_finish_edit)

        settings_lo.addWidget(target_label)
        settings_lo.addWidget(self.target_input)
        settings_lo.addWidget(comment_label)
        settings_lo.addWidget(self.comment_input)

        container.addLayout(header_lo)
        container.addLayout(settings_lo)
        self.setLayout(container)

    def refresh(self, init=False):
        self.status = self.item.file_status.get()
        if self.status == 'OK' or self.status == 'NEW':
            self.checkbox.setEnabled(True)
            self.checkbox.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkbox.setEnabled(False)
            self.checkbox.setCheckState(QtCore.Qt.Unchecked)
        self.statusicon.setIcon(self.ICON_BY_STATUS[self.item.file_status.get()])
        self.file_revision.setText(self.item.rev_version.get())
        if init:
            if self.item.file_format.get():
                self.fileicon.setIcon(CHOICES_ICONS.get(self.item.file_format.get(), ('icons.gui', 'text-file-1')))
            else:
                self.fileicon.setIcon(('icons.gui', 'folder-white-shape'))
            self.filename.setText(self.item.file_name.get())
            self.file_preset_name.setCurrentText(self.item.file_preset_name.get())
            self.file_preset_name.currentIndexChanged.connect(self._on_preset_finish_edit)
            self.preset_edit.editingFinished.connect(self._on_preset_finish_edit)
            self.target_input.setText(self.item.file_target.get())
            self.target_input.set_source_display()
            self.target_input.target_original = self.item.file_target.get()
            if self.item.task_name.get() != '':
                self.file_preset_name.addItems(self.page_widget.session.cmds.Flow.call(self.oid, 'get_files_choices', {}, {}))

    def event(self, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
                widget = QtWidgets.QApplication.focusWidget()
                if isinstance(widget, TargetInput):
                    if not widget.property('error'):
                        widget.blockSignals(True)
                        widget.focusNextPrevChild(True)
                        widget.blockSignals(False)
                else:
                    widget.clearFocus()
        return super().event(event)

    def _on_comment_finish_edit(self):
        self.item.file_comment.set(self.comment_input.text())

    def _on_preset_finish_edit(self):
        if self.target_input.text() == '':
            return

        if not self.target_input.property('error'):
            self.item.file_preset_name.set(self.file_preset_name.currentText())
            self.page_widget.session.cmds.Flow.call(self.oid, 'check_revision', {}, {})
            self.refresh()

    def _on_remove_file_action_clicked(self):
        self.page_widget.remove_file(self.item.name())
        self.deleteLater()
        self.list.refresh()

    def _on_context_menu(self, event):
        context_menu = QtWidgets.QMenu(self)
        remove_file = context_menu.addAction(QtGui.QIcon(resources.get_icon(('icons.gui', 'remove-symbol'))), 'Remove File')
        remove_file.triggered.connect(self._on_remove_file_action_clicked)

        context_menu.exec_(self.mapToGlobal(event))


class FilesList(QtWidgets.QScrollArea):

    def __init__(self, page_widget):
        super(FilesList, self).__init__()
        self.page_widget = page_widget
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setAcceptDrops(True)
        self.setWidgetResizable(True)

        self.build()

    def build(self):
        container = QtWidgets.QWidget()
        container.setObjectName('ScrollAreaContainer')
        container.setStyleSheet('QWidget#ScrollAreaContainer {background-color: #2b2b2b;}')
        self.layout = QtWidgets.QVBoxLayout(container)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.setSpacing(10)
        self.layout.setMargin(10)
        self.setWidget(container)

    def refresh(self, force_update=False):
        if force_update:
            files = self.page_widget.get_files()
        
            for f in files:
                exist = False
                for i in reversed(range(self.layout.count())):
                    if self.layout.itemAt(i).widget().oid == f.oid():
                        exist = True
                if not exist:
                    item = FileItem(self, f)
                    self.layout.addWidget(item)

        count = self.page_widget.refresh_files_count()
        if count > 0:
            if self.page_widget.files_list.isVisible() == False:
                self.page_widget.files_list.show()
                self.page_widget.dragdrop.hide()
                self.page_widget.checkbox_selectall.setEnabled(True)
                self.page_widget.checkbox_selectall.setCheckState(QtCore.Qt.Checked)
            self.page_widget.button_import.setEnabled(True)
        else:
            self.page_widget.files_list.hide()
            self.page_widget.dragdrop.show()
            self.page_widget.checkbox_selectall.setEnabled(False)
            self.page_widget.checkbox_selectall.setCheckState(QtCore.Qt.Unchecked)
            self.page_widget.button_import.setEnabled(False)

    def sizeHint(self):
        return QtCore.QSize(800, 500)

    def get_count(self):
        return len(self.page_widget.get_files())

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
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.page_widget.add_files(links)
        else:
            event.ignore()
