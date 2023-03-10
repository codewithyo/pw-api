import logging

from requests import get

import utils.logger
from utils.logger import LoggingMessage


def get_response(url: str) -> bytes:
    """ Return the response data in `bytes`. """
    # Get the id
    _id = url.rsplit('/', 2)[-2]

    # Download url prefix
    prefix = 'https://drive.google.com/uc?export=download&id='

    # Get the url response
    r = get(prefix + _id)
    logging.info(LoggingMessage.get_request_log.format(prefix + _id))
    logging.info(LoggingMessage.status_code_log.format(r.status_code))

    r.raise_for_status()

    return r.content


def download(url: str, filename: str, file_ext: bool = False) -> None:
    """Download and save the data in `downloads/` folder.

    `Note:` Maybe the **file extension** differ from actual extension.
    So, if you find problem try to fix it.

    Args:
        url (str): Google drive files url.
        filename (str): Provide the filename of the file to be saved.
        file_ext (bool): File extension provided in **filename**. Default to False.
    """
    data = get_response(url)

    if not file_ext:
        ext = ('.docx' if 'docs' in url else
               '.ipynb' if 'drive' in url or 'colab' in url else
               '.pdf')
    else:
        ext = ''

    try:
        file_path = f'downloads/{filename + ext}'
        with open(file_path, 'wb') as f:
            logging.info(LoggingMessage.file_downloaded_log.format(file_path))
            f.write(data)
    except FileNotFoundError:
        raise FileNotFoundError('To download please create a directory as `downloads` or \
            run `main.py` to maintain the directory structure.')
