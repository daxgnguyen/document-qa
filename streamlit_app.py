import streamlist as st
st.title('IST 488 Labs')
Lab1 = st.Page('labs/lab1.py', title = 'Lab 1', icon = '📝')
Lab2 = st.Page('labs/lab2.py', title = 'Lab 2', icon = '📝')
pg = st.navigation([Lab1, Lab2])
st.st_page_config(page_title = 'IST 488 Lasbs'
                  initial_sidebar_state = 'expanded')
pg.run()