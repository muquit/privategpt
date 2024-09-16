import logging
import sys

#====================================================================
# muquit@muquit.com Sep-15-2024 
#====================================================================
def setup_logging(log_file="private_gpt.log", log_level=logging.DEBUG,console_level=logging.DEBUG):
    logger = logging.getLogger()
    logger.setLevel(log_level)

    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # file handler (always used)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # console handler (only if stderr is available)
    if sys.stderr:
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setLevel(console_level)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger


