import streamlit as st

# LOGO sempre na sidebar
with st.sidebar:
    st.image("assets/icons/SIG_Logo_RGB_Black.png", width=140)
    st.write("")

# TÍTULO COM PNG NATIVO
st.markdown(f"""
<div style='display:flex; align-items:center; gap:16px;'>
    <img src="assets/icons/data_2_perfromance.png" width="48">
    <h1>Dashboard</h1>
</div>
""", unsafe_allow_html=True)

st.write("Conteúdo da página Dashboard.")
