"""
base class for python applications with a graphical user interface
==================================================================

the abstract base class :class:`MainAppBase` provided by this ae namespace portion allows the integration of any Python
GUI framework into the ae namespace.

on overview about the available GUI-framework-specific ae namespace portion implementations can be found in the
documentation of the ae namespace portion :mod:`ae.lisz_app_data`.


extended console application environment
----------------------------------------

the abstract base class :class:`MainAppBase` inherits directly from the ae namespace class
:class:`ae console application environment class <ae.console.ConsoleApp>`. the so inherited helper methods are useful
to log, configure and control the run-time of your GUI app via command line arguments.

.. hint::
    please see the documentation of :ref:`config-options` and :ref:`config-files` in the :mod:`ae.console` namespace
    portion/module for more detailed information.

:class:`MainAppBase` adds on top of the :class:`~ae.console.ConsoleApp` the concepts of :ref:`application status` and
:ref:`application flow`, explained further down.


application events
------------------

the events described in this section are fired on application startup and shutdown. additional events get fired e.g. in
relation to the app states (documented further down in the section :ref:`app state events`) or on start or stop of an
:ref:`app tour <app tour start and stop events>`.

the following application events are fired exactly one time at startup in the following order:

* `on_app_init`: fired **after** :class:`ConsoleApp` app instance got initialized (detected config files)
  and **before** the image and sound resources and app states get loaded and the GUI framework app class instance gets
  initialized.
* `on_app_start`: fired **after** the call of the method :meth:`~MainAppBase.run_app` and **before** the command line
  options get parsed.
* `on_app_run`: fired **after** the parsing of the command line arguments and options and **before** all portion
  resources got imported.
* `on_app_build`: fired **after** all portion resources got loaded/imported and **before** the framework event
  loop of the used GUI framework gets started.

.. note::
    the `on_app_build` application event has to be fired by the used GUI framework.

.. hint::
    depending on the used gui framework there can be more app start events. e.g. the :mod:`ae.kivy_app` module fires the
    events `on_app_built` and `on_app_started` (all of them fired after `on_app_run` and `on_app_build`). see also
    :ref:`kivy application events`.


when an application gets stopped then the following events get fired in the following order:

* `on_app_stop`: fired **after** the call of the method :meth:`~MainAppBase.stop_app` and **before** the framework win
  will be closed.
* `on_app_exit`: fired **after* framework win got closed and just **before** the event loop of the GUI framework will be
  stopped and the app shutdown.
* `on_app_quit`: fired **after** the event loop of the GUI framework got stopped and before the :meth:`AppBase.shutdown`
  method will be called.

.. note::
    the `on_app_stop` and `on_app_exit` events will only be fired if the app is explicitly calling the
    :meth:`~MainAppBase.stop_app` method.

.. hint::
    depending on the used gui framework there can be more events. e.g. the :mod:`ae.kivy_app` module fires the event
    `on_app_stopped` (before `on_app_stop` respectively `on_app_quit`).


application status
------------------

any application- and user-specific configurations like e.g. the last window position/size, the app theme/font/language
or the last selected flow within your app, could be included in the application status.

this namespace portion introduces the section `aeAppState` in the app :ref:`config-files`, where any status values can
be stored persistently to be recovered on the next startup of your application.

.. hint::
    the section name `aeAppState` is declared by the :data:`APP_STATE_SECTION_NAME` constant. if you need to access this
    config section directly then please use this constant instead of the hardcoded section name.


.. _app-state-variables:

app state variables
^^^^^^^^^^^^^^^^^^^

this module is providing/pre-defining the following application state variables:

    * :attr:`~MainAppBase.app_state_version`
    * :attr:`~MainAppBase.flow_id`
    * :attr:`~MainAppBase.flow_id_ink`
    * :attr:`~MainAppBase.flow_path`
    * :attr:`~MainAppBase.flow_path_ink`
    * :attr:`~MainAppBase.font_size`
    * :attr:`~MainAppBase.lang_code`
    * :attr:`~MainAppBase.light_theme`
    * :attr:`~MainAppBase.selected_item_ink`
    * :attr:`~MainAppBase.sound_volume`
    * :attr:`~MainAppBase.unselected_item_ink`
    * :attr:`~MainAppBase.vibration_volume`
    * :attr:`~MainAppBase.win_rectangle`

which app state variables are finally used by your app project is (fully data-driven) depending on the app state
:ref:`config-variables` detected in all the :ref:`config-files` that are found/available at run-time of your app. the
names of all the available application state variables can be determined with the main app helper method
:meth:`~MainAppBase.app_state_keys`.

if no config-file is provided then this package ensures at least the proper initialization of the following
app state variables:

    * :attr:`~MainAppBase.font_size`
    * :attr:`~MainAppBase.lang_code`
    * :attr:`~MainAppBase.light_theme`
    * :attr:`~MainAppBase.win_rectangle`

if your application is e.g. supporting a user-defined font size, using the provided/pre-defined app state variable
:attr:`~MainAppBase.font_size`, then it has to call the method :meth:`change_app_state` with the argument of
:paramref:`~MainAppBase.change_app_state.app_state_name` set to `font_size` every time when the user has changed the
font size of your app.

.. hint::
    the two built-in app state variables are :attr:`~MainAppBase.flow_id` and :attr:`~MainAppBase.flow_path` will be
    explained detailed in the next section.

the :meth:`~MainBaseApp.load_app_states` method is called on instantiation from the implemented main app class to
load the values of all app state variables from the :ref:`config-files`, and is then calling
:meth:~MainAppBase.setup_app_states` for pass them into their corresponding instance attributes.

use the main app instance attribute to read/get the actual value of a single app state variable. the actual values of
all app state variables as a dict is determining the method :meth:`~MainBaseApp.retrieve_app_states`, and can be saved
into the :ref:`config-files` for the next app run via the method :meth:`~MainBaseApp.save_app_states` - this could be
done e.g. after the app state has changed or at least on quiting the application.

always call the method :meth:`~MainBaseApp.change_app_state` to change an app state value to ensure:

    (1) the propagation to any duplicated (observable/bound) framework property and
    (2) the event notification of the related (optionally declared) main app instance method.


.. _app-state-constants:

app state constants
^^^^^^^^^^^^^^^^^^^

this module is also providing some pre-defined constants that can be optionally used in your application in relation to
the app states data store and for the app state config variables :attr:`~MainAppBase.app_state_version`,
:attr:`~MainAppBase.font_size` and :attr:`~MainAppBase.light_theme`:

    * :data:`APP_STATE_SECTION_NAME`
    * :data:`APP_STATE_VERSION_VAR_NAME`
    * :data:`MIN_FONT_SIZE`
    * :data:`MAX_FONT_SIZE`
    * :data:`THEME_LIGHT_BACKGROUND_COLOR`
    * :data:`THEME_LIGHT_FONT_COLOR`
    * :data:`THEME_DARK_BACKGROUND_COLOR`
    * :data:`THEME_DARK_FONT_COLOR`


app state events
^^^^^^^^^^^^^^^^

there are three types of notification events get fired in relation to the app state variables, using the method names:

* `on_<app_state_name>`: fired if the user of the app is changing the value of an app state variable.
* `on_<app_state_name>_save`: fired if an app state gets saved to the config file.
* `on_app_state_version_upgrade`: fired if the user upgrades a previously installed app to a higher version.

the method name of the app state change notification event consists of the prefix ``on_`` followed by the variable name
of the app state. so e.g. on a change of the `font_size` app state the notification event `on_font_size` will be
fired/called (if exists as a method of the main app instance). these events don't provide any event arguments.

the second event gets fired for each app state value just after the app states getting retrieved from the app class
instance, and before they get stored into the main config file. the method name of this event includes also the name of
the app state with the suffix `_save`, so e.g. for the app state `flow_id` the event method name will result in
:meth:`on_app_state_flow_id_save`. this event is providing one event argument with the value of the app state. if the
event method returns a value that is not `None` then this value will be stored/saved.

the third event gets fired on app startup when the app got upgraded to a higher version of the app state variable
APP_STATE_VERSION_VAR_NAME (`app_state_version`). it will be called providing the version number for each version to
upgrade, starting with the version of the previously installed main config file, until the upgrade version of the main
config file get reached. so if e.g. the previously installed app state version was 3 and the new version number is
6 then this event will be fired 3 times with the argument 3, 4 and 5. it can be used e.g. to change or add app state
variables or to adapt the app environment.


application flow
----------------

to control the current state and application/work flow (or context) of your application, and to persist it until the
next app start, :class:`MainBaseApp` provides two :ref:`app-state-variables`: :attr:`~MainAppBase.flow_id` to store the
currently working flow and :attr:`~MainAppBase.flow_path` to store the history of nested flows.

an application flow is represented by an id string that defines three things: (1) the action to enter into the flow, (2)
the data or object that gets currently worked on and (3) an optional key string that is identifying/indexing a widget or
data item of your application context/flow.

.. note::
    never concatenate a flow id string manually, use the :func:`id_of_flow` function instead.

the flow id is initially an empty string. as soon as the user is starting a new work flow or the current selection your
application should call the method :meth:`~MainBaseApp.change_flow` passing the flow id string into the
:paramref:`~MainAppBase.change_flow.new_flow_id` argument to change the app flow.

for more complex applications you can specify a path of nested flows. this flow path gets represented by the app state
variable :attr:`~MainAppBase.flow_path`, which is a list of flow id strings.

to enter into a deeper/nested flow you simply call :meth:`~MainBaseApp.change_flow` with one of the actions defined
in :data:`ACTIONS_EXTENDING_FLOW_PATH`.

to go back to a previous flow in the flow path call :meth:`~MainBaseApp.change_flow` passing one of the actions
defined in :data:`ACTIONS_REDUCING_FLOW_PATH`.


application flow change events
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

the flow actions specified by :data:`ACTIONS_CHANGING_FLOW_WITHOUT_CONFIRMATION` don't need a flow change confirmation
event handler:

* `'enter'` or `'leave'` extend/reduce the flow path.
* `'focus'` pass/change the input focus.
* `'suggest'` for autocompletion or other suggestions.

all other flow actions need to confirmed to be changed by :meth:`~MainAppBase.change_flow`, either by a custom flow
change confirmation method/event-handler or by declaring a popup class that has the same name returned by
:func:`flow_popup_class_name` if called with the new flow id.

the name of the flow change confirmation method that gets fired when the app want to change the flow (via the method
:meth:`~MainAppBase.change_flow`) depends on the new flow id and gets determined by the function
:func:`flow_change_confirmation_event_name`.

if the flow-specific change confirmation event handler does not exist or returns in a boolean `False` or `None` then
:meth:`~MainAppBase.on_flow_change` will be called. if this call also returns `False` then the action of the new flow id
will be searched within :data:`ACTIONS_CHANGING_FLOW_WITHOUT_CONFIRMATION` and if not found then the flow change will be
rejected and :meth:`~MainAppBase.change_flow` returns `False`.

if in contrary either the flow change confirmation event handler exists and does return `True` or
:meth:`~MainAppBase.on_flow_change` returns True or the flow action of the new flow id is in
:data:`ACTIONS_CHANGING_FLOW_WITHOUT_CONFIRMATION` then the flow id and path will be changed accordingly.

after the flow id/path change confirmation the method :meth:`~MainAppBase.change_flow` checks if the optional
event_kwargs key `changed_event_name` got specified and if yes then it calls this method.

finally, if a confirmed flow change results in a `'focus'` flow action then the event `on_flow_widget_focused` will be
fired. this event can be used by the GUI framework to set the focus to the widget associated with the new focus flow id.


key press events
----------------

to provide key press events to the applications that will use the new GUI framework you have to catch the key press
events of the framework, convert/normalize them and then call the :meth:`~MainAppBase.key_press_from_framework` with the
normalized modifiers and key args.

the :paramref:`~MainAppBase.key_press_from_framework.modifiers` arg is a string that can contain several of the
following sub-strings, always in the alphabetic order (like listed below):

    * Alt
    * Ctrl
    * Meta
    * Shift

the :paramref:`~MainAppBase.key_press_from_framework.key` arg is a string that is specifying the last pressed key. if
the key is not representing a single character but a command key, then `key` will be one of the following strings:

    * escape
    * tab
    * backspace
    * enter
    * del
    * enter
    * up
    * down
    * right
    * left
    * home
    * end
    * pgup
    * pgdown

on call of :meth:`~MainAppBase.key_press_from_framework` this method will try to dispatch the key press event to your
application. first it will check the app instance if it has declared a method with the name
`on_key_press_of_<modifiers>_<key>` and if so it will call this method.

if this method does return False (or any other value resulting in False) then method
:meth:`~MainAppBase.key_press_from_framework` will check for a method with the same name in lower-case and if exits it
will call this method.

if also the second method does return False, then it will try to call the event method `on_key_press` of the app
instance (if exists) with the modifiers and the key as arguments.

if the `on_key_press` method does also return False then :meth:`~MainAppBase.key_press_from_framework` will finally pass
the key press event to the original key press handler of the GUI framework for further processing.


integrate new gui framework
---------------------------

to integrate a new Python GUI framework you have to declare a new class that inherits from :class:`MainAppBase` and
implements at least the abstract method :meth:`~MainAppBase.init_app`.

additionally and to load the resources of the app (after the portions resources got loaded) the event `on_app_build` has
to be fired, executing the :meth:`MainAppBase.on_app_build` method. this could be done directly from within
:meth:`~MainAppBase.init_app` or by redirecting one of the events of the app instance of the GUI framework.

a minimal implementation of the :meth:`~MainAppBase.init_app` method would look like the following::

    def init_app(self):
        self.call_method('on_app_build')
        return None, None

most GUI frameworks are providing classes that need to be instantiated on application startup, like e.g. the instance of
the GUI framework app class, the root widget or layout of the main GUI framework window(s). to keep a reference to
these instances within your main app class you can use the attributes :attr:`~MainAppBase.framework_app`,
:attr:`~MainAppBase.framework_root` and :attr:`~MainAppBase.framework_win` of the class :class:`MainAppBase`.

the initialization of the attributes :attr:`~MainAppBase.framework_app`, :attr:`~MainAppBase.framework_root` and
:attr:`~MainAppBase.framework_win` is optional and can be done e.g. within :meth:`~MainAppBase.init_app` or in the
`on_app_build` application event fired later by the framework app instance.

.. note::
    if :attr:`~MainAppBase.framework_win` is set to a window instance, then the window instance has to provide a `close`
    method, which will be called automatically by the :meth:`~MainAppBase.stop_app`.

a typical implementation of a framework-specific main app class looks like::

    from new_gui_framework import NewFrameworkApp, MainWindowClassOfNewFramework

    class NewFrameworkMainApp(MainAppBase):
        def init_app(self):
            self.framework_app = NewFrameworkAppClass()
            self.framework_win = MainWindowClassOfNewFramework()

            # return callables to start/stop the event loop of the GUI framework
            return self.framework_app.start, self.framework_app.stop

in this example the `on_app_build` application event gets fired either from within the `start` method of the framework
app instance or by an event provided by the GUI framework.

:meth:`~MainAppBase.init_app` will be executed only once at the main app class instantiation. only the main app instance
has to initialize the GUI framework to prepare the app startup and has to return at least a callable to start the event
loop of the GUI framework.

.. hint::
    although not recommended because of possible namespace conflicts, one could e.g. alternatively integrate the
    framework application class as a mixin to the main app class.

to initiate the app startup the :meth:`~MainAppClass.run_app` method has to be called from the main module of your
app project. :meth:`~MainAppBase.run_app` will then start the GUI event loop by calling the first method that got
returned by :meth:`~MainAppBase.init_app`.


optional configuration and extension
------------------------------------

most of the base implementation helper methods can be overwritten by either the inheriting framework portion or directly
by user main app class.


base resources for your gui app
-------------------------------

this portion is also providing base resources for commonly used images and sounds.

the image file resources provided by this portion are taken from:

* `iconmonstr <https://iconmonstr.com/interface/>`_.


the sound files provides by this portion are taken from:

* `Erokia <https://freesound.org/people/Erokia/>`_ at `freesound.org <https://freesound.org>`_.
* `plasterbrain <https://freesound.org/people/plasterbrain/>`_ at `freesound.org <https://freesound.org>`_.

.. hint:: the i18n translation texts of this module are provided by the ae namespace portion :mod:`ae.gui_help`.

TODO:
implement OS-independent detection of dark/light screen mode and automatic notification on day/night mode switch.
- see https://github.com/albertosottile/darkdetect for MacOS, MSWindows and Ubuntu
- see https://github.com/kvdroid/Kvdroid/blob/master/kvdroid/tools/darkmode.py for Android
"""
import os
import re

