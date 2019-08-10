import sys
import logging

LOGGER_NAME = 'handout'

def configure_logger():
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO) # A user can change this level later.
    logger.propagate = False  # Global logger should not print messages again.
    if not logger.handlers: # Prevents creation of multiple handlers.
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(handler)


def get_logger(): 
    return logging.getLogger(LOGGER_NAME)
