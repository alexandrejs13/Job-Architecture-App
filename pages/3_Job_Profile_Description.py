# pages/3_Job_Profile_Description.py
# Job Profile Description – Comparação executiva com 3 cards congelados e scroll sincronizado

import streamlit as st
import pandas as pd
import html
from pathlib import Path

# ==========================================================
# CONFIG DA PÁGINA
# ==========================================================
st.set_page_config(page_title="Job Profile Description", layout="wide")


# ==========================================================
# HEADER CORPORATIVO PADRÃO
# ==========================================================
def header(icon_path, title):
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
    st.markdown("<hr style='margin-top:5px;'>", unsafe_allow_html=True)


header("assets/icons/sig/business_review_clipboard.png", "Job Profile Description")


# ==========================================================
# CSS GLOBAL + CARD + SCROLL SINCRONIZADO
# ==========================================================
css = """
<style>

body, div, p, span, h1, h2, h3, h4 {
    font-family: 'PPSIGFlow', sans-serif !important;
}

/* GRID DOS CARDS */
.jp-comparison-grid {
    display: grid;
    gap: 20px;
    width: 100%;
}

/* CARD */
.jp-card {
    background: white;
    border-radius: 14px;
    border: 1px solid #e3e3e3;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    padding: 18px 20px 20px 18px;
    display: flex;
    flex-direction: column;
    height: 760px;
    overflow-y: scroll;
}

/* SCROLL */
.jp-card::-webkit-scrollbar { width: 8px; }
.jp-card::-webkit-scrollbar-thumb {
    background: #c8c8c8;
    border-radius: 10px;
}

/* CABEÇALHO FIXO NO CARD */
.jp-title {
    font-size: 1.25rem;
    font-weight: 800;
    color: #222;
    position: sticky;
    top: 0;
    background: white;
    padding-bottom: 4px;
    padding-top: 4px;
    z-index: 20;
}

.jp-gg {
    font-size: 1rem;
    font-weight: 800;
    color: #145efc;
    margin-bottom: 12px;
    position: sticky;
    top: 38px;
    background: white;
    z-index: 20;
}

.jp-meta-block {
    background: #f5f4f1;
    border-radius: 10px;
    padding: 10px 12px;
    font-size: 0.88rem;
    margin-bottom: 14px;
    position: sticky;
    top: 76px;
    z-index: 19;
}

/* SEÇÕES */
.jp-section {
    border-radius: 10px;
    padding: 10px 12px;
    margin-bottom: 14px;
    background: #fafafa;
    border-left: 4px solid #145efc;
}

.jp-section.alt {
    background: #f0f4ff;
    border-left-color: #4f5d75;
}

.jp-section-title {
    font-weight: 700;
    font-size: 0.92rem;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
}

.jp-section-title img {
    width: 18px;
    margin-bottom: -3px;
}

.jp-text {
    font-size: 0.88rem;
    line-height: 1.45;
    white-space: pre-wrap;
}

</style>
"""

st.markdown(css, unsafe_allow_html=True)


# JS PARA SCROLL SINCRONIZADO ENTRE OS CARDS
sync_js = """
<script>
function syncScroll() {
    const cards = window.parent.document.querySelectorAll('.jp-card');
    cards.forEach((card) => {
        card.addEventListener('scroll', () => {
            let pos = card.scrollTop;
            cards.forEach((c) => {
                if (c !== card) c.scrollTop = pos;
            });
        });
    });
}
setTimeout(syncScroll, 1500);
</script>
"""

st.markdown(sync_js, unsafe_allow_html=True)


# ==========================================================
# MAPA DE ÍCONES CORPORATIVOS PARA AS SEÇÕES
# ==========================================================
ICONES_SECOES = {
    "Sub Job Family Description": "assets/icons/sig/Hierarchy.svg",
    "Job Profile Description": "assets/icons/sig/File_Clipboard_Text.svg",
    "Career Band Description": "assets/icons/sig/Hierarchy.svg",
    "Role Description": "assets/icons/sig/Shopping_Business_Target.svg",
    "Grade Differentiator": "assets/icons/sig/Edit_Pencil.svg",
    "Qualifications": "assets/icons/sig/Content_Book_Phone.svg",
    "Specific parameters / KPIs": "assets/icons/sig/Graph_Bar.svg",
    "Competencies 1": "assets/icons/sig/Setting_Cog.svg",
    "Competencies 2": "assets/icons/sig/Setting_Cog.svg",
    "Competencies 3": "assets/icons/sig/Setting_Cog.svg",
}


# ==========================================================
# CARREGAR ARQUIVO Job Profile.xlsx
# ==========================================================
@st.cache_data(ttl=600)
def load_job_profile():
    path = Path("data/Job Profile.xlsx")
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_excel(path)

    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype(str).str.strip()

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
    st.error("Arquivo Job Profile.xlsx não encontrado.")
    st.stop()


# ==========================================================
# FILTROS
# ==========================================================
st.markdown(
    '<div style="font-size:1.2rem; font-weight:700; margin-bottom:10px;">🔍 Explorador de Perfis</div>',
    unsafe_allow_html=True,
)

