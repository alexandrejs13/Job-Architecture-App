import streamlit as st

# Cabeçalho com ícone NATIVO
col1, col2 = st.columns([0.1, 0.9])
with col1:
    st.image("assets/icons/globe_trade.png", width=48)
with col2:
    st.header("Job Maps")

st.markdown("---")
st.write("Conteúdo da página Job Maps.")
