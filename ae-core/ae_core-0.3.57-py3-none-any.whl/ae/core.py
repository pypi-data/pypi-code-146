"""
application core constants, helper functions and base classes
=============================================================

this module declares practical constants, tiny helper functions and app base classes, which are reducing the code of
your application (and of other ae namespace modules/portions).

core constants
--------------

there are three debug level constants: :data:`DEBUG_LEVEL_DISABLED`, :data:`DEBUG_LEVEL_ENABLED` and
:data:`DEBUG_LEVEL_VERBOSE`. short names for all debug level constants are provided by the dict :data:`DEBUG_LEVELS`.
the debug level of your application can be either set in your code or optionally data-driven externally (using the
:ref:`config-files` or :ref:`config-options` of the module :mod:`ae.console`).

to use the :mod:`python logging module <logging>` in conjunction with this module the constant :data:`LOGGING_LEVELS` is
providing a mapping between the debug levels and the python logging levels.

the encoding of strings into byte-strings (to output them to the console/stdout or to file contents) can be tricky
sometimes. to not lose any logging output because of invalid characters this module will automatically handle any
:exc:`UnicodeEncodeError` exception for you. invalid characters will then automatically be converted to the default
encoding (specified by :data:`~ae.base.DEF_ENCODING`) with the default error handling method specified by
:data:`~ae.base.DEF_ENCODE_ERRORS` (both defined in the :mod:`ae.base` namespace portion/module).


core helper functions
---------------------

the :func:`print_out` function, which is fully compatible to pythons :func:`print`, is using the encode helpers
:func:`~ae.base.force_encoding` and :func:`~.ae.base.to_ascii` to auto-correct invalid characters.

the function :func:`hide_dup_line_prefix` is very practical if you want to remove or hide redundant line prefixes in
your log files, to make them better readable.


application base classes
------------------------

the classes :class:`AppBase` and :class:`SubApp` are applying logging and debugging features to your application. create
in your application one instance of :class:`AppBase` to represent the main application task. if your application needs a
separate logging/debugging configuration for sub-threads or sub-tasks then create an :class:`SubApp` instance for each
of these sub-apps.

sub-apps are very flexible and not tied to any fix use-case. they can be created e.g. for each sub-task or application
thread. you could also create a :class:`SubApp` instance for each of your external systems, like a database server or to
connect your application onto different test environments or to your live/production system (e.g. for system
comparison and maintenance).

both application classes are automatically catching and handling any exceptions and run-time errors: only if any
critical exception/error cannot be handled then the :meth:`~AppBase.shutdown` method will make sure that all sub-apps
and threads get terminated and joined. additionally all print-out buffers will be flushed to include all the info of the
critical error (the last debug and error messages) into the standard error/output and into any activated log files.


basic usage of an application base class
........................................

at the top of your python application main file/module create an instance of the class :class:`AppBase`::

    \"\"\"  docstring at the top of the main module of your application  \"\"\"
    from ae.core import AppBase

    __version__ = '1.2.3'

    ca = AppBase()

in the above example the :class:`AppBase` instance will automatically use the docstring title of the module as
application title and the string in the module variable __version___ as application version. to overwrite these defaults
pass your application title and version string via the arguments :paramref:`~AppBase.app_title` and
:paramref:`~AppBase.app_version` to the instantiation of :class:`AppBase`::

    ca = AppBase(app_title="title of this app instance", app_version='3.2.1')

other automatically initialized instance attributes of :class:`AppBase` are documented underneath in the
:class:`class docstring <AppBase>`. they include e.g. the
:attr:`date and time when the instance got created <AppBase.startup_beg>`, the
:attr:`name/id of this application instance <AppBase.app_name>` or the :attr:`application path <AppBase.app_path>`.


application class hierarchy
...........................

for most use cases you will not instantiate from :class:`AppBase` directly - instead you will instantiate one of the
extended application classes that are inherited from this base class.

the class :class:`~ae.console.ConsoleApp` e.g. inherits from :class:`AppBase` and is adding configuration options and
variables to it. so in your console application it is recommended to directly use instances of
:class:`~ae.console.ConsoleApp` instead of :class:`AppBase`.

for applications with an GUI use instead one of the classes :class:`~ae.kivy_app.KivyApp`,
:class:`~ae.enaml_app.EnamlApp` or :class:`~ae.toga_app.TogaApp`.


application logging
-------------------

print-outs are an essential tool for the debugging and logging of your application at run-time. in python the print-outs
are done with the :func:`print` function or with the python :mod:`logging` module. these print-outs get per default send
to the standard output and error streams of your OS and so displayed on your system console/shell. the :func:`print_out`
function and the :meth:`~AppBase.print_out` method of this :mod:`.core` module are adding two more sophisticated ways
for print-outs to the console/log-files.

using :class:`AppBase` is making the logging much easier and also ensures that print-outs of any imported library or
package will be included within your log files. this is done by redirecting the standard output and error streams to
your log files with the help of the :class:`_PrintingReplicator` class.

head-less server applications like web servers are mostly not allowed to use the standard output streams. for some these
applications you could redirect the standard output and error streams to a log file by using the OS redirection
character (``>``)::

    python your_application.py >log_std_out.log 2>log_std_err.log

but because most web servers doesn't allow you to use this redirection, you can alternatively specify the
:paramref:`~AppBase.suppress_stdout` parameter as ``True`` in the instantiation of an :class:`AppBase` instance.
additionally you can call the :meth:`~AppBase.init_logging` method to activate a log file. after that all print-outs of
your application and libraries will only appear in your log file.

also in complex applications, where huge print-outs to the console can get lost easily, you want to use a log file
instead. but even a single log file can get messy to read, especially for multithreading server applications. for that
:class:`SubApp` is allowing you to create for each thread a separate sub-app instance with its own log file.

using this module ensures that any crashes or freezes happening in your application will be fully logged. apart from the
gracefully handling of :exc:`UnicodeEncodeError` exceptions, the :mod:`Python faulthandler <faulthandler>` will be
enabled automatically to catch system errors and to dump a traceback of them to the console and any activated log file.


activate ae log file
....................

.. _ae-log-file:

ae log files are text files using by default the encoding of your OS console/shell. to activate the redirection of your
applications print-outs into an ae log file for a :class:`AppBase` instance you simply specify the file name of the log
file in the :meth:`~AppBase.init_logging` method call::

    app = AppBase()
    app.init_logging(log_file_name='my_log_file.log')


activate ae logging features
............................

for multi-threaded applications include the thread-id of the printing thread automatically into your log files by
passing a ``True`` value to the :paramref:`~AppBase.multi_threading` argument. to additionally also suppress any
print-outs to the standard output/error streams pass ``True`` to the :paramref:`~AppBase.suppress_stdout` argument::

    app = AppBase(multi_threading=True, suppress_stdout=True)
    app.init_logging(log_file_name='my_log_file.log')

the ae log files provided by this module are automatically rotating if the size of a log file succeeds the value in
MBytes defined in the :data:`LOG_FILE_MAX_SIZE`. to adapt this value to your needs you can specify the maximum log file
size in MBytes with the argument :paramref:`~AppBase.init_logging.log_file_size_max` in your call of
:meth:`~AppBase.init_logging`::

    app.init_logging(log_file_name='my_log_file.log', log_file_size_max=9.)

by using the :class:`~ae.console.ConsoleApp` class instead of :class:`AppBase` you can alternatively store the logging
configuration of your application within a :ref:`configuration variable <config-variables>` or a
:ref:`configuration option <config-options>`. the order of precedence to find the appropriate logging configuration of
each app instance is documented :meth:`here <ae.console.ConsoleApp._init_logging>`.


using python logging module
...........................

if you prefer to use instead the python logging module for the print-outs of your application, then pass a
:mod:`python logging configuration dictionary <logging.config>` with the individual configuration of your logging
handlers, files and loggers to the :paramref:`~AppBase.init_logging.py_logging_params` argument of the
:meth:`~AppBase.init_logging` method::

    app.init_logging(py_logging_params=my_py_logging_config_dict)

passing the python logging configuration dictionary to one of the :class:`AppBase` instances created by your application
will automatically disable the ae log file of this instance.


application debugging
---------------------

to use the debug features of :mod:`~.core` you simply have to import the needed
:ref:`debug level constant <debug-level-constants>` to pass it at instantiation of your :class:`AppBase` or
:class:`SubApp` class to the :paramref:`~AppBase.debug_level` argument::

    app = AppBase(..., debug_level= :data:`DEBUG_LEVEL_ENABLED`)     # same for :class:`SubApp`

by passing :data:`DEBUG_LEVEL_ENABLED` the print-outs (and log file contents) will be more detailed, and even more
verbose if you use instead the debug level :data:`DEBUG_LEVEL_VERBOSE`.

the debug level can be changed at any time in your application code by directly assigning the new debug level to the
:attr:`~AppBase.debug_level` property. if you prefer to change the debug levels dynamically, then use the
:class:`~.console.ConsoleApp` instead of :class:`AppBase`, because :class:`~.console.ConsoleApp` provides this property
as a :ref:`configuration file variable <config-variables>` and :ref:`commend line option <config-options>`. this way you
can specify :ref:`the actual debug level <pre-defined-config-options>` without the need to change (and re-build) your
application code.

.. _debug-level-constants:

"""
import datetime
import faulthandler
import logging
import logging.config
import os
import sys
import threading
import traceback
import weakref

