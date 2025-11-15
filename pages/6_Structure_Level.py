import streamlit as st
from pathlib import Path
st.set_page_config(page_title='Structure Level',page_icon='📌',layout='wide')
css=Path('assets/css/theme.css').read_text()
st.markdown(f'<style>{css}</style>',unsafe_allow_html=True)
with st.sidebar:
    st.markdown('''<div style="display:flex;justify-content:center;margin:20px 0;"><img src="assets/icons/SIG_Logo_RGB_Black.svg" width="120"></div>''',unsafe_allow_html=True)
st.markdown('''<h1 class="page-title"><img src="assets/icons/process.png" width="48" style="vertical-align:middle;margin-right:12px;">Structure Level</h1>''',unsafe_allow_html=True)
