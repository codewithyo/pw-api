from json import load, loads

import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup
from requests import HTTPError, get

from utils import AnalyticsSubmissions, AnalyticsUsers, get_live_course_df
from utils.logger import LoggingMessage, logging
from utils.streamlit.analytics import QuizAnalytics

# Page config
st.set_page_config('Course Analytics', '🎁', 'wide')


@st.cache_resource
def get_analytics_data(url):
    r = get(url)
    logging.info(LoggingMessage.get_request_log.format(url))
    logging.info(LoggingMessage.status_code_log.format(r.status_code))

    if r.status_code != 200:
        logging.error('URL response is not 200.')
        raise HTTPError('URL: {url} response is not 200.')

    # Parse html with BeautifulSoup
    soup = BeautifulSoup(r.text, 'html.parser')
    script = soup.find('script', {'id': '__NEXT_DATA__'})
    data = loads(script.text)   # type: ignore

    # Get submission, user and quizAnalytics data
    submissions = data['props']['pageProps']['analytics']['submissions']
    users = data['props']['pageProps']['analytics']['users']
    quiz_analytics = data['props']['pageProps']['quizAnalytics']

    return (
        AnalyticsSubmissions(**{'submissions': submissions}),
        AnalyticsUsers(**{'users': users}),
        QuizAnalytics(**{'quizAnalytics': quiz_analytics}),
        get_live_course_df(
            data['props']['pageProps']['sections'],
            sl_course,
            courses_dict[sl_course],
        )
    )


def get_url(course_name: str):
    """ Course analytics url constructor. """
    base = f'https://learn.pwskills.com/course-analytics/{course_name.replace(" ", "-")}/'
    return base + courses_dict[course_name]


courses_dict = load(open('data/courses/all_courses_dict.json'))

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
# Sidebar
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
with st.sidebar:
    sl_course = str(st.selectbox('Select Course', courses_dict))

    radio = st.radio('Select Analytics',
                     ['Assignments Analytics', 'Quiz Analytics'])

try:
    (sub, users, qz, lc) = get_analytics_data(get_url(sl_course))
except KeyError:
    st.title('This course has not any analytics.')
else:
    st.metric(courses_dict[sl_course], sl_course)

    resource_type_count = lc['type'].value_counts().to_dict()
    total_assignment_points = int(lc['totalPointsInAssignment'].sum())
    try:
        total_quiz_points = int(lc['totalQuestionsInQuiz'].sum())
    except KeyError as e:
        lc[e] = pd.NA
        total_quiz_points = 0

    total_video_duration = int(lc['duration'].sum()/3600)

    col1, col2 = st.columns(2)
    col1.markdown(
        f"""
        **:red[Max Points in Assignments:]** {total_assignment_points}  
        **:red[Max Points in Quiz:]** {total_quiz_points}  
        **:red[Total Duration of Lectures:]** {total_video_duration} Hours

        ---
        """
    )
    try:
        assign_count = resource_type_count['assignment']
        quiz_count = resource_type_count['quiz']
        video_count = resource_type_count['video']
    except KeyError as e:
        resource_type_count[e] = 0
    else:
        col2.markdown(
            f"""
            **:red[Total No. of Assignment:]** {assign_count}  
            **:red[Total No. of Quizzes:]** {quiz_count}  
            **:red[Total No. of Lectures:]** {video_count}

            ---
            """
        )

    def get_img_url(img_url: str):
        return f'https://learn.pwskills.com/_next/image?url=https%3A%2F%2Fcdn.pwskills.com%2Fuser%2Fprofile_pictures%2F{img_url}&w=96&q=75'

    def get_ggl_img_url(img_url: str):
        base = f'https://learn.pwskills.com/_next/image?url={img_url}&w=96&q=75'
        return base

    if radio == 'Assignments Analytics':
        # --- --- Top 3 - Students --- ---
        cols = st.columns(3)
        for i in range(3):
            # for i, col in zip(range(3), cols):
            student_submission = sub.submissions[i]
            student = users.users[i]

            # Display Profile Pic
            dp = student.img
            if dp is not None:
                dp = dp.link
                if '.jpeg' in dp:
                    cols[i].write(
                        f"""<img alt="student-pic" src="{get_img_url(dp)}" height=50 width=50 style="border-radius:10px;">""",
                        unsafe_allow_html=True
                    )
                else:
                    cols[i].write(
                        f"""<img alt="student-pic" src="{get_ggl_img_url(dp)}" height=50 width=50 style="border-radius:10px;">""",
                        unsafe_allow_html=True
                    )
            else:
                dp = 'https://th.bing.com/th/id/OIP.XKH_KhtSn3INzWSxQG8ZTQHaHa?pid=ImgDet&rs=1'
                cols[i].write(
                    f"""<img alt="student-pic" src="{dp}" height=50 width=50 style="border-radius:10px;">""",
                    unsafe_allow_html=True
                )

            # Display Student Metrics
            cols[i].metric(
                f'**:green[{student.firstName} {student.lastName}]**',
                f'{student_submission.totalAssignmentsScore} / {student_submission.assignmentsMarkedCount}',
                help='Assignments Score / Assignments Marked Count'
            )
            cols[i].write('---')

        # --- --- Under 50 - Students --- --- #
        _, col_for_table, _ = st.columns([0.25, 0.5, 0.25])

        df1, df2 = users.get_df(), sub.get_df()
        df1['Name'] = df1['firstName'] + ' ' + df1['lastName']
        df = pd.concat([df1, df2], axis=1)

        col_for_table.table(
            df[['Name', 'assignmentsMarkedCount', 'totalAssignmentsScore']].loc[3:]
        )

    elif radio == 'Quiz Analytics':
        col, _ = st.columns([0.4, 0.6])
        col.header('Top 10 Students')

        df = qz.get_df()
        df['Name'] = df['firstName'] + ' ' + df['lastName']
        col.table(df[['Name', 'totalPoints']])
