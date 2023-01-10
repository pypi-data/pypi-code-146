import time

from remotemanager.logging import LoggingMixin
from remotemanager import Dataset

from IPython.core.magic import (Magics, magics_class,
                                cell_magic, needs_local_scope)


@magics_class
class RCell(Magics, LoggingMixin):
    """
    Magic function that allows running an ipython cell on a remote machine
    with minimal lines of code.
    """
    @cell_magic 
    @needs_local_scope
    def execute_remotely(self,
                         line: str,
                         cell: str,
                         local_ns: dict) -> None:
        """
        Execute a jupyter cell using an implicit remote Dataset

        Args:
            line:
                magic line, includes arguments for cell and Dataset
            cell:
                Cell contents
            local_ns:
                dict containing current notebook runtime attributes
        """
        fstr, args, fargs = self.parse_line(line, cell, local_ns)

        self._logger.info(f'generated function string {fstr}')
        # Build the runner and run
        ds = Dataset(function=fstr, block_reinit=False, **args)
        ds.append_run(args=fargs)
        ds.run()

        for cmd in ds.run_cmds:
            if cmd.stderr:
                raise RuntimeError(f'error detected in magic run: '
                                   f'{cmd.stderr}')
        while not ds.all_finished:
            time.sleep(1)
        ds.fetch_results()

        local_ns['magic_dataset'] = ds

    def parse_line(self,
                   line: str,
                   cell: str,
                   local_ns: dict):

        self._logger.info(f'creating magic cell with line {line}')
        # Extract arguments from the line
        args = {}
        fargs = {}
        foundc = False
        # iterate through line, switching from runtime args to function args
        # on hitting the split token ":"
        for token in line.split():
            if token == ":":
                foundc = True
                continue
            elif token == '#':
                break
            k, v = token.split("=")
            if foundc:
                fargs[k] = local_ns[v]
            else:
                args[k] = local_ns[v]

        # Build function string
        fstr = "def f("
        if fargs:
            fstr += ", ".join(list(fargs)) + ", "
        fstr += "):\n"
        for c in cell.split("\n"):
            fstr += "  " + c + "\n"

        return fstr, args, fargs
