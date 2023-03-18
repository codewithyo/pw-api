import re
from json import load
from pathlib import Path

import streamlit as st

from utils import Quiz, User

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
             font-family: 'Poppins' !important;
         }
         </style>""", unsafe_allow_html=True)


def selected_quiz(path: Path):
    all_files = User.get_all_files('data', 'quiz')

    options = [i.stem for i in all_files]
    sl = str(st.sidebar.selectbox('Select Quiz', options))

    parent = all_files[options.index(sl)].parent
    return Path.joinpath(parent, sl+'.json')


quiz = selected_quiz(Path('data/quiz'))

q = Quiz(load(open(quiz))['data'])


def write_question(questions: list[tuple]):
    res: list[str] = []
    for n, question in enumerate(questions, 1):
        sl = st.radio(re.sub(r'<.*?>', '', fr'{n}\. {question[0]}'),
                      ['']+[re.sub(r'<.*?>|&nbsp;', ' ', i) for i in question[1:]])
        res.append(str(sl))
    return res


st.error('For now evaluation of quizzes is not available.', icon='🚨')
st.metric(q.id, q.title)
st.write(f'##### **:red[Date :]** :green[{q.date_created:%d %h, %y}]')
st.write(f'##### :red[Marks :] :green[{q.marks}]')

'---'
r = write_question(q.questions())

'---'
'### You Selected'
st.write(r)