from io import StringIO
from typing import Any, Callable, Dict, List, Optional, TextIO, Tuple, Union, cast

from ae.base import DATE_TIME_ISO, DEF_ENCODE_ERRORS, force_encoding, stack_var, to_ascii           # type: ignore
from ae.paths import app_name_guess, app_data_path, app_docs_path, PATH_PLACEHOLDERS                # type: ignore


__version__ = '0.3.57'


# DON'T RE-ORDER: using module doc-string as _debug-level-constants sphinx hyperlink to following DEBUG_ constants
DEBUG_LEVEL_DISABLED: int = 0       #: lowest debug level - only display logging levels ERROR/CRITICAL.
DEBUG_LEVEL_ENABLED: int = 1        #: minimum debugging info - display logging levels WARNING or higher.
DEBUG_LEVEL_VERBOSE: int = 2        #: verbose debug info - display logging levels INFO/DEBUG or higher.

DEBUG_LEVELS: Dict[int, str] = {DEBUG_LEVEL_DISABLED: 'disabled', DEBUG_LEVEL_ENABLED: 'enabled',
                                DEBUG_LEVEL_VERBOSE: 'verbose'}
""" numeric ids and names of all supported debug levels. """

LOGGING_LEVELS: Dict[int, int] = {DEBUG_LEVEL_DISABLED: logging.WARNING, DEBUG_LEVEL_ENABLED: logging.INFO,
                                  DEBUG_LEVEL_VERBOSE: logging.DEBUG}
""" association between ae debug levels and python logging levels. """

HIDDEN_CREDENTIALS = ('password', 'token')      #: credential keys that are hidden in print/repr output (not if verbose)


def hide_dup_line_prefix(last_line: str, current_line: str) -> str:
    """ replace duplicate characters at the start of two strings with spaces.

    :param last_line:       last line string (e.g. the last line of text/log file).
    :param current_line:    current line string.
    :return:                current line string but duplicate characters at the beginning are replaced by space chars.
    """
    idx = 0
    min_len = min(len(last_line), len(current_line))
    while idx < min_len and last_line[idx] == current_line[idx]:
        idx += 1
    return " " * idx + current_line[idx:]


MAX_NUM_LOG_FILES: int = 69                         #: maximum number of :ref:`ae log files <ae-log-file>`
LOG_FILE_MAX_SIZE: int = 15                         #: max. size in MB of rotating :ref:`ae log files <ae-log-file>`
LOG_FILE_IDX_WIDTH: int = len(str(MAX_NUM_LOG_FILES)) + 3
""" width of rotating log file index within log file name; adding +3 to ensure index range up to factor 10^3. """

