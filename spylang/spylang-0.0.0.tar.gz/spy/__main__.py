import sys
import os
import pathlib

USAGE = """
Usage:
    python -m spy compile FILE
    python -m spy dump_ir
"""

def spy_compile(filename):
    """
    XXX the following is a completely hackish and demo implementation, written
    in 5 minutes just to have something which works. Refactor me please.
    """
    import spy.parser
    import spy.vm
    from spy.backend import compile_module_to_wat
    import sexpdata

    with open(filename) as f:
        src = f.read()

    w_mod = spy.parser.parse(src)
    w_mod = spy.vm.meta_eval(w_mod)
    wat = compile_module_to_wat(w_mod)
    tmpwat = '/tmp/' + filename + '.wat'
    with open(tmpwat, 'w') as f:
        f.write(wat)

    wasm = pathlib.Path(filename).with_suffix('.wasm')
    os.system(f'wat2wasm {tmpwat} -o {wasm}')


def dump_ir():
    from spy import ir
    print(ir.extend.dump_skeleton())

def main():
    if len(sys.argv) == 3 and sys.argv[1] == 'compile':
        return spy_compile(sys.argv[2])

    if len(sys.argv) == 2 and sys.argv[1] == 'dump_ir':
        return dump_ir()

    print(USAGE)

if __name__ == '__main__':
    main()
