import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from loguru import logger


class LogLevel(Enum):
    ...


@dataclass
class LoggingMixin:
    log_level: str
    output_dir: str

    _FORMAT_CONSOLE_LOG = "[<green>{time}</green>] <level>{level: <8}</level>    - {message}"
    _FORMAT_LOG_FILE = "[<green>{time}</green>] <level>{level: <8}</level>    - {message}"

    def get_logger(self):
        logger.remove()
        logger.add(
            sys.stdout,
            format=self._FORMAT_CONSOLE_LOG,
            colorize=True, level=self.log_level
        )
        log_dir = Path(self.output_dir) / "logs" / f"{self.__class__.__name__}_{{time}}.log"
        logger.add(
            log_dir,
            format=self._FORMAT_LOG_FILE,
            colorize=False, level=self.log_level
        )
        logger.info('Initialize logging...')
