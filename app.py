import streamlit as st
import os

st.set_page_config(
    page_title="SIG Job Architecture",
    layout="wide",
)

# ============================
# CARREGAR CSS CORRETAMENTE
# ============================
css_path = os.path.join("assets", "css", "theme.css")

with open(css_path, "r") as f:
    css = f.read()

# A única forma aceita pelo Streamlit
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


# ============================
# CONTEÚDO DA HOME
# ============================

st.title("Home")
st.write("Bem-vindo.")
