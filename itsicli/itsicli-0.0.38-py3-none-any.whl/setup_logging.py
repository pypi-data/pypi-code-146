import os
import logging, logging.handlers
from itsicli import __version__

extra = {'cp_id': 'unknown'}
LOG_DEFAULT_FMT = '%(asctime)s process:%(process)d thread:%(threadName)s %(levelname)s [cp_id: %(cp_id)s] [%(name)s] [%(module)s:%(lineno)d] [%(funcName)s] %(message)s'
ITSI_CLI_LOGGER = 'itsicli'
ITSI_CLI_LOG_FILE = 'itsi_content_packs_itsicli.log'

try:
    SPLUNK_HOME = os.environ['SPLUNK_HOME']
except KeyError:
    SPLUNK_HOME = None

if SPLUNK_HOME is None:
    home_dir = os.path.expanduser("~")
    LOGGING_FILE_NAME = os.path.join(home_dir, ITSI_CLI_LOG_FILE)

    print('-----> itsicli log file is created at {}'.format(os.path.abspath(LOGGING_FILE_NAME)))

else:
    LOGGING_DEFAULT_CONFIG_FILE = os.path.join(SPLUNK_HOME, 'etc', 'log.cfg')
    LOGGING_LOCAL_CONFIG_FILE = os.path.join(SPLUNK_HOME, 'etc', 'log-local.cfg')

    LOGGING_STANZA_NAME = 'python'
    BASE_LOG_PATH = os.path.join('var', 'log', 'splunk')
    LOGGING_FILE_NAME = os.path.join(SPLUNK_HOME, BASE_LOG_PATH, ITSI_CLI_LOG_FILE)

'''
cloned from splunk.setupSplunkLogger
'''
def setupSplunkLogger(baseLogger, defaultConfigFile, localConfigFile, loggingStanzaName, verbose=True):
    '''
    Takes the base logging.logger instance, and scaffolds the splunk logging namespace
    and sets up the logging levels as defined in the config files
    '''

    levels = getSplunkLoggingConfig(baseLogger, defaultConfigFile, localConfigFile, loggingStanzaName, verbose)

    for item in levels:
        loggerName = item[0]
        level = item[1]
        if hasattr(logging, level):
            logging.getLogger(loggerName).setLevel(getattr(logging, level))
        if verbose and (loggerName == "appender.python.maxFileSize" or loggerName == "appender.python.maxBackupIndex"):
            baseLogger.info('Python log rotation is not supported. Ignoring %s' % loggerName)

'''
Setting the content pack id in global dictionary
'''
def set_content_pack_id(cp_id):
    extra['cp_id'] = cp_id


'''
cloned from splunk.getSplunkLoggingConfig
'''
def getSplunkLoggingConfig(baseLogger, defaultConfigFile, localConfigFile, loggingStanzaName, verbose):
    loggingLevels = []

    # read in config file and set logging levels
    if os.access(localConfigFile, os.R_OK):
        if verbose:
            baseLogger.info('Using local logging config file: %s' % localConfigFile)
        logConfig = open(localConfigFile, 'r')
    else:
        if verbose:
            baseLogger.info('Using default logging config file: %s' % defaultConfigFile)
        logConfig = open(defaultConfigFile, 'r')

    try:
        inStanza = False
        for line in logConfig:

            # strip comments
            line = line.strip()
            if '#' in line:
                line = line[:(line.index('#'))]

            # skip blank lines
            line = line.strip()
            if not line:
                continue

            # # # skip malformatted lines: stanza, key=value, or WTF?
            if line.startswith('['):
                if not line.endswith(']') or line.index(']') != (len(line) - 1):
                    continue
            elif '=' in line:
                key_test, value_test = line.split('=')
                if not key_test or not value_test:
                    continue
            else:
                continue

            # # # validation done, now we finally have parsing logic proper
            if not inStanza and line.startswith('[%s]' % loggingStanzaName):
                inStanza = True
                continue
            elif inStanza:
                if line.startswith('['):
                    break
                else:
                    name, level = line.split('=', 1)
                    if verbose:
                        baseLogger.info('Setting logger=%s level=%s' % (name.strip(), level.strip()))
                    loggingLevels.append((name.strip(), level.strip().upper()))
    except Exception as e:
        baseLogger.exception(e)
    finally:
        if logConfig: logConfig.close()

    return loggingLevels


def setup_logging():

    _logger = logging.getLogger(ITSI_CLI_LOGGER)

    if not _logger.hasHandlers():
        splunk_log_handler = logging.handlers.RotatingFileHandler(LOGGING_FILE_NAME, maxBytes=5000000, backupCount=5)
        splunk_log_handler.setFormatter(logging.Formatter(LOG_DEFAULT_FMT))
        _logger.addHandler(splunk_log_handler)
        _logger = logging.LoggerAdapter(_logger, extra)

        if SPLUNK_HOME is not None:
            # splunk.setupSplunkLogger
            setupSplunkLogger(_logger, LOGGING_DEFAULT_CONFIG_FILE, LOGGING_LOCAL_CONFIG_FILE, LOGGING_STANZA_NAME)

        _logger.setLevel(logging.INFO)

        _logger.debug('itsicli version={} logger configured. LOGGING_FILE_NAME={}'.format(__version__,
                                                                                    LOGGING_FILE_NAME))
    return _logger


logger = setup_logging()
