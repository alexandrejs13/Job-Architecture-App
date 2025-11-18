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
# HEADER
# ==========================================================
icon_path = "assets/icons/data_2_perfromance.png"
icon_b64 = load_icon_png(icon_path)

st.markdown(f"""
<div style="display:flex; align-items:center; gap:16px; margin-top:12px;">
    <img src="data:image/png;base64,{icon_b64}" style="width:56px; height:56px;">
    <h1 style="font-size:36px; font-weight:700; margin:0; padding:0;">Dashboard</h1>
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
COL_GRADE = "Global Grade"

# ==========================================================
# SIG COLOR PALETTE (ROTATING)
# ==========================================================
SIG_COLORS = [
    "#145EFC", "#DCA0FF", "#00493B", "#F5F073",
    "#167665", "#A0B905", "#BFBAA5", "#F2EFEB",
]

def rotating_color(i):
    return SIG_COLORS[i % len(SIG_COLORS)]

# ==========================================================
# CSS — CARDS RESPONSIVOS, SLIM SIG
# ==========================================================
st.markdown("""
<style>

section.main > div {
    max-width: 1180px;
    padding-left: 10px !important;
    padding-right: 10px !important;
}

/* GRID RESPONSIVO */
.sig-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
}

/* CARD */
.sig-card {
    background: #F2EFEB;
    padding: 12px 16px;
    border-radius: 14px;
    border: 1px solid #E5E0D8;
}

.sig-card-title {
    font-size: 13px;
    font-weight: 600;
    color: #000;
    margin-bottom: 4px;
}

.sig-card-value {
    font-size: 24px;
    font-weight: 800;
    color: #145EFC;
}

.legend-row {
    display:flex; 
    align-items:center; 
    gap:10px; 
    margin-bottom:6px;
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
# TABS
# ==========================================================
tab1, tab2 = st.tabs(["Overview", "Family Micro-Analysis"])

# ==========================================================
# 1) OVERVIEW
# ==========================================================
with tab1:

    st.markdown("## Overview")

    kpis = {
        "Families": df[COL_FAMILY].nunique(),
        "Subfamilies": df[COL_SUBFAMILY].nunique(),
        "Job Profiles": df[COL_PROFILE].nunique(),
        "Career Paths": df[COL_CAREER_PATH].nunique(),
        "Global Grades": df[COL_GRADE].nunique(),
    }

    st.markdown("<div class='sig-grid'>", unsafe_allow_html=True)
    for t, v in kpis.items():
        st.markdown(
            f"<div class='sig-card'><div class='sig-card-title'>{t}</div><div class='sig-card-value'>{v}</div></div>",
            unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # ======================================================
    # A) SUBFAMILIES PER FAMILY (DONUT)
    # ======================================================
    st.markdown("### Subfamilies per Family")

    subf = (
        df.groupby(COL_FAMILY)[COL_SUBFAMILY]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    # Color map
    subf["Color"] = [rotating_color(i) for i in range(len(subf))]

    colA, colB = st.columns([1,1])

    with colA:
        donut = (
            alt.Chart(subf)
            .mark_arc(innerRadius=70)
            .encode(
                theta="Count:Q",
                color=alt.Color("Color:N", scale=None),
                tooltip=[COL_FAMILY, "Count"],
            )
            .properties(height=360)
        )
        st.altair_chart(donut, use_container_width=True)

    with colB:
        for i, row in subf.iterrows():
            st.markdown(
                f"""
                <div class='legend-row'>
                    <div style="width:12px; height:12px; background:{row['Color']}; border-radius:50%;"></div>
                    <div style="font-weight:600; font-size:15px;">{row[COL_FAMILY]}</div>
                    <div class='legend-badge' style="background:{row['Color']};">{row['Count']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # ======================================================
    # B) PROFILES PER SUBFAMILY (BARRAS)
    # ======================================================
    st.markdown("### Profiles per Subfamily (Total)")

    subprofiles = (
        df.groupby(COL_SUBFAMILY)[COL_PROFILE]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )
    subprofiles["Color"] = [rotating_color(i) for i in range(len(subprofiles))]

    bar = (
        alt.Chart(subprofiles)
        .mark_bar(size=26)
        .encode(
            x=alt.X("Count:Q", title=""),
            y=alt.Y(f"{COL_SUBFAMILY}:N", sort="-x", title=""),
            color=alt.Color("Color:N", scale=None),
            tooltip=[COL_SUBFAMILY, "Count"],
        )
        .properties(height=550)
    )

    st.altair_chart(bar, use_container_width=True)


# ==========================================================
# 2) FAMILY MICRO-ANALYSIS
# ==========================================================
with tab2:

    st.markdown("## Family Micro-Analysis")

    families = sorted(df[COL_FAMILY].unique())
    fam = st.selectbox("Select Family", families)

    fam_df = df[df[COL_FAMILY] == fam]

    metrics = {
        "Subfamilies": fam_df[COL_SUBFAMILY].nunique(),
        "Job Profiles": fam_df[COL_PROFILE].nunique(),
        "Career Paths": fam_df[COL_CAREER_PATH].nunique(),
        "Global Grades": fam_df[COL_GRADE].nunique(),
    }

    st.markdown("<div class='sig-grid'>", unsafe_allow_html=True)
    for t, v in metrics.items():
        st.markdown(
            f"<div class='sig-card'><div class='sig-card-title'>{t}</div><div class='sig-card-value'>{v}</div></div>",
            unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # chart
    st.markdown("### Profiles per Subfamily")

    fam_sub = (
        fam_df.groupby(COL_SUBFAMILY)[COL_PROFILE]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )
    fam_sub["Color"] = [rotating_color(i) for i in range(len(fam_sub))]

    col1, col2 = st.columns([1,1])

    with col1:
        donut2 = (
            alt.Chart(fam_sub)
            .mark_arc(innerRadius=70)
            .encode(
                theta="Count:Q",
                color=alt.Color("Color:N", scale=None),
                tooltip=[COL_SUBFAMILY, "Count"],
            )
            .properties(height=360)
        )
        st.altair_chart(donut2, use_container_width=True)

    with col2:
        for _, row in fam_sub.iterrows():
            st.markdown(
                f"""
                <div class='legend-row'>
                    <div style="width:12px; height:12px; background:{row['Color']}; border-radius:50%;"></div>
                    <div style="font-weight:600; font-size:15px;">{row[COL_SUBFAMILY]}</div>
                    <div class='legend-badge' style="background:{row['Color']};">{row['Count']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("### Full Job Profile Listing")
    st.dataframe(
        fam_df[[COL_SUBFAMILY, COL_PROFILE, COL_CAREER_PATH, COL_GRADE]],
        use_container_width=True
    )
