import streamlit as st
import pandas as pd
import base64, os
import altair as alt

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(page_title="Dashboard", layout="wide")


# ==========================================================
# LOAD ICON INLINE
# ==========================================================
def load_icon_png(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


icon_path = "assets/icons/data_2_perfromance.png"
icon_b64 = load_icon_png(icon_path)


# ==========================================================
# HEADER SIG
# ==========================================================
st.markdown(
    f"""
<div style="display:flex; align-items:center; gap:18px; margin-top:12px;">
    <img src="data:image/png;base64,{icon_b64}" style="width:56px; height:56px;">
    <h1 style="font-size:36px; font-weight:700; margin:0; padding:0;">
        Dashboard
    </h1>
</div>

<hr style="margin-top:14px; margin-bottom:26px;">
""",
    unsafe_allow_html=True,
)


# ==========================================================
# LOAD DATA
# ==========================================================
@st.cache_data
def load_job_profile():
    return pd.read_excel("data/Job Profile.xlsx")


df = load_job_profile()

COL_FAMILY = "Job Family"
COL_SUB = "Sub Job Family"
COL_PROFILE = "Job Profile"
COL_PATH = "Career Path"
COL_BAND = "Career Band Short"
COL_GRADE = "Global Grade"
COL_LEVEL = "Career Level"


# ==========================================================
# CSS — FULL SIG IDENTITY
# ==========================================================
st.markdown(
    """
<style>

section.main > div {
    max-width: 1180px;
    padding-left: 8px;
    padding-right: 8px;
}

/* --- Responsive SIG card grid --- */
.sig-card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
    gap: 16px;
}

.sig-card {
    background: #F2EFEB; /* SIG Sand1 */
    padding: 14px 18px;
    border-radius: 14px;
    border: 1px solid #E5E0D8;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.sig-card-title {
    font-size: 13px;
    font-weight: 600;
    color: #000000;
    margin-bottom: 4px;
}

.sig-card-value {
    font-size: 24px;
    font-weight: 800;
    color: #145EFC; /* SIG Sky */
}

/* Legend counters */
.sig-legend-item {
    display:flex;
    align-items:center;
    gap:10px;
    margin-bottom:8px;
}

.sig-legend-dot {
    width:14px;
    height:14px;
    border-radius:50%;
}

.sig-legend-badge {
    margin-left:auto;
    background:#145EFC;
    color:white;
    padding:2px 12px;
    border-radius:14px;
    font-weight:700;
    font-size:14px;
}

.block-space { margin-top: 36px; }

</style>
""",
    unsafe_allow_html=True,
)


# ==========================================================
# TABS
# ==========================================================
tab1, tab2 = st.tabs(["Overview", "Family Micro-Analysis"])


# ==========================================================
# TAB 1 — OVERVIEW
# ==========================================================
with tab1:
    st.markdown("## Overview")

    # KPIs
    kpis = {
        "Families": df[COL_FAMILY].nunique(),
        "Subfamilies": df[COL_SUB].nunique(),
        "Job Profiles": df[COL_PROFILE].nunique(),
        "Career Paths": df[COL_PATH].nunique(),
        "Global Grades": df[COL_GRADE].nunique(),
    }

    # Cards
    st.markdown("<div class='sig-card-grid'>", unsafe_allow_html=True)
    for title, value in kpis.items():
        st.markdown(
            f"""
        <div class='sig-card'>
            <div class='sig-card-title'>{title}</div>
            <div class='sig-card-value'>{value}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='block-space'></div>", unsafe_allow_html=True)

    # ==========================================================
    # GRAPH 1 — Pizza SIG (Subfamilies per Family)
    # ==========================================================
    st.markdown("## Subfamilies per Family")

    data1 = (
        df.groupby(COL_FAMILY)[COL_SUB]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    colA, colB = st.columns([1, 1])

    with colA:
        chart1 = (
            alt.Chart(data1)
            .mark_arc(innerRadius=65)
            .encode(
                theta="Count:Q",
                color=alt.Color(COL_FAMILY, legend=None),
                tooltip=[COL_FAMILY, "Count"],
            )
        )

        st.altair_chart(chart1, use_container_width=True)

    with colB:
        for _, row in data1.iterrows():
            st.markdown(
                f"""
            <div class="sig-legend-item">
                <div class="sig-legend-dot" style="background:#145EFC;"></div>
                <div style="font-weight:600; font-size:16px;">{row[COL_FAMILY]}</div>
                <div class="sig-legend-badge">{row['Count']}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    # ==========================================================
    # GRAPH 2 — Horizontal Bars (Profiles per Subfamily)
    # ==========================================================
    st.markdown("<div class='block-space'></div>", unsafe_allow_html=True)
    st.markdown("## Profiles per Subfamily (Total)")

    data2 = (
        df.groupby(COL_SUB)[COL_PROFILE]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    bars = (
        alt.Chart(data2)
        .mark_bar(color="#145EFC")
        .encode(
            x="Count:Q",
            y=alt.Y(COL_SUB, sort="-x"),
            tooltip=[COL_SUB, "Count"],
        )
        .properties(height=420)
    )

    st.altair_chart(bars, use_container_width=True)


# ==========================================================
# TAB 2 — FAMILY MICRO-ANALYSIS
# ==========================================================
with tab2:
    st.markdown("## Family Micro-Analysis")

    families = sorted(df[COL_FAMILY].unique())
    family_sel = st.selectbox("Select Family:", families)

    fam_df = df[df[COL_FAMILY] == family_sel]

    metrics = {
        "Subfamilies": fam_df[COL_SUB].nunique(),
        "Job Profiles": fam_df[COL_PROFILE].nunique(),
        "Career Paths": fam_df[COL_PATH].nunique(),
        "Global Grades": fam_df[COL_GRADE].nunique(),
        "Career Levels": fam_df[COL_LEVEL].nunique(),
    }

    # Cards responsive
    st.markdown("<div class='sig-card-grid'>", unsafe_allow_html=True)
    for title, value in metrics.items():
        st.markdown(
            f"""
        <div class='sig-card'>
            <div class='sig-card-title'>{title}</div>
            <div class='sig-card-value'>{value}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='block-space'></div>", unsafe_allow_html=True)

    # Graph — Profiles per Subfamily inside family (Bars)
    st.markdown("## Profiles per Subfamily")

    subdata = (
        fam_df.groupby(COL_SUB)[COL_PROFILE]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    bars_local = (
        alt.Chart(subdata)
        .mark_bar(color="#167865")
        .encode(
            x="Count:Q",
            y=alt.Y(COL_SUB, sort="-x"),
            tooltip=[COL_SUB, "Count"],
        )
        .properties(height=380)
    )

    st.altair_chart(bars_local, use_container_width=True)

    st.markdown("<div class='block-space'></div>", unsafe_allow_html=True)

    # Table
    st.markdown("## Full Job Profile Listing")
    st.dataframe(
        fam_df[
            [COL_SUB, COL_PROFILE, COL_PATH, COL_BAND, COL_LEVEL, COL_GRADE]
        ],
        use_container_width=True,
    )
