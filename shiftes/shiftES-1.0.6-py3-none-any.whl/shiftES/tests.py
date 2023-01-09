#!/usr/bin/env python
import pkg_resources
from shiftES.shift_effectsize import parse_args, run_from_cmdline

if __name__ == '__main__':
    filepath = lambda fn: pkg_resources.resource_filename(__name__, f'test_files/{fn}')
    # need to test:
    # * csv/tsv/xlsx headed/headerless
    # * auto detection of file types
    # * xlsx sheets
    # * output file

    testargs = {
        'csv headed ALL': f"{filepath('test_data.csv')} ALL ALL",
        'tsv no head, specific cols, write tst.out': f"{filepath('test_data.nohead.tsv')} 1,2 3,4 -o tst.out --no-head",
        'xlsx, confidence intervals':f"{filepath('test.excel.xlsx')} 1 2 --no-head --ci --type x --nboot 100 --sheet 2",
        #'Expected to fail opening .xlsx as .csv':f"{filepath('test.excel.xlsx')} 1 2 --type c"
    }

    fails = []
    for desc, argstr in testargs.items():
        print(f"Testing: {desc}\nArguments: {argstr}")
        try:
            args = parse_args(argstr.split())
            print('Args parsed, running...')
            run_from_cmdline(args)
            print('Ran okay\n')

        except Exception as e:
            fails.append(e)
            print('Failed\n'
                  f'Error: {str(e)}')
            raise e

    print('Printing output file:')
    with open('tst.out') as f:
        for line in f:
            print(line, end='')

