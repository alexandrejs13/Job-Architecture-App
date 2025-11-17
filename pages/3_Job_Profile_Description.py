# pages/3_Job_Profile_Description.py
# Job Profile Description – Comparação com design SIG, ícones SVG inline e cards alinhados

import streamlit as st
import pandas as pd
import html
from pathlib import Path

# ==========================================================
# CONFIG DA PÁGINA
# ==========================================================
st.set_page_config(page_title="Job Profile Description", layout="wide")

# ==========================================================
# FUNÇÃO: HEADER COM PNG HD
# ==========================================================
def header_hd_png(icon_path, title):
    st.markdown(
        f"""
        <style>
            .page-header {{
                display: flex;
                align-items: center;
                gap: 16px;
                margin-top: 10px;
                margin-bottom: 6px;
            }}
            .page-header img {{
                width: 40px;
                height: 40px;
                image-rendering: -webkit-optimize-contrast;
                image-rendering: crisp-edges;
            }}
            .page-header h1 {{
                font-size: 36px;
                margin: 0;
                padding: 0;
                font-weight: 700;
                font-family: 'PPSIGFlow', sans-serif;
            }}
        </style>

        <div class="page-header">
            <img src="{icon_path}">
            <h1>{title}</h1>
        </div>
        <hr>
        """,
        unsafe_allow_html=True,
    )

header_hd_png("assets/icons/business_review_clipboard.png", "Job Profile Description")

