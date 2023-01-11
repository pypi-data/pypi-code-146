#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# __aml_shim__.py: AML wants to run a python script, so we use this to launch on shell/batch script
import sys
import os

# don't take on any XTLIB dependencies here (it may only be installed while processing the target setup cmds)

# MAIN code
args = sys.argv[1:]
print("__aml_shim__: args=", args)

cmd = args[0]    # all are passed as a logical string (but args[1] is "1", so don't use that)
print("__aml_shim__: about to run cmd=", cmd)
os.system(cmd)
