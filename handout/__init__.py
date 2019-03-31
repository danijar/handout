import sys
import logging

from .handout import Handout


# Set up logger.
logger = logging.getLogger('handout')
logger.setLevel(logging.INFO)
logger.propagate = False  # Global logger should not print messages again.
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(handler)
