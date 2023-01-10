from IPython.core.magic import (
    Magics,
    magics_class,
    line_magic,
    cell_magic,
    line_cell_magic,
)

import ast


def print_ast_or_ignore(src, src_name='cell'):
    try:
        print(ast.parse(src))
    except Exception:
        print(f"Couldn't parse this {src_name}")
        pass


# The class MUST call this class decorator at creation time
@magics_class
class MyMagics(Magics):
    @line_cell_magic
    def dispdag(self, line, cell=None):
        'Magic that works both as %lcmagic and as %%lcmagic'
        from meshed import code_to_dag

        src = cell or line  # take line if cell is None
        dag = code_to_dag(src)
        self.shell.user_ns[dag.__name__] = dag
        return dag.dot_digraph()

    @line_magic
    def lmagic(self, line):
        'my line magic'
        print('Full access to the main IPython object:', self.shell)
        print('')
        print(f'{dir(self.shell)=}')
        print('')
        print('Variables in the user namespace:', list(self.shell.user_ns.keys()))
        return line

    @cell_magic
    def cmagic(self, line, cell):
        'my cell magic'
        return line, cell

    @line_cell_magic
    def lcmagic(self, line, cell=None):
        'Magic that works both as %lcmagic and as %%lcmagic'
        if cell is None:
            # print("Called as line magic")
            print_ast_or_ignore(line, src_name='line')
            return line
        else:
            print('Called as cell magic')
            print_ast_or_ignore(cell, src_name='cell')
            return line, cell


# In order to actually use these magics, you must register them with a
# running IPython.


def load_ipython_extension(ipython):
    """
    Any module file that define a function named `load_ipython_extension`
    can be loaded via `%load_ext module.path` or be configured to be
    autoloaded by IPython at startup time.
    """
    # You can register the class itself without instantiating it.  IPython will
    # call the default constructor on it.
    ipython.register_magics(MyMagics)