ori_std_out: TextIO = sys.stdout                    #: original sys.stdout on app startup
ori_std_err: TextIO = sys.stderr                    #: original sys.stderr on app startup

log_file_lock: threading.RLock = threading.RLock()  #: log file rotation multi-threading lock


_LOGGER = None       #: python logger for this module gets lazy/late initialized and only if requested by caller


def logger_late_init():
    """ check if logging modules got initialized already and if not then do it now. """
    global _LOGGER
    if not _LOGGER:
        _LOGGER = logging.getLogger(__name__)


_MULTI_THREADING_ACTIVATED: bool = False            #: flag if threading is used in your application


def activate_multi_threading():
    """ activate multi-threading for all app instances (normally done at main app startup). """
    global _MULTI_THREADING_ACTIVATED
    _MULTI_THREADING_ACTIVATED = True


def _deactivate_multi_threading():
    """ disable multi threading (needed to reset app environment in unit testing). """
    global _MULTI_THREADING_ACTIVATED
    _MULTI_THREADING_ACTIVATED = False


def print_out(*objects, sep: str = " ", end: str = "\n", file: Optional[TextIO] = None, flush: bool = False,
              encode_errors_def: str = DEF_ENCODE_ERRORS, logger: Optional['logging.Logger'] = None,
              app: Optional['AppBase'] = None, **kwargs):
    """ universal/unbreakable print function - replacement for the :func:`built-in python function print() <print>`.

    :param objects:             tuple of objects to be printed. if the first object is a string that starts with a \\\\r
                                character then the print-out will be only sent to the standard output (and will not be
                                added to any active log files - see also :paramref:`~print_out.end` argument).
    :param sep:                 separator character between each printed object/string (def=" ").
    :param end:                 finalizing character added to the end of this print-out (def="\\\\n"). pass \\\\r to
                                suppress the print-out into :ref:`ae log file <ae-log-file>` or to any activated python
                                logger - useful for console/shell processing animation (see :meth:`.tcp.TcpServer.run`).
    :param file:                output stream object to be printed to (def=None which will use standard output streams).
                                if given then the redirection to all active log files and python logging loggers will be
                                disabled (even if the :paramref:`~print_out.logger` argument is specified).
    :param flush:               flush stream after printing (def=False).
    :param encode_errors_def:   default error handling to encode (def=:data:`DEF_ENCODE_ERRORS`).
    :param logger:              used logger to output `objects` (def=None). ignored if the :paramref:`~print_out.file`
                                argument gets specified/passed.
    :param app:                 the app instance from where this print-out got initiated.
    :param kwargs:              catch unsupported kwargs for debugging (all items will be printed to all the activated
                                logging/output streams).

    this function is silently handling and autocorrecting string encode errors for output/log streams which are not
    supporting unicode. any instance of :class:`AppBase` is providing this function as a method with the
    :func:`same name <AppBase.print_out>`). it is recommended to call/use this instance method instead of this function.

    in multithreading applications this function prevents dismembered/fluttered print-outs from different threads.

    .. note:: this function has an alias named :func:`.po`.
    """
    processing = end == "\r" or (objects and str(objects[0]).startswith('\r'))  # True if called by Progress.next()
    enc = getattr(file or ori_std_out if processing else sys.stdout, 'encoding', 'utf-8')
    use_py_logger = False

    main_app = main_app_instance()
    if main_app:
        file = main_app.log_file_check(file)    # check if late init of logging system is needed
    if app and app != main_app:
        file = app.log_file_check(file)         # check sub-app suppress_stdout/log file status and rotation
    else:
        app = main_app

    if processing:
        file = ori_std_out
    elif logger is not None and file is None and (
            app and app.py_log_params and main_app != app or main_app and main_app.py_log_params):
        use_py_logger = True
        logger_late_init()

    if kwargs:
        objects += (f"\n   *  EXTRA KWARGS={kwargs}", )

    retries = 2
    while retries:
        try:
            print_strings = tuple(map(lambda _: str(_).encode(enc, errors=encode_errors_def).decode(enc), objects))
            if use_py_logger or _MULTI_THREADING_ACTIVATED:
                # concatenating objects also prevents fluttered log file content in multi-threading apps
                # .. see https://stackoverflow.com/questions/3029816/how-do-i-get-a-thread-safe-print-in-python-2-6
                # .. and https://stackoverflow.com/questions/50551637/end-key-in-print-not-thread-safe
                print_one_str = sep.join(print_strings)
                sep = ""
                if end and (not use_py_logger or end != '\n'):
                    print_one_str += end
                    end = ""
                print_strings = (print_one_str, )

            if use_py_logger:
                debug_level = app.debug_level if app else DEBUG_LEVEL_VERBOSE
                if logger:      # mypy insists on have this extra check, although `use_py_logger` is including logger
                    logger.log(level=LOGGING_LEVELS[debug_level], msg=print_strings[0])
            else:
                print(*print_strings, sep=sep, end=end, file=file, flush=flush)
            break
        except UnicodeEncodeError:
            fixed_objects = []
            for obj in objects:
                if not isinstance(obj, str) and not isinstance(obj, bytes):
                    obj = str(obj)
                if retries == 2:
                    obj = force_encoding(obj, encoding=enc)
                else:
                    obj = to_ascii(obj)
                fixed_objects.append(obj)
            objects = tuple(fixed_objects)
            retries -= 1
        except (IOError, OSError, ValueError, Exception):   # pragma: no cover
            traceback.print_exc()
            print("...... in ae.core.print_out(", objects, ")")
            break


po = print_out              #: alias of function :func:`.print_out`


APP_KEY_SEP: str = '@'      #: separator character used in :attr:`~AppBase.app_key` of :class:`AppBase` instance

