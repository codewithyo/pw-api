""" README page for the PW Skills Live Course analysis. """

import streamlit as st

from src.pw.utils import get_all_courses_dict

# Page config
st.set_page_config('README.md', '🗒️', 'wide', 'expanded')

with st.sidebar:
    st.button('Get New Courses', on_click=get_all_courses_dict,
              use_container_width=True)

# Read the markdown file to display.
with open('README.md', 'r') as md:
    st.markdown(md.read())
