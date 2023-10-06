""" README page for the PW Skills Live Course analysis. """

import streamlit as st

from src.pw.utils import store_all_courses_data

# Page config
st.set_page_config("README.md", "🗒️", "wide", "expanded")

with st.sidebar:
    st.button(
        "Get New Courses",
        on_click=store_all_courses_data,
        use_container_width=True,
    )

# Read the markdown file to display.
with open("README.md", "r") as md:
    st.markdown(md.read())
