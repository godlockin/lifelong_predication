import os
import logging
from logging.handlers import TimedRotatingFileHandler


def get_logger(clazz_name):
    # Set up logging
    log_file_name = 'logs/app.log'
    log_level = logging.INFO
    os.makedirs(os.path.dirname(log_file_name), exist_ok=True)

    # Create a logger
    logger = logging.getLogger(clazz_name)
    logger.setLevel(log_level)

    # Create a file handler
    # backupCount is set to 14 to keep logs for 14 days
    handler = TimedRotatingFileHandler(log_file_name, when='midnight', backupCount=14)
    handler.setLevel(log_level)

    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(handler)

    return logger
