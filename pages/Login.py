""" Login to get access to amazing features. """

from json import dumps, load

import streamlit as st
from requests import ReadTimeout

from src import courses_dict
from src.pw import Credentials, LoggedUser, PWApi

st.set_page_config("PW API Login", "random", "wide", "expanded")
msg = st.empty()


def login_form():
    """Login form for user."""
    with st.form("pw-api-login"):
        auth_key = st.text_input("Authorization Token")
        cid = str(
            st.selectbox(
                label="Select Course",
                options=courses_dict.keys(),
                format_func=lambda x: courses_dict[x],
            )
        )
        login_for = int(
            st.number_input(
                label="Enter minutes for Logged In",
                min_value=0,
                max_value=30,
                value=10,
                format="%d",
                help="After X minutes you get automatically logout.",
            )
        )

        if st.form_submit_button():
            with st.spinner():
                try:
                    Credentials(auth_key, cid, login_for).download()
                    st.session_state["auth_key"] = auth_key
                    st.session_state["cid"] = cid
                    st.experimental_rerun()
                except ValueError:
                    msg.error("Please check your auth key or chosen course.")


try:
    user = LoggedUser()
    profile = user.profile
    api = PWApi(st.session_state["auth_key"], st.session_state["cid"])

    # Show profile image
    img = profile.get("img")
    if img is not None:
        if img["source"] == "oauth":
            url = f"https://learn.pwskills.com/_next/image?url={img['link']}&w=96&q=75"
        elif img["source"] == "bucket":
            url = f"https://learn.pwskills.com/_next/image?url=https%3A%2F%2Fcdn.pwskills.com%2Fuser%2Fprofile_pictures%2F{img['link']}&w=96&q=75"
        else:
            url = "https://learn.pwskills.com/_next/image?url=https%3A%2F%2Fcdn.pwskills.com%2Fuser%2Fprofile_pictures%2F63a1f5889d90b2b9e65c8a73.jpeg&w=96&q=75"

        st.image(url)

    st.title(f"Hi! {profile['firstName']} {profile['lastName']}")
    st.subheader(f":red[E-mail:] {profile['email']}")

    # User social media
    user_social = profile.get("social")
    if user_social is not None:
        for media in user_social:
            st.subheader(f":red[{media.title()}:] {user_social[media]}")

    # Update Assignment Solutions Link
    update_solution_link = st.container()

    # Fetches new quiz or assignment data and store it
    fetch_new_quiz_assignment = st.container()

    # Download quiz or assignment data of logged in course
    save_quiz_assignment_json = st.container()

    # Logout button
    if st.button(
        label="**Logout**",
        use_container_width=True,
        on_click=Credentials.delete,
    ):
        st.experimental_rerun()

except FileNotFoundError:
    login_form()
    st.stop()

except KeyError:
    Credentials.delete()
    st.experimental_rerun()


with update_solution_link:
    l, r = st.columns([0.06, 0.6])
    force = l.checkbox(
        label="Force",
        help="Force to update the stored links.",
    )
    r.button(
        label="Update Assignment Solutions Link",
        on_click=api.update_solution_links,
        kwargs={"force_update": force},
        use_container_width=True,
    )


with fetch_new_quiz_assignment:
    l, r = st.columns(2)
    quiz_dl = l.button("Fetch Course Quizzes", use_container_width=True)
    assign_dl = r.button("Fetch Course Assignments", use_container_width=True)
    type_ = "quiz" if quiz_dl else "assignment" if assign_dl else None

    if type_ is not None:
        try:
            with st.spinner(f"Fetching {type_}(s)..."):
                msg.info("**Do not refresh the page.**")
                api.export_data(st.session_state["cid"], type_, 0.5)
            msg.success(f"You fetches all {type_!r} data of your course")
        except ReadTimeout:
            msg.error(f"Re-click the {type_!r} button to restart the fetching process.")


with save_quiz_assignment_json:
    quiz_fp = api.generate_fp("quiz")
    assignment_fp = api.generate_fp("assignment")

    l, r = st.columns(2)
    l.download_button(
        label="Save Quiz Data",
        data=(dumps(load(open(quiz_fp)), indent=2) if quiz_fp.exists() else "[]"),
        file_name=quiz_fp.name,
        mime="json",
        use_container_width=True,
    )
    r.download_button(
        label="Save Assignment Data",
        data=(
            dumps(load(open(assignment_fp)), indent=2)
            if assignment_fp.exists()
            else "[]"
        ),
        file_name=assignment_fp.name,
        mime="json",
        use_container_width=True,
    )
