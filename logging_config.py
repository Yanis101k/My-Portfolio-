# Import the built-in logging module to record messages for debugging, info, warnings, and errors
import logging

# Import RotatingFileHandler to manage log files and automatically rotate them when they get too big
from logging.handlers import RotatingFileHandler

# Import os to work with file paths and check for folder existence
import os

def setup_logging():
    """
    Sets up logging for the Flask application.
    Logs are saved to 'logs/app.log' with rotation when the file grows too large.
    """
    # Make sure the 'logs' directory exists
    if not os.path.exists('logs'):
        os.mkdir('logs')

    # Create a rotating file handler:
    # - Max file size: 10 KB
    # - Keep up to 5 backup log files
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=5)

    # Set the format for each log entry: timestamp, log level, message, source file and line number
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(message)s [in %(pathname)s:%(lineno)d]'
    )
    file_handler.setFormatter(formatter)

    # Set log level to DEBUG (captures all log types: debug, info, warning, error, critical)
    file_handler.setLevel(logging.DEBUG)

    # Add the handler to the root logger
    logging.getLogger().addHandler(file_handler)

    # Set the global log level to DEBUG
    logging.getLogger().setLevel(logging.DEBUG)

    # Confirm logging setup was successful (this message will be written to the log file)
    logging.info("Logging system initialized.")
