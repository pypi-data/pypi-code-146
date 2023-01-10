import inspect

from remotemanager import URL
from remotemanager.storage.sendablemixin import SendableMixin


class BaseComputer(URL):
    """
    Base computer module for HPC connection management.

    Extend this class for connecting to your machine

    Adds `module_purge`, set to False to ignore the pre-module
    `module purge` call.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.shebang = '#!/bin/bash'
        self.pragma = NotImplemented

        self.module_purge = kwargs.get('module_purge', True)

        self.modules = kwargs.get('modules', [])

        self.extra = None

    def __setattr__(self, key, value):
        """
        If the set `key` attribute is an MPI option, instead set the `value`
        of that attribute

        Args:
            key:
                attribute name to set
            value:
                value to set to

        Returns:
            None
        """
        if key in self.__dict__:
            if isinstance(getattr(self, key), (optional, required)):
                getattr(self, key).value = value
                return

        object.__setattr__(self, key, value)

    @property
    def arguments(self):
        return [k for k, v in self.__dict__.items()
                if isinstance(v, (optional, required))]

    @property
    def argument_dict(self):
        return {k.strip(): getattr(self, k) for k in self.arguments}

    @property
    def required(self):
        """
        Returns the required arguments
        """

        # grab the required arguments for the class, and fill with placeholders
        # of the correct type
        params = inspect.signature(self.__class__).parameters
        required_args = {}
        for arg_name, v in params.items():
            if v.default is inspect._empty and arg_name != 'kwargs':
                required_args[arg_name] = v.annotation

        if 'dummy' in params.keys():
            required_args['dummy'] = True

        temp = self.__class__(**required_args)
        return [k for k, v in temp.__dict__.items() if isinstance(v, required)]

    @property
    def missing(self):
        """
        Returns the currently missing arguments
        """
        return [k for k in self.required if not getattr(self, k)]

    @property
    def valid(self):
        return len(self.missing) == 0

    def update_resources(self, **kwargs):
        """
        Set any arguments passed to the script call

        Args:
            **kwargs:
                kwarg updates e.g. mpi=128
        Returns:
            None
        """
        for k, v in kwargs.items():
            setattr(self, k, v)

    def resources_block(self, **kwargs):

        if 'name' in kwargs:
            # Dataset `name` param detected, use as a default
            if not hasattr(self, 'jobname') or 'jobname' not in kwargs:
                kwargs['jobname'] = kwargs.pop('name')

        self.update_resources(**kwargs)

        if not self.valid:
            raise RuntimeError(f'missing required arguments: {self.missing}')

        options = {}
        for k, v in self.argument_dict.items():
            if v:
                options[v.flag] = v.value

        return [f'{self.pragma} {k}={v}'
                for k, v in sorted(options.items()) if v]

    def modules_block(self):
        base = []
        if self.module_purge:
            base.append('\nmodule purge')
        return base + [f'module load {m}' for m in self.modules]

    def script(self,
               **kwargs) -> str:
        """
        Takes job arguments and produces a valid jobscript

        Returns:
            (str):
                script
        """
        script = [self.shebang]

        script += self.resources_block(**kwargs)
        script += self.modules_block()

        if hasattr(self, 'postscript') and self.postscript is not None:
            script.append(self.postscript)

        if hasattr(self, 'extra') and self.extra is not None:
            script.append(self.extra)

        return '\n'.join(script)


class placeholder_option(SendableMixin):
    """
    .. warning::
        This class is intended to be subclassed by the optional and required
        placeholders.

    Stub class to sit in place of an option within a computer.

    Args:
        mode (string):
            storage mode, required or optional
        flag (string):
            flag to append value to (`--nodes`, `--walltime`, etc)
    """

    def __init__(self, mode, flag):
        self._mode = mode
        self._flag = flag
        self._value = None
        self._bool = False

    def __hash__(self):
        return hash(self._mode)

    def __str__(self):
        return str(self.value)

    def __bool__(self):
        """
        Makes objects "falsy" if no value has been set, "truthy" otherwise
        """
        return self.value is not None

    @property
    def flag(self):
        return self._flag

    @property
    def value(self):
        if hasattr(self, '_default') and self._value is None:
            return self._default
        return self._value

    @value.setter
    def value(self, value):
        self._bool = True
        self._value = value


class required(placeholder_option):
    """
    .. warning::
        This class is intended to be subclassed by the optional and required
        placeholders.

    Stub class to sit in place of an option within a computer.

    This option is _required_, and should raise an error if no value is found

    Args:
        flag (string):
            flag to append value to (`--nodes`, `--walltime`, etc)
    """

    def __init__(self, flag):
        super().__init__('required', flag)


class optional(placeholder_option):
    """
    .. warning::
        This class is intended to be subclassed by the optional and required
        placeholders.

    Stub class to sit in place of an option within a computer.

    This option is not required, and should have an accessible default if
    no value is found

    Args:
        flag (string):
            flag to append value to (`--nodes`, `--walltime`, etc)
        default:
            default value to use if none is assigned
    """

    def __init__(self, flag, default=None):
        super().__init__('optional', flag)

        self._default = default

    @property
    def default(self):
        return self._default
