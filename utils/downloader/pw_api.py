""" Use for fetching/downloading the data using PW APIs.

Also store the files in respective paths in JSON format.
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from time import sleep
from typing import Literal

from pandas import read_csv
from requests import get

from utils.logger import LoggingMessage


class StatusCodeError(Exception):
    """ Used to raise Error while response's status code is not equal to 200. """

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def data_from_api(url: str, auth_key: str) -> dict:
    """Get JSON response from the provided PW API `URL` using `auth_key`.

    Args:
        url (str): PW Skills API url of course's quiz and assignment.
        auth_key (str): Authorization Bearer Token for request header.

    Raises:
        StatusCodeError: When the response is not equal to 200.

    Returns:
        dict: JSON response of the provided url.
    """
    headers = {
        'Authorization': auth_key,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0'
    }

    logging.info(LoggingMessage.get_request_log.format(url))
    r = get(url, headers=headers, timeout=3)
    logging.info(LoggingMessage.status_code_log.format(r.status_code))

    if r.status_code == 200:
        return r.json()
    else:
        raise StatusCodeError(f'Response has not status code of 200.\n> {url}')


def export_data(url: str,
                auth_key: str,
                type: Literal['quiz', 'assignment'] = 'quiz') -> None:
    """Store/Export the response data in JSON format in a structured manner.

    Also, excludes the URL which are already downloaded and stored in the directory.

    Args:
        url (str): Quiz and Assignment Url.
        auth_key (str): Authorization Bearer Token for request header.
        type (Literal['quiz', 'assignment'], optional): Type of the response data. Defaults to 'quiz'.

    Returns:
        None: Export the data get in response from the Url as JSON format.
    """
    # Check if url id already exists
    if url.rsplit('/', 1)[-1] in get_downloaded_id():
        return None

    # Get data from API using url
    data = data_from_api(url, auth_key)

    # Date for filename
    date = datetime.fromisoformat(data['data']['lesson']['createdAt'])
    # Title for filename
    title = data['data']['lesson']['title']

    # Create folder if not exists
    FOLDER = f'downloads/{type}/{date:%h}'
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER, exist_ok=True)

    FILENAME = f"{FOLDER}/{date:%d %h} - {title}.json"

    # Dump data in JSON format
    json.dump(data, open(FILENAME, 'w'), indent=2)
    logging.info(LoggingMessage.file_downloaded_log.format(FILENAME))


def get_downloaded_id() -> list[str]:
    """ Returns the ID of all downloaded Quizzes and Assignments. """
    ids = []

    # Get all quiz file path
    quiz_path = Path('downloads/quiz/')
    quizzes = [j for i in quiz_path.iterdir() for j in i.iterdir()]

    # Get all assignment file path
    assignment_path = Path('downloads/assignment/')
    assignments = [j for i in assignment_path.iterdir() for j in i.iterdir()]

    # Get all quiz_id and assignment_id from JSON file.
    ids += [json.load(open(i))['data']['lesson']['_id'] for i in quizzes]
    ids += [json.load(open(i))['data']['lesson']['_id'] for i in assignments]

    return ids


def download_all(csv_fp: str,
                 auth_key: str,
                 type: Literal['quiz', 'assignment', 'all'] = 'all') -> None:
    """Download all the Quizzes and Assignments by providing the CSV file of course.

    Get the CSV file from `Notebooks/live_course_analysis.ipynb`.

    Args:
        csv_fp (str): CSV file from `live_course_analysis.ipynb`
        auth_key (str): Authorization Bearer Token for request header.
        type (Literal['quiz', 'assignment', 'all'], optional): Type of the response data. Defaults to 'all'.
            If `'all'` both Quiz and Assignment get downloaded.
    """
    df = read_csv(csv_fp)

    # If type == 'all'
    query = ['quiz', 'assignment'] if type == 'all' else type

    main_df = df.query("type==@query")

    count = 1
    for title, _type, url in main_df['lessonTitle', 'type', 'url'].itertuples(name=None):
        print(f"{count}. {_type.ljust(10)} >>  {title.strip()}")

        sleep(3)
        export_data(url, auth_key, _type)

        count += 1


def download(url: str, auth_key: str, type: str) -> None:
    """ Download any data by specifying its type.

    If **type** is other than `['quiz', 'assignment']` then files were stored in 
    `data/others/` folder.
    """

    if type.lower() in ['quiz', 'assignment']:
        return export_data(url, auth_key, type)    # type: ignore

    data = data_from_api(url, auth_key)

    filename = 'downloads/others/' + f'{type}.json'
    os.makedirs('downloads/others/', exist_ok=True)

    json.dump(data, open(filename), indent=2)
    logging.info(LoggingMessage.file_downloaded_log.format(filename))
