# pages/3_Job_Profile_Description.py
# Job Profile Description – comparison of up to 3 profiles

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
                {html.escape(title)}
            </h1>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("<hr style='margin-top:5px; margin-bottom: 1.25rem;'>", unsafe_allow_html=True)

header("assets/icons/business_review_clipboard.png", "Job Profile Description")

# ==========================================================
# GLOBAL CSS
# ==========================================================
custom_css = """
<style>
/* --------------------------------------------------------
   FONTES
---------------------------------------------------------*/
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
    font-family: 'PPSIGFlow', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
    background: #ffffff !important;
    color: #222 !important;
}

.block-container {
    max-width: 1600px !important;
    padding-top: 0.5rem !important;
}

/* --------------------------------------------------------
   FORM CONTROLS
---------------------------------------------------------*/
.jp-filters-subtitle {
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 0.35rem;
}

/* --------------------------------------------------------
   GRID GERAL
---------------------------------------------------------*/
.jp-fixed-header-row,
.jp-descriptions-grid {
    display: grid;
    gap: 24px;
}

/* número de colunas controlado por CSS variable */
.jp-fixed-header-row {
    grid-template-columns: repeat(var(--jp-cols, 1), minmax(0, 1fr));
    position: sticky;
    top: 112px;  /* abaixo do header + filtros */
    z-index: 20;
    padding: 12px 0 6px 0;
    background: linear-gradient(#ffffff 85%, rgba(255,255,255,0.0));
}

/* grid de descrições (não é sticky) */
.jp-descriptions-grid {
    grid-template-columns: repeat(var(--jp-cols, 1), minmax(0, 1fr));
    margin-top: 18px;
}

/* --------------------------------------------------------
   CARDS – CABEÇALHO (FIXO)
---------------------------------------------------------*/
.jp-header-card {
    background: #ffffff;
    border-radius: 18px;
    border: 1px solid #e6e6e6;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    padding: 20px 22px 18px 22px;
}

.jp-title {
    font-size: 1.35rem;
    font-weight: 700;
    margin-bottom: 4px;
}

.jp-gg {
    color: #145efc;
    font-weight: 700;
    margin-bottom: 12px;
}

.jp-meta-block {
    background: #f5f4f1;
    border-radius: 12px;
    padding: 12px 14px;
    font-size: 0.92rem;
}

/* --------------------------------------------------------
   CARDS – DESCRIÇÕES
---------------------------------------------------------*/
.jp-desc-card {
    background: #ffffff;
    border-radius: 18px;
    border: 1px solid #e6e6e6;
    box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    padding: 16px 18px 18px 18px;
}

.jp-section {
    padding: 10px 2px 12px 2px;
    border-bottom: 1px solid #f0f0f0;
}

.jp-section:last-child {
    border-bottom: none;
}

.jp-section-title {
    font-weight: 700;
    font-size: 0.95rem;
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
    line-height: 1.42;
    font-size: 0.9rem;
    white-space: pre-wrap;
}

/* --------------------------------------------------------
   PEQUENOS AJUSTES
---------------------------------------------------------*/
.jp-desc-wrapper {
    margin-top: 10px;
    margin-bottom: 24px;
}

/* diminuir um pouco o espaço acima da comparação */
.jp-compare-title {
    font-size: 1.05rem;
    font-weight: 600;
    margin: 0.8rem 0 0.4rem 0;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================================
# LOAD DATA
# ==========================================================
@st.cache_data(ttl=600)
def load_job_profile():
    path = Path("data") / "Job Profile.xlsx"
    if not path.exists():
        return pd.DataFrame()
    df_ = pd.read_excel(path)
    df_.columns = df_.columns.str.strip()
    return df_

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
    st.markdown('<div class="jp-filters-subtitle">Job Family</div>', unsafe_allow_html=True)
    family = st.selectbox(
        label="Job Family",
        options=["Select..."] + families,
        label_visibility="collapsed",
    )

with col2:
    st.markdown('<div class="jp-filters-subtitle">Sub Job Family</div>', unsafe_allow_html=True)
    subs = (
        sorted(df[df["Job Family"] == family]["Sub Job Family"].dropna().unique())
        if family != "Select..."
        else []
    )
    sub_family = st.selectbox(
        label="Sub Job Family",
        options=["Select..."] + subs,
        label_visibility="collapsed",
    )

with col3:
    st.markdown('<div class="jp-filters-subtitle">Career Path</div>', unsafe_allow_html=True)
    paths = (
        sorted(df[df["Sub Job Family"] == sub_family]["Career Path"].dropna().unique())
        if sub_family != "Select..."
        else []
    )
    career_path = st.selectbox(
        label="Career Path",
        options=["Select..."] + paths,
        label_visibility="collapsed",
    )

filtered = df.copy()
if family != "Select...":
    filtered = filtered[filtered["Job Family"] == family]
if sub_family != "Select...":
    filtered = filtered[filtered["Sub Job Family"] == sub_family]
if career_path != "Select...":
    filtered = filtered[filtered["Career Path"] == career_path]

if filtered.empty:
    st.info("No profiles found for the selected criteria.")
    st.stop()

# ==========================================================
# PICKLIST
# ==========================================================
filtered["label"] = filtered.apply(
    lambda r: f"GG {str(r['Global Grade']).replace('.0','')} • {r['Job Profile']}",
    axis=1,
)

label_to_profile = dict(zip(filtered["label"], filtered["Job Profile"]))

selected_labels = st.multiselect(
    "Select up to 3 profiles to compare:",
    options=list(label_to_profile.keys()),
    max_selections=3,
)

if not selected_labels:
    st.info("Please select at least one profile to display.")
    st.stop()

selected_profiles = [label_to_profile[l] for l in selected_labels]
rows = [filtered[filtered["Job Profile"] == p].iloc[0].to_dict() for p in selected_profiles]

num_cols = len(rows)

st.markdown('<p class="jp-compare-title">Selected profiles</p>', unsafe_allow_html=True)

# ==========================================================
# ICONS / SECTIONS
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
# BUILD HTML – FIXED HEADER CARDS
# ==========================================================
header_parts = [f'<div class="jp-fixed-header-row" style="--jp-cols:{num_cols};">']

for card in rows:
    job = html.escape(str(card.get("Job Profile", "")))
    gg = html.escape(str(card.get("Global Grade", ""))).replace(".0", "")
    jf = html.escape(str(card.get("Job Family", "")))
    sf = html.escape(str(card.get("Sub Job Family", "")))
    cp = html.escape(str(card.get("Career Path", "")))
    fc = html.escape(str(card.get("Full Job Code", "")))

    header_parts.append(
        f"""
        <div class="jp-header-card">
            <div class="jp-title">{job}</div>
            <div class="jp-gg">GG {gg}</div>
            <div class="jp-meta-block">
                <div><b>Job Family:</b> {jf}</div>
                <div><b>Sub Job Family:</b> {sf}</div>
                <div><b>Career Path:</b> {cp}</div>
                <div><b>Full Job Code:</b> {fc}</div>
            </div>
        </div>
        """
    )

header_parts.append("</div>")  # close jp-fixed-header-row
st.markdown("".join(header_parts), unsafe_allow_html=True)

# ==========================================================
# BUILD HTML – DESCRIPTION CARDS
# ==========================================================
desc_parts = [f'<div class="jp-descriptions-grid" style="--jp-cols:{num_cols};">']

for card in rows:
    desc_parts.append('<div class="jp-desc-card">')

    for sec in sections_order:
        content_raw = str(card.get(sec, "")).strip()
        if not content_raw or content_raw.lower() == "nan":
            continue
        content = html.escape(content_raw)
        icon_file = icons[sec]
        desc_parts.append(
            f"""
            <div class="jp-section">
                <div class="jp-section-title">
                    <img src="assets/icons/sig/{icon_file}">
                    {html.escape(sec)}
                </div>
                <div class="jp-text">{content}</div>
            </div>
            """
        )

    desc_parts.append("</div>")  # close jp-desc-card

desc_parts.append("</div>")  # close jp-descriptions-grid

st.markdown('<div class="jp-desc-wrapper">', unsafe_allow_html=True)
st.markdown("".join(desc_parts), unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
