# Copyright 2021 Vincent Texier <vit@free.fr>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import annotations

from typing import Any, List, Optional

from PyQt5.QtCore import QAbstractItemModel, QLocale, QModelIndex, Qt, QVariant
from PyQt5.QtGui import QFont, QIcon, QPixmap

from tikka.domains.application import Application
from tikka.domains.entities.address import DisplayAddress
from tikka.domains.entities.constants import AMOUNT_UNIT_KEY
from tikka.domains.entities.identity import STATUS_VALIDATED
from tikka.interfaces.adapters.repository.accounts import AccountsRepositoryInterface
from tikka.interfaces.adapters.repository.preferences import (
    SELECTED_UNIT,
    TABLE_CATEGORY_FILTER,
    TABLE_SORT_COLUMN,
    TABLE_SORT_ORDER,
    TABLE_WALLET_FILTER,
)
from tikka.slots.pyqt.entities.constants import (
    ICON_ACCOUNT_NO_WALLET,
    ICON_ACCOUNT_WALLET_LOCKED,
    ICON_ACCOUNT_WALLET_UNLOCKED,
    ICON_IDENTITY,
)


class AccountTableModel(QAbstractItemModel):
    """
    AccountTableModel class that drives the population of table display
    """

    REPOSITORY_COLUMNS = [
        "",
        AccountsRepositoryInterface.COLUMN_IDENTITY_INDEX,
        AccountsRepositoryInterface.COLUMN_BALANCE,
        AccountsRepositoryInterface.COLUMN_NAME,
        AccountsRepositoryInterface.COLUMN_ADDRESS,
        AccountsRepositoryInterface.COLUMN_PATH,
        AccountsRepositoryInterface.COLUMN_ROOT,
        AccountsRepositoryInterface.COLUMN_CRYPTO_TYPE,
        AccountsRepositoryInterface.COLUMN_CATEGORY_ID,
    ]

    def __init__(self, application: Application, locale: QLocale):
        super().__init__()

        self.application = application
        self._ = self.application.translator.gettext
        # get parent widget locale to localize balance display
        self.locale = locale

        # calculate balance display by unit preference
        unit_preference = self.application.preferences_repository.get(SELECTED_UNIT)
        if unit_preference is not None:
            self.amount = self.application.amounts.get_amount(unit_preference)
        else:
            self.amount = self.application.amounts.get_amount(AMOUNT_UNIT_KEY)

        # drag and drop mime-type
        self.mime_type = "application/vnd.text.list"

        # Number of column displayed, see self.data()
        self._column_count = len(AccountTableModel.REPOSITORY_COLUMNS)

        self.table_view_data: List[AccountsRepositoryInterface.TableViewRow] = []

        self.init_data()

    def init_data(self):
        """
        Fill data from repository

        :return:
        """
        # calculate balance display by unit preference
        unit_preference = self.application.preferences_repository.get(SELECTED_UNIT)
        if unit_preference is not None:
            self.amount = self.application.amounts.get_amount(unit_preference)
        else:
            self.amount = self.application.amounts.get_amount(AMOUNT_UNIT_KEY)

        sort_column_index = self.application.preferences_repository.get(
            TABLE_SORT_COLUMN
        )
        if sort_column_index is not None:
            sort_column_index = int(sort_column_index)
        repository_sort_order = self.application.preferences_repository.get(
            TABLE_SORT_ORDER
        )

        filters = {}
        category_id_filter = self.application.preferences_repository.get(
            TABLE_CATEGORY_FILTER
        )
        if category_id_filter is not None:
            filters[
                AccountsRepositoryInterface.TABLE_VIEW_FILTER_BY_CATEGORY_ID
            ] = category_id_filter

        wallet_filter_preference = self.application.preferences_repository.get(
            TABLE_WALLET_FILTER
        )
        if wallet_filter_preference is not None:
            # preference store boolean as integer in a string column ("0" or "1")
            # convert it to boolean
            wallet_filter = int(wallet_filter_preference) == 1
            filters[
                AccountsRepositoryInterface.TABLE_VIEW_FILTER_BY_WALLET
            ] = wallet_filter

        if len(filters) == 0:
            filters = None

        self.beginResetModel()
        self.table_view_data = self.application.accounts.repository.table_view(
            filters,
            sort_column_index=sort_column_index,
            sort_order=repository_sort_order,
        )
        self.endResetModel()

    def rowCount(
        self, parent: QModelIndex = QModelIndex()  # pylint: disable=unused-argument
    ) -> int:
        """
        Return row count from account list

        :param parent: QModelIndex instance
        :return:
        """
        return len(self.table_view_data)

    def columnCount(
        self, parent: QModelIndex = QModelIndex()  # pylint: disable=unused-argument
    ) -> int:
        """
        Return column count of parent QModelIndex

        :param parent: QModelIndex instance
        :return:
        """
        return self._column_count

    def index(
        self, row: int, column: int, parent: QModelIndex = QModelIndex()
    ) -> QModelIndex:
        """
        Return QModelIndex for row, column and parent

        :param row: Row index
        :param column: Column index
        :param parent: Parent QModelIndex instance
        :return:
        """
        if not QAbstractItemModel.hasIndex(self, row, column, parent):
            return QModelIndex()

        if row < len(self.table_view_data):
            return QAbstractItemModel.createIndex(
                self, row, column, self.table_view_data[row]
            )

        return QModelIndex()

    def parent(
        self, child: Optional[QModelIndex] = None
    ):  # pylint: disable=unused-argument
        """
        Return parent QModelIndex of child QModelIndex

        :param child: QModelIndex instance
        :return:
        """
        return QModelIndex()

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        """
        Return data of cell for column index.column

        :param index: QModelIndex instance
        :param role: Item data role
        :return:
        """
        data = QVariant()
        if not index.isValid():
            return data

        table_view_row = self.table_view_data[index.row()]

        # display root account in italic
        if role == Qt.FontRole and table_view_row.root is None:
            font = QFont()
            font.setUnderline(True)
            return QVariant(font)

        # align right for balance column
        if (
            role == Qt.TextAlignmentRole
            and index.column()
            == AccountTableModel.REPOSITORY_COLUMNS.index(
                AccountsRepositoryInterface.COLUMN_BALANCE
            )
        ):
            return Qt.AlignRight

        # display account properties
        # display wallet lock status icon for account in first column
        if (
            index.column() == AccountTableModel.REPOSITORY_COLUMNS.index("")
            and role == Qt.DecorationRole
        ):
            if (
                table_view_row.wallet_address is not None
                and self.application.wallets.exists(table_view_row.wallet_address)
            ):
                data = (
                    QVariant(QIcon(QPixmap(ICON_ACCOUNT_WALLET_UNLOCKED)))
                    if self.application.wallets.is_unlocked(
                        table_view_row.wallet_address
                    )
                    else QVariant(QIcon(QPixmap(ICON_ACCOUNT_WALLET_LOCKED)))
                )
            else:
                data = QVariant(QIcon(QPixmap(ICON_ACCOUNT_NO_WALLET)))
        elif (
            index.column()
            == AccountTableModel.REPOSITORY_COLUMNS.index(
                AccountsRepositoryInterface.COLUMN_IDENTITY_INDEX
            )
            and role == Qt.DecorationRole
        ):
            if table_view_row.identity_index is not None:
                identity = self.application.identities.get(
                    table_view_row.identity_index
                )
                if identity is not None and identity.status == STATUS_VALIDATED:
                    data = QVariant(
                        QPixmap(ICON_IDENTITY).scaled(
                            16, 16, aspectRatioMode=Qt.KeepAspectRatio
                        )
                    )
        elif (
            index.column()
            == AccountTableModel.REPOSITORY_COLUMNS.index(
                AccountsRepositoryInterface.COLUMN_BALANCE
            )
            and role == Qt.DisplayRole
            and table_view_row.balance is not None
        ):
            data = QVariant(
                self.locale.toString(self.amount.value(table_view_row.balance), "f", 2)
            )
        elif index.column() == AccountTableModel.REPOSITORY_COLUMNS.index(
            AccountsRepositoryInterface.COLUMN_NAME
        ) and role in (Qt.DisplayRole, Qt.EditRole):
            data = QVariant(table_view_row.name)
        elif (
            index.column()
            == AccountTableModel.REPOSITORY_COLUMNS.index(
                AccountsRepositoryInterface.COLUMN_ADDRESS
            )
            and role == Qt.DisplayRole
        ):
            data = QVariant(table_view_row.address)
        elif (
            index.column()
            == AccountTableModel.REPOSITORY_COLUMNS.index(
                AccountsRepositoryInterface.COLUMN_PATH
            )
            and role == Qt.DisplayRole
        ):
            data = QVariant(table_view_row.path)
        elif (
            index.column()
            == AccountTableModel.REPOSITORY_COLUMNS.index(
                AccountsRepositoryInterface.COLUMN_ROOT
            )
            and role == Qt.DisplayRole
            and table_view_row.root is not None
        ):
            data = QVariant(DisplayAddress(table_view_row.root).shorten)
        elif (
            index.column()
            == AccountTableModel.REPOSITORY_COLUMNS.index(
                AccountsRepositoryInterface.COLUMN_CRYPTO_TYPE
            )
            and role == Qt.DisplayRole
        ):
            data = (
                QVariant("SR25519")
                if table_view_row.crypto_type == 1
                else QVariant("ED25519")
            )
        elif (
            index.column()
            == AccountTableModel.REPOSITORY_COLUMNS.index(
                AccountsRepositoryInterface.COLUMN_CATEGORY_ID
            )
            and role == Qt.DisplayRole
        ):
            data = (
                QVariant(table_view_row.category_name)
                if table_view_row.category_name is not None
                else QVariant()
            )

        return data

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,  # pylint: disable=unused-argument
        role: int = Qt.DisplayRole,
    ) -> QVariant:
        """
        Return header data

        :param section: Section offset
        :param orientation: Qt Orientation flag
        :param role: Qt Role flag
        :return:
        """
        data = QVariant()
        if (
            section == AccountTableModel.REPOSITORY_COLUMNS.index("")
            and role == Qt.DisplayRole
        ):
            data = QVariant(self._("Wallet"))
        elif (
            section
            == AccountTableModel.REPOSITORY_COLUMNS.index(
                AccountsRepositoryInterface.COLUMN_IDENTITY_INDEX
            )
            and role == Qt.DisplayRole
        ):
            data = QVariant(self._("Identity"))
        elif (
            section
            == AccountTableModel.REPOSITORY_COLUMNS.index(
                AccountsRepositoryInterface.COLUMN_BALANCE
            )
            and role == Qt.DisplayRole
        ):
            data = QVariant(
                self._("Balance ({symbol})").format(symbol=self.amount.symbol())
            )
        elif (
            section
            == AccountTableModel.REPOSITORY_COLUMNS.index(
                AccountsRepositoryInterface.COLUMN_NAME
            )
            and role == Qt.DisplayRole
        ):
            data = QVariant(self._("Name"))
        elif (
            section
            == AccountTableModel.REPOSITORY_COLUMNS.index(
                AccountsRepositoryInterface.COLUMN_ADDRESS
            )
            and role == Qt.DisplayRole
        ):
            data = QVariant(self._("Address"))
        elif (
            section
            == AccountTableModel.REPOSITORY_COLUMNS.index(
                AccountsRepositoryInterface.COLUMN_PATH
            )
            and role == Qt.DisplayRole
        ):
            data = QVariant(self._("Derivation"))
        elif (
            section
            == AccountTableModel.REPOSITORY_COLUMNS.index(
                AccountsRepositoryInterface.COLUMN_ROOT
            )
            and role == Qt.DisplayRole
        ):
            data = QVariant(self._("Root"))
        elif (
            section
            == AccountTableModel.REPOSITORY_COLUMNS.index(
                AccountsRepositoryInterface.COLUMN_CRYPTO_TYPE
            )
            and role == Qt.DisplayRole
        ):
            data = QVariant(self._("Crypto"))
        elif (
            section
            == AccountTableModel.REPOSITORY_COLUMNS.index(
                AccountsRepositoryInterface.COLUMN_CATEGORY_ID
            )
            and role == Qt.DisplayRole
        ):
            data = QVariant(self._("Category"))

        return data

    def sort(self, column: int, order: Qt.SortOrder = None) -> None:
        """
        Sort by column number in order

        :param column: Column index
        :param order: Qt.SortOrder flag
        :return:
        """
        if column > -1:
            sort_order = (
                AccountsRepositoryInterface.SORT_ORDER_ASCENDING
                if order == Qt.AscendingOrder
                else AccountsRepositoryInterface.SORT_ORDER_DESCENDING
            )
            self.application.preferences_repository.set(TABLE_SORT_COLUMN, str(column))
            self.application.preferences_repository.set(TABLE_SORT_ORDER, sort_order)
            self.init_data()
