import streamlit as st
import pandas as pd
import html
import streamlit.components.v1 as components

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="Job Profile Description", layout="wide")

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.markdown("""
<h1 style="font-size:36px; font-weight:700; margin-bottom:4px;">
    Job Profile Description
</h1>
<hr style="margin-top:0;">
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
@st.cache_data
def load_profiles():
    return pd.read_excel("data/Job Profile.xlsx")

df = load_profiles()

# ---------------------------------------------------------
# FILTERS
# ---------------------------------------------------------
st.subheader("🔍 Job Profile Description Explorer")

c1, c2, c3 = st.columns(3)

with c1:
    job_family = st.selectbox("Job Family",
        ["All"] + sorted(df["Job Family"].dropna().unique()))

with c2:
    subfam_list = (
        df[df["Job Family"] == job_family]["Sub Job Family"].dropna().unique()
        if job_family != "All"
        else df["Sub Job Family"].dropna().unique()
    )
    sub_family = st.selectbox("Sub Job Family",
        ["All"] + sorted(subfam_list))

with c3:
    path_list = (
        df[df["Sub Job Family"] == sub_family]["Career Path"].dropna().unique()
        if sub_family != "All"
        else df["Career Path"].dropna().unique()
    )
    career_path = st.selectbox("Career Path",
        ["All"] + sorted(path_list))

flt = df.copy()

if job_family != "All":
    flt = flt[flt["Job Family"] == job_family]
if sub_family != "All":
    flt = flt[flt["Sub Job Family"] == sub_family]
if career_path != "All":
    flt = flt[flt["Career Path"] == career_path]

flt["label"] = flt["Global Grade"].astype(str) + " • " + flt["Job Profile"]

selected = st.multiselect("Select up to 3 profiles:",
    flt["label"].tolist(), max_selections=3)

if not selected:
    st.stop()

profiles = [flt[flt["label"] == s].iloc[0].to_dict() for s in selected]

# ---------------------------------------------------------
# SECTIONS
# ---------------------------------------------------------
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

icons = {
    "Sub Job Family Description": "Hierarchy.svg",
    "Job Profile Description": "File_Clipboard_Text.svg",
    "Career Band Description": "Hierarchy.svg",
    "Role Description": "Shopping_Business_Suitcase.svg",
    "Grade Differentiator": "Edit_Pencil.svg",
    "Qualifications": "Content_Book_Phone.svg",
    "Specific parameters / KPIs": "Graph_Bar.svg",
    "Competencies 1": "Setting_Cog.svg",
    "Competencies 2": "Setting_Cog.svg",
    "Competencies 3": "Setting_Cog.svg",
}

# ---------------------------------------------------------
# BUILD HTML SAFELY
# ---------------------------------------------------------

def build_html(profiles):

    n = len(profiles)

    html_template = r"""
<html>
<head>
<meta charset="UTF-8">

<style>

html, body {
    margin: 0;
    padding: 0;
    height: 100%;
    overflow: hidden;
    font-family: 'Segoe UI', sans-serif;
}

#viewport {
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

/* TOPO */
#top-area {
    background: white;
    padding: 12px 18px;
    position: sticky;
    top: 0;
    z-index: 20;
}

.grid-top {
    display: grid;
    grid-template-columns: repeat(FILL_COLS, 1fr);
    gap: 24px;
}

.card-top {
    background: white;
    border-radius: 16px;
    padding: 22px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.12);
}

.title {
    font-size: 21px;
    font-weight: 700;
    line-height: 1.15;
}

.gg {
    color: #145efc;
    font-size: 18px;
    font-weight: 700;
    margin-top: 6px;
}

.meta {
    background: #f5f3ee;
    padding: 14px;
    border-radius: 12px;
    margin-top: 10px;
    border: 1px solid #e3e1dd;
    font-size: 15px;
    line-height: 1.45;
}

/* SCROLL */
#scroll-area {
    flex: 1;
    overflow-y: auto;
    padding: 22px;
}

.grid-row {
    display: grid;
    grid-template-columns: repeat(FILL_COLS, 1fr);
    gap: 36px;
    margin-bottom: 36px;
}

.section-title {
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.section-title img {
    width: 20px;
}

.text {
    font-size: 15px;
    line-height: 1.45;
    white-space: pre-wrap;
}

</style>
</head>

<body>
<div id="viewport">

    <div id="top-area">
        <div class="grid-top">
TOP_CARDS
        </div>
    </div>

    <div id="scroll-area">
SECTIONS_HTML
    </div>

</div>
</body>
</html>
"""

    # ---------- BUILD TOP CARDS ----------
    top_cards = ""
    for p in profiles:
        top_cards += f"""
<div class="card-top">
    <div class="title">{html.escape(p['Job Profile'])}</div>
    <div class="gg">GG {html.escape(str(p['Global Grade']))}</div>
    <div class="meta">
        <b>Job Family:</b> {html.escape(p['Job Family'])}<br>
        <b>Sub Job Family:</b> {html.escape(p['Sub Job Family'])}<br>
        <b>Career Path:</b> {html.escape(p['Career Path'])}<br>
        <b>Full Job Code:</b> {html.escape(p['Full Job Code'])}
    </div>
</div>
"""

    # ---------- BUILD SECTIONS ----------
    sections_html = ""
    for sec in sections:
        row = f'<div class="grid-row">\n'
        for p in profiles:
            txt = html.escape(str(p.get(sec, "")).strip())
            ic = icons[sec]
            row += f"""
<div>
    <div class="section-title">
        <img src="assets/icons/sig/{ic}">
        {sec}
    </div>
    <div class="text">{txt}</div>
</div>
"""
        row += "</div>"
        sections_html += row

    # ---------- FINAL HTML ----------
    html_final = html_template.replace("FILL_COLS", str(n)) \
                              .replace("TOP_CARDS", top_cards) \
                              .replace("SECTIONS_HTML", sections_html)

    return html_final


components.html(build_html(profiles), height=900, scrolling=False)
