import logging
from functools import lru_cache
from logging import Logger

from .config import get_settings

config = get_settings()


@lru_cache()
def get_logger() -> Logger:
    """Setup and cache logger, avoiding unnecessary calls and file access issues.

    Returns
    -------
    Logger
        Instance of the logger.
    """

    logging.basicConfig(
        level=config.ASC_LOG_LEVEL,
        format=config.ASC_LOG_FORMAT,
    )
    logger = logging.getLogger(config.ASC_LOG_NAME)

    if config.ASC_LOG_PATH is not None:
        file_handler = logging.FileHandler(config.ASC_LOG_PATH)
        file_handler.setLevel(config.ASC_LOG_LEVEL)
        logger.addHandler(file_handler)

    return logger
