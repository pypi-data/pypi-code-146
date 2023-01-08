# Copyright (C) 2000-2001 The OpenRPG Project
# Copyright (C) 2010-2021 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

from enum import IntEnum, auto
from math import pi
import re

from orpg.config import Settings
import orpg.tools.bitmap
import orpg.lib.ui as ui
from orpg.mapper.whiteboard_line import WhiteboardLine
from orpg.mapper.whiteboard_circle import WhiteboardCircle
from orpg.mapper.whiteboard_text import WhiteboardText
from orpg.mapper.whiteboard_mini import WhiteboardMini
from orpg.mapper.miniature_lib import *
from orpg.mapper.min_dialogs import *
from orpg.networking.roles import *
from .textpropdialog import TextPropDialog

class Tool(IntEnum):
    MODE_SELECT         = auto()
    MODE_FREEFORM       = auto()
    MODE_POLYLINE       = auto()
    MODE_CIRCLE         = auto()
    MODE_CONE           = auto()
    MODE_TEXT           = auto()
    MODE_ADD_MINI       = auto()
    ZOOM_IN             = auto()
    ZOOM_OUT            = auto()
    RESET_VIEW          = auto()
    PEN_COLOR           = auto()
    MINI_SELECTOR       = auto()
    LINE_WIDTH_SELECTOR = auto()
    MAP_SAVE            = auto()
    MAP_OPEN            = auto()

mode_cursors = {
    Tool.MODE_SELECT: wx.CURSOR_ARROW,
    Tool.MODE_FREEFORM: wx.CURSOR_PENCIL,
    Tool.MODE_POLYLINE: wx.CURSOR_PENCIL,
    Tool.MODE_CIRCLE: wx.CURSOR_PENCIL,
    Tool.MODE_CONE: wx.CURSOR_PENCIL,
    Tool.MODE_TEXT: wx.CURSOR_IBEAM,
    Tool.MODE_ADD_MINI: wx.CURSOR_CROSS,
}


class LineWidthIcon:
    def __init__(self, width):
        self._width = width
        self._bitmap = orpg.tools.bitmap.create_from_file(f"tool_line_width_{width}.png")
        self._image = self._bitmap.ConvertToImage()

    @property
    def width(self):
        return self._width

    def image(self):
        return self._image

    def tool_bitmap(self, toolbar):
        return self._bitmap

class LineWidthIcons:
    def __init__(self):
        self._icons = []
        for width in (1, 2, 4, 8):
            self._icons.append(LineWidthIcon(width))

    def __getitem__(self, n):
        return self._icons[n]

    def count(self):
        return len(self._icons)

    def image(self, n):
        return self._icons[n].image()


