import logging
import webbrowser
from json import load, loads

import streamlit as st
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from requests import get

import utils.logger
from utils import LiveCourse
from utils.logger import LoggingMessage

courses_dict: dict = load(open('data/courses/all_courses_dict.json'))

# Set page config
st.set_page_config('Preview Courses', '🗂️', 'wide')

# --- --- Sidebar --- --- #
with st.sidebar:
    sl = str(st.selectbox('Select Course', courses_dict.keys()))
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
lc_dict = get_live_course_dict(sl, courses_dict[sl])
lc = LiveCourse(**lc_dict)

# Merged section and lesson data as df
df = lc.merged_df(courses_dict[sl])


def display_curr_details(title: str):
    """ Display the desired section details. """
    for i in df['sectionsTitle'].unique():
        if title == i:
            new_df = df.query('sectionsTitle==@i')
            # Get date
            date = new_df['date'].mean()

            if date:
                exp = st.expander(f'🗂️ {i} - **{date:%d %B, %Y}**', True)
            else:
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
                exp.write('Quiz url does not work. You have go to [Quiz Page.](\
                    http://localhost:8501/Quiz)')
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
        st.write(f'For detailed analysis head to [Jupyter Notebook.](\
            https://github.com/arv-anshul/working-with-pw-api/blob/main/analysis/live_course_analysis.ipynb)')
        st.title(f'Overview of :red[{sl}] course.')

        # Quiz and Assignment details
        col1, col2, col3, col4 = st.columns(4)
        total_quiz_ques = df['totalQuestionsInQuiz'].sum()
        total_asg_points = df['totalPointsInAssignment'].sum()
        total_video_duration = round(df['duration'].sum() / 3600, 2)

        col1.metric('No. of questions in Quiz', int(total_quiz_ques))
        col2.metric('Total Assignments points', int(total_asg_points))
        col3.metric('Total Duration of videos in course', total_video_duration)

        # Dates metrics
        max_date = df['date'].max()
        min_date = df['date'].min()

        col4.metric('The course has runs for',
                    f'{(max_date-min_date).days} days')
        col1.metric('First update in course', f'{min_date:%d %h, %y}')
        col2.metric('Last update in course', f'{max_date:%d %h, %y}')

        st.write('---')
        # Plot course resource count plot
        fig, ax = plt.subplots()
        df['type'].value_counts().plot(kind='bar', ax=ax,
                                       title='Distribution of resources in the Course',
                                       xlabel='Resources', ylabel='Count',
                                       figsize=(6, 4))
        fig_col1, fig_col2 = st.columns(2)
        fig_col1.pyplot(fig)

    case 'Topics Resource':
        st.title(f'Resources of {sl} course.')

        form = st.form('Section Resources')
        title = form.selectbox('Select Course Section',
                               sorted(df['sectionsTitle'].unique()))
        if form.form_submit_button():
            display_curr_details(str(title))

    case 'Extra Resource':
        st.title(f'Extra Resourses in {sl} course.')

        # new_df includes sectionResources type
        new_df = df.query('type=="sectionResource"')

        # One expander for every section
        for i in new_df['sectionsTitle'].unique():
            sl_df = new_df.query('sectionsTitle==@i')

            # Get date to display
            date = sl_df['date'].mean()

            text = f'🗂️ {i} - **{date:%d %h, %y}**' if date else f'🗂️ {i}'

            with st.expander(text):

                for _, title, url in sl_df[['lessonsTitle', 'url']].itertuples():
                    st.write(f'- [{title}]({url})')
