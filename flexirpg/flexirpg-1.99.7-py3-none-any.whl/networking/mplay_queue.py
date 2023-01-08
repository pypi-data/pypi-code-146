# FlexiRPG -- message queue that posts events
#
# Copyright (C) 2010 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
from queue import Queue
import wx

QueueEventType = wx.NewEventType()
EVT_QUEUE_READY = wx.PyEventBinder(QueueEventType, 1)

class queue(Queue):
    """Message queue that posts events.

    An EVT_QUEUE_READY event is posted to the specified window when a
    item is put onto the queue.
    """
    def __init__(self, window):
        Queue.__init__(self)
        self.window = window

    def put(self, item, block=True, timeout=None):
        Queue.put(self, item, block, timeout)
        evt = QueueReadyEvent(QueueEventType, -1)
        wx.PostEvent(self.window, evt)

class QueueReadyEvent(wx.PyCommandEvent):
    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self, evtType, id)
