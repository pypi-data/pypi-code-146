# -*- coding: utf-8 -*-

##########################################################################
# OpenLP - Open Source Lyrics Projection                                 #
# ---------------------------------------------------------------------- #
# Copyright (c) 2008-2023 OpenLP Developers                              #
# ---------------------------------------------------------------------- #
# This program is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <https://www.gnu.org/licenses/>. #
##########################################################################

from PyQt5 import QtWidgets

from openlp.core.common.i18n import translate
from openlp.core.lib.ui import create_button_box


class Ui_AddGroupDialog(object):
    def setup_ui(self, add_group_dialog):
        add_group_dialog.setObjectName('add_group_dialog')
        add_group_dialog.resize(300, 10)
        self.dialog_layout = QtWidgets.QVBoxLayout(add_group_dialog)
        self.dialog_layout.setObjectName('dialog_layout')
        self.name_layout = QtWidgets.QFormLayout()
        self.name_layout.setObjectName('name_layout')
        self.parent_group_label = QtWidgets.QLabel(add_group_dialog)
        self.parent_group_label.setObjectName('parent_group_label')
        self.parent_group_combobox = QtWidgets.QComboBox(add_group_dialog)
        self.parent_group_combobox.setObjectName('parent_group_combobox')
        self.name_layout.addRow(self.parent_group_label, self.parent_group_combobox)
        self.name_label = QtWidgets.QLabel(add_group_dialog)
        self.name_label.setObjectName('name_label')
        self.name_edit = QtWidgets.QLineEdit(add_group_dialog)
        self.name_edit.setObjectName('name_edit')
        self.name_label.setBuddy(self.name_edit)
        self.name_layout.addRow(self.name_label, self.name_edit)
        self.dialog_layout.addLayout(self.name_layout)
        self.button_box = create_button_box(add_group_dialog, 'button_box', ['cancel', 'save'])
        self.dialog_layout.addWidget(self.button_box)
        self.retranslate_ui(add_group_dialog)
        add_group_dialog.setMaximumHeight(add_group_dialog.sizeHint().height())

    def retranslate_ui(self, add_group_dialog):
        add_group_dialog.setWindowTitle(translate('ImagePlugin.AddGroupForm', 'Add group'))
        self.parent_group_label.setText(translate('ImagePlugin.AddGroupForm', 'Parent group:'))
        self.name_label.setText(translate('ImagePlugin.AddGroupForm', 'Group name:'))
