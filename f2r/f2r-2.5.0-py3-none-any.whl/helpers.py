import yaml
import subprocess
import logging
import sys


def parseRecipeHeader(path):
    """ Parses header of alidist recipe"""
    tempString = ''
    with open(path, 'r') as file:
        for line in iter(lambda: file.readline().rstrip(), '---'):
            tempString += line + '\n'
    return yaml.safe_load(tempString)


def parseYamlDict(path):
    """ Parses a yaml list into a dict """
    with open(path, 'r') as file:
        return yaml.safe_load(file)


def runSubprocess(command, **flags):
    options = {
        'failOnError': True,
        'forceTty': False
    }
    for option in options:
        if option in flags:
            options[option] = flags[option]
            del flags[option]
    output = ''
    if options['forceTty']:
        command = ["script -q -e -c '" + ' '.join(command) + "'"]

    try:
        logging.debug('Running as subprocess: %s' % (subprocess.list2cmdline(command)))
        output = subprocess.check_output(command, **flags).strip()
        if type(output) != str:
            output = output.decode('ascii')
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        output = e.output
        if type(output) != str:
            output = output.decode('ascii')
        if 'File already exists' in output:
            logging.warning('The RPM already exists, continuing...')
        else:
            logging.error(output)
            logging.error(e)
            if options['failOnError']:
                logging.critical('Exiting...')
                sys.exit(1)
            else:
                return False
    logging.debug('Subprocess completed with output length %d' % len(output))
    if (len(output) < 1):
        output = True
    return output
