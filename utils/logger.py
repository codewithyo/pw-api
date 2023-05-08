""" Basic logging definition for this project. """

import logging
from datetime import date
from pathlib import Path

log_dir_path = Path('logs')
log_dir_path.mkdir(exist_ok=True)

log_fp = log_dir_path / (date.today().strftime('%d-%m-%Y') + '.log')

logging.basicConfig(
    filename=log_fp,
    format="[ %(asctime)s ] %(filename)s:[%(lineno)d] %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


class LoggingMessage:
    """ Provide logging message templates to log. """
    get_request_log = 'GET Request: {}'
    status_code_log = 'Response Code: {}'
    file_downloaded_log = 'Downloaded: {}'
