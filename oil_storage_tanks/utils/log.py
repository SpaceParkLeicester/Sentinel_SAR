import logging

def logger():
    """Custom logging fucntion"""
    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create a file handler
    fh = logging.FileHandler('log_messages.log')
    fh.setLevel(logging.DEBUG)

    # Create a stream handler
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)

    # Set the log format
    formatter = logging.Formatter('\n%(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)

    # Add the file handler and stream handler to the logger
    logger.addHandler(sh)
    logger.addHandler(fh)

    # Log messages
    logger.debug('Debug message')
    logger.info('Info message')
    logger.warning('Warning message')
    logger.error('Error message')
    logger.critical('Critical message')

    return logger
