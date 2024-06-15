import logging


def setup_logger(name: str, level: str = "INFO"):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger


logger = setup_logger("MEMES")
