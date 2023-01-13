import argparse
import importlib.util
import logging
import sys
from typing import List

from jumonc import reset_logging as reset_logger
from jumonc import settings
from jumonc.models import planed_tasks


logger = logging.getLogger(__name__)



def parseCMDOptions(args: List[str] = None) -> None:
    if args is None:
        args = []

    parser = setupParser()
    evaluateArgs(parser, args)



def setupParser() -> argparse.ArgumentParser:
    #pylint: disable=import-outside-toplevel
    from jumonc._version import __DB_version__, __REST_version__, REST_version_info, __version__
    #pylint: enable=import-outside-toplevel

    parser = argparse.ArgumentParser(description=("jumonc is the Jülich Monitoring and Control programm, "
                                                  "it allows to monitore your running simulations and access avaiable data using a REST-API"),
                                     prog="app.py",)

    parser.add_argument("--CACHE-DEFAULT-ENTRIES-PER-PAGE".lower() ,
                       dest="CACHE_DEFAULT_ENTRIES_PER_PAGE",
                       help="Number of cache entries that are on one page of /cache/list by default",
                       default=10,
                       type=int)
    parser.add_argument("--DATETIME-FORMAT".lower() ,
                       dest="DATETIME_FORMAT",
                       help=("Datetime format that will be used in the REST-API, "
                           "see: https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior"),
                       default="%d.%m.%Y, %H:%M:%S",
                       type=str)
    parser.add_argument("--DB-PATH".lower() ,
                       dest="DB_PATH",
                       help=("Path and filename to either an existing jumonc database, that will be used, or a new one that will be created"),
                       default="jumonc.db",
                       type=str)
    parser.add_argument("--DISABLE-SCHEDULED-TASKS".lower(),
                       dest="SCHEDULED_TASKS_ENABLED",
                       help="Allows to disable the execution and REST-API paths used for task scheduling",
                       default=True,
                       action='store_false')
    parser.add_argument("--DONT-DEFAULT-TO-HUMAN-READABLE-NUMBERS".lower(), 
                       dest="DONT_DEFAULT_TO_HUMAN_READABLE_NUMBERS", 
                       help="Sets wether numbers are converted into smaller numbers by default, can be overwritten for each API call", 
                       default=True, 
                       action='store_false')
    parser.add_argument("--FLASK-DEBUG".lower(), 
                       dest="FLASK_DEBUG", 
                       help=("If used enable Flask debugging. As this is a security risk, because it always the execution of python code, "
                       "this will set the --LOCAL-ONLY flag as well"), 
                       default=False, 
                       action='store_true')
    parser.add_argument("--INIT-FILE".lower() ,
                       dest="INIT_FILE",
                       help=(("Path and filename to an init file, to overwrite settings. This file will be imported and allows abitrary code execution. "
                              "Only use trustworthy sources for this init file. "
                              "The settings from the init File take priority over all CMD arguments and will not be verified for correctness. "
                              "All possible values (with their default values): "
                              "https://gitlab.jsc.fz-juelich.de/coec/jumonc/-/blob/main/jumonc/settings/__init__.py "
                              "An example init file can be seen at: https://gitlab.jsc.fz-juelich.de/coec/jumonc/-/blob/main/doc/CMD/init_jumonc.py ")),
                       default=None,
                       type=str)
    parser.add_argument("--LOCAL-ONLY".lower(), 
                       dest="LOCAL_ONLY", 
                       help="If used the REST-API will only be available from localhost", 
                       default=False, 
                       action='store_true')
    parser.add_argument("--LOG-FORMAT".lower(), 
                       dest="LOG_FORMAT", 
                       help=("Set log format, usable values are the values supported by logging"
                       "(https://docs.python.org/3/howto/logging.html#)"),
                       default="[%(asctime)s][PID:%(process)d][%(levelname)s][%(name)s] %(message)s", type=ascii)
    parser.add_argument("--LOG-LEVEL".lower(), 
                       dest="LOG_LEVEL", 
                       help="Set the log level used by the logging", 
                       default="INFO", 
                       type=ascii, 
                       choices=["'ERROR'", "'WARN'", "'INFO'", "'DEBUG'"])
    parser.add_argument("--LOG-STDOUT".lower(), 
                       dest="LOG_STDOUT", 
                       help="If used log to stdout, otherwise to stderr", 
                       default=False, 
                       action='store_true')
    parser.add_argument("--LOG-PREFIX".lower(), 
                       dest="LOG_PREFIX", 
                       help="Set a prefix that will be prefaced to every logging output", 
                       default="", 
                       type=ascii)
    parser.add_argument("--MAX-WORKER-THREADS".lower(), 
                       dest="MAX_WORKER_THREADS", 
                       help="Limits the number of worker threads that work on the actual tasks at once", 
                       default=4, 
                       type=int)
    parser.add_argument("--ONLY-CHOOSEN-REST-API-VERSION".lower(), 
                       dest="ONLY_CHOOSEN_REST_API_VERSION", 
                       help="If set will only provide one version of the api links", 
                       default=False, 
                       action='store_true')
    parser.add_argument("--PENDING-TASKS-SOFT-LIMIT".lower(), 
                       dest="PENDING_TASKS_SOFT_LIMIT", 
                       help="Limits tasks being added by the REST-API, to not have more than PENDING-TASKS-SOFT-LIMIT tasks waiting", 
                       default=100, 
                       type=int)
    parser.add_argument("--PLUGIN-PATHS".lower(), 
                       dest="PLUGIN_PATHS", 
                       help="Paths to jumonc plugins, multiple values allowed", 
                       default=[],
                       nargs='*',
                       type=str)
    parser.add_argument("-p", "--REST-API-PORT".lower(), 
                       dest="REST_API_PORT", 
                       help="Choose a port that the REST-API will be listening on", 
                       default=12121, 
                       type=int, 
                       metavar="[1024-65535]")
    parser.add_argument("--REST-API-VERSION".lower(), 
                       dest="REST_API_VERSION", 
                       help=("Choose a major version of the rest api. Depending on ONLY-CHOOSEN-REST-API-VERSION, "
                       "only this version, or all versions up to this version will be avaiable"), 
                       default=REST_version_info[0], 
                       choices=range(REST_version_info[0]+1), 
                       type=int)
    parser.add_argument("--SCHEDULE-TASK".lower(), 
                       dest="SCHEDULE_TASK", 
                       help=("schedule tasks, repetition time[ms] followed by the REST-API path, separated by:. "
                             "Example \"1000:/v1/cpu/status/load?token=12345678\""), 
                       default=[],
                       action='append',
                       #nargs='*',
                       type=str)
    parser.add_argument("--SHORT-JOB-MAX-TIME".lower(), 
                       dest="SHORT_JOB_MAX_TIME", 
                       help=("Short jobs will be executed rigth away and return results directly via REST-API, "
                       "blocking all other mpi communication in between [s]"), 
                       default=0.1, 
                       type=float)
    parser.add_argument("--SSL-ENABLED".lower(),
                       dest="SSL_ENABLED",
                       help=("You are able to use SSL encrypted connections, by enabeling with this flag you are using adhoc"
                       "certificates. For further information see https://gitlab.jsc.fz-juelich.de/coec/jumonc#encryption"),
                       default=False,
                       action='store_true')
    parser.add_argument("--SSL-CERT".lower(),
                       dest="SSL_CERT",
                       help=("Supply a certificate to use for the SSL connection, can only be used with --SSL-ENABLED and --SSL-KEY."
                       "For further information see https://gitlab.jsc.fz-juelich.de/coec/jumonc#encryption"),
                       default=None,
                       type=str)
    parser.add_argument("--SSL-KEY".lower(),
                       dest="SSL_KEY",
                       help=("Supply a key to use for the SSL connection, can only be used with --SSL-ENABLED and --SSL-CERT."
                       "For further information see https://gitlab.jsc.fz-juelich.de/coec/jumonc#encryption"),
                       default=None,
                       type=str)
    parser.add_argument("--USER-DEFINED-TOKEN".lower(), 
                       dest="USER_DEFINED_TOKEN", 
                       help=("Define one additional token with scope level, separate multiple tokens by ;"
                       "Example \"--USER-DEFINED-TOKEN=12345678:100\""), 
                       default=None, 
                       type=str)
    parser.add_argument("-v", 
                       "--version", 
                       help="Print Version number of jumonc", 
                       action='version', 
                       version=f'jumonc\'s {__version__},\n REST-API\'s {__REST_version__},\n DB\'s {__DB_version__}')
    
    
    return parser





def evaluateArgs(parser: argparse.ArgumentParser, args: List[str]) -> None:
    #pylint: disable=import-outside-toplevel
    from jumonc.helpers.PluginManager import addPluginArgs
    from jumonc.helpers.PluginManager import evaluatePluginArgs
    #pylint: enable=import-outside-toplevel
    
    parsed, unknown = parser.parse_known_args(args)
    logger.debug("Argument parsing, first pass")
    logger.debug("Parsed: %s", str(parsed))
    logger.debug("Unknown: %s", str(unknown))

    # first evaluate log args, to use them as fast as possible
    evaluateLogArgs(parsed)
    # then evaluate misc args, to load all plugins as well
    evaluateMiscellaneousArgs(parsed)
    
    # After adding plugin arguments, reparse
    addPluginArgs(parser)
    #parsed = parser.parse_args(args)   
    
    parsed, unknown = parser.parse_known_args(args)
    logger.debug("Argument parsing, first pass")
    logger.debug("Parsed: %s", str(parsed))
    logger.debug("Unknown: %s", str(unknown))

    
    evaluateRESTAPIArgs(parsed)
    evaluateDBArgs(parsed)
    evaluateThreadingArgs(parsed)
    evaluateSecurityArgs(parsed)
    evaluateSchedulingArgs(parsed)
    evaluteInitFile(parsed)
    
    evaluatePluginArgs(parsed)
    
    logger.debug("Argument parsing")
    logger.debug("Parsed: %s", str(parsed))



