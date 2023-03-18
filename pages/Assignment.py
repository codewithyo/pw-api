from json import load
from pathlib import Path
from webbrowser import open_new_tab

import streamlit as st

from utils import Assignment, User


def selected_assignment() -> Path:
    all_files = User.get_all_files('data', 'assignment')

    options = sorted([i.stem for i in all_files])
    sl = str(st.selectbox('Select Assignment', options))

    parent = all_files[options.index(sl)].parent
    return parent / (sl+'.json')


# Create Assignment parser
a = Assignment(load(open(selected_assignment()))['data'])

# Display components in page
'---'
st.metric(a.id, a.title)
f'##### :red[Date :] {a.date_created:%d %B, %Y}'
f'##### :red[Marks :] {a.marks}'


if st.button('Open PDF'):
    open_new_tab(a.url)

if st.button('Download PDF'):
    open_new_tab(a.download_url)

if st.button('Get Solution'):
    d = a.date_created
    prefix = 'https://github.com/arv-anshul/pw-impact-batch/blob/main/'
    open_new_tab(f'{prefix}{d:%B}/{d:%d %h}/{d:%d %h} - Answer.ipynb')
