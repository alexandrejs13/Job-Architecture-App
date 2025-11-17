# pages/3_Job_Profile_Description.py
# Job Profile Description – Comparação de até 3 perfis (SIG Design System)

import streamlit as st
import pandas as pd
import html
from pathlib import Path

# ==========================================================
# CONFIG DA PÁGINA
# ==========================================================
st.set_page_config(page_title="Job Profile Description", layout="wide")

# ==========================================================
# CSS GLOBAL (fonte SIG + layout + sidebar fixa)
# ==========================================================
GLOBAL_CSS = """
<style>
/* ---------- FONTES SIG ---------- */
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

/* Aplica fonte no app inteiro */
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'PPSIGFlow', sans-serif !important;
    background: #ffffff !important;
    color: #222 !important;
}

/* Sidebar travada em 300px */
[data-testid="stSidebar"] {
    width: 300px !important;
    min-width: 300px !important;
    max-width: 300px !important;
}
[data-testid="stSidebar"] > div {
    width: 300px !important;
}

/* Container central */
.block-container {
    max-width: 1600px !important;
    padding-top: 1rem !important;
    padding-left: 1.2rem !important;
    padding-right: 1.2rem !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* ---------- HEADER DA PÁGINA ---------- */
.page-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 10px;
}
.page-header-icon {
    width: 40px;
    height: 40px;
    image-rendering: -webkit-optimize-contrast;
    image-rendering: crisp-edges;
}
.page-header-title {
    font-size: 36px;
    font-weight: 700;
    margin: 0;
}

/* ---------- TÍTULO DA ÁREA DE FILTROS ---------- */
.jp-section-title-main {
    font-size: 1.1rem;
    font-weight: 700;
    margin-top: 0.5rem;
    margin-bottom: 0.75rem;
}

/* ---------- GRID DOS CARDS ---------- */
.jp-grid {
    display: grid;
    gap: 24px;
    width: 100%;
}

/* Card principal */
.jp-card {
    background: #ffffff;
    border: 1px solid #e6e6e6;
    border-radius: 14px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.06);
    display: flex;
    flex-direction: column;
    height: 650px;                /* Altura padrão A) */
    overflow: hidden;             /* esconde scroll externo */
    position: relative;
}

/* Header fixo dentro do card (title + meta) */
.jp-card-header {
    padding: 18px 22px 14px 22px;
    border-bottom: 1px solid #f0f0f0;
    background: #ffffff;
    position: sticky;
    top: 0;
    z-index: 10;
}
.jp-title {
    font-size: 1.25rem;
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
    border-radius: 10px;
    padding: 8px 10px;
    font-size: 0.9rem;
}
.jp-meta-row {
    margin-bottom: 2px;
}

/* Corpo rolável do card (onde ficam as descrições) */
.jp-body {
    padding: 14px 22px 6px 22px;
    overflow-y: auto;
    height: calc(650px - 140px); /* altura do body = altura total - header */
}

/* Seções internas (Sub Job Family, Job Profile etc.) */
.jp-section {
    border-radius: 10px;
    padding: 10px 12px;
    margin-bottom: 10px;
    background: #fafafa;
    border-left: 4px solid #145efc;
}
.jp-section.alt {
    background: #f0f4ff;
    border-left-color: #4f5d75;
}
.jp-section-title {
    font-weight: 700;
    font-size: 0.9rem;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.jp-section-title svg {
    width: 20px;
    height: 20px;
}

/* Texto da descrição */
.jp-text {
    font-size: 0.9rem;
    line-height: 1.45;
    white-space: pre-wrap;
}

/* Footer com ícone de PDF alinhado à direita */
.jp-footer {
    padding: 10px 18px 14px 18px;
    text-align: right;
}
.jp-footer img {
    width: 24px;
    height: 24px;
    cursor: pointer;
    opacity: 0.8;
    image-rendering: -webkit-optimize-contrast;
    image-rendering: crisp-edges;
    transition: 0.2s ease;
}
.jp-footer img:hover {
    opacity: 1;
    transform: scale(1.05);
}

/* Responsivo – 2 colunas e depois 1 */
@media (max-width: 1200px) {
    .jp-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
    }
}
@media (max-width: 900px) {
    .jp-grid {
        grid-template-columns: 1fr !important;
    }
}
</style>

<script>
/* Sincroniza o scroll entre todos os elementos .jp-body */
window.addEventListener('load', function () {
  const bodies = document.querySelectorAll('.jp-body');
  bodies.forEach((body) => {
    body.addEventListener('scroll', () => {
      const pos = body.scrollTop;
      bodies.forEach((b) => {
        if (b !== body) {
          b.scrollTop = pos;
        }
      });
    });
  });

  /* Exportar cada card individual para impressão (simples) */
  const pdfButtons = document.querySelectorAll('.jp-footer img[data-card-id]');
  pdfButtons.forEach((btn) => {
    btn.addEventListener('click', () => {
      const cardId = btn.getAttribute('data-card-id');
      const card = document.getElementById(cardId);
      if (!card) return;
      const win = window.open('', '_blank');
      win.document.write('<html><head><title>Job Profile</title>');
      win.document.write('<style>body{font-family:Arial, sans-serif;padding:24px;}');
      win.document.write('.card{max-width:900px;margin:0 auto;}');
      win.document.write('</style></head><body>');
      win.document.write('<div class="card">');
      win.document.write(card.innerHTML);
      win.document.write('</div></body></html>');
      win.document.close();
      win.focus();
      win.print();
    });
  });
});
</script>
"""
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ==========================================================
# HEADER DA PÁGINA (PNG nítido)
# ==========================================================
st.markdown(
    """
    <div class="page-header">
        <img src="assets/icons/business_review_clipboard.png"
             class="page-header-icon">
        <h1 class="page-header-title">Job Profile Description</h1>
    </div>
    <hr>
    """,
    unsafe_allow_html=True,
)

