import streamlit as st

# LOGO sempre na sidebar
with st.sidebar:
    st.image("assets/icons/SIG_Logo_RGB_Black.png", width=140)
    st.write("")

# TÍTULO COM PNG NATIVO
st.markdown(f"""
<div style='display:flex; align-items:center; gap:16px;'>
    <img src="assets/icons/governance.png" width="48">
    <h1>Structure Level</h1>
</div>
""", unsafe_allow_html=True)

st.write("Conteúdo da página Structure Level.")
