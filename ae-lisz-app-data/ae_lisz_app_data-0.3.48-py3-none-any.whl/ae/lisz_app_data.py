"""
lisz demo app data handling
===========================

this module provides common constants, functions and methods for the showcase/demo application `Lisz`, which is
demonstrating the usage of the GUI framework packages provided by the `ae namespace <https://ae.readthedocs.io>`__.


usage demonstration of ae namespace portions
--------------------------------------------

the usage of the following ae namespace portions get demonstrated by this application:

* :mod:`ae.base`: basic constants and helper functions
* :mod:`ae.files`: file collection, grouping and caching
* :mod:`ae.deep`: deep data structure search and replace
* :mod:`ae.i18n`: internationalization / localization helpers
* :mod:`ae.paths`: generic file path helpers
* :mod:`ae.dynamicod`: evaluation and execution helper functions
* :mod:`ae.updater`: application environment updater
* :mod:`ae.core`: application core constants, helper functions and base classes
* :mod:`ae.literal`: literal type detection and evaluation
* :mod:`ae.console`: console application environment
* :mod:`ae.parse_date`: parse date strings more flexible and less strict
* :mod:`ae.gui_app`: base class for python applications with a graphical user interface
* :mod:`ae.gui_help`: main app base class with context help for flow and app state changes


.. hint::
    the Kivy variant of this demo app uses additionally the following ae namespace portions: :mod:`ae.kivy_auto_width`,
    :mod:`ae.kivy_dyn_chi`, :mod:`ae.kivy_help`, :mod:`ae.kivy_relief_canvas`, :mod:`ae.kivy_app` and
    :mod:`ae.kivy_user_prefs`.


features of the lisz demo app
-----------------------------

* internationalization of texts, user messages, help texts, button/label texts (:mod:`ae.i18n`)
* easy mapping of files in complex folder structures (:mod:`ae.files`, :mod:`ae.paths`)
* providing help screens (:mod:`ae.gui_help`, :mod:`ae.kivy_help`)
* colors changeable by user (:mod:`ae.kivy_user_prefs`, :mod:`ae.enaml_app`)
* font and button sizes are changeable by user (:mod:`ae.gui_app`)
* dark and light theme switchable by user
* sound output support with sound volume configurable by user
* recursive item data tree manipulation: add, edit and delete item
* each item can be selected/check marked
* filtering of selected/checked and unselected/unchecked items
* an item represents either a sub-node (sub-list) or a leaf of the data tree
* item order changeable via drag & drop
* item can be moved to the parent or a sub-node
* easy navigation within the item tree (up/down navigation in tree and quick jump)


lisz application data model
---------------------------

fhe lisz demo app is managing a recursive item tree - a list of lists - that can be used e.g. as to-do or shopping list.

to keep this demo app simple, the data managed by the lisz application is a minimalistic tree structure that gets stored
as an :ref:`application status`, without the need of any database. the root node and with that the whole recursive data
structure gets stored in the app state variable `root_node`.

the root of the tree structure is a list of the type `LiszNode` containing list items of type `LiszItem`. a `LiszItem`
element represents a dict of the type `Dict[str, Any]`.

each `LiszItem` element of the tree structure is either a leaf or a node. and each node is a sub-list with a recursive
structure identical to the root node and of the type `LiszNode`.

the following graph is showing an example data tree:

.. graphviz::

    digraph {
        node [shape=record, width=3]
        rec1 [label="{<rec1>Root Node | { <A>Item A | <C>Item C | <D>... } }"]
        "root_node app state variable" -> rec1 [arrowhead=crow style=tapered penwidth=3]
        rec1:A -> "Leaf Item A" [minlen=3]
        rec2 [label="{<rec2>Node Item C (sub-node) | { <CA>Item CA | <CB>Item CB | <CN>... } }"]
        rec1:C -> rec2
        rec2:CA -> "Leaf Item CA" [minlen=2]
        rec3 [label="{<rec3>Node Item CB (sub-sub-node) | { <CBA>Item CBA | <CDn>... } }"]
        rec2:CB -> rec3
        rec3:CBA -> "Leaf Item CBA"
    }

the above example tree structure is containing the root node items `A` (which is a leaf) and `C` (which is a sub-node).

the node `C` consists of the items `CA` and `CB` where `CA` is a leaf and `CB` is a node.

the first item of the node `CB` is another sub-node with the leaf item `CBA`.


GUI framework demo implementations
==================================

the plan is to integrate the following GUI frameworks on top of the :class:`abstract base class <~.gui_app.MainAppBase>`
(implemented in the :mod:`ae.gui_app` portion of the `ae namespace <https://ae.readthedocs.io>`__):

* :mod:`Kivy <ae.kivy_app>` based on the `kivy framework <https://kivy.org>`__:
  `kivy lisz demo app <https://gitlab.com/ae-group/kivy_lisz>`__
* :mod:`Enaml <ae.enaml_app>` based on `the enaml framework <https://enaml.readthedocs.io/en/latest/>`__:
  `enaml lisz demo app <https://gitlab.com/ae-group/enaml_lisz>`__
* :mod:`Beeware Toga <ae.toga_app>` based on `the beeware framework <https://beeware.org>`__:
  `beeware toga lisz demo app <https://gitlab.com/ae-group/toga_lisz>`__
* :mod:`Dabo <ae.dabo_app>` based on `the dabo framework <https://dabodev.com/>`__:
  `dabo lisz demo app <https://gitlab.com/ae-group/dabo_lisz>`__
* :mod:`pyglet <ae.pyglet_app>`
* :mod:`pygobject <ae.pygobject_app>`
* :mod:`AppJar <ae.appjar_app>`

the main app base mixin class :class:`LiszDataMixin` provided by this module is used to manage the common data
structures, functions and methods for the various demo applications variants based on :mod:`ae.gui_app` and the related
GUI framework implementation portions (like e.g. :mod:`ae.kivy_app` and :mod:`ae.enaml_app`) of the ae namespace.


gui framework implementation variants
=====================================

kivy
----

the `kivy lisz app <https://gitlab.com/ae-group/kivy_lisz>`__ is based on the `kivy framework <https://kivy.org>`__, a
`pypi package <https://pypi.org/project/Kivy/>`__ documented `here <https://kivy.org/doc/stable/>`__.

.. list-table::

    * - .. figure:: ../img/kivy_lisz_root.png
           :alt: root list of a dark themed kivy lisz app
           :scale: 30 %

           kivy lisz app root list

      - .. figure:: ../img/kivy_lisz_fruits.png
           :alt: fruits sub-list of a dark themed kivy lisz app
           :scale: 30 %

           fruits sub-list

      - .. figure:: ../img/kivy_lisz_fruits_light.png
           :alt: fruits sub-list of a light themed kivy lisz app
           :scale: 30 %

           using light theme

    * - .. figure:: ../img/kivy_lisz_user_prefs.png
           :alt: user preferences dropdown
           :scale: 30 %

           lisz user preferences

      - .. figure:: ../img/kivy_lisz_color_editor.png
           :alt: kivy lisz color editor
           :scale: 30 %

           kivy lisz color editor

      - .. figure:: ../img/kivy_lisz_font_size_big.png
           :alt: lisz app using bigger font size
           :scale: 30 %

           bigger font size


kivy wish list
^^^^^^^^^^^^^^

* kv language looper pseudo widget (like enaml is providing) to easily generate sets of similar widgets.


enaml
-----

the `enaml lisz demo app <https://gitlab.com/ae-group/enaml_lisz>`__ is based on the
`enaml framework <https://pypi.org/project/enaml/>`__, a `pypi package <https://pypi.org/project/enaml/>`__ documented
`here at ReadTheDocs <https://enaml.readthedocs.io/en/latest/>`__.

.. list-table::
    :widths: 27 66

    * - .. figure:: ../img/enaml_lisz_fruits_sub_list.png
           :alt: fruits sub-list of dark themed enaml lisz app
           :scale: 27 %

           enaml/qt lisz app

      - .. figure:: ../img/enaml_lisz_light_landscape.png
           :alt: fruits sub-list of a light themed enaml lisz app in landscape
           :scale: 66 %

           light themed in landscape


automatic update of widget attributes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

dependencies have to be executed/read_from, so e.g. the icon attribute will not be updated if app.app_state_light_theme
gets changed::

    icon << main_app.cached_icon('font_size') or app.app_state_light_theme

in contrary the icon will be updated by the following two statements::

    icon << main_app.cached_icon('font_size') if app.app_state_light_theme else main_app.cached_icon('font_size')
    icon << app.app_state_light_theme == None or main_app.cached_icon('font_size')

KeyEvent implementation based on this SO answer posted by the enamlx author frmdstryr/Jairus Martin:
https://stackoverflow.com/questions/20380940/how-to-get-key-events-when-using-enaml. alternative and more complete
implementation can be found in the enamlx package (https://github.com/frmdstryr/enamlx).


enaml wish list
^^^^^^^^^^^^^^^

* type and syntax checking, code highlighting and debugging of enaml files within PyCharm.
* fix freezing of linux/Ubuntu system in debugging of opening/opened PopupViews in PyCharm.
"""
import ast
import os
import pathlib
from copy import deepcopy
from pprint import pformat
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from ae.base import norm_line_sep, norm_name                                                    # type: ignore
from ae.files import read_file_text, write_file_text                                            # type: ignore
from ae.i18n import get_f_string                                                                # type: ignore
from ae.core import DEBUG_LEVEL_VERBOSE                                                         # type: ignore
from ae.gui_app import id_of_flow, flow_action, flow_key, flow_path_strip, replace_flow_action  # type: ignore


