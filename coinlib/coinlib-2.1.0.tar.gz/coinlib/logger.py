import logging
import logging.config
import time
import os

from coinlib import Registrar


def replaceConfFileWithVariables():
    # input file
    fin = open('python.conf', "rt")
    # output file to write the result to
    fout = open('python_replaced.conf', "wt")
    services = os.getenv("MODULES") if os.getenv("MODULES") is not None else "python"
    # for each line in the input file
    for line in fin:
        # read replace the string and write to output file
        fout.write(line.replace('$TAGS', services))
    # close input and output files
    fin.close()
    fout.close()




def install_cloud_logger():
    registrar = Registrar()

    if os.getenv("LOGGLY_ENABLED") == "true":
        replaceConfFileWithVariables()

        print("Starting with loggly logger");
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        # set a format which is simpler for console use
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        # add the handler to the root logger

        logging.config.fileConfig('python_replaced.conf')
        logging.Formatter.converter = time.gmtime
        logger = logging.getLogger(__name__)
        logger.addHandler(console)
        registrar.logger = logger

