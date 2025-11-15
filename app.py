import streamlit as st
import os

st.set_page_config(
    page_title="SIG Job Architecture",
    layout="wide"
)

# Carrega o CSS correto
css_path = os.path.join("assets", "css", "theme.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Conteúdo padrão da Home
st.title("Home")
st.write("Bem-vindo.")
