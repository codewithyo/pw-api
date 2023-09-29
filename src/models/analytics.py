from __future__ import annotations

from typing import Optional

import pandas as pd
from pydantic import BaseModel

from src.models.live_course import LiveCourse


class Img(BaseModel):
    link: str | None = None


class User(BaseModel):
    firstName: str
    lastName: str
    img: Optional[Img] = None

    def get_img_link(self) -> str:
        rv = """<img alt="student-pic" src="{}" height=50 width=50 style="border-radius:10px;">"""

        if self.img is None or self.img.link is None:
            src = "https://learn.pwskills.com/_next/image?url=https%3A%2F%2Fcdn.pwskills.com%2Fuser%2Fprofile_pictures%2F63a1f5889d90b2b9e65c8a73.jpeg&w=96&q=75"
            return rv.format(src)

        if ".jpeg" in self.img.link:
            src = f"https://learn.pwskills.com/_next/image?url=https%3A%2F%2Fcdn.pwskills.com%2Fuser%2Fprofile_pictures%2F{self.img.link}&w=96&q=75"
            return rv.format(src)
        else:
            src = (
                f"https://learn.pwskills.com/_next/image?url={self.img.link}&w=96&q=75"
            )
            return rv.format(src)


class Submission(BaseModel):
    assignmentsMarkedCount: int
    totalAssignmentsScore: int


class QuizAnalytic(BaseModel):
    totalPoints: int
    firstName: str
    lastName: str
    img: Optional[Img] = None


class AnalyticsUsers(BaseModel):
    users: list[User]

    def get_df(self):
        df = pd.DataFrame(self.model_dump()["users"])
        return df


class AnalyticsSubmissions(BaseModel):
    submissions: list[Submission]

    def get_df(self):
        df = pd.DataFrame(self.model_dump()["submissions"])
        return df


class QuizAnalytics(BaseModel):
    quizAnalytics: list[QuizAnalytic]

    def get_df(self):
        df = pd.DataFrame(self.model_dump()["quizAnalytics"])
        return df


def get_live_course_df(data: dict, course_name: str, course_id: str) -> pd.DataFrame:
    live_course = {
        "courseName": course_name,
        "sections": data,
    }
    return LiveCourse(**live_course).merged_df(course_id)
