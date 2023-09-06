# This module will handle the logging setup.
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    my_handler = RotatingFileHandler('pp_log.txt', mode='a', maxBytes=4*1024*1024,
                                     backupCount=4, encoding="ascii", delay=0)
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(logging.DEBUG)
    
    log = logging.getLogger('root')
    log.addHandler(my_handler)
    log.setLevel(logging.DEBUG)