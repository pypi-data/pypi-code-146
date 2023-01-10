import importlib
import inspect
import os
import typing

from remotemanager.storage.sendablemixin import SendableMixin
from remotemanager.utils.uuid import generate_uuid
from remotemanager.logging import LoggingMixin


_SCRIPT_TEMPLATE = """
{function}

if __name__ == '__main__':    
\tkwargs = {args}

\tresult = {name}(**kwargs)
"""


class Function(SendableMixin, LoggingMixin):
    """
    Serialise function to an executable python file for transfer

    Args:
        func:
            python function for serialisation
    """
    def __init__(self,
                 func: typing.Callable):

        self._logger.debug(f'creating new serialisable function for {func}')

        self._uuid = ''
        try:
            source = inspect.getsource(func)
            source = source.replace('@RemoteFunction', '').strip()

            self._signature = Function.prepare_signature(
                inspect.signature(func))

            self._logger.debug(f'updated signature to {self._signature}')
            rawsig = Function.get_raw_signature(source)
            self._logger.debug(f'raw typed signature detected as'
                               f' {self._signature}')
            source = source.replace(rawsig, self._signature, 1)

            self._source = source
            self._fname = func.__name__
        except TypeError as e:
            if isinstance(func, str):
                self._source = func
                self._fname = "f"
            else:
                raise e
        self._uuid = generate_uuid(self._source)

    def __call__(self, *args, **kwargs):
        return self.object(*args, **kwargs)

    @staticmethod
    def get_raw_signature(source):
        """
        Strips the signature as it is typed.
        inspect.signature does some formatting which can cause replacement to
        break in some conditions

        Args:
            source (str):
                raw source

        Returns:
            (str): raw signature as typed
        """
        definition = []
        for line in source.split('\n'):
            # we need to split from the function name for the raw signature
            if '(' in line:
                # split from first ( and up,
                # then join for any tuples defined as default
                line = '(' + '('.join(line.split('(')[1:])

            # appending the final ":" causes issues, strip that in a safe
            # manner then append
            definition.append(':'.join(line.split(':')[:-1]))

            # we've reached the end of the definition
            if line.endswith(':'):
                break

        return '\n'.join(definition)

    @staticmethod
    def prepare_signature(sig) -> str:
        """
        Inserts *args and **kwargs into any signature that does not already
        have it

        Args:
            sig:
                inspect.signature(func)

        Returns:
            (str): formatted sig
        """

        args = [str(a) for a in sig.parameters.values()]

        if '*args' not in args:
            if '**kwargs' in args:
                args.insert(-1, '*args')
            else:
                args.append('*args')

        if '**kwargs' not in args:
            args.append('**kwargs')

        return f'({", ".join(args)})'

    @property
    def name(self):
        """
        Function name
        """
        return self._fname

    @property
    def raw_source(self):
        """
        Function source
        """
        return self._source

    @property
    def source(self):
        """
        Function source

        Returns:
            (str): source code
        """
        return self._source

    @property
    def signature(self):
        return self._signature

    @property
    def uuid(self):
        """
        Function uuid (64 characters)
        """
        return self._uuid

    @property
    def object(self):
        """
        Recreates the function object by writing out the source, and importing.

        Returns:
            typing.Callable:
                the originally passed function
        """

        tmp_file = ''
        try:
            tmp_file = os.path.abspath(f'{self.uuid}.py')

            with open(tmp_file, 'w+') as o:
                o.write(self.source)

            func_module = importlib.import_module(self.uuid)
            func_object = getattr(func_module, f'{self.name}')

        finally:
            os.remove(tmp_file)

        return func_object

    def dump_to_string(self, args):
        """
        Dump this function to a serialised string, ready to be written to a
        python file

        Args:
            args (dict):
                arguments to be used for this dumped run

        Returns:
            (str):
                serialised file
        """

        if args is None:
            args = {}

        return _SCRIPT_TEMPLATE.format(**{'function': self.source,
                                          'name': self.name,
                                          'args': args})