# had to use type comment because the following line is throwing an error in the Sphinx docs make:
# _APP_INSTANCES: weakref.WeakValueDictionary[str, "AppBase"] = weakref.WeakValueDictionary()
_APP_INSTANCES = weakref.WeakValueDictionary()   # type: weakref.WeakValueDictionary[str, AppBase]
""" dict that is weakly holding references to all :class:`AppBase` instances created at run time.

gets automatically initialized in :meth:`AppBase.__init__` to allow log file split/rotation
and debug_level access at application thread or module level.

the first created :class:`AppBase` instance is called the main app instance. :data:`_MAIN_APP_INST_KEY`
stores the dict key of the main instance.
"""
_MAIN_APP_INST_KEY: str = ''    #: key in :data:`_APP_INSTANCES` of main :class:`AppBase` instance

app_inst_lock: threading.RLock = threading.RLock()  #: app instantiation multi-threading lock


def main_app_instance() -> Optional['AppBase']:
    """ determine the main instance of the :class:`AppBase` in the current running application.

    :return:                    main/first-instantiated :class:`AppBase` instance or None (if app is not fully
                                initialized yet).
    """
    with app_inst_lock:
        return _APP_INSTANCES.get(_MAIN_APP_INST_KEY)


def registered_app_names() -> List[str]:
    """ determine the app names of all registered/running applications. """
    with app_inst_lock:
        return [app.app_name for app in _APP_INSTANCES.values()]


def _register_app_instance(app: 'AppBase'):
    """ register new :class:`AppBase` instance in :data:`_APP_INSTANCES`.

    :param app:                 :class:`AppBase` instance to register
    """
    with app_inst_lock:
        global _APP_INSTANCES, _MAIN_APP_INST_KEY
        msg = f"register_app_instance({app}) expects "
        assert app not in _APP_INSTANCES.values(), msg + "new instance - this app got already registered"

        key = app.app_key
        assert key and key not in _APP_INSTANCES, \
            msg + f"non-empty, unique app key (app_name+sys_env_id=={key} keys={list(_APP_INSTANCES.keys())})"

        cnt = len(_APP_INSTANCES)
        if _MAIN_APP_INST_KEY:
            assert cnt > 0, f"No app instances registered but main app key is set to {_MAIN_APP_INST_KEY}"
        else:
            assert cnt == 0, f"{cnt} sub-apps {list(_APP_INSTANCES.keys())} found after main app remove"
            _MAIN_APP_INST_KEY = key
        _APP_INSTANCES[key] = app


def _unregister_app_instance(app_key: str) -> Optional['AppBase']:
    """ unregister/remove :class:`AppBase` instance from within :data:`_APP_INSTANCES`.

    :param app_key:             app key of the instance to remove.
    :return:                    removed :class:`AppBase` instance.
    """
    with app_inst_lock:
        global _APP_INSTANCES, _MAIN_APP_INST_KEY
        app = _APP_INSTANCES.pop(app_key, None)
        cnt = len(_APP_INSTANCES)
        if app_key == _MAIN_APP_INST_KEY:
            _MAIN_APP_INST_KEY = ''
            assert cnt == 0, f"{cnt} sub-apps {list(_APP_INSTANCES.keys())} found after main app {app_key}{app} remove"
        elif _MAIN_APP_INST_KEY:
            assert cnt > 0, f"Unregistered last app {app_key}/{app} but was not the main app {_MAIN_APP_INST_KEY}"
        return app


def _shut_down_sub_app_instances(timeout: Optional[float] = None):
    """ shut down all :class:`SubApp` instances.

    :param timeout:             timeout float value in seconds used for the :class:`SubApp` shutdowns and for the
                                acquisition of the threading locks of :data:`the ae log file <log_file_lock>` and the
                                :data:`app instances <app_inst_lock>`.
    """
    aqc_kwargs: Dict[str, Any] = (dict(blocking=False) if timeout is None else dict(timeout=timeout))
    blocked = app_inst_lock.acquire(**aqc_kwargs)
    main_app = main_app_instance()
    for app in list(_APP_INSTANCES.values()):   # list is needed because weak ref dict get changed in loop
        if app is not main_app:
            app.shutdown(timeout=timeout)
    if blocked:
        app_inst_lock.release()


class _PrintingReplicator:
    """ replacement of standard/error stream replicating print-outs to all active logging streams (log files/buffers).
    """
    def __init__(self, sys_out_obj: TextIO = ori_std_out) -> None:
        """ initialise a new T-stream-object

        :param sys_out_obj:     standard output/error stream to be replicated (def=sys.stdout)
        """
        self.sys_out_obj = sys_out_obj

    def write(self, any_str: Union[str, bytes]) -> None:
        """ write string to ae logging and standard output streams.

        automatically suppressing UnicodeEncodeErrors if console/shell or log file has different encoding by forcing
        re-encoding with DEF_ENCODE_ERRORS.

        :param any_str:         string or bytes to output.
        """
        message = any_str.decode() if isinstance(any_str, bytes) else any_str
        app_streams: List[Tuple[Optional[AppBase], TextIO]] = []
        with log_file_lock, app_inst_lock:
            for app in list(_APP_INSTANCES.values()):
                stream = app.log_file_check(app.active_log_stream)  # check if log rotation or buf-to-file-switch needed
                if stream:
                    app_streams.append((app, stream))
            if not self.sys_out_obj.closed:
                app_streams.append((main_app_instance(), self.sys_out_obj))

            if message and message[0] != '\n' and message[-1] == '\n':
                message = '\n' + message[:-1]
            log_lines = message.split('\n')
            for app_or_none, stream in app_streams:
                line_prefix = '\n' + (app_or_none.log_line_prefix() if app_or_none else '')
                app_msg = line_prefix.join(log_lines)
                try:
                    stream.write(app_msg)
                except UnicodeEncodeError:
                    stream.write(force_encoding(app_msg, encoding=stream.encoding))

    def __getattr__(self, attr: str) -> Any:
        """ get attribute value from standard output stream.

        :param attr:            name of the attribute to retrieve/return.
        :return:                value of the attribute.
        """
        return getattr(self.sys_out_obj, attr)


