# Flexible, rule-agnostic, character node.
#
# Copyright (C) 2009-2011 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import wx

from orpg.gametree.nodehandlers.core import *
from orpg.dieroller.parser import dice_roll_parser, parse_all_dice_rolls, \
    dice_roll_error, dice_roll_num, dice_roll_string
from orpg.gametree.icons import *
import orpg.lib.ui as ui
import orpg.lib.xmlutil as xmlutil

class flexinode_handler(node_handler):
    def __init__(self, tree, xml_dom, tree_node):
        super().__init__(tree, xml_dom, tree_node)

        self.expressions = []
        self.action = None
        self.reset = None

        self.load_children()
        self.init_magic_exprs()

    def load_children(self):
        children = self.master_dom.childNodes
        for c in children:
            if c.tagName == "expression":
                expr = flexiexpr(self, c)
                self.add_expression(expr)
            elif c.tagName == "action":
                if not self.action:
                    self.action = flexiaction(self, c)
            elif c.tagName == "reset":
                if not self.reset:
                    self.reset = flexireset(self, c)
            else:
                self.tree.load_xml(c, self.mytree_node);
        if not self.action:
            self.action = flexiaction(self)
        if not self.reset:
            self.reset = flexireset(self)

    def init_magic_exprs(self):
        self.magic_exprs = {}
        self.magic_exprs['__name'] = flexiexpr_magic_name(self)
        self.magic_exprs['__parent_name'] = flexiexpr_magic_parent_name(self)
        self.magic_exprs['__icon'] = flexiexpr_magic_icon(self)
        self.magic_exprs['__enabled'] = flexiexpr_magic_enabled(self)
        self.magic_exprs['__roll'] = flexiexpr_magic_roll(self)
        self.magic_exprs['__reset'] = self.magic_exprs['__roll']

    def refresh(self):
        for expr in self.expressions:
            for var, magic_expr in list(self.magic_exprs.items()):
                if expr.variable == var:
                    try:
                        magic_expr.set_value(expr.eval())
                    except dice_roll_error as e:
                        self.tree.frame.chat.InfoPost("Dice error: " + e.str)

    def add_expression(self, expr):
        self.expressions.append(expr)

    def del_expression(self, expr):
        self.expressions.remove(expr)
        expr.delete()

    def find_expr(self, var):
        if var in self.magic_exprs:
            return self.magic_exprs[var]
        return self.__find_expr(var, self)

    def __find_expr(self, var, requester):
        expr = None
        for e in self.expressions:
            if e.variable == var:
                expr = e
                break;
        if not expr:
            e = None
            c = self.tree.GetFirstChild(self.mytree_node)[0]
            while c.IsOk():
                n = self.tree.GetItemData(c)
                if isinstance(n, flexinode_handler) and n != requester:
                    expr = n.__find_expr(var, self)
                    if expr:
                        break
                c = self.tree.GetNextSibling(c)
            if not expr:
                parent = self.parent()
                if parent and parent != requester:
                    expr = parent.__find_expr(var, self)
        return expr

    def path(self):
        if self.parent() == None:
            return self.name
        return self.parent().path() + " / " + self.name

    def parent(self):
        """Return the parent flexinode or None.
        """
        parent_node = self.tree.GetItemParent(self.mytree_node)
        parent = self.tree.GetItemData(parent_node)
        if isinstance(parent, flexinode_handler):
            return parent
        return None

    def on_use(self):
        text = self.action.formatted()
        if text != "":
            self.tree.frame.chat.ParsePost(text, True, True, self)

    def on_design(self, evt):
        if not self.myeditor:
            self.myeditor = flexinode_frame(self)
        self.myeditor.Show()
        self.myeditor.Raise()

    def on_reset(self):
        try:
            parse_all_dice_rolls(self, self.reset.text)
        except dice_roll_error as e:
            self.tree.frame.chat.InfoPost("Dice error: " + e.str)

    def status_text(self):
        try:
            return parse_all_dice_rolls(self, self.action.text)
        except dice_roll_error as e:
            return f"Dice error: {e.str}"

    def lookup(self, var):
        return self.find_expr(var)

    def format_error(self, err):
        return "action in " + self.path() + ": " + err

