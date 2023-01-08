#! /usr/bin/env python

""" Bid for Game create Distribution zip file."""

import wx
import os
import re
import shutil
from zipfile import ZipFile

from bfg_components import VERSION


class DeployPackage(wx.Frame):
    """Application to deploy BfG package in a zip file."""
    APP_NAME = 'bfg'
    HOME = '/home/jeff/projects/bfg/'
    VERSION_HOME = '/home/jeff/Dropbox/Bridge/bfg/versions/'
    ANDREW_DROPBOX = '/home/jeff/Dropbox/Andrew/'
    HANDS_DIRECTORY = '/home/jeff/Dropbox/Bridge/bfg/test_hands/'
    SPECIFICATION_HANDS = ''.join([HANDS_DIRECTORY, 'specification_hands.pbn'])
    XL_BOOK = '/home/jeff/Dropbox/Bridge/bfg/bfg_bidding_tests.xlsx'
    PACKAGES = ['bfg_python', 'deal_display',
                'comment_editor', 'comment_viewer',
                'bfg_components', 'bridgeobjects',
                'batch_tests', 'bfg_wx']

    def __init__(self, *args, **kwargs):
        super(DeployPackage, self).__init__(None, *args, **kwargs)
        self.all_files = []
        self.Title = 'BfG deployment'
        self.panel = MainPanel(self)
        sizer = wx.BoxSizer()
        sizer.Add(self.panel)
        self.SetSizerAndFit(sizer)
        self.Center()
        self.Show()
        self.panel.txt_version.SetValue(VERSION)
        self.version = ''
        self.target_root = ''

    def on_create_click(self, event):
        """Run the deployment."""
        del event
        wait = wx.BusyCursor
        self._copy_side_files()
        txt_version = self.panel.txt_version.GetValue()
        self.version = '_{}'.format(txt_version.replace('.', '_'))
        self.target_root = ''.join([self.VERSION_HOME, self.APP_NAME, self.version])
        if not self._continue_to_deploy(self.target_root):
            self._create_directories()
            self._create_zip_file()

            del wait
            message = 'Creation complete\nzip file: {}'
            dialog = wx.MessageDialog(None, message.format(self.target_root),
                                      self.Title, wx.OK | wx.ICON_INFORMATION)
            dialog.ShowModal()
        self.Destroy()

    def _continue_to_deploy(self, target_root):
        """Return True if new target or OK to overwrite."""
        if os.path.isdir(target_root):
            over_write = self._overwrite_existing_target(target_root)
            if over_write:
                shutil.rmtree(self.target_root)
            return not over_write
        else:
            return False

    def _overwrite_existing_target(self, target_root):
        """Return True if user agrees to overwrite."""
        message = '{} exists. Overwrite'
        dialog = wx.MessageDialog(None, message.format(target_root),
                                  self.Title, wx.YES_NO | wx.ICON_QUESTION)
        value = dialog.ShowModal() == wx.ID_YES
        dialog.Destroy()
        return value

    def _create_directories(self, ):
        """Create the directory tree."""
        self._create_root()

        # create distribution directories
        os.makedirs(os.sep.join([self.target_root, self.APP_NAME, self.version]))

    def _create_root(self):
        """Remove the root directory if it exists. In any case create it."""
        try:
            shutil.rmtree(self.target_root)
        except FileNotFoundError:
            pass
        try:
            os.makedirs(self.target_root)
        except FileExistsError:
            pass

    def _create_zip_file(self):
        """Create a zip file of the version."""
        current_directory = os.getcwd()
        os.chdir("../../bfg/")
        file_list = self._files_to_zip()
        zip_path = ''.join([self.VERSION_HOME, self.APP_NAME, self.version, '.zip'])
        with ZipFile(zip_path, 'w') as zip_file:
            for file_ in file_list:
                zip_file.write(file_)
        os.chdir(current_directory)

    def _files_to_zip(self):
        """Return a list of files to add to the zip file."""
        file_list = []
        for package in self.PACKAGES:
            for (root, subdirectories, files) in os.walk(package):
                for file_ in files:
                    file_list.append(os.sep.join([root, file_]))
        return file_list

    def _copy_side_files(self):
        """Place side files in Andrew's dropbox."""

        file_name = os.path.basename(self.SPECIFICATION_HANDS)
        destination = ''.join([self.ANDREW_DROPBOX, file_name])
        shutil.copyfile(self.SPECIFICATION_HANDS, destination)

        file_name = os.path.basename(self.XL_BOOK)
        destination = ''.join([self.ANDREW_DROPBOX, file_name])
        shutil.copyfile(self.XL_BOOK, destination)

        for base, directories, files in os.walk(self.HANDS_DIRECTORY):
            for file_name in files:
                if 'test_deals_' in file_name and '999' not in file_name and '998' not in file_name:
                    destination = ''.join([self.ANDREW_DROPBOX, file_name])
                    shutil.copyfile(''.join([self.HANDS_DIRECTORY ,file_name]), destination)

        for zip_name in os.listdir(self.ANDREW_DROPBOX):
            if re.search(r'[\w]*Win.zip', zip_name):
                os.remove(''.join([self.ANDREW_DROPBOX, zip_name]))

    def on_cancel_click(self, event):
        """Tear down the application."""
        del event
        self.Destroy()


class MainPanel(wx.Panel):
    """Create the panel for the Main Frame."""

    def __init__(self, parent):
        """Initialise the class."""
        wx.Panel.__init__(self, parent)

        sizer = wx.GridBagSizer()

        lbl_version = wx.StaticText(self, label='Version:')
        self.txt_version = wx.TextCtrl(self, size=(150, 30))

        cmd_create = wx.Button(self, id=wx.ID_OK)
        cmd_create.Bind(wx.EVT_BUTTON, parent.on_create_click)
        cmd_create.SetFocus()

        cmd_cancel = wx.Button(self, id=wx.ID_CANCEL)
        cmd_cancel.Bind(wx.EVT_BUTTON, parent.on_cancel_click)

        sizer.Add(lbl_version, pos=(1, 0), flag=wx.LEFT | wx.TOP, border=10)
        sizer.Add(self.txt_version, pos=(1, 1), span=(1, 2),
                  flag=wx.ALL, border=10)
        sizer.Add(cmd_create, pos=(2, 0), span=(1, 2), flag=wx.LEFT, border=10)
        sizer.Add(cmd_cancel, pos=(2, 2),
                  flag=wx.RIGHT | wx.BOTTOM | wx.ALIGN_RIGHT, border=10)
        self.SetSizer(sizer)


class Deploy(wx.Frame):
    """Run the application."""

    def __init__(self, *args, **kwargs):
        app = wx.App()
        super(Deploy, self).__init__(*args, **kwargs)
        DeployPackage()
        app.MainLoop()
