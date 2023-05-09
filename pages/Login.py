""" Login to get access to amazing features. """

import streamlit as st

from utils import courses_dict
from utils.pw import Credentials, LoggedUser, PWApi

st.set_page_config('PW API Login', 'random', 'wide', 'expanded')
st_msg = st.empty()


def login_form():
    """ Login form for user. """
    with st.form('pw-api-login'):
        auth_key = st.text_input('Authorization Token')
        course_id = str(st.selectbox('Select Course', courses_dict.keys(),
                                     format_func=lambda x: courses_dict[x]))

        if st.form_submit_button():
            with st.spinner():
                try:
                    Credentials(auth_key, course_id).download()
                    st.session_state['auth_key'] = auth_key
                    st.session_state['cid'] = course_id
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
    l, r = st.columns([0.01, 0.6])
    force = l.checkbox('Force Update Links', label_visibility='collapsed',
                       help='Force Update Links')
    r.button('Update Assignment Solutions Link',
             on_click=api.update_solution_links,
             kwargs={'force_update': force},
             use_container_width=True)

    # Logout button
    if st.button('**Logout**', use_container_width=True,
                 on_click=Credentials.delete):
        st.experimental_rerun()
except FileNotFoundError:
    login_form()
except KeyError:
    Credentials.delete()
    st.experimental_rerun()
