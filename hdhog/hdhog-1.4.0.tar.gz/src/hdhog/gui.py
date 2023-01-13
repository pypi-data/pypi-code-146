import os
from tkinter import Tk, Button, Entry, Label
from tkinter.ttk import Treeview, Notebook, Frame, Scrollbar
from tkinter import RIGHT, LEFT, TOP, BOTTOM, END
from tkinter import W
from tkinter import filedialog, messagebox
from math import log

from .catalogue import Catalogue
from .container import DirItem
from .tree import Tree
from .logger import logger

item_colors = {"file": "#fcfade", "dir": "#D7F4F3"}  # Cornsilk, Water


def humanReadableSize(size: int) -> str:
    """Takes a size in bytes and returns a string with size suffix.

    Takes a size in bytes (as returned from the OS FS functions) and
    turns it into a size string in the manner of Unix' ls -lh.

    Args:
        size (int): size in bytes

    Returns:
        str: size string in human readable form
    """
    size_suffixes = ["K", "M", "G", "T"]

    if size <= 0:
        return "0"

    logger.debug(f"Calculating h.r. size for bytes: {size}.")

    loga = int(log(size, 1000))

    if loga == 0:
        return f"{size}"
    else:
        amount_suffix_x = size // (1000 ** loga)

        if len(str(amount_suffix_x)) > 1:
            hr_size = f"{amount_suffix_x}{size_suffixes[loga - 1]}"
            logger.debug(f"Human readable size is {hr_size}")
            return hr_size
        else:
            size_point = size / (1000 ** loga)
            hr_size = f"{size_point:.1f}{size_suffixes[loga - 1]}"
            logger.debug(f"Human readable size is {hr_size}")
            return hr_size


class GUITree(Tree, Treeview):
    def __init__(
        self, parent_widget, columns, xscrollcommand, yscrollcommand,
    ):
        Treeview.__init__(
            self,
            parent_widget,
            columns=columns,
            show="tree headings",
            selectmode="extended",
            xscrollcommand=xscrollcommand,
            yscrollcommand=yscrollcommand,
        )
        self.tag_configure("file", background=item_colors["file"])
        self.tag_configure("dir", background=item_colors["dir"])

    def deleteSubtree(self, item):
        self.delete(item.iid)

    def updateAncestors(self, item):
        parent_iid = self.parent(item.iid)
        parent_item = item.parent
        while parent_iid:
            new_hr_size = humanReadableSize(parent_item.size)
            self.item(parent_iid, values=(new_hr_size,))
            parent_iid = self.parent(parent_iid)
            parent_item = item.parent

    def insertDirItem(self, dir_item: DirItem):
        dir_iid = dir_item.iid
        dir_name = dir_item.name
        dir_size = humanReadableSize(dir_item.size)

        if not self.exists(dir_iid):
            self.insert(
                "", 0, iid=dir_iid, text=dir_name, values=(dir_size,), tags=["dir"]
            )

        # insert sorted dirs, then sorted files

        for child in dir_item.dirs:
            c_iid = child.iid
            c_name = child.name
            c_size = humanReadableSize(child.size)
            self.move(c_iid, dir_iid, "end")

        for child in dir_item.files:
            c_iid = child.iid
            c_name = child.name
            c_size = humanReadableSize(child.size)
            self.insert(
                dir_iid, END, iid=c_iid, text=c_name, values=(c_size,), tags=["file"]
            )

    def getRootIID(self) -> str:
        ch = self.get_children()
        if ch:
            return ch[0]
        else:
            return ""


