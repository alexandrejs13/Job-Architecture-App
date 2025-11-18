import streamlit as st
import pandas as pd
import altair as alt
import base64, os

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(page_title="Dashboard", layout="wide")

# ==========================================================
# SAFE FONT LOADER (SIG Flow)
# ==========================================================
def load_font_base64(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

font_regular = load_font_base64("assets/fonts/PP-SIG-Flow-Regular.ttf")
font_semibold = load_font_base64("assets/fonts/PP-SIG-Flow-Semibold.ttf")

css_fonts = ""
if font_regular:
    css_fonts += f"""
    @font-face {{
        font-family: 'SIGFlow';
        src: url(data:font/ttf;base64,{font_regular}) format('truetype');
        font-weight: 400;
    }}"""
if font_semibold:
    css_fonts += f"""
    @font-face {{
        font-family: 'SIGFlow';
        src: url(data:font/ttf;base64,{font_semibold}) format('truetype');
        font-weight: 600;
    }}"""

# ==========================================================
# GLOBAL CSS — SIG COLORS (PANTONE)
# ==========================================================
st.markdown(f"""
<style>

{css_fonts}

* {{
    font-family: 'SIGFlow', sans-serif !important;
}}

section.main > div {{
    max-width: 1250px;
    margin-left: auto;
    margin-right: auto;
}}

h2 {{
    font-weight: 600;
}}

.kpi-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
    gap: 20px;
    margin: 25px 0;
}}

.kpi {{
    background: #ffffff;
    border-radius: 16px;
    border: 1px solid #e2e2e2;
    padding: 16px 22px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.06);
}}

.kpi-title {{
    color: #73706d;
    font-size: 15px;
    font-weight: 600;
}}

.kpi-value {{
    font-size: 34px;
    font-weight: 600;
    margin-top: 8px;
    color: #145efc; /* SIG Sky */
}}

.chart-card {{
    background: #ffffff;
    border-radius: 18px;
    padding: 22px 28px;
    box-shadow: 0 3px 14px rgba(0,0,0,0.05);
    border: 1px solid #e3e0da;
    margin-bottom: 26px;
}}

.legend-item {{
    display:flex;
    align-items:center;
    gap:10px;
    margin-bottom:8px;
}}

.legend-dot {{
    width:12px;
    height:12px;
    border-radius:50%;
}}

.legend-badge {{
    margin-left:auto;
    background:#145EFC;
    color:white;
    padding:2px 12px;
    border-radius:12px;
    font-weight:600;
}}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# HEADER SIG (Mantido padrão)
# ==========================================================
def load_icon_png(path):
    if not os.path.exists(path): return ""
    with open(path,"rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

icon_path = "assets/icons/data_2_perfromance.png"
icon_b64 = load_icon_png(icon_path)

st.markdown(f"""
<div style="display:flex; align-items:center; gap:18px; margin-top:12px;">
    <img src="data:image/png;base64,{icon_b64}" style="width:56px; height:56px;">
    <h1 style="font-size:36px; font-weight:600; margin:0; padding:0;">
        Dashboard
    </h1>
</div>
<hr style="margin-top:14px; margin-bottom:26px;">
""", unsafe_allow_html=True)

# ==========================================================
# LOAD DATA
# ==========================================================
@st.cache_data
def load_data():
    return pd.read_excel("data/Job Profile.xlsx")

df = load_data()

COL_FAMILY = "Job Family"
COL_SUBFAMILY = "Sub Job Family"
COL_PROFILE = "Job Profile"
COL_CAREER_PATH = "Career Path"
COL_GRADE = "Global Grade"

# ==========================================================
# TABS
# ==========================================================
tab1, tab2 = st.tabs(["📊 Overview", "🔍 Family & Subfamily Explorer"])

# ==========================================================
# TAB 1 — EXECUTIVE OVERVIEW
# ==========================================================
with tab1:

    st.markdown("## Executive Overview")

    # KPIs
    kpis = {
        "Job Families": df[COL_FAMILY].nunique(),
        "Subfamilies": df[COL_SUBFAMILY].nunique(),
        "Job Profiles": df[COL_PROFILE].nunique(),
        "Career Paths": df[COL_CAREER_PATH].nunique(),
        "Global Grades": df[COL_GRADE].nunique(),
    }

    st.markdown("<div class='kpi-grid'>", unsafe_allow_html=True)
    for title, value in kpis.items():
        st.markdown(
            f"""
            <div class='kpi'>
                <div class='kpi-title'>{title}</div>
                <div class='kpi-value'>{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)


    # -------------------------------------------
    # Subfamilies per Family — DONUT
    # -------------------------------------------
    st.markdown("### Subfamilies per Family")
    subf = (
        df.groupby(COL_FAMILY)[COL_SUBFAMILY]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    SIG_COLORS = [
        "#145EFC", "#dca0ff", "#167665", "#f5f073",
        "#73706d", "#e5dfd9", "#4fa593", "#a0b9b5"
    ]
    subf["Color"] = [SIG_COLORS[i % len(SIG_COLORS)] for i in range(len(subf))]

    donut = (
        alt.Chart(subf)
        .mark_arc(innerRadius=70)
        .encode(
            theta="Count",
            color=alt.Color("Color:N", scale=None),
            tooltip=[COL_FAMILY, "Count"]
        )
    )

    c1, c2 = st.columns([1.2,1])
    with c1:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.altair_chart(donut, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        for _, row in subf.iterrows():
            st.markdown(
                f"""
                <div class='legend-item'>
                    <div class='legend-dot' style='background:{row["Color"]};'></div>
                    <div style="font-weight:600;">{row[COL_FAMILY]}</div>
                    <div class='legend-badge'>{row["Count"]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------------------------
    # Profiles per Subfamily — Bar Chart
    # -------------------------------------------
    st.markdown("### Profiles per Subfamily")

    bars_df = (
        df.groupby(COL_SUBFAMILY)[COL_PROFILE]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    bars = (
        alt.Chart(bars_df)
        .mark_bar(size=32)
        .encode(
            x="Count:Q",
            y=alt.Y(f"{COL_SUBFAMILY}:N", sort='-x'),
            color=alt.value("#145EFC")
        )
        .properties(height=36 * len(bars_df))
    )

    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.altair_chart(bars, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================================
# TAB 2 — FAMILY & SUBFAMILY EXPLORER
# ==========================================================
with tab2:

    st.markdown("## Family & Subfamily Explorer")

    families = sorted(df[COL_FAMILY].unique())
    selected_family = st.selectbox("Select a Family:", families)

    subf = sorted(df[df[COL_FAMILY] == selected_family][COL_SUBFAMILY].unique())
    selected_subfamily = st.selectbox("Select a Subfamily:", subf)

    filtered = df[
        (df[COL_FAMILY] == selected_family) &
        (df[COL_SUBFAMILY] == selected_subfamily)
    ][[COL_PROFILE, COL_CAREER_PATH, COL_GRADE]]

    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.dataframe(filtered, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
