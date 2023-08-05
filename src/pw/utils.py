from json import dump

from requests import get

from src import courses_dict_fp


def get_all_courses_dict():
    url = 'https://api.pwskills.com/v1/course'
    courses = get(url).json()['data']

    dd = {i['_id']: i['title'] for i in courses
          if 'popular' in i['tags']}

    # Reverse the dict which arrange the courses as older to newer
    courses_dict = {i: dd[i] for i in reversed(dd.keys())}
    try:
        dump(courses_dict, open(courses_dict_fp, 'w'), indent=2)
    except Exception:
        dump({}, open(courses_dict_fp, 'w'))
