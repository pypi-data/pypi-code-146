# FlexiRPG -- UI for managing the miniature library.
#
# Copyright (C) 2021 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
from collections import namedtuple
import io
import os

import wx

from orpg.config import Paths, Settings
import orpg.lib.ui as ui
from orpg.mapper.image import Image
from orpg.lib.imageid import ImageId
from orpg.main import image_library
from orpg.mapper.miniature_composer import MiniatureComposer
import orpg.tools.bitmap

IMAGE_DEFAULT = 0
IMAGE_STAR = 1

class MiniaturePreview(wx.Panel):
    def __init__(self, parent, size):
        super().__init__(parent, size=size)
        self._bitmap = None

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.Bind(wx.EVT_PAINT, self.on_paint)

    def set_bitmap(self, bitmap):
        self._bitmap = bitmap
        self.Refresh()

    def set_mini(self, mini):
        if mini:
            bitmap = wx.Bitmap(mini.image())
        else:
            bitmap = None
        self.set_bitmap(bitmap)

    def on_paint(self, evt):
        dc = wx.AutoBufferedPaintDC(self)
        dc.SetBackground(wx.Brush(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW), wx.SOLID))
        dc.Clear()

        if self._bitmap:
            x, y = self.GetClientSize()
            mx, my = self._bitmap.Size
            dc.DrawBitmap(self._bitmap, (x - mx) // 2, (y - my) // 2, useMask=True)

class MiniatureManager(wx.Dialog):

    last_directory = Settings.define("map.minilib.last_directory", "")

    def __init__(self, minilib, parent):
        super().__init__(parent, title="Miniatures Library",
                         style=wx.DEFAULT_DIALOG_STYLE)

        self.minilib = minilib
        self.creator = MiniatureCreator(self)

        self.mini_tree = wx.TreeCtrl(self, size=(300, 400), style=wx.TR_HIDE_ROOT)
        self.tree_icons = wx.ImageList(16, 16, False)
        self.tree_icons.Add(orpg.tools.bitmap.create_from_file("tree_default.png"))
        self.tree_icons.Add(orpg.tools.bitmap.create_from_file("tree_star.png"))
        self.mini_tree.SetImageList(self.tree_icons)

        self.root = self.mini_tree.AddRoot("root")

        self.up_btn = ui.BitmapButton(self, "tool_mini_up.png", "Move Miniature Up")
        self.down_btn = ui.BitmapButton(self, "tool_mini_down.png", "Move Miniature Down")
        self.create_btn = ui.BitmapButton(self, "tool_add_mini.png", "Create Miniature")
        self.add_btn = ui.BitmapButton(self, "tool_open.png", "Add from Image File")
        self.del_btn = ui.BitmapButton(self, "tool_mini_del.png", "Delete Miniature")

        self.name_text = wx.TextCtrl(self)
        self.preview = MiniaturePreview(self, (200, 200))
        self.favourite_check = wx.CheckBox(self, label="Favourite")
        self.select_btn = wx.Button(self, id=wx.ID_OK, label="Select")
        self.select_btn.SetDefault()
        self.close_btn = wx.Button(self, id=wx.ID_CANCEL, label="Close")

        self.mini_tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.on_mini_activated)
        self.mini_tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_mini_selection_changed)
        self.up_btn.Bind(wx.EVT_BUTTON, self.on_up)
        self.down_btn.Bind(wx.EVT_BUTTON, self.on_down)
        self.create_btn.Bind(wx.EVT_BUTTON, self.on_create)
        self.add_btn.Bind(wx.EVT_BUTTON, self.on_add)
        self.del_btn.Bind(wx.EVT_BUTTON, self.on_del)
        self.name_text.Bind(wx.EVT_TEXT, self.on_name_text)
        self.favourite_check.Bind(wx.EVT_CHECKBOX, self.on_favourite)

        col_box = wx.BoxSizer(wx.HORIZONTAL)

        # Left column
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(ui.StaticTextHeader(self, label="Miniatures"))
        vbox.Add((0, 6))
        vbox.Add(self.mini_tree, 1, wx.EXPAND | wx.LEFT, border=12)
        vbox.Add((0, 6))
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.up_btn)
        hbox.Add(self.down_btn)
        hbox.Add((6, 0))
        hbox.Add(self.create_btn)
        hbox.Add(self.del_btn)
        hbox.Add((6, 0))
        hbox.Add(self.add_btn)
        vbox.Add(hbox)
        col_box.Add(vbox, 1, wx.EXPAND)

        col_box.Add((18, 0))

        # Right column
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(ui.StaticTextHeader(self, label="Name"))
        vbox.Add((0, 6))
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.name_text, 1, wx.EXPAND | wx.LEFT, border=12)
        vbox.Add(hbox, 0, wx.EXPAND)
        vbox.Add((0, 12))
        vbox.Add(ui.StaticTextHeader(self, label="Preview"))
        vbox.Add((0, 6))
        vbox.Add(self.preview, 0, wx.LEFT, border=12)
        vbox.Add((0, 12))
        vbox.Add(self.favourite_check)
        col_box.Add(vbox, 0, wx.EXPAND)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(col_box, 1, wx.EXPAND)
        vbox.Add((0, 12))

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.select_btn)
        hbox.Add((6,0))
        hbox.Add(self.close_btn)
        vbox.Add(hbox, 0, wx.ALIGN_RIGHT)

        self.box = wx.BoxSizer(wx.HORIZONTAL)
        self.box.Add(vbox, 0, wx.ALL, border=12)

        self.SetSizerAndFit(self.box)

    def select(self):
        self._update_tree()
        self._update_controls()

        selected_mini = None
        if self.ShowModal() == wx.ID_OK:
            item = self.mini_tree.GetSelection()
            if item.IsOk():
                selected_mini = self.mini_tree.GetItemData(item)
        self.minilib.save()
        return selected_mini

    def on_mini_activated(self, evt):
        self.EndModal(wx.ID_OK)

    def on_mini_selection_changed(self, evt):
        selection = self.mini_tree.GetSelection()
        self._update_controls()

    def on_up(self, evt):
        item = self.mini_tree.GetSelection()
        mini = self.mini_tree.GetItemData(item)
        prev = self.mini_tree.GetPrevSibling(item)
        if prev.IsOk():
            self.minilib.move_before(self.mini_tree.GetItemData(prev), mini)
            self.mini_tree.Delete(item)
            item = self._add(mini, self.mini_tree.GetPrevSibling(prev))
            self.mini_tree.SelectItem(item)

    def on_down(self, evt):
        item = self.mini_tree.GetSelection()
        mini = self.mini_tree.GetItemData(item)
        next = self.mini_tree.GetNextSibling(item)
        if next.IsOk():
            self.minilib.move_after(self.mini_tree.GetItemData(next), mini)
            self.mini_tree.Delete(item)
            item = self._add(mini, next)
            self.mini_tree.SelectItem(item)

    def on_create(self, evt):
        if self.creator.ShowModal() == wx.ID_OK:
            image = self.creator.image()
            mini = self.minilib.add("New", image)
            item = self._add(mini)
            self.mini_tree.SelectItem(item)
            self.name_text.SetFocus()
            self.name_text.SetSelection(-1, -1)

    def on_add(self, evt):
        d = wx.FileDialog(self.GetParent(), "Add Miniatures to Library",
                          self.last_directory.value, "",
                          "Images (*.png;*.jpg;*.jpeg)|*.png;*.jpg;*.jpeg",
                          wx.FD_OPEN | wx.FD_MULTIPLE)
        if d.ShowModal() == wx.ID_OK:
            self.last_directory.value = d.GetDirectory()
            item = None
            for path in d.GetPaths():
                image = image_library.get_from_file(path)
                if image:
                    name = os.path.splitext(os.path.basename(path))[0].replace("_", " ")
                    mini = self.minilib.add(name, image)
                    item = self._add(mini)
            if item:
                self.mini_tree.SelectItem(item)
                self.name_text.SetFocus()

    def on_del(self, evt):
        item = self.mini_tree.GetSelection()
        mini = self.mini_tree.GetItemData(item)
        if mini is not None:
            self.minilib.remove(mini)
            self.mini_tree.Delete(item)

    def on_name_text(self, evt):
        item = self.mini_tree.GetSelection()
        mini = self.mini_tree.GetItemData(item)
        mini.name = self.name_text.Value
        self.mini_tree.SetItemText(item, mini.name)

    def on_favourite(self, evt):
        item = self.mini_tree.GetSelection()
        mini = self.mini_tree.GetItemData(item)
        if mini.favourite != self.favourite_check.IsChecked():
            mini.favourite = self.favourite_check.IsChecked()
            self.mini_tree.SetItemImage(item, IMAGE_STAR if mini.favourite else IMAGE_DEFAULT)

    def _add(self, mini, prev_item=None):
        if prev_item is None:
            item = self.mini_tree.AppendItem(self.root, mini.name)
        elif prev_item:
            item = self.mini_tree.InsertItem(self.root, prev_item, mini.name)
        else:
            item = self.mini_tree.PrependItem(self.root, mini.name)
        self.mini_tree.SetItemImage(item, IMAGE_STAR if mini.favourite else IMAGE_DEFAULT)
        self.mini_tree.SetItemData(item, mini)
        return item

    def _update_tree(self):
        selected_mini = self.Parent.controls.selected_mini()
        self.mini_tree.DeleteChildren(self.root)
        for mini in self.minilib:
            item = self._add(mini)
            if mini == selected_mini:
                self.mini_tree.SelectItem(item)

    def _update_controls(self):
        item = self.mini_tree.GetSelection()
        if item.IsOk():
            mini = self.mini_tree.GetItemData(item)
        else:
            mini = None
        if mini is not None:
            self.up_btn.Enable(self.mini_tree.GetPrevSibling(item).IsOk())
            self.down_btn.Enable(self.mini_tree.GetNextSibling(item).IsOk())
            self.del_btn.Enable(True)
            self.name_text.Enable(True)
            self.name_text.ChangeValue(mini.name)
            self.preview.set_mini(mini)
            self.favourite_check.Enable(True)
            self.favourite_check.Value = mini.favourite
            self.select_btn.Enable(True)
        else:
            self.up_btn.Enable(False)
            self.down_btn.Enable(False)
            self.del_btn.Enable(False)
            self.name_text.ChangeValue("")
            self.name_text.Enable(False)
            self.preview.set_mini(None)
            self.favourite_check.Enable(False)
            self.favourite_check.Value = False
            self.select_btn.Enable(False)


