import streamlit as st

from utils import User

st.title('Update the Authorization Key')
st.subheader(
    'You need to update the Authorization Key continuously because after 24 hours key get deprecated.')
st.markdown('##### `Note :` This is not compulsory to use this application.')
'---'

auth_key = st.text_input('Update Authorization Key',
                         placeholder=User.auth_key())

if st.button('Update Key', on_click=User.update_auth_key(auth_key)):
    st.balloons()
