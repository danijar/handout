import sys
import logging

from .handout import Handout


# Set up logger.
logger = logging.getLogger('handout')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))
