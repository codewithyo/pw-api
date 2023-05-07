""" Used create directory structure and storing the auth_key in local directory. """

from datetime import datetime as dt
from datetime import timedelta
from json import dump
from pathlib import Path
from shutil import rmtree
from time import sleep

from .api import PWApi


class Credentials:
    def __init__(self, auth_key: str, course_id: str, login_for: int = 10):
        if len(auth_key.split('.')) != 3:
            raise ValueError('Authorization token is wrong.')

        self.auth_key = auth_key
        self.cid = course_id
        self.login_for = login_for
        self.api = PWApi(auth_key, course_id)

        dirname = str(dt.now().replace(microsecond=0)) + '.cookie'
        self.cookie_dir = Path(dirname)
        # Create cookie directory to store credential data
        self.__create_cookie()

    @classmethod
    def get_cookie_dir(cls) -> Path | None:
        root = Path('.')
        cookie_dir = [i for i in root.iterdir() if '.cookie' in i.name]
        if len(cookie_dir) == 0:
            return None
        return cookie_dir[0]

    def __create_cookie(self):
        if self.__check_cookie_existence():
            self.cookie_dir.mkdir()

    def __check_cookie_existence(self) -> bool:
        """ Check whether it is 10 minutes old and delete it """
        cookie_dir = self.get_cookie_dir()
        if cookie_dir is None:
            return True

        created_at = dt.fromisoformat(cookie_dir.stem)
        expired_at = created_at + timedelta(minutes=self.login_for)
        if expired_at >= dt.now():
            return False
        else:
            # Delete the folder because it is now expired
            rmtree(cookie_dir)
            return True

    def download(self) -> None:
        """ Download the credentials data using `auth_key` and `course_id`. """
        base = 'https://api.pwskills.com/v1'
        links = {
            'profile': f'{base}/auth/profile',
            'submission': f'{base}/learn/submission/{self.cid}',
            'progress': f'{base}/learn/analytics/progress/course/{self.cid}'
        }

        for fname, url in links.items():
            sleep(1)
            res = self.api.get(url)
            with open(self.cookie_dir / (fname+'.json'), 'w') as f:
                dump(res, f, indent=2)

    @classmethod
    def delete(cls):
        cookie_dir = cls.get_cookie_dir()
        if cookie_dir is None:
            raise FileNotFoundError('Cookie not found.')

        dirname = Path(str(dt.fromisoformat(cookie_dir.stem)) + '.cookie')
        rmtree(dirname)
