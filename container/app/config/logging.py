"""Set up logging for the application. """

import logging
import colorlog

# Set up colored logging with full relative path and line number
handler = colorlog.StreamHandler()
handler.setFormatter(
    colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
    )
)

# Configure root logger first
root_logger = colorlog.getLogger()
root_logger.addHandler(handler)
root_logger.setLevel(logging.INFO)

# Then create and export a logger instance
logger = logging.getLogger(__name__)
