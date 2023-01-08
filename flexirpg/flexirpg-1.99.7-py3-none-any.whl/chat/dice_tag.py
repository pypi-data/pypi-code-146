import wx.html

class dice_tag_handler(wx.html.HtmlWinTagHandler):
    """
    Parse DICE HTML tags, turning them into "dice:..." links.
    """

    def __init__(self):
        wx.html.HtmlWinTagHandler.__init__(self)

    def GetSupportedTags(self):
        return "DICE"

    def HandleTag(self, tag):
        p = self.GetParser()

        old_link = p.Link
        p.Link = wx.html.HtmlLinkInfo("dice:" + tag.GetParam("RESULT"))
        self.ParseInner(tag)
        p.Link = old_link

        return True

wx.html.HtmlWinParser_AddTagHandler(dice_tag_handler)
