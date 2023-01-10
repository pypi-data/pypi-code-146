import subprocess
from rctl.cli import RctlValidReqError

def fix_subparsers(subparsers):
    subparsers.required = True
    subparsers.dest = "cmd"

def run_command_on_subprocess(command, cwd=None, err_skip=False):
    if cwd:
        result = subprocess.run(command, capture_output=True, shell=True, cwd=cwd)
        stderr = str(result.stderr, 'UTF-8')
        stdout = str(result.stdout, 'UTF-8')
        if stdout:                        
            print(stdout) 
            return True

        if stderr:            
            if not err_skip:
                raise RctlValidReqError(stderr)
            else:
                print(stderr)
                
    else:
        result = subprocess.run(command, capture_output=True, shell=True)
        stderr = str(result.stderr, 'UTF-8')
        stdout = str(result.stdout, 'UTF-8')
        if stdout:                        
            print(stdout) 
            return True

        if stderr:            
            if not err_skip:
                raise RctlValidReqError(stderr)
            else:
                print(stderr)
                

def repo_name_valid(name):
    for c in name:        
        if c == '_':
            raise RctlValidReqError("Error: Bucket name contains invalid characters")
    if len(name) <3 or len(name)>63:
        raise RctlValidReqError("Error: Bucket names should be between 3 and 63 characters long")   