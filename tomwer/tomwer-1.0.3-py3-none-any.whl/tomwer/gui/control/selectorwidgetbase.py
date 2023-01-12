from silx.gui import qt
import logging

_logger = logging.getLogger(__name__)


class _SelectorWidget(qt.QWidget):
    """widget used to select a dataset on a list (a scan or a volume for now)"""

    sigSelectionChanged = qt.Signal(list)
    """Signal emitted when the selection changed"""

    sigUpdated = qt.Signal()
    """signal emitted when the scan list change"""

    def __init__(self, parent=None):

        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QVBoxLayout())
        self.dataList = self._buildDataList()
        self.dataList.setSelectionMode(qt.QAbstractItemView.ExtendedSelection)
        self.layout().addWidget(self.dataList)
        self.layout().addWidget(self._getAddAndRmButtons())
        self.layout().addWidget(self._getSendButton())
        self.setAcceptDrops(True)

    def add(self, scan):
        added_scans = self.dataList.add(scan)
        self.sigUpdated.emit()
        return added_scans

    def remove(self, scan):
        self.dataList.remove(scan)
        self.sigUpdated.emit()

    def n_data(self) -> int:
        return len(self.dataList.items)

    def _buildDataList(self):
        raise NotImplementedError("Base class")

    def _getAddAndRmButtons(self):
        lLayout = qt.QHBoxLayout()
        w = qt.QWidget(self)
        w.setLayout(lLayout)
        self._addButton = qt.QPushButton("Add")
        self._addButton.clicked.connect(self._callbackAddData)
        self._rmButton = qt.QPushButton("Remove")
        self._rmButton.clicked.connect(self._callbackRemoveData)

        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        lLayout.addWidget(spacer)
        lLayout.addWidget(self._addButton)
        lLayout.addWidget(self._rmButton)

        return w

    def _getSendButton(self):
        lLayout = qt.QHBoxLayout()
        widget = qt.QWidget(self)
        widget.setLayout(lLayout)
        self._sendButton = qt.QPushButton("Select")
        self._sendButton.clicked.connect(self._selectActiveData)

        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        lLayout.addWidget(spacer)
        lLayout.addWidget(self._sendButton)

        return widget

    def selectAll(self):
        self.dataList.selectAll()

    def setMySelection(self, selection: tuple):
        self.dataList.setMySelection(selection)

    def _callbackAddData(self):
        raise NotImplementedError("Base class")

    def _selectActiveData(self):
        sItem = self.dataList.selectedItems()
        if sItem and len(sItem) >= 1:
            selection = [_item.text() for _item in sItem]
            self.sigSelectionChanged.emit(list(selection))
        else:
            _logger.warning("No active scan detected")

    def _callbackRemoveData(self):
        """ """
        selectedItems = self.dataList.selectedItems()
        if selectedItems is not None:
            for item in selectedItems:
                self.dataList.remove_item(item)
        self.sigUpdated.emit()

    def setActiveData(self, data):
        """
        set the given scan as the active one

        :param scan: the scan to set active
        :type scan: Union[str, TomoBase]
        """
        data_id = data
        self.dataList.setCurrentItem(self.dataList.items[data_id])
