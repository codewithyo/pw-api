from __future__ import annotations

from typing import List, Optional

import pandas as pd
from pydantic import BaseModel

from utils.streamlit.live_course import LiveCourse


class Img(BaseModel):
    link: str
    source: str


class User(BaseModel):
    _id: str
    firstName: str
    lastName: str
    img: Optional[Img] = None


class Submission(BaseModel):
    _id: str
    assignmentsMarkedCount: int
    totalAssignmentsScore: int
    userId: str


class QuizAnalytic(BaseModel):
    _id: str
    totalPoints: int
    firstName: str
    lastName: str
    img: Optional[Img] = None


class AnalyticsUsers(BaseModel):
    users: List[User]

    def get_df(self):
        df = pd.DataFrame(self.dict()['users'])
        return df


class AnalyticsSubmissions(BaseModel):
    submissions: List[Submission]

    def get_df(self):
        df = pd.DataFrame(self.dict()['submissions'])
        return df


class QuizAnalytics(BaseModel):
    quizAnalytics: List[QuizAnalytic]

    def get_df(self):
        df = pd.DataFrame(self.dict()['quizAnalytics'])
        return df


def get_live_course_df(data, course_name, course_id) -> pd.DataFrame:
    live_course = {
        "paramLength": 0,
        "sections": data,
        "courseName": course_name,
    }

    return LiveCourse(**live_course).merged_df(course_id)
