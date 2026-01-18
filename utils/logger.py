import logging
from config.settings import config


def setup_logger(name):
    logger = logging.getLogger(name)
    level = config.get("log_level", "INFO")
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
