

from distutils.log import INFO
import logging

print('--------------__')
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

# logging.log(INFO,'helooooaiudgfydfdfyu')
logging.info('helooooaiudgfydfdfyu')
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')
print('--------------__')