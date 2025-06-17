import logging
import sys


class CustomFormatter(logging.Formatter):
    LOG_COLORS = {
        logging.DEBUG: "\033[94m",  # Blue
        logging.INFO: "\033[32m",  # Dark Green
        logging.WARNING: "\033[93m",  # Yellow
        logging.ERROR: "\033[91m",  # Red
        logging.CRITICAL: "\033[95m",  # Magenta
    }
    RESET_COLOR = "\033[0m"

    def format(self, record):
        log_color = self.LOG_COLORS.get(record.levelno, self.RESET_COLOR)
        log_msg = super().format(record)
        return f"{log_color}{log_msg}{self.RESET_COLOR}"


logger = logging.getLogger("rl_intro")
logger.setLevel(logging.DEBUG)


handler = logging.StreamHandler(sys.stdout)
formatter = CustomFormatter(
    "[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d] %(message)s",
    datefmt="%H:%M:%S",
)
handler.setFormatter(formatter)

if not logger.hasHandlers():
    logger.addHandler(handler)

logger.propagate = False