from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

from ae.base import (                                                                                   # type: ignore
    CFG_EXT, INI_EXT, NAME_PARTS_SEP, UNSET,
    instantiate_config_parser, norm_name, norm_path, now_str, os_platform, snake_to_camel, stack_var)
from ae.files import RegisteredFile                                                                     # type: ignore
from ae.paths import (                                                                                  # type: ignore
    add_common_storage_paths, copy_file, copy_tree, normalize, path_folders, path_name, placeholder_path,
    Collector, FilesRegister, placeholder_key)
from ae.updater import MOVES_SRC_FOLDER_NAME, check_all                                                 # type: ignore
from ae.dynamicod import try_call                                                                       # type: ignore
from ae.i18n import (                                                                                   # type: ignore
    default_language, get_f_string, get_text, load_language_texts, register_translations_path)
from ae.core import DEBUG_LEVELS, registered_app_names                                                  # type: ignore
from ae.console import ConsoleApp                                                                       # type: ignore


__version__ = '0.3.88'


APP_STATE_SECTION_NAME = 'aeAppState'           #: config section name to store app state

#: config variable name to store the current application state version
APP_STATE_VERSION_VAR_NAME = 'app_state_version'

COLOR_BLACK = [0.009, 0.006, 0.003, 1.0]        #: != 0/1 to differentiate from framework pure black/white colors
COLOR_WHITE = [0.999, 0.996, 0.993, 1.0]
THEME_DARK_BACKGROUND_COLOR = COLOR_BLACK       #: dark theme background color in rgba(0.0 ... 1.0)
THEME_DARK_FONT_COLOR = COLOR_WHITE             #: dark theme font color in rgba(0.0 ... 1.0)
THEME_LIGHT_BACKGROUND_COLOR = COLOR_WHITE      #: light theme background color in rgba(0.0 ... 1.0)
THEME_LIGHT_FONT_COLOR = COLOR_BLACK            #: light theme font color in rgba(0.0 ... 1.0)

