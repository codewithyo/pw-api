import logging
from json import loads

import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from requests import get

from utils import LiveCourse, courses_dict
from utils.logger import LoggingMessage

plt.style.use('ggplot')


# Set page config
st.set_page_config('Preview Courses', '🗂️', 'wide')

# --- --- Sidebar --- --- #
with st.sidebar:
    cid = str(st.selectbox('Select Course', courses_dict.keys(),
                           format_func=lambda x: courses_dict[x]))
    course_name = courses_dict[cid]
    radio = st.radio('Select Page', ['Overview', 'Topics Resource', 'Extra Resource'],
                     label_visibility='hidden')


# Get response from api
@st.cache_resource
def get_live_course_dict(course_name: str, course_id: str):
    """ Return the required live course data as Python dict. """
    url = 'https://learn.pwskills.com/course/{}/{}'.format(course_name.replace(' ', '-'),
                                                           course_id)
    r = get(url)
    logging.info(LoggingMessage.get_request_log.format(url))
    logging.info(LoggingMessage.status_code_log.format(r.status_code))

    soup = BeautifulSoup(r.text, 'html.parser')
    script = soup.find('script', {'id': '__NEXT_DATA__'})

    if script:
        data = script.text
    else:
        raise TypeError('Required script tag is not available.')

    return loads(data)['props']['pageProps']


# LiveCourse Instance
lc_dict = get_live_course_dict(course_name, cid)
lc = LiveCourse(**lc_dict)

# Merged section and lesson data as df
df = lc.merged_df(cid)


def display_curr_details(title: str):
    """ Display the desired section details. """
    for i in df['sectionsTitle'].unique():
        if title == i:
            new_df = df.query('sectionsTitle==@i')
            # Get date
            date = new_df['date'].mean()

            try:
                exp = st.expander(f'🗂️ {i} - **{date:%d %B, %Y}**', True)
            except ValueError:
                exp = st.expander(f'🗂️ {i}', True)

            for j in new_df.query('type=="video"')['lessonsTitle'].values:
                exp.write(f' - {j}')

            # Get urls of selected
            q_url = (new_df.query('type=="quiz"')
                     [['lessonsTitle', 'url']].values)
            as_url = (new_df.query('type=="assignment"')
                      [['lessonsTitle', 'url']].values)

            # Display quiz url
            if len(q_url) > 0:
                exp.write('---')
                exp.write(f'##### Quiz Url:')
                exp.write(
                    'Quiz url does not work. You have go to [Quiz Page.](/Quiz)')
                for q_title, url in q_url:
                    exp.write(f'- [{q_title}]({url})')

            # Display assignment url
            if len(as_url) > 0:
                exp.write('---')
                exp.write(f'##### Assignment Url:')
                for asg_title, url in as_url:
                    exp.write(f'- [{asg_title}]({url})')


match radio:
    case 'Overview':
        st.title(f'Overview of :red[{course_name}] course')

        # Quiz and Assignment details
        col1, col2, col3, col4 = st.columns(4)
        try:
            total_quiz_ques = df['totalQuestionsInQuiz'].sum()
            total_asg_points = df['totalPointsInAssignment'].sum()
            total_video_duration = round(df['duration'].sum() / 3600)
        except KeyError:
            total_quiz_ques = 0
            total_asg_points = 0
            total_video_duration = 'N/A'

        col1.metric('No. of questions in Quiz', int(total_quiz_ques))
        col2.metric('Total Assignments points', int(total_asg_points))
        col3.metric('Duration of videos in course',
                    f'{total_video_duration} hours')

        # Dates metrics
        max_date = df['date'].max()
        min_date = df['date'].min()

        col4.metric('The course has runs for',
                    f'{(max_date-min_date).days} days')
        try:
            col1.metric('First update in course', f'{min_date:%d %h, %y}')
            col2.metric('Last update in course', f'{max_date:%d %h, %y}')
        except ValueError:
            col1.metric('First update in course', 'N/A')
            col2.metric('Last update in course', 'N/A')

        st.write('---')
        # Plot course resource count plot
        fig, ax = plt.subplots()
        df['type'].value_counts().plot(kind='barh', ax=ax,
                                       title='Distribution of course resources',
                                       ylabel='Resources', xlabel='Count',
                                       figsize=(10, 3), grid=False)
        st.pyplot(fig)

    case 'Topics Resource':
        st.title(f'Resources of :red[{course_name}] course')

        form = st.form('Section Resources')
        title = form.selectbox('Select Course Section',
                               sorted(df['sectionsTitle'].unique()))
        if form.form_submit_button():
            display_curr_details(str(title))

    case 'Extra Resource':
        st.title(f'Extra Resourses in :red[{course_name}] course')

        new_df = df.query('type=="sectionResource"')
        for i in new_df['sectionsTitle'].unique():
            sl_df = new_df.query('sectionsTitle==@i')
            date = sl_df['date'].mean()
            text = f'🗂️ {i}' if date else f'🗂️ {i}'

            with st.expander(text):
                for _, title, url in sl_df[['lessonsTitle', 'url']].itertuples():
                    st.write(f'- [{title}]({url})')
