import streamlit as st
from pathlib import Path
st.set_page_config(page_title="Dashboard", page_icon="📌", layout="wide")
css = Path("assets/css/theme.css").read_text()
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
st.markdown(f"<h1 class='page-title'><img src='assets/icons/data_2_performance.png' width='64' style='vertical-align:middle;margin-right:10px;'>Dashboard</h1>", unsafe_allow_html=True)
