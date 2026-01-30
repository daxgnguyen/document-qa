import streamlit as st

st.set_page_config(page_title = 'IST 488 Labs',
                  initial_sidebar_state = 'expanded')

st.title('IST 488 Labs')
Lab1 = st.Page('labs/lab1.py', title = 'Lab 1', icon = '📝')
Lab2 = st.Page('labs/lab2.py', title = 'Lab 2', icon = '📝')
pg = st.navigation([Lab2, Lab1])

pg.run()