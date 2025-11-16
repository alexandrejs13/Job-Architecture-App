import streamlit as st
st.set_page_config(page_title="Job Architecture", layout="wide")

def header(icon_path, title):
    st.markdown(f"""
        <div style="display:flex; align-items:center; gap:15px; margin-bottom:10px;">
            <img src="{icon_path}" style="width:48px; height:48px;">
            <h1 style="margin:0; padding:0; font-size:36px; font-weight:700;">
                {title}
            </h1>
        </div>
        <hr style="margin-top:5px;">
    """, unsafe_allow_html=True)

header("assets/icons/governance.png", "Job Architecture")

