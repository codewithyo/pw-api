from __future__ import annotations

from typing import Optional

import pandas as pd
from pydantic import BaseModel, Field


class Pricing(BaseModel):
    IN: int
    discount: float


class Social(BaseModel):
    linkedin: Optional[str] = None
    instagram: Optional[str] = None
    facebook: Optional[str] = None
    youtube: Optional[str] = None
    github: Optional[str] = None


class Img(BaseModel):
    source: str
    link: str


class InstructorsDetail(BaseModel):
    name: str
    social: Social
    img: Img
    description: str


class Overview(BaseModel):
    learn: list[str]
    requirements: list[str]
    features: list[str]
    language: str


class CourseMeta(BaseModel):
    instructors: list[str]
    certificateBenchmark: int
    overview: Overview
    curriculum: list[dict]
    projects: list[dict]
    duration: str = 'N/A'


class PreviewCourse(BaseModel):
    courseId: str = Field(..., alias='_id')
    title: str
    pricing: Pricing
    img: str
    instructorsDetails: list[InstructorsDetail]
    courseMetas: list[CourseMeta]

    def curriculum_df(self):
        data = self.courseMetas[0].curriculum
        df = pd.DataFrame(data)

        df = df.merge(df[['parent', 'title']],
                      how='inner',
                      left_on='_id',
                      right_on='parent',
                      suffixes=('_parent', '_child'))

        df.drop(columns=['_id', 'preview', 'parent_parent', 'parent_child'],
                inplace=True)

        df.rename(columns={
            'title_parent': 'parentTitle',
            'title_child': 'childTitle'
        }, inplace=True)

        return df

    def projects_df(self):
        projects = self.courseMetas[0].projects

        if not projects:
            raise ValueError('No project in this course.')

        paren_proj = (pd.DataFrame([i for i in projects if len(i) == 2])
                      .rename(columns={'_id': 'parentId',
                                       'title': 'parentTitle'}))

        child_proj = (pd.DataFrame([i for i in projects if len(i) != 2])
                      .rename(columns={'_id': 'childId',
                                       'parent': 'parentId',
                                       'title': 'childTitle'}))

        project_df = paren_proj.merge(child_proj, 'inner', 'parentId')

        return project_df
