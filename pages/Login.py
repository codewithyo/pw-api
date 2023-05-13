""" Login to get access to amazing features. """

from json import dumps, load

import streamlit as st
from requests import ReadTimeout

from utils import courses_dict
from utils.pw import Credentials, LoggedUser, PWApi

st.set_page_config('PW API Login', 'random', 'wide', 'expanded')
st_msg = st.empty()


def login_form():
    """ Login form for user. """
    with st.form('pw-api-login'):
        auth_key = st.text_input('Authorization Token')
        cid = str(st.selectbox('Select Course', courses_dict.keys(),
                               format_func=lambda x: courses_dict[x]))

        if st.form_submit_button():
            with st.spinner():
                try:
                    Credentials(auth_key, cid).download()
                    st.session_state['auth_key'] = auth_key
                    st.session_state['cid'] = cid
                    st.experimental_rerun()
                except ValueError:
                    st_msg.error(
                        'Please check your auth key or chosen course.')


try:
    user = LoggedUser()
    profile = user.profile
    api = PWApi(st.session_state['auth_key'], st.session_state['cid'])

    # Show profile image
    img = profile.get('img', None)
    if img is not None:
        if img['source'] == 'oauth':
            st.image(
                f"https://learn.pwskills.com/_next/image?url={img['link']}&w=96&q=75")
        elif img['source'] == 'bucket':
            url = f"https://learn.pwskills.com/_next/image?url=https%3A%2F%2Fcdn.pwskills.com%2Fuser%2Fprofile_pictures%2F{img['link']}&w=96&q=75"
            st.image(url)

    st.title(f"Hi! {profile['firstName']} {profile['lastName']}")
    st.subheader(f":red[E-mail:] {profile['email']}")

    # User social media
    user_social = profile.get('social', None)
    if user_social is not None:
        for media in user_social:
            st.subheader(f":red[{media.title()}:] {user_social[media]}")

    # Update Assignment Solutions Link
    update_solution_link = st.empty()

    # Fetches new quiz or assignment data and store it
    fetch_new_quiz_assignment = st.empty()

    # Download quiz or assignment data of logged in course
    save_quiz_assignment_json = st.empty()

    # Logout button
    if st.button('**Logout**', use_container_width=True,
                 on_click=Credentials.delete):
        st.experimental_rerun()
except FileNotFoundError:
    login_form()
    st.stop()
except KeyError:
    Credentials.delete()
    st.experimental_rerun()

with update_solution_link.container():
    l, r = st.columns([0.01, 0.6])
    force = l.checkbox('Force Update Links', label_visibility='collapsed',
                       help='Force Update Links')
    r.button('Update Assignment Solutions Link',
             on_click=api.update_solution_links,
             kwargs={'force_update': force},
             use_container_width=True)

with fetch_new_quiz_assignment.container():
    l, r = st.columns(2)
    quiz_dl = l.button('Fetch Course Quizzes', use_container_width=True)
    assign_dl = r.button('Fetch Course Assignments', use_container_width=True)
    type = 'quiz' if quiz_dl else 'assignment' if assign_dl else None

    if type is not None:
        try:
            with st.spinner(f'Fetching {type}(s)...'):
                st_msg.info('**Do not refresh the page.**')
                api.export_data(st.session_state['cid'], type)
            st_msg.success(f'You fetches all {type!r} data of your course')
        except ReadTimeout:
            st_msg.error(
                f'Re-click the {type!r} button to restart the fetching process.'
            )

with save_quiz_assignment_json.container():
    quiz_fp = api.generate_fp('quiz')
    assignment_fp = api.generate_fp('assignment')

    l, r = st.columns(2)
    l.download_button(
        'Save Quiz Data',
        dumps(load(open(quiz_fp)), indent=2) if quiz_fp.exists() else '[]',
        quiz_fp.name, 'json',
        use_container_width=True,
    )
    r.download_button(
        'Save Assignment Data',
        dumps(load(open(assignment_fp)), indent=2,
              ) if assignment_fp.exists() else '[]',
        assignment_fp.name, 'json',
        use_container_width=True,
    )
