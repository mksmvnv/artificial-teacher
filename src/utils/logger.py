import logging
import os
import sys


class Logger:
    """Custom logger."""

    def __init__(self, name: str = "app", log_file: str = ".logs/app.log", level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        self.logger.handlers.clear()

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        if log_file:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def debug(self, message: str) -> None:
        """Log debug level message."""
        self.logger.debug(message)

    def info(self, message: str) -> None:
        """Log info level message."""
        self.logger.info(message)

    def warning(self, message: str) -> None:
        """Log warning level message."""
        self.logger.warning(message)

    def error(self, message: str) -> None:
        """Log error level message."""
        self.logger.error(message)

    def critical(self, message: str) -> None:
        """Log critical level message."""
        self.logger.critical(message)


logger = Logger()