MIN_FONT_SIZE = 15.0                            #: minimum (s.a. :attr:`~ae.kivy_app.FrameworkApp.min_font_size`) and
MAX_FONT_SIZE = 99.0                            #: .. maximum font size in pixels


ACTIONS_EXTENDING_FLOW_PATH = ['add', 'confirm', 'edit', 'enter', 'open', 'show', 'suggest']
""" flow actions that are extending the flow path. """
ACTIONS_REDUCING_FLOW_PATH = ['close', 'leave']
""" flow actions that are shrinking/reducing the flow paths. """
ACTIONS_CHANGING_FLOW_WITHOUT_CONFIRMATION = ['', 'enter', 'focus', 'leave', 'suggest']
""" flow actions that are processed without the need to be confirmed. """
FLOW_KEY_SEP = ':'                              #: separator character between flow action/object and flow key

FLOW_ACTION_RE = re.compile("[a-z0-9]+")        #: regular expression detecting invalid characters in flow action string
FLOW_OBJECT_RE = re.compile("[A-Za-z0-9_]+")    #: regular expression detecting invalid characters in flow object string

HIDDEN_GLOBALS = (
    'ABC', 'abstractmethod', '_add_base_globals', 'Any', '__builtins__', '__cached__', 'Callable', '_d_', 'Dict',
    '__doc__', '__file__', 'List', '__loader__', 'module_globals', '__name__', 'Optional', '__package__', '__path__',
    '__spec__', 'Tuple', 'Type', '__version__')
""" tuple of global/module variable names that are hidden in :meth:`~MainAppBase.global_variables` """

PORTIONS_IMAGES = FilesRegister()               #: register of image files found in portions/packages at import time
PORTIONS_SOUNDS = FilesRegister()               #: register of sound files found in portions/packages at import time

USER_NAME_MAX_LEN = 12          #: maximal length of a username/id (restricting :attr:`~ae.console.ConsoleApp.user_id`)


AppStateType = Dict[str, Any]                   #: app state config variable type
EventKwargsType = Dict[str, Any]                #: change flow event kwargs type

ColorRGB = Union[Tuple[float, float, float], List[float]]           #: color red, green and blue parts
ColorRGBA = Union[Tuple[float, float, float, float], List[float]]   #: ink is rgb color and alpha
ColorOrInk = Union[ColorRGB, ColorRGBA]                             #: color or ink type


# check/install any outstanding updates or new app versions if imported directly from main app module
if stack_var('__name__') == '__main__':
    check_all()                                                                                 # pragma: no cover


def ensure_tap_kwargs_refs(init_kwargs: EventKwargsType, tap_widget: Any):
    """ ensure that the passed widget.__init__ kwargs dict contains a reference to itself within kwargs['tap_kwargs'].

    :param init_kwargs:         kwargs of the widgets __init__ method.
    :param tap_widget:          reference to the tap widget.

    this alternative version is only 10 % faster but much less clean than the current implementation::

        if 'tap_kwargs' not in init_kwargs:
            init_kwargs['tap_kwargs'] = {}
        tap_kwargs = init_kwargs['tap_kwargs']

        if 'tap_widget' not in tap_kwargs:
            tap_kwargs['tap_widget'] = tap_widget

        if 'popup_kwargs' not in tap_kwargs:
            tap_kwargs['popup_kwargs'] = {}
        popup_kwargs = tap_kwargs['popup_kwargs']
        if 'parent' not in popup_kwargs:
            popup_kwargs['parent'] = tap_kwargs['tap_widget']

    """
    init_kwargs['tap_kwargs'] = tap_kwargs = init_kwargs.get('tap_kwargs', {})
    tap_kwargs['tap_widget'] = tap_widget = tap_kwargs.get('tap_widget', tap_widget)
    tap_kwargs['popup_kwargs'] = popup_kwargs = tap_kwargs.get('popup_kwargs', {})
    popup_kwargs['parent'] = popup_kwargs.get('parent', tap_widget)


def flow_action(flow_id: str) -> str:
    """ determine the action string of a flow_id.

    :param flow_id:             flow id.
    :return:                    flow action string.
    """
    return flow_action_split(flow_id)[0]


def flow_action_split(flow_id: str) -> Tuple[str, str]:
    """ split flow id string into action part and the rest.

    :param flow_id:             flow id.
    :return:                    tuple of (flow action string, flow obj and key string)
    """
    idx = flow_id.find(NAME_PARTS_SEP)
    if idx != -1:
        return flow_id[:idx], flow_id[idx + 1:]
    return flow_id, ""


def flow_change_confirmation_event_name(flow_id: str) -> str:
    """ determine the name of the event method for the change confirmation of the passed flow_id.

    :param flow_id:             flow id.
    :return:                    tuple with 2 items containing the flow action and the object name (and id).
    """
    flow, _index = flow_key_split(flow_id)
    action, obj = flow_action_split(flow)
    return f'on_{obj}_{action}'


def flow_class_name(flow_id: str, name_suffix: str) -> str:
    """ determine class name for the given flow id and class name suffix.

    :param flow_id:             flow id.
    :param name_suffix:         class name suffix.
    :return:                    name of the class. please note that the flow action `open` will not be added
                                to the returned class name.
    """
    flow, _index = flow_key_split(flow_id)
    action, obj = flow_action_split(flow)
    if action == 'open':
        action = ''
    return f'{snake_to_camel(obj)}{action.capitalize()}{name_suffix}'


def flow_key(flow_id: str) -> str:
    """ return the key of a flow id.

    :param flow_id:             flow id string.
    :return:                    flow key string.
    """
    _action_object, index = flow_key_split(flow_id)
    return index


def flow_key_split(flow_id: str) -> Tuple[str, str]:
    """ split flow id into action with object and flow key.

    :param flow_id:             flow id to split.
    :return:                    tuple of (flow action and object string, flow key string).
    """
    idx = flow_id.find(FLOW_KEY_SEP)
    if idx != -1:
        return flow_id[:idx], flow_id[idx + 1:]
    return flow_id, ""


def flow_object(flow_id: str) -> str:
    """ determine the object string of the passed flow_id.

    :param flow_id:             flow id.
    :return:                    flow object string.
    """
    return flow_action_split(flow_key_split(flow_id)[0])[1]


def flow_path_id(flow_path: List[str], path_index: int = -1) -> str:
    """ determine the flow id of the newest/last entry in the flow_path.

    :param flow_path:           flow path to get the flow id from.
    :param path_index:          index in the flow_path.
    :return:                    flow id string or empty string if flow path is empty or index does not exist.
    """
    if len(flow_path) >= (abs(path_index) if path_index < 0 else path_index + 1):
        return flow_path[path_index]
    return ''


def flow_path_strip(flow_path: List[str]) -> List[str]:
    """ return copy of passed flow_path with all non-enter actions stripped from the end.

    :param flow_path:           flow path list to strip.
    :return:                    stripped flow path copy.
    """
    deep = len(flow_path)
    while deep and flow_action(flow_path_id(flow_path, path_index=deep - 1)) != 'enter':
        deep -= 1
    return flow_path[:deep]


