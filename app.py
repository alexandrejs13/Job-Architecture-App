import streamlit as st

st.set_page_config(page_title="Job Architecture App", layout="wide")

# ----- CENTRALIZED CARD LAYOUT -----
st.markdown("<div style='display:flex; justify-content:center; width:100%;'>", unsafe_allow_html=True)

with st.container():
    st.markdown(
        """
        <div style='
            max-width:900px;
            width:100%;
            margin-top:40px;
            background-color:#f2efeb;
            padding:30px;
            border-radius:20px;
            box-shadow:0 4px 12px rgba(0,0,0,0.08);
        '>
        """,
        unsafe_allow_html=True
    )

    st.image("assets/home/home_card.jpg", use_column_width=True)

    st.markdown("<h1 style='font-size:42px; margin-top:25px;'>Job Architecture</h1>", unsafe_allow_html=True)

    st.markdown(
        """
        <p style='font-size:20px; line-height:1.5; margin-top:10px;'>
        A unified database of generic job descriptions that serves as a global reference for classifying, harmonizing, and standardizing all roles across the company. Here you will find consistent titles, clear levels, and internationally aligned profiles. This is designed so managers only need to select the correct local job while the system handles the rest. This creates simplicity in daily operations, reduces uncertainty, and promotes a fully integrated organizational structure.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <a href="1_Job_Architecture" style='
            font-size:20px;
            color:#145efc;
            text-decoration:none;
            font-weight:600;
        '>Job Architecture →</a>
        """,
        unsafe_allow_html=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
