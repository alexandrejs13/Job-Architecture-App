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

COL_FAMILY     = "Job Family"
COL_SUBFAMILY  = "Sub Job Family"
COL_PROFILE    = "Job Profile"
COL_CAREER_PATH = "Career Path"
COL_BAND       = "Career Band Short"
COL_GRADE      = "Global Grade"
COL_LEVEL      = "Career Level"


# ==========================================================
# SIG COLORS
# ==========================================================
SIG_PALETTE = [
    "#145EFC",  # Sky
    "#DCA0FF",  # Spark
    "#00493B",  # Forest 3
    "#167665",  # Forest 2
    "#4FA593",  # Forest 1
    "#F2EFEB",  # Sand 1
    "#E5DFD9",  # Sand 2
    "#000000",  # Black
]


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
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 18px;
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
    color: #000000;
}

.sig-card-value {
    font-size: 24px;
    font-weight: 800;
    color: #145EFC;
}

.block-space {
    margin-top: 36px;
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
        "Families":       df[COL_FAMILY].nunique(),
        "Subfamilies":    df[COL_SUBFAMILY].nunique(),
        "Job Profiles":   df[COL_PROFILE].nunique(),
        "Global Grades":  df[COL_GRADE].nunique(),
        "Career Paths":   df[COL_CAREER_PATH].nunique(),
    }

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
    # DONUT — Subfamilies per Family
    # ==========================================================
    st.markdown("<div class='block-space'></div>", unsafe_allow_html=True)
    st.markdown("## Subfamilies per Family")

    donut_df = (
        df.groupby(COL_FAMILY)[COL_SUBFAMILY]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    donut_df["Color"] = [SIG_PALETTE[i % len(SIG_PALETTE)] for i in range(len(donut_df))]

    colA, colB = st.columns([1, 1])

    with colA:
        chart = (
            alt.Chart(donut_df)
            .mark_arc(innerRadius=60, outerRadius=120)
            .encode(
                theta="Count:Q",
                color=alt.Color("Color:N", scale=None, legend=None),
                tooltip=[COL_FAMILY, "Count"],
            )
        )
        st.altair_chart(chart, use_container_width=True)

    with colB:
        for _, row in donut_df.iterrows():
            st.markdown(
                f"""
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
                    <div style="width:14px; height:14px; background:{row['Color']}; border-radius:50%;"></div>
                    <div style="font-size:16px; font-weight:600;">{row[COL_FAMILY]}</div>
                    <div style="margin-left:auto; background:{row['Color']}; color:white;
                                padding:2px 12px; border-radius:12px; font-weight:700;">
                        {row['Count']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


    # ==========================================================
    # BAR CHART — Profiles per Subfamily (Total)
    # ==========================================================
    st.markdown("<div class='block-space'></div>", unsafe_allow_html=True)
    st.markdown("## Profiles per Subfamily (Total)")

    bar_df = (
        df.groupby(COL_SUBFAMILY)[COL_PROFILE]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    bar_chart = (
        alt.Chart(bar_df)
        .mark_bar(size=28, cornerRadius=4)
        .encode(
            x=alt.X("Count:Q", title="Count"),
            y=alt.Y(COL_SUBFAMILY + ":N", sort="-x"),
            color=alt.value("#145EFC"),
            tooltip=[COL_SUBFAMILY, "Count"],
        )
        .properties(height=650)
    )

    st.altair_chart(bar_chart, use_container_width=True)



# ==========================================================
# TAB 2 — FAMILY MICRO-ANALYSIS
# ==========================================================
with tab2:

    st.markdown("## Family Micro-Analysis")

    families = sorted(df[COL_FAMILY].unique())
    family_sel = st.selectbox("Select Family:", families)

    fam_df = df[df[COL_FAMILY] == family_sel]

    metrics = {
        "Subfamilies":  fam_df[COL_SUBFAMILY].nunique(),
        "Job Profiles": fam_df[COL_PROFILE].nunique(),
        "Global Grades": fam_df[COL_GRADE].nunique(),
        "Career Paths": fam_df[COL_CAREER_PATH].nunique(),
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


    # Subfamily bar chart for selected family
    st.markdown("<div class='block-space'></div>", unsafe_allow_html=True)
    st.markdown("## Profiles per Subfamily")

    fam_sub = (
        fam_df.groupby(COL_SUBFAMILY)[COL_PROFILE]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    fam_chart = (
        alt.Chart(fam_sub)
        .mark_bar(size=28, cornerRadius=4)
        .encode(
            x=alt.X("Count:Q", title="Count"),
            y=alt.Y(COL_SUBFAMILY + ":N", sort="-x"),
            color=alt.value("#145EFC"),
            tooltip=[COL_SUBFAMILY, "Count"],
        )
        .properties(height=450)
    )

    st.altair_chart(fam_chart, use_container_width=True)


    st.markdown("<div class='block-space'></div>", unsafe_allow_html=True)
    st.markdown("## Full Job Profile Listing")

    st.dataframe(
        fam_df[[COL_SUBFAMILY, COL_PROFILE, COL_CAREER_PATH, COL_BAND, COL_LEVEL, COL_GRADE]],
        use_container_width=True
    )