_APP_THREADS = weakref.WeakValueDictionary()   # type: weakref.WeakValueDictionary[int, threading.Thread]
""" weak dict to keep the references of all application threads. added to prevent
the joining of unit testing threads in the test teardown (resetting app environment). """


def _register_app_thread():
    """ add new app thread to _APP_THREADS if not already added. """
    global _APP_THREADS
    tid = threading.get_ident()
    if tid not in _APP_THREADS:
        _APP_THREADS[tid] = threading.current_thread()


def _join_app_threads(timeout: Optional[float] = None):
    """ join/finish all app threads and finally deactivate multi-threading.

    :param timeout:             timeout float value in seconds for thread joining (def=None - block/no-timeout).

    .. note:: this function has to be called by the main app instance only.
    """
    global _APP_THREADS
    main_thread = threading.current_thread()
    for app_thread in list(_APP_THREADS.values()):     # threading.enumerate() also includes PyCharm/pytest threads
        if app_thread is not main_thread:
            po(f"  **  joining thread id <{app_thread.ident: >6}> name={app_thread.getName()}", logger=_LOGGER)
            app_thread.join(timeout)
            if app_thread.ident is not None:     # mypy needs it because ident is Optional
                _APP_THREADS.pop(app_thread.ident)
    _deactivate_multi_threading()


