import logging
from telogger import Telogger

def main():
    tlogger = Telogger()  # Using environment variables
    
    # Configure logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    tlogger.add_logging_handler(logger, level=logging.WARNING)
    
    # Test log messages
    logger.debug("This won't be sent")  # Below threshold
    logger.info("This won't be sent either")  # Below threshold
    logger.warning("This will go to Telegram!")
    logger.error("Important error notification")

if __name__ == "__main__":
    main()