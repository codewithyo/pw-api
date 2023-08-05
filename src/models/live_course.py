from __future__ import annotations

import pandas as pd
from pydantic import BaseModel, Field


class Sections(BaseModel):
    sectionId: str = Field(alias='_id')
    sections: list[dict]
    lessonDetails: list[dict]


class LiveCourse(BaseModel):
    courseName: str
    sections: Sections

    def sections_df(self):
        sections = pd.json_normalize(
            data=self.sections.sections,
            record_path='lessons',
            meta='title',
        )

        sections.rename(columns={0: '_id', 'title': 'sectionsTitle'},
                        inplace=True)

        return sections

    def lessons_df(self):
        lessons = pd.DataFrame(self.sections.lessonDetails)
        lessons['duration'] = (
            lessons['data'].str.get('duration'))  # type: ignore
        lessons['totalPointsInAssignment'] = (
            lessons['data'].str.get('maxPoints'))  # type: ignore
        lessons['url'] = lessons['data'].str.get('resourceURL')  # type: ignore

        lessons.drop(columns=['data', 'quizQuestions'], inplace=True)
        lessons.rename(columns={'title': 'lessonsTitle'}, inplace=True)

        return lessons

    def merged_df(self, course_id: str):
        sections = self.sections_df()
        lessons = self.lessons_df()

        df = sections.merge(lessons, on='_id', how='inner')

        # Base URL
        base_url = f'https://api.pwskills.com/v1/learn/lesson/course/{course_id}/'

        # URL for videos
        videos = df.query('type=="video"')
        df.loc[videos.index, 'url'] = base_url + videos['_id']

        # URL for quizzes
        quizzes = df.query('type=="quiz"')
        df.loc[quizzes.index, 'url'] = base_url + quizzes['_id']

        # URL for assignments
        assignments = df.query('type=="assignment"')
        df.loc[assignments.index, 'url'] = base_url + assignments['_id']

        return df
