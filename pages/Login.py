""" Login to get access to amazing features. """

from json import load

import streamlit as st

from utils.pw.credentials import Credentials
from utils.pw.user import LoggedUser

st.set_page_config('PW API Login', 'random', 'wide', 'expanded')
st_msg = st.empty()
courses_dict: dict = load(open('data/courses/all_courses_dict.json'))


def login_form():
    """ Login form for user. """
    with st.form('pw-api-login'):
        auth_key = st.text_input('Authorization Token')
        sl_course = st.selectbox('Select Course', courses_dict.keys())

        # Get course id from course dict
        course_id = courses_dict[sl_course]

        if st.form_submit_button():
            with st.spinner():
                try:
                    Credentials(auth_key, course_id).download()
                    st.experimental_rerun()
                except ValueError:
                    st_msg.error('Please check your auth key or chosen course.')


try:
    user = LoggedUser()
    profile = user.profile

    # Show profile image
    img = profile.get('img', None)
    if img is not None:
        if img['source'] == 'oauth':
            st.image(img['link'])
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

    # Logout button
    if st.button('**Logout**', use_container_width=True,
                 on_click=Credentials.delete):
        st.experimental_rerun()
except FileNotFoundError:
    login_form()
except KeyError:
    Credentials.delete()
    st.experimental_rerun()
