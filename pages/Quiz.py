import re

import streamlit as st

from utils import courses_dict
from utils.pw import Quiz
from utils.pw.parser import QuizQuestions

st_msg = st.empty()

# --- --- CSS --- --- #
st.write("""<style>
         [data-testid="stMetricValue"] div {
            font-weight: bold;
         }
         [data-testid="stMetricLabel"] p{
            color: grey;
            font-weight: 600;
         }
        .stRadio p {
            font-size: 20px;
            font-weight: 600;
        }
         label[data-baseweb="radio"]:first-child {
             display: none;
         }
         label[data-baseweb="radio"] div {
             font-family: monospace !important;
         }
         </style>""", unsafe_allow_html=True)

with st.sidebar:
    cid = str(st.selectbox('Select Course', courses_dict.keys(),
                           format_func=lambda x: courses_dict[x],
                           ))

    try:
        questions = Quiz.get_all_title_with_id(Quiz.generate_fp(cid))
    except FileNotFoundError:
        st_msg.error(f'Quiz for {courses_dict[cid]} course not available.')
        st.stop()

    quiz_id = str(st.selectbox(
        'Select Quiz', questions.keys(),
        format_func=lambda x: questions[x],
    ))

q_obj = Quiz.from_id(Quiz.generate_fp(cid), quiz_id)


def write_question(questions: QuizQuestions):
    res: list = []
    for n, question in enumerate(questions, 1):
        sl = st.radio(re.sub(r'<.*?>', '', fr'{n}\. {question[0]}'),
                      ['']+[re.sub(r'<.*?>|&nbsp;', '', i) for i in question[1]])
        res.append(sl)
    return res


# st.warning('Quiz evaluation is not available.')
st.metric(q_obj.id_, q_obj.title)
st.write(f'##### **:red[Date :]** :green[{q_obj.date_created:%d %h, %y}]')
st.write(f'##### **:red[Marks :]** :green[{q_obj.marks}]')

'---'
r = write_question(q_obj.questions())
'---'
f'### :red[{q_obj.title}] - :green[{q_obj.date_created:%d %b, %Y}]'
st.write(r)
