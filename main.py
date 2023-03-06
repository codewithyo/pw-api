""" Used create directory structure and storing the auth_key in local directory. """

from argparse import ArgumentParser
from json import dump
from pathlib import Path
from time import sleep

from utils.downloader import pw_api
from utils.user import User


def mimic_dir() -> None:
    """ Create the important directories inside the cloned repo. """
    downloads = Path('downloads')

    # First make the downloads dir
    downloads.mkdir(exist_ok=True)

    # Sub folders in downloads dir
    downloads_sub_folder = ['assignment', 'courses', 'others', 'quiz']

    # Make all the dirs if not exists.
    for i in downloads_sub_folder:
        if not (f := downloads / i).exists():
            f.mkdir()

    # Make more dirs
    Path('logs').mkdir(exist_ok=True)


def cli_args() -> None:
    """ Used to taking argument before run. """
    parser = ArgumentParser()

    # Add arguments
    parser.add_argument('--auth-key', type=str, default=None,
                        help='Authorization Bearer Token from website. If not available pass `N/A`')
    parser.add_argument('--course-id', type=str, default=None,
                        help="Course ID from website's Url. If not available pass `N/A`")

    # Get passed args
    args = parser.parse_args()

    AUTH_KEY: str = args.AUTH_KEY
    COURSE_ID: str = args.COURSE_ID

    # Create user dictionary
    user = {
        "auth_key": AUTH_KEY,
        "course_id": COURSE_ID
    }

    # Store the auth_key into a file
    if AUTH_KEY is not None and COURSE_ID is not None and len(AUTH_KEY.split('.')) == 3:
        dump(user, open('user.json', 'w'))
    else:
        raise ValueError('Please provide the auth key.\n\
                         If you have not the key then enter `N/A` as string value.')


def download_credentials(auth_key: str, course_id: str) -> None:
    """ Used to download the credentials data using `auth_key` and `course_id`. """
    links = {
        'profile': 'https://api.pwskills.com/v1/auth/profile',
        'submission': f'https://api.pwskills.com/v1/learn/submission/{course_id}',
        'user_progress': f'https://api.pwskills.com/v1/learn/analytics/progress/course/{course_id}'
    }

    for type, url in links.values():
        sleep(2)
        pw_api.download(url, auth_key, type)


def main() -> None:
    cli_args()
    mimic_dir()

    auth_key = User.auth_key()
    course_id = User.course_id()

    if auth_key is not None and course_id is not None:
        download_credentials(auth_key, course_id)


if __name__ == '__main__':
    main()