def flow_popup_class_name(flow_id: str) -> str:
    """ determine name of the Popup class for the given flow id.

    :param flow_id:             flow id.
    :return:                    name of the Popup class. please note that the action `open` will not be added
                                to the returned class name.
    """
    return flow_class_name(flow_id, 'Popup')


def id_of_flow(action: str, obj: str = "", key: str = "") -> str:
    """ create flow id string.

    :param action:              flow action string.
    :param obj:                 flow object (defined by app project).
    :param key:                 flow index/item_id/field_id/... (defined by app project).
    :return:                    complete flow_id string.
    """
    assert action == '' or FLOW_ACTION_RE.fullmatch(action), \
        f"flow action only allows lowercase letters and digits: got '{action}'"
    assert obj == '' or FLOW_OBJECT_RE.fullmatch(obj), \
        f"flow object only allows letters, digits and underscores: got '{obj}'"
    cid = f'{action}{NAME_PARTS_SEP if action and obj else ""}{obj}'
    if key:
        cid += f'{FLOW_KEY_SEP}{key}'
    return cid


def register_package_images():
    """ call from module scope of the package to register/add image/img resources path.

    no parameters needed because we use here :func:`~ae.base.stack_var` helper function to determine the
    module file path via the `__file__` module variable of the caller module in the call stack. in this call
    we have to overwrite the default value (:data:`~ae.base.SKIPPED_MODULES`) of the
    :paramref:`~ae.base.stack_var.skip_modules` parameter to not skip ae portions that are providing
    package resources and are listed in the :data:`~ae.base.SKIPPED_MODULES`, like e.g. :mod:`ae.gui_app` and
    :mod:`ae.gui_help` (passing empty string '' to overwrite default skip list).
    """
    global PORTIONS_IMAGES

    package_path = os.path.dirname(norm_path(stack_var('__file__', '')))
    search_path = os.path.join(package_path, 'img/**')
    PORTIONS_IMAGES.add_paths(search_path)


def register_package_sounds():
    """ call from module scope of the package to register/add sound file resources.

    no parameters needed because we use here :func:`~ae.base.stack_var` helper function to determine the
    module file path via the `__file__` module variable of the caller module in the call stack. in this call
    we have to overwrite the default value (:data:`~ae.base.SKIPPED_MODULES`) of the
    :paramref:`~ae.base.stack_var.skip_modules` parameter to not skip ae portions that are providing
    package resources and are listed in the :data:`~ae.base.SKIPPED_MODULES`, like e.g. :mod:`ae.gui_app`
    :mod:`ae.gui_help` (passing empty string '' to overwrite default skip list).
    """
    global PORTIONS_SOUNDS

    package_path = os.path.dirname(norm_path(stack_var('__file__', '')))
    search_path = os.path.join(package_path, 'snd/**')
    PORTIONS_SOUNDS.add_paths(search_path)


def replace_flow_action(flow_id: str, new_action: str):
    """ replace action in given flow id.

    :param flow_id:             flow id.
    :param new_action:          action to be set/replaced within passed flow id.
    :return:                    flow id with new action and object/key from passed flow id.
    """
    return id_of_flow(new_action, *flow_key_split(flow_action_split(flow_id)[1]))


def update_tap_kwargs(widget: Any, popup_kwargs: Optional[EventKwargsType] = None, **tap_kwargs) -> EventKwargsType:
    """ update or simulate widget's tap_kwargs property and return the updated dictionary (for kv rule of tap_kwargs).

    :param widget:              widget with tap_kwargs property to be updated.
    :param popup_kwargs:        dict with items to update popup_kwargs key of tap_kwargs
    :param tap_kwargs:          additional tap_kwargs items to update.
    :return:
    """
    handle = dict(tap_kwargs=widget.tap_kwargs) if hasattr(widget, 'tap_kwargs') else {}
    ensure_tap_kwargs_refs(handle, widget)
    new_kwargs = handle['tap_kwargs']
    if popup_kwargs:
        new_kwargs['popup_kwargs'].update(popup_kwargs)
    if tap_kwargs:
        new_kwargs.update(tap_kwargs)
    return new_kwargs


