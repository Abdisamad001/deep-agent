from utils.logger import setup_logger

logger = setup_logger(__name__)


def handle_error(e: Exception):
    logger.error(f"An error occurred: {str(e)}", exc_info=True)
