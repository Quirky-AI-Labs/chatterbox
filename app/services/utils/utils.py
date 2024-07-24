import traceback

from loguru import logger


def log_traceback():
    logger.error(f"TRACEBACK: {traceback.format_exc()}")
