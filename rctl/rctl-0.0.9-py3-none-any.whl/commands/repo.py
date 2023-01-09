import argparse
import logging
import os

from rctl.cli.command import CmdBase
from rctl.cli.utils import run_command_on_subprocess, repo_name_valid
from rctl.cli import RctlValidReqError
logger = logging.getLogger(__name__)

"""
----------------------------
***Bucket Name Validation***
----------------------------
Bucket names should not contain upper-case letters
Bucket names should not contain underscores (_)
Bucket names should not end with a dash
Bucket names should be between 3 and 63 characters long
Bucket names cannot contain dashes next to periods (e.g., my-.bucket.com and my.-bucket are invalid)
Bucket names cannot contain periods - Due to our S3 client utilizing SSL/HTTPS, Amazon documentation indicates that a bucket name cannot contain a period, otherwise you will not be able to upload files from our S3 browser in the dashboard.
"""
     

def create_repo(args):
    repository_name = args.name                    
    run_command_on_subprocess("mc mb --with-lock local/{}".format(repository_name))
    print(f"MINIO Bucket: {repository_name}")
    run_command_on_subprocess("gh repo create {} --private --clone".format(repository_name))
    print(f"Git Repository: {repository_name}")
    run_command_on_subprocess("dvc init", repository_name)    
    run_command_on_subprocess("dvc remote add -d minio s3://{} -f".format(repository_name), repository_name)  
    print("DVC remote added")  
    run_command_on_subprocess("dvc remote modify minio endpointurl {}".format(os.environ.get("MINIO_ENDPOINT")), repository_name)    
    print("DVC endpointurl {} added".format(os.environ.get("MINIO_ENDPOINT")))  
    run_command_on_subprocess("dvc remote modify minio secret_access_key {}".format(os.environ.get("MINIO_SECRET_ACCESS_KEY")), repository_name)    
    print("MINIO Access key added")  
    run_command_on_subprocess("dvc remote modify minio access_key_id {}".format(os.environ.get("MINIO_ACCESS_KEY_ID")), repository_name)    
    print("MINIO Access key id added")   
    run_command_on_subprocess("dvc config core.autostage true", repository_name)   
    run_command_on_subprocess("git commit -m 'Init DVC' -a", repository_name)    
    run_command_on_subprocess("git branch -M master", repository_name)    
    run_command_on_subprocess("git push --set-upstream origin master", repository_name)  
    print("Git pushed to master")        
    print("Repository has been created. `cd {}`".format(repository_name))

def clone_repo(args):
    repository_name = args.name     
    print('Git being clone...')
    run_command_on_subprocess("gh repo clone {}".format(repository_name), None, True)       


class CmdRepo(CmdBase):
    def __init__(self, args):
        super().__init__(args)        
        if getattr(self.args, "name", None):
            self.args.name = self.args.name.lower()            
            repo_name_valid(self.args.name)
        else:
            raise RctlValidReqError("Error: Please provide a valid name, -n")
class CmdRepoCreate(CmdRepo):
    def run(self):             
        if self.args.create:
            create_repo(self.args)
        if self.args.clone:
            clone_repo(self.args)                                    
        return 0


def add_parser(subparsers, parent_parser):
    REPO_HELP = "Create a new repository."
    REPO_DESCRIPTION = (
        "Create a new repository."
    )

    repo_parser = subparsers.add_parser(
        "repo",
        parents=[parent_parser],
        description=REPO_DESCRIPTION,
        help=REPO_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    repo_parser.add_argument(
        "-create",
        "--create",
        action="store_true",
        default=False,
        help="Create new repo",
    )

    repo_parser.add_argument(
        "-clone",
        "--clone",
        action="store_true",
        default=False,
        help="Clone new repo",
    )

    repo_parser.add_argument(
        "-n", 
        "--name", 
        nargs="?", 
        help="Name of the repo",
    )
    
    repo_parser.set_defaults(func=CmdRepoCreate)
