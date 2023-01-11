#!/usr/bin/env python3

###
# This module implements file construction using templates, data,
# and eventually hooks.
###


from typing import (
    Any,
    List,
    Union
)

import                 os
import                 shlex
from subprocess import run

from jinja2 import (
    BaseLoader,
    Environment,
    FileSystemLoader,
)

from .config    import *
from .jngconfig import *
from .jngdata   import *


# ------------------------------- #
# -- SPECIAL LOADER FOR JINJA2 -- #
# ------------------------------- #

###
# This class is used to work with string templates.
#
# ref::
#     * https://jinja.palletsprojects.com/en/3.0.x/api/#jinja2.BaseLoader
###
class StringLoader(BaseLoader):
    def get_source(self, environment, template):
        return template, None, lambda: True


# --------------------- #
# -- JINJANG BUILDER -- #
# --------------------- #

AUTO_FLAVOUR = ":auto-flavour:"


SPE_VARS = [
    'data',
    'template',
    'output',
]

SPE_VARS += [
    f'{name}_stem' for name in SPE_VARS
]


TERM_STYLE_DEFAULT = "\033[0m"
TERM_STYLE_INFO    = "\033[32m\033[1m"
TERM_STYLE_ERROR   = "\033[91m\033[1m"


_ERROR_KEY_TEMPLATE = "KeyError: '{e}'" + TERM_STYLE_ERROR + """

Following command has an unused key '{e}'.

  + RAW VERSION >  {command}{aboutcmd}
""".rstrip()


_ERROR_PROCESS = "\n{stderr}" + TERM_STYLE_ERROR + """
Following command has failed (see the lines above).

  + RAW VERSION
       > {command}

  + EXPANDED ONE
       > {command_expanded}{aboutcmd}
""".rstrip()


###
# This class allows to build either string, or file contents from ¨jinjang
# templates, data, and eventually hooks.
###
class JNGBuilder:
    _RENDER_LOC_VARS = [
        "flavour",
        "launch_py",
        "config",
        "verbose",
    ]

###
# prototype::
#     flavour   : this is to choose the dialect of a template.
#               @ flavour = AUTO_FLAVOUR
#                 or
#                 flavour in config.jngflavours.ALL_FLAVOURS
#     launch_py : the value ``True`` allows the execution of ¨python files
#                 suchas to build feeding data.
#                 Otherwise, no ¨python script will be launched.
#     config    : :see: jngconfig.JNGConfig
#     verbose   : the value ``True`` asks to show the outputs of external
#                 commands launched.
#                 Otherwise, these outputs will be hidden from the user.
###
    def __init__(
        self,
        flavour  : str  = AUTO_FLAVOUR,
        launch_py: bool = False,
        config   : Any  = NO_CONFIG,
        verbose  : bool = False,
    ) -> None:
        self.flavour = flavour
        self.config  = config
        self.verbose = verbose

# The update of ``launch_py`` implies the use of a new instance of
# ``self._build_data`` via ``JNGData(value).build``.
        self.launch_py = launch_py


###
# One getter, and one setter for ``config`` are used to secure the values
# used for this special attribut.
###
    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
# Case of a path for a specific config file.
        if value not in [AUTO_CONFIG, NO_CONFIG]:
            value = str(value)

# Nothing left to do.
        self._config = value


###
# One getter, and one setter for ``launch_py`` are used to secure the values
# used for this special attribut.
###
    @property
    def launch_py(self):
        return self._launch_py

    @launch_py.setter
    def launch_py(self, value):
        self._launch_py  = value
        self._build_data = JNGData(value).build


###
# One getter, and one setter for ``flavour`` are used to secure the values
# used for this special attribut.
###
    @property
    def flavour(self):
        return self._flavour

    @flavour.setter
    def flavour(self, value):
        if (
            value != AUTO_FLAVOUR
            and
            not value in ALL_FLAVOURS
        ):
            list_flavours = ', '.join([
                f"''{fl}''"
                for fl in ALL_FLAVOURS
            ])

            raise ValueError(
                f"flavour ''{value}'' is neither AUTO_FLAVOUR, "
                f"not one of {list_flavours}."
            )

        self._flavour = value


