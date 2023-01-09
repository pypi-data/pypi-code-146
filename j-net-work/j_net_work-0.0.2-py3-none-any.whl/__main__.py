# When run as a module, eg
#   python -m net_work [args]
# we pass args to `net_work.run_server`
# which waits for incoming tasks to a directory,
# executes them, and writes results to another directory.
import sys
import net_work
#net_work.run_server(sys.argv)
net_work.run_gui_server(sys.argv)