__version__ = '0.3.48'


FLOW_PATH_ROOT_ID = '^^^^'  #: pseudo item id needed for flow path jumper and for drop onto leave item button
FLOW_PATH_TEXT_SEP = " / "  #: flow path separator for :meth:`~LiszDataMixin.flow_path_text`

FOCUS_FLOW_PREFIX = "->"    #: prefix shown in front of flow key of focused item

INVALID_ITEM_ID_PREFIX_CHARS = '[' + '{'  #: invalid initial chars in item id (to detect id | literal in flow key)
# currently only the '[' char is used (to put the node list data as literal in a flow key - see

NODE_FILE_PREFIX = 'node_'                      #: file name prefix for node imports/exports
NODE_FILE_EXT = '.txt'                          #: file extension for node imports/exports

IMPORT_NODE_MAX_FILE_LEN = 8192                 #: maximum file length of importable <file.NODE_FILE_EXT> file
IMPORT_NODE_MAX_ITEMS = 12                      #: maximum number of items to import or paste from clipboard

LiszItem = Dict[str, Any]                       #: node item data (nid) type
LiszNode = List[LiszItem]                       #: node/list type

NodeFileInfo = Tuple[str, LiszNode, str, str]   #: tuple of (node-parent-name, node-list, file_path, error-message)
NodeFilesInfo = List[NodeFileInfo]              #: list of node file info tuples


def check_item_id(item_id: str) -> str:
    """ check if the passed item id string is valid.

    :param item_id:             item id to check.
    :return:                    "" if all chars in the specified :paramref:`.item_id` argument are valid,
                                else one of the translated message strings.
    """
    msg = get_f_string("item id '{item_id}' ")
    if not isinstance(item_id, str):
        return msg + get_f_string("has to be a string but got {type(item_id)}")
    if not item_id.strip():
        return msg + get_f_string("has to be non-empty")
    if item_id == FLOW_PATH_ROOT_ID:
        return msg + get_f_string("cannot be equal to '{FLOW_PATH_ROOT_ID}'")
    if FLOW_PATH_TEXT_SEP in item_id:
        return msg + get_f_string("cannot contain '{FLOW_PATH_TEXT_SEP}'")
    if item_id[0] in INVALID_ITEM_ID_PREFIX_CHARS:
        return msg + get_f_string("cannot start with one of the characters '{INVALID_ITEM_ID_PREFIX_CHARS}'")
    return ""


def correct_item_id(item_id: str) -> str:
    """ strip and replace extra/invalid characters from the passed item id string.

    :param item_id:             item id string to correct.
    :return:                    corrected item id (can result in an empty string).
    """
    item_id = item_id.replace(FLOW_PATH_TEXT_SEP, '/').strip().strip('@~*-#.,;:').strip()
    if item_id == FLOW_PATH_ROOT_ID:
        item_id += '!'
    return item_id.lstrip(INVALID_ITEM_ID_PREFIX_CHARS)


