import streamlit as st
import os

st.set_page_config(page_title="SIG Job Architecture", layout="wide")

# Carrega CSS global
css_path = os.path.join("assets", "css", "theme.css")
with open(css_path, "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Redireciona automaticamente para a Home
st.switch_page("pages/1_Home.py")
