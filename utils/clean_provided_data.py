""" This module is only for `providers`.

Used to remove the `userSubmission` key from JSON file. To avoid vulnerability.
"""

import logging
from json import dump, load
from pathlib import Path

import logger

from utils.utils import get_all_files


def clean_quiz_assignment_data():
    all_files = (get_all_files('data', 'quiz') +
                 get_all_files('data', 'assignment'))

    for i in all_files:
        d = load(open(i))

        # Delete userSubmission key
        try:
            del d['data']['userSubmission']
        except KeyError:
            continue
        else:
            # Save the modified data
            with open(i, 'w') as f:
                logging.info(f'Cleaned `{i}` for repo data.')
                dump(d, f, indent=2)

    print('clean_quiz_assignment_data >> Done!')


def clean_all_courses_data(path: Path):
    """ Get and Save the all courses details in JSON file. """
    try:
        data = (load(open(path))['pageProps']
                ['initialState']['filter']['initCourses'])

        courses = data['filter']['initCourses']
        to_dump = {"courses": courses}

        dump(to_dump, open(path, 'w'), indent=2)
    except KeyError:
        return None

    print('clean_all_courses_data >> Done!')


def main():
    clean_quiz_assignment_data()
    clean_all_courses_data(Path('data/courses/all_course_data.json'))


if __name__ == '__main__':
    main()
