import logging

def get_logger(name='logfile.txt', level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    logger.addHandler(console_handler)
    return logger