def evaluateLogArgs(parsed:argparse.Namespace) -> None:
          
    reset_logger()

    #set new logging options first, to then use them
    LOG_LEVEL = parsed.LOG_LEVEL[1:-1]
    if settings.LOG_LEVEL != LOG_LEVEL:
        settings.LOG_LEVEL = LOG_LEVEL
        logger.warning("Changing LOG_LEVEL to %s", settings.LOG_LEVEL)
        reset_logger()
    
    if settings.LOG_STDOUT != parsed.LOG_STDOUT:
        settings.LOG_STDOUT = parsed.LOG_STDOUT
        logger.warning("Changing LOG_STDOUT to %s", str(settings.LOG_STDOUT))
        reset_logger()
    
    LOG_PREFIX = parsed.LOG_PREFIX[1:-1]
    if settings.LOG_PREFIX != LOG_PREFIX:
        settings.LOG_PREFIX = LOG_PREFIX
        logger.warning("Changing LOG_PREFIX to %s", settings.LOG_PREFIX)
        reset_logger()
    
    LOG_FORMAT = parsed.LOG_FORMAT[1:-1]
    if settings.LOG_FORMAT != LOG_FORMAT:
        settings.LOG_FORMAT = LOG_FORMAT
        logger.warning("Changing LOG_FORMAT to %s", settings.LOG_FORMAT)
        reset_logger()