###
# prototype::
#     data     : data feeding the template.
#     template : one template.
#
#     :return: the output made by using ``data`` on ``template``.
###
    def render_frompy(
        self,
        data    : dict,
        template: str
    ) -> str:
# With ¨python variable, we can't detect automatically the flavour.
        if self.flavour == AUTO_FLAVOUR:
            raise ValueError(
                "no ''auto-flavour'' when working with strings."
            )

# A dict must be used for the values of the ¨jinjang variables.
        if not isinstance(data, dict):
            raise TypeError(
                "''data'' must be a ''dict'' variable."
            )

# Let's wirk!
        jinja2env        = self._build_jinja2env(self.flavour)
        jinja2env.loader = StringLoader()

        jinja2template = jinja2env.get_template(template)
        content        = jinja2template.render(data)

        return content


###
# prototype::
#     data     : data feeding the template.
#     template : one template.
#              @ exists path(str(template))
#     output   : the file used for the output build after using ``data``
#                on ``template``.
#     flavour  : if the value is not ``None``, a local value is used
#                without deleting the previous one.
#                :see: self.__init__
#     launch_py: if the value is not ``None``, a local value is used
#                without deleting the previous one.
#                :see: self.__init__
#     config   : if the value is not ``None``, a local value is used
#                without deleting the previous one.
#                :see: self.__init__
#     verbose  : if the value is not ``None``, a local value is used
#                without deleting the previous one.
#                :see: self.__init__
#
#     :action: the file ``output`` is built by using ``data`` on
#              ``template``, while respecting any additional behaviour
#              specified.
###
    def render(
        self,
        data     : Any,
        template : Any,
        output   : Any,
        flavour  : Union[str, None]  = None,
        launch_py: Union[bool, None] = None,
        config   : Any               = None,
        verbose  : Union[bool, None] = None,
    ) -> None:
# Local settings.
        oldsettings = dict()

        for param in self._RENDER_LOC_VARS:
            val = locals()[param]

            if val is not None:
                oldsettings[param] = getattr(self, param)
                setattr(self, param, val)

# What is the flavour to use?
        if self.flavour == AUTO_FLAVOUR:
            flavour = self._auto_flavour(template)

        else:
            flavour = self.flavour

# `Path` version of the paths.
        for name, val in {
            'data'    : data,
            'template': template,
            'output'  : output,
        }.items():
            val = Path(str(val))
            setattr(self, f"_{name}", val)

            val = val.parent / val.stem
            setattr(self, f"_{name}_stem", val)

        self._template_parent = self._template.parent

# Configs used for hooks.
        self._dict_config = build_config(
            config = self.config,
            parent = self._template_parent
        )

# Pre-hooks?
        self._pre_hooks()

# Let's go!
        jinja2env        = self._build_jinja2env(flavour)
        jinja2env.loader = FileSystemLoader(
            str(self._template_parent)
        )

        jinja2template = jinja2env.get_template(
            str(self._template.name)
        )

        dictdata = self._build_data(self._data)
        content  = jinja2template.render(dictdata)

        output.write_text(
            data     = content,
            encoding = "utf-8",
        )

# Post-hooks?
        self._post_hooks()

# Restore previous settings if local ones have been used.
        for param, oldval in oldsettings.items():
            setattr(self, param, oldval)


###
# prototype::
#     template : the path of a template.
#
#     :return: the flavour to be used on ``template``.
###
    def _auto_flavour(
        self,
        template: Path
    ) -> str:
        flavour_found = FLAVOUR_ASCII

        for flavour, extensions in ASSOCIATED_EXT.items():
            if flavour == FLAVOUR_ASCII:
                continue

            for glob_ext in extensions:
                if template.match(glob_ext):
                    flavour_found = flavour
                    break

            if flavour_found != FLAVOUR_ASCII:
                break

        return flavour_found


