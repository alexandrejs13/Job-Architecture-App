import streamlit as st
import pandas as pd
import html

st.set_page_config(
    page_title="Job Profile Description Explorer",
    layout="wide"
)

st.markdown(
    """
    <style>
        /* remove padding padrão do Streamlit */
        .block-container {
            padding-top: 1rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        /* GRID principal */
        .jp-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 32px;
            width: 100%;
        }

        /* Card do topo (sticky) */
        .jp-card-top {
            background: white;
            padding: 24px;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            position: sticky;
            top: 0;
            z-index: 20;
        }

        /* Card das descrições (scroll conjunto) */
        .jp-card-desc {
            background: white;
            padding: 24px;
            border-radius: 16px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.06);
            margin-top: 24px;
            height: auto;
        }

        /* Área única de rolagem */
        .scroll-area {
            height: 800px;      /* AJUSTE COMO QUISER */
            overflow-y: auto;
            overflow-x: hidden;
            padding-right: 12px;
            margin-top: 12px;
        }

        .section-title {
            font-weight: 700;
            font-size: 18px;
            margin-bottom: 8px;
        }

        .jp-labelbox {
            background: #f6f5f2;
            padding: 16px;
            border-radius: 12px;
            font-size: 16px;
            margin-top: 12px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------------------------------------
# LOAD DATA (ajuste o caminho conforme seu projeto)
# ---------------------------------------------------------------------------------------
@st.cache_data
def load_profiles():
    df = pd.read_excel("data/Job_Profile.xlsx")
    return df

df = load_profiles()

# ---------------------------------------------------------------------------------------
# FILTROS
# ---------------------------------------------------------------------------------------
st.markdown("## 🔍 Job Profile Description Explorer")

col1, col2, col3 = st.columns(3)

with col1:
    job_family = st.selectbox(
        "Job Family",
        ["All"] + sorted(df["Job Family"].dropna().unique().tolist())
    )

with col2:
    sub_family = st.selectbox(
        "Sub Job Family",
        ["All"] + sorted(df["Sub Job Family"].dropna().unique().tolist())
    )

with col3:
    career_path = st.selectbox(
        "Career Path",
        ["All"] + sorted(df["Career Path"].dropna().unique().tolist())
    )

flt = df.copy()

if job_family != "All":
    flt = flt[flt["Job Family"] == job_family]

if sub_family != "All":
    flt = flt[flt["Sub Job Family"] == sub_family]

if career_path != "All":
    flt = flt[flt["Career Path"] == career_path]

flt["label"] = flt["GG"].astype(str) + " • " + flt["Job Profile"]

selected = st.multiselect(
    "Select up to 3 profiles to compare:",
    options=flt["label"].tolist(),
    max_selections=3
)

if not selected:
    st.info("Select profiles to display.")
    st.stop()

profiles = [
    flt[flt["label"] == s].iloc[0].to_dict()
    for s in selected
]

# ---------------------------------------------------------------------------------------
# HTML FINAL
# ---------------------------------------------------------------------------------------

html_blocks_top = ""
html_blocks_desc = ""

for p in profiles:
    # ESCAPA HTML
    title = html.escape(p["Job Profile"])
    gg = html.escape(str(p["GG"]))
    jf = html.escape(str(p["Job Family"]))
    sjf = html.escape(str(p["Sub Job Family"]))
    cp = html.escape(str(p["Career Path"]))
    fjc = html.escape(str(p["Full Job Code"]))

    sjf_desc = html.escape(str(p.get("Sub Job Family Description", "")))
    jpd = html.escape(str(p.get("Job Profile Description", "")))
    cbd = html.escape(str(p.get("Career Band Description", "")))

    # CARD TOP STICKY
    html_blocks_top += f"""
    <div class="jp-card-top">
        <div class="section-title">{title}</div>
        <div style="color:#145efc; font-weight:700; font-size:20px;">GG {gg}</div>

        <div class="jp-labelbox">
            <b>Job Family:</b> {jf}<br>
            <b>Sub Job Family:</b> {sjf}<br>
            <b>Career Path:</b> {cp}<br>
            <b>Full Job Code:</b> {fjc}
        </div>
    </div>
    """

    # CARD DE DESCRIÇÃO
    html_blocks_desc += f"""
    <div class="jp-card-desc">
        <div class="section-title">Sub Job Family Description</div>
        <p>{sjf_desc}</p>

        <div class="section-title">Job Profile Description</div>
        <p>{jpd}</p>

        <div class="section-title">Career Band Description</div>
        <p>{cbd}</p>
    </div>
    """

# GRID (3 colunas)
html_final = f"""
<div class="scroll-area">
    <div class="jp-grid">
        {html_blocks_top}
    </div>

    <div class="jp-grid" style="margin-top:32px;">
        {html_blocks_desc}
    </div>
</div>
"""

st.components.v1.html(html_final, height=900, scrolling=False)