def flow_path_items_from_text(text: str) -> Tuple[str, str, LiszNode]:
    """ parse and interpret text block for (optional) flow path text and node data (in pprint.pformat/repr format).

    :param text:                text block to be parsed. the text block can optionally be prefixed with an extra
                                line (separated by a new line '\\n' character) containing the destination flow path
                                in text format (using FLOW_PATH_TEXT_SEP to separate the flow path items).

                                the (rest of the) text block represents the node/item data in one of the
                                following formats:

                                * single text line (interpreted as single leaf item).
                                * multiple text lines (interpreted as multiple leaf items).
                                * dict repr string, starting with '{' character.
                                * list repr string, starting with '[' character.

    :return:                    tuple of
                                error message (empty string if no error occurred),
                                flow path (empty string if root or not given) and
                                node list.
    """
    flow_path_text = ""
    if text.startswith('{'):
        node_lit = '[' + text + ']'
    elif text.startswith('['):
        node_lit = text
    else:
        text = norm_line_sep(text)
        parts = text.split("\n", maxsplit=1)
        if len(parts) == 2 and parts[1].startswith(('[', '{')):
            flow_path_text = parts[0]
            node_lit = parts[1] if parts[1][0] == '[' else "[" + parts[1] + "]"
        else:
            node_lit = "[" + ",".join("{'id': '" + line + "'}" for line in text.split("\n") if line) + "]"

    parse_err_msg = ""
    try:
        node = ast.literal_eval(node_lit)
    except (SyntaxError, ValueError) as ex:
        parse_err_msg = str(ex)
        node = []

    return parse_err_msg, flow_path_text, node


def item_sel_filter(item: LiszItem) -> bool:
    """ callable to filter selected LiszItems.

    :param item:                item data structure to check.
    :return:                    True if item is a selected leaf or if item is a node with only selected sub-leaves,
                                else False.
    """
    if 'node' in item:
        for sub_item in item['node']:
            if not item_sel_filter(sub_item):
                return False
        return True
    return item.get('sel') == 1


def item_unsel_filter(item: LiszItem) -> bool:
    """ callable to filter unselected LiszItems.

    :param item:                item data structure to check.
    :return:                    True if item is an unselected leaf or if item is a node with only unselected leaves,
                                else False.
    """
    if 'node' in item:
        for sub_item in item['node']:
            if not item_unsel_filter(sub_item):
                return False
        return True
    return item.get('sel', 0) == 0