# ==========================================================
# CSS GLOBAL
# ==========================================================
st.markdown(
    """
    <style>

    /* Fonte SIG */
    @font-face {
        font-family: 'PPSIGFlow';
        src: url('assets/css/fonts/PPSIGFlow-Regular.otf') format('opentype');
        font-weight: 400;
    }

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'PPSIGFlow', sans-serif !important;
        background: #ffffff !important;
        color: #222 !important;
    }

    /* Sidebar fixa */
    [data-testid="stSidebar"] {
        width: 300px !important;
        min-width: 300px !important;
        max-width: 300px !important;
    }

    .block-container {
        max-width: 1600px;
        padding-top: 0.8rem;
    }

    /* GRID DE CARDS */
    .cards-grid {
        display: grid;
        gap: 24px;
        margin-top: 22px;
    }

    /* CARD */
    .jp-card {
        border: 1px solid #e6e6e6;
        border-radius: 14px;
        background: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        padding: 0;
        overflow: hidden;
    }

    .jp-card-header {
        padding: 20px 24px 14px 24px;
        border-bottom: 1px solid #f0f0f0;
        background: #fff;
    }

    .jp-title {
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 4px;
    }
    .jp-gg {
        color: #145efc;
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 14px;
    }

    .jp-meta-block {
        background: #f5f4f1;
        border-radius: 10px;
        padding: 12px 14px;
        font-size: 0.92rem;
        line-height: 1.35;
    }

    /* SEÇÕES */
    .jp-section {
        padding: 20px 24px;
        border-bottom: 1px solid #f0f0f0;
    }

    .jp-section-title {
        font-weight: 700;
        font-size: 0.98rem;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 10px;
    }

    .jp-section-title svg {
        width: 22px;
        height: 22px;
        opacity: 0.9;
    }

    .jp-text {
        font-size: 0.93rem;
        line-height: 1.45;
        white-space: pre-wrap;
        margin-top: 2px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# CARREGAR DADOS
# ==========================================================
@st.cache_data(ttl=600)
def load_job_profile():
    p = Path("data") / "Job Profile.xlsx"
    if not p.exists():
        return pd.DataFrame()
    df = pd.read_excel(p)
    df.columns = df.columns.str.strip()
    return df

df = load_job_profile()
if df.empty:
    st.error("❌ Erro ao carregar o arquivo Job Profile.xlsx no diretório /data")
    st.stop()

# ==========================================================
# FILTROS
# ==========================================================
st.markdown("### 🔍 Explorador de Perfis")

familias = sorted(df["Job Family"].dropna().unique())
col1, col2, col3 = st.columns(3)

with col1:
    familia = st.selectbox("Job Family", ["Selecione..."] + familias)

with col2:
    subs = sorted(df[df["Job Family"] == familia]["Sub Job Family"].dropna().unique()) if familia!="Selecione..." else []
    sub = st.selectbox("Sub Job Family", ["Selecione..."] + subs)

with col3:
    paths = sorted(df[df["Sub Job Family"] == sub]["Career Path"].dropna().unique()) if sub!="Selecione..." else []
    trilha = st.selectbox("Career Path", ["Selecione..."] + paths)

filtered = df.copy()
if familia != "Selecione...":
    filtered = filtered[filtered["Job Family"] == familia]
if sub != "Selecione...":
    filtered = filtered[filtered["Sub Job Family"] == sub]
if trilha != "Selecione...":
    filtered = filtered[filtered["Career Path"] == trilha]

filtered["label"] = filtered.apply(
    lambda r: f"GG {str(r['Global Grade']).replace('.0','')} • {r['Job Profile']}",
    axis=1
)

label_to_profile = dict(zip(filtered["label"], filtered["Job Profile"]))

selecionados_labels = st.multiselect(
    "Selecione até 3 perfis:",
    options=list(label_to_profile.keys()),
    max_selections=3,
)

if not selecionados_labels:
    st.stop()

selecionados = [label_to_profile[l] for l in selecionados_labels]

rows = [filtered[filtered["Job Profile"] == p].iloc[0].to_dict() for p in selecionados]


# ==========================================================
# CARREGAR TODOS OS SVG INLINE
# ==========================================================
def svg(name):
    path = Path(f"assets/icons/sig/{name}")
    if not path.exists():
        return ""
    return path.read_text()

icons = {
    "Sub Job Family Description": svg("Hierarchy.svg"),
    "Job Profile Description": svg("Content_Book_Phone.svg"),
    "Career Band Description": svg("File_Clipboard_Text.svg"),
    "Role Description": svg("Shopping_Business_Target.svg"),
    "Grade Differentiator": svg("User_Add.svg"),
    "Qualifications": svg("Edit_Pencil.svg"),
    "Specific parameters / KPIs": svg("Graph_Bar.svg"),
    "Competencies 1": svg("Setting_Cog.svg"),
    "Competencies 2": svg("Setting_Cog.svg"),
    "Competencies 3": svg("Setting_Cog.svg"),
}

sections_order = list(icons.keys())


# ==========================================================
# RENDER DOS CARDS
# ==========================================================
st.markdown("### ✨ Comparativo de Perfis Selecionados")

# Grid automático com N colunas
grid = f"grid-template-columns: repeat({len(rows)}, 1fr);"
st.markdown(f'<div class="cards-grid" style="{grid}">', unsafe_allow_html=True)

for card in rows:

    job = html.escape(str(card.get("Job Profile","")))
    gg = html.escape(str(card.get("Global Grade","")))
    jf = html.escape(str(card.get("Job Family","")))
    sf = html.escape(str(card.get("Sub Job Family","")))
    cp = html.escape(str(card.get("Career Path","")))
    fc = html.escape(str(card.get("Full Job Code","")))

    html_card = []

    html_card.append('<div class="jp-card">')

    # HEADER
    html_card.append('<div class="jp-card-header">')
    html_card.append(f'<div class="jp-title">{job}</div>')
    html_card.append(f'<div class="jp-gg">GG {gg}</div>')

    html_card.append('<div class="jp-meta-block">')
    html_card.append(f"<div><b>Job Family:</b> {jf}</div>")
    html_card.append(f"<div><b>Sub Job Family:</b> {sf}</div>")
    html_card.append(f"<div><b>Career Path:</b> {cp}</div>")
    html_card.append(f"<div><b>Full Job Code:</b> {fc}</div>")
    html_card.append("</div>")  # meta block
    html_card.append("</div>")  # header

    # SEÇÕES
    for sec in sections_order:
        content = str(card.get(sec, "")).strip()
        if not content or content.lower()=="nan":
            continue
        icon_svg = icons[sec]

        html_card.append('<div class="jp-section">')
        html_card.append(
            f'<div class="jp-section-title">{icon_svg} {sec}</div>'
        )
        html_card.append(f'<div class="jp-text">{html.escape(content)}</div>')
        html_card.append('</div>')

    html_card.append("</div>")  # card

    st.markdown("".join(html_card), unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