class MainAppBase(ConsoleApp, ABC):
    """ abstract base class to implement a GUIApp-conform app class """
    # app states
    app_state_version: int = 0                              #: version number of the app state variables in <config>.ini

    flow_id: str = ""                                       #: id of the current app flow (entered by the app user)
    flow_path: List[str]                                    #: list of flow ids, reflecting recent user actions
    flow_id_ink: ColorOrInk = [0.99, 0.99, 0.69, 0.69]      #: rgba color for flow id / drag&drop node placeholder
    flow_path_ink: ColorOrInk = [0.99, 0.99, 0.39, 0.48]    #: rgba color for flow_path/drag&drop item placeholder

    font_size: float = 21.0                                 #: font size used toolbar and flow screens
    lang_code: str = ""                                     #: optional language code (e.g. 'es_ES' for Spanish)
    light_theme: bool = False                               #: True=light theme/background, False=dark theme

    selected_item_ink: ColorOrInk = [0.69, 1.0, 0.39, 0.18]  #: rgba color for list items (selected)
    unselected_item_ink: ColorOrInk = [0.39, 0.39, 0.39, 0.18]  #: rgba color for list items (unselected)

    sound_volume: float = 0.12                              #: sound volume of current app (0.0=mute, 1.0=max)
    vibration_volume: float = 0.3                           #: vibration volume of current app (0.0=mute, 1.0=max)

    win_rectangle: tuple = (0, 0, 1920, 1080)               #: window coordinates (x, y, width, height)

    # optional generic run-time shortcut references
    framework_app: Any = None                               #: app class instance of the used GUI framework
    framework_win: Any = None                               #: window instance of the used GUI framework
    framework_root: Any = None                              #: app root layout widget

    # optional app resources caches
    image_files: Optional[FilesRegister] = None             #: image/icon files
    sound_files: Optional[FilesRegister] = None             #: sound/audio files

    def __init__(self, **console_app_kwargs):
        """ create instance of app class.

        :param console_app_kwargs:  kwargs to be passed to the __init__ method of :class:`~ae.console_app.ConsoleApp`.
        """
        self._exit_code: int = 0                            #: init by stop_app() and passed onto OS by run_app()
        self._last_focus_flow_id: str = id_of_flow('')      #: id of the last valid focused window/widget/item/context

        self._start_event_loop: Optional[Callable]          #: callable to start event loop of GUI framework
        self._stop_event_loop: Optional[Callable]           #: callable to start event loop of GUI framework

        self.flow_path = []         # init for literal type recognition - will be overwritten by setup_app_states()

        add_common_storage_paths()  # determine platform specific path placeholders, like e.g. {pictures}, {downloads}..

        super().__init__(**console_app_kwargs)

        self.call_method('on_app_init')

        self._start_event_loop, self._stop_event_loop = self.init_app()

        self.load_app_states()

    def _init_default_user_cfg_vars(self):
        super()._init_default_user_cfg_vars()
        self.user_specific_cfg_vars |= {
            (APP_STATE_SECTION_NAME, 'flow_id'),
            (APP_STATE_SECTION_NAME, 'flow_id_ink'),
            (APP_STATE_SECTION_NAME, 'flow_path'),
            (APP_STATE_SECTION_NAME, 'flow_path_ink'),
            (APP_STATE_SECTION_NAME, 'font_size'),
            (APP_STATE_SECTION_NAME, 'lang_code'),
            (APP_STATE_SECTION_NAME, 'light_theme'),
            (APP_STATE_SECTION_NAME, 'selected_item_ink'),
            (APP_STATE_SECTION_NAME, 'sound_volume'),
            (APP_STATE_SECTION_NAME, 'unselected_item_ink'),
            (APP_STATE_SECTION_NAME, 'vibration_volume'),
            (APP_STATE_SECTION_NAME, 'win_rectangle'),
        }

    @abstractmethod
    def init_app(self, framework_app_class: Any = None) -> Tuple[Optional[Callable], Optional[Callable]]:
        """ initialize framework app instance and root window/layout, return GUI event loop start/stop methods.

        :param framework_app_class: class to create app instance (optionally extended by app project).
        :return:                    tuple of two callable, the 1st to start and the 2nd to stop/exit
                                    the GUI event loop.
        """

    def app_state_keys(self) -> Tuple[str, ...]:
        """ determine current config variable names/keys of the app state section :data:`APP_STATE_SECTION_NAME`.

        :return:                tuple of all app state item keys (config variable names).
        """
        return self.cfg_section_variable_names(APP_STATE_SECTION_NAME)

    @staticmethod
    def backup_config_resources() -> str:   # pragma: no cover
        """ backup config files and image/sound/translations resources to {ado}<now_str>.

        config files are collected from {ado}, {usr} or {cwd} (the first found file name only - see/sync-with
        :meth:`ae.console.ConsoleApp.add_cfg_files`).

        resources are copied from {ado} or {cwd} (only the first found resources root path).
        """
        backup_root = normalize("{ado}") + now_str(sep="_")
        os.makedirs(backup_root)

        coll = Collector()
        app_configs = tuple(ana + ext for ana in registered_app_names() for ext in (INI_EXT, CFG_EXT))
        coll.collect("{ado}", "{usr}", "{cwd}", append=app_configs, only_first_of=())
        for file in coll.files:
            copy_file(file, os.path.join(backup_root, placeholder_key(file) + "_" + os.path.basename(file)))

        coll = Collector(path_scanner=path_folders)
        coll.collect("{ado}", "{cwd}", append=('img', 'loc', 'snd'), only_first_of=())
        for path in coll.paths:
            copy_tree(path, os.path.join(backup_root, placeholder_key(path) + "_" + os.path.basename(path)))

        return backup_root

    def change_app_state(self, app_state_name: str, state_value: Any, send_event: bool = True, old_name: str = ''):
        """ change app state to :paramref:`~change_app_state.state_value` in self.<app_state_name> and app_states dict.

        :param app_state_name:  name of the app state to change.
        :param state_value:     new value of the app state to change.
        :param send_event:      pass False to prevent send/call of the main_app.on_<app_state_name> event.
        :param old_name:        pass to add state to the main config file: old state name to rename/migrate or
                                :data:`~ae.base.UNSET` to only add a new app state variable with the name specified in
                                :paramref:`~change_app_state.app_state_name`.
        """
        self.vpo(f"MainAppBase.change_app_state({app_state_name}, {state_value!r}, {send_event}, {old_name!r})"
                 f" flow={self.flow_id} last={self._last_focus_flow_id} path={self.flow_path}")

        self.change_observable(app_state_name, state_value, is_app_state=True)

        if old_name or old_name is UNSET:
            self.set_var(app_state_name, state_value, section=APP_STATE_SECTION_NAME, old_name=old_name or "")

        if send_event:
            self.call_method('on_' + app_state_name)

    def change_observable(self, name: str, value: Any, is_app_state: bool = False):
        """ change observable attribute/member/property in framework_app instance (and shadow copy in main app).

        :param name:            name of the observable attribute/member or key of an observable dict property.
        :param value:           new value of the observable.
        :param is_app_state:    pass True for an app state observable.
        """
        setattr(self, name, value)
        if is_app_state:
            if hasattr(self.framework_app, 'app_states'):       # has observable DictProperty duplicates
                self.framework_app.app_states[name] = value
            name = 'app_state_' + name
        if hasattr(self.framework_app, name):                   # has observable attribute duplicate
            setattr(self.framework_app, name, value)

    def change_flow(self, new_flow_id: str, **event_kwargs) -> bool:
        """ try to change/switch the current flow id to the value passed in :paramref:`~change_flow.new_flow_id`.

        :param new_flow_id:     new flow id (maybe overwritten by flow change confirmation event handlers by assigning a
                                flow id to event_kwargs['flow_id']).

        :param event_kwargs:    optional args to pass additional data or info onto and from the flow change confirmation
                                event handler.

                                the following keys are currently supported/implemented by this module/portion
                                (additional keys can be added by the modules/apps using this method):

                                * `changed_event_name`: optional main app event method name to be called if the flow got
                                  confirmed and changed.
                                * `count`: optional number used to render a pluralized help text for this flow change
                                  (this number gets also passed to the help text formatter by/in
                                  :meth:`~ae.gui_help.HelpAppBase.change_flow`).
                                * `edit_widget`: optional widget instance for edit/input.
                                * `flow_id`: process :attr:`~MainAppBase.flow_path` as specified by the
                                  :paramref:`~change_flow.new_flow_id` argument, but then overwrite this flow id with
                                  this event arg value to set :attr:`~MainAppBase.flow_id`.
                                * `popup_kwargs`: optional dict passed to the Popup `__init__` method, like e.g.
                                  dict(parent=parent_widget_of_popup, data=...).
                                * `popups_to_close`: optional sequence of widgets to be closed by this method after flow
                                  change got confirmed. to prevent weakref-errors the `attach_to` attribute of each
                                  widget will additionally be reset to None.
                                * 'reset_last_focus_flow_id': pass `True` to reset the last focus flow id, pass `False`
                                  or `None` to ignore the last focus id (and not use to set flow id) or pass a flow id
                                  string value to change the last focus flow id to the passed value.
                                * `tap_widget`: optional tapped button widget instance (initiating this flow change).

                                some of these keys get specified directly on the call of this method, e.g. via
                                :attr:`~.kivy_app.FlowButton.tap_kwargs` or :attr:`~.kivy_app.FlowToggler.tap_kwargs`,
                                where others get added by the flow change confirmation handlers/callbacks.

        :return:                True if flow got confirmed by a declared custom flow change confirmation event handler
                                (either event method or Popup class) of the app and changed accordingly, else False.

                                some flow actions are handled internally independent of the return value of a
                                custom event handler, like e.g. `'enter'` or `'leave'` will always extend or reduce the
                                flow path and the action `'focus'` will give the indexed widget the input focus (these
                                exceptions are configurable via :data:`ACTIONS_CHANGING_FLOW_WITHOUT_CONFIRMATION`).
        """
        msg = f" MainAppBase.change_flow({new_flow_id!r}, {event_kwargs}) id={self.flow_id!r} path={self.flow_path}"
        self.vpo("CHECK   " + msg)

        action = flow_action(new_flow_id)
        if not self.call_method(flow_change_confirmation_event_name(new_flow_id), flow_key(new_flow_id), event_kwargs) \
                and not self.on_flow_change(new_flow_id, event_kwargs) \
                and action not in ACTIONS_CHANGING_FLOW_WITHOUT_CONFIRMATION:
            self.vpo("REJECTED" + msg)
            return False

        has_flow_focus = flow_action(self.flow_id) == 'focus'
        empty_flow = id_of_flow('')
        if action in ACTIONS_EXTENDING_FLOW_PATH:
            if action == 'edit' and self.flow_path_action() == 'edit' \
                    and flow_key_split(self.flow_path[-1])[0] == flow_key_split(new_flow_id)[0]:
                self.flow_path.pop()
            self.flow_path.append(new_flow_id)
            self.change_app_state('flow_path', self.flow_path)
            flow_id = empty_flow if action == 'enter' else new_flow_id
        elif action in ACTIONS_REDUCING_FLOW_PATH:
            # dismiss gets sent sometimes twice (e.g. on heavy double-clicking on drop-down-open-buttons)
            # .. therefore prevent run-time error
            if not self.flow_path:
                self.dpo("IGNORED reduce on empty flow path" + msg)
                return False
            ended_flow_id = self.flow_path.pop()
            self.change_app_state('flow_path', self.flow_path)
            if action == 'leave':
                flow_id = replace_flow_action(ended_flow_id, 'focus')
            else:
                flow_id = self.flow_id if has_flow_focus else empty_flow
        else:
            flow_id = new_flow_id if action == 'focus' else (self.flow_id if has_flow_focus else empty_flow)

        popups_to_close = event_kwargs.get('popups_to_close', ())
        for widget in reversed(popups_to_close):
            widget.close()
            if hasattr(widget, 'attach_to'):
                widget.attach_to = None     # mainly for DropDown widgets to prevent weakref-error/-exception

        if action not in ACTIONS_REDUCING_FLOW_PATH or not has_flow_focus:
            flow_id = event_kwargs.get('flow_id', flow_id)  # update flow_id from event_kwargs
        if 'reset_last_focus_flow_id' in event_kwargs:
            last_flow_id = event_kwargs['reset_last_focus_flow_id']
            if last_flow_id is True:
                self._last_focus_flow_id = empty_flow
            elif isinstance(last_flow_id, str):
                self._last_focus_flow_id = last_flow_id
        elif flow_id == empty_flow and self._last_focus_flow_id and action not in ACTIONS_EXTENDING_FLOW_PATH:
            flow_id = self._last_focus_flow_id
        self.change_app_state('flow_id', flow_id)

        changed_event_name = event_kwargs.get('changed_event_name', '')
        if changed_event_name:
            self.call_method(changed_event_name)

        if flow_action(flow_id) == 'focus':
            self.call_method('on_flow_widget_focused')
            self._last_focus_flow_id = flow_id

        self.vpo("CHANGED " + msg + f"+path={self.flow_path} args={event_kwargs} last_foc='{self._last_focus_flow_id}'")

        return True

    @staticmethod
    def class_by_name(class_name: str) -> Optional[Type]:
        """ search class name in framework modules as well as in app main.py to return class object.

        :param class_name:      name of the class.
        :return:                class object with the specified class name or :data:`~ae.base.UNSET` if not found.
        """
        return stack_var(class_name)

    @staticmethod
    def dpi_factor() -> float:
        """ dpi scaling factor - override if the used GUI framework supports dpi scaling. """
        return 1.0

    def close_popups(self):
        """ close all opened popups (starting with the topmost popup). """
        for popup in self.popups_opened():
            popup.close()

    def find_image(self, image_name: str, height: float = 32.0, light_theme: bool = True) -> Optional[RegisteredFile]:
        """ find best fitting image in img app folder (see also :meth:`~MainAppBase.img_file` for easier usage).

        :param image_name:      name of the image (file name without extension).
        :param height:          preferred height of the image/icon.
        :param light_theme:     preferred theme (dark/light) of the image.
        :return:                image file object (RegisteredFile/CachedFile) if found else None.
        """
        def property_matcher(file) -> bool:
            """ find images with matching theme.

            :param file:        RegisteredFile instance.
            :return:            True if theme is matching.
            """
            return bool(file.properties.get('light', 0)) == light_theme

        def file_sorter(file) -> float:
            """ sort images files by height delta.

            :param file:        RegisteredFile instance.
            :return:            height delta.
            """
            return abs(file.properties.get('height', -MAX_FONT_SIZE) - height)

        if self.image_files:
            return self.image_files(image_name, property_matcher=property_matcher, file_sorter=file_sorter)
        return None

    def find_sound(self, sound_name: str) -> Optional[RegisteredFile]:
        """ find sound by name.

        :param sound_name:      name of the sound to search for.
        :return:                cached sound file object (RegisteredFile/CachedFile) if sound name was found else None.
        """
        if self.sound_files:    # prevent error on app startup (setup_app_states() called before load_images()
            return self.sound_files(sound_name)
        return None

    def find_widget(self, match: Callable[[Any], bool]) -> Optional[Any]:
        """ search the widget tree returning the first matching widget in reversed z-order (top-most first).

        :param match:           callable called with the widget as argument, returning True if widget matches.
        :return:                first found widget in reversed z-order (top-most widget first).
        """
        def child_wid(children):
            """ bottom up search within children for a widget with matching attribute name and value. """
            for widget in reversed(children):
                found = child_wid(self.widget_children(widget))
                if found:
                    return found
                if match(widget):
                    return widget
            return None

        return child_wid(self.widget_children(self.framework_win))

    def flow_path_action(self, flow_path: Optional[List[str]] = None, path_index: int = -1) -> str:
        """ determine the action of the last (newest) entry in the flow_path.

        :param flow_path:       optional flow path to get the flow action from (default=self.flow_path).
        :param path_index:      optional index in the flow_path (default=-1).
        :return:                flow action string or empty string if flow path is empty or index does not exist.
        """
        if flow_path is None:
            flow_path = self.flow_path
        return flow_action(flow_path_id(flow_path=flow_path, path_index=path_index))

    def global_variables(self, **patches) -> Dict[str, Any]:
        """ determine generic/most-needed global variables to evaluate expressions/macros.

        :param patches:         dict of variable names and values to add/replace on top of generic globals.
        :return:                dict of global variables patched with :paramref:`~global_variables.patches`.
        """
        glo_vars = {k: v for k, v in module_globals.items() if k not in HIDDEN_GLOBALS}
        glo_vars.update((k, v) for k, v in globals().items() if k not in HIDDEN_GLOBALS)
        glo_vars['app'] = self.framework_app
        glo_vars['main_app'] = self
        glo_vars['_add_base_globals'] = ""          # instruct ae.dynamicod.try_eval to add generic/base globals

        self.vpo(f"MainAppBase.global_variables patching {patches} over {glo_vars}")

        glo_vars.update(**patches)

        return glo_vars

    def img_file(self, image_name: str, font_size: Optional[float] = None, light_theme: Optional[bool] = None) -> str:
        """ shortcutting :meth:`~MainAppBase.find_image` method w/o bound property to get image file path.

        :param image_name:      image name (file name stem).
        :param font_size:       optional font size in pixels.
        :param light_theme:     optional theme (True=light, False=dark).
        :return:                file path of image file or empty string if image file not found.
        """
        if font_size is None:
            font_size = self.font_size
        if light_theme is None:
            light_theme = self.light_theme

        img_obj = self.find_image(image_name, height=font_size, light_theme=light_theme)
        if img_obj:
            return img_obj.path
        return ''

    def key_press_from_framework(self, modifiers: str, key: str) -> bool:
        """ dispatch key press event, coming normalized from the UI framework.

        :param modifiers:       modifier keys.
        :param key:             key character.
        :return:                True if key got consumed/used else False.
        """
        self.vpo(f"MainAppBase.key_press_from_framework({modifiers}+{key})")
        event_name = f'on_key_press_of_{modifiers}_{key}'
        en_lower = event_name.lower()
        if self.call_method(en_lower):
            return True
        if event_name != en_lower and self.call_method(event_name):
            return True
        # call default handler; pass lower key code (enaml/Qt sends upper-case key code if Shift modifier is pressed)
        return self.call_method('on_key_press', modifiers, key.lower()) or False

    def load_app_states(self):
        """ load application state from the config files to prepare app.run_app """
        app_states = {}
        for key in self.app_state_keys():
            pre = f"   #  app state '{key}' "
            if not hasattr(self, key):
                self.dpo(f"{pre}ignored because it is not declared as MainAppBase attribute")
                continue

            type_class = type(getattr(self, key))
            value = self.get_var(key, section=APP_STATE_SECTION_NAME)
            if not isinstance(value, type_class):   # type mismatch - try to autocorrect
                self.dpo(f"{pre}type mismatch: attr={type_class} config-var={type(value)}")
                corr_val = try_call(type_class, value, ignored_exceptions=(Exception, TypeError, ValueError))
                if corr_val is UNSET:
                    self.po(f"{pre}type mismatch in '{value}' could not be corrected to {type_class}")
                else:
                    value = corr_val

            app_states[key] = value

        self.setup_app_states(app_states)

    def load_images(self):
        """ load images from app folder img. """
        file_reg = FilesRegister()
        file_reg.add_register(PORTIONS_IMAGES)
        file_reg.add_paths('img/**')
        file_reg.add_paths('{ado}/img/**')
        self.image_files = file_reg

    def load_sounds(self):
        """ load audio sounds from app folder snd. """
        file_reg = FilesRegister()
        file_reg.add_register(PORTIONS_SOUNDS)
        file_reg.add_paths('snd/**')
        file_reg.add_paths('{ado}/snd/**')
        self.sound_files = file_reg

    def load_translations(self, lang_code: str):
        """ load translation texts for the passed language code.

        :param lang_code:       the new language code to be set (passed as flow key). empty on first app run/start.
        """
        is_empty = not lang_code
        old_lang = self.lang_code

        lang_code = load_language_texts(lang_code)
        self.change_app_state('lang_code', lang_code)

        if is_empty or lang_code != old_lang:
            default_language(lang_code)
            self.set_var('lang_code', lang_code, section=APP_STATE_SECTION_NAME)  # add optional app state var to config

    def mix_background_ink(self):
        """ remix background ink if one of the basic back colours change. """
        self.framework_app.mixed_back_ink = [sum(_) / len(_) for _ in zip(
            self.flow_id_ink, self.flow_path_ink, self.selected_item_ink, self.unselected_item_ink)]

    def on_app_build(self):
        """ default/fallback flow change confirmation event handler. """
        self.vpo("MainAppBase.on_app_build default/fallback event handler called")

    def on_app_exit(self):
        """ default/fallback flow change confirmation event handler. """
        self.vpo("MainAppBase.on_app_exit default/fallback event handler called")

    def on_app_init(self):
        """ default/fallback flow change confirmation event handler. """
        self.vpo("MainAppBase.on_app_init default/fallback event handler called")

    def on_app_quit(self):
        """ default/fallback flow change confirmation event handler. """
        self.vpo("MainAppBase.on_app_quit default/fallback event handler called")

    def on_app_run(self):
        """ default/fallback flow change confirmation event handler. """
        self.vpo("MainAppBase.on_app_run default/fallback event handler called")

    def on_app_start(self):
        """ default/fallback flow change confirmation event handler, used to load app resources. """
        self.vpo("MainAppBase.on_app_start default/fallback event handler called - loading app resources")

        self.load_images()

        self.load_sounds()

        register_translations_path()
        register_translations_path("{ado}")
        self.load_translations(self.lang_code)

    def on_app_stop(self):
        """ default/fallback flow change confirmation event handler. """
        self.vpo("MainAppBase.on_app_stop default/fallback event handler called")

    def on_debug_level_change(self, level_name: str, _event_kwargs: EventKwargsType) -> bool:
        """ debug level app state change flow change confirmation event handler.

        :param level_name:      the new debug level name to be set (passed as flow key).
        :param _event_kwargs:   unused event kwargs.
        :return:                True to confirm the debug level change.
        """
        debug_level = next(num for num, name in DEBUG_LEVELS.items() if name == level_name)
        self.vpo(f"MainAppBase.on_debug_level_change to {level_name} -> {debug_level}")
        self.set_opt('debug_level', debug_level)
        return True

    def on_flow_change(self, flow_id: str, event_kwargs: EventKwargsType) -> bool:
        """ checking if exists a Popup class for the new flow and if yes then open it.

        :param flow_id:         new flow id.
        :param event_kwargs:    optional event kwargs; the optional item with the key `popup_kwargs`
                                will be passed onto the `__init__` method of the found Popup class.
        :return:                True if Popup class was found and displayed.

        this method is mainly used as the last fallback clicked flow change confirmation event handler of a FlowButton.
        """
        class_name = flow_popup_class_name(flow_id)
        self.vpo(f"MainAppBase.on_flow_change '{flow_id}' {event_kwargs} lookup={class_name}")

        if flow_id:
            popup_class = self.class_by_name(class_name)
            if popup_class:
                popup_kwargs = event_kwargs.get('popup_kwargs', {})
                self.open_popup(popup_class, **popup_kwargs)
                return True
        return False

    def on_flow_id_ink(self):
        """ redirect flow id back ink app state color change event handler to actualize mixed_back_ink. """
        self.mix_background_ink()

    def on_flow_path_ink(self):
        """ redirect flow path back ink app state color change event handler to actualize mixed_back_ink. """
        self.mix_background_ink()

    @staticmethod
    def on_flow_popup_close(_flow_key: str, _event_kwargs: EventKwargsType) -> bool:
        """ default popup close handler of FlowPopup widget, ensuring update of :attr:`flow_path`.

        :param _flow_key:       unused flow key.
        :param _event_kwargs:   unused popup args.
        :return:                always returning True.
        """
        return True

    def on_lang_code_change(self, lang_code: str, _event_kwargs: EventKwargsType) -> bool:
        """ language app state change flow change confirmation event handler.

        :param lang_code:       the new language code to be set (passed as flow key). empty on first app run/start.
        :param _event_kwargs:   unused event kwargs.
        :return:                True to confirm the language change.
        """
        self.vpo(f"MainAppBase.on_lang_code_change to {lang_code}")
        self.load_translations(lang_code)
        return True

    def on_light_theme_change(self, _flow_key: str, event_kwargs: EventKwargsType) -> bool:
        """ app theme app state change flow change confirmation event handler.

        :param _flow_key:       flow key.
        :param event_kwargs:    event kwargs with key `'light_theme'` containing True|False for light|dark theme.
        :return:                True to confirm change of flow id.
        """
        light_theme: bool = event_kwargs['light_theme']
        self.vpo(f"MainAppBase.on_light_theme_change to {light_theme}")
        self.change_app_state('light_theme', light_theme)
        return True

    def on_selected_item_ink(self):
        """ redirect selected item back ink app state color change event handler to actualize mixed_back_ink. """
        self.mix_background_ink()

    def on_unselected_item_ink(self):
        """ redirect unselected item back ink app state color change event handler to actualize mixed_back_ink. """
        self.mix_background_ink()

    def on_user_add(self, user_name: str, event_kwargs: Dict[str, Any]) -> bool:
        """ called on close of UserNameEditorPopup to check user input and create/register the current os user.

        :param user_name:       new user id.
        :param event_kwargs:    optionally pass True in the `unique_user_name` key to prevent duplicate usernames.
        :return:                True if user got registered else False.
        """
        if not user_name:
            self.show_message(get_text("please enter your user or nick name"))
            return False
        if len(user_name) > USER_NAME_MAX_LEN:
            self.show_message(get_f_string(
                "please shorten your user name to not more than {USER_NAME_MAX_LEN} characters", glo_vars=globals()))
            return False

        chk_id = norm_name(user_name)
        if user_name != chk_id:
            self.show_message(get_f_string(
                "please remove spaces and the characters "
                "'{''.join(ch for ch in user_name if ch not in chk_id)}' from your user name",
                glo_vars=locals().copy()))
            return False

        if self.user_id in self.registered_users:
            if event_kwargs.get('unique_user_name', False) and \
                    any(usr for usr in self.registered_users.values() if usr.get('user_name') == user_name):
                self.show_message(get_f_string("user name {user_name} already exists", glo_vars=locals().copy()))
                return False

            idx = 1
            while True:
                user_id = f'usr_id_{idx}'
                if user_id not in self.registered_users:
                    break
                idx += 1
            self.user_id: str = user_id

        user_data = dict(user_name=user_name)
        self.register_user(**user_data)

        return True

    def play_beep(self):
        """ make a short beep sound, should be overwritten by GUI framework. """
        self.po(chr(7), "MainAppBase.BEEP")

    def play_sound(self, sound_name: str):
        """ play audio/sound file, should be overwritten by GUI framework.

        :param sound_name:  name of the sound to play.
        """
        self.po(f"MainAppBase.play_sound {sound_name}")

    def play_vibrate(self, pattern: Tuple = (0.0, 0.09, 0.21, 0.3, 0.09, 0.09, 0.21, 0.09)):
        """ play vibrate pattern, should be overwritten by GUI framework.

        :param pattern:     optional tuple of pause and vibrate time sequence - use error pattern if not passed.
        """
        self.po(f"MainAppBase.play_vibrate {pattern}")

    def open_popup(self, popup_class: Type, **popup_kwargs) -> Any:
        """ open Popup/DropDown, calling the `open`/`show` method of the instance created from the passed popup class.

        :param popup_class:     class of the Popup/DropDown widget/window.
        :param popup_kwargs:    args to instantiate and show/open the popup.
        :return:                created and displayed/opened popup class instance.

        .. hint::
            overwrite this method if framework is using different method to open popup window or if
            a widget in the Popup/DropDown need to get the input focus.
        """
        self.dpo(f"MainAppBase.open_popup {popup_class} {popup_kwargs}")
        popup_instance = popup_class(**popup_kwargs)
        open_method = getattr(popup_instance, 'open', getattr(popup_instance, 'show', None))
        if callable(open_method):
            open_method()
        return popup_instance

    def popups_opened(self, classes: Tuple = ()) -> List:
        """ determine all popup-like container widgets that are currently opened.

        :param classes:         optional class filter - if not passed then only the widgets underneath win/root with an
                                `open` method will be added. pass tuple to restrict found popup widgets to certain
                                classes. like e.g. by passing (Popup, DropDown, FlowPopup) to get all popups of an
                                ae/Kivy app.
        :return:                list of opened/visible popup class instances that are children of either the
                                root layout or the app window, ordered by their z-coordinate (most front widget last).
        """
        filter_func = (lambda _wg: isinstance(_wg, classes)) if classes else \
            (lambda _wg: callable(getattr(_wg, 'open', None)))

        popups = []
        for wid in self.framework_win.children + self.framework_root.children:
            if filter_func(wid):
                popups.append(wid)

        return popups

    def retrieve_app_states(self) -> AppStateType:
        """ determine the state of a running app from the main app instance and return it as dict.

        :return:                dict with all app states available in the config files.
        """
        app_states = {}
        for key in self.app_state_keys():
            app_states[key] = getattr(self, key)

        self.dpo(f"MainAppBase.retrieve_app_states {app_states}")
        return app_states

    def run_app(self):
        """ startup main and framework applications. """
        self.dpo(f"MainAppBase.run_app {self.app_name}")

        self.call_method('on_app_start')

        super().run_app()                               # parse command line arguments into config options

        self.call_method('on_app_run')

        if self._start_event_loop:                      # not needed for SubApp or additional Window instances
            try:
                self._start_event_loop()
            finally:
                self.call_method('on_app_quit')
                self.shutdown(self._exit_code or None)  # don't call sys.exit() for zero exit code

    def save_app_states(self) -> str:
        """ save app state in config file.

        :return:                empty string if app status could be saved into config files else error message.
        """
        err_msg = ""

        app_states = self.retrieve_app_states()
        for key, state in app_states.items():
            if isinstance(state, (list, dict)):
                state = deepcopy(state)

            new_state = self.call_method(f'on_app_state_{key}_save', state)
            if new_state is not None:
                state = new_state

            if key == 'flow_id' and flow_action(state) != 'focus':
                state = id_of_flow('')
            elif key == 'flow_path':
                state = flow_path_strip(state)

            err_msg = self.set_var(key, state, section=APP_STATE_SECTION_NAME)
            self.vpo(f"MainAppBase.save_app_state {key}={state} {err_msg or 'OK'}")
            if err_msg:
                break

        self.load_cfg_files()

        if self.debug_level:
            self.play_sound('error' if err_msg else 'debug_save')

        return err_msg

    def setup_app_states(self, app_states: AppStateType):
        """ put app state variables into main app instance to prepare framework app.run_app.

        :param app_states:      dict of app states.
        """
        self.vpo(f"MainAppBase.setup_app_states {app_states}")

        # init/add most needed app states (e.g. for self.img_file() calls in .kv with font_size/light_theme bindings)
        font_size = app_states.get('font_size', 0.0)
        if not MIN_FONT_SIZE <= font_size <= MAX_FONT_SIZE:
            if font_size < 0.0:
                font_size = self.dpi_factor() * -font_size      # adopt device scaling on very first app start
            elif font_size == 0.0:
                font_size = self.font_size
            app_states['font_size'] = min(max(MIN_FONT_SIZE, font_size), MAX_FONT_SIZE)
        if 'light_theme' not in app_states:
            app_states['light_theme'] = self.light_theme

        for key, val in app_states.items():
            self.change_app_state(key, val, send_event=False)   # don't send on_-events as framework is not initialized
            if key == 'flow_id' and flow_action(val) == 'focus':
                self._last_focus_flow_id = val

        current_version = app_states.get(APP_STATE_VERSION_VAR_NAME, 0)
        upgrade_version = self.upgraded_config_app_state_version()
        if upgrade_version > current_version:
            for from_version in range(current_version, upgrade_version):
                self.call_method('on_app_state_version_upgrade', from_version)
            self.change_app_state(APP_STATE_VERSION_VAR_NAME, upgrade_version, send_event=False, old_name=UNSET)

    def show_message(self, message: str, title: str = "", is_error: bool = True):
        """ display (error) message popup to the user.

        :param message:         message string to display.
        :param title:           title of message box.
        :param is_error:        pass False to not emit error tone/vibration.
        """
        if is_error:
            self.play_vibrate()
            self.play_beep()

        popup_kwargs = dict(message=message)
        if title:
            popup_kwargs['title'] = title

        self.change_flow(id_of_flow('show', 'message'), popup_kwargs=popup_kwargs)

    def stop_app(self, exit_code: int = 0):
        """ quit this application.

        :param exit_code:   optional exit code.
        """
        self.dpo(f"MainAppBase.stop_app {exit_code}")
        self._exit_code = exit_code

        self.call_method('on_app_stop')

        if self.framework_win:
            self.framework_win.close()      # close window to save app state data

        self.call_method('on_app_exit')

        if self._stop_event_loop:
            self._stop_event_loop()         # will exit the self._start_event_loop() method called by self.run_app()

    def upgraded_config_app_state_version(self) -> int:
        """ determine app state version of an app upgrade.

        :return:                value of app state variable APP_STATE_VERSION_VAR_NAME if the app got upgraded (and has
                                a config file from a previous app installation), else 0.
        """
        cfg_file_name = os.path.join(MOVES_SRC_FOLDER_NAME, self.app_name + INI_EXT)
        cfg_parser = instantiate_config_parser()
        cfg_parser.read(cfg_file_name, encoding='utf-8')
        return cfg_parser.getint(APP_STATE_SECTION_NAME, APP_STATE_VERSION_VAR_NAME, fallback=0)

    def widget_by_attribute(self, att_name: str, att_value: str) -> Optional[Any]:
        """ determine the first (top-most) widget having the passed attribute name and value.

        :param att_name:        name of the attribute of the searched widget.
        :param att_value:       attribute value of the searched widget.
        :return:                widget that has the specified attribute with the specified value or None if not found.
        """
        return self.find_widget(lambda widget: getattr(widget, att_name, None) == att_value)

    def widget_by_flow_id(self, flow_id: str) -> Optional[Any]:
        """ determine the first (top-most) widget having the passed flow_id.

        :param flow_id:         flow id value of the searched widget's `tap_flow_id`/`focus_flow_id` attribute.
        :return:                widget that has a `tap_flow_id`/`focus_flow_id` attribute with the value of the passed
                                flow id or None if not found.
        """
        return self.widget_by_attribute('tap_flow_id', flow_id) or self.widget_by_attribute('focus_flow_id', flow_id)

    def widget_by_app_state_name(self, app_state_name: str) -> Optional[Any]:
        """ determine the first (top-most) widget having the passed app state name (app_state_name).

        :param app_state_name:  app state name of the widget's `app_state_name` attribute.
        :return:                widget that has a `app_state_name` attribute with the passed app state name
                                or None if not found.
        """
        return self.widget_by_attribute('app_state_name', app_state_name)

    def widget_children(self, wid: Any, only_visible: bool = False) -> List:
        """ determine the children of widget or its container (if exists) in z-order (top-most last).

        :param wid:             widget to determine the children from.
        :param only_visible:    pass True to only return visible widgets.
        :return:                list of children widgets of the passed widget.
        """
        wid_visible = self.widget_visible
        return [chi for chi in getattr(wid, 'container', wid).children if not only_visible or wid_visible(chi)]

    @staticmethod
    def widget_pos(wid) -> Tuple[float, float]:
        """ return the absolute window x and y position of the passed widget.

        :param wid:             widget to determine the position of.
        :return:                tuple of x and y screen coordinate.
        """
        return wid.x, wid.y

    def widgets_enclosing_rectangle(self, widgets: Union[list, tuple]) -> Tuple[float, float, float, float]:
        """ calculate the minimum bounding rectangle all the passed widgets.

        :param widgets:         list/tuple of widgets to determine the minimum bounding rectangle for.
        :return:                tuple of floats with the x, y, width, height values of the bounding rectangle.
        """
        min_x = min_y = 999999.9
        max_x = max_y = 0.0

        for wid in widgets:
            w_x, w_y = self.widget_pos(wid)
            if w_x < min_x:
                min_x = w_x
            if w_y < min_y:
                min_y = w_y

            w_w, w_h = self.widget_size(wid)
            if w_x + w_w > max_x:
                max_x = w_x + w_w
            if w_y + w_h > max_y:
                max_y = w_y + w_h

        return min_x, min_y, max_x - min_x, max_y - min_y

    @staticmethod
    def widget_size(wid) -> Tuple[float, float]:
        """ return the size (width and height) in pixels of the passed widget.

        :param wid:             widget to determine the size of.
        :return:                tuple of width and height in pixels.
        """
        return wid.width, wid.height

    @staticmethod
    def widget_visible(wid: Any) -> bool:
        """ determine if the passed widget is visible (has width and height and (visibility or opacity) set).

        :param wid:             widget to determine visibility of.
        :return:                True if widget is visible (or visibility cannot be determined), False if hidden.
        """
        return bool(wid.width and wid.height and
                    getattr(wid, 'visible', True) in (True, None) and   # containers/BoxLayout.visible is None ?!?!?
                    getattr(wid, 'opacity', True))

    def win_pos_size_change(self, *win_pos_size):
        """ screen resize handler called on window resize or when app will exit/stop via closed event.

        :param win_pos_size:    window geometry/coordinates: x, y, width, height.
        """
        app = self.framework_app
        win_width, win_height = win_pos_size[2:]
        app.landscape = win_width >= win_height                 # update landscape flag

        self.vpo(f"MainAppBase.win_pos_size_change {win_pos_size}: landscape={app.landscape}")

        self.change_app_state('win_rectangle', win_pos_size)
        self.call_method('on_win_pos_size')


register_package_images()   # register base image files of this portion
register_package_sounds()   # register base sound files of this portion

# reference imported but unused names in pseudo variable `_d_`, to be available in :meth:`MainAppBase.global_variables`
_d_ = (os_platform, path_name, placeholder_path)
module_globals = globals()
#: used. e.g. by :mod:`ae.gui_help` for execution/evaluation of dynamic code, expressions and f-strings
