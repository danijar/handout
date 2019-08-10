import sys
import logging

def strip_empty_lines(lines):
  output = []
  for line in lines:
    if not line and not output:
      continue
    output.append(line)
  lines = reversed(output)
  output = []
  for line in lines:
    if not line and not output:
      continue
    output.append(line)
  lines = reversed(output)
  return list(lines)


def get_logger():
  logger = logging.getLogger('handout')
  logger.setLevel(logging.INFO) # A user can change this level later.
  logger.propagate = False  # Global logger should not print messages again.
  if not logger.handlers: # Prevents creation of multiple handlers.
      handler = logging.StreamHandler(sys.stdout)
      handler.setFormatter(logging.Formatter('%(message)s'))
      logger.addHandler(handler)
  # The logger can be accessed anywhere in code by its name with 
  # `logging.getLogger('handout')`. However, we retrun the logger 
  # explcitly here as function result, for convenience of use.
  return logger