SizeOption = namedtuple("SizeOption", ["x", "y", "hint"])

class MiniatureCreator(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Create Miniature",
                         style=wx.DEFAULT_DIALOG_STYLE)

        self.composer = MiniatureComposer()

        self.sizes = [
            SizeOption(14, 14, "Small"),
            SizeOption(20, 20, "Medium"),
            SizeOption(40, 40, "Large"),
            SizeOption(60, 60, "Huge"),
            SizeOption(80, 80, "Gargantuan"),
            SizeOption(120, 120, "Colossal"),
        ]
        size_choices = [f"{s.x}x{s.y} ({s.hint})" for s in self.sizes]

        self.size_choice = wx.Choice(self, choices=size_choices)
        self.size_choice.SetSelection(1)
        self.edge_color = ui.ColorSelectorButton(self, self.composer.edge_color,
                                                 tooltip="Edge Color")
        self.border_color = ui.ColorSelectorButton(self, self.composer.border_color,
                                                   tooltip="Border Color")
        self.fill_color = ui.ColorSelectorButton(self, self.composer.fill_color,
                                                 tooltip="Fill Color")
        self.text_color = ui.ColorSelectorButton(self, self.composer.text_color,
                                                 tooltip="Text Color")
        self.text_text = wx.TextCtrl(self, value=self.composer.text)

        self.preview = MiniaturePreview(self, (200, 200))
        self.preview.set_bitmap(self.composer.bitmap())

        self.create_btn = wx.Button(self, id=wx.ID_OK, label="Create")
        self.create_btn.SetDefault()
        self.cancel_btn = wx.Button(self, id=wx.ID_CANCEL, label="Cancel")

        self.size_choice.Bind(wx.EVT_CHOICE, self.on_size_choice)
        self.edge_color.Bind(ui.EVT_COLOR_SELECTED, self.on_color)
        self.border_color.Bind(ui.EVT_COLOR_SELECTED, self.on_color)
        self.fill_color.Bind(ui.EVT_COLOR_SELECTED, self.on_color)
        self.text_color.Bind(ui.EVT_COLOR_SELECTED, self.on_color)
        self.text_text.Bind(wx.EVT_TEXT, self.on_text_text)

        col_box = wx.BoxSizer(wx.HORIZONTAL)

        # Left column
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(ui.StaticTextHeader(self, label="Size"))
        vbox.Add((0, 6))
        vbox.Add(self.size_choice, wx.LEFT, border=12)
        vbox.Add((0, 12))
        vbox.Add(ui.StaticTextHeader(self, label="Colors"))
        vbox.Add((0, 6))
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.edge_color)
        hbox.Add(self.border_color)
        hbox.Add(self.fill_color)
        hbox.Add(self.text_color)
        vbox.Add(hbox, 0, wx.LEFT, border=12)
        vbox.Add((0, 12))
        vbox.Add(ui.StaticTextHeader(self, label="Text"))
        vbox.Add((0, 6))
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.text_text, 1, wx.EXPAND)
        vbox.Add(hbox, 0, wx.EXPAND | wx.LEFT, border=12)
        col_box.Add(vbox)

        col_box.Add((18,0))

        # Right colomn
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(ui.StaticTextHeader(self, label="Preview"))
        vbox.Add((0, 6))
        vbox.Add((0, 6))
        vbox.Add(self.preview, 0, wx.LEFT, border=12)
        col_box.Add(vbox, 0, wx.EXPAND)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(col_box, 1, wx.EXPAND)
        vbox.Add((0, 12))

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.create_btn)
        hbox.Add((6,0))
        hbox.Add(self.cancel_btn)
        vbox.Add(hbox, 0, wx.ALIGN_RIGHT)

        self.box = wx.BoxSizer(wx.HORIZONTAL)
        self.box.Add(vbox, 0, wx.ALL, border=12)

        self.SetSizerAndFit(self.box)

    def on_size_choice(self, evt):
        size = self.sizes[self.size_choice.GetSelection()]
        self.composer.size = (size.x, size.y)
        self._update_preview()

    def on_color(self, evt):
        self.composer.edge_color = self.edge_color.color
        self.composer.border_color = self.border_color.color
        self.composer.fill_color = self.fill_color.color
        self.composer.text_color = self.text_color.color
        self._update_preview()

    def on_text_text(self, evt):
        self.composer.text = self.text_text.Value
        self._update_preview()

    def image(self):
        wximage = self.composer.bitmap().ConvertToImage()
        d = io.BytesIO()
        wximage.SaveFile(d, "image/png")
        return image_library.get_from_data(d.getvalue())

    def _update_preview(self):
        self.preview.set_bitmap(self.composer.bitmap())
