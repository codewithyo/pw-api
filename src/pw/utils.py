from typing import Any

from requests import get, post

from src import courses_dict_fp
from src.core import io
from src.core.logger import get_logger

logger = get_logger(__name__)


def get_all_courses_dict() -> None:
    url = "https://api.pwskills.com/v1/course"

    courses: list[dict[str, Any]] = get(url).json()["data"]
    courses = courses + get_courses_from_v2()

    new_courses_dict = {
        i["_id"]: i["title"]
        for i in courses
        if "popular" in i["tags"] or "live" in i["tags"]
    }

    all_courses_dict: dict[str, str] = io.load_json(courses_dict_fp)
    try:
        all_courses_dict.update(new_courses_dict)
        io.dump_json(all_courses_dict, courses_dict_fp)
    except Exception:
        io.dump_json({}, courses_dict_fp)
        logger.error("")
    finally:
        io.dump_json(all_courses_dict, courses_dict_fp)


def get_courses_from_v2() -> list[dict[str, Any]]:
    """Get courses from API v2 of PW Skills."""
    params = {
        "page": "NaN",
        "limit": "10000",
    }

    json_data = {
        "level": "",
        "programType": "",
        "instructors": [],
        "categories": [],
        "languages": [],
        "subcategories": [],
        "domains": [],
    }

    r = post(
        url="https://api.pwskills.com/v2/course/search",
        params=params,
        json=json_data,
    )
    r.raise_for_status()

    courses = r.json()["data"]["courses"]
    return courses