class AppBase:
    """ provides easy logging and debugging for your application.

    most applications only need a single instance of this class; apps with threads could create separate instances
    for each thread.

    instance Attributes (ordered alphabetically - ignoring underscore characters):

    * :attr:`app_key`               id/key of this application instance.
    * :attr:`app_name`              basename (without the file name extension) of the executable.
    * :attr:`app_path`              file path of app executable.
    * :attr:`app_title`             application title/description.
    * :attr:`app_version`           application version (set via the :paramref:`AppBase.app_version` argument).
    * :attr:`debug_level`           debug level of this instance.
    * :attr:`_last_log_line_prefix` last ae log file line prefix that got print-out to the log of this app instance.
    * :attr:`_log_buf_stream`       ae log file buffer stream.
    * :attr:`_log_file_index`       index of the current rotation ae log file backup.
    * :attr:`_log_file_name`        path and file name of the ae log file.
    * :attr:`_log_file_size_max`    maximum size in MBytes of an ae log file.
    * :attr:`_log_file_stream`      ae log file TextIO output stream.
    * :attr:`_log_with_timestamp`   log timestamp line prefix if True or a non-empty strftime compatible format string.
    * :attr:`py_log_params`         python logging config dictionary.
    * :attr:`_nul_std_out`          null stream used to prevent print-outs to :attr:`standard output <sys.stdout>`.
    * :attr:`_shut_down`            flag set to True if this application instance got already shutdown.
    * :attr:`startup_beg`           datetime of begin of the instantiation/startup of this app instance.
    * :attr:`startup_end`           datetime of end of the instantiation/startup of this application instance.
    * :attr:`suppress_stdout`       flag set to True if this application does not print to stdout/console.
    * :attr:`sys_env_id`            system environment id of this application instance.
    """
    app_title: str = ""                             #: title/description of this app instance
    app_name: str = ''                              #: name of this app instance
    app_version: str = ''                           #: version of this app instance
    _debug_level: int = DEBUG_LEVEL_VERBOSE         #: debug level of this app instance
    sys_env_id: str = ''                            #: system environment id of this app instance
    suppress_stdout: bool = True                    #: flag to suppress prints to stdout
    startup_end: Optional[datetime.datetime] = None  #: end datetime of the application startup
    _last_log_line_prefix: str = ""                 #: prefix of the last printed log line
    _log_buf_stream: Optional[StringIO] = None      #: log file buffer stream instance
    _log_file_stream: Optional[TextIO] = None       #: log file stream instance
    _log_file_index: int = 0                        #: log file index (for rotating logs)
    _log_file_size_max: float = LOG_FILE_MAX_SIZE   #: maximum log file size in MBytes (rotating log files)
    _log_file_name: str = ""                        #: log file name
    _log_with_timestamp: Union[bool, str] = False   #: True of strftime format string to enable timestamp
    _nul_std_out: Optional[TextIO] = None           #: logging null stream
    py_log_params: Dict[str, Any] = {}              #: dict of config parameters for py logging
    _shut_down: bool = False                        #: True if this app instance got shut down already

    def __init__(self, app_title: str = '', app_name: str = '', app_version: str = '', sys_env_id: str = '',
                 debug_level: int = DEBUG_LEVEL_DISABLED, multi_threading: bool = False, suppress_stdout: bool = False):
        """ initialize a new :class:`AppBase` instance.

        :param app_title:       application title/description setting the attribute :attr:`~ae.core.AppBase.app_title`.
                                if not specified then the docstring of your app's main module will be used (see
                                :ref:`example <app-title>`).
        :param app_name:        application instance name to set the attribute :attr:`~ae.core.AppBase.app_name`. if not
                                specified then base name of the main module file name will be used.
        :param app_version:     application version string to set the attribute :attr:`~ae.core.AppBase.app_version`. if
                                not specified then value of a global variable with the name `__version__` will be used
                                (if declared in the actual call stack).
        :param sys_env_id:      system environment id to set the instance attribute :attr:`~ae.core.AppBase.sys_env_id`.
                                the default value of this argument is an empty string.
        :param debug_level:     default debug level to set the instance attribute :attr:`~ae.core.AppBase.debug_level`.
                                the default value of this argument is :data:`~ae.core.DEBUG_LEVEL_DISABLED`.
        :param multi_threading: pass True if instance is used in multi-threading app.
        :param suppress_stdout: pass True (for wsgi apps) to prevent any python print outputs to stdout.
        """
        self.startup_beg: datetime.datetime = datetime.datetime.now()   #: begin of app startup datetime
        self.app_path: str = os.path.dirname(sys.argv[0])               #: path to folder of your main app code file

        if not app_title:
            doc_str = stack_var('__doc__')
            app_title = doc_str.strip().split('\n')[0] if doc_str else ""
        if app_name:
            PATH_PLACEHOLDERS['app_name'] = app_name
            PATH_PLACEHOLDERS['app'] = app_data_path()
            PATH_PLACEHOLDERS['ado'] = app_docs_path()
        else:
            app_name = app_name_guess()
        if PATH_PLACEHOLDERS.get('main_app_name', "") in ("", 'pyTstConsAppKey', '_jb_pytest_runner'):
            PATH_PLACEHOLDERS['main_app_name'] = app_name
        if not app_version:
            app_version = stack_var('__version__') or ""

        self.app_title: str = app_title                         #: title/description of this app instance
        self.app_name: str = app_name                           #: name of this app instance
        self.app_version: str = app_version                     #: version of this app instance
        self._debug_level: int = debug_level                    #: debug level of this app instance
        self.sys_env_id: str = sys_env_id                       #: system environment id of this app instance
        if multi_threading:
            activate_multi_threading()
        self.suppress_stdout: bool = suppress_stdout            #: flag to suppress prints to stdout

        self.startup_end: Optional[datetime.datetime] = None    #: end datetime of the application startup

        _register_app_thread()
        _register_app_instance(self)

    def __del__(self):
        """ deallocate this app instance by calling :func:`AppBase.shutdown`.
        """
        self.shutdown(exit_code=None)

    @property
    def active_log_stream(self) -> Optional[Union[StringIO, TextIO]]:
        """ check if ae logging is active and if yes then return the currently used log stream (read-only property).

        :return:                log file or buf stream if logging is activated, else None.
        """
        with log_file_lock:
            return self._log_file_stream or self._log_buf_stream

    @property
    def app_key(self) -> str:
        """ determine the key of this application class instance (read-only property).

        :return:                application key string.
        """
        return self.app_name + APP_KEY_SEP + self.sys_env_id

    @property
    def debug_level(self) -> int:
        """ debug level property:

        :getter:                return the current debug level of this app instance.
        :setter:                change the debug level of this app instance.
        """
        return self._debug_level

    @debug_level.setter
    def debug_level(self, debug_level: int):
        """ debug level setter (added for easier overwrite in inheriting classes). """
        self._debug_level = debug_level

    @property
    def debug(self) -> bool:
        """ True if app is in debug mode. """
        return self._debug_level >= DEBUG_LEVEL_ENABLED

    @property
    def verbose(self) -> bool:
        """ True if app is in verbose debug mode. """
        return self._debug_level >= DEBUG_LEVEL_VERBOSE

    def call_method(self, callback: Union[Callable, str], *args, **kwargs) -> Any:
        """ call passed callable/method with the passed args, catching and logging exceptions preventing app exit.

    :param callback:            either a callable or the name of the main app method of this instance to call.
    :param args:                args passed to the main app method to be called.
    :param kwargs:              kwargs passed to the main app method to be called.
    :return:                    return value of the called method or None if method throws exception or does not exist.
        """
        if isinstance(callback, str):
            method_name = callback
            callback = getattr(self, method_name, None)     # type: ignore
            if callback is None:
                return None
            assert callable(callback), f"AppBase.call_method: main app method {method_name!r} is not callable"

        try:
            return callback(*args, **kwargs)
        except Exception as ex:     # AttributeError, LookupError, ValueError
            self.po(f" ***  AppBase.call_method({callback}, {args}, {kwargs}): {ex}\n{traceback.format_exc()}")

        return None

    def init_logging(self, py_logging_params: Optional[Dict[str, Any]] = None, log_file_name: str = "",
                     log_file_size_max: float = LOG_FILE_MAX_SIZE, log_with_timestamp: Union[bool, str] = False,
                     disable_buffering: bool = False):
        """ initialize logging system.

        :param py_logging_params:   config dict for python logging configuration. if this dict is not empty then python
                                    logging is configured with the given options in this dict and all the other kwargs
                                    are ignored.
        :param log_file_name:       default log file name for ae logging (def='' - ae logging disabled).
        :param log_file_size_max:   max. size in MB of ae log file (def=LOG_FILE_MAX_SIZE).
        :param log_with_timestamp:  add timestamp prefix to each log line if True or a non-empty strftime compatible
                                    format string.
        :param disable_buffering:   pass True to disable ae log buffering at app startup.

        log files and config values will be initialized as late as possible in :meth:`~AppBase.log_file_check`, e.g.
        indirectly triggered by a request to a config variable via :meth:`~AppBase._parse_args` (like `logFile`).
        """
        with log_file_lock:
            if py_logging_params:                   # init python logging - app is using python logging module
                logger_late_init()
                # logging.basicConfig(level=logging.DEBUG, style='{')
                logging.config.dictConfig(py_logging_params)     # re-configure py logging module
                self.py_log_params = py_logging_params
            else:                                   # (re-)init ae logging
                if self._log_file_stream:
                    self._close_log_file()
                    self._std_out_err_redirection(False)
                self._log_file_name = log_file_name
                self._log_file_size_max = log_file_size_max
                self._log_with_timestamp = log_with_timestamp
                if not disable_buffering:
                    self._log_buf_stream = StringIO(initial_value="####  Log Buffer\n" if self.debug else "")

    def log_line_prefix(self) -> str:
        """ compile prefix of log print-out line for this :class:`AppBase` instance.

        the line prefix consists of (depending on the individual values of either a module variable or of an
        attribute this app instance):

        * :data:`_MULTI_THREADING_ACTIVATED`: if True then the thread id gets printed surrounded with
          angle brackets (< and >), right aligned and space padded to minimal 6 characters.
        * :attr:`sys_env_id`: if not empty then printed surrounded with curly brackets ({ and }), left aligned
          and space padded to minimal 4 characters.
        * :attr:`_log_with_timestamp`: if (a) True or (b) a non-empty string then the system time
          (determined with :meth:`~datetime.datetime.now`) gets printed in the format specified either by the
          (a) the :data:`~ae.base.DATE_TIME_ISO` constant or (b) by the string in this attribute.

        this method is using the instance attribute :attr:`_last_log_line_prefix` to keep a copy of
        the last printed log line prefix to prevent the printout of duplicate characters in consecutive
        log lines.

        :return:                log file line prefix string including one space as separator character at the end.
        """
        parts = []
        if _MULTI_THREADING_ACTIVATED:
            parts.append(f"<{threading.get_ident(): >6}>")
        if self.app_key[-1] != APP_KEY_SEP:
            parts.append(f"{{{self.app_key: <6}}}")
        if self._log_with_timestamp:
            format_string = DATE_TIME_ISO if isinstance(self._log_with_timestamp, bool) else self._log_with_timestamp
            parts.append(datetime.datetime.now().strftime(format_string))
        if self.debug:
            parts.append(f"[{DEBUG_LEVELS[self.debug_level][0]}]")

        prefix = "".join(parts)
        with log_file_lock:
            last_pre = self._last_log_line_prefix
            self._last_log_line_prefix = prefix

        return hide_dup_line_prefix(last_pre, prefix) + " "

    def log_file_check(self, curr_stream: Optional[TextIO] = None) -> Optional[TextIO]:
        """ check and possibly correct log file status and the passed currently used stream.

        :param curr_stream:     currently used stream.
        :return:                stream passed into :paramref:`~log_file_check.curr_stream` or
                                new/redirected stream of :paramref:`~log_file_check.curr_stream` or
                                None if :paramref:`~log_file_check.curr_stream` is None.

        for already opened log files check if the ae log file is big enough and if yes then do a file rotation.
        if log file is not opened but log file name got already set, then check if log startup buffer is active
        and if yes then create log file, pass log buffer content to log file and close the log buffer.
        """
        old_stream = new_stream = None
        with log_file_lock:
            if self._log_file_stream:
                old_stream = self._log_file_stream
                self._log_file_stream.seek(0, 2)  # due to non-posix-compliant windows feature
                if self._log_file_stream.tell() >= self._log_file_size_max * 1024 * 1024:
                    self._close_log_file()
                    self._rename_log_file()
                    self._open_log_file()
                    new_stream = self._log_file_stream
            elif self._log_file_name:
                old_stream = self._log_buf_stream
                self._open_log_file()
                self._std_out_err_redirection(True)
                self._flush_and_close_log_buf()
                new_stream = self._log_file_stream
            elif self.suppress_stdout and not self._nul_std_out:    # pragma: no cover/_std_out_err_redirection does it
                old_stream = sys.stdout
                sys.stdout = self._nul_std_out = new_stream = open(os.devnull, 'w')

        if curr_stream == old_stream and new_stream:
            return new_stream
        return curr_stream

    def print_out(self, *objects, file: Optional[TextIO] = None, **kwargs):
        """ app-instance-specific print-outs.

        :param objects:         objects to be printed out.
        :param file:            output stream object to be printed to (def=None). passing None on a main app instance
                                will print the objects to the standard output and any active log files, but on a
                                :class:`SubApp` instance with an active log file the print-out will get redirected
                                exclusively/only to log file of this :class:`SubApp` instance.
        :param kwargs:          all the other supported kwargs of this method are documented
                                :func:`at the print_out() function of this module <print_out>`.

        this method has an alias named :meth:`.po`
        """
        if file is None and main_app_instance() is not self:
            with log_file_lock:
                file = self._log_buf_stream or self._log_file_stream
        if file:
            kwargs['file'] = file
        if 'app' not in kwargs:
            kwargs['app'] = self
        print_out(*objects, **kwargs)

    po = print_out          #: alias of method :meth:`.print_out`

    def debug_out(self, *objects, minimum_debug_level: int = DEBUG_LEVEL_ENABLED, **kwargs):
        """ special debug version of :func:`builtin print() function <print>`.

        this method will print out the passed objects only if the :attr:`current debug level
        <.core.AppBase.debug_level>` of this app instance is higher than the value passed into the
        :paramref:`~debug_out.minimum_debug_level` argument. in this case the print-out will be
        delegated onto the :meth:`~.print_out`.

        :param objects:             objects to be printed out.
        :param minimum_debug_level: minimum debug level to print the passed objects.
        :param kwargs:              all the supported kwargs of this method are documented at the
                                    :func:`print_out() function <~.core.print_out>` of the :mod:`~ae.core` module
                                    (including the :paramref:`~.print_out.file` argument).

        this method has an alias named :meth:`.dpo`.
        """
        if self.debug_level >= minimum_debug_level:
            self.po(*objects, **kwargs)

    dpo = debug_out         #: alias of method :meth:`.debug_out`

    def verbose_out(self, *objects, **kwargs):
        """ special verbose debug version of :func:`builtin print() function <print>`.

        :param objects:         objects to be printed out.
        :param kwargs:          the :paramref:`~.core.AppBase.print_out.file` argument is documented at the
                                :meth:`~.core.AppBase.print_out` method of the :class:`~.core.AppBase` class. all other
                                supported kwargs of this method are documented at the
                                :func:`print_out() function <~.core.print_out>` of the :mod:`~.core` module.

        this method has an alias named :meth:`.vpo`.
        """
        if self.debug_level >= DEBUG_LEVEL_VERBOSE:
            self.po(*objects, **kwargs)

    vpo = verbose_out         #: alias of method :meth:`.verbose_out`

    def shutdown(self, exit_code: Optional[int] = 0, timeout: Optional[float] = None):
        """ shutdown this app instance and if it is the main app instance then also any created sub-app-instances.

        :param exit_code:       set application OS exit code - ignored if this is NOT the main app instance (def=0).
                                pass None to prevent call of sys.exit(exit_code).
        :param timeout:         timeout float value in seconds used for the thread termination/joining, for the
                                :class:`SubApp` shutdowns and for the acquisition of the threading locks of
                                :data:`the ae log file <log_file_lock>` and the :data:`app instances <app_inst_lock>`.
        """
        if self._shut_down:
            return
        aqc_kwargs: Dict[str, Any] = dict(blocking=False) if timeout is None else dict(timeout=timeout)
        is_main_app_instance = main_app_instance() is self
        force = is_main_app_instance and exit_code      # prevent deadlock on app error exit/shutdown

        if exit_code is not None:
            self.po(f"####  Shutdown {self.app_name}..........  {exit_code if force else ''} {timeout}", logger=_LOGGER)

        a_blocked = (False if force else app_inst_lock.acquire(**aqc_kwargs))
        if is_main_app_instance:
            _shut_down_sub_app_instances(timeout=timeout)
            if _MULTI_THREADING_ACTIVATED:
                _join_app_threads(timeout=timeout)

        l_blocked = (False if force else log_file_lock.acquire(**aqc_kwargs))

        self._flush_and_close_log_buf()
        self._close_log_file()
        if self._log_file_index:
            self._rename_log_file()

        if self._nul_std_out:
            if not self._nul_std_out.closed:
                self._append_eof_and_flush_file(self._nul_std_out, "NUL stdout")
                self._nul_std_out.close()
            self._nul_std_out = None

        if self.py_log_params:
            logging.shutdown()

        self._std_out_err_redirection(False)

        if l_blocked:
            log_file_lock.release()

        _unregister_app_instance(self.app_key)
        if a_blocked:
            app_inst_lock.release()
        self._shut_down = True
        if is_main_app_instance and exit_code is not None:
            sys.exit(exit_code)             # pragma: no cover (would break/cancel test run)

    def _std_out_err_redirection(self, redirect: bool):
        """ enable/disable the redirection of the standard output/error TextIO streams if needed.

        :param redirect:        pass ``True`` to enable or ``False`` to disable the redirection.
        """
        is_main_app_instance = main_app_instance() is self
        if redirect:
            if not isinstance(sys.stdout, _PrintingReplicator):  # sys.stdout==ori_std_out not works with pytest/capsys
                if not self.suppress_stdout:
                    std_out = ori_std_out
                elif self._nul_std_out and not self._nul_std_out.closed:
                    std_out = self._nul_std_out     # pragma: no cover - should never happen
                else:
                    std_out = self._nul_std_out = open(os.devnull, 'w')
                sys.stdout = cast(TextIO, _PrintingReplicator(sys_out_obj=std_out))
                sys.stderr = cast(TextIO, _PrintingReplicator(sys_out_obj=ori_std_err))
        else:
            if is_main_app_instance:
                sys.stderr = ori_std_err
                sys.stdout = ori_std_out

        if is_main_app_instance:
            if redirect:
                faulthandler.enable(file=sys.stdout)
            elif faulthandler.is_enabled():
                faulthandler.disable()  # pragma: no cover (badly testable - would cancel/break test runs)

    def _append_eof_and_flush_file(self, stream_file: TextIO, stream_name: str):
        """ add special end-of-file marker and flush the internal buffers to the file stream.

        :param stream_file:     file stream.
        :param stream_name:     name of the file stream (only used for debugging/error messages).
        """
        try:
            try:
                # cannot use print_out() here because of recursions on log file rotation, so use built-in print()
                print(file=stream_file)
                if self.debug:
                    print('EoF', file=stream_file)
            except Exception as ex:     # pragma: no cover - pylint: disable=broad-except
                self.po(f"Ignorable {stream_name} end-of-file marker exception={ex}", logger=_LOGGER)

            stream_file.flush()

        except Exception as ex:         # pylint: disable=broad-except
            self.po(f"Ignorable {stream_name} flush exception={ex}", logger=_LOGGER)

    def _flush_and_close_log_buf(self):
        """ flush and close ae log buffer and pass content to log stream if opened. """
        stream = self._log_buf_stream
        if stream:
            if self._log_file_stream:
                self._append_eof_and_flush_file(stream, "ae log buf")
                buf = stream.getvalue() + ("\n####  End Of Log Buffer" if self.debug else "")
                self._log_file_stream.write(buf)
            self._log_buf_stream = None
            stream.close()

    def _open_log_file(self):
        """ open the ae log file with path and file name specified by :attr:`_log_file_name`.

        tries to create a log sub-folder - if specified in :attr:`_log_file_name` and
        the folder does not exist (folder creation is limited to one folder level).

        .. note:: a already existing file with the same file name will be overwritten (file contents get lost!).
        """
        log_dir = os.path.dirname(self._log_file_name)
        if log_dir and not os.path.exists(log_dir):
            os.mkdir(log_dir)
        self._log_file_stream = open(self._log_file_name, "w", errors=DEF_ENCODE_ERRORS)

    def _close_log_file(self):
        """ close the ae log file. """
        if self._log_file_stream:
            stream = self._log_file_stream
            self._append_eof_and_flush_file(stream, "ae log file")
            self._log_file_stream = None
            stream.close()

    def _rename_log_file(self):
        """ rename rotating log file while keeping first/startup log and log file count below :data:`MAX_NUM_LOG_FILE`.
        """
        file_base, file_ext = os.path.splitext(self._log_file_name)
        dfn = f"{file_base}-{self._log_file_index:0>{LOG_FILE_IDX_WIDTH}}{file_ext}"
        if os.path.exists(dfn):
            os.remove(dfn)                              # remove old log file from previous app run
        if os.path.exists(self._log_file_name):         # prevent errors after log file error or unit test cleanup
            os.rename(self._log_file_name, dfn)

        self._log_file_index += 1
        if self._log_file_index > MAX_NUM_LOG_FILES:    # use > instead of >= to always keep first/startup log file
            first_idx = self._log_file_index - MAX_NUM_LOG_FILES
            dfn = f"{file_base}-{first_idx:0>{LOG_FILE_IDX_WIDTH}}{file_ext}"
            if os.path.exists(dfn):
                os.remove(dfn)


class SubApp(AppBase):
    """ separate/additional sub-app/thread/task with own/individual logging/debug configuration.

    create an instance of this class for every extra thread and task where your application needs separate
    logging and/or debug configuration - additional to the main app instance.

    all members of this class are documented at the :class:`AppBase` class.
    """