class LiszDataMixin:
    """ lisz data model - independent from used GUI framework. """
    root_node: LiszNode = []        #: root of lisz data structure
    current_node_items: LiszNode    #: node item data of the current node / sub list (stored as app state via root_node)
    filtered_indexes: List[int]     #: indexes of the filtered/displayed items in the current node
    # additional app-common attributes (never directly referenced/needed, keep for completeness/documentation).
    filter_selected: bool = False   #: True to hide/filter selected node items
    filter_unselected: bool = False  #: True to hide/filter unselected node items

    # mixin shadow attributes - implemented by :class:`~ae.console_app.ConsoleApp` or :class:`~ae.gui_app.MainAppBase`
    debug_level: int                #: :attr:`~AppBase.debug_level`
    flow_id: str                    #: current attr:`flow id <ae.gui_app.MainAppBase.flow_id>`
    flow_path: List[str]            #: :attr:`flow path <ae.gui_app.MainAppBase.flow_path>` ref. current node

    _refreshing_data: bool = False                      #: DEBUG True while running :meth:`~.refresh_all` method

    # abstract methods mostly implemented by :mod:`ae.gui_app`, some by the inheriting main app class

    call_method: Callable
    call_method_delayed: Callable
    change_app_state: Callable
    change_flow: Callable
    flow_path_action: Callable
    play_sound: Callable
    refresh_node_widgets: Callable      # implemented by the inheriting main app class

    # helper methods

    def add_item(self, nid: LiszItem, node_to_add_to: Optional[LiszNode] = None, new_item_index: int = 0) -> str:
        """ add item (leaf or node) to currently displayed node.

        :param nid:             LiszItem to add (has to have a non-empty item id).
        :param node_to_add_to:  node where the passed item will be added to (def=current node).
        :param new_item_index:  index where the new item will be inserted (default=0, ignored if item already exists).
        :return:                error message if any error happened, else empty string.
        """
        if node_to_add_to is None:
            node_to_add_to = self.current_node_items

        item_id = nid['id']
        want_node = 'node' in nid
        err_msg = self.edit_validate(-1, item_id, want_node=want_node,
                                     parent_node=node_to_add_to, new_item_index=new_item_index)
        if not err_msg:
            # overwrite inserted nid because edit_validate(used to ensure proper id and no dup) creates new nid
            node_to_add_to[new_item_index] = nid

        elif want_node:             # then first check if error is dup error and fixable
            item_idx = self.find_item_index(item_id, searched_node=node_to_add_to)
            if item_idx >= 0:                                   # found the blocking/duplicate item id
                if 'node' not in node_to_add_to[item_idx]:
                    node_to_add_to[item_idx]['node'] = []       # convert blocking item from leaf to node
                err_msg = ("(ignorable) " + err_msg) if self.debug_level else ""
                sub_err = self.add_items(nid['node'], node_to_add_to=node_to_add_to[item_idx]['node'])
                if sub_err:                                     # add (ignorable?) errors from sub-node adds
                    err_msg += "\n" + sub_err

        return err_msg

    def add_items(self, items: LiszNode, node_to_add_to: Optional[LiszNode] = None) -> str:
        """ add item to currently displayed node.

        :param items:           LiszNode list to add (each item has to have a non-empty item id).
        :param node_to_add_to:  node where the passed item will be added to (def=current node).
        :return:                error message if any error happened (multiple error messages are separated by \\\\n),
                                else empty string.
        """
        if node_to_add_to is None:
            node_to_add_to = self.current_node_items

        errors = []
        for item in reversed(items):
            err_msg = self.add_item(item, node_to_add_to=node_to_add_to)
            if err_msg:
                errors.append(err_msg)

        return "\n".join(errors)

    def change_sub_node_sel(self, node: LiszNode, set_sel_to: bool):
        """ change the selection of all the sub-leaves of the passed node to the specified value.

        :param node:            node of which to change the selection of the sub-item leaves.
        :param set_sel_to:      True will only toggle the unselected sub-item leaves, False only the selected ones.
        """
        for item in node:
            item.pop('sel', None)       # always first remove sel left-overs
            if 'node' in item:
                self.change_sub_node_sel(item['node'], set_sel_to)
            if set_sel_to:
                item['sel'] = 1.0

    def current_item_or_node_literal(self) -> str:
        """ return the currently focused/displayed item or node as repr string.

        :return:                pformat repr string of the currently focused item id/node or of the displayed node.
        """
        flow_id = self.flow_id
        if flow_action(flow_id) != 'focus':
            lit = pformat(self.flow_path_node())
        else:
            item = self.item_by_id(flow_key(flow_id))
            if 'node' in item:
                lit = pformat(item)
            else:
                lit = item['id']
        return lit

    def delete_items(self, *item_ids: str, parent_node: Optional[LiszNode] = None, node_only: bool = False) -> LiszNode:
        """ delete either complete items or sub node of the items (identified by the passed item ids).

        :param item_ids:        tuple of item ids to identify the items/sub-nodes to be deleted.
        :param parent_node:     node from where the item has to be removed from (default=current node).
        :param node_only:       True if only delete the sub-node of the identified item, False to delete the item.
        """
        if parent_node is None:
            parent_node = self.current_node_items

        del_items = []
        for item_id in item_ids:
            nid = self.item_by_id(item_id, searched_node=parent_node)
            if node_only:
                del_items.extend(nid.pop('node'))
            else:
                assert nid in parent_node, f"DEL item data: {nid} not in {parent_node}"
                parent_node.remove(nid)
                del_items.append(nid)

        return del_items

    def edit_validate(self, old_item_index: int, new_id: Optional[str] = None, want_node: Optional[bool] = None,
                      parent_node: Optional[LiszNode] = None, new_item_index: int = 0) -> str:
        """ validate the user changes after adding a new item or editing an existing item.

        :param old_item_index:  index in the current node of the edited item or -1 if a new item (to be added).
        :param new_id:          new/edited id string.
        :param want_node:       True if the new/edited item will have a sub-node, False if not.
        :param parent_node:     node where the edited/added item as to be updated/inserted (default=current list).
        :param new_item_index:  index where the new item have to be inserted (default=0, ignored in edit item mode).
        :return:                empty string on successful edit validation or on cancellation of new item (with
                                empty id string), else error string or
                                `'request_delete_confirmation_for_item'` if the user has to confirm the deletion
                                after the user wiped the item id string or
                                `'request_delete_confirmation_for_node'` if the user has to confirm the
                                removal of the sub-node.
        """
        add_item = old_item_index == -1
        if parent_node is None:
            parent_node = self.current_node_items

        if new_id is not None:
            if not new_id:
                # on empty id cancel addition (if add_item), else request confirmation from user for item deletion
                return "" if add_item else 'request_delete_confirmation_for_item'

            if add_item:
                new_id = correct_item_id(new_id)
            else:
                chk_err = check_item_id(new_id)
                if chk_err:
                    return chk_err

            found_item_index = self.find_item_index(new_id, searched_node=parent_node)
            if found_item_index != -1 and (add_item or found_item_index != old_item_index):
                return get_f_string("item id '{new_id}' exists already")

        if add_item:                        # add new item
            if not new_id:
                return ""
            nid = dict(id=new_id)
            if want_node:
                nid['node'] = []            # type: ignore   # mypy not supports recursive types see issue #731
            parent_node.insert(new_item_index, nid)

        else:                               # edit item
            nid = parent_node[old_item_index]
            if new_id:
                nid['id'] = new_id
            if want_node is not None and want_node != ('node' in nid):  # note: != has lower priority than in operator
                if want_node:
                    nid['node'] = []        # type: ignore   # mypy not supports recursive types see issue #731
                elif nid['node']:           # let user confirm node deletion of non-empty nid['node']
                    return 'request_delete_confirmation_for_node'
                else:
                    nid.pop('node')         # remove empty node

        self.play_sound('added' if add_item else 'edited')

        return ""

    def export_node(self, flow_path: List[str], file_path: str = ".", node: Optional[LiszNode] = None) -> str:
        """ export node specified by the passed :paramref:`~export_node.flow_path` argument.

        :param flow_path:   flow path of the node to export.
        :param file_path:   folder to store the node data into (def=current working directory).
        :param node:        explicit/filtered node items (if not passed then all items will be exported).
        :return:            empty string if node got exported without errors, else the error message/raised exception.
        """
        if not node:
            node = self.flow_path_node(flow_path)
        flow_path = flow_path_strip(flow_path)
        file_name = NODE_FILE_PREFIX + (norm_name(flow_key(flow_path[-1]), allow_num_prefix=True) if flow_path else
                                        FLOW_PATH_ROOT_ID) + NODE_FILE_EXT

        try:
            # the alternative `os.makedirs(exist_ok=True)` has problems on POSIX with '..' in the path
            pathlib.Path(file_path).mkdir(parents=True, exist_ok=True)
            err_msg = "" if write_file_text(pformat(node), os.path.join(file_path, file_name)) \
                else f"export_node() error writing to file {os.path.join(file_path, file_name)}"
        except (FileExistsError, FileNotFoundError, OSError, ValueError) as ex:
            err_msg = str(ex)
        return err_msg

    def find_item_index(self, item_id: str, searched_node: Optional[LiszNode] = None) -> int:
        """ determine list index of the passed item id in the searched node or in the current node.

        :param item_id:         item id to find.
        :param searched_node:   searched node. if not passed then the current node will be searched instead.
        :return:                item list index in the searched node or -1 if item id was not found.
        """
        if searched_node is None:
            searched_node = self.current_node_items
        for list_idx, nid in enumerate(searched_node):
            if nid['id'] == item_id:
                return list_idx
        return -1

    def flow_key_text(self, flow_id: str, landscape: bool) -> str:
        """ determine the shortest possible text fragment of the passed flow key that is unique in the current node.

        used to display unique part of the key of the focused item/node.

        :param flow_id:         flow id to get key to check from (pass the observed value to update GUI automatically,
                                either self.app_state_flow_id or self.app_states['flow_id']).
        :param landscape:       True if window has landscape shape (resulting in larger abbreviation). pass the observed
                                attribute, mostly situated in the framework_win (e.g. self.framework_win.landscape).
        :return:                display text containing flow key.
        """
        if flow_action(flow_id) == 'focus':
            key = flow_key(flow_id)
            key_len = len(key)
            id_len = 6 if landscape else 3
            for nid in self.current_node_items:
                item_id = nid['id']
                if item_id != key:
                    while item_id.startswith(key[:id_len]) and id_len < key_len:
                        id_len += 1
            return f" {FOCUS_FLOW_PREFIX}{key[:id_len]}"
        return f".{flow_id}" if self.debug_level >= DEBUG_LEVEL_VERBOSE else ""

    def flow_path_from_text(self, text: str, skip_check: bool = False) -> List[str]:
        """ restore the full complete flow path from the shortened flow keys generated by :meth:`.flow_path_text`.

        :param text:            flow path text - like returned by :meth:`~LiszDataMixin.flow_path_text`.
        :param skip_check:      pass True to skip the check if the flow path exists in the current self.root_node.
        :return:                flow path list.
        """
        flow_path = []
        if text not in ('', FLOW_PATH_ROOT_ID):
            node = self.root_node
            for part in text.split(FLOW_PATH_TEXT_SEP):
                if skip_check:
                    flo_key = part
                else:
                    for nid in node:
                        if nid['id'].startswith(part) and 'node' in nid:
                            flo_key = nid['id']
                            node = nid['node']
                            break
                    else:
                        break       # should actually not be needed, will repair data tree errors
                flow_path.append(id_of_flow('enter', 'item', flo_key))
        return flow_path

    def flow_path_node(self, flow_path: Optional[List[str]] = None, create: bool = False) -> LiszNode:
        """ determine the node specified by the passed flow path, optionally create missing nodes of the flow path.

        :param flow_path:       flow path list.
        :param create:          pass True to create missing nodes.
                                only on False this method will return empty list on invalid/broken flow_path.
        :return:                node list at flow_path (if found -or- created is True and no-creation-errors)
                                or empty list (if flow_path not found and created is False or on creation error).
        """
        if flow_path is None:
            flow_path = self.flow_path

        node = self.root_node

        for flow_id in flow_path:
            if flow_action(flow_id) == 'enter':
                node_id = flow_key(flow_id)
                item = self.item_by_id(node_id, searched_node=node)
                if item not in node or 'node' not in item:
                    if not create or item not in node and self.add_item(item, node_to_add_to=node):
                        return []               # on error RETURN empty list
                    if 'node' not in item:
                        item['node'] = []
                node = item['node']

        return node

    def flow_path_quick_jump_nodes(self) -> List[str]:
        """ determine the current flow paths of all nodes excluding the current, to quick-jump from current node.

        :return:                list of flow path texts of all nodes apart from the current one.
        """
        paths: List[str] = []
        deeper_flow_path: List[str] = []

        def append_node_path_texts(node):
            """ recursively collect all available nodes (possible flow paths) """
            if node != self.current_node_items:
                paths.append(self.flow_path_text(deeper_flow_path, display_root=True))
            for nid in node:
                if 'node' in nid:
                    deeper_flow_path.append(id_of_flow('enter', 'item', nid['id']))
                    append_node_path_texts(nid['node'])
                    deeper_flow_path.pop()

        append_node_path_texts(self.root_node)

        return paths

    def flow_path_text(self, flow_path: List[str], min_len: int = 3, display_root: bool = False,
                       separator: str = FLOW_PATH_TEXT_SEP) -> str:
        """ generate shortened display text from the passed flow path.

        :param flow_path:       flow path list.
        :param min_len:         minimum length of node ids (flow id keys). pass zero value to not shorten ids.
        :param display_root:    pass True to return FLOW_PATH_ROOT_ID on empty/root path.
        :param separator:       path item separator (default=FLOW_PATH_TEXT_SEP).
        :return:                shortened display text string of the passed flow path (which can be converted back
                                to a flow path list with the method :meth:`.flow_path_from_text`).
        """
        path_nid = None         # suppress Pycharm PyUnboundLocalVariable inspection warning
        shortening = bool(min_len)
        shortened_ids = []
        node = self.root_node
        for flow_id in flow_path:
            if flow_action(flow_id) != 'enter':
                continue
            node_id = flow_key(flow_id)
            sub_id_len = len(node_id)
            id_len = min_len if shortening else sub_id_len
            for nid in node:
                if nid['id'] == node_id:
                    path_nid = nid
                elif shortening:
                    while nid['id'].startswith(node_id[:id_len]) and id_len < sub_id_len:
                        id_len += 1

            shortened_ids.append(node_id[:id_len])
            if path_nid and 'node' in path_nid:     # prevent error in quick jump to root
                node = path_nid['node']

        return separator.join(shortened_ids) if shortened_ids else (FLOW_PATH_ROOT_ID if display_root else '')

    def focus_neighbour_item(self, delta: int):
        """ move flow id to previous/next displayed/filtered node item.

        :param delta:           moving step (if greater 0 then forward, else backward).
        """
        filtered_indexes = self.filtered_indexes
        if filtered_indexes:
            flow_id = self.flow_id
            if flow_id:
                item_idx = self.find_item_index(flow_key(flow_id))
                assert item_idx >= 0
                filtered_idx = filtered_indexes.index(item_idx)
                idx = min(max(0, filtered_idx + delta), len(filtered_indexes) - 1)
            else:
                idx = min(max(-1, delta), 0)
            self.change_flow(id_of_flow('focus', 'item', self.current_node_items[filtered_indexes[idx]]['id']))

    def global_variables(self, **patches) -> Dict[str, Any]:
        """ overridden to add app-specific globals. """
        # noinspection PyUnresolvedReferences
        return super().global_variables(FLOW_PATH_ROOT_ID=FLOW_PATH_ROOT_ID, **patches)  # type: ignore

    def importable_node_files(self, folder_path: str = ".") -> NodeFilesInfo:
        """ load and check all nodes found in the app folder documents of this app.

        :param folder_path: path to the folder where the node files are situated (def=current working directory).
        :return:            list of node file tuples of (node_name, node, file_path, error-message).
        """
        node_file_info_tuples = []
        for node_file in os.scandir(folder_path):
            # noinspection PyUnresolvedReferences
            file_name = node_file.name
            # noinspection PyUnresolvedReferences
            if file_name.endswith(NODE_FILE_EXT) and node_file.is_file():
                # noinspection PyUnresolvedReferences
                node_file_info_tuples.append(self.import_file_info(node_file.path))
        return node_file_info_tuples

    @staticmethod
    def import_file_info(file_path: str, node_name: str = "") -> NodeFileInfo:
        """ load node file and determine node content.

        :param file_path:   path to the node file to import.
        :param node_name:   optional name/id of the parent node name. if not passed then it will be determined
                            from the file name (removing :data:`NODE_FILE_PREFIX` and file extension).
        :return:            node file info tuple as: (node name, node-data or empty list, file path, error message).
        """
        if not node_name:
            node_name = os.path.splitext(os.path.basename(file_path))[0]
            if node_name.startswith(NODE_FILE_PREFIX):
                node_name = node_name[len(NODE_FILE_PREFIX):]

        content = read_file_text(file_path, error_handling='strict')
        if content is None:
            return node_name, [], file_path, "file load error"

        file_len = len(content)
        if file_len > IMPORT_NODE_MAX_FILE_LEN:
            return (node_name, [], file_path,
                    f"import file is bigger than {IMPORT_NODE_MAX_FILE_LEN} bytes ({file_len})")

        err_msg, _, node = flow_path_items_from_text(content)       # ignore optional flow path given in 1st line
        if err_msg or not node:
            return node_name, [], file_path, "invalid file content or empty file; ERR=" + err_msg

        if len(node) > IMPORT_NODE_MAX_ITEMS:
            return (node_name, [], file_path,
                    f"import file contains more than {IMPORT_NODE_MAX_ITEMS} items ({len(node)})")

        return node_name, node, file_path, ""

    def import_items(self, node: LiszNode, parent: Optional[LiszNode] = None, item_index: int = 0) -> str:
        """ import passed node items into the passed parent/destination node at the given index.

        :param node:            node with items to import/add.
        :param parent:          destination node to add the node items to (def=current node list).
        :param item_index:      list index in the destination node where the items have to be inserted (default=0).
        :return:                empty string if all items of node got imported correctly, else error message string.
        """
        error_messages = []
        for item in node:
            err_msg = self.edit_validate(-1, item['id'], parent_node=parent, new_item_index=item_index)
            if err_msg:
                error_messages.append(err_msg)
            else:
                item_index += 1

        return "\n".join(error_messages)

    def import_node(self, node_id: str, node: LiszNode, parent: Optional[LiszNode] = None, item_index: int = 0) -> str:
        """ import passed node as new node into the passed parent node at the given index.

        :param node_id:         id of the new node to import/add.
        :param node:            node with items to import/add.
        :param parent:          destination node to add the new node to (def=current node list).
        :param item_index:      list index in the parent node where the items have to be inserted (default=0).
        :return:                empty string if node got added/imported correctly, else error message string.
        """
        if parent is None:
            parent = self.current_node_items

        err_msg = self.edit_validate(-1, node_id, want_node=True, parent_node=parent, new_item_index=item_index)
        if not err_msg:
            # extend the list instance (that got already created/added by edit_validate()) with the loaded node data
            # use self.import_items() to ensure correct node ids, instead of: parent[item_index]['node'].extend(node)
            err_msg = self.import_items(node, parent=parent[item_index]['node'])

        return err_msg

    def item_by_id(self, item_id: str, searched_node: Optional[LiszNode] = None) -> LiszItem:
        """ search item in either the passed or the current node.

        :param item_id:         item id to find.
        :param searched_node:   searched node. if not passed then the current node will be searched instead.
        :return:                found item or if not found a new dict with the single key=value 'id'=item_id.
        """
        if searched_node is None:
            searched_node = self.current_node_items
        index = self.find_item_index(item_id, searched_node=searched_node)
        if index != -1:
            return searched_node[index]
        return dict(id=item_id)

    def move_item(self, dragged_node: LiszNode, dragged_id: str,
                  dropped_path: Optional[List[str]] = None, dropped_id: str = '') -> bool:
        """ move item id from passed dragged_node to the node and index specified by dropped_path and dropped_id.

        :param dragged_node:    node where the item got dragged/moved from.
        :param dragged_id:      id of the dragged/moved item.
        :param dropped_path:    optional destination/drop node path, if not passed use dragged_node.
        :param dropped_id:      optional destination item where the dragged item will be moved before it.
                                if empty string passed or not passed then the item will be placed at the end of
                                the destination node.
        """
        if dropped_path is None:
            dropped_node = dragged_node
        else:
            dropped_node = self.flow_path_node(dropped_path)

        src_node_idx = self.find_item_index(dragged_id, searched_node=dragged_node)
        dst_node_idx = self.find_item_index(dropped_id, searched_node=dropped_node) if dropped_id else len(dropped_node)
        assert src_node_idx >= 0 and dst_node_idx >= 0

        if dragged_node != dropped_node and self.find_item_index(dragged_id, searched_node=dropped_node) != -1:
            self.play_sound('error')
            return False

        nid = dragged_node.pop(src_node_idx)
        if dragged_node == dropped_node and dst_node_idx > src_node_idx:
            dst_node_idx -= 1
        dropped_node.insert(dst_node_idx, nid)

        return True

    def node_info(self, node: LiszNode, what: Tuple[str, ...] = (), recursive: bool = True
                  ) -> Dict[str, Union[int, str, List[str]]]:
        """ determine statistics info for the node specified by :paramref:`~node_info.flow_path`.

        :param node:            node to get info for.

        :param what:            pass tuple of statistic info fields to include only these into the returned dict
                                (passing an empty tuple or nothing will include all the following fields):

                                * 'count': number of items (nodes and leaves) in this node (including sub-nodes).
                                * 'leaf_count': number of sub-leaves.
                                * 'node_count': number of sub-nodes.
                                * 'selected_leaf_count': number of selected sub-leaves.
                                * 'unselected_leaf_count': number of unselected sub-leaves.
                                * 'names': list of all sub-item/-node names/ids.
                                * 'leaf_names': list of all sub-leaf names.
                                * 'selected_leaf_names': list of all selected sub-leaf names.
                                * 'unselected_leaf_names': list of all unselected sub-leaf names.

        :param recursive:       pass False if only the passed node has to be investigated.

        :return:                dict with the node info specified by the :paramref:`~node_info.what` argument.
        """
        names = self.sub_item_ids(node=node, leaves_only=False, recursive=recursive)
        count = len(names)
        leaf_names = self.sub_item_ids(node=node, recursive=recursive)
        leaf_count = len(leaf_names)
        selected_leaf_names = self.sub_item_ids(node=node, hide_sel_val=False, recursive=recursive)
        selected_leaf_count = len(selected_leaf_names)          # noqa: F841 # pylint: disable=possibly-unused-variable
        unselected_leaf_names = self.sub_item_ids(node=node, hide_sel_val=True, recursive=recursive)
        unselected_leaf_count = len(unselected_leaf_names)      # noqa: F841 # pylint: disable=possibly-unused-variable
        node_count = count - leaf_count                         # noqa: F841 # pylint: disable=possibly-unused-variable

        return {k: v for k, v in locals().items() if not what or k in what}

    def on_app_state_root_node_save(self, root_node: LiszNode) -> LiszNode:
        """ shrink root_node app state variable before it get saved to the config file. """
        self.shrink_node_size(root_node)
        return root_node

    def on_filter_toggle(self, toggle_attr: str, _event_kwargs: Dict[str, Any]) -> bool:
        """ toggle filter on click of either the selected or the unselected filter button.

        note that the inverted filter may be toggled to prevent both filters active.

        :param toggle_attr:     specifying the filter button to toggle, either 'filter_selected' or 'filter_unselected'.
        :param _event_kwargs:   unused.
        :return:                True to process flow id change.
        """
        # inverted filter will be set to False if was True and toggled filter get changed to True.
        invert_attr = 'filter_unselected' if toggle_attr == 'filter_selected' else 'filter_selected'

        filtering = not getattr(self, toggle_attr)
        self.change_app_state(toggle_attr, filtering)
        if filtering and getattr(self, invert_attr):
            self.change_app_state(invert_attr, False)

        self.play_sound(f'filter_{"on" if filtering else "off"}')
        self.refresh_node_widgets()

        return True

    def on_item_enter(self, _key: str, event_kwargs: dict) -> bool:
        """ entering sub node from current node.

        :param _key:            flow key (item id).
        :param event_kwargs:    event kwargs.
        :return:                True to process/change flow id.
        """
        self.play_sound(id_of_flow('enter', 'item'))
        event_kwargs['changed_event_name'] = 'refresh_all'
        return True

    def on_item_leave(self, _key: str, event_kwargs: dict) -> bool:
        """ leaving sub node, setting current node to parent node.

        :param _key:            flow key (item id).
        :param event_kwargs:    event kwargs.
        :return:                True to process/change flow id.
        """
        self.play_sound(id_of_flow('leave', 'item'))
        event_kwargs['changed_event_name'] = 'refresh_all'
        return True

    def on_item_sel_toggle(self, item_id: str, event_kwargs: dict) -> bool:
        """ toggle selection of leaf item.

        :param item_id:         item id of the leaf to toggle selection for.
        :param event_kwargs:    event kwargs.
        :return:                True to process/change flow id.
        """
        self.toggle_item_sel(self.find_item_index(item_id))
        event_kwargs['flow_id'] = id_of_flow('focus', 'item', item_id)
        return True

    def on_item_sel_change(self, item_id: str, event_kwargs: dict) -> bool:
        """ toggle, set or reset in the current node the selection of a leaf item or of the sub-leaves of a node item.

        :param item_id:         item id of the leaf/node to toggle selection for.
        :param event_kwargs:    event kwargs, containing a `set_sel_to` key with a boolean value, where
                                True will select and False deselect the item (or the sub-items if the item is a
                                non-empty node).
        :return:                True to process/change flow id.

        this flow change event can be used alternatively to :meth:`~LiszDataMixin.on_item_sel_toggle`
        for more sophisticated lisz app implementations, like e.g. the
        `kivy lisz demo app <https://gitlab.com/ae-group/kivy_lisz>`__ .
        """
        node_idx = self.find_item_index(item_id)
        set_sel_to = event_kwargs['set_sel_to']
        item = self.current_node_items[node_idx]
        node = item.get('node')
        if node is not None:
            self.change_sub_node_sel(node, set_sel_to)
            if set_sel_to:
                item['sel'] = 1.0
        else:
            self.toggle_item_sel(node_idx)
        event_kwargs['changed_event_name'] = 'refresh_node_widgets'
        event_kwargs['flow_id'] = id_of_flow('focus', 'item', item_id)
        return True

    on_item_sel_confirming = on_item_sel_change     #: confirming sub-list item de-/selection from ItemSelConfirmPopup

    def on_key_press(self, modifiers: str, key_code: str) -> bool:
        """  check key press event to be handled and processed as command/action.

        :param modifiers:       modifier keys string.
        :param key_code:        key code string.
        :return:                True if key event got processed/used, else False.
        """
        if modifiers == 'Ctrl' and key_code in ('c', 'v', 'x'):
            if self.call_method('on_clipboard_key_' + key_code):    # redirect to framework-specific implementation
                return True

        elif key_code == 'r':
            if modifiers == 'Shift':
                self.change_app_state('flow_path', [])  # quick jump to root (also repairing any flow path errors)
                self.change_app_state('flow_id', '')
            self.refresh_all()
            return True

        flo_act = flow_action(self.flow_id)
        if modifiers or flo_act not in ('', 'focus'):
            return False

        # handle hot key without a modifier key and while in item list, first current item flow changes
        focused_id = flo_act == 'focus' and flow_key(self.flow_id)
        if key_code == 'up':
            self.focus_neighbour_item(-1)
        elif key_code == 'down':
            self.focus_neighbour_item(1)
        elif key_code == 'pgup':
            self.focus_neighbour_item(-15)
        elif key_code == 'pgdown':
            self.focus_neighbour_item(15)
        elif key_code == 'home':
            self.focus_neighbour_item(-999999)
        elif key_code == 'end':
            self.focus_neighbour_item(999999)

        # toggle selection of current item
        elif key_code == ' ' and focused_id:    # key string 'space' is not in Window.command_keys
            self.change_flow(id_of_flow('toggle', 'item_sel', focused_id))

        # enter/leave flow in current list
        elif key_code in ('enter', 'right') and focused_id and 'node' in self.item_by_id(focused_id):
            self.change_flow(id_of_flow('enter', 'item', focused_id))
        elif key_code in ('escape', 'left') and self.flow_path:
            self.change_flow(id_of_flow('leave', 'item'))

        # item processing: add, edit or request confirmation of deletion of current item
        elif key_code in ('a', '+'):
            self.change_flow(id_of_flow('add', 'item'))

        elif key_code == 'e' and focused_id:
            self.change_flow(replace_flow_action(self.flow_id, 'edit'))  # popup_kwargs=dict(parent=self.framework_win))

        elif key_code in ('-', 'del') and focused_id:
            self.change_flow(id_of_flow('confirm', 'item_deletion', focused_id))

        else:
            return False    # pressed key not processable in the current flow/app-state

        return True         # key press processed

    def on_node_extract(self, flow_path_text: str, event_kwargs: dict) -> bool:
        """ extract the leaves of the node specified by `flow_path_text`.

        :param flow_path_text:  flow path text or list literal (identifying the start node to extract from).

        :param event_kwargs:    extra arguments specifying extract options (only `extract_type` is mandatory):

                                `extract_type` specifies extract destination and an optional filter on un-/selected
                                items. the first part defines the extract action (copy/cut/delete/export/share)
                                and an optional second part (separated by an underscore) the filter.
                                e.g. the following string values can be passed for a 'copy' extract action:

                                * 'copy' is copying all items of the specified node to the clipboard.
                                * 'copy_sel' is copying only the selected items of the node to the clipboard.
                                * 'copy_unsel' is copying only the unselected items to the clipboard.

                                `recursive` specifies if `False` that the extraction affects only the leaves of the
                                current node specified by `flow_path_text` and
                                if `True` the extraction affects also the leaves of the sub-nodes (default=True).

                                `export_path` specifies the destination folder of the export action (default='.'/CWD).

        :return:                True to process/change flow.
        """
        flow_path = ast.literal_eval(flow_path_text) if flow_path_text and flow_path_text[0] == '[' else \
            self.flow_path_from_text(flow_path_text)
        node = self.flow_path_node(flow_path)
        extract_action, *what = event_kwargs['extract_type'].split('_')
        recursive = event_kwargs.get('recursive', True)

        if not what:
            extract_filter = None
            delete_filter = lambda item: True   # noqa: E731
        elif what[0] == 'sel':
            extract_filter = item_unsel_filter
            delete_filter = item_sel_filter
        else:
            extract_filter = item_sel_filter
            delete_filter = item_unsel_filter

        extract_node = deepcopy(node) if recursive else [item for item in node if 'node' not in item]
        snd_name = 'added'
        if extract_action in ('cut', 'delete'):
            self.shrink_node_size(node, item_filter=delete_filter, recursive=recursive)      # in-place deletion
            snd_name = 'deleted'
            event_kwargs['flow_id'] = id_of_flow('')
            event_kwargs['reset_last_focus_flow_id'] = True
            event_kwargs['changed_event_name'] = 'refresh_all'
        self.shrink_node_size(extract_node, item_filter=extract_filter, recursive=recursive)

        if extract_action in ('copy', 'cut'):
            self.call_method('on_clipboard_key_c', pformat(extract_node))  # Clipboard.copy(repr(node))
        elif extract_action == 'export':
            self.export_node(flow_path, file_path=event_kwargs.get('export_path', '.'), node=extract_node)
        elif extract_action == 'share':
            self.call_method_delayed(0.69, 'share_node', flow_path, node=extract_node)

        # dismiss prevents dropdown._reposition() weakref-err (refresh_all() recreates attach_to widget)
        # event_kwargs['popups_to_close'][0].attach_to = None  # close() results in weakref-err in container.on_dismiss
        # now fixed by resetting attach_to to None in MainAppBase.change_flow()

        self.play_sound(snd_name)
        return True

    def on_node_jump(self, flow_path_text: str, event_kwargs: Dict[str, Any]) -> bool:
        """ FlowButton clicked event handler restoring flow path from the flow key.

        :param flow_path_text:  flow path text (identifying where to jump to).
        :param event_kwargs:    event arguments (used to reset flow id).
        :return:                always True to process/change flow.
        """
        flow_path = self.flow_path_from_text(flow_path_text)

        # cannot close popup here because the close event will be processed in the next event loop
        # and because flow_path_from_text() is overwriting the open popup action in self.flow_path
        # we have to re-add the latest flow id entry from the current/old flow path that opened the jumper
        # here (for it can be removed by FlowPopup closed event handler when the jumper popup closes).
        # open_jumper_flow_id = id_of_flow('open', 'flow_path_jumper')
        # assert open_jumper_flow_id == self.flow_path[-1]
        if self.flow_path_action(flow_path) == 'enter' and self.flow_path_action() == 'open':
            flow_path.append(self.flow_path[-1])

        self.change_app_state('flow_path', flow_path)
        self.play_sound(id_of_flow('enter', 'item'))

        event_kwargs['flow_id'] = id_of_flow('')
        event_kwargs['reset_last_focus_flow_id'] = True             # reset _last_focus_flow_id of last node
        event_kwargs['changed_event_name'] = 'refresh_all'

        return True

    def refresh_all(self):
        """ changed flow event handler refreshing currently displayed items after changing current node/flow path. """
        assert not self._refreshing_data
        self._refreshing_data = True
        try:
            if self.debug_level:
                self.play_sound('debug_draw')

            self.refresh_current_node_items_from_flow_path()

            # save last actual flow id (because refreshed/redrawn widget observers could change flow id via focus)
            flow_id = self.flow_id

            self.refresh_node_widgets()

            if flow_action(flow_id) == 'focus':
                item_idx = self.find_item_index(flow_key(flow_id))
                if item_idx not in self.filtered_indexes:
                    flow_id = id_of_flow('')  # reset flow id because last focused item got filtered/deleted by user

            self.change_app_state('flow_id', flow_id, send_event=False)     # correct flow or restore silently

            if flow_action(flow_id) == 'focus':
                self.call_method('on_flow_widget_focused')                  # restore focus
        finally:
            assert self._refreshing_data
            self._refreshing_data = False

    def refresh_current_node_items_from_flow_path(self):
        """ refresh current node including the depending on display node. """
        self.current_node_items = self.flow_path_node()

    def shrink_node_size(self, node: LiszNode, item_filter: Optional[Callable[[LiszItem], bool]] = None,
                         recursive: bool = True):
        """ shrink node size by removing unneeded items and `sel` keys, e.g. to export or save space in config file.

        :param node:            start or root node to shrink (in-place!).
        :param item_filter:     pass callable to remove items from the passed node and its sub-nodes.
                                the callable is getting each item as argument and has to return True
                                to remove it from its node.
        :param recursive:       pass False if only the passed start node has to be shrunk.
        """
        del_items = []

        for item in node:
            is_node = 'node' in item
            if is_node or item.get('sel', 0) == 0:
                item.pop('sel', None)
            elif 'sel' in item:
                item['sel'] = 1  # remove also decimal point and zero (float to int) from this selected leaf item
            if recursive and is_node:
                self.shrink_node_size(item['node'], item_filter=item_filter)
            if item_filter and item_filter(item):
                del_items.append(item)

        for item in del_items:
            node.remove(item)

    def sub_item_ids(self, node: Optional[LiszNode] = None, item_ids: Tuple[str, ...] = (),
                     leaves_only: bool = True, hide_sel_val: Optional[bool] = None, recursive: bool = True,
                     sub_ids: Optional[List[str]] = None) -> List[str]:
        """ return item names/ids of the specified items including their sub-node items (if exists and recursive==True).

        used to determine the affected item ids if user want to delete or de-/select the sub-items of
        the item(s) specified by the passed arguments.

        :param node:            searched node, if not passed use the current node as default.
        :param item_ids:        optional item id filter, if passed only items with an id in this tuple will be returned.
                                this filter will not be used for sub-node filtering (if recursive==True).
        :param leaves_only:     pass False to also include/return node item ids.
        :param hide_sel_val:    pass False/True to exclude un-/selected leaf items from the returned list of ids.
                                if None or not passed then all found items will be included.
        :param recursive:       pass False if only the passed start node has to be investigated/included.
        :param sub_ids:         already found sub item ids (used for the recursive calls of this method).
        :return:                list of found item ids.
        """
        if node is None:
            node = self.current_node_items
        if sub_ids is None:
            sub_ids = []

        for item in node:
            if item_ids and item['id'] not in item_ids:
                continue
            if (not leaves_only) if 'node' in item else (hide_sel_val is None or bool(item.get('sel')) != hide_sel_val):
                sub_ids.append(item['id'])
            sub_node = item.get('node')
            if recursive and sub_node:
                self.sub_item_ids(node=sub_node, leaves_only=leaves_only, hide_sel_val=hide_sel_val, sub_ids=sub_ids)

        return sub_ids

    def toggle_item_sel(self, node_idx: int):
        """ toggle the item selection of the item identified by the list index in the current node.

        :param node_idx:            list index of the item in the current node to change the selection for.
        """
        if item_sel_filter(self.current_node_items[node_idx]):
            self.current_node_items[node_idx].pop('sel', None)
        else:
            self.current_node_items[node_idx]['sel'] = 1.0
