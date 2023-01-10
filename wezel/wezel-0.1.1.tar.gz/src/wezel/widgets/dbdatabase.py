from PyQt5.QtCore import  Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QTreeWidget, QTreeWidgetItem, QFileSystemModel, QTreeView,
)

class DICOMFolderTree(QTreeWidget):
    """Displays a DICOM folder as a Tree."""

    itemSelectionChanged = pyqtSignal(dict)
    itemDoubleClicked = pyqtSignal(dict)
    databaseSet = pyqtSignal()

    def __init__(self, folder):
        super().__init__()

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.itemDoubleClicked.connect(lambda item, col: self._itemDoubleClickedEvent(item, col))
        self.itemClicked.connect(lambda item, col: self._itemClickedEvent(item, col))
        # self.setModel(QFileSystemModel()) #This only works for QTreeView
        self.setFolder(folder)

    def setFolder(self, folder=None):
        if folder is not None: 
            self.database=folder
        self.dict = {
            'label': self.database.manager.path,
            'level': 'Database',
            'uid': 'Database',
            'key': None,
        }
        self.setUpdatesEnabled(False)
        self.clear()
        self.setHeaderLabels([self.database.manager.path])
        # This does not show empty patients or studies
        database = self.database.manager.tree()
        for patient in database['patients']:
            patientWidget = self._treeWidgetItem('Patient', patient, self)
            for study in patient['studies']:
                studyWidget = self._treeWidgetItem('Study', study, patientWidget)
                for sery in study['series']:
                    seriesWidget = self._treeWidgetItem('Series', sery, studyWidget)
        self.setUpdatesEnabled(True)
        #self.databaseSet.emit()


    def _treeWidgetItem(self, level, record, parent, expanded=True):
        """Build an item in the Tree"""

        item = QTreeWidgetItem(parent)
        # Custom attributes
        item.checked = False
        item.dict = {
            'label': self.database.manager.label(key=record['key'], type=level),
            'level': level,
            'uid': record['uid'],
            'key': record['key'],
        }
        # Built-in attributes
        item.setText(0, item.dict['label'])
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable)
        item.setCheckState(0, Qt.Unchecked)
        item.setExpanded(expanded)
        return item


    def _itemDoubleClickedEvent(self, item, col):
        self.itemDoubleClicked.emit(item.dict)

    def _itemClickedEvent(self, item, col):
        """Update checked state of children and parents"""

        self.setUpdatesEnabled(False)
        #item.treeWidget().blockSignals(True)
        if was_toggled(item):
            checked = item.checkState(0) == Qt.Checked
            _set_checked(item, checked)
            #_check_children(item, item.checked)
        else:       
            selectedItems = self.selectedItems()
            if selectedItems:
                if len(selectedItems) == 1:
                    checked = item.checkState(0) == Qt.Checked
                    self.uncheck_all()
                    _set_checked(item, not checked)
                else:
                    self.uncheck_all()
                    for i in selectedItems:
                        _set_checked(i, True) 
        #item.treeWidget().blockSignals(False)
        self.setUpdatesEnabled(True)
        self.itemSelectionChanged.emit(item.dict)


    def selectRecords(self, uid, checked=True):

        root = self.invisibleRootItem()
        if uid == 'Database':
            _check_children(root, checked)
        else:
            generation = [root]
            for _ in range(3):
                generation = _children(generation)
                for item in generation:
                    if item.dict['uid'] == uid:
                        _set_checked(item, checked)
                        return

    def uncheck_all(self):
        """Uncheck all TreeView items."""

        self.selectRecords('Database', False)


    def get_selected(self, generation=1):
        if generation == 4: 
            return []
        try:
            root = self.invisibleRootItem()
        except RuntimeError:
            return []
        if generation == 0:
            records = []
            for gen in [1,2,3]:
                records += self.get_selected(gen)
            return records
        items = _children([root])
        while generation > 1:
            items = _children(items)
            generation -= 1
        return [self.database.record(i.dict['level'], i.dict['uid']) for i in items if i.checkState(0)==Qt.Checked]

    def selected(self, generation):
        if isinstance(generation, str):
            if generation == 'Patients':
                generation=1
            elif generation == 'Studies':
                generation=2
            elif generation == 'Series':
                generation=3
            elif generation == 'Instances':
                generation=4
        if generation == 4: 
            return []  
        return self.get_selected(generation) 

    def nr_selected(self, generation):
        if isinstance(generation, str):
            if generation == 'Patients':
                generation=1
            elif generation == 'Studies':
                generation=2
            elif generation == 'Series':
                generation=3
            elif generation == 'Instances':
                generation=4
        selected = self.get_selected(generation)
        return len(selected)            

def was_toggled(item):

    checked = item.checkState(0) == Qt.Checked
    return checked != item.checked

def _set_checked(item, checked):
    """Check or uncheck an item"""

    if checked: 
        item.setCheckState(0, Qt.Checked)
        #item.setSelected(True)
    else: 
        item.setCheckState(0, Qt.Unchecked)
        #item.setSelected(False)
    item.checked = checked
    _check_children(item, checked)


def _check_children(item, checked):
    """Set the checkstate of all children of an item."""

    for child in _children([item]):
        _set_checked(child, checked)


def _children(items):

    children = []
    for item in items:
        cnt = item.childCount()
        children += [item.child(i) for i in range(cnt)]
    return children