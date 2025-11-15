import streamlit as st

# O LOGO foi movido para o app.py
# Cabeçalho com ícone usando recursos nativos (st.columns e st.image)
col1, col2 = st.columns([0.1, 0.9])

with col1:
    st.image("assets/icons/governance.png", width=48)

with col2:
    st.header("Job Architecture")

st.write("Conteúdo da página Job Architecture.")