class GUI:
    def __init__(self):

        """ ### Data models ### """
        self.catalogue = Catalogue()

        """ ### GUI elements ### """

        self.root = Tk()
        self.root.title("Big File Finder - Find biggest files and delete or move them.")

        """ initial position and size """
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        w = int(sw * 0.66)
        h = int(sh * 0.66)
        x = (sw // 2) - (w // 2)
        y = (sh // 2) - (h // 2)

        self.root.geometry(f"{w}x{h}+{x}+{y}")

        """ ### create right side ### """

        right_frame_w = w // 4

        self.frame_right = Frame(self.root, borderwidth=10, width=right_frame_w)
        self.frame_right.pack(side=RIGHT, fill="both")
        self.frame_right.pack_propagate(0)

        # self.frame_counter = Frame(self.frame_right, borderwidth=30, height=200)
        # self.frame_counter.pack(side=BOTTOM)
        # self.lbl_counter = Label(self.frame_counter, text="Total count")
        # self.lbl_counter.pack(side=TOP)

        self.lbl_choose_info = Label(
            self.frame_right, text="Start folder:", width=50, anchor=W
        )
        self.lbl_choose_info.pack(side=TOP, pady=(30, 0))

        """ Folder entry """

        self.startdir_entry = Entry(self.frame_right, width=50, bd=5)
        self.startdir_entry.pack(side=TOP)

        """ Browse for directory button"""

        self.button_choose_folder = Button(
            self.frame_right,
            text="Choose folder...",
            width=50,
            command=self.btnChooseFolder,
        )
        self.button_choose_folder.pack(side=TOP, pady=15)

        """ Button walk and list directory in folder entry """
        self.button_list = Button(
            self.frame_right, text="List", width=50, command=self.bntList,
        )
        self.button_list.pack(side=TOP)

        """ Total count info """

        frame_counter = Frame(
            self.frame_right, borderwidth=2, height=200, relief="groove"
        )
        frame_counter.pack(side=TOP, pady=30)

        self.lbl_count_title = Label(frame_counter, text="Total numbers")
        self.lbl_count_title.pack(side=TOP, pady=(10, 20))

        padding_2_frame = 10

        frame_usedspace = Frame(frame_counter)
        frame_usedspace.pack(side=BOTTOM, anchor=W, padx=padding_2_frame)
        frame_fcount = Frame(frame_counter)
        frame_fcount.pack(side=BOTTOM, anchor=W, padx=padding_2_frame)
        frame_dcount = Frame(frame_counter)
        frame_dcount.pack(side=BOTTOM, anchor=W, padx=padding_2_frame)

        self.lbl_usedspace = Label(frame_usedspace, text="0", font="Arial 9 bold")
        self.lbl_usedspace.pack(side=RIGHT, pady=5, padx=(5, 5))
        txt_dirs = Label(frame_usedspace, text="Used space:", width=10)
        txt_dirs.pack(side=LEFT, pady=5)

        self.lbl_dir_counter = Label(frame_dcount, text="0", font="Arial 9 bold")
        self.lbl_dir_counter.pack(side=RIGHT, pady=5, padx=(5, 5))
        txt_dirs = Label(frame_dcount, text="Folders:", width=10)
        txt_dirs.pack(side=LEFT, pady=5)

        self.lbl_file_counter = Label(frame_fcount, text="0", font="Arial 9 bold")
        self.lbl_file_counter.pack(side=RIGHT, pady=5, padx=(5, 5))
        txt_files = Label(frame_fcount, text="Files:", width=10)
        txt_files.pack(side=LEFT, pady=5)

        """ button delete selection """

        self.button_delete_selected = Button(
            self.frame_right,
            text="Delete Selected",
            width=50,
            command=self.btnDeleteSelected,
        )
        self.button_delete_selected.pack(side=TOP, pady=20)

        """ quit button """

        self.button_quit = Button(
            self.frame_right, text="Quit", width=50, command=self.__del__
        )
        self.button_quit.pack(side=BOTTOM)

        """ ### create left side ### """

        left_frame_w = w - right_frame_w

        self.frame_left = Frame(
            self.root, borderwidth=10, height=360, width=left_frame_w
        )
        self.frame_left.pack(side=LEFT, expand=1, fill="both")
        self.frame_left.pack_propagate(0)

        """ create tabs """

        self.tabs = Notebook(self.frame_left)
        tab_files = Frame(self.tabs)
        tab_dirs = Frame(self.tabs)
        tab_tree = Frame(self.tabs)
        self.tabs.add(tab_files, text="Files")
        self.tabs.add(tab_dirs, text="Folders")
        self.tabs.add(tab_tree, text="Tree View")
        self.tabs.pack(expand=1, fill="both")

        """ create files view """

        columns = ["name", "size", "dir"]

        sb_v = Scrollbar(tab_files, orient="vertical")
        sb_v.pack(side=RIGHT, fill="y")
        sb_h = Scrollbar(tab_files, orient="horizontal")
        sb_h.pack(side=BOTTOM, fill="x")

        self.tv_files = Treeview(
            tab_files,
            columns=columns,
            show="headings",
            selectmode="extended",
            xscrollcommand=sb_h.set,
            yscrollcommand=sb_v.set,
        )

        sb_v.config(command=self.tv_files.yview)
        sb_h.config(command=self.tv_files.xview)

        self.tv_files.column("size", width=80, minwidth=80, stretch=False)
        self.tv_files.column("name", width=200, minwidth=200, stretch=False)
        self.tv_files.column("dir", width=400, stretch=True)

        self.tv_files.heading("name", text="File Name")
        self.tv_files.heading("size", text="File Size")
        self.tv_files.heading("dir", text="Parent Folder")

        self.tv_files.tag_configure("file", background=item_colors["file"])

        self.tv_files.pack(expand=1, fill="both")

        """ create directory view """

        columns = ["name", "size", "dir"]

        sb_v = Scrollbar(tab_dirs, orient="vertical")
        sb_v.pack(side=RIGHT, fill="y")
        sb_h = Scrollbar(tab_dirs, orient="horizontal")
        sb_h.pack(side=BOTTOM, fill="x")

        self.tv_dirs = Treeview(
            tab_dirs,
            columns=columns,
            show="headings",
            selectmode="extended",
            xscrollcommand=sb_h.set,
            yscrollcommand=sb_v.set,
        )

        sb_v.config(command=self.tv_dirs.yview)
        sb_h.config(command=self.tv_dirs.xview)

        self.tv_dirs.column("size", width=80, minwidth=80, stretch=False)
        self.tv_dirs.column("name", width=200, minwidth=200, stretch=False)
        self.tv_dirs.column("dir", width=400, stretch=True)

        self.tv_dirs.heading("name", text="Folder Name")
        self.tv_dirs.heading("size", text="Folder Size")
        self.tv_dirs.heading("dir", text="Parent Folder")

        self.tv_dirs.tag_configure("dir", background=item_colors["dir"])

        self.tv_dirs.pack(expand=1, fill="both")

        """ create tree view """

        sb_v = Scrollbar(tab_tree, orient="vertical")
        sb_v.pack(side=RIGHT, fill="y")
        sb_h = Scrollbar(tab_tree, orient="horizontal")
        sb_h.pack(side=BOTTOM, fill="x")

        self.guitree = GUITree(
            tab_tree,
            columns=["size"],
            xscrollcommand=sb_h.set,
            yscrollcommand=sb_v.set,
        )

        sb_v.config(command=self.guitree.yview)
        sb_h.config(command=self.guitree.xview)

        self.tv_tree = self.guitree
        self.tv_tree.column("size", width=80, minwidth=80, stretch=False)
        self.tv_tree.heading("size", text="Size")
        self.tv_tree.pack(expand=1, fill="both")

        # important
        self.catalogue.registerMirrorTrees([self.guitree])

        """ ### Keybindings ### """

        self.root.bind("<Control-q>", self.ctrlQ)

    def __del__(self):
        self.root.quit()

    def run(self):
        self.root.mainloop()

    def ctrlQ(self, event):
        self.root.quit()

    def btnChooseFolder(self):
        path = filedialog.askdirectory(parent=self.frame_right, mustexist=True)
        self.startdir_entry.delete(0, END)
        self.startdir_entry.insert(0, path)

    def bntList(self):
        startdir = self.startdir_entry.get()
        if not startdir:
            messagebox.showinfo(
                title="Folder field empty", message="Choose a folder to list."
            )
        elif not os.path.isdir(startdir):
            messagebox.showerror(
                title="Invalid Folder", message="Folder does not exist!"
            )
        else:
            gui_root = self.guitree.getRootIID()
            if gui_root:
                self.guitree.delete(gui_root)
            self.catalogue.createCatalogue(start=startdir)
            self.delFiles()
            self.listFiles()
            self.delDirs()
            self.listDirs()

            self._setFileCountTxt()
            self._setDirCountTxt()
            self._setUsedSpace()

    def btnDeleteSelected(self):
        tab = self.tabs.tab(self.tabs.select(), "text")

        if tab == "Files":
            selection = self.tv_files.selection()
            for iid in selection:
                self.tv_files.delete(iid)
        elif tab == "Folders":
            selection = self.tv_dirs.selection()
            for iid in selection:
                self.tv_dirs.delete(iid)
        else:
            selection = self.tv_tree.selection()

        logger.info(f"Deleting selection from tab {tab}.")

        self.catalogue.deleteByIDs(selection)

        # completely deleting an resinserting is for simplicity
        # right now and will be changed
        self.delFiles()
        self.listFiles()
        self.delDirs()
        self.listDirs()

        self._setFileCountTxt()
        self._setDirCountTxt()
        self._setUsedSpace()

    def delFiles(self):
        items = self.tv_files.get_children()
        for iid in items:
            self.tv_files.delete(iid)

    def listFiles(self):
        for item in self.catalogue.files:
            iid = item.iid
            name = item.name
            size = humanReadableSize(item.size)
            parent = item.dirpath
            self.tv_files.insert(
                "", END, iid=iid, values=(name, size, parent), tags=["file"]
            )

    def delDirs(self):
        items = self.tv_dirs.get_children()
        for iid in items:
            self.tv_dirs.delete(iid)

    def listDirs(self):
        for item in self.catalogue.dirs:
            iid = item.iid
            name = item.name
            size = humanReadableSize(item.size)
            parent = item.dirpath
            self.tv_dirs.insert(
                "", END, iid=iid, values=(name, size, parent), tags=["dir"]
            )

    def _setFileCountTxt(self):
        self.lbl_file_counter.config(text=str(self.catalogue.num_files))

    def _setDirCountTxt(self):
        self.lbl_dir_counter.config(text=str(self.catalogue.num_dirs))

    def _setUsedSpace(self):
        hr_total_size = humanReadableSize(self.catalogue.total_space)
        self.lbl_usedspace.config(text=hr_total_size)
