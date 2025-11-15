import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Job Architecture App", page_icon="🏠", layout="wide")

css = Path("assets/css/theme.css").read_text()
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

st.logo("assets/icons/SIG_Logo_RGB_Black.svg")

st.markdown("<h1 class='page-title'>🏠 Home</h1>", unsafe_allow_html=True)
