from json import load
from pathlib import Path

from utils.streamlit.analytics import (AnalyticsSubmissions, AnalyticsUsers,
                                       QuizAnalytics, get_live_course_df)
from utils.streamlit.course import Course, get_course_id_title
from utils.streamlit.live_course import LiveCourse
from utils.streamlit.preview_course import PreviewCourse

courses_dict_fp = Path('data/courses/all_courses_dict.json')
courses_dict: dict[str, str] = load(open(courses_dict_fp))
