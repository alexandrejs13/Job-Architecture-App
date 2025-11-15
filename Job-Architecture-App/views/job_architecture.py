
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Job Architecture", page_icon="📌", layout="wide")

css = Path("assets/css/theme.css").read_text()
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


with st.sidebar:
    cols = st.columns([1,3,1])
    with cols[1]:
        st.logo("assets/icons/SIG_Logo_RGB_Black.svg", size="medium")

    def menu_item(icon, label, target):
        c1, c2 = st.columns([1,4])
        with c1: st.image(f"assets/icons/{icon}", width=28)
        with c2: st.page_link(target, label=label)

    menu_item("governance.png","Job Architecture","views/job_architecture.py")
    menu_item("people_employees.png","Job Families","views/job_families.py")
    menu_item("business_review_clipboard.png","Job Profile Description","views/job_profile_description.py")
    menu_item("globe_trade.png","Job Maps","views/job_maps.py")
    menu_item("checkmark_success.png","Job Match","views/job_match.py")
    menu_item("process.png","Structure Level","views/structure_level.py")
    menu_item("data_2_performance.png","Dashboard","views/dashboard.py")


st.markdown(f"""
<h1 class='page-title'>
<img src='./assets/icons/governance.png' width='64' style='vertical-align:middle;margin-right:10px;'>
Job Architecture
</h1>
""", unsafe_allow_html=True)
