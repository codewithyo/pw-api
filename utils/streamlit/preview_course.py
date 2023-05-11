from __future__ import annotations

from typing import List, Optional

import pandas as pd
from pydantic import BaseModel


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
    learn: List[str]
    requirements: List[str]
    features: List[str]
    language: str


class CourseMeta(BaseModel):
    instructors: List[str]
    certificateBenchmark: int
    overview: Overview
    curriculum: list[dict]
    projects: list[dict]
    duration: str = 'N/A'


class PreviewCourse(BaseModel):
    _id: str
    title: str
    pricing: Pricing
    img: str
    instructorsDetails: List[InstructorsDetail]
    courseMetas: List[CourseMeta]

    def curriculum_df(self):
        data = self.courseMetas[0].curriculum
        df = pd.DataFrame(data)

        df = df.merge(df[['parent', 'title']],
                      how='inner',
                      left_on='_id',
                      right_on='parent',
                      suffixes=('_parent', '_child'))

        # Drop columns
        df.drop(columns=['_id', 'preview', 'parent_parent', 'parent_child'],
                inplace=True)

        # Rename columns
        df.rename(columns={
            'title_parent': 'parentTitle',
            'title_child': 'childTitle'
        }, inplace=True)

        # Create date column
        df['date'] = pd.to_datetime(
            df['parentTitle']
            .str.rsplit(r'23', n=1).str.get(0).add('23')
            .str.replace(r'^\d{1,2} - ', '', regex=True),
            format="%d %b'%y", errors='coerce')

        # Remove date sub-string from parentTitle
        df['parentTitle'] = (df['parentTitle']
                             .apply(lambda x: str(x).rsplit('23', 1)[-1] if x else x)
                             .str.strip())

        return df

    def projects_df(self):
        projects = self.courseMetas[0].projects

        if not projects:
            raise ValueError('No any projects available for this course.')

        paren_proj = (pd.DataFrame([i for i in projects if len(i) == 2])
                      .rename(columns={'_id': 'parentId',
                                       'title': 'parentTitle'}))

        child_proj = (pd.DataFrame([i for i in projects if len(i) != 2])
                        .rename(columns={'_id': 'childId',
                                         'parent': 'parentId',
                                         'title': 'childTitle'}))

        # Merge dfs
        project_df = paren_proj.merge(child_proj, 'inner', 'parentId')

        # Create date column
        project_df['date'] = (project_df['childTitle']
                              .str.extract(r"(\d{1,2} \w{3,5}'23)"))

        # Fill the null dates values
        null_date = project_df[project_df['date'].isnull() == 1]
        project_df.loc[null_date.index, 'date'] = (null_date['parentTitle']
                                                   .str.extract(r"(\d{1,2} \w{3,5}'23)")[0])

        # Convert date column data type
        project_df['date'] = pd.to_datetime(project_df['date'],
                                            format="%d %b'%y", errors='coerce')

        # Filter parenTitle
        project_df['parentTitle'] = (project_df['parentTitle']
                                     .str.replace(r"(\d{1,2} \w{3,5}'23)", '', regex=True)
                                     .str.split('-').str.get(-1)
                                     .str.strip())

        # Filter childTitle
        project_df['childTitle'] = (project_df['childTitle']
                                    .str.replace(r"(\d{1,2} \w{3,5}'23)", '', regex=True)
                                    .str.strip())

        return project_df
