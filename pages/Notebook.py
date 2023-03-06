
import streamlit as st

from utils.course import Course, Instructors, get_course_id_title

# --- --- Sidebar --- --- #
course_dict = get_course_id_title()

with st.sidebar:
    sl = st.selectbox('Select Course', course_dict.keys())
    radio = st.radio(
        'Select Page', ['Main', 'Curriculum'])


def get_course(selected):
    cid = course_dict[selected]
    return Course(selected, cid)


# Course Object
c = get_course(selected=sl)

# --- --- Containers --- --- #
main = st.container()
curriculum = st.container()

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
if radio == 'Main':
    # with main:
    st.metric(c.id, c.name)
    f'###### :red[Language :] {c.language.capitalize()}'
    f'###### :red[Duration :] {c.duration}'

    with st.expander('**🔖 &nbsp; &nbsp; What you Learn from this course?**'):
        for i, j in enumerate(c.learn, 1):
            f'{i}. {j}'

    with st.expander('**🎁 &nbsp; &nbsp; Features of the Course.**'):
        for i, j in enumerate(c.features, 1):
            f'{i}. {j}'

    with st.expander('**👨 &nbsp; &nbsp; Instructors Details**'):
        for ins in c.instructors():
            f'### 👨‍🏫 &nbsp; {ins.name}'
            f'{ins.description}'

            for name, url in ins.social.items():
                if url:
                    f'###### 🔗 {name.capitalize()}: {url}'
            '---'


if radio == 'Curriculum':
    with curriculum:
        st.error(
            'For curriculum you have to provide the URL of the original webpage.',
            icon='🚨')
