# FlexiRPG -- stack of z-ordered whiteboard objects.
#
# Copyright (C) 2009-2010 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
from orpg.mapper.base import *
from orpg.mapper.whiteboard_object import WhiteboardObject

class WhiteboardStack(object):
    def __init__(self):
        self.stack = []
        self.top_z = 0

    def append(self, obj):
        self._set(self.top_z, obj)
        self.top_z += 1

    def insert(self, obj, new_z):
        if new_z >= self.top_z:
            self.append(obj)
        else:
            self._shift_up(new_z, self.top_z)
            self._set(new_z, obj)
            self.top_z += 1

    def remove(self, obj):
        self.top_z -= 1
        self._shift_down(obj.z_order, self.top_z)
        del self.stack[self.top_z]
        obj.destroy()

    def move(self, obj, new_z):
        if obj.z_order != new_z:
            self.remove(obj)
            self.insert(obj, new_z)

    def clear(self):
        self.stack.clear()
        self.top_z = 0

    def raise_(self, obj):
        new_z = obj.z_order + 1
        if new_z >= self.top_z:
            return
        self._swap(obj, self.stack[new_z])

    def lower(self, obj):
        new_z = obj.z_order - 1
        if new_z < 0:
            return
        self._swap(obj, self.stack[new_z])

    def raise_to_top(self, obj):
        new_z = self.top_z - 1
        self._shift_down(obj.z_order, new_z)
        self._set(new_z, obj)

    def lower_to_bottom(self, obj):
        new_z = 0
        self._shift_up(new_z, obj.z_order)
        self._set(new_z, obj)

    def _set(self, z, obj):
        if z == self.top_z:
            self.stack.append(obj)
        else:
            self.stack[z] = obj
        obj.z_order = z

    def _shift_up(self, begin, end):
        for i in range(end, begin, -1):
            self._set(i, self.stack[i-1])

    def _shift_down(self, begin, end):
        for i in range(begin, end):
            self._set(i, self.stack[i+1])

    def _swap(self, a, b):
        t = a.z_order
        a.z_order = b.z_order
        b.z_order = t
        self.stack[a.z_order] = a;
        self.stack[b.z_order] = b

    def __len__(self):
        return len(self.stack)

    def __iter__(self):
        for obj in self.stack[:]:
            yield obj

    def __reversed__(self):
        for obj in reversed(self.stack[:]):
            yield obj
