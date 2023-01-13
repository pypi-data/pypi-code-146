import logging
import os
from pathlib import Path
from datetime import datetime

def logging_setup():
    
    logger = logging.getLogger()

    if (logger.hasHandlers()):
        logger.handlers.clear()

    logger.setLevel(logging.NOTSET)

    # our first handler is a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler_format = '%(asctime)s | %(levelname)s: %(message)s'
    console_handler.setFormatter(logging.Formatter(console_handler_format))
    logger.addHandler(console_handler)

    # # the second handler is a file handler
    # log_path = f'{self.output_path}{os.path.sep}logging'
    
    # if not Path(log_path).exists():
    #     os.makedirs(log_path)
    
    # logfile_name = f'{log_path}{os.path.sep}{datetime.today().strftime("%Y-%m-%d")}_{self.analysis_id}.log'
    # file_handler = logging.FileHandler(logfile_name)
    # file_handler.setLevel(logging.DEBUG)
    # file_handler_format = '%(asctime)s | %(levelname)s | %(lineno)d: %(message)s'
    # file_handler.setFormatter(logging.Formatter(file_handler_format))
    # logger.addHandler(file_handler)
   
    return logger