class flexiexpr(object):
    """Docs
    """
    def __init__(self, fnode, node=None):
        self.fnode = fnode
        if not node:
            self.expr_node = fnode.tree.xml_doc.createElement("expression")
            self.expr_node.setAttribute("variable", "")
            self.fnode.master_dom.appendChild(self.expr_node)
        else:
            self.expr_node = node
        self.value_node = xmlutil.safe_get_text_node(self.expr_node)
        self.in_eval = False
        self.changed = None

    def __repr__ (self):
        return self.variable + " = " + self.value

    def __get_var(self):
        return self.expr_node.getAttribute("variable")

    def __set_var(self, var):
        self.expr_node.setAttribute("variable", var)

    variable = property(__get_var, __set_var)

    def __get_val(self):
        return self.value_node.data

    def __set_val(self, v):
        old_val = self.value_node.data
        self.value_node.data = v
        if self.changed and v != old_val:
            self.changed()

    value = property(__get_val, __set_val)

    def evaluating(self):
        return self.in_eval

    def eval(self):
        self.in_eval = True
        try:
            return dice_roll_parser(self).parse(self.value)
        finally:
            self.in_eval = False

    def set_value(self, val):
        self.value = val.quoted_string()

    def delete(self):
        self.fnode.master_dom.removeChild(self.expr_node)

    def lookup(self, var):
        return self.fnode.find_expr(var)

    def format_error(self, err):
        return "expression '" + self.variable + "' in " + self.fnode.path() + ": " + err

class flexiaction(object):
    def __init__(self, fnode, action_node = None):
        self.fnode = fnode
        if not action_node:
            action_node = fnode.tree.xml_doc.createElement("action")
            self.fnode.master_dom.appendChild(action_node)
        self.text_node = action_node.firstChild
        if self.text_node == None:
            self.text_node = fnode.tree.xml_doc.createTextNode("")
            self.text_node = action_node.appendChild(self.text_node)

    def __get_text(self):
        return self.text_node.data

    def __set_text(self, text):
        self.text_node.data = text

    text = property(__get_text, __set_text)

    def formatted(self):
        if self.text == "":
            return ""
        if self.text[0] == ":":
            return self.text[1:]
        else:
            return "<b>" + self.fnode.name + ":</b> " + self.text

class flexireset(object):
    def __init__(self, fnode, reset_node = None):
        self.fnode = fnode
        if not reset_node:
            reset_node = fnode.tree.xml_doc.createElement("reset")
            self.fnode.master_dom.appendChild(reset_node)
        self.text_node = reset_node.firstChild
        if self.text_node == None:
            new_node = fnode.tree.xml_doc.createTextNode("")
            self.text_node = reset_node.appendChild(new_node)

    def __get_text(self):
        return self.text_node.data

    def __set_text(self, text):
        self.text_node.data = text

    text = property(__get_text, __set_text)


class flexiexpr_magic_name(object):
    def __init__(self, fnode):
        self.fnode = fnode

    def eval(self):
        return dice_roll_string(self.fnode.name)

    def evaluating(self):
        return False

    def set_value(self, val):
        self.fnode.name = val.bare_string()

class flexiexpr_magic_parent_name(object):
    def __init__(self, fnode):
        self.fnode = fnode

    def eval(self):
        parent = self.fnode.parent()
        if not parent:
            return dice_roll_string('')
        return dice_roll_string(parent.name)

    def evaluating(self):
        return False

    def set_value(self, val):
        parent = self.fnode.parent()
        if not parent:
            return
        parent.name = val.bare_string()

class flexiexpr_magic_icon(object):
    def __init__(self, fnode):
        self.fnode = fnode

    def eval(self):
        return dice_roll_string(self.fnode.tree.icons.name(self.fnode.icon))

    def evaluating(self):
        return False

    def set_value(self, val):
        name = val.bare_string()
        if not name in self.fnode.tree.icons:
            raise dice_roll_error(None, "no such icon '" + name + "'")
        self.fnode.icon = self.fnode.tree.icons[name]

class flexiexpr_magic_enabled(object):
    def __init__(self, fnode):
        self.fnode = fnode

    def eval(self):
        return dice_roll_value(1)

    def evaluating(self):
        return False

    def set_value(self, val):
        if val.value == 0:
            self.fnode.enabled = False
        else:
            self.fnode.enabled = True

