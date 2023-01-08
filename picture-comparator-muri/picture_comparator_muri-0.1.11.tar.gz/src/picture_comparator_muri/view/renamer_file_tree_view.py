from __future__ import annotations

from PySide6.QtGui import QDropEvent
from PySide6.QtWidgets import QTreeView


class RenamerFileTreeView(QTreeView):
    def dropEvent(self, event: QDropEvent) -> None:
        print("Dropping", event)
        super().dropEvent(event)

    def startDrag(self, supportedActions: Qt.DropActions) -> None:
        print("Strat drag", supportedActions)
        return super().startDrag(supportedActions)

