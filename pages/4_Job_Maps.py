
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Job Maps", page_icon="📌", layout="wide")

css = Path("assets/css/theme.css").read_text()
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


with st.sidebar:
    st.logo("assets/icons/SIG_Logo_RGB_Black.svg", size="medium")


st.markdown(f"""
<h1 class='page-title'>
<img src='./assets/icons/globe_trade.png' width='64' style='vertical-align:middle;margin-right:10px;'>
Job Maps
</h1>
""", unsafe_allow_html=True)