# ==========================================================
# CARREGAR DADOS
# ==========================================================
@st.cache_data(ttl=600)
def load_job_profile() -> pd.DataFrame:
    path = Path("data") / "Job Profile.xlsx"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip()

    # Normaliza Global Grade (tira .0)
    if "Global Grade" in df.columns:
        df["Global Grade"] = (
            df["Global Grade"]
            .astype(str)
            .str.strip()
            .str.replace(r"\\.0$", "", regex=True)
        )
    return df


df = load_job_profile()
if df.empty:
    st.error("Arquivo 'Job Profile.xlsx' não encontrado ou vazio em data/Job Profile.xlsx.")
    st.stop()

# Garante colunas que vamos usar
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
for col in expected_cols:
    if col not in df.columns:
        df[col] = ""

# ==========================================================
# CARREGAR SVGs SIG (inline)
# ==========================================================
def load_svg(name: str) -> str:
    svg_path = Path("assets") / "icons" / "sig" / name
    try:
        return svg_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""  # se faltar algum, não quebra


SVG_ICONS = {
    "Sub Job Family Description": load_svg("Hierarchy.svg"),
    "Job Profile Description": load_svg("File_Clipboard_Text.svg"),
    "Career Band Description": load_svg("Hierarchy.svg"),
    "Role Description": load_svg("Shopping_Business_Target.svg"),
    "Grade Differentiator": load_svg("Edit_Pencil.svg"),
    "Qualifications": load_svg("Content_Book_Phone.svg"),
    "Specific parameters / KPIs": load_svg("Graph_Bar.svg"),
    "Competencies 1": load_svg("Setting_Cog.svg"),
    "Competencies 2": load_svg("Setting_Cog.svg"),
    "Competencies 3": load_svg("Setting_Cog.svg"),
}

SECTIONS_ORDER = list(SVG_ICONS.keys())

# ==========================================================
# FILTROS – Família / Subfamilia / Career Path
# ==========================================================
st.markdown(
    '<div class="jp-section-title-main">🔍 Explorador de Perfis</div>',
    unsafe_allow_html=True,
)