familias = sorted(df["Job Family"].dropna().unique())

col1, col2, col3 = st.columns(3)

with col1:
    familia = st.selectbox("Job Family:", ["Selecione..."] + familias)

with col2:
    if familia != "Selecione...":
        subs = sorted(df[df["Job Family"] == familia]["Sub Job Family"].dropna().unique())
    else:
        subs = []
    sub = st.selectbox("Sub Job Family:", ["Selecione..."] + subs)

with col3:
    if sub != "Selecione...":
        paths = sorted(df[df["Sub Job Family"] == sub]["Career Path"].dropna().unique())
    else:
        paths = []
    trilha = st.selectbox("Career Path:", ["Selecione..."] + paths)


filtered = df.copy()
if familia != "Selecione...":
    filtered = filtered[filtered["Job Family"] == familia]
if sub != "Selecione...":
    filtered = filtered[filtered["Sub Job Family"] == sub]
if trilha != "Selecione...":
    filtered = filtered[filtered["Career Path"] == trilha]

if filtered.empty:
    st.info("Ajuste os filtros para visualizar perfis.")
    st.stop()


# ==========================================================
# MULTISELECT PARA ESCOLHER ATÉ 3 PERFIS
# ==========================================================
filtered["GG_clean"] = filtered["Global Grade"].astype(str)
filtered["label"] = filtered.apply(
    lambda r: f"GG {r['GG_clean']} • {r['Job Profile']}", axis=1
)
label_to_profile = dict(zip(filtered["label"], filtered["Job Profile"]))

selected_labels = st.multiselect(
    "Selecione até 3 perfis para comparar:",
    options=list(label_to_profile.keys()),
    max_selections=3,
)

if not selected_labels:
    st.info("Selecione ao menos 1 perfil.")
    st.stop()

selected_profiles = [label_to_profile[l] for l in selected_labels]


# ==========================================================
# PREPARAR DADOS DOS CARDS
# ==========================================================
cards_data = []
for nome in selected_profiles:
    row = filtered[filtered["Job Profile"] == nome]
    if not row.empty:
        cards_data.append(row.iloc[0].to_dict())

num_cards = len(cards_data)
grid_template = f"grid-template-columns: repeat({num_cards}, 1fr);"

st.markdown("### ✨ Comparativo de Perfis Selecionados")

html_cards = [f'<div class="jp-comparison-grid" style="{grid_template}">']


# ==========================================================
# RENDERIZAR CARDS
# ==========================================================
for card in cards_data:
    job_profile = html.escape(card.get("Job Profile", ""))
    gg = html.escape(card.get("Global Grade", ""))
    job_family = html.escape(card.get("Job Family", ""))
    sub_family = html.escape(card.get("Sub Job Family", ""))
    career_path = html.escape(card.get("Career Path", ""))
    full_code = html.escape(card.get("Full Job Code", ""))

    def esc(c):
        return html.escape(str(card.get(c, "") or "")).strip()

    sections = [
        ("Sub Job Family Description", esc("Sub Job Family Description")),
        ("Job Profile Description", esc("Job Profile Description")),
        ("Career Band Description", esc("Career Band Description")),
        ("Role Description", esc("Role Description")),
        ("Grade Differentiator", esc("Grade Differentiator")),
        ("Qualifications", esc("Qualifications")),
        ("Specific parameters / KPIs", esc("Specific parameters / KPIs")),
        ("Competencies 1", esc("Competencies 1")),
        ("Competencies 2", esc("Competencies 2")),
        ("Competencies 3", esc("Competencies 3")),
    ]

    html_card = ['<div class="jp-card">']

    # CABEÇALHO
    html_card.append(f'<div class="jp-title">{job_profile}</div>')
    html_card.append(f'<div class="jp-gg">GG {gg}</div>')

    html_card.append('<div class="jp-meta-block">')
    html_card.append(f"<div><b>Job Family:</b> {job_family}</div>")
    html_card.append(f"<div><b>Sub Job Family:</b> {sub_family}</div>")
    html_card.append(f"<div><b>Career Path:</b> {career_path}</div>")
    html_card.append(f"<div><b>Full Job Code:</b> {full_code}</div>")
    html_card.append("</div>")

    # SEÇÕES COM ÍCONES
    for idx, (title, content) in enumerate(sections):
        if not content or content.lower() == "nan":
            continue

        icon_path = ICONES_SECOES.get(title, "")
        icon_html = f'<img src="{icon_path}">' if icon_path else ""

        section_class = "jp-section alt" if idx % 2 == 1 else "jp-section"

        html_card.append(f"""
        <div class="{section_class}">
            <div class="jp-section-title">
                {icon_html} {html.escape(title)}
            </div>
            <div class="jp-text">{content}</div>
        </div>
        """)

    html_card.append("</div>")
    html_cards.append("".join(html_card))


html_cards.append("</div>")
st.markdown("".join(html_cards), unsafe_allow_html=True)