def evaluateRESTAPIArgs(parsed:argparse.Namespace) -> None:
    #pylint: disable=import-outside-toplevel
    from jumonc._version import REST_version_info
    #pylint: enable=import-outside-toplevel
    
    settings.ONLY_CHOOSEN_REST_API_VERSION = parsed.ONLY_CHOOSEN_REST_API_VERSION
    logger.info("Set ONLY_CHOOSEN_REST_API_VERSION to %s", str(settings.ONLY_CHOOSEN_REST_API_VERSION))

    if parsed.REST_API_PORT >=1024 and parsed.REST_API_PORT<=65535:
        settings.REST_API_PORT = parsed.REST_API_PORT
        logger.info("Set REST_API_PORT to %s", str(settings.REST_API_PORT))
    else:
        logger.error("Invalid value for REST_API_PORT: %s%s", str(settings.REST_API_PORT), ", needs to be between 1024 and 65535")
        sys.exit(-1)

    if parsed.REST_API_VERSION >= 1 and parsed.REST_API_VERSION <= REST_version_info[0]:
        settings.REST_API_VERSION = parsed.REST_API_VERSION
        logger.info("Set REST_API_VERSION to %s", str(settings.REST_API_VERSION))
    else:
        settings.REST_API_VERSION = REST_version_info[0]
        logger.warning("Invalid value for REST_API_VERSION: %s%s%s%s",
                        str(parsed.REST_API_VERSION), 
                        ", needs to be at least 1! Set to ",
                        str(settings.REST_API_VERSION ),
                        " now.")

    if parsed.FLASK_DEBUG:
        settings.FLASK_DEBUG = True
        logger.warning("Set FLASK_DEBUG to True")
        logger.warning("The Flask debugger allows arbitary code execution, only use in safe local setups")
        
    if parsed.FLASK_DEBUG or parsed.LOCAL_ONLY:
        settings.FLASK_HOST = "localhost"
        logger.info("Set FLASK_HOST to %s", str(settings.FLASK_HOST))
        
    
    settings.DATETIME_FORMAT = parsed.DATETIME_FORMAT
    logger.info("Set DATETIME_FORMAT to %s", str(settings.DATETIME_FORMAT ))

    settings.DEFAULT_TO_HUMAN_READABLE_NUMBERS = parsed.DONT_DEFAULT_TO_HUMAN_READABLE_NUMBERS
    logger.info("Set DEFAULT_TO_HUMAN_READABLE_NUMBERS to %s", str(settings.DEFAULT_TO_HUMAN_READABLE_NUMBERS))

    settings.CACHE_DEFAULT_ENTRIES_PER_PAGE  = parsed.CACHE_DEFAULT_ENTRIES_PER_PAGE 
    logger.info("Set CACHE_DEFAULT_ENTRIES_PER_PAGE  to %s", str(settings.CACHE_DEFAULT_ENTRIES_PER_PAGE ))


def evaluateDBArgs(parsed:argparse.Namespace) -> None:

    settings.DB_PATH = parsed.DB_PATH
    logger.info("Set DB_PATH to %s", str(settings.DB_PATH ))



def evaluateThreadingArgs(parsed:argparse.Namespace) -> None:

    if parsed.MAX_WORKER_THREADS >= 1:
        settings.MAX_WORKER_THREADS = parsed.MAX_WORKER_THREADS
        logger.info("Set MAX_WORKER_THREADS to %s", str(settings.MAX_WORKER_THREADS))
    else:
        settings.MAX_WORKER_THREADS = 1
        logger.warning("Invalid value for MAX_WORKER_THREADS: %s%s%s%s",
                        str(parsed.MAX_WORKER_THREADS), 
                        ", needs to be at valid version! Set to ",
                        str(settings.MAX_WORKER_THREADS ),
                        " now.")

    settings.SHORT_JOB_MAX_TIME = parsed.SHORT_JOB_MAX_TIME
    logger.info("Set SHORT_JOB_MAX_TIME to %s", str(settings.SHORT_JOB_MAX_TIME))

    if parsed.PENDING_TASKS_SOFT_LIMIT >= 1:
        settings.PENDING_TASKS_SOFT_LIMIT = parsed.PENDING_TASKS_SOFT_LIMIT
        logger.info("Set PENDING_TASKS_SOFT_LIMIT to %s", str(settings.PENDING_TASKS_SOFT_LIMIT))
    else:
        settings.PENDING_TASKS_SOFT_LIMIT = 1
        logger.warning("Invalid value for PENDING_TASKS_SOFT_LIMIT: %s%s%s%s",
                        str(parsed.PENDING_TASKS_SOFT_LIMIT), 
                        ", needs to be at valid version! Set to ",
                        str(settings.PENDING_TASKS_SOFT_LIMIT ),
                        " now.")