familias = sorted(
    [f for f in df["Job Family"].dropna().unique() if str(f).strip() != ""]
)

col1, col2, col3 = st.columns(3)

with col1:
    familia = st.selectbox("Job Family:", ["Selecione..."] + familias, index=0)

with col2:
    if familia != "Selecione...":
        subs = sorted(
            [
                s
                for s in df[df["Job Family"] == familia]["Sub Job Family"]
                .dropna()
                .unique()
                if str(s).strip() != ""
            ]
        )
    else:
        subs = []
    sub = st.selectbox("Sub Job Family:", ["Selecione..."] + subs, index=0)

with col3:
    if sub != "Selecione...":
        paths = sorted(
            [
                p
                for p in df[df["Sub Job Family"] == sub]["Career Path"]
                .dropna()
                .unique()
                if str(p).strip() != ""
            ]
        )
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
filtered["label"] = filtered.apply(
    lambda r: f'GG {r["GG_clean"] or "-"} • {r["Job Profile"]}', axis=1
)
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
# RENDER – GRID DE CARDS (HTML)
# ==========================================================
html_parts = [f'<div class="jp-grid" style="{grid_template}">']

for idx, card in enumerate(cards_data):
    card_id = f"jp-card-{idx}"

    job_profile = html.escape(str(card.get("Job Profile", "")))
    gg = html.escape(str(card.get("Global Grade", "")))
    job_family = html.escape(str(card.get("Job Family", "")))
    sub_family = html.escape(str(card.get("Sub Job Family", "")))
    career_path = html.escape(str(card.get("Career Path", "")))
    full_code = html.escape(str(card.get("Full Job Code", "")))

    def esc(colname: str) -> str:
        return html.escape(str(card.get(colname, "") or "")).strip()

    card_html = []
    card_html.append(f'<div class="jp-card" id="{card_id}">')

    # HEADER FIXO
    card_html.append('<div class="jp-card-header">')
    card_html.append(f'<div class="jp-title">{job_profile}</div>')
    card_html.append(f'<div class="jp-gg">GG {gg}</div>')
    card_html.append('<div class="jp-meta-block">')
    card_html.append(
        f'<div class="jp-meta-row"><b>Job Family:</b> {job_family}</div>'
    )
    card_html.append(
        f'<div class="jp-meta-row"><b>Sub Job Family:</b> {sub_family}</div>'
    )
    card_html.append(
        f'<div class="jp-meta-row"><b>Career Path:</b> {career_path}</div>'
    )
    card_html.append(
        f'<div class="jp-meta-row"><b>Full Job Code:</b> {full_code}</div>'
    )
    card_html.append("</div>")  # fecha meta-block
    card_html.append("</div>")  # fecha header

    # BODY ROLÁVEL
    card_html.append('<div class="jp-body">')

    for i, section_name in enumerate(SECTIONS_ORDER):
        content = esc(section_name)
        if not content or content.lower() == "nan":
            continue

        section_classes = "jp-section"
        if i % 2 == 1:
            section_classes += " alt"

        svg = SVG_ICONS.get(section_name, "")

        card_html.append(f'<div class="{section_classes}">')
        card_html.append('<div class="jp-section-title">')
        if svg:
            card_html.append(svg)
        card_html.append(f"<span>{section_name}</span>")
        card_html.append("</div>")  # título
        card_html.append(f'<div class="jp-text">{content}</div>')
        card_html.append("</div>")  # seção

    card_html.append("</div>")  # fecha jp-body

    # FOOTER COM ÍCONE PDF
    card_html.append('<div class="jp-footer">')
    card_html.append(
        f'<img src="assets/icons/sig/pdf_c3_white.svg" '
        f'title="Exportar PDF" data-card-id="{card_id}">'
    )
    card_html.append("</div>")  # footer

    card_html.append("</div>")  # jp-card
    html_parts.append("".join(card_html))

html_parts.append("</div>")  # jp-grid

st.markdown("".join(html_parts), unsafe_allow_html=True)
