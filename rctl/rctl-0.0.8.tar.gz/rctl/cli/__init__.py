import logging
import os
import subprocess
logger = logging.getLogger("rctl")

class RctlParserError(Exception):
    """Base class for CLI parser errors."""
    def __init__(self):
        super().__init__("Parser error")

class RctlValidReqError(Exception):
    def __init__(self, msg, *args):
        assert msg
        self.msg = msg
        super().__init__(msg, *args)

def parse_args(argv=None):
    from .parser import get_main_parser

    parser = get_main_parser()
    args = parser.parse_args(argv)
    args.parser = parser
    return args

def valid_requirement():
    try:        
        subprocess.run(['mc', '--version'], capture_output=True)
    except OSError as err:        
        raise RctlValidReqError('minio cli not found! Please install minio cli')
    try:        
        subprocess.run(['gh', '--version'], capture_output=True)
    except OSError as err:        
        raise RctlValidReqError('git hub cli not found! Please install git hub cli')
    try:        
        subprocess.run(['git', '--version'], capture_output=True)
    except OSError as err:        
        raise RctlValidReqError('git not found! Please install git')
        
    if not os.environ.get("GH_TOKEN"):
        raise RctlValidReqError("Error: GH_TOKEN not found. Please add GH_TOKEN Environment Variable")
    
    if not os.environ.get("MINIO_ENDPOINT"):
        raise RctlValidReqError("Error: MINIO_ENDPOINT not found. Please add GH_TOKEN Environment Variable")

    if not os.environ.get("MINIO_SECRET_ACCESS_KEY"):
        raise RctlValidReqError("Error: MINIO_SECRET_ACCESS_KEY not found. Please add MINIO_SECRET_ACCESS_KEY Environment Variable")

    if not os.environ.get("MINIO_ACCESS_KEY_ID"):
        raise RctlValidReqError("Error: MINIO_ACCESS_KEY_ID not found. Please add MINIO_ACCESS_KEY_ID Environment Variable")

def main(argv=None):
    try:
        valid_requirement()
        args = parse_args(argv)
        cmd = args.func(args)
        cmd.do_run()
    except KeyboardInterrupt as exc:
        logger.exception(exc)
    except RctlParserError as exc:
        # logger.error(exc)
        ret = 254
    except RctlValidReqError as exc:
        print(exc.msg)
    except Exception as exc:  # noqa, pylint: disable=broad-except
       logger.exception(exc)
    
