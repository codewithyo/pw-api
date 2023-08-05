import logging
from dataclasses import dataclass
from datetime import datetime as dt
from pathlib import Path


def get_logger(logger_name: str) -> logging.Logger:
    """
    :logger_name (str): `__name__`

    :returns: logging.Logger
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    run_id = dt.now()
    fp = Path(f'logs/{run_id:%d%m%y-%H}/{run_id:%d%m%y-%H%M%S}.log')
    fp.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        '[%(asctime)s]:%(levelname)s:[%(lineno)d]:%(name)s - %(message)s',
    )

    file_handler = logging.FileHandler(fp)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


@dataclass
class LoggingMessage:
    """ Provide logging message templates to log. """
    get_request_log = 'GET Request: {}'
    status_code_log = 'Response Code: {}'
    file_downloaded_log = 'Downloaded: {}'
