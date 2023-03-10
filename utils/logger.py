import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime(r'%m_%d_%Y')}.log"
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE[:-4])
os.makedirs(logs_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(filename)s:[%(lineno)d] %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


class LoggingMessage:
    """ Provide logging message templates to log. """
    get_request_log = 'GET Request: {}'
    status_code_log = 'Response Code: {}'
    file_downloaded_log = 'Downloaded: {}'