class MapControls(wx.Panel):
    def __init__(self, parent, id, canvas):
        wx.Panel.__init__(self, parent, id)
        self.parent = parent
        self.frame = parent.frame
        self.canvas = canvas

        self.mode = Tool.MODE_SELECT
        self.drawing = False
        self.selected = None
        self.dragging = None
        self.right_clicked = None

        self.pen_color = wx.Colour(wx.BLACK)

        self.minilib = parent.minilib
        self.mini_manager = parent.mini_manager

        self.build_ctrls()
        self.build_menu()
        self.text_prop_dialog = TextPropDialog(self.frame)

    def build_ctrls(self):
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.sizer.Add((3, 0))

        self.toolbar = ui.ToolBar(self)
        self.toolbar.AddRadioTool(Tool.MODE_SELECT, "Select",
                                  orpg.tools.bitmap.create_from_file("tool_select.png"),
                                  shortHelp="Select objects")
        self.toolbar.AddRadioTool(Tool.MODE_FREEFORM, "Freehand",
                                  orpg.tools.bitmap.create_from_file("tool_freehand.png"),
                                  shortHelp="Draw freehand lines")
        self.toolbar.AddRadioTool(Tool.MODE_POLYLINE, "Polyline",
                                  orpg.tools.bitmap.create_from_file("tool_polyline.png"),
                                  shortHelp="Draw straight lines")
        self.toolbar.AddRadioTool(Tool.MODE_CIRCLE, "Circle",
                                  orpg.tools.bitmap.create_from_file("tool_circle.png"),
                                  shortHelp="Draw circles")
        self.toolbar.AddRadioTool(Tool.MODE_CONE, "Cone",
                                  orpg.tools.bitmap.create_from_file("tool_cone.png"),
                                  shortHelp="Draw cones (circle segments)")
        self.toolbar.AddRadioTool(Tool.MODE_TEXT, "Text",
                                  orpg.tools.bitmap.create_from_file("tool_text.png"),
                                  shortHelp="Add text")
        self.toolbar.AddRadioTool(Tool.MODE_ADD_MINI, "Add Mini",
                                  orpg.tools.bitmap.create_from_file("tool_add_mini.png"),
                                  shortHelp="Add miniatures")
        self.toolbar.ToggleTool(self.mode, True);
        self.toolbar.AddSeparator()

        self.color_icon = orpg.tools.bitmap.ColorIcon("tool_color.png")
        self.toolbar.AddTool(Tool.PEN_COLOR, "Pen color",
                             self.color_icon.bitmap(self.pen_color),
                             shortHelp="Pen color")
        self.toolbar.AddIconSelector(Tool.LINE_WIDTH_SELECTOR, "Line width",
                                     LineWidthIcons(),
                                     shortHelp="Line width")
        self.toolbar.AddIconSelector(Tool.MINI_SELECTOR, "Select miniature",
                                     self.minilib.favourites,
                                     shortHelp="Select miniature")

        self.toolbar.AddTool(Tool.ZOOM_IN, "Zoom in",
                             orpg.tools.bitmap.create_from_file("tool_zoom_in.png"),
                             shortHelp="Zoom in")
        self.toolbar.AddTool(Tool.ZOOM_OUT, "Zoom out",
                             orpg.tools.bitmap.create_from_file("tool_zoom_out.png"),
                             shortHelp="Zoom out")
        self.toolbar.AddTool(Tool.RESET_VIEW, "Reset view",
                             orpg.tools.bitmap.create_from_file("tool_reset_view.png"),
                             shortHelp="Reset view to default")
        self.toolbar.AddTool(Tool.MAP_OPEN, "Open map",
                             orpg.tools.bitmap.create_from_file("tool_open.png"),
                             shortHelp="Open a map")
        self.toolbar.AddTool(Tool.MAP_SAVE, "Save map",
                             orpg.tools.bitmap.create_from_file("tool_save.png"),
                             shortHelp="Save the map")

        self.toolbar.Realize()
        self.sizer.Add(self.toolbar)

        self.SetSizer(self.sizer)

        self.Bind(wx.EVT_TOOL, self.on_mode_change, id=Tool.MODE_SELECT)
        self.Bind(wx.EVT_TOOL, self.on_mode_change, id=Tool.MODE_FREEFORM)
        self.Bind(wx.EVT_TOOL, self.on_mode_change, id=Tool.MODE_POLYLINE)
        self.Bind(wx.EVT_TOOL, self.on_mode_change, id=Tool.MODE_CIRCLE)
        self.Bind(wx.EVT_TOOL, self.on_mode_change, id=Tool.MODE_CONE)
        self.Bind(wx.EVT_TOOL, self.on_mode_change, id=Tool.MODE_TEXT)
        self.Bind(wx.EVT_TOOL, self.on_mode_change, id=Tool.MODE_ADD_MINI)
        self.Bind(wx.EVT_TOOL, self.on_pen_color, id=Tool.PEN_COLOR)
        self.Bind(wx.EVT_TOOL, self.on_line_width, id=Tool.LINE_WIDTH_SELECTOR)
        self.Bind(wx.EVT_TOOL, self.on_mini_selector, id=Tool.MINI_SELECTOR)
        self.Bind(wx.EVT_TOOL, self.canvas.on_zoom_in, id=Tool.ZOOM_IN)
        self.Bind(wx.EVT_TOOL, self.canvas.on_zoom_out, id=Tool.ZOOM_OUT)
        self.Bind(wx.EVT_TOOL, self.canvas.on_reset_view, id=Tool.RESET_VIEW)
        self.Bind(wx.EVT_TOOL, self.parent.on_open, id=Tool.MAP_OPEN)
        self.Bind(wx.EVT_TOOL, self.parent.on_save, id=Tool.MAP_SAVE)

    def build_menu(self):
        # Default menu.
        main_menu = wx.Menu()

        item = wx.MenuItem(main_menu, wx.ID_ANY, "&Load Map", "Load Map")
        self.canvas.Bind(wx.EVT_MENU, self.parent.on_open, item)
        main_menu.Append(item)

        item = wx.MenuItem(main_menu, wx.ID_ANY, "&Save Map", "Save Map")
        self.canvas.Bind(wx.EVT_MENU, self.parent.on_save, item)
        main_menu.Append(item)

        main_menu.AppendSeparator()

        item = wx.MenuItem(main_menu, wx.ID_ANY, "&Properties", "Properties")
        self.canvas.Bind(wx.EVT_MENU, self.canvas.on_prop, item)
        main_menu.Append(item)

        main_menu.AppendSeparator()

        item = wx.MenuItem(main_menu, wx.ID_ANY, "Show &Labels", "Show Miniature Labels",
                           wx.ITEM_CHECK)
        self.canvas.Bind(wx.EVT_MENU, self.on_show_labels, item)
        main_menu.Append(item)
        item.Check(Settings.lookup("map.mini.label.show").value)

        self.main_menu = main_menu

        # Line menu.
        self.line_menu = wx.Menu()
        self.add_z_order_menu_items(self.line_menu)

        item = wx.MenuItem(self.line_menu, wx.ID_ANY, "&Delete")
        self.canvas.Bind(wx.EVT_MENU, self.on_delete, item)
        self.line_menu.Append(item)

        # Text menu.
        self.text_menu = wx.Menu()
        self.add_z_order_menu_items(self.text_menu)

        item = wx.MenuItem(self.text_menu, wx.ID_ANY, "&Properties", "Properties")
        self.canvas.Bind(wx.EVT_MENU, self.on_text_properties, item)
        self.text_menu.Append(item)

        item = wx.MenuItem(self.text_menu, wx.ID_ANY, "&Delete")
        self.canvas.Bind(wx.EVT_MENU, self.on_delete, item)
        self.text_menu.Append(item)

        # Miniature menu.
        self.mini_menu = wx.Menu()
        self.add_z_order_menu_items(self.mini_menu)

        self.add_to_library_item = wx.MenuItem(self.mini_menu, wx.ID_ANY, "&Add to Library")
        self.canvas.Bind(wx.EVT_MENU, self.on_add_to_library, self.add_to_library_item)
        self.mini_menu.Append(self.add_to_library_item)

        item = wx.MenuItem(self.mini_menu, wx.ID_ANY, "&Properties", "Properties")
        self.canvas.Bind(wx.EVT_MENU, self.get_mini_properties, item)
        self.mini_menu.Append(item)

        item = wx.MenuItem(self.mini_menu, wx.ID_ANY, "&Delete")
        self.canvas.Bind(wx.EVT_MENU, self.on_delete, item)
        self.mini_menu.Append(item)

    def add_z_order_menu_items(self, menu):
        item = wx.MenuItem(menu, wx.ID_ANY, "&Raise")
        self.canvas.Bind(wx.EVT_MENU, self.on_raise, item)
        menu.Append(item)
        item = wx.MenuItem(menu, wx.ID_ANY, "&Lower")
        self.canvas.Bind(wx.EVT_MENU, self.on_lower, item)
        menu.Append(item)
        item = wx.MenuItem(menu, wx.ID_ANY, "Raise to &Top")
        self.canvas.Bind(wx.EVT_MENU, self.on_raise_to_top, item)
        menu.Append(item)
        item = wx.MenuItem(menu, wx.ID_ANY, "Lower to &Bottom")
        self.canvas.Bind(wx.EVT_MENU, self.on_lower_to_bottom, item)
        menu.Append(item)
        menu.AppendSeparator()

    def do_line_menu(self):
        self.right_clicked.highlight()
        self.canvas.Refresh()
        self.canvas.PopupMenu(self.line_menu)

    def update_object(self, obj):
        xml_str = "<map><whiteboard>"
        xml_str += obj.toxml('update')
        xml_str += "</whiteboard></map>"
        self.frame.session.send(xml_str)
        self.canvas.Refresh(False)

    def do_text_menu(self):
        self.right_clicked.highlight()
        self.canvas.Refresh()
        self.canvas.PopupMenu(self.text_menu)

    def on_text_properties(self, evt):
        if self.text_prop_dialog.show(self.right_clicked) == wx.ID_OK:
            self.update_object(self.right_clicked)

    def on_add_to_library(self, evt):
        name = re.sub(' [0-9]$', '', self.right_clicked.label)
        self.minilib.add(name, self.right_clicked.image)
        self.minilib.save()

    def get_mini_properties(self, evt):
        dlg = min_edit_dialog(self.frame, self.right_clicked)
        if dlg.ShowModal() == wx.ID_OK:
            self.update_object(self.right_clicked)

    def do_mini_menu(self):
        self.right_clicked.highlight()
        self.add_to_library_item.Enabled = self.right_clicked.image.has_image()
        self.canvas.Refresh()
        self.canvas.PopupMenu(self.mini_menu)

    def on_right_down(self,evt):
        self.right_clicked = None

        pos = self.canvas.get_position_from_event(evt)

        if self.mode == Tool.MODE_POLYLINE:
            self.polyline_last_point(evt)

        self.right_clicked = self.canvas.layers['whiteboard'].find_object_at_position(pos)
        if self.right_clicked:
            if isinstance(self.right_clicked, WhiteboardLine):
                self.do_line_menu()
            elif isinstance(self.right_clicked, WhiteboardCircle):
                self.do_line_menu()
            elif isinstance(self.right_clicked, WhiteboardText):
                self.do_text_menu()
            elif isinstance(self.right_clicked, WhiteboardMini):
                self.do_mini_menu()
        else:
            self.canvas.PopupMenu(self.main_menu)

        if self.right_clicked:
            self.right_clicked.highlight(False)
            self.canvas.Refresh()

    def on_pen_color(self,evt):
        data = wx.ColourData()
        data.SetChooseFull(True)
        dlg = wx.ColourDialog(self.canvas, data)
        if dlg.ShowModal() == wx.ID_OK:
            self.pen_color = wx.Colour(dlg.GetColourData().GetColour())
            self.toolbar.SetToolNormalBitmap(Tool.PEN_COLOR, self.color_icon.bitmap(self.pen_color))
        dlg.Destroy()

    def on_line_width(self, evt):
        self.toolbar.PopupIconSelector(Tool.LINE_WIDTH_SELECTOR)

    def on_mini_selector(self, evt):
        self.toolbar.PopupIconSelector(Tool.MINI_SELECTOR, self.mini_manager)
        self.toolbar.ToggleTool(Tool.MODE_ADD_MINI, True)
        self._set_mode(Tool.MODE_ADD_MINI)

    def on_show_labels(self, evt):
        Settings.lookup("map.mini.label.show").value = evt.IsChecked()
        self.canvas.Refresh()

    def delete_all_objects(self):
        self.un_highlight()
        self.canvas.layers['whiteboard'].del_all_objects()

    def on_delete(self, evt):
        if self.right_clicked == self.selected:
            self.un_highlight()
        self.canvas.layers['whiteboard'].del_object(self.right_clicked)
        self.right_clicked = None

    def on_raise(self, evt):
        self.canvas.layers['whiteboard'].raise_object(self.right_clicked)

    def on_lower(self, evt):
        self.canvas.layers['whiteboard'].lower_object(self.right_clicked)

    def on_raise_to_top(self, evt):
        self.canvas.layers['whiteboard'].raise_object_to_top(self.right_clicked)

    def on_lower_to_bottom(self, evt):
        self.canvas.layers['whiteboard'].lower_object_to_bottom(self.right_clicked)

    def on_mode_change(self, event):
        self._set_mode(event.GetId())

    def on_left_down(self,evt):
        session = self.frame.session
        if session.denied(ROLE_PLAYER):
            self.frame.chat.InfoPost("You must be a player or GM to use this feature.")
            return

        pos = self.canvas.get_position_from_event(evt)
        
        if self.mode == Tool.MODE_SELECT:
            self.try_select(pos)

        elif self.mode == Tool.MODE_FREEFORM:
            self.freeform_start(pos)

        elif self.mode == Tool.MODE_POLYLINE:
            self.polyline_add_point(pos)

        elif self.mode == Tool.MODE_CIRCLE:
            self.circle_start(pos)

        elif self.mode == Tool.MODE_CONE:
            self.cone_start(pos)

        elif self.mode == Tool.MODE_TEXT:
            self.on_text_left_down(pos)

        elif self.mode == Tool.MODE_ADD_MINI:
            mini_tmpl = self.selected_mini()
            if mini_tmpl:
                self.canvas.layers['whiteboard'].add_miniature(mini_tmpl, pos)

    def on_left_dclick(self, evt):
        if self.mode == Tool.MODE_FREEFORM:
            #Freeform mode ignores the double click
            pass
        elif self.mode == Tool.MODE_POLYLINE:
            self.polyline_last_point( evt )
        elif self.mode == Tool.MODE_TEXT:
            pass

    def on_left_up(self,evt):
        session = self.frame.session
        if session.denied(ROLE_PLAYER):
            return

        pos = self.canvas.get_position_from_event(evt)

        if self.mode == Tool.MODE_SELECT:
            if self.dragging:
                self.dragging.snap_to_grid(self.canvas.layers['grid'])
                self.update_object(self.dragging)
                self.dragging = False
        if self.mode == Tool.MODE_FREEFORM:
            self.on_freeform_left_up(evt)
        elif self.mode == Tool.MODE_POLYLINE:
            #Polyline mode relies on the down click
            #not the mouse button release
            pass
        elif self.mode == Tool.MODE_CIRCLE:
            self.circle_complete()
        elif self.mode == Tool.MODE_CONE:
            self.cone_complete()
        elif self.mode == Tool.MODE_TEXT:
            pass
        elif self.mode == Tool.MODE_ADD_MINI:
            pass

    def on_motion(self,evt):
        session = self.frame.session
        if session.denied(ROLE_PLAYER):
            return

        pos = self.canvas.get_position_from_event(evt)

        if self.mode == Tool.MODE_SELECT:
            if evt.LeftIsDown() and self.selected:
                self.dragging = self.selected
                self.dragging.move(pos - self.last_pos)
                self.last_pos = pos
                self.canvas.Refresh()
        elif self.mode == Tool.MODE_FREEFORM:
            if evt.LeftIsDown():
                self.freeform_motion(evt)
        elif self.mode == Tool.MODE_POLYLINE:
            if self.drawing:
                self.polyline_motion( evt )
        elif self.mode == Tool.MODE_CIRCLE:
            if evt.LeftIsDown():
                self.circle_motion(evt)
        elif self.mode == Tool.MODE_CONE:
            if evt.LeftIsDown():
                self.cone_motion(evt)

    def try_select(self, pos):
        hit = self.canvas.layers['whiteboard'].find_object_at_position(pos)
        if hit:
            self.highlight(hit)
        else:
            self.un_highlight()
        self.last_pos = pos

    def highlight(self, obj):
        if self.selected == obj:
            return;
        if self.selected:
            self.selected.highlight(False)
        self.selected = obj
        self.selected.highlight(True)
        self.canvas.Refresh(True)

    def un_highlight(self):
        if self.selected:
            self.selected.highlight(False)
            self.selected = None
            self.canvas.Refresh(True)

    def polyline_add_point(self, pos):
        #if this point doens't end the line
        #add a new point into the line string
        if not self.drawing:
            self.working_obj = self.new_line()
            self.working_obj.add_point(pos.x, pos.y)
            self.working_obj.add_point(pos.x, pos.y)
            self.drawing = True
        else:
            if not self.polyline_end_check(pos):
                self.working_obj.add_point(pos.x, pos.y)
            else: #end of line. Send and reset vars for next line
                self.drawing = False
                self.canvas.layers['whiteboard'].complete_object(self.working_obj)
        self.canvas.Refresh()

    def polyline_last_point(self, evt):
        if not self.drawing:
            return
        self.drawing = False

        self.canvas.layers['whiteboard'].complete_object(self.working_obj)
        self.canvas.Refresh()


    # Check if the last two points are sufficiently close to consider
    # the poly line as ended.
    def polyline_end_check(self, pos):
        tol = 5

        (xa, ya) = self.working_obj.points[-2]
        (xb, yb) = self.working_obj.points[-1]

        if xa - tol <= xb <= xa + tol and ya - tol <= yb <= ya + tol:
            self.working_obj.points.pop()
            return True
        return False

    def polyline_motion(self, evt):
        if self.drawing != True:
            return

        pos = self.canvas.get_position_from_event(evt)

        self.working_obj.points[-1] = pos
        self.canvas.Refresh()

    def freeform_start(self, pos):
        self.working_obj = self.new_line()
        self.working_obj.add_point(pos.x, pos.y)
        self.drawing = True

    def new_line(self):
        width = self.toolbar.GetSelected(Tool.LINE_WIDTH_SELECTOR).width
        return self.canvas.layers['whiteboard'].new_line(self.pen_color, width)

    def freeform_motion(self, evt):
        if not self.drawing:
            return
        pos = self.canvas.get_position_from_event(evt)
        self.working_obj.add_point(pos.x, pos.y)
        self.canvas.Refresh()

    def on_freeform_left_up(self,evt):
        if self.drawing == True:
            self.canvas.layers['whiteboard'].complete_object(self.working_obj)
            self.working_obj = None
            self.drawing = False

    def circle_start(self, pos):
        width = self.toolbar.GetSelected(Tool.LINE_WIDTH_SELECTOR).width
        self.working_obj = self.canvas.layers['whiteboard'].new_circle(self.pen_color, width)
        self.working_obj.centre = pos
        self.working_obj.radius = 0
        self.canvas.Refresh()

    def circle_motion(self, evt):
        pos = self.canvas.get_position_from_event(evt)
        self.working_obj.radius = distance_between(
            self.working_obj.centre.x, self.working_obj.centre.y,
            pos.x, pos.y)
        self.canvas.Refresh()

    def circle_complete(self):
        self.canvas.layers['whiteboard'].complete_object(self.working_obj)
        self.working_obj = None

    def cone_start(self, pos):
        width = self.toolbar.GetSelected(Tool.LINE_WIDTH_SELECTOR).width
        self.working_obj = self.canvas.layers['whiteboard'].new_circle(self.pen_color, width)
        self.working_obj.centre = pos
        self.working_obj.radius = 0
        self.working_obj.arc_angle = pi / 2
        self.canvas.Refresh()

    def cone_motion(self, evt):
        pos = self.canvas.get_position_from_event(evt)
        self.working_obj.radius = distance_between(
            self.working_obj.centre.x, self.working_obj.centre.y,
            pos.x, pos.y)
        self.working_obj.centre_angle = atan2(
            pos.y - self.working_obj.centre.y,
            pos.x - self.working_obj.centre.x)
        self.canvas.Refresh()

    def cone_complete(self):
        self.canvas.layers['whiteboard'].complete_object(self.working_obj)
        self.working_obj = None

    def on_text_left_down(self, pos):
        if self.text_prop_dialog.show() != wx.ID_OK:
            return

        props = self.text_prop_dialog.properties
        if props.text == "":
            return

        self.canvas.layers['whiteboard'].add_text(props.text, pos,
                                                  props.pointsize,
                                                  props.color,
                                                  props.bold,
                                                  props.italic)

    def _set_mode(self, mode):
        self.mode = mode
        if mode != Tool.MODE_SELECT:
            self.un_highlight()

        # Change mouse cursor to reflect mode.
        self.canvas.SetCursor(wx.Cursor(mode_cursors[mode]))

    def selected_mini(self):
        return self.toolbar.GetSelected(Tool.MINI_SELECTOR)
