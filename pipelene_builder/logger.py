import logging
import sys


class LoggerConfig:
    @staticmethod
    def get_logger(name: str, level=logging.INFO):
        logger = logging.getLogger(name)
        if not logger.hasHandlers():
            logger.setLevel(level)

            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(level)

            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            console_handler.setFormatter(formatter)

            logger.addHandler(console_handler)

        return logger
