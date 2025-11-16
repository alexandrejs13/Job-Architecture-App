import streamlit as st
import pandas as pd
import html
from utils.global_css import load_global_css

st.set_page_config(page_title="Job Profile Description", layout="wide")

# CSS geral do app
load_global_css()

# ==========================================================
# HEADER DO NOVO APP
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
            unsafe_allow_html=True
        )
    st.markdown("<hr style='margin-top:5px;'>", unsafe_allow_html=True)

header("assets/icons/business_review_clipboard.png", "Job Profile Description")

# ==========================================================
# CSS LOCAL
# ==========================================================
st.markdown("""
<style>

:root {
    --sig-blue: #145efc;
    --sig-sand1: #f5f3f0;
    --border: #d9d9d9;
}

.jp-grid {
    display: grid;
    gap: 22px;
    margin-top: 15px;
}

.jp-card {
    background: var(--sig-sand1);
    padding: 22px;
    border-radius: 12px;
    border: 1px solid #e5e5e5;
    width: 100%;
}

.jp-title {
    font-size: 22px;
    font-weight: 800;
    margin-bottom: 4px;
}

.jp-gg {
    color: var(--sig-blue);
    font-size: 18px;
    font-weight: 800;
    margin-bottom: 16px;
}

.jp-meta-block {
    background: white;
    border-radius: 12px;
    padding: 16px;
    border: 1px solid #eee;
    margin-bottom: 18px;
}

.jp-meta-row { font-size: 15px; margin-bottom: 5px; }

.jp-section {
    background: #fff;
    border: 1px solid var(--border);
    border-left-width: 6px;
    border-radius: 10px;
    padding: 16px 18px;
    margin-bottom: 18px;
}

.jp-section-title {
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 8px;
}

.jp-text {
    font-size: 15px;
    line-height: 1.45;
    white-space: pre-wrap;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# CARREGAR DADOS (ÚNICA FONTE)
# ==========================================================
@st.cache_data
def load_df():
    df = pd.read_excel("data/Job Profile.xlsx")
    df = df.fillna("")
    for c in df.columns:
        df[c] = df[c].astype(str)
    return df

df = load_df()

# Seções textuais
SECOES = [
    ("Sub Job Family Description", "🧭 Sub Job Family Description"),
    ("Job Profile Description", "🧠 Job Profile Description"),
    ("Career Band Description", "🏛️ Career Band Description"),
    ("Role Description", "🎯 Role Description"),
    ("Grade Differentiator", "🏅 Grade Differentiator"),
    ("Qualifications", "🎓 Qualifications"),
    ("Specific parameters / KPIs", "📌 Specific parameters / KPIs"),
    ("Competencies 1", "⚙️ Competencies 1"),
    ("Competencies 2", "⚙️ Competencies 2"),
    ("Competencies 3", "⚙️ Competencies 3"),
]

# ==========================================================
# FILTROS
# ==========================================================
st.markdown("### 🔍 Explore os perfis")

familias = sorted(df["Job Family"].unique())
col1, col2, col3 = st.columns(3)

with col1:
    fam = st.selectbox("Job Family", ["Selecione…"] + familias)

with col2:
    subs = sorted(df[df["Job Family"] == fam]["Sub Job Family"].unique()) if fam != "Selecione…" else []
    subfam = st.selectbox("Sub Family", ["Selecione…"] + subs)

with col3:
    roles = sorted(df[df["Sub Job Family"] == subfam]["Job Profile"].unique()) if subfam != "Selecione…" else []
    selected = st.multiselect("Selecione até 3 perfis", roles, max_selections=3)

if not selected:
    st.info("Selecione ao menos 1 perfil.")
    st.stop()

# ==========================================================
# GRID DINÂMICO 1/2/3 COLUNAS
# ==========================================================
cols = len(selected)
grid_css = f"grid-template-columns: repeat({cols}, 1fr);"
st.markdown(f'<div class="jp-grid" style="{grid_css}">', unsafe_allow_html=True)

# ==========================================================
# RENDERIZA CADA CARD
# ==========================================================
for prof in selected:
    row = df[df["Job Profile"] == prof].iloc[0]

    card_html = f"""
    <div class="jp-card">

        <div class="jp-title">{html.escape(row['Job Profile'])}</div>
        <div class="jp-gg">GG {html.escape(row['Global Grade'])}</div>

        <div class="jp-meta-block">
            <div class="jp-meta-row"><b>Job Family:</b> {html.escape(row['Job Family'])}</div>
            <div class="jp-meta-row"><b>Sub Job Family:</b> {html.escape(row['Sub Job Family'])}</div>
            <div class="jp-meta-row"><b>Career Path:</b> {html.escape(row['Career Path'])}</div>
            <div class="jp-meta-row"><b>Full Job Code:</b> {html.escape(row['Full Job Code'])}</div>
        </div>
    """

    for col, titulo in SECOES:
        txt = row[col].strip()
        if len(txt) > 0:
            card_html += f"""
            <div class="jp-section">
                <div class="jp-section-title">{titulo}</div>
                <div class="jp-text">{html.escape(txt)}</div>
            </div>
            """

    card_html += "</div>"

    st.markdown(card_html, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
