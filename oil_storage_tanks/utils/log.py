import logging
import colorlog

def logger():
    """Custom logging fucntion"""
    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Remove the default handler
    logger.handlers = []

    # Create a stream handler
    sh = logging.StreamHandler()

    # Set the log format
    formatter = colorlog.ColoredFormatter(
    '%(asctime)s - %(log_color)s%(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    log_colors={
        'DEBUG': 'blue',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
    )

    # Set the log format on the stream and file handler
    sh.setFormatter(formatter)

    # Add the file handler and stream handler to the logger
    logger.addHandler(sh)

    # Disable propagation of messages to the root logger
    logger.propagate = False
    
    # Log messages
    logger.debug('Debug message')
    logger.info('Info message')
    logger.warning('Warning message')
    logger.error('Error message')
    logger.critical('Critical message')
    logger.info('======================================================================================')

    return logger