def evaluateSecurityArgs(parsed:argparse.Namespace) -> None:

    # SSL configuration, due to security concerns, jumonc wil lbe stopped in case of incomplet configuration
    if parsed.SSL_ENABLED:
        if parsed.SSL_CERT or parsed.SSL_KEY:
            if parsed.SSL_CERT and parsed.SSL_KEY:
                settings.SSL_MODE = (parsed.SSL_CERT, parsed.SSL_KEY)
                logger.warning("Enabling SSL connection with user certificate and key")
            else:
                logger.warning("Cert: %s, Key: %s", str(parsed.SSL_CERT), str(parsed.SSL_KEY))
                logger.error(("For use of self supplied certificates jumonc needs both the certificate and key.",
                                  " See: https://gitlab.jsc.fz-juelich.de/coec/jumonc#encryption"))
                sys.exit(-5)
        else:
            settings.SSL_MODE='adhoc'
            logger.warning("Enabling adhoc SSL connection")
        settings.SSL_ENABLED = parsed.SSL_ENABLED
    if (parsed.SSL_CERT or parsed.SSL_KEY) and not parsed.SSL_ENABLED:
        logger.error(("For use of self supplied certificates jumonc needs the certificate, the key and SSl needs to be enabled.",
                          " See: https://gitlab.jsc.fz-juelich.de/coec/jumonc#encryption"))
        sys.exit(-5)
    
    settings.USER_DEFINED_TOKEN = parsed.USER_DEFINED_TOKEN
    logger.info("Set USER_DEFINED_TOKEN to %s", str(settings.USER_DEFINED_TOKEN))



def evaluateMiscellaneousArgs(parsed:argparse.Namespace) -> None:

    settings.PLUGIN_PATHS.extend(parsed.PLUGIN_PATHS)
    logger.info("Set PLUGIN_PATHS to %s", str(settings.PLUGIN_PATHS))
    


def evaluateSchedulingArgs(parsed:argparse.Namespace) -> None:
    settings.SCHEDULED_TASKS_ENABLED = parsed.SCHEDULED_TASKS_ENABLED
    logger.info("Set SCHEDULED_TASKS_ENABLED to %s", str(settings.SCHEDULED_TASKS_ENABLED))

    if settings.SCHEDULED_TASKS_ENABLED:
        settings.SCHEDULE_TASKS.extend(parsed.SCHEDULE_TASK)
        logger.info("SCHEDULE_TASK: %s", str(settings.SCHEDULE_TASKS))
        for task in settings.SCHEDULE_TASKS:
            split = task.split(":")
            planed_tasks.addScheduledTask(":".join(split[1:]), int(split[0]))


def evaluteInitFile(parsed:argparse.Namespace) -> None:

    if parsed.INIT_FILE is not None:
        logger.info("Using INIT_FILE %s", str(parsed.INIT_FILE))
        try:
            init_spec=importlib.util.spec_from_file_location("init_file", parsed.INIT_FILE)
            if init_spec is None or init_spec.loader is None:
                logger.error("Error trying to load the init file: %s", str(parsed.INIT_FILE))
                return
            init = importlib.util.module_from_spec(init_spec)
            init_spec.loader.exec_module(init)
        except FileNotFoundError:
            logger.error("The provided init file \"%s\" can not be found, starting jumonc without init file", str(parsed.INIT_FILE))
        except SyntaxError:
            logger.error("The provided init file \"%s\" has syntax errors, starting jumonc without init file", str(parsed.INIT_FILE), exc_info = True)
        except Exception:
            logger.error("The provided init file \"%s\" has errors, starting jumonc without init file", str(parsed.INIT_FILE), exc_info = True)
            
        # call in case the init file changed logging operations
        reset_logger()
