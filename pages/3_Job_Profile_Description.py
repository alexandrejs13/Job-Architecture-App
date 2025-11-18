# pages/3_Job_Profile_Description.py
# Job Profile Description – Comparison up to 3 profiles

import streamlit as st
import pandas as pd
import html
from pathlib import Path

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(page_title="Job Profile Description", layout="wide")

# =============================================================================
# HEADER
# =============================================================================
def header(icon_path, title: str):
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
    st.markdown(
        "<hr style='margin-top:8px; margin-bottom:18px;'>",
        unsafe_allow_html=True,
    )

header("assets/icons/business_review_clipboard.png", "Job Profile Description")

# =============================================================================
# GLOBAL CSS
# =============================================================================
custom_css = """
<style>
/* ------------------------------------------------------------------ */
/* FONTS                                                              */
/* ------------------------------------------------------------------ */
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
    padding-top: 0.5rem !important;
}

/* ------------------------------------------------------------------ */
/* FILTERS AREA                                                       */
/* ------------------------------------------------------------------ */
.jp-filters-title {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 0.4rem;
}

/* ------------------------------------------------------------------ */
/* GRID                                                              */
/* ------------------------------------------------------------------ */
.jp-comparison-grid {
    display: grid;
    gap: 24px;
}

/* ------------------------------------------------------------------ */
/* CARDS                                                              */
/* ------------------------------------------------------------------ */
.jp-card {
    background: #ffffff;
    border-radius: 18px;
    border: 1px solid #e5e5e5;
    box-shadow: 0 6px 14px rgba(0,0,0,0.06);
    display: flex;
    flex-direction: column;
    overflow: hidden;          /* MUITO IMPORTANTE: texto não invade fora */
}

/* Header que fica colado dentro do card, nunca fora dele */
.jp-card-header {
    position: sticky;
    top: 0;
    background: #ffffff;
    padding: 20px 24px 16px 24px;
    z-index: 2;
    border-bottom: 1px solid #f0f0f0;
}

/* Títulos do card */
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

/* Bloco meta (Job Family, Sub Job Family etc.) */
.jp-meta-block {
    background: #f7f6f3;
    border-radius: 12px;
    padding: 10px 14px;
    font-size: 0.90rem;
}

/* Corpo do card – onde as descrições rolam junto com a página */
.jp-card-body {
    padding: 16px 24px 22px 24px;
    font-size: 0.9rem;
    line-height: 1.45;
}

/* Seções dentro do corpo */
.jp-section {
    padding: 10px 0 12px 0;
    border-bottom: 1px solid #f3f3f3;
}
.jp-section:last-child {
    border-bottom: none;
}

.jp-section-title {
    font-weight: 700;
    font-size: 0.93rem;
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
    white-space: pre-wrap;
}

/* ------------------------------------------------------------------ */
/* RESPONSIVIDADE                                                     */
/* ------------------------------------------------------------------ */
@media (max-width: 1100px) {
    .jp-comparison-grid {
        grid-template-columns: repeat(2, minmax(260px, 1fr));
    }
}

@media (max-width: 768px) {
    .jp-comparison-grid {
        grid-template-columns: repeat(1, minmax(260px, 1fr));
    }
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# =============================================================================
# LOAD JOB PROFILE
# =============================================================================
@st.cache_data(ttl=600)
def load_job_profile() -> pd.DataFrame:
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

# =============================================================================
# FILTERS
# =============================================================================
st.subheader("🔍 Job Profile Description Explorer")

families = sorted(df["Job Family"].dropna().unique())

col1, col2, col3 = st.columns(3)

with col1:
    family = st.selectbox(
        "Job Family",
        ["Select..."] + families,
        index=0,
    )

with col2:
    if family != "Select...":
        subs = sorted(
            df[df["Job Family"] == family]["Sub Job Family"].dropna().unique()
        )
    else:
        subs = []
    sub_family = st.selectbox(
        "Sub Job Family",
        ["Select..."] + subs,
        index=0,
    )

with col3:
    if sub_family != "Select...":
        paths = sorted(
            df[df["Sub Job Family"] == sub_family]["Career Path"].dropna().unique()
        )
    else:
        paths = []
    career_path = st.selectbox(
        "Career Path",
        ["Select..."] + paths,
        index=0,
    )

# Apply filters
flt = df.copy()
if family != "Select...":
    flt = flt[flt["Job Family"] == family]
if sub_family != "Select...":
    flt = flt[flt["Sub Job Family"] == sub_family]
if career_path != "Select...":
    flt = flt[flt["Career Path"] == career_path]

# =============================================================================
# PICKLIST
# =============================================================================
if flt.empty:
    st.info("No profiles found with current filters.")
    st.stop()

flt["label"] = flt.apply(
    lambda r: f"GG {str(r.get('Global Grade', '')).replace('.0','')} • {r.get('Job Profile', '')}",
    axis=1,
)

label_to_profile = dict(zip(flt["label"], flt["Job Profile"]))

selected_labels = st.multiselect(
    "Select up to 3 profiles to compare:",
    options=list(label_to_profile.keys()),
    max_selections=3,
)

if not selected_labels:
    st.info("Select at least one profile.")
    st.stop()

selected_profiles = [label_to_profile[l] for l in selected_labels]
rows = [
    flt[flt["Job Profile"] == p].iloc[0].to_dict()
    for p in selected_profiles
]

num_cards = len(rows)
grid_template = f"grid-template-columns: repeat({num_cards}, minmax(260px, 1fr));"

st.markdown("<br>", unsafe_allow_html=True)

# Icons for sections
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

# =============================================================================
# BUILD HTML FOR CARDS
# =============================================================================
html_parts = [f'<div class="jp-comparison-grid" style="{grid_template}">']

for card in rows:
    job = html.escape(str(card.get("Job Profile", "")))
    gg_raw = card.get("Global Grade", "")
    gg = html.escape(str(gg_raw).replace(".0", ""))
    jf = html.escape(str(card.get("Job Family", "")))
    sf = html.escape(str(card.get("Sub Job Family", "")))
    cp = html.escape(str(card.get("Career Path", "")))
    fc = html.escape(str(card.get("Full Job Code", "")))

    card_html = []
    card_html.append('<div class="jp-card">')

    # HEADER (sticky inside card)
    card_html.append('<div class="jp-card-header">')
    card_html.append(f'<div class="jp-title">{job}</div>')
    if gg:
        card_html.append(f'<div class="jp-gg">GG {gg}</div>')

    card_html.append('<div class="jp-meta-block">')
    if jf:
        card_html.append(f"<div><b>Job Family:</b> {jf}</div>")
    if sf:
        card_html.append(f"<div><b>Sub Job Family:</b> {sf}</div>")
    if cp:
        card_html.append(f"<div><b>Career Path:</b> {cp}</div>")
    if fc:
        card_html.append(f"<div><b>Full Job Code:</b> {fc}</div>")
    card_html.append("</div>")  # meta-block
    card_html.append("</div>")  # header

    # BODY (scrolls with the page, text some inside card)
    card_html.append('<div class="jp-card-body">')

    for sec in sections_order:
        content_raw = card.get(sec, "")
        content = "" if pd.isna(content_raw) else str(content_raw).strip()
        if not content:
            continue

        icon_file = icons[sec]
        card_html.append('<div class="jp-section">')
        card_html.append(
            f'<div class="jp-section-title">'
            f'<img src="assets/icons/sig/{icon_file}"> {html.escape(sec)}'
            f'</div>'
        )
        card_html.append(
            f'<div class="jp-text">{html.escape(content)}</div>'
        )
        card_html.append("</div>")  # section

    card_html.append("</div>")  # body
    card_html.append("</div>")  # card

    html_parts.append("".join(card_html))

html_parts.append("</div>")  # grid wrapper

st.markdown("".join(html_parts), unsafe_allow_html=True)
