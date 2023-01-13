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

import logging
from pathlib import Path

from PyQt5 import QtCore, QtWidgets

from openlp.core.common import delete_file, get_images_filter, sha256_file_hash
from openlp.core.common.applocation import AppLocation
from openlp.core.common.i18n import UiStrings, get_natural_key, translate
from openlp.core.common.path import create_paths
from openlp.core.common.registry import Registry
from openlp.core.common.enum import ImageThemeMode
from openlp.core.lib import ServiceItemContext, build_icon, check_item_selected, create_thumb, validate_thumb
from openlp.core.lib.mediamanageritem import MediaManagerItem
from openlp.core.lib.plugin import StringContent
from openlp.core.lib.serviceitem import ItemCapabilities
from openlp.core.lib.ui import create_widget_action, critical_error_message_box
from openlp.core.ui.icons import UiIcons
from openlp.core.widgets.views import TreeWidgetWithDnD
from openlp.plugins.images.forms.addgroupform import AddGroupForm
from openlp.plugins.images.forms.choosegroupform import ChooseGroupForm
from openlp.plugins.images.lib.db import ImageFilenames, ImageGroups


log = logging.getLogger(__name__)


class ImageMediaItem(MediaManagerItem):
    """
    This is the custom media manager item for images.
    """
    images_go_live = QtCore.pyqtSignal(list)
    images_add_to_service = QtCore.pyqtSignal(list)
    log.info('Image Media Item loaded')

    def __init__(self, parent, plugin):
        self.icon_path = 'images/image'
        self.manager = None
        self.choose_group_form = None
        self.add_group_form = None
        super(ImageMediaItem, self).__init__(parent, plugin)

    def setup_item(self):
        """
        Do some additional setup.
        """
        self.images_go_live.connect(self.go_live_remote)
        self.images_add_to_service.connect(self.add_to_service_remote)
        self.quick_preview_allowed = True
        self.has_search = True
        self.manager = self.plugin.manager
        self.choose_group_form = ChooseGroupForm(self)
        self.add_group_form = AddGroupForm(self)
        self.fill_groups_combobox(self.choose_group_form.group_combobox)
        self.fill_groups_combobox(self.add_group_form.parent_group_combobox)
        Registry().register_function('live_theme_changed', self.on_display_changed)
        Registry().register_function('slidecontroller_live_started', self.on_display_changed)
        # Allow DnD from the desktop.
        self.list_view.activateDnD()

    def retranslate_ui(self):
        self.on_new_prompt = translate('ImagePlugin.MediaItem', 'Select Image(s)')
        file_formats = get_images_filter()
        self.on_new_file_masks = '{formats};;{files} (*)'.format(formats=file_formats, files=UiStrings().AllFiles)
        self.add_group_action.setText(UiStrings().AddGroupDot)
        self.add_group_action.setToolTip(UiStrings().AddGroupDot)
        self.replace_action.setText(UiStrings().ReplaceBG)
        self.replace_action.setToolTip(UiStrings().ReplaceLiveBG)
        self.replace_action_context.setText(UiStrings().ReplaceBG)
        self.replace_action_context.setToolTip(UiStrings().ReplaceLiveBG)
        self.reset_action.setText(UiStrings().ResetBG)
        self.reset_action.setToolTip(UiStrings().ResetLiveBG)
        self.reset_action_context.setText(UiStrings().ResetBG)
        self.reset_action_context.setToolTip(UiStrings().ResetLiveBG)

    def required_icons(self):
        """
        Set which icons the media manager tab should show.
        """
        super().required_icons()
        self.has_file_icon = True
        self.has_new_icon = False
        self.has_edit_icon = False
        self.add_to_service_item = True

    def initialise(self):
        log.debug('initialise')
        self.list_view.clear()
        self.list_view.setIconSize(QtCore.QSize(88, 50))
        self.list_view.setIndentation(self.list_view.default_indentation)
        self.list_view.allow_internal_dnd = True
        self.service_path = AppLocation.get_section_data_path(self.settings_section) / 'thumbnails'
        create_paths(self.service_path)
        # Load images from the database
        self.load_full_list(
            self.manager.get_all_objects(ImageFilenames, order_by_ref=ImageFilenames.file_path), initial_load=True)

    def add_list_view_to_toolbar(self):
        """
        Creates the main widget for listing items the media item is tracking. This method overloads
        MediaManagerItem.add_list_view_to_toolbar.
        """
        # Add the List widget
        self.list_view = TreeWidgetWithDnD(self, self.plugin.name)
        self.list_view.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list_view.setAlternatingRowColors(True)
        self.list_view.setObjectName('{name}TreeView'.format(name=self.plugin.name))
        # Add to pageLayout
        self.page_layout.addWidget(self.list_view)
        # define and add the context menu
        self.list_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        if self.has_edit_icon:
            create_widget_action(
                self.list_view,
                text=self.plugin.get_string(StringContent.Edit)['title'],
                icon=UiIcons().edit,
                triggers=self.on_edit_click)
            create_widget_action(self.list_view, separator=True)
        create_widget_action(
            self.list_view,
            'listView{name}{preview}Item'.format(name=self.plugin.name.title(), preview=StringContent.Preview.title()),
            text=self.plugin.get_string(StringContent.Preview)['title'],
            icon=UiIcons().preview,
            can_shortcuts=True,
            triggers=self.on_preview_click)
        create_widget_action(
            self.list_view,
            'listView{name}{live}Item'.format(name=self.plugin.name.title(), live=StringContent.Live.title()),
            text=self.plugin.get_string(StringContent.Live)['title'],
            icon=UiIcons().live,
            can_shortcuts=True,
            triggers=self.on_live_click)
        create_widget_action(
            self.list_view,
            'listView{name}{service}Item'.format(name=self.plugin.name.title(), service=StringContent.Service.title()),
            can_shortcuts=True,
            text=self.plugin.get_string(StringContent.Service)['title'],
            icon=UiIcons().add,
            triggers=self.on_add_click)
        if self.add_to_service_item:
            create_widget_action(self.list_view, separator=True)
            create_widget_action(
                self.list_view,
                text=translate('OpenLP.MediaManagerItem', '&Add to selected Service Item'),
                icon=UiIcons().add,
                triggers=self.on_add_edit_click)
            create_widget_action(self.list_view, separator=True)
        if self.has_delete_icon:
            create_widget_action(
                self.list_view,
                'listView{name}{delete}Item'.format(name=self.plugin.name.title(), delete=StringContent.Delete.title()),
                text=self.plugin.get_string(StringContent.Delete)['title'],
                icon=UiIcons().delete,
                can_shortcuts=True, triggers=self.on_delete_click)
        self.add_custom_context_actions()
        # Create the context menu and add all actions from the list_view.
        self.menu = QtWidgets.QMenu()
        self.menu.addActions(self.list_view.actions())
        self.list_view.doubleClicked.connect(self.on_double_clicked)
        self.list_view.itemSelectionChanged.connect(self.on_selection_change)
        self.list_view.customContextMenuRequested.connect(self.context_menu)
        self.list_view.addAction(self.replace_action)

    def add_custom_context_actions(self):
        """
        Add custom actions to the context menu.
        """
        create_widget_action(self.list_view, separator=True)
        create_widget_action(
            self.list_view,
            text=UiStrings().AddGroup, icon=UiIcons().folder, triggers=self.on_add_group_click)
        create_widget_action(
            self.list_view,
            text=translate('ImagePlugin', 'Add new image(s)'),
            icon=UiIcons().open, triggers=self.on_file_click)
        create_widget_action(self.list_view, separator=True)
        self.replace_action_context = create_widget_action(
            self.list_view, text=UiStrings().ReplaceBG, icon=UiIcons().theme, triggers=self.on_replace_click)
        self.reset_action_context = create_widget_action(
            self.list_view, text=UiStrings().ReplaceLiveBG, icon=UiIcons().close,
            visible=False, triggers=self.on_reset_click)

    def add_middle_header_bar(self):
        """
        Add custom buttons to the start of the toolbar.
        """
        self.add_group_action = self.toolbar.add_toolbar_action('add_group_action',
                                                                icon=UiIcons().folder,
                                                                triggers=self.on_add_group_click)

    def add_end_header_bar(self):
        """
        Add custom buttons to the end of the toolbar
        """
        self.replace_action = self.toolbar.add_toolbar_action('replace_action',
                                                              icon=UiIcons().theme,
                                                              triggers=self.on_replace_click)
        self.reset_action = self.toolbar.add_toolbar_action('reset_action',
                                                            icon=UiIcons().close,
                                                            visible=False, triggers=self.on_reset_click)

    def recursively_delete_group(self, image_group):
        """
        Recursively deletes a group and all groups and images in it.

        :param image_group: The ImageGroups instance of the group that will be deleted.
        """
        images = self.manager.get_all_objects(ImageFilenames, ImageFilenames.group_id == image_group.id)
        for image in images:
            delete_file(self.service_path / image.file_path.name)
            delete_file(self.generate_thumbnail_path(image))
            self.manager.delete_object(ImageFilenames, image.id)
        image_groups = self.manager.get_all_objects(ImageGroups, ImageGroups.parent_id == image_group.id)
        for group in image_groups:
            self.recursively_delete_group(group)
            self.manager.delete_object(ImageGroups, group.id)

    def on_delete_click(self):
        """
        Remove an image item from the list.
        """
        # Turn off auto preview triggers.
        self.list_view.blockSignals(True)
        if check_item_selected(self.list_view, translate('ImagePlugin.MediaItem',
                                                         'You must select an image or group to delete.')):
            item_list = self.list_view.selectedItems()
            self.application.set_busy_cursor()
            self.main_window.display_progress_bar(len(item_list))
            for row_item in item_list:
                if row_item:
                    item_data = row_item.data(0, QtCore.Qt.UserRole)
                    if isinstance(item_data, ImageFilenames):
                        delete_file(self.service_path / row_item.text(0))
                        delete_file(self.generate_thumbnail_path(item_data))
                        if item_data.group_id == 0:
                            self.list_view.takeTopLevelItem(self.list_view.indexOfTopLevelItem(row_item))
                        else:
                            row_item.parent().removeChild(row_item)
                        self.manager.delete_object(ImageFilenames, row_item.data(0, QtCore.Qt.UserRole).id)
                    elif isinstance(item_data, ImageGroups):
                        if QtWidgets.QMessageBox.question(
                                self.list_view.parent(),
                                translate('ImagePlugin.MediaItem', 'Remove group'),
                                translate('ImagePlugin.MediaItem',
                                          'Are you sure you want to remove "{name}" and everything in it?'
                                          ).format(name=item_data.group_name)
                        ) == QtWidgets.QMessageBox.Yes:
                            self.recursively_delete_group(item_data)
                            self.manager.delete_object(ImageGroups, row_item.data(0, QtCore.Qt.UserRole).id)
                            if item_data.parent_id == 0:
                                self.list_view.takeTopLevelItem(self.list_view.indexOfTopLevelItem(row_item))
                            else:
                                row_item.parent().removeChild(row_item)
                            self.fill_groups_combobox(self.choose_group_form.group_combobox)
                            self.fill_groups_combobox(self.add_group_form.parent_group_combobox)
                self.main_window.increment_progress_bar()
            self.main_window.finished_progress_bar()
            self.application.set_normal_cursor()
        self.list_view.blockSignals(False)

    def add_sub_groups(self, group_list, parent_group_id):
        """
        Recursively add subgroups to the given parent group in a QTreeWidget.

        :param group_list: The List object that contains all QTreeWidgetItems.
        :param parent_group_id: The ID of the group that will be added recursively.
        """
        image_groups = self.manager.get_all_objects(ImageGroups, ImageGroups.parent_id == parent_group_id)
        image_groups.sort(key=lambda group_object: get_natural_key(group_object.group_name))
        folder_icon = UiIcons().folder
        for image_group in image_groups:
            group = QtWidgets.QTreeWidgetItem()
            group.setText(0, image_group.group_name)
            group.setData(0, QtCore.Qt.UserRole, image_group)
            group.setIcon(0, folder_icon)
            if parent_group_id == 0:
                self.list_view.addTopLevelItem(group)
            else:
                group_list[parent_group_id].addChild(group)
            group_list[image_group.id] = group
            self.add_sub_groups(group_list, image_group.id)

    def fill_groups_combobox(self, combobox, parent_group_id=0, prefix=''):
        """
        Recursively add groups to the combobox in the 'Add group' dialog.

        :param combobox: The QComboBox to add the options to.
        :param parent_group_id: The ID of the group that will be added.
        :param prefix: A string containing the prefix that will be added in front of the groupname for each level of
            the tree.
        """
        if parent_group_id == 0:
            combobox.clear()
            combobox.top_level_group_added = False
        image_groups = self.manager.get_all_objects(ImageGroups, ImageGroups.parent_id == parent_group_id)
        image_groups.sort(key=lambda group_object: get_natural_key(group_object.group_name))
        for image_group in image_groups:
            combobox.addItem(prefix + image_group.group_name, image_group.id)
            self.fill_groups_combobox(combobox, image_group.id, prefix + '   ')

    def expand_group(self, group_id, root_item=None):
        """
        Expand groups in the widget recursively.

        :param group_id: The ID of the group that will be expanded.
        :param root_item: This option is only used for recursion purposes.
        """
        return_value = False
        if root_item is None:
            root_item = self.list_view.invisibleRootItem()
        for i in range(root_item.childCount()):
            child = root_item.child(i)
            if self.expand_group(group_id, child):
                child.setExpanded(True)
                return_value = True
        if isinstance(root_item.data(0, QtCore.Qt.UserRole), ImageGroups):
            if root_item.data(0, QtCore.Qt.UserRole).id == group_id:
                return True
        return return_value

    def generate_thumbnail_path(self, image):
        """
        Generate a path to the thumbnail

        :param openlp.plugins.images.lib.db.ImageFilenames image: The image to generate the thumbnail path for.
        :return: A path to the thumbnail
        :rtype: Path
        """
        ext = image.file_path.suffix.lower()
        return self.service_path / '{name:s}{ext}'.format(name=image.file_hash or image.file_path.stem, ext=ext)

    def load_full_list(self, images, initial_load=False, open_group=None):
        """
        Replace the list of images and groups in the interface.

        :param list[openlp.plugins.images.lib.db.ImageFilenames] images: A List of Image Filenames objects that will be
            used to reload the mediamanager list.
        :param initial_load: When set to False, the busy cursor and progressbar will be shown while loading images.
        :param open_group: ImageGroups object of the group that must be expanded after reloading the list in the
            interface.
        """
        if not initial_load:
            self.application.set_busy_cursor()
            self.main_window.display_progress_bar(len(images))
        self.list_view.clear()
        # Load the list of groups and add them to the treeView.
        group_items = {}
        self.add_sub_groups(group_items, parent_group_id=0)
        if open_group is not None:
            self.expand_group(open_group.id)
        # Sort the images by its filename considering language specific.
        # characters.
        images.sort(key=lambda image_object: get_natural_key(image_object.file_path.name))
        for image in images:
            log.debug('Loading image: {name}'.format(name=image.file_path))
            file_name = image.file_path.name
            thumbnail_path = self.generate_thumbnail_path(image)
            if not image.file_path.exists():
                icon = UiIcons().delete
            else:
                if validate_thumb(image.file_path, thumbnail_path):
                    icon = build_icon(thumbnail_path)
                else:
                    icon = create_thumb(image.file_path, thumbnail_path)
            item_name = QtWidgets.QTreeWidgetItem([file_name])
            item_name.setText(0, file_name)
            item_name.setIcon(0, icon)
            item_name.setToolTip(0, str(image.file_path))
            item_name.setData(0, QtCore.Qt.UserRole, image)
            if image.group_id == 0:
                self.list_view.addTopLevelItem(item_name)
            else:
                group_items[image.group_id].addChild(item_name)
            if not initial_load:
                self.main_window.increment_progress_bar()
        if not initial_load:
            self.main_window.finished_progress_bar()
        self.application.set_normal_cursor()

    def validate_and_load(self, file_paths, target_group=None):
        """
        Process a list for files either from the File Dialog or from Drag and Drop.
        This method is overloaded from MediaManagerItem.

        :param list[Path] file_paths: A List of paths  to be loaded
        :param target_group: The QTreeWidgetItem of the group that will be the parent of the added files
        """
        self.application.set_normal_cursor()
        self.load_list(file_paths, target_group)
        last_dir = file_paths[0].parent
        self.settings.setValue('images/last directory', last_dir)

    def load_list(self, image_paths, target_group=None, initial_load=False):
        """
        Add new images to the database. This method is called when adding images using the Add button or DnD.

        :param list[Path] image_paths: A list of file paths to the images to be loaded
        :param target_group: The QTreeWidgetItem of the group that will be the parent of the added files
        :param initial_load: When set to False, the busy cursor and progressbar will be shown while loading images
        """
        parent_group = None
        if target_group is None:
            # Find out if a group must be pre-selected
            preselect_group = None
            selected_items = self.list_view.selectedItems()
            if selected_items:
                selected_item = selected_items[0]
                if isinstance(selected_item.data(0, QtCore.Qt.UserRole), ImageFilenames):
                    selected_item = selected_item.parent()
                if isinstance(selected_item, QtWidgets.QTreeWidgetItem):
                    if isinstance(selected_item.data(0, QtCore.Qt.UserRole), ImageGroups):
                        preselect_group = selected_item.data(0, QtCore.Qt.UserRole).id
            # Enable and disable parts of the 'choose group' form
            if self.manager.get_object_count(ImageGroups) == 0:
                self.choose_group_form.existing_radio_button.setDisabled(True)
                self.choose_group_form.group_combobox.setDisabled(True)
            else:
                self.choose_group_form.existing_radio_button.setDisabled(False)
                self.choose_group_form.group_combobox.setDisabled(False)
            # Ask which group the image_paths should be saved in
            if self.choose_group_form.exec(selected_group=preselect_group):
                if self.choose_group_form.nogroup_radio_button.isChecked():
                    # User chose 'No group'
                    parent_group = ImageGroups()
                    parent_group.id = 0
                elif self.choose_group_form.existing_radio_button.isChecked():
                    # User chose 'Existing group'
                    group_id = self.choose_group_form.group_combobox.itemData(
                        self.choose_group_form.group_combobox.currentIndex(), QtCore.Qt.UserRole)
                    parent_group = self.manager.get_object_filtered(ImageGroups, ImageGroups.id == group_id)
                elif self.choose_group_form.new_radio_button.isChecked():
                    # User chose 'New group'
                    parent_group = ImageGroups()
                    parent_group.parent_id = 0
                    parent_group.group_name = self.choose_group_form.new_group_edit.text()
                    self.manager.save_object(parent_group)
                    self.fill_groups_combobox(self.choose_group_form.group_combobox)
                    self.fill_groups_combobox(self.add_group_form.parent_group_combobox)
        else:
            parent_group = target_group.data(0, QtCore.Qt.UserRole)
            if isinstance(parent_group, ImageFilenames):
                if parent_group.group_id == 0:
                    parent_group = ImageGroups()
                    parent_group.id = 0
                else:
                    parent_group = target_group.parent().data(0, QtCore.Qt.UserRole)
        # If no valid parent group is found, do nothing
        if not isinstance(parent_group, ImageGroups):
            return
        # Initialize busy cursor and progress bar
        self.application.set_busy_cursor()
        self.main_window.display_progress_bar(len(image_paths))
        # Save the new image_paths in the database
        self.save_new_images_list(image_paths, group_id=parent_group.id, reload_list=False)
        self.load_full_list(self.manager.get_all_objects(ImageFilenames, order_by_ref=ImageFilenames.file_path),
                            initial_load=initial_load, open_group=parent_group)
        self.application.set_normal_cursor()

    def save_new_images_list(self, image_paths, group_id=0, reload_list=True):
        """
        Convert a list of image filenames to ImageFilenames objects and save them in the database.

        :param list[Path] image_paths: A List of file paths to image
        :param group_id: The ID of the group to save the images in
        :param reload_list: This boolean is set to True when the list in the interface should be reloaded after saving
            the new images
        """
        for image_path in image_paths:
            if not isinstance(image_path, Path):
                continue
            log.debug('Adding new image: {name}'.format(name=image_path))
            image_file = ImageFilenames()
            image_file.group_id = group_id
            image_file.file_path = image_path
            image_file.file_hash = sha256_file_hash(image_path)
            self.manager.save_object(image_file)
            self.main_window.increment_progress_bar()
        if reload_list and image_paths:
            self.load_full_list(self.manager.get_all_objects(ImageFilenames, order_by_ref=ImageFilenames.file_path))

    def dnd_move_internal(self, target):
        """
        Handle drag-and-drop moving of images within the media manager

        :param target: This contains the QTreeWidget that is the target of the DnD action
        """
        items_to_move = self.list_view.selectedItems()
        # Determine group to move images to
        target_group = target
        if target_group is not None and isinstance(target_group.data(0, QtCore.Qt.UserRole), ImageFilenames):
            target_group = target.parent()
        # Move to toplevel
        if target_group is None:
            target_group = self.list_view.invisibleRootItem()
            target_group.setData(0, QtCore.Qt.UserRole, ImageGroups())
            target_group.data(0, QtCore.Qt.UserRole).id = 0
        # Move images in the treeview
        items_to_save = []
        for item in items_to_move:
            if isinstance(item.data(0, QtCore.Qt.UserRole), ImageFilenames):
                if isinstance(item.parent(), QtWidgets.QTreeWidgetItem):
                    item.parent().removeChild(item)
                else:
                    self.list_view.invisibleRootItem().removeChild(item)
                target_group.addChild(item)
                item.setSelected(True)
                item_data = item.data(0, QtCore.Qt.UserRole)
                item_data.group_id = target_group.data(0, QtCore.Qt.UserRole).id
                items_to_save.append(item_data)
        target_group.setExpanded(True)
        # Update the group ID's of the images in the database
        self.manager.save_objects(items_to_save)
        # Sort the target group
        group_items = []
        image_items = []
        for item in target_group.takeChildren():
            if isinstance(item.data(0, QtCore.Qt.UserRole), ImageGroups):
                group_items.append(item)
            if isinstance(item.data(0, QtCore.Qt.UserRole), ImageFilenames):
                image_items.append(item)
        group_items.sort(key=lambda item: get_natural_key(item.text(0)))
        target_group.addChildren(group_items)
        image_items.sort(key=lambda item: get_natural_key(item.text(0)))
        target_group.addChildren(image_items)

    def generate_slide_data(self, service_item, *, item=None, remote=False, context=ServiceItemContext.Service,
                            **kwargs):
        """
        Generate the slide data. Needs to be implemented by the plugin.

        :param service_item: The service item to be built on
        :param item: The Song item to be used
        :param remote: Triggered from remote
        :param context: Why is it being generated
        :param kwargs: Consume other unused args specified by the base implementation, but not use by this one.
        """
        if item:
            items = [item]
        else:
            items = self.list_view.selectedItems()
            if not items:
                return False
        # Determine service item title
        if isinstance(items[0].data(0, QtCore.Qt.UserRole), ImageGroups) or len(items) == 1:
            service_item.title = items[0].text(0)
        else:
            service_item.title = str(self.plugin.name_strings['plural'])

        service_item.add_capability(ItemCapabilities.CanMaintain)
        service_item.add_capability(ItemCapabilities.CanPreview)
        service_item.add_capability(ItemCapabilities.CanLoop)
        service_item.add_capability(ItemCapabilities.CanAppend)
        service_item.add_capability(ItemCapabilities.CanEditTitle)
        service_item.add_capability(ItemCapabilities.HasThumbnails)
        service_item.add_capability(ItemCapabilities.ProvidesOwnTheme)
        if self.settings.value('images/background mode') == ImageThemeMode.CustomTheme:
            service_item.theme = self.settings.value('images/theme')
        else:
            # force a nonexistent theme
            service_item.theme = -1
        missing_items_file_names = []
        images = []
        existing_images = []
        # Expand groups to images
        for bitem in items:
            if isinstance(bitem.data(0, QtCore.Qt.UserRole), ImageGroups) or bitem.data(0, QtCore.Qt.UserRole) is None:
                for index in range(0, bitem.childCount()):
                    if isinstance(bitem.child(index).data(0, QtCore.Qt.UserRole), ImageFilenames):
                        images.append(bitem.child(index).data(0, QtCore.Qt.UserRole))
            elif isinstance(bitem.data(0, QtCore.Qt.UserRole), ImageFilenames):
                images.append(bitem.data(0, QtCore.Qt.UserRole))
        # Don't try to display empty groups
        if not images:
            return False
        # Find missing files
        for image in images:
            if not image.file_path.exists():
                missing_items_file_names.append(str(image.file_path))
            else:
                existing_images.append(image)
        # We cannot continue, as all images do not exist.
        if not existing_images:
            if not remote:
                critical_error_message_box(
                    translate('ImagePlugin.MediaItem', 'Missing Image(s)'),
                    translate('ImagePlugin.MediaItem', 'The following image(s) no longer exist: {names}'
                              ).format(names='\n'.join(missing_items_file_names)))
            return False
        # We have missing as well as existing images. We ask what to do.
        elif missing_items_file_names and QtWidgets.QMessageBox.question(
                self, translate('ImagePlugin.MediaItem', 'Missing Image(s)'),
                translate('ImagePlugin.MediaItem', 'The following image(s) no longer exist: {names}\n'
                          'Do you want to add the other images anyway?'
                          ).format(names='\n'.join(missing_items_file_names))) == \
                QtWidgets.QMessageBox.No:
            return False
        # Continue with the existing images.
        for image in existing_images:
            name = image.file_path.name
            thumbnail_path = self.generate_thumbnail_path(image)
            service_item.add_from_image(image.file_path, name, thumbnail_path)
        return True

    def check_group_exists(self, new_group):
        """
        Returns *True* if the given Group already exists in the database, otherwise *False*.

        :param new_group: The ImageGroups object that contains the name of the group that will be checked
        """
        groups = self.manager.get_all_objects(ImageGroups, ImageGroups.group_name == new_group.group_name)
        if groups:
            return True
        else:
            return False

    def on_add_group_click(self):
        """
        Called to add a new group
        """
        # Find out if a group must be pre-selected
        preselect_group = 0
        selected_items = self.list_view.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            if isinstance(selected_item.data(0, QtCore.Qt.UserRole), ImageFilenames):
                selected_item = selected_item.parent()
            if isinstance(selected_item, QtWidgets.QTreeWidgetItem):
                if isinstance(selected_item.data(0, QtCore.Qt.UserRole), ImageGroups):
                    preselect_group = selected_item.data(0, QtCore.Qt.UserRole).id
        # Show 'add group' dialog
        if self.add_group_form.exec(show_top_level_group=True, selected_group=preselect_group):
            new_group = ImageGroups.populate(parent_id=self.add_group_form.parent_group_combobox.itemData(
                self.add_group_form.parent_group_combobox.currentIndex(), QtCore.Qt.UserRole),
                group_name=self.add_group_form.name_edit.text())
            if not self.check_group_exists(new_group):
                if self.manager.save_object(new_group):
                    self.load_full_list(self.manager.get_all_objects(
                        ImageFilenames, order_by_ref=ImageFilenames.file_path))
                    self.expand_group(new_group.id)
                    self.fill_groups_combobox(self.choose_group_form.group_combobox)
                    self.fill_groups_combobox(self.add_group_form.parent_group_combobox)
                else:
                    critical_error_message_box(
                        message=translate('ImagePlugin.AddGroupForm', 'Could not add the new group.'))
            else:
                critical_error_message_box(message=translate('ImagePlugin.AddGroupForm', 'This group already exists.'))

    def on_reset_click(self):
        """
        Called to reset the Live background with the image selected.
        """
        self.reset_action.setVisible(False)
        self.reset_action_context.setVisible(False)
        self.live_controller.reload_theme()

    def on_display_changed(self, service_item=None):
        """
        Triggered by the change of theme in the slide controller.
        """
        self.reset_action.setVisible(False)
        self.reset_action_context.setVisible(False)

    def on_replace_click(self):
        """
        Called to replace Live background with the image selected.
        """
        if check_item_selected(
                self.list_view,
                translate('ImagePlugin.MediaItem', 'You must select an image to replace the background with.')):
            bitem = self.list_view.selectedItems()[0]
            if not isinstance(bitem.data(0, QtCore.Qt.UserRole), ImageFilenames):
                # Only continue when an image is selected.
                return
            file_path = bitem.data(0, QtCore.Qt.UserRole).file_path
            if file_path.exists():
                self.live_controller.set_background_image(file_path)
                self.reset_action.setVisible(True)
                self.reset_action_context.setVisible(True)
            else:
                critical_error_message_box(
                    UiStrings().LiveBGError,
                    translate('ImagePlugin.MediaItem', 'There was a problem replacing your background, '
                              'the image file "{name}" no longer exists.').format(name=file_path))

    def search(self, string, show_error=True):
        """
        Perform a search on the image file names.

        :param str string: The glob to search for
        :param bool show_error: Unused.
        """
        files = self.manager.get_all_objects(
            ImageFilenames, filter_clause=ImageFilenames.file_path.contains(string),
            order_by_ref=ImageFilenames.file_path)
        results = []
        for file_object in files:
            file_name = file_object.file_path.name
            results.append([str(file_object.file_path), file_name])
        return results

    def create_item_from_id(self, item_id):
        """
        Create a media item from an item id. Overridden from the parent method to change the item type.

        :param item_id: Id to make live
        """
        item_id = Path(item_id)
        item = QtWidgets.QTreeWidgetItem()
        item_data = self.manager.get_object_filtered(ImageFilenames, ImageFilenames.file_path == item_id)
        item.setText(0, item_data.file_path.name)
        item.setData(0, QtCore.Qt.UserRole, item_data)
        return item
