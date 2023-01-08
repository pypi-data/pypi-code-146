"""Get all images for application and assign them to the user."""
import os
from os import walk
import wx
from bridgeobjects import Board, CALLS


class Images(object):
    """Handle images for BfG applications."""
    IMAGE_DIRECTORY = 'images'
    CARD_IMAGE_DIRECTORY = 'card_images'
    CALL_IMAGE_DIRECTORY = 'call_images'
    APP_IMAGE_DIRECTORY = 'app_images'
    IMAGE_EXTENSION = 'png'

    def __init__(self, locales_directory, loc):
        """Ensure image file exist."""
        image_directory = os.sep.join([locales_directory, loc, self.IMAGE_DIRECTORY])
        self.card_directory = os.sep.join([image_directory, self.CARD_IMAGE_DIRECTORY])
        self.call_directory = os.sep.join([image_directory, self.CALL_IMAGE_DIRECTORY])
        self.app_directory = os.sep.join([image_directory, self.APP_IMAGE_DIRECTORY])
        self._check_image_directory(image_directory)
        self._check_image_directory(self.card_directory)
        self._check_image_directory(self.call_directory)

    def card_images(self):
        """Return the card images dict."""
        card_images = {}
        pack = [card for card in Board.full_pack()]
        for card in pack:
            card_images[card.name] = wx.Image('{}/{}.{}'.format(self.card_directory, card.name, self.IMAGE_EXTENSION))
        return card_images

    def call_images(self):
        """Return the call images dict."""
        call_images = {}
        call_list = [call for call in CALLS]
        call_list.extend(['right', 'wrong', 'hyphen', 'blank', 'question',
                          'NS_non', 'NS_vun', 'EW_non', 'EW_vun',
                          'spade', 'heart', 'diamond', 'club'])
        for call_name in call_list:
            path = '{}/{}.{}'.format(self.call_directory, call_name, self.IMAGE_EXTENSION)
            if os.path.isfile(path):
                call_images[call_name] = wx.Image(path)
        return call_images

    def app_images(self):
        """Return the app images dict."""
        files = []
        for (directory_path, directory_names, file_names) in walk(self.app_directory):
            files.extend(file_names)
            break
        app_images = {}
        for file_name in files:
            if file_name[-1 * len(self.IMAGE_EXTENSION):] == self.IMAGE_EXTENSION:
                file_name = os.path.splitext(file_name)[0]
                app_images[file_name] = wx.Image('{}/{}.{}'.format(self.app_directory, file_name, self.IMAGE_EXTENSION))
        return app_images

    def icon(self, application_id='default'):
        """Return the app icon image."""
        icon = wx.Icon('{}/{}.ico'.format(self.app_directory, application_id))
        return icon

    @staticmethod
    def _check_image_directory(directory):
        """Return True if the directory exists, else quits."""
        if not os.path.isdir(directory):
            message = _('missing_directory') + ' ' + directory
            wx.MessageDialog(None, message, _('missing_image_directory_title'),  wx.OK | wx.ICON_ERROR).ShowModal()
            quit()


class Bitmap(wx.Bitmap):
    """Bitmap class with extra features."""
    def __init__(self, path):
        wx.Bitmap.__init__(self, path)

    def Rescale(self, width, height):
        """Resize the bitmap to given height and width."""
        image = self.ConvertToImage()
        image.Rescale(width, height)
        return image.ConvertToBitmap()

    def Scale(self, scale):
        """Scale the bitmap in proportion to scale."""
        size = self.GetSize()
        width, height = int(size[0] * scale), int(size[1] * scale)
        image = self.ConvertToImage()
        image.Rescale(width, height)
        return image.ConvertToBitmap()
