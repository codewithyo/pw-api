from json import load
from pathlib import Path
from typing import TypeAlias

from utils.streamlit.analytics import (AnalyticsSubmissions, AnalyticsUsers,
                                       QuizAnalytics, get_live_course_df)
from utils.streamlit.live_course import LiveCourse
from utils.streamlit.preview_course import PreviewCourse

CourseName: TypeAlias = str
CourseId: TypeAlias = str

courses_dict_fp = Path('data/all_courses_dict.json')
courses_dict: dict[CourseId, CourseName] = load(open(courses_dict_fp))
