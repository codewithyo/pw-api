import pandas as pd
import streamlit as st
from requests import get

from src import courses_dict
from src.core.logger import get_logger
from src.models.preview_course import PreviewCourse

logger = get_logger(__name__)

# Set page config
st.set_page_config("Preview Courses", "🗂️", "wide")

# --- --- Sidebar --- --- #
with st.sidebar:
    cid = str(
        st.selectbox(
            "Select Course", courses_dict.keys(), format_func=lambda x: courses_dict[x]
        )
    )
    radio = st.radio(
        "Select Page", ["Main", "Curriculum", "Projects"], label_visibility="hidden"
    )


@st.cache_resource
def get_preview_course_object(id: str) -> PreviewCourse:
    url = f"https://api.pwskills.com/v1/course/{id}?withAllCourseMetas=true&ignoreInActive=true"
    r = get(url)
    pc_dict = r.json()["data"]
    logger.info(f"[{r.status_code}]:{r.url}")

    pc = PreviewCourse(**pc_dict)
    return pc


def display_curr_details(
    df: pd.DataFrame,
    pat: str = "All",
) -> None:
    """Display the desired project."""
    pat = "" if str(pat) == "All" else pat

    for i in df["parentTitle"].unique():
        if pat.lower() in i.lower():
            new_df = df.query("parentTitle==@i")
            exp = st.expander(f"🗂️ {i}")

            for c in new_df["childTitle"].values:
                exp.write(f"  - {c}")


pc = get_preview_course_object(cid)

if radio == "Main":
    st.title(f"Details of :orange[{pc.title}]")

    course_price = round(pc.pricing.IN - (pc.pricing.IN * pc.pricing.discount / 100))
    inst_names = ", ".join([i.name for i in pc.instructorsDetails])
    cert_bench = pc.courseMetas[0].certificateBenchmark
    lang = pc.courseMetas[0].overview.language.title()
    duration = pc.courseMetas[0].duration

    st.write(f"###### :red[Price of Course:] :green[₹{course_price} /-]")
    st.write(f"###### :red[Name of instructors:] :green[{inst_names}]")
    st.write(f"###### :red[Certificate Benchmark:] :green[{cert_bench}%]")
    st.write(f"###### :red[Language of Course:] :green[{lang}]")
    st.write(f"###### :red[Course duration:] :green[{duration}]")

    with st.expander("**🔖 &nbsp; &nbsp; What you Learn from this course?**"):
        for i, j in enumerate(pc.courseMetas[0].overview.learn, 1):
            st.write(f"{i}. {j}")

    with st.expander("**🎁 &nbsp; &nbsp; Features of the Course.**"):
        for i, j in enumerate(pc.courseMetas[0].overview.features, 1):
            st.write(f"{i}. {j}")

    with st.expander("**👨 &nbsp; &nbsp; Instructors Details**"):
        for inst in pc.instructorsDetails:
            st.write(f"### 👨‍🏫 &nbsp; {inst.name}")
            st.write(f"{inst.description}")

            for name, url in inst.social.model_dump().items():
                if url:
                    st.write(f"###### 🔗 {name.capitalize()}: {url}")

            if not inst == pc.instructorsDetails[-1]:
                st.write("---")

elif radio == "Curriculum":
    df = pc.curriculum_df()

    st.title(f"Curriculum of :orange[{pc.title}]")
    l, r = st.columns([0.2, 0.8])
    l.write(f'#### :red[No. of Sections:] :green[{df["parentTitle"].nunique()}]')
    r.write(f'#### :red[No. of Lessons:] :green[{df["childTitle"].nunique()}]')
    st.write("---")

    choice = st.text_input("Enter Section Name", "All")
    display_curr_details(df, choice)

elif radio == "Projects":
    st.title(f"Projects of :orange[{pc.title}]")
    try:
        df = pc.projects_df()
    except ValueError as e:
        st.error(e, icon="🚨")
        st.stop()
    else:
        with st.expander(
            f"📌&nbsp; This course has **{df['parentId'].nunique()}** "
            "different **types of (parent) topics** for project which are:"
        ):
            for i in df["parentTitle"].unique():
                st.write(f"  - {i}")

        with st.expander(
            f"📍 There are **{df['childId'].nunique()}+** different "
            "**(child) topics** for project which are:"
        ):
            for i in df["parentTitle"].unique():
                st.write(f"  + {i}")
                for _, ii, j in df[["parentTitle", "childTitle"]].itertuples():
                    if ii == i:
                        st.write(f"    - {j}")

        st.write("---")

        choice = st.text_input("Enter Parent Project Name", "All")
        display_curr_details(df, choice)
