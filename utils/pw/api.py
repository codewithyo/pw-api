""" Use for fetching/downloading the data using PW APIs.

Also store the files in respective paths in JSON format.
"""

from json import dump, load
from pathlib import Path
from time import sleep
from typing import Literal, TypeAlias

from requests import get

UrlType: TypeAlias = Literal['quiz', 'assignment']


class PWApi:
    def __init__(self, auth_key: str, course_id: str) -> None:
        self.auth_key = auth_key
        self.cid = course_id

    def get(self, url: str) -> dict:
        """ Get JSON response from the provided PW API `URL` using `auth_key` """
        headers = {
            'Authorization': self.auth_key,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0'
        }
        r = get(url, headers=headers, timeout=3)

        if r.status_code == 200:
            return r.json()
        else:
            raise ValueError(f'Response has not status code of 200: {url}')

    def _id_from_url(self, url: str) -> str:
        return url.rsplit('/', 1)[-1]

    def generate_fp(self, type: UrlType) -> Path:
        fp = Path('data') / type
        return fp / f'{type}_{self.cid}.json'

    def export_data(
        self, url_list: list[str], type: UrlType, wait: int = 1
    ) -> None:
        """
        Stores quizzes and assignments in JSON format.
        Also, excludes the URL which are already downloaded and stored in the directory.
        """
        fp = self.generate_fp(type)
        stored_ids = self.load_downloaded_ids(fp) if fp.exists() else []
        res: list = load(open(fp))
        for url in url_list:
            sleep(wait)
            if self._id_from_url(url) not in stored_ids:
                if type == 'quiz':
                    res.append(self.get_quiz_data(url))
                else:
                    res.append(self.get_assignment_data(url))
        dump(res, open(fp, 'w'), indent=2)

    def load_downloaded_ids(self, fp: Path) -> list[str]:
        """ Returns ID of all downloaded Quizzes and Assignments. """
        ids = []
        data = load(open(fp))
        for d in data:
            ids.append(d['_id'])
        return ids

    def get_assignment_data(self, url: str):
        data = self.get(url)['data']
        res = {
            '_id': data['_id'],
            'title': data['title'],
            'data': data['data'],
            'createdAt': data['createdAt'],
        }
        return res

    def get_quiz_data(self, url: str):
        data = self.get(url)['data']
        res = {
            '_id': data['_id'],
            'title': data['title'],
            'options': data['options'],
            'createdAt': data['createdAt'],
        }
        return res
