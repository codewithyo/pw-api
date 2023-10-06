from typing import Any

import requests

from src import COURSES_MAPPING_PATH
from src.core import io
from src.core.logger import get_logger

logger = get_logger(__name__)


def get_courses_from_v1() -> list[dict[str, Any]]:
    url = "https://api.pwskills.com/v1/course"
    r = requests.get(url)
    r.raise_for_status()
    logger.info(f"[{r.status_code}]:{r.url}")
    return r.json()["data"]


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

    r = requests.post(
        url="https://api.pwskills.com/v2/course/search",
        params=params,
        json=json_data,
    )
    r.raise_for_status()
    logger.info(f"[{r.status_code}]:{r.url}")

    courses = r.json()["data"]["courses"]
    return courses


def updated_courses_data() -> dict[str, str]:
    v1_courses = get_courses_from_v1()
    v2_courses = get_courses_from_v2()

    courses = v1_courses + v2_courses
    new_courses_dict = {
        i["_id"]: i["title"]
        for i in courses
        if "popular" in i["tags"] or "live" in i["tags"]
    }

    stored_courses_dict: dict[str, str] = io.load_json(COURSES_MAPPING_PATH)
    logger.info(f"Count of previous stored courses is {len(stored_courses_dict)}.")

    stored_courses_dict.update(new_courses_dict)
    logger.info(
        f"Count of courses after adding new courses is {len(stored_courses_dict)}."
    )

    return stored_courses_dict


def store_all_courses_data() -> None:
    data = updated_courses_data()

    try:
        logger.info(f"Storing all courses data into '{COURSES_MAPPING_PATH}'")
        io.dump_json(data, COURSES_MAPPING_PATH)
    except FileNotFoundError as e:
        logger.error(e)
        logger.warning(f"Storing empty data into '{COURSES_MAPPING_PATH}'")
        io.dump_json({}, COURSES_MAPPING_PATH)
    finally:
        io.dump_json(data, COURSES_MAPPING_PATH)
        logger.info(f"Successfully stored courses data at '{COURSES_MAPPING_PATH}'")
