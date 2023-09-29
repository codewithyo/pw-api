import streamlit as st

from src import courses_dict
from src.pw import Assignment

st_msg = st.empty()

with st.sidebar:
    cid = str(
        st.selectbox(
            "Select Course", courses_dict.keys(), format_func=lambda x: courses_dict[x]
        )
    )

    try:
        assignments = Assignment.get_all_title_with_id(Assignment.generate_fp(cid))
    except FileNotFoundError:
        st_msg.error(
            f"Assignment for {courses_dict[cid]} course not available.",
            icon="🤖",
        )
        st.stop()

    assignment_id = str(
        st.selectbox(
            label="Select Assignment",
            options=assignments.keys(),
            format_func=lambda x: assignments[x],
        )
    )

as_obj = Assignment.from_id(Assignment.generate_fp(cid), assignment_id)

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
st.metric(courses_dict[cid], as_obj.title)
st.write(f"##### :red[Date :] {as_obj.date_created:%d %B, %Y}")
st.write(f"##### :red[Total Marks :] {as_obj.marks}")
st.write(f"## [Question Pdf]({as_obj.question_url})")

if as_obj.solution_url:
    st.write(f"## [Solution Notebook]({as_obj.solution_url})")
