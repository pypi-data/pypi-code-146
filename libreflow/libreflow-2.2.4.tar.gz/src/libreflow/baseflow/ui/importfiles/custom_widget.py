import time

from kabaret.app.ui.gui.widgets.flow.flow_view import QtCore, QtGui, QtWidgets, CustomPageWidget
from kabaret.app import resources

from .files_list import FilesList

STYLESHEET = '''
    QPushButton:disabled {
        background-color: rgba(255, 255, 255, 0);
        color: rgba(255, 255, 255, 50);
    }
    QLineEdit#PresetComboBox {
        border: none;
        padding: 0px;
    }
'''

class WaitThread(QtCore.QThread):

    def run(self):
        pass


class DragDropWidget(QtWidgets.QWidget):

    def __init__(self, custom_widget):
        super(DragDropWidget, self).__init__(custom_widget)
        self.custom_widget = custom_widget

        self.setAcceptDrops(True)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.frame = QtWidgets.QFrame()
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setStyleSheet('''
            background-color: #2b2b2b;
            border: 1px solid #22222b;
        ''')

        self.asset = QtWidgets.QWidget()
        asset_lo = QtWidgets.QVBoxLayout()
        icon = QtGui.QIcon(resources.get_icon(('icons.gui', 'file')))
        pixmap = icon.pixmap(QtCore.QSize(128, 128))
        self.icon_lbl = QtWidgets.QLabel('')
        self.icon_lbl.setPixmap(pixmap)
        self.label = QtWidgets.QLabel('Drop your files here')

        asset_lo.addWidget(self.icon_lbl, 0, QtCore.Qt.AlignCenter)
        asset_lo.addWidget(self.label, 1, QtCore.Qt.AlignCenter)
        self.asset.setLayout(asset_lo)
        
        glo = QtWidgets.QGridLayout()
        glo.setContentsMargins(0,0,0,0)
        glo.addWidget(self.frame, 0, 0, 3, 0)
        glo.addWidget(self.asset, 1, 0, QtCore.Qt.AlignCenter)
        self.setLayout(glo)

    def sizeHint(self):
        return QtCore.QSize(800, 493)

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
            self.custom_widget.add_files(links)
        else:
            event.ignore()


class ImportFilesWidget(CustomPageWidget):

    def build(self):
        self.setStyleSheet(STYLESHEET)

        self.clear_list()

        self.files_list = FilesList(self)
        self.files_count = QtWidgets.QLabel(str(self.files_list.get_count())+' files')
        self.dragdrop = DragDropWidget(self)
        
        self.button_settings = QtWidgets.QPushButton('Settings')
        self.button_settings.setAutoDefault(False)

        # self.button_browse = QtWidgets.QPushButton('Browse')
        self.checkbox_selectall = QtWidgets.QCheckBox('Select all')
        self.checkbox_selectall.setEnabled(False)
        self.label_feedback = QtWidgets.QLabel('')
        self.button_import = QtWidgets.QPushButton('Import')
        self.button_import.setAutoDefault(False)

        if self.files_list.get_count() == 0:
            self.files_list.hide()
            self.button_import.setEnabled(False)
        else:
            self.dragdrop.hide()
        
        glo = QtWidgets.QGridLayout()
        glo.addWidget(self.files_count, 0, 0, 1, 6)
        glo.addWidget(self.files_list, 1, 0, 1, 6)
        glo.addWidget(self.dragdrop, 1, 0, 1, 6)
        glo.addWidget(self.button_settings, 2, 0)
        # glo.addWidget(self.button_browse, 2, 1)
        glo.addWidget(self.checkbox_selectall, 2, 1)
        glo.addWidget(self.label_feedback, 2, 3, QtCore.Qt.AlignRight)
        glo.addWidget(self.button_import, 2, 4)
        glo.setColumnStretch(2, 2)
        self.setLayout(glo)
    
        self.button_settings.clicked.connect(self._on_button_settings_clicked)
        # self.button_browse.clicked.connect(self._on_button_browse_clicked)
        self.checkbox_selectall.stateChanged.connect(self._on_checkbox_selectall_state_changed)
        self.button_import.clicked.connect(self._on_button_import_clicked)

        self.wait = WaitThread()
        if not self.wait.isRunning():
            self.wait.start()
            self.wait.finished.connect(self._add_base_files)

    def _add_base_files(self):
        if self.session.cmds.Flow.get_value(self.oid+'/paths') != []:
            self.add_files(self.session.cmds.Flow.get_value(self.oid+'/paths'))

    def add_files(self, paths):
        self.button_import.setEnabled(False)
        self.label_feedback.setText('Waiting...')
        QtWidgets.QApplication.processEvents()
        QtWidgets.QApplication.processEvents()

        self.session.cmds.Flow.call(self.oid, 'check_files', [paths], {})
        self.files_list.refresh(True)
       
        self.label_feedback.setText('')
        self.session.cmds.Flow.set_value(self.oid+'/paths', [])

    def remove_file(self, name):
        return self.session.cmds.Flow.call(
            self.oid + '/settings/files_map', 'remove', [name], {}
        )

    def clear_list(self):
        return self.session.cmds.Flow.call(
            self.oid + '/settings/files_map', 'clear', {}, {}
        )

    def get_files(self):
        return self.session.cmds.Flow.call(
            self.oid + '/settings/files_map', 'mapped_items', {}, {}
        )

    def refresh_files_count(self):
        count = self.files_list.get_count()
        if count == 1:
            self.files_count.setText(str(count)+' file')
        else:
            self.files_count.setText(str(count)+' files')
        return count
    
    def check_new_target(self, target):
        return self.session.cmds.Flow.call(
            self.oid, 'check_new_target', [target], {}
        )

    def _on_button_settings_clicked(self):
        self.page.goto(self.oid + '/settings')

    # def _on_button_browse_clicked(self):
    #     dialog = QtWidgets.QFileDialog()
    #     dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
    #     dialog.setStyleSheet('''
    #         QLineEdit:focus {
    #             border: none;
    #             padding: 0px;
    #             padding-left: 2px;
    #         }
    #     ''')
    #     dialog.setFileMode(QtWidgets.QFileDialog.Directory)
    #     dialog.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)

    #     file_view = dialog.findChild(QtWidgets.QListView, 'listView')
    #     if file_view:
    #         file_view.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
    #         file_view.setSelectionRectVisible(True)
    #     f_tree_view = dialog.findChild(QtWidgets.QTreeView)
    #     if f_tree_view:
    #         f_tree_view.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

    #     if dialog.exec():
    #         paths = dialog.selectedFiles()
    #         self.add_files(paths)

    def _on_checkbox_selectall_state_changed(self, state):
        state = QtCore.Qt.CheckState(state)
        for i in range(self.files_list.layout.count()):
            widget = self.files_list.layout.itemAt(i).widget()
            if widget:
                if widget.status == 'OK' or widget.status == 'NEW':
                    widget.checkbox.setCheckState(state)

    def _on_button_import_clicked(self):
        files = []
        for i in range(self.files_list.layout.count()):
            widget = self.files_list.layout.itemAt(i).widget()
            if widget:
                if widget.checkbox.checkState() == QtCore.Qt.Checked:
                    files.append(widget.item)
        
        self.button_import.setEnabled(False)
        self.label_feedback.setText('Importing...')
        QtWidgets.QApplication.processEvents()
        QtWidgets.QApplication.processEvents()
        
        self.session.cmds.Flow.call(
            self.oid, 'import_files', [files], {}
        )

        self.files_list.refresh(True)

        self.label_feedback.setText('Completed')