from json import load
from pathlib import Path
from typing import TypeAlias

from src.models.analytics import (AnalyticsSubmissions, AnalyticsUsers,
                                  QuizAnalytics, get_live_course_df)
from src.models.live_course import LiveCourse
from src.models.preview_course import PreviewCourse

CourseName: TypeAlias = str
CourseId: TypeAlias = str

courses_dict_fp = Path('data/all_courses_dict.json')
courses_dict: dict[CourseId, CourseName] = load(open(courses_dict_fp))
