from json import dump, load
from pathlib import Path
from typing import Literal


class User:
    """ Give information about the user. """
    @classmethod
    def auth_key(cls) -> str | None:
        """ Authorization Key of the User. """
        auth_key = load(open('user.json'))['auth_key']

        if auth_key != 'N/A':
            return auth_key

    @classmethod
    def course_id(cls) -> str | None:
        """ Course Id provided by the User. """
        course_id = load(open('usr.json'))['course_id']

        if course_id != 'N/A':
            return course_id

    @classmethod
    def update_auth_key(cls, value: str) -> None:
        if len(value.split('.')) == 3:
            # Load user.json
            user = load(open('user.json'))

            # Update auth_key
            user['auth_key'] = value

            # Dump updated user dictionary
            dump(user, open('user.json', 'w'))

    @classmethod
    def update_course_id(cls, value: str) -> None:
        # Load user.json
        user = load(open('user.json'))

        # Update course_id
        user['course_id'] = value

        # Dump updated user dictionary
        dump(user, open('user.json', 'w'))

    @classmethod
    def get_all_files(cls,
                      from_: Literal['data', 'downloads'],
                      type: Literal['quiz', 'assignment', 'others']) -> list[Path]:
        """ Return all the path of JSON files present in the Folder. """
        path = Path() / from_ / type

        files = []
        for i in path.iterdir():
            if i.is_dir():
                files += [j for j in i.iterdir() if j.suffix == '.json']
            else:
                if i.suffix == '.json':
                    files.append(i)
        return files
