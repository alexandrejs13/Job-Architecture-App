# pages/3_Job_Profile_Description.py
# Job Profile Description – Comparação de até 3 perfis, layout executivo, somente Job Profile.xlsx

import streamlit as st
import pandas as pd
import html
from pathlib import Path

# ==========================================================
# CONFIG DA PÁGINA
# ==========================================================
st.set_page_config(page_title="Job Profile Description", layout="wide")

# ==========================================================
# HEADER PADRÃO (NOVA IDENTIDADE)
# ==========================================================
def header(icon_path, title):
    col1, col2 = st.columns([0.08, 0.92])
    with col1:
        st.image(icon_path, width=48)
    with col2:
        st.markdown(
            f"""
            <h1 style="margin:0; padding:0; font-size:36px; font-weight:700; font-family:'PPSIGFlow', sans-serif;">
                {title}
            </h1>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("<hr style='margin-top:5px;'>", unsafe_allow_html=True)

header("assets/icons/sig/business_review_clipboard.png", "Job Profile Description")

# ==========================================================
# CSS LOCAL – FUNDO BRANCO + LAYOUT EXECUTIVO
# ==========================================================
custom_css = """
<style>
@font-face {
    font-family: 'PPSIGFlow';
    src: url('../assets/css/fonts/PPSIGFlow-Regular.otf') format('opentype');
    font-weight: normal;
    font-style: normal;
}
body, h1, h2, h3, h4, p, div {
    font-family: 'PPSIGFlow', sans-serif !important;
}

/* Fundo branco do app */
[data-testid="stAppViewContainer"] {
    background-color: #ffffff !important;
    color: #222 !important;
}

/* Limita a largura do conteúdo principal (evita stretching infinito) */
.block-container {
    max-width: 1600px !important;
    padding-top: 1rem !important;
    padding-left: 1.2rem !important;
    padding-right: 1.2rem !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* Sidebar fixa e não redimensionável */
[data-testid="stSidebar"] {
    width: 300px !important;
    min-width: 300px !important;
    max-width: 300px !important;
}
[data-testid="stSidebar"] > div {
    width: 300px !important;
}

/* GRID DE CARDS CONFIGURAÇÃO */
.jp-comparison-grid {
    display: grid;
    gap: 20px;
    width: 100%;
}
.jp-card {
    background: #ffffff;
    border: 1px solid #e6e6e6;
    border-radius: 14px;
    padding: 22px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    display: flex;
    flex-direction: column;
    height: 650px;           /* Altura fixa padrão */
    overflow-y: auto;        /* Scroll interno */
    position: relative;
}
.jp-card-header {
    /* Se quiser, poderia usar para cabeçalho interno do card */
}
.jp-title {
    font-size: 1.35rem;
    font-weight: 800;
    margin-bottom: 4px;
    color: #222;
}
.jp-gg {
    color: #145efc;
    font-weight: 700;
    margin-bottom: 12px;
}
.jp-meta-block {
    margin-bottom: 18px;
    font-size: 0.95rem;
}
.jp-meta-row {
    padding: 3px 0;
}

/* Seções do cartão */
.jp-section {
    border-left: 5px solid #145efc;
    padding-left: 12px;
    margin-bottom: 22px;
}
.jp-section.alt {
    background: #fafafa;
    border-left-color: #1d6bff !important;
}
.jp-section-title {
    font-size: 1rem;
    font-weight: 700;
    margin-bottom: 4px;
    color: #145efc;
    display: flex;
    align-items: center;
    gap: 6px;
}
.jp-text {
    white-space: pre-wrap;
    line-height: 1.45;
    color: #444;
    font-size: 0.93rem;
}

/* Ícone de PDF no final do card */
.jp-footer {
    margin-top: auto; /* para empurrar para baixo */
    text-align: right;
}
.jp-footer img {
    width: 26px;
    height: 26px;
    cursor: pointer;
    opacity: 0.75;
    transition: 0.2s ease;
}
.jp-footer img:hover {
    opacity: 1;
    transform: scale(1.1);
}

/* Responsividade */
@media (max-width: 1200px) {
    .jp-comparison-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}
@media (max-width: 900px) {
    .jp-comparison-grid {
        grid-template-columns: 1fr;
    }
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================================
# CARREGAMENTO DOS DADOS – APENAS Job Profile.xlsx
# ==========================================================
@st.cache_data(ttl=600)
def load_job_profile():
    path = Path("data") / "Job Profile.xlsx"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_excel(path)

    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype(str).str.strip()
    if "Global Grade" in df.columns:
        df["Global Grade"] = df["Global Grade"].astype(str).str.strip().replace(r"\.0$", "", regex=True)
    return df

df = load_job_profile()

if df.empty:
    st.error("Arquivo 'Job Profile.xlsx' não encontrado ou vazio em data/Job Profile.xlsx.")
    st.stop()

expected_cols = [
    "Job Family",
    "Sub Job Family",
    "Career Path",
    "Job Profile",
    "Global Grade",
    "Full Job Code",
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
for c in expected_cols:
    if c not in df.columns:
        df[c] = ""

# ==========================================================
# FILTROS – Família / Subfamilia / Career Path
# ==========================================================
st.markdown('<div style="font-family:\'PPSIGFlow\', sans-serif; font-size:1.1rem; font-weight:700; margin-top:0.5rem; margin-bottom:0.75rem;">🔍 Explorador de Perfis</div>', unsafe_allow_html=True)

familias = sorted([f for f in df["Job Family"].dropna().unique() if str(f).strip() != ""])
col1, col2, col3 = st.columns(3)

with col1:
    familia = st.selectbox("Job Family:", ["Selecione..."] + familias, index=0)
with col2:
    if familia != "Selecione...":
        subs = sorted([s for s in df[df["Job Family"] == familia]["Sub Job Family"].dropna().unique() if str(s).strip() != ""])
    else:
        subs = []
    sub = st.selectbox("Sub Job Family:", ["Selecione..."] + subs, index=0)
with col3:
    if sub != "Selecione...":
        paths = sorted([p for p in df[df["Sub Job Family"] == sub]["Career Path"].dropna().unique() if str(p).strip() != ""])
    else:
        paths = []
    trilha = st.selectbox("Career Path:", ["Selecione..."] + paths, index=0)

filtered = df.copy()
if familia != "Selecione...":
    filtered = filtered[filtered["Job Family"] == familia]
if sub != "Selecione...":
    filtered = filtered[filtered["Sub Job Family"] == sub]
if trilha != "Selecione...":
    filtered = filtered[filtered["Career Path"] == trilha]

if filtered.empty:
    st.info("Ajuste os filtros para visualizar os perfis.")
    st.stop()

# ==========================================================
# PICKLIST – até 3 perfis para comparar
# ==========================================================
filtered = filtered.copy()
filtered["GG_clean"] = filtered["Global Grade"].astype(str).str.strip()
filtered["label"] = filtered.apply(lambda r: f'GG {r["GG_clean"] or "-"} • {r["Job Profile"]}', axis=1)
label_to_profile = dict(zip(filtered["label"], filtered["Job Profile"]))

selecionados_labels = st.multiselect(
    "Selecione até 3 perfis para comparar:",
    options=list(label_to_profile.keys()),
    max_selections=3,
)
if not selecionados_labels:
    st.info("Selecione pelo menos 1 perfil para exibir os detalhes.")
    st.stop()

selecionados = [label_to_profile[l] for l in selecionados_labels]

# ==========================================================
# PREPARAR DADOS DOS CARDS
# ==========================================================
cards_data = []
for nome in selecionados:
    row = filtered[filtered["Job Profile"] == nome]
    if row.empty:
        continue
    cards_data.append(row.iloc[0].to_dict())
if not cards_data:
    st.warning("Nenhum perfil encontrado após aplicar os filtros.")
    st.stop()

num_cards = len(cards_data)
grid_template = f"grid-template-columns: repeat({num_cards}, minmax(0, 1fr));"

st.markdown("---")
st.markdown("### ✨ Comparativo de Perfis Selecionados", unsafe_allow_html=True)

# ==========================================================
# RENDER – GRID DE CARDS
# ==========================================================
html_parts = [f'<div class="jp-comparison-grid" style="{grid_template}">']

for card in cards_data:
    job_profile = html.escape(str(card.get("Job Profile", "")))
    gg = html.escape(str(card.get("Global Grade", "")))
    job_family = html.escape(str(card.get("Job Family", "")))
    sub_family = html.escape(str(card.get("Sub Job Family", "")))
    career_path = html.escape(str(card.get("Career Path", "")))
    full_code = html.escape(str(card.get("Full Job Code", "")))

    def esc(colname: str) -> str:
        return html.escape(str(card.get(colname, "") or "")).strip()

    sections = [
        ("assets/icons/sig/Hierarchy.svg", "🧭 Sub Job Family Description", esc("Sub Job Family Description")),
        ("assets/icons/sig/File_Clipboard_Text.svg", "🧠 Job Profile Description", esc("Job Profile Description")),
        ("assets/icons/sig/Hierarchy.svg", "🏛️ Career Band Description", esc("Career Band Description")),
        ("assets/icons/sig/Shopping_Bag_Suitcase.svg", "🎯 Role Description", esc("Role Description")),
        ("assets/icons/sig/Edit_Pencil.svg", "🏅 Grade Differentiator", esc("Grade Differentiator")),
        ("assets/icons/sig/Content_Book_Phone.svg", "🎓 Qualifications", esc("Qualifications")),
        ("assets/icons/sig/Graph_Bar.svg", "📌 Specific parameters / KPIs", esc("Specific parameters / KPIs")),
        ("assets/icons/sig/Setting_Cog.svg", "⚙️ Competencies 1", esc("Competencies 1")),
        ("assets/icons/sig/Setting_Cog.svg", "⚙️ Competencies 2", esc("Competencies 2")),
        ("assets/icons/sig/Setting_Cog.svg", "⚙️ Competencies 3", esc("Competencies 3")),
    ]

    card_html = []
    card_html.append('<div class="jp-card">')
    card_html.append(f'<div class="jp-title">{job_profile}</div>')
    card_html.append(f'<div class="jp-gg">GG {gg}</div>')
    card_html.append('<div class="jp-meta-block">')
    card_html.append(f'<div class="jp-meta-row"><b>Job Family:</b> {job_family}</div>')
    card_html.append(f'<div class="jp-meta-row"><b>Sub Job Family:</b> {sub_family}</div>')
    card_html.append(f'<div class="jp-meta-row"><b>Career Path:</b> {career_path}</div>')
    card_html.append(f'<div class="jp-meta-row"><b>Full Job Code:</b> {full_code}</div>')
    card_html.append("</div>")

    for idx, (icon_path, title, content) in enumerate(sections):
        if not content:
            continue
        section_classes = "jp-section"
        if idx % 2 == 1:
            section_classes += " alt"
        card_html.append(f'<div class="{section_classes}">')
        card_html.append(f'<div class="jp-section-title"><img src="{icon_path}" width="22px" style="vertical-align:middle; margin-right:6px;">{title}</div>')
        card_html.append(f'<div class="jp-text">{content}</div>')
        card_html.append("</div>")

    # Botão PDF no final
    card_html.append('<div class="jp-footer">')
    card_html.append('<img src="assets/icons/sig/pdf_c3_white.svg" title="Export PDF">')
    card_html.append("</div>')

    card_html.append("</div>")
    html_parts.append("".join(card_html))

html_parts.append("</div>")
st.markdown("".join(html_parts), unsafe_allow_html=True)
