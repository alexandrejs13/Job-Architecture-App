import streamlit as st
import pandas as pd
import base64, os
import altair as alt

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(page_title="Dashboard", layout="wide")

# ==========================================================
# ICON LOADING
# ==========================================================
def load_icon_png(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# ==========================================================
# HEADER SIG
# ==========================================================
icon_path = "assets/icons/data_2_perfromance.png"
icon_b64 = load_icon_png(icon_path)

st.markdown(f"""
<div style="display:flex; align-items:center; gap:18px; margin-top:12px;">
    <img src="data:image/png;base64,{icon_b64}" style="width:56px; height:56px;">
    <h1 style="font-size:36px; font-weight:700; margin:0; padding:0;">
        Dashboard
    </h1>
</div>
<hr style="margin-top:14px; margin-bottom:26px;">
""", unsafe_allow_html=True)

# ==========================================================
# LOAD DATA
# ==========================================================
@st.cache_data
def load_job_profile():
    return pd.read_excel("data/Job Profile.xlsx")

df = load_job_profile()

COL_FAMILY = "Job Family"
COL_SUBFAMILY = "Sub Job Family"
COL_PROFILE = "Job Profile"
COL_CAREER_PATH = "Career Path"
COL_BAND = "Career Band Short"
COL_GRADE = "Global Grade"
COL_LEVEL = "Career Level"

# ==========================================================
# CSS — Cards horizontais pequenos
# ==========================================================
st.markdown("""
<style>

section.main > div {
    max-width: 1180px;
}

.kpi-row {
    display: flex;
    flex-wrap: wrap;
    gap: 18px;
    margin-bottom: 28px;
}

.kpi-box {
    background: #F2EFEB;
    border: 1px solid #E5E0D8;
    border-radius: 14px;
    padding: 12px 16px;
    width: 200px;
    height: 88px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.kpi-title {
    font-size: 14px;
    font-weight: 600;
    color: black;
}

.kpi-value {
    font-size: 24px;
    font-weight: 800;
    color: #145EFC;
}

/* legenda premium */
.legend-item {
    display:flex;
    align-items:center;
    gap:10px;
    margin-bottom:8px;
}

.legend-dot {
    width:12px;
    height:12px;
    border-radius:50%;
}

.legend-badge {
    margin-left:auto;
    background:#145EFC;
    color:white;
    padding:2px 12px;
    border-radius:12px;
    font-weight:700;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# ABAS
# ==========================================================
tab1, tab2 = st.tabs(["Overview", "Family Micro-Analysis"])

# ==========================================================
# TAB 1 — OVERVIEW
# ==========================================================
with tab1:

    st.markdown("## Overview")

    kpis = {
        "Families": df[COL_FAMILY].nunique(),
        "Subfamilies": df[COL_SUBFAMILY].nunique(),
        "Job Profiles": df[COL_PROFILE].nunique(),
        "Global Grades": df[COL_GRADE].nunique(),
        "Career Paths": df[COL_CAREER_PATH].nunique()
    }

    # CARDS
    st.markdown("<div class='kpi-row'>", unsafe_allow_html=True)
    for title, value in kpis.items():
        st.markdown(
            f"""
            <div class='kpi-box'>
                <div class='kpi-title'>{title}</div>
                <div class='kpi-value'>{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # ======================================================
    # DONUT — Subfamilies per Family
    # ======================================================
    st.markdown("## Subfamilies per Family")

    subf = (
        df.groupby(COL_FAMILY)[COL_SUBFAMILY]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    SIG_COLORS = [
        "#145EFC", "#dca0ff", "#167665", "#f5f073", "#73706d",
        "#bfba b5", "#e5dfd9", "#4fa593"
    ]

    subf["Color"] = [SIG_COLORS[i % len(SIG_COLORS)] for i in range(len(subf))]

    c1, c2 = st.columns([1.2, 1])

    with c1:
        donut = (
            alt.Chart(subf)
            .mark_arc(innerRadius=60)
            .encode(
                theta="Count",
                color=alt.Color("Color:N", scale=None),
                tooltip=[COL_FAMILY, "Count"]
            )
        )
        st.altair_chart(donut, use_container_width=True)

    with c2:
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

    # ======================================================
    # BARRAS — Profiles per Subfamily (TOTAL)
    # ======================================================
    st.markdown("## Profiles per Subfamily (Total)")

    profiles_sub = (
        df.groupby(COL_SUBFAMILY)[COL_PROFILE]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    bars = (
        alt.Chart(profiles_sub)
        .mark_bar(size=32)
        .encode(
            x="Count:Q",
            y=alt.Y(f"{COL_SUBFAMILY}:N", sort='-x'),
            color=alt.value("#145EFC"),
            tooltip=[COL_SUBFAMILY, "Count"]
        )
    ).properties(height=34 * len(profiles_sub))

    st.altair_chart(bars, use_container_width=True)


# ==========================================================
# TAB 2 — FAMILY MICRO-ANALYSIS
# ==========================================================
with tab2:

    st.markdown("## Family Micro-Analysis")

    families = sorted(df[COL_FAMILY].unique())
    selected = st.selectbox("Select Family:", families)

    fam_df = df[df[COL_FAMILY] == selected]

    metrics = {
        "Subfamilies": fam_df[COL_SUBFAMILY].nunique(),
        "Job Profiles": fam_df[COL_PROFILE].nunique(),
        "Global Grades": fam_df[COL_GRADE].nunique(),
        "Career Paths": fam_df[COL_CAREER_PATH].nunique(),
    }

    # CARDS
    st.markdown("<div class='kpi-row'>", unsafe_allow_html=True)
    for title, value in metrics.items():
        st.markdown(
            f"""
            <div class='kpi-box'>
                <div class='kpi-title'>{title}</div>
                <div class='kpi-value'>{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # DONUT por subfamily
    st.markdown("## Profiles per Subfamily (Inside Family)")

    sublocal = (
        fam_df.groupby(COL_SUBFAMILY)[COL_PROFILE]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )
    sublocal["Color"] = [SIG_COLORS[i % len(SIG_COLORS)] for i in range(len(sublocal))]

    s1, s2 = st.columns([1.2, 1])

    with s1:
        donut2 = (
            alt.Chart(sublocal)
            .mark_arc(innerRadius=60)
            .encode(
                theta="Count",
                color=alt.Color("Color:N", scale=None),
                tooltip=[COL_SUBFAMILY, "Count"]
            )
        )
        st.altair_chart(donut2, use_container_width=True)

    with s2:
        for _, row in sublocal.iterrows():
            st.markdown(
                f"""
                <div class='legend-item'>
                    <div class='legend-dot' style='background:{row["Color"]};'></div>
                    <div style="font-weight:600;">{row[COL_SUBFAMILY]}</div>
                    <div class='legend-badge'>{row["Count"]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # TABELA
    st.markdown("## Full Job Profile Listing")
    st.dataframe(
        fam_df[[COL_SUBFAMILY, COL_PROFILE, COL_CAREER_PATH, COL_BAND, COL_LEVEL, COL_GRADE]],
        use_container_width=True
    )
