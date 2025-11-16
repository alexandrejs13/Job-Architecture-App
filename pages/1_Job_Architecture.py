import streamlit as st

col1, col2 = st.columns([0.12, 0.88])

with col1:
    st.image("assets/icons/ICON_PATH", width=70)

with col2:
    st.markdown("<h1 style='margin-top:10px;'>PAGE_TITLE</h1>", unsafe_allow_html=True)

st.markdown("---")
st.write("Page content here.")
