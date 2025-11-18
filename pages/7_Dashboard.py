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
# HEADER SIG (PADRÃO)
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
# CSS — CARDS SLIM PADRÃO SIG
# ==========================================================
st.markdown("""
<style>

section.main > div {
    max-width: 1180px;
    padding-left: 10px;
    padding-right: 10px;
}

.sig-card-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
}

.sig-card {
    background: #F2EFEB;
    padding: 12px 16px;
    border-radius: 14px;
    border: 1px solid #E5E0D8;
    height: 88px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.sig-card-title {
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 6px;
}

.sig-card-value {
    font-size: 24px;
    font-weight: 800;
    color: #145EFC;
}

.block-space {
    margin-top: 32px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# ABAS
# ==========================================================
tab1, tab2 = st.tabs(["Overview", "Family Micro-Analysis"])



# ==========================================================
# 1) TAB — OVERVIEW
# ==========================================================
with tab1:

    st.markdown("## Overview")

    # Basic KPIs
    kpis = {
        "Families": df[COL_FAMILY].nunique(),
        "Subfamilies": df[COL_SUBFAMILY].nunique(),
        "Job Profiles": df[COL_PROFILE].nunique(),
        "Career Paths": df[COL_CAREER_PATH].nunique(),
        "Career Bands": df[COL_BAND].nunique(),
        "Global Grades": df[COL_GRADE].nunique(),
        "Avg Profiles / Family": round(df[COL_PROFILE].nunique() / df[COL_FAMILY].nunique(), 1),
        "Avg Profiles / Subfamily": round(df[COL_PROFILE].nunique() / df[COL_SUBFAMILY].nunique(), 1),
    }

    # ---- CARDS ----
    st.markdown("<div class='sig-card-grid'>", unsafe_allow_html=True)
    for title, value in kpis.items():
        st.markdown(
            f"""
            <div class='sig-card'>
                <div class='sig-card-title'>{title}</div>
                <div class='sig-card-value'>{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)



    # ==========================================================
    # GRAPH 1 — Subfamilies per Family
    # ==========================================================
    st.markdown("<div class='block-space'></div>", unsafe_allow_html=True)
    st.markdown("## Subfamilies per Family")

    subfamily_count = (
        df.groupby(COL_FAMILY)[COL_SUBFAMILY]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    colA, colB = st.columns([1,1])

    with colA:
        chart1 = alt.Chart(subfamily_count).mark_arc(innerRadius=65, outerRadius=120).encode(
            theta="Count:Q",
            color=alt.Color(COL_FAMILY, legend=None),
            tooltip=[COL_FAMILY, "Count"]
        )
        st.altair_chart(chart1, use_container_width=False)

    with colB:
        for _, row in subfamily_count.iterrows():
            st.markdown(
                f"""
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
                    <div style="width:12px; height:12px; background:#145EFC; border-radius:50%;"></div>
                    <div style="font-weight:600; font-size:16px;">{row[COL_FAMILY]}</div>
                    <div style="margin-left:auto; background:#145EFC; color:white; padding:2px 12px; border-radius:12px; font-weight:700;">
                        {row['Count']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )



    # ==========================================================
    # GRAPH 2 — Profiles per Subfamily
    # ==========================================================
    st.markdown("<div class='block-space'></div>", unsafe_allow_html=True)
    st.markdown("## Profiles per Subfamily (Total)")

    profiles_sub = (
        df.groupby(COL_SUBFAMILY)[COL_PROFILE]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    col1, col2 = st.columns([1,1])

    with col1:
        chart2 = alt.Chart(profiles_sub).mark_arc(innerRadius=65, outerRadius=120).encode(
            theta="Count:Q",
            color=alt.Color(COL_SUBFAMILY, legend=None),
            tooltip=[COL_SUBFAMILY, "Count"]
        )
        st.altair_chart(chart2, use_container_width=False)

    with col2:
        for _, row in profiles_sub.iterrows():
            st.markdown(
                f"""
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
                    <div style="width:12px; height:12px; background:#145EFC; border-radius:50%;"></div>
                    <div style="font-weight:600; font-size:16px;">{row[COL_SUBFAMILY]}</div>
                    <div style="margin-left:auto; background:#145EFC; color:white; padding:2px 12px; border-radius:12px; font-weight:700;">
                        {row['Count']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )



# ==========================================================
# 2) TAB — FAMILY MICRO-ANALYSIS
# ==========================================================
with tab2:

    st.markdown("## Family Micro-Analysis")

    families = sorted(df[COL_FAMILY].unique())
    family_sel = st.selectbox("Select Family:", families)

    fam_df = df[df[COL_FAMILY] == family_sel]

    metrics = {
        "Subfamilies": fam_df[COL_SUBFAMILY].nunique(),
        "Job Profiles": fam_df[COL_PROFILE].nunique(),
        "Career Paths": fam_df[COL_CAREER_PATH].nunique(),
        "Career Bands": fam_df[COL_BAND].nunique(),
        "Global Grades": fam_df[COL_GRADE].nunique(),
        "Career Levels": fam_df[COL_LEVEL].nunique(),
    }

    st.markdown("<div class='sig-card-grid'>", unsafe_allow_html=True)
    for title, value in metrics.items():
        st.markdown(
            f"""
            <div class='sig-card'>
                <div class='sig-card-title'>{title}</div>
                <div class='sig-card-value'>{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)


    # GRAPH — Profiles per Subfamily (inside family)
    st.markdown("<div class='block-space'></div>", unsafe_allow_html=True)
    st.markdown("## Profiles per Subfamily")

    subfamily_local = (
        fam_df.groupby(COL_SUBFAMILY)[COL_PROFILE]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    colx, coly = st.columns([1,1])

    with colx:
        chart_local = alt.Chart(subfamily_local).mark_arc(innerRadius=65, outerRadius=120).encode(
            theta="Count:Q",
            color=alt.Color(COL_SUBFAMILY, legend=None),
            tooltip=[COL_SUBFAMILY, "Count"]
        )
        st.altair_chart(chart_local, use_container_width=False)

    with coly:
        for _, row in subfamily_local.iterrows():
            st.markdown(
                f"""
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
                    <div style="width:12px; height:12px; background:#167665; border-radius:50%;"></div>
                    <div style="font-weight:600; font-size:16px;">{row[COL_SUBFAMILY]}</div>
                    <div style="margin-left:auto; background:#167665; color:white; padding:2px 12px; border-radius:12px; font-weight:700;">
                        {row['Count']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


    # TABLE
    st.markdown("<div class='block-space'></div>", unsafe_allow_html=True)
    st.markdown("## Full Job Profile Listing")
    st.dataframe(
        fam_df[[COL_SUBFAMILY, COL_PROFILE, COL_CAREER_PATH, COL_BAND, COL_LEVEL, COL_GRADE]],
        use_container_width=True
    )
