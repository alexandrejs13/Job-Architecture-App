# ==========================================================
# HEADER — padrão SIG (NÃO ALTERAR)
# ==========================================================
import streamlit as st
import base64
import os

def load_icon_png(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

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
# IMPORTS
# ==========================================================
import pandas as pd
import altair as alt

# SIG Palette
SIG_SKY = "#145EFC"
SIG_SPARK = "#DCA0FF"
SIG_FOREST = "#167665"
SIG_MOSS = "#C8C84E"
SIG_BLACK = "#000000"
SIG_SAND1 = "#F2EFEB"
SIG_PALETTE = [SIG_SKY, SIG_SPARK, SIG_BLACK, SIG_FOREST, SIG_MOSS]

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
# GLOBAL PAGE CSS (mesma largura das outras páginas)
# ==========================================================
st.markdown("""
<style>
section.main > div { 
    max-width: 1180px !important;
    padding-left: 12px;
    padding-right: 12px;
}

/* SIG Slim Cards */
.sig-card-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}
.sig-card {
    background: #F2EFEB;
    padding: 14px 18px;
    border-radius: 14px;
    border: 1px solid #E6E0D8;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    height: 95px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.sig-card-title {
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 4px;
    color: #000;
}
.sig-card-value {
    font-size: 28px;
    font-weight: 800;
    color: #145EFC;
    margin-top: -2px;
}

/* Legend icons */
.sig-icon-wrapper {
    display: flex;
    align-items: center;
    gap: 10px;
}
</style>
""", unsafe_allow_html=True)


# ==========================================================
# ABAS
# ==========================================================
tab1, tab2 = st.tabs(["Overview", "Family Micro-Analysis"])



# ==========================================================
# TAB 1 — OVERVIEW (com rico detalhamento)
# ==========================================================
with tab1:

    st.markdown("## Overview")

    # Basic indicators
    total_families = df[COL_FAMILY].nunique()
    total_subfamilies = df[COL_SUBFAMILY].nunique()
    total_profiles = df[COL_PROFILE].nunique()
    total_paths = df[COL_CAREER_PATH].nunique()
    total_bands = df[COL_BAND].nunique()
    total_grades = df[COL_GRADE].nunique()

    # Additional consolidated metrics
    avg_profiles_per_family = round(total_profiles / total_families, 1)
    avg_profiles_per_subfamily = round(total_profiles / total_subfamilies, 1)

    family_sizes = df.groupby(COL_FAMILY)[COL_PROFILE].nunique()
    largest_family = family_sizes.idxmax()
    largest_family_pct = round(family_sizes.max() / total_profiles * 100, 1)

    overview_cards = {
        "Total Families": total_families,
        "Total Subfamilies": total_subfamilies,
        "Total Job Profiles": total_profiles,
        "Total Career Paths": total_paths,
        "Total Career Bands": total_bands,
        "Total Global Grades": total_grades,
        "Avg Profiles per Family": avg_profiles_per_family,
        "Avg Profiles per Subfamily": avg_profiles_per_subfamily,
        f"Largest Family (% of portfolio)": f"{largest_family_pct}%"
    }

    st.markdown("<div class='sig-card-grid'>", unsafe_allow_html=True)
    for title, value in overview_cards.items():
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
# TAB 2 — FAMILY MICRO-ANALYSIS (refinado)
# ==========================================================
with tab2:

    st.markdown("## Family Micro-Analysis")

    families = sorted(df[COL_FAMILY].unique())
    family_selected = st.selectbox("Select a Job Family:", families)
    family_df = df[df[COL_FAMILY] == family_selected]

    # --------------------------------------------
    # CARDS (slim, equal to overview)
    # --------------------------------------------
    metrics = {
        "Subfamilies": family_df[COL_SUBFAMILY].nunique(),
        "Job Profiles": family_df[COL_PROFILE].nunique(),
        "Career Paths": family_df[COL_CAREER_PATH].nunique(),
        "Career Bands": family_df[COL_BAND].nunique(),
        "Global Grades": family_df[COL_GRADE].nunique(),
        "Career Levels": family_df[COL_LEVEL].nunique(),
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


    # --------------------------------------------
    # DONUT — Profiles by Subfamily
    # --------------------------------------------
    st.markdown("## Distribution of Job Profiles by Subfamily")

    sub_dist = (
        family_df.groupby(COL_SUBFAMILY)[COL_PROFILE]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    colA, colB = st.columns([1,1])

    with colA:
        donut = alt.Chart(sub_dist).mark_arc(
            innerRadius=70, outerRadius=130
        ).encode(
            theta="Count:Q",
            color=alt.Color(COL_SUBFAMILY, scale=alt.Scale(range=SIG_PALETTE), legend=None),
            tooltip=[COL_SUBFAMILY, "Count"]
        )
        st.altair_chart(donut, use_container_width=False)

    with colB:
        st.markdown("### ")
        st.markdown("### ")
        for i, row in sub_dist.iterrows():
            color = SIG_PALETTE[i % len(SIG_PALETTE)]
            st.markdown(
                f"""
                <div class='sig-icon-wrapper' style="margin-bottom:6px;">
                    <div style="width:14px; height:14px; border-radius:50%; background:{color};"></div>
                    <div style="font-weight:600;">{row[COL_SUBFAMILY]}</div>
                    <div style="margin-left:auto; padding:2px 10px; border-radius:10px; background:{color}; color:white; font-weight:600;">
                        {row['Count']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


    # --------------------------------------------
    # BARS — Career Path, Band, Grade
    # --------------------------------------------
    st.markdown("## Structure Distribution")

    # Career Paths
    path_dist = (
        family_df.groupby(COL_CAREER_PATH)[COL_PROFILE]
        .nunique()
        .reset_index(name="Profiles")
        .sort_values("Profiles", ascending=False)
    )

    st.markdown("### Job Profiles per Career Path")
    bar1 = alt.Chart(path_dist).mark_bar(
        cornerRadiusTopLeft=6, cornerRadiusBottomLeft=6
    ).encode(
        x="Profiles:Q",
        y=alt.Y(COL_CAREER_PATH, sort='-x'),
        color=alt.Color("Profiles:Q", scale=alt.Scale(range=[SIG_SPARK, SIG_SKY]), legend=None),
    )
    st.altair_chart(bar1, use_container_width=True)

    # Career Bands
    band_dist = (
        family_df.groupby(COL_BAND)[COL_PROFILE]
        .nunique()
        .reset_index(name="Profiles")
        .sort_values("Profiles", ascending=False)
    )

    st.markdown("### Job Profiles per Career Band")
    bar2 = alt.Chart(band_dist).mark_bar(
        cornerRadiusTopLeft=6, cornerRadiusBottomLeft=6
    ).encode(
        x="Profiles:Q",
        y=alt.Y(COL_BAND, sort='-x'),
        color=alt.Color("Profiles:Q", scale=alt.Scale(range=[SIG_MOSS, SIG_SKY]), legend=None),
    )
    st.altair_chart(bar2, use_container_width=True)


    # Grades
    grade_dist = (
        family_df.groupby(COL_GRADE)[COL_PROFILE]
        .nunique()
        .reset_index(name="Profiles")
        .sort_values(COL_GRADE)
    )

    st.markdown("### Job Profiles per Global Grade")
    bar3 = alt.Chart(grade_dist).mark_bar(
        cornerRadiusTopLeft=6, cornerRadiusBottomLeft=6
    ).encode(
        x="Profiles:Q",
        y=alt.Y(COL_GRADE, sort='-x'),
        color=alt.Color("Profiles:Q", scale=alt.Scale(range=[SIG_FOREST, SIG_SKY]), legend=None),
    )
    st.altair_chart(bar3, use_container_width=True)


    # --------------------------------------------
    # TABLE
    # --------------------------------------------
    st.markdown("## Complete Job Profile Listing")
    st.dataframe(
        family_df[[COL_SUBFAMILY, COL_PROFILE, COL_CAREER_PATH, COL_BAND, COL_LEVEL, COL_GRADE]],
        use_container_width=True
    )
