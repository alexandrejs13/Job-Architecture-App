# pages/3_Job_Profile_Description.py
# Job Profile Description – up to 3 profiles comparison (SIG Design System)

import streamlit as st
import pandas as pd
import html
from pathlib import Path

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(page_title="Job Profile Description", layout="wide")

# ==========================================================
# HEADER
# ==========================================================
def header(icon_path: str, title: str):
    col1, col2 = st.columns([0.08, 0.92])
    with col1:
        st.image(icon_path, width=48)
    with col2:
        st.markdown(
            f"""
            <h1 style="margin:0; padding:0; font-size:36px; font-weight:700;">
                {title}
            </h1>
            """,
            unsafe_allow_html=True,
        )
    # Thin separator just below the title
    st.markdown(
        "<hr style='margin-top:5px; margin-bottom:0;'>",
        unsafe_allow_html=True,
    )


header("assets/icons/business_review_clipboard.png", "Job Profile Description")

# ==========================================================
# GLOBAL CSS
# ==========================================================
custom_css = """
<style>
@font-face {
    font-family: 'PPSIGFlow';
    src: url('assets/css/fonts/PPSIGFlow-Regular.otf') format('opentype');
    font-weight: 400;
}
@font-face {
    font-family: 'PPSIGFlow';
    src: url('assets/css/fonts/PPSIGFlow-SemiBold.otf') format('opentype');
    font-weight: 600;
}
@font-face {
    font-family: 'PPSIGFlow';
    src: url('assets/css/fonts/PPSIGFlow-Bold.otf') format('opentype');
    font-weight: 700;
}

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'PPSIGFlow', sans-serif !important;
    background: #ffffff !important;
    color: #222 !important;
}

.block-container {
    max-width: 1600px !important;
    padding-top: 0.5rem !important;  /* título bem próximo do conteúdo */
}

/* ===== GRID FOR 1–3 COLUMNS ===== */
.jp-grid {
    display: grid;
    gap: 24px;
}

/* COLUMN WRAPPER */
.jp-col {
    position: relative;
}

/* ===== HEADER CARD (STICKY SUMMARY PER COLUMN) ===== */
.jp-header-card {
    background: #ffffff;
    border: 1px solid #e6e6e6;
    border-radius: 14px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.06);
    padding: 18px 22px 16px 22px;
    position: sticky;
    top: 90px;  /* abaixo da barra do Streamlit + título da página */
    z-index: 5;
}

/* ===== BODY CARD (DESCRIPTIONS – SCROLL WITH PAGE) ===== */
.jp-body-card {
    margin-top: 16px;  /* espaço visível entre o card de resumo e o de descrição */
    background: #ffffff;
    border: 1px solid #e6e6e6;
    border-radius: 14px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.06);
    overflow: hidden;  /* a borda inferior sempre limpa, sem texto "borrado" */
}

/* Inner padding so sections start a bit inside the card */
.jp-body-inner {
    padding: 12px 22px 18px 22px;
}

/* ===== TITLES ===== */
.jp-title {
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 4px;
}

.jp-gg {
    color: #145efc;
    font-weight: 700;
    margin-bottom: 10px;
}

/* META BLOCK */
.jp-meta-block {
    background: #f5f4f1;
    border-radius: 10px;
    padding: 10px 12px;
    font-size: 0.9rem;
}

/* ===== SECTIONS ===== */
.jp-section {
    padding: 10px 0 12px 0;
    border-bottom: 1px solid #f0f0f0;
}

.jp-section:last-child {
    border-bottom: none;
}

/* Linha alternada com leve destaque, mantendo o card inteiro */
.jp-section.alt {
    background: #fafafa;
    margin: 0 -22px;
    padding-left: 22px;
    padding-right: 22px;
}

.jp-section-title {
    font-weight: 700;
    font-size: 0.92rem;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.jp-section-title img {
    width: 20px;
    opacity: 0.9;
}

.jp-text {
    line-height: 1.45;
    font-size: 0.9rem;
    white-space: pre-wrap;
}

/* FOOTER PDF ICON */
.jp-footer {
    padding-top: 10px;
    text-align: right;
}

.jp-footer img {
    width: 26px;
    opacity: 0.8;
    cursor: pointer;
}

.jp-footer img:hover {
    opacity: 1;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================================
# LOAD JOB PROFILE
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
# FILTERS
# ==========================================================
st.subheader("🔍 Job Profile Description Explorer")

families = sorted(df["Job Family"].dropna().unique())

col1, col2, col3 = st.columns(3)

with col1:
    family = st.selectbox("Job Family", ["Select..."] + families)

with col2:
    subs = (
        sorted(
            df[df["Job Family"] == family]["Sub Job Family"].dropna().unique()
        )
        if family != "Select..."
        else []
    )
    sub_family = st.selectbox("Sub Job Family", ["Select..."] + subs)

with col3:
    paths = (
        sorted(
            df[df["Sub Job Family"] == sub_family]["Career Path"]
            .dropna()
            .unique()
        )
        if sub_family != "Select..."
        else []
    )
    career_path = st.selectbox("Career Path", ["Select..."] + paths)

filtered = df.copy()
if family != "Select...":
    filtered = filtered[filtered["Job Family"] == family]
if sub_family != "Select...":
    filtered = filtered[filtered["Sub Job Family"] == sub_family]
if career_path != "Select...":
    filtered = filtered[filtered["Career Path"] == career_path]

# ==========================================================
# PICKLIST
# ==========================================================
if filtered.empty:
    st.info("No profiles found for the selected filters.")
    st.stop()

filtered["label"] = filtered.apply(
    lambda r: f"GG {str(r['Global Grade']).replace('.0','')} • {r['Job Profile']}",
    axis=1,
)

label_to_profile = dict(zip(filtered["label"], filtered["Job Profile"]))

selected_labels = st.multiselect(
    "Select up to 3 profiles:",
    options=list(label_to_profile.keys()),
    max_selections=3,
)

if not selected_labels:
    st.info("Select at least one profile to display the job profile description.")
    st.stop()

selected_profiles = [label_to_profile[l] for l in selected_labels]
rows = [filtered[filtered["Job Profile"] == p].iloc[0].to_dict() for p in selected_profiles]

num_cols = len(rows)
grid_style = f"grid-template-columns: repeat({num_cols}, minmax(0, 1fr));"

# ==========================================================
# ICONS & SECTIONS
# ==========================================================
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

# ==========================================================
# BUILD HTML GRID (HEADER CARD + BODY CARD POR COLUNA)
# ==========================================================
html_parts = [f'<div class="jp-grid" style="{grid_style}">']

for idx, card in enumerate(rows):
    job = html.escape(str(card.get("Job Profile", "")))
    gg = html.escape(str(card.get("Global Grade", ""))).replace(".0", "")
    jf = html.escape(str(card.get("Job Family", "")))
    sf = html.escape(str(card.get("Sub Job Family", "")))
    cp = html.escape(str(card.get("Career Path", "")))
    fc = html.escape(str(card.get("Full Job Code", "")))

    col_parts = ['<div class="jp-col">']

    # HEADER CARD (STICKY)
    col_parts.append('<div class="jp-header-card">')
    col_parts.append(f'<div class="jp-title">{job}</div>')
    col_parts.append(f'<div class="jp-gg">GG {gg}</div>')
    col_parts.append('<div class="jp-meta-block">')
    col_parts.append(f"<div><b>Job Family:</b> {jf}</div>")
    col_parts.append(f"<div><b>Sub Job Family:</b> {sf}</div>")
    col_parts.append(f"<div><b>Career Path:</b> {cp}</div>")
    col_parts.append(f"<div><b>Full Job Code:</b> {fc}</div>")
    col_parts.append("</div>")  # meta-block
    col_parts.append("</div>")  # jp-header-card

    # BODY CARD (DESCRIPTIONS – ROLA JUNTO COM A PÁGINA)
    col_parts.append('<div class="jp-body-card"><div class="jp-body-inner">')

    for i, sec in enumerate(sections_order):
        content = str(card.get(sec, "") or "").strip()
        if not content or content.lower() == "nan":
            continue

        icon = icons[sec]
        alt_class = " alt" if i % 2 == 1 else ""

        col_parts.append(f'<div class="jp-section{alt_class}">')
        col_parts.append(
            f'<div class="jp-section-title"><img src="assets/icons/sig/{icon}"> {sec}</div>'
        )
        col_parts.append(f'<div class="jp-text">{html.escape(content)}</div>')
        col_parts.append("</div>")  # jp-section

    # FOOTER ICON (PDF)
    col_parts.append('<div class="jp-footer">')
    col_parts.append(
        '<img src="assets/icons/sig/pdf_c3_white.svg" title="Export PDF">'
    )
    col_parts.append("</div>")  # jp-footer

    col_parts.append("</div></div>")  # jp-body-inner + jp-body-card + jp-col

    html_parts.append("".join(col_parts))

html_parts.append("</div>")  # jp-grid

# ==========================================================
# RENDER
# ==========================================================
st.markdown("".join(html_parts), unsafe_allow_html=True)
