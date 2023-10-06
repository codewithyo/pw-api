from json import loads

import streamlit as st
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from requests import get

from src import LiveCourse, courses_dict
from src.core.logger import get_logger

plt.style.use("ggplot")

logger = get_logger(__name__)

# Set page config
st.set_page_config("Preview Courses", "🗂️", "wide")


with st.sidebar:
    cid = str(
        st.selectbox(
            label="Select Course",
            options=courses_dict.keys(),
            format_func=lambda x: courses_dict[x],
        )
    )
    course_name = courses_dict[cid]
    radio = st.radio(
        label="Select Page",
        options=["Overview", "Topics Resource", "Extra Resource"],
        label_visibility="hidden",
    )


# Get response from api
@st.cache_resource
def get_live_course_dict(course_name: str, course_id: str):
    """Return the required live course data as Python dict."""
    url = "https://learn.pwskills.com/course/{}/{}".format(
        course_name.replace(" ", "-"), course_id
    )
    r = get(url)
    logger.info(f"[{r.status_code}]:{r.url}")

    soup = BeautifulSoup(r.text, "html.parser")
    script = soup.find("script", {"id": "__NEXT_DATA__"})

    if script is not None:
        data = script.text
    else:
        raise TypeError("Required script tag is not available.")

    return loads(data)["props"]["pageProps"]


lc_dict = get_live_course_dict(course_name, cid)
lc = LiveCourse(**lc_dict)
df = lc.merged_df(cid)


def display_curr_details(title: str):
    """Display the desired section details."""
    for i in df["sectionsTitle"].unique():
        if title != i:
            continue

        new_df = df.query("sectionsTitle==@i")
        with st.expander(f"🗂️ {i}", True):
            for j in new_df.query('type=="video"')["lessonsTitle"].values:
                st.write(f" - {j}")

            qz_ = new_df.query('type=="quiz"')["lessonsTitle"].values
            as_ = new_df.query('type=="assignment"')["lessonsTitle"].values

            if len(qz_) > 0:
                st.write("---")
                st.write("#### Quizzes:")
                for q_title in qz_:
                    st.write(f"- {q_title}")

            if len(as_) > 0:
                st.write("---")
                st.write("#### Assignments:")
                for asg_title in as_:
                    st.write(f"- {asg_title}")


if radio == "Overview":
    st.title(f"Overview of :orange[{course_name}] course")

    try:
        total_quiz_ques = df["totalQuestionsInQuiz"].sum()
        total_asg_points = df["totalPointsInAssignment"].sum()
        total_video_duration = round(df["duration"].sum() / 3600)
    except KeyError:
        total_quiz_ques = 0
        total_asg_points = 0
        total_video_duration = "N/A"

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("No. of questions in Quiz", int(total_quiz_ques))
    col2.metric("Total Assignments points", int(total_asg_points))
    col3.metric("Duration of videos", f"{total_video_duration} hours")

    # Course resources countplot
    fig, ax = plt.subplots()
    df["type"].value_counts().plot(
        kind="barh",
        ax=ax,
        title="Distribution of course resources",
        ylabel="Resources",
        xlabel="Count",
        figsize=(10, 3),
        grid=False,
    )
    st.write("---")
    st.pyplot(fig)

elif radio == "Topics Resource":
    st.title(f"Resources of :orange[{course_name}] course")

    title = st.selectbox(
        label="Select Course Section",
        options=df["sectionsTitle"].unique()[::-1],
    )
    display_curr_details(str(title))

elif radio == "Extra Resource":
    st.title(f"Extra Resources in :orange[{course_name}] course")

    new_df = df.query('type=="sectionResource"')
    for i in new_df["sectionsTitle"].unique()[::-1]:
        sl_df = new_df.query("sectionsTitle==@i")

        with st.expander(f"🗂️ {i}"):
            for title in sl_df["lessonsTitle"].values:
                st.write(f"- {title}")
