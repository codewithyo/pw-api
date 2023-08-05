from __future__ import annotations

from typing import Optional

import pandas as pd
from pydantic import BaseModel


class Sections(BaseModel):
    _id: str
    sections: list[dict]
    lessonDetails: list[dict]


class LiveCourse(BaseModel):
    paramLength: Optional[int]
    courseName: str
    sections: Sections

    def sections_df(self):
        sections = pd.json_normalize(data=self.sections.sections,
                                     record_path='lessons',
                                     meta='title')

        # Create date column
        sections['date'] = pd.to_datetime(
            (sections['title']
             .str.rsplit('23', n=1).str.get(0).add('23')
             .str.replace(r" ?' ?23", ' 23', regex=True)
             .str.replace(r'^23$', '', regex=True)
             .str.replace(r'.*- ?', '', regex=True)
             .str.replace(r'st|th|rd', '', regex=True)
             ), format='%d %b %y', errors='coerce').bfill()

        # Clean title column
        sections['title'] = (sections['title']
                             .apply(lambda x: str(x).rsplit('23', 1)[-1] if x else x)
                             .str.strip())

        # Rename the cols
        sections.rename(columns={0: '_id', 'title': 'sectionsTitle'},
                        inplace=True)

        return sections

    def lessons_df(self):
        lessons = pd.DataFrame(self.sections.lessonDetails)

        # Get duration from data column
        lessons['duration'] = (lessons['data']
                               .str.get('duration'))  # type: ignore

        # Extract assignments maxPoints from data column.
        lessons['totalPointsInAssignment'] = (lessons['data']
                                              .str.get('maxPoints'))  # type: ignore

        # Create url column
        lessons['url'] = lessons['data'].str.get('resourceURL')  # type: ignore

        # Drop cols
        lessons.drop(columns=['data', 'quizQuestions'], inplace=True)

        # Rename the title column to differentiate
        lessons.rename(columns={
            'title': 'lessonsTitle'
        }, inplace=True)

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
