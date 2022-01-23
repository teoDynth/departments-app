"""Module with logging setup."""
import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('log.log', mode='w')
std_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s : %(name)s  : %(funcName)s :'
                              ' %(levelname)s : %(message)s')
file_handler.setFormatter(formatter)
std_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(std_handler)
