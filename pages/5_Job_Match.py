# ==========================================================
# Job Match — WTW Guided Matching (Página Final)
# ==========================================================
import streamlit as st
import pandas as pd
import base64
import os
import html

st.set_page_config(page_title="WTW Job Match Wizard", layout="wide")


# ==========================================================
# HEADER — padrão SIG
# ==========================================================
def load_icon_png(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

icon_path = "assets/icons/checkmark_success.png"
icon_b64 = load_icon_png(icon_path)

st.markdown(f"""
<div style="
    display:flex;
    align-items:center;
    gap:18px;
    margin-top:12px;
">
    <img src="data:image/png;base64,{icon_b64}"
         style="width:56px; height:56px;">
    <h1 style="
        font-size:36px;
        font-weight:700;
        margin:0;
        padding:0;
    ">
        Job Match (WTW Guided)
    </h1>
</div>

<hr style="margin-top:14px; margin-bottom:26px;">
""", unsafe_allow_html=True)


# ==========================================================
# GLOBAL LAYOUT
# ==========================================================
st.markdown("""
<style>
    .main > div {
        max-width: 1400px;
        margin-left: auto;
        margin-right: auto;
        padding-left: 20px;
        padding-right: 20px;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================================
# LOAD DATA
# ==========================================================
@st.cache_data
def load_profiles():
    return pd.read_excel("data/Job Profile.xlsx")

df = load_profiles()


# ==========================================================
# 1) FILTERS — Family / Subfamily
# ==========================================================
st.subheader("Step 1 — Select Job Family")

c1, c2 = st.columns(2)

with c1:
    family = st.selectbox(
        "Job Family",
        sorted(df["Job Family"].dropna().unique())
    )

with c2:
    subfamily_list = df[df["Job Family"] == family]["Sub Job Family"].dropna().unique()
    subfamily = st.selectbox(
        "Sub Job Family",
        sorted(subfamily_list)
    )


# ==========================================================
# 2) WTW QUESTIONS — EXECUTIVE VS MANAGER VS IC
# ==========================================================
st.subheader("Step 2 — Determine Career Band (WTW Guidelines)")

career_band = st.radio(
    "Select the option that describes the role:",
    [
        "Executive — defines long-term strategy, influences business unit strategy, broader org impact",
        "Manager — manages people, teams, projects or a body of work",
        "Individual Contributor — applies professional/technical expertise without people management"
    ]
)

if "Executive" in career_band:
    band = "EX"
elif "Manager" in career_band:
    band = "M"
else:
    band = "P"   # default IC band before refining


# ==========================================================
# 3) IC BAND DETAIL — Professional / Technical / Business Support / Manual Labor
# ==========================================================
path = None

if band == "P":
    st.subheader("Step 3 — Identify the IC Career Path")

    path = st.radio(
        "For IC, which Career Path best matches?",
        [
            "Professional (P)",
            "Technical Support (T)",
            "Business Support (U)",
            "Production / Manual Labor (W)"
        ]
    )

    if "Professional" in path:
        band = "P"
    elif "Technical" in path:
        band = "T"
    elif "Business" in path:
        band = "U"
    elif "Production" in path:
        band = "W"


# ==========================================================
# 4) WTW CAREER LEVEL
# ==========================================================
st.subheader("Step 4 — Career Level")

levels_map = {
    "M": ["M1", "M2", "M3", "M4", "M5"],
    "P": ["P1", "P2", "P3", "P4", "P5", "P6"],
    "T": ["T1", "T2", "T3", "T4"],
    "U": ["U1", "U2", "U3", "U4"],
    "W": ["W1", "W2", "W3", "W4"],
    "EX": ["15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25"]
}

career_level = st.selectbox(
    "Select Career Level",
    levels_map[band]
)


# ==========================================================
# 5) MATCHING IN THE JOB PROFILE DATASET
# ==========================================================
st.subheader("Step 5 — Recommended Job Profile")

# Filtra DF pelo Family/Subfamily primeiro
df_f = df[(df["Job Family"] == family) & (df["Sub Job Family"] == subfamily)].copy()

# Career Path (quando existir)
if band in ["P", "T", "U", "W"]:
    df_f = df_f[df_f["Career Path"].str.startswith(band)]

# Global Grade
df_f = df_f[df_f["Global Grade"].astype(str) == str(career_level)]

if df_f.empty:
    st.error("Nenhum Job Profile encontrado com esses critérios. Ajuste Family/Subfamily/Level.")
    st.stop()

# pega o primeiro match (único)
profile = df_f.iloc[0].to_dict()

st.success(f"**Job Profile recomendado:** {profile['Job Profile']} (GG {profile['Global Grade']})")


# ==========================================================
# 6) DISPLAY — SINGLE COLUMN DESCRIPTION (modelo da página anterior)
# ==========================================================
st.subheader("Job Profile Description")

sections = [
    "Sub Job Family Description",
    "Job Profile Description",
    "Career Band Description",
    "Role Description",
    "Grade Differentiator",
    "Qualifications",
    "Specific parameters / KPIs",
    "Competencies 1",
    "Competencies 2",
    "Competencies 3",
]

for sec in sections:
    st.markdown(f"### {sec}")
    st.markdown(
        f"""
        <div style="
            background:#f7f6f3;
            border:1px solid #e2e0dc;
            padding:18px;
            border-radius:12px;
            font-size:15px;
            line-height:1.45;
        ">
            {html.escape(str(profile.get(sec,'')))}
        </div>
        """,
        unsafe_allow_html=True
    )