class flexiexpr_magic_roll(object):
    def __init__(self, fnode):
        self.fnode = fnode

    def eval(self):
        roll = self.fnode.tree.roll_value
        return dice_roll_num(roll, str(roll))

    def evaluating(self):
        return False

    def set_value(self, val):
        pass

class flexinode_frame(wx.Frame):
    def __init__(self, fnode):
        wx.Frame.__init__(self, fnode.tree, 0, fnode.path())
        self.panel = flexinode_panel(self, fnode)

class flexinode_panel(wx.Panel):
    def __init__(self, parent, fnode):
        wx.Panel.__init__(self, parent)

        self.flexinode = fnode

        self.action_sizer = flexinode_action_sizer(self, fnode)
        self.expr_sizer = flexinode_expr_sizer(self, fnode)

        expr_label = ui.StaticTextHeader(self, label="Expressions")
        action_label = ui.StaticTextHeader(self, label="Action when Used")
        reset_label = ui.StaticTextHeader(self, label="Action when Reset")
        self.icon_btn = ui.IconSelectorButton(self, fnode.tree.icons, fnode.icon)
        self.icon_btn.SetToolTip(wx.ToolTip("Change the icon"))
        self.auto_reset_check = wx.CheckBox(self, label="Auto Reset")
        self.auto_reset_check.SetToolTip(wx.ToolTip("Reset when dice rolls are clicked (deprecated)"))
        self.auto_reset_check.SetValue(self.flexinode.auto_reset)
        self.auto_reset_check.Enable(self.flexinode.auto_reset)
        self.preview_btn = wx.Button(self, label="Preview")

        vbox = wx.BoxSizer(wx.VERTICAL)

        # Expressions
        vbox.Add(expr_label, 0)
        vbox.Add((0, 6))
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add((12, 0))
        hbox.Add(self.expr_sizer, 1, wx.EXPAND)
        vbox.Add(hbox, 0, wx.EXPAND)

        vbox.Add((0, 12))

        # Action
        vbox.Add(action_label, 0)
        vbox.Add((0, 6))
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add((12, 0))
        hbox.Add(self.action_sizer, 1, wx.EXPAND)
        vbox.Add(hbox, 3, wx.EXPAND)

        vbox.Add((0, 12))

        # Reset
        vbox.Add(reset_label, 0)
        vbox.Add((0, 6))
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add((12, 0))
        self.reset_text = wx.TextCtrl(self, 0, self.flexinode.reset.text, style=wx.TE_MULTILINE)
        hbox.Add(self.reset_text, 1, wx.EXPAND)
        vbox.Add(hbox, 1, wx.EXPAND)

        self.reset_text.Bind(wx.EVT_TEXT, self.on_reset_text)

        vbox.Add((0, 12))

        # Buttons
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.icon_btn, 0, wx.ALIGN_CENTER_VERTICAL)
        hbox.Add((12, 0))
        hbox.Add(self.auto_reset_check, 0, wx.ALIGN_CENTER_VERTICAL)
        hbox.AddStretchSpacer(1)
        hbox.Add(self.preview_btn, 0, wx.EXPAND)
        vbox.Add(hbox, 0, wx.EXPAND)

        self.box = wx.BoxSizer(wx.VERTICAL)
        self.box.Add(vbox, 1, wx.EXPAND | wx.ALL, border = 12)
        self.SetSizer(self.box)
        self.adjust_size()

        self.icon_btn.Bind(ui.EVT_ICON_SELECTED, self.on_icon_selected)
        self.auto_reset_check.Bind(wx.EVT_CHECKBOX, self.on_auto_reset_checked)
        self.preview_btn.Bind(wx.EVT_BUTTON, self.on_preview_button)

    def adjust_size(self):
        self.box.Layout()
        self.box.SetSizeHints(self.GetParent())
        self.GetParent().Fit()

    def on_reset_text(self, evt):
        self.flexinode.reset.text = self.reset_text.GetValue()

    def on_icon_selected(self, evt):
        self.flexinode.icon = evt.GetId()
        evt.Skip()

    def on_auto_reset_checked(self, evt):
        self.flexinode.auto_reset = self.auto_reset_check.IsChecked()
        self.auto_reset_check.Enable(self.flexinode.auto_reset)

    def on_preview_button(self, evt):
        self.action_sizer.update_preview()

