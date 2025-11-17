# pages/3_Job_Profile_Description.py
# Job Profile Description – Comparison up to 3 profiles (SIG Design System)

import streamlit as st
import pandas as pd
import html
from pathlib import Path

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(page_title="Job Profile Description", layout="wide")

# ==========================================================
# PAGE HEADER (VISIBLE + FIXED)
# ==========================================================
def header():
    st.markdown("""
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:6px;position:relative;z-index:1000;">
            <img src='assets/icons/business_review_clipboard.png' width='48'>
            <h1 style="margin:0;padding:0;font-size:36px;font-weight:700;color:#000;">
                Job Profile Description
            </h1>
        </div>
        <hr style="margin-top:4px;margin-bottom:10px;">
    """, unsafe_allow_html=True)

header()

# ==========================================================
# CSS — FINAL + PRO + CLEAN
# ==========================================================
custom_css = """
<style>

:root {
    --sticky-offset: 100px; /* distance from top, safe for Streamlit header */
}

/* Fonts */
@font-face {
    font-family: 'PPSIGFlow';
    src: url('assets/css/fonts/PPSIGFlow-Regular.otf');
    font-weight: 400;
}
@font-face {
    font-family: 'PPSIGFlow';
    src: url('assets/css/fonts/PPSIGFlow-SemiBold.otf');
    font-weight: 600;
}
@font-face {
    font-family: 'PPSIGFlow';
    src: url('assets/css/fonts/PPSIGFlow-Bold.otf');
    font-weight: 700;
}

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'PPSIGFlow', sans-serif !important;
    background: #ffffff !important;
    color: #222 !important;
}

.block-container {
    max-width: 1580px !important;
}

/* ==========================================================
   GRID — responsive: 1, 2 or 3 columns
   ========================================================== */
.jp-comparison-grid {
    display: grid;
    gap: 24px;
    grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
}

/* ==========================================================
   CARD — perfect borders, no overflow leaks
   ========================================================== */
.jp-card {
    background: #ffffff;
    border: 1px solid #e6e6e6;
    border-radius: 14px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.06);
    overflow: hidden !important;
    position: relative;
}

.jp-inner {
    position: relative;
}

/* ==========================================================
   FULL STICKY BLOCK — EXACTLY WHAT SHOULD STAY FIXED
   ========================================================== */
.jp-sticky {
    position: sticky;
    top: var(--sticky-offset);
    background: #ffffff;
    padding: 22px 22px 18px 22px;
    z-index: 10;
    box-shadow: 0 6px 10px rgba(0,0,0,0.05);
    border-bottom: 1px solid #eee;
}

/* Titles */
.jp-title {
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: 6px;
}

.jp-gg {
    color: #145efc;
    font-weight: 700;
    margin-bottom: 14px;
}

/* Meta info block */
.jp-meta {
    background: #f5f4f1;
    border-radius: 10px;
    padding: 10px 12px;
    font-size: 0.9rem;
    line-height: 1.35;
}

/* Sections */
.jp-section {
    padding: 18px 22px;
    border-bottom: 1px solid #f0f0f0;
}

.jp-section.alt {
    background: #fafafa;
}

.jp-section-title {
    font-weight: 700;
    font-size: 0.92rem;
    margin-bottom: 10px;
    display:flex;
    align-items:center;
    gap:8px;
}

.jp-section-title img {
    width: 20px;
}

.jp-text {
    line-height: 1.45;
    font-size: 0.9rem;
    white-space: pre-wrap;
}

/* Footer */
.jp-footer {
    padding: 15px;
    text-align: right;
}

.jp-footer img {
    width: 26px;
    cursor: pointer;
    opacity: 0.75;
}
.jp-footer img:hover {
    opacity: 1;
}

</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================================
# LOAD JOB PROFILE DATA
# ==========================================================
@st.cache_data(ttl=600)
def load_job_profile():
    path = Path("data") / "Job Profile.xlsx"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip()
    return df

df = load_job_profile()
if df.empty:
    st.error("Error loading Job Profile.xlsx")
    st.stop()

# ==========================================================
# FILTERS — IN ENGLISH
# ==========================================================
st.subheader("🔍 Job Profile Description Explorer")

families = sorted(df["Job Family"].dropna().unique())

col1, col2, col3 = st.columns(3)

with col1:
    family = st.selectbox("Job Family", ["Select..."] + families)

with col2:
    subs = sorted(df[df["Job Family"] == family]["Sub Job Family"].dropna().unique()
                  ) if family != "Select..." else []
    sub = st.selectbox("Sub Job Family", ["Select..."] + subs)

with col3:
    paths = sorted(df[df["Sub Job Family"] == sub]["Career Path"].dropna().unique()
                   ) if sub != "Select..." else []
    path = st.selectbox("Career Path", ["Select..."] + paths)

filtered = df.copy()
if family != "Select...":
    filtered = filtered[filtered["Job Family"] == family]
if sub != "Select...":
    filtered = filtered[filtered["Sub Job Family"] == sub]
if path != "Select...":
    filtered = filtered[filtered["Career Path"] == path]

# ==========================================================
# PICKLIST — ENGLISH
# ==========================================================
filtered["label"] = filtered.apply(
    lambda r: f"GG {str(r['Global Grade']).replace('.0','')} • {r['Job Profile']}",
    axis=1
)

label_to_profile = dict(zip(filtered["label"], filtered["Job Profile"]))

selected_labels = st.multiselect(
    "Select up to 3 profiles to compare:",
    options=list(label_to_profile.keys()),
    max_selections=3,
)

if not selected_labels:
    st.info("Select at least one profile.")
    st.stop()

selected_profiles = [label_to_profile[l] for l in selected_labels]
rows = [filtered[filtered["Job Profile"] == p].iloc[0].to_dict()
        for p in selected_profiles]

# ==========================================================
# BUILD CARDS GRID
# ==========================================================
st.markdown("---")

html_parts = ['<div class="jp-comparison-grid">']

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

sections_order = list(icons.keys())

for card in rows:

    job = html.escape(str(card.get("Job Profile", "")))
    gg = html.escape(str(card.get("Global Grade", "")))
    jf = html.escape(str(card.get("Job Family", "")))
    sf = html.escape(str(card.get("Sub Job Family", "")))
    cp = html.escape(str(card.get("Career Path", "")))
    fc = html.escape(str(card.get("Full Job Code", "")))

    card_html = []
    card_html.append('<div class="jp-card">')
    card_html.append('<div class="jp-inner">')

    # STICKY BLOCK (FULL HEADER)
    card_html.append('<div class="jp-sticky">')
    card_html.append(f'<div class="jp-title">{job}</div>')
    card_html.append(f'<div class="jp-gg">GG {gg}</div>')
    card_html.append('<div class="jp-meta">')
    card_html.append(f"<div><b>Job Family:</b> {jf}</div>")
    card_html.append(f"<div><b>Sub Job Family:</b> {sf}</div>")
    card_html.append(f"<div><b>Career Path:</b> {cp}</div>")
    card_html.append(f"<div><b>Full Job Code:</b> {fc}</div>")
    card_html.append("</div></div>")  # close sticky

    # SECTIONS
    for i, sec in enumerate(sections_order):
        content = str(card.get(sec, "")).strip()
        if not content or content.lower() == "nan":
            continue

        icon = icons[sec]
        alt = " alt" if i % 2 else ""

        card_html.append(f'<div class="jp-section{alt}">')
        card_html.append(
            f'<div class="jp-section-title"><img src="assets/icons/sig/{icon}"> {sec}</div>'
        )
        card_html.append(f'<div class="jp-text">{html.escape(content)}</div>')
        card_html.append("</div>")

    # FOOTER
    card_html.append('<div class="jp-footer">')
    card_html.append(
        '<img src="assets/icons/sig/pdf_c3_white.svg" title="Export PDF">'
    )
    card_html.append("</div>")

    card_html.append("</div>")  # jp-inner
    card_html.append("</div>")  # jp-card

    html_parts.append("".join(card_html))

html_parts.append("</div>")

st.markdown("".join(html_parts), unsafe_allow_html=True)