###
# prototype::
#     flavour : an exiting dialect.
#             @ flavour in config.jngflavours.ALL_FLAVOURS
#
#     :return: a ``jinja2.Environment`` that will create the final output.
###
    def _build_jinja2env(
        self,
        flavour: str
    ) -> Environment:
        return Environment(
            keep_trailing_newline = True,
            **JINJA_TAGS[flavour]
        )


###
# prototype::
#     :action: launching of pre-processing
###
    def _pre_hooks(self) -> None:
        self._some_hooks(TAG_PRE)


###
# prototype::
#     :action: launching of post-processing
###
    def _post_hooks(self) -> None:
        self._some_hooks(TAG_POST)


###
# prototype::
#     kind : the kind of external processing.
#
#     :action: launching of external processing
###
    def _some_hooks(self, kind: str) -> None:
        if not TAG_HOOKS in self._dict_config:
            return None

        self.launch_commands(
            kind = f"{TAG_HOOKS}/{kind}",
            loc  = self._dict_config[TAG_HOOKS][kind]
        )


###
# prototype::
#     kind   : the kind of processing
#     loc    : [l]-ist [o]-f [c]-ommands to execute
#     frompy : ``True`` indicates the use of the method within a ¨python
#              script.
#              Otherwise, the method is used in a "command line" context.
#
#     :action: attempt to execute all commands in ``loc``.
###
    def launch_commands(
        self,
        kind  : str,
        loc   : List[str],
        frompy: bool = False
    ) -> None:
        if not loc:
            return None

# Lets' try to build expanded version of each command, and then execute it.
        savedwd = os.getcwd()
        os.chdir(str(self._template_parent))

        tochange = {
            sv: str(getattr(self, f"_{sv}"))
            for sv in SPE_VARS
        }

        for nbcmd, command in enumerate(loc, 1):
            aboutcmd = self._about_command(nbcmd, kind, frompy)

            try:
                command_expanded = command.format(**tochange)

            except KeyError as e:
                raise Exception(
                    _ERROR_KEY_TEMPLATE.format(
                        command  = command,
                        e        = e,
                        aboutcmd = aboutcmd
                    )
                )

            try:
                self._print_info(
                     "Launching"
                     "\n"
                    f"  > {command_expanded}"
                )

                listcmd = shlex.split(command_expanded)

                r = run(
                    listcmd,
                    check          = True,
                    capture_output = True,
                    encoding       = "utf-8"
                )

                if self.verbose:
                    print(r.stdout)

            except Exception as e:
                raise Exception(
                    _ERROR_PROCESS.format(
                        command          = command,
                        command_expanded = command_expanded,
                        stderr           = getattr(e, 'stderr', e),
                        aboutcmd         = aboutcmd
                    )
                )

        os.chdir(savedwd)

# No problem met.
        howmany = "One" if nbcmd == 1 else nbcmd
        plurial = ""    if nbcmd == 1 else "s"

        self._print_info(f"{howmany} command{plurial} launched with success.")


###
# prototype::
#     nbcmd  : the rank of the command
#     kind   : :see: self.launch_commands
#     frompy : :see: self.launch_commands
#
#     :return: an empty string if ``frompy = True``.
#              Otherwise, a message indicates the block used in the
#              path::``YAML`` configuration file, as well as the rank of
#              the command.
###
    def _about_command(
        self,
        nbcmd : int,
        kind  : str,
        frompy: bool
    ) -> str:
        if frompy:
            return ""

        return f"\n\nSee the block '{kind}', and the command #{nbcmd}."


###
# prototype::
#     message : one message for the user
#
#     :action: display in bold green of the message in the terminal
###
    def _print_info(self, message: str) -> None:
        print(TERM_STYLE_INFO + message + TERM_STYLE_DEFAULT)
        print()
