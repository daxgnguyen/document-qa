import streamlit as st

st.set_page_config(page_title = 'IST 488 Labs',
                  initial_sidebar_state = 'expanded')

st.title('IST 488 Labs')
Lab1 = st.Page('labs/lab1.py', title = 'Lab 1', icon = '📝')
Lab2 = st.Page('labs/lab2.py', title = 'Lab 2', icon = '📝')
Lab3 = st.Page('labs/lab3.py', title = 'Lab 3', icon = '📝')
Lab4 = st.Page('labs/lab4.py', title = 'Lab 4', icon = '📝')
Lab5 = st.Page('labs/lab5.py', title = 'Lab 5', icon = '📝')
Lab6 = st.Page('labs/lab6.py', title = 'Lab 6', icon = '📝')
Lab8 = st.Page('labs/lab8.py', title = 'Lab 8', icon = '📝')
Lab9 = st.Page('labs/lab9.py', title = 'Lab 9', icon = '📝')
pg = st.navigation([Lab2, Lab1, Lab3, Lab4, Lab5, Lab6, Lab8, Lab9])

pg.run()