class flexinode_expr_sizer(wx.BoxSizer):
    def __init__(self, panel, fnode):
        wx.BoxSizer.__init__(self, wx.VERTICAL)

        self.panel = panel
        self.flexinode = fnode
        self.num_expressions = 0

        self.plus_btn = wx.Button(self.panel, 0, '+', style=wx.BU_EXACTFIT)
        self.plus_btn.SetToolTip(wx.ToolTip("Add new expression"))

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.AddStretchSpacer(1)
        hbox.Add(self.plus_btn, 0)

        self.Add(hbox, 0, wx.EXPAND)
        self.SetMinSize((400, 0))

        self.plus_btn.Bind(wx.EVT_BUTTON, self.on_plus_button)

        for expr in self.flexinode.expressions:
            self.add_expr(expr)

    def add_expr(self, expr):
        expr_box = flexinode_expr_box(self.panel, expr)
        self.Insert(self.num_expressions, expr_box, 0, wx.EXPAND)
        self.num_expressions = self.num_expressions + 1
        expr_box.val_text.MoveBeforeInTabOrder(self.panel.action_sizer.action_text)
        expr_box.var_text.MoveBeforeInTabOrder(expr_box.val_text)
        expr_box.minus_btn.MoveBeforeInTabOrder(self.plus_btn)

    def del_expr(self, expr_box):
        expr_box.Clear(True)
        self.Remove(expr_box)
        self.panel.adjust_size()
        self.num_expressions = self.num_expressions - 1

    def on_plus_button(self, evt):
        expr = flexiexpr(self.flexinode)
        self.flexinode.add_expression(expr)
        self.add_expr(expr)
        self.panel.adjust_size()

class flexinode_expr_box(wx.BoxSizer):
    def __init__(self, window, expr):
        wx.BoxSizer.__init__(self, wx.HORIZONTAL)

        self.window = window
        self.expr = expr

        self.var_text = wx.TextCtrl(window, 0, self.expr.variable)
        self.eq_label = wx.StaticText(window, 0, "=")
        self.val_text = wx.TextCtrl(window, 0, self.expr.value)
        self.minus_btn = wx.Button(window, 0, '\u2212', style=wx.BU_EXACTFIT) # minus
        self.minus_btn.SetToolTip(wx.ToolTip("Remove this expression"))

        self.Add(self.var_text, 1, wx.EXPAND)
        self.Add((6,0))
        self.Add(self.eq_label, 0, wx.ALIGN_CENTRE_VERTICAL)
        self.Add((6,0))
        self.Add(self.val_text, 3, wx.EXPAND)
        self.Add(self.minus_btn, 0, wx.EXPAND)

        self.minus_btn.Bind(wx.EVT_BUTTON, self.on_minus_button)
        self.var_text.Bind(wx.EVT_TEXT, self.on_variable_text)
        self.val_text.Bind(wx.EVT_TEXT, self.on_value_text)

        self.expr.changed = self

    def __call__(self):
        if self.expr.value != self.val_text.GetValue():
            self.val_text.SetValue(self.expr.value)

    def on_minus_button(self, evt):
        self.window.flexinode.del_expression(self.expr)
        self.window.expr_sizer.del_expr(self)

    def on_variable_text(self, evt):
        self.expr.variable = self.var_text.GetValue()

    def on_value_text(self, evt):
        if self.val_text.GetValue() != self.expr.value:
            self.expr.value = self.val_text.GetValue()

class flexinode_action_sizer(wx.BoxSizer):
    def __init__(self, panel, fnode):
        wx.BoxSizer.__init__(self, wx.VERTICAL)

        self.panel = panel
        self.flexinode = fnode

        self.action_text = wx.TextCtrl(panel, 0, self.flexinode.action.text, style=wx.TE_MULTILINE)
        self.preview = wx.html.HtmlWindow(panel)

        self.Add(self.action_text, 1, wx.EXPAND)
        self.Add((0,6))
        self.Add(self.preview, 1, wx.EXPAND)
        self.SetMinSize((0, 200))

        self.action_text.Bind(wx.EVT_TEXT, self.on_action_text)

    def update_preview(self):
        try:
            text = parse_all_dice_rolls(self.flexinode, self.flexinode.action.formatted())
        except dice_roll_error as e:
            text = "<i>Dice error: " + e.str + "</i>"
        self.preview.SetPage(text)

    def on_action_text(self, evt):
        self.flexinode.action.text = self.action_text.GetValue()
