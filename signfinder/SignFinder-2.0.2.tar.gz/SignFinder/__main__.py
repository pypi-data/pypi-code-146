# SignFinder2 by d3ranged (d3ranged_blog@proton.me)


import os
import sys


if sys.version_info < (3, 8):
	print('\n\tSF2 requires Python 3.8+\n')
	sys.exit()

try:
	__import__('rich')
	__import__('prompt_toolkit')
except ImportError:
	print('\n\tpip install requirements.txt\n')
	sys.exit()


from .core import *


def cli_start():

	core_inst = SF_CORE(__file__)

	try:

		core_inst.init_core()
		core_inst.start_cli()

	except SystemExit:

		pass

	except ValueError as valid_err:

		core_inst.repl.enable()
		core_inst.repl.ecrror(valid_err)

	except PermissionError as error:

		core_inst.repl.enable()
		core_inst.repl.error(f'Permission denied:  {error.filename}')
		core_inst.repl.status(f'Set permission or SF_WORK_DIR -> user_config.py')

	except:

		core_inst.repl.console.print_exception()
		core_inst.repl.new_line()
		core_inst.repl.status(f'Please, report it -> https://github.com/d3ranged/sf2/issues\n')


if __name__ == '__main__':
	
	cli_start()

