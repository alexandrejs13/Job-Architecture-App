# pages/3_Job_Profile_Description.py
# Job Profile Description – comparação de até 3 perfis (sem scroll interno, seções alinhadas)

import streamlit as st
import pandas as pd
import html
from pathlib import Path

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="Job Profile Description", layout="wide")


# ---------------------------------------------------------
# HEADER COM PNG (nítido) + TÍTULO
# ---------------------------------------------------------
def header_png(icon_path: str, title_text: str):
    st.markdown(
        f"""
        <style>
            .page-title {{
                display: flex;
                align-items: center;
                gap: 14px;
                margin-bottom: 8px;
            }}
            .page-title img {{
                width: 38px;
                height: 38px;
                image-rendering: -webkit-optimize-contrast;
                image-rendering: crisp-edges;
            }}
            .page-title h1 {{
                margin: 0;
                padding: 0;
                font-size: 34px;
                font-weight: 700;
            }}
        </style>
        <div class="page-title">
            <img src="{icon_path}">
            <h1>{title_text}</h1>
        </div>
        <hr style="margin-top:8px;">
        """,
        unsafe_allow_html=True,
    )


header_png("assets/icons/business_review_clipboard.png", "Job Profile Description")


# ---------------------------------------------------------
# CSS GLOBAL DA PÁGINA
# ---------------------------------------------------------
st.markdown(
    """
<style>
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'PPSIGFlow', sans-serif;
    background: #ffffff !important;
    color: #222 !important;
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

/* Conteúdo principal */
.block-container {
    max-width: 1600px !important;
    padding-top: 1rem !important;
}

/* GRID – 1, 2 ou 3 colunas */
.jp-grid {
    display: grid;
    gap: 26px;
}

/* 1 coluna – mobile / telas pequenas */
@media (max-width: 899px) {
    .jp-grid {
        grid-template-columns: 1fr;
    }
}

/* 2 colunas – médio */
@media (min-width: 900px) and (max-width: 1299px) {
    .jp-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

/* 3 colunas – grande */
@media (min-width: 1300px) {
    .jp-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}

/* CARD clean, sem borda colorida lateral */
.jp-card {
    background: #ffffff;
    border: 1px solid #e8e8e8;
    border-radius: 14px;
    padding: 22px 26px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.06);
}

/* Título do card */
.jp-title {
    font-weight: 700;
    font-size: 1.25rem;
    margin-bottom: 2px;
}
.jp-gg {
    color: #145efc;
    font-weight: 700;
    margin-bottom: 14px;
}

/* Bloco meta */
.jp-meta {
    background: #f5f4f1;
    border-radius: 10px;
    padding: 12px 14px;
    margin-bottom: 18px;
    font-size: 0.94rem;
}

/* Seções */
.jp-section {
    margin-bottom: 24px;
}
.jp-section-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 700;
    font-size: 0.98rem;
    margin-bottom: 6px;
}
.jp-section-title svg {
    width: 22px;
    height: 22px;
}

/* Texto */
.jp-text {
    white-space: pre-wrap;
    font-size: 0.94rem;
    line-height: 1.45;
}

/* ------------------------------------------------------
   SINCRONIZAÇÃO DE ALTURA POR LINHA (por seção)
   – usa data-sec-index em cada .jp-section
   ------------------------------------------------------ */
</style>

<script>
function syncSectionHeights() {{
    const sections = document.querySelectorAll('.jp-section[data-sec-index]');
    if (!sections.length) return;

    // Reset minHeight antes de recalcular
    sections.forEach(s => s.style.minHeight = '0px');

    const maxByIndex = {{}};

    sections.forEach(sec => {{
        const idx = sec.getAttribute('data-sec-index');
        if (!idx) return;
        const h = sec.offsetHeight;
        if (!maxByIndex[idx] || h > maxByIndex[idx]) {{
            maxByIndex[idx] = h;
        }}
    }});

    Object.keys(maxByIndex).forEach(idx => {{
        const h = maxByIndex[idx];
        document.querySelectorAll('.jp-section[data-sec-index="' + idx + '"]').forEach(sec => {{
            sec.style.minHeight = h + 'px';
        }});
    }});
}}

window.addEventListener('load', function() {{
    syncSectionHeights();
    // Em caso de resize da janela
    window.addEventListener('resize', function() {{
        syncSectionHeights();
    }});
}});
</script>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# CARREGAR Job Profile.xlsx
# ---------------------------------------------------------
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
    st.error("Não foi possível carregar data/Job Profile.xlsx")
    st.stop()


# ---------------------------------------------------------
# FILTROS
# ---------------------------------------------------------
st.subheader("🔍 Explorador de Perfis")

familias = sorted(df["Job Family"].dropna().unique())

col1, col2, col3 = st.columns(3)

with col1:
    familia = st.selectbox("Job Family", ["Selecione..."] + familias)

with col2:
    if familia != "Selecione...":
        subs = sorted(
            df[df["Job Family"] == familia]["Sub Job Family"].dropna().unique()
        )
    else:
        subs = []
    sub = st.selectbox("Sub Job Family", ["Selecione..."] + subs)

with col3:
    if sub != "Selecione...":
        paths = sorted(
            df[df["Sub Job Family"] == sub]["Career Path"].dropna().unique()
        )
    else:
        paths = []
    trilha = st.selectbox("Career Path", ["Selecione..."] + paths)

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


# ---------------------------------------------------------
# PICKLIST – até 3 perfis
# ---------------------------------------------------------
filtered = filtered.copy()
filtered["label"] = filtered.apply(
    lambda r: f"GG {str(r['Global Grade']).replace('.0','')} • {r['Job Profile']}",
    axis=1,
)
label_to_profile = dict(zip(filtered["label"], filtered["Job Profile"]))

selecionados_labels = st.multiselect(
    "Selecione até 3 perfis para comparar:",
    options=list(label_to_profile.keys()),
    max_selections=3,
)

if not selecionados_labels:
    st.stop()

selecionados = [label_to_profile[l] for l in selecionados_labels]

rows = []
for nome in selecionados:
    subdf = filtered[filtered["Job Profile"] == nome]
    if not subdf.empty:
        rows.append(subdf.iloc[0].to_dict())

if not rows:
    st.warning("Nenhum perfil encontrado após aplicar os filtros.")
    st.stop()


# ---------------------------------------------------------
# FUNÇÃO PARA LER SVG INLINE
# ---------------------------------------------------------
def read_svg(name: str) -> str:
    try:
        svg_path = Path("assets") / "icons" / "sig" / name
        with open(svg_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        # Fallback: ícone vazio
        return "<svg width='22' height='22'></svg>"


# Mapa de seções + SVG correto (como você pediu)
sections = [
    ("Sub Job Family Description", read_svg("Hierarchy.svg")),
    ("Job Profile Description", read_svg("Content_Book_Phone.svg")),
    ("Career Band Description", read_svg("File_Clipboard_Text.svg")),
    ("Role Description", read_svg("Shopping_Business_Target.svg")),
    ("Grade Differentiator", read_svg("User_Add.svg")),
    ("Qualifications", read_svg("Edit_Pencil.svg")),
    ("Specific parameters / KPIs", read_svg("Graph_Bar.svg")),
    ("Competencies 1", read_svg("Setting_Cog.svg")),
    ("Competencies 2", read_svg("Setting_Cog.svg")),
    ("Competencies 3", read_svg("Setting_Cog.svg")),
]


# ---------------------------------------------------------
# RENDER – GRID DE CARDS (1/2/3 colunas)
# ---------------------------------------------------------
st.markdown("### ✨ Comparativo de Perfis Selecionados")

st.markdown('<div class="jp-grid">', unsafe_allow_html=True)

for card in rows:
    job = html.escape(str(card.get("Job Profile", "")))
    gg = html.escape(str(card.get("Global Grade", "")))
    jf = html.escape(str(card.get("Job Family", "")))
    sf = html.escape(str(card.get("Sub Job Family", "")))
    cp = html.escape(str(card.get("Career Path", "")))
    fc = html.escape(str(card.get("Full Job Code", "")))

    card_html = f"""
    <div class="jp-card">
        <div class="jp-title">{job}</div>
        <div class="jp-gg">GG {gg}</div>

        <div class="jp-meta">
            <div><b>Job Family:</b> {jf}</div>
            <div><b>Sub Job Family:</b> {sf}</div>
            <div><b>Career Path:</b> {cp}</div>
            <div><b>Full Job Code:</b> {fc}</div>
        </div>
    """

    # seções em ordem fixa, sempre exibidas (mesmo que vazias -> "—")
    for idx, (sec_name, svg_icon) in enumerate(sections):
        raw_content = str(card.get(sec_name, "") or "").strip()
        if not raw_content or raw_content.lower() == "nan":
            content = "—"
        else:
            content = html.escape(raw_content)

        card_html += f"""
        <div class="jp-section" data-sec-index="{idx}">
            <div class="jp-section-title">
                {svg_icon}
                <span>{sec_name}</span>
            </div>
            <div class="jp-text">{content}</div>
        </div>
        """

    card_html += "</div>"  # fecha jp-card

    st.markdown(card_html, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
