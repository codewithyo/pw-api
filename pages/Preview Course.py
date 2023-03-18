import logging
from json import load

import pandas as pd
import streamlit as st
from requests import get

import utils.logger
from utils.logger import LoggingMessage
from utils.streamlit.preview_course import PreviewCourse

courses_dict: dict = load(open('data/courses/all_courses_dict.json'))

# Set page config
st.set_page_config('Preview Courses', '🗂️', 'wide')

# --- --- Sidebar --- --- #
with st.sidebar:
    sl = str(st.selectbox('Select Course', courses_dict.keys()))
    radio = st.radio('Select Page', ['Main', 'Curriculum', 'Projects'],
                     label_visibility='hidden')


# Get response from api
@st.cache_resource
def get_preview_course_object(id: str):
    url = f"https://api.pwskills.com/v1/course/{id}?withAllCourseMetas=true&ignoreInActive=true"
    r = get(url)
    pc = r.json()['data']
    logging.info(LoggingMessage.get_request_log.format(url))
    logging.info(LoggingMessage.status_code_log.format(r.status_code))

    return pc


# PreviewCourse Instance
pc_dict = get_preview_course_object(courses_dict[sl])
pc = PreviewCourse(**pc_dict)


def display_curr_details(df: pd.DataFrame, pat: str):
    """ Display the desired project. """
    for i in df['parentTitle'].unique():
        if pat.lower() in i.lower():
            new_df = df.query('parentTitle==@i')

            # Get date
            date = new_df['date'].mean()

            if date:
                exp = st.expander(f'🗂️ {i} - **{date:%d %B, %Y}**')
            else:
                exp = st.expander(f'🗂️ {i}')

            for c in new_df['childTitle'].values:
                exp.write(f'  - {c}')


match radio:
    case 'Main':
        st.write('For detailed analysis head to [Jupyter Notebook](\
                https://github.com/arv-anshul/working-with-pw-api/blob/main/analysis/_course_analysis.ipynb).')

        # st.metric(courses_dict[sl], pc.title)
        st.title(pc.title)
        f'###### :red[Language :] :green[{pc.courseMetas[0].overview.language.capitalize()}]'
        f'###### :red[Duration :] :green[{pc.courseMetas[0].duration}]'

        # Price of the Course
        course_price = round(
            pc.pricing.IN - (pc.pricing.IN * pc.pricing.discount/100))
        st.write(f'###### :red[Price of Course:] :green[₹{course_price} /-]')

        # Instructors Name
        inst_names = [i.name for i in pc.instructorsDetails]
        st.write(
            f"###### :red[Name of instructors:] :green[{', '.join(inst_names)}]")

        # Course Certificate Benchmark
        cert_bench = pc.courseMetas[0].certificateBenchmark
        st.write(f'###### :red[Certificate Benchmark:] :green[{cert_bench}%]')

        # Language of the Course
        lang = pc.courseMetas[0].overview.language
        st.write(
            f'###### :red[Language of Course:] :green[{lang.capitalize()}]')

        # Course duration
        duration = pc.courseMetas[0].duration
        st.write(f'###### :red[Course duration:] :green[{duration}]')

        with st.expander('**🔖 &nbsp; &nbsp; What you Learn from this course?**'):
            for i, j in enumerate(pc.courseMetas[0].overview.learn, 1):
                f'{i}. {j}'

        with st.expander('**🎁 &nbsp; &nbsp; Features of the Course.**'):
            for i, j in enumerate(pc.courseMetas[0].overview.features, 1):
                f'{i}. {j}'

        with st.expander('**👨 &nbsp; &nbsp; Instructors Details**'):
            for ins in pc.instructorsDetails:
                f'### 👨‍🏫 &nbsp; {ins.name}'
                f'{ins.description}'

                for name, url in ins.social.dict().items():
                    if url:
                        f'###### 🔗 {name.capitalize()}: {url}'
                '---'

    case 'Curriculum':
        st.title(f'Curriculum of :red[{pc.title}] Course.')

        df = pc.curriculum_df()

        st.metric(courses_dict[sl], pc.title)
        st.write(
            f":red[Sections in Course:] :green[{df['parentTitle'].nunique()}]")
        st.write(
            f":red[Lessons in Course:] :green[{df['childTitle'].nunique()}]")

        st.write('---')

        form = st.form('curriculum_choice')
        choice = form.text_input('Enter Section Name')

        if form.form_submit_button():
            display_curr_details(df, choice)

    case 'Projects':

        st.metric(courses_dict[sl], pc.title)
        st.write('---')
        try:
            df = pc.projects_df()
        except ValueError as e:
            st.error(e, icon='🚨')
        else:
            # Expander 1
            exp1 = st.expander(f"📌&nbsp; This course has **{df['parentId'].nunique()}** \
                different **types of (parent) topics** for project which are:")

            for i in df['parentTitle'].unique():
                exp1.write(f'  - {i}')

            # Expander 2
            exp2 = st.expander(f"📍 There are **{df['childId'].nunique()}+** \
                    different **(child) topics** for project which are:")

            for i in df['parentTitle'].unique():
                exp2.write(f'  + {i}')
                for _, ii, j in df[['parentTitle', 'childTitle']].itertuples():
                    if ii == i:
                        exp2.write(f"    - {j}")

            st.write('---')

            form = st.form('project_choice')
            choice = form.text_input('Enter Parent Project Name')

            if form.form_submit_button():
                display_curr_details(df, choice)

    case _:
        st.error('Nothing Selected!!')
