import streamlit as st
import pandas as pd
import html
from pathlib import Path

st.set_page_config(page_title="Job Profile Description", layout="wide")

# HEADER -----------------------------------------------------

def header_png(icon_path, title_text):
    st.markdown(
        f"""
        <div class="page-title" style="display:flex; align-items:center; gap:12px; margin-bottom:4px;">
            <img src="{icon_path}" style="width:40px; height:40px; image-rendering:crisp-edges;">
            <h1 style="margin:0; font-size:34px; font-weight:800;">{title_text}</h1>
        </div>
        <hr>
        """,
        unsafe_allow_html=True,
    )

header_png("assets/icons/business_review_clipboard.png", "Job Profile Description")

# CSS GRID CORRETO ---------------------------------------------

st.markdown("""
<style>

.jp-grid {
    display: grid;
    gap: 26px;
    width: 100%;
}

@media (max-width: 899px) {
    .jp-grid { grid-template-columns: 1fr; }
}
@media (min-width: 900px) and (max-width: 1299px) {
    .jp-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (min-width: 1300px) {
    .jp-grid { grid-template-columns: repeat(3, 1fr); }
}

.jp-card {
    background: #faf9f7;
    border-radius: 14px;
    border: 1px solid #e6e2db;
    padding: 26px;
}

.jp-title {
    font-size: 1.35rem;
    font-weight: 800;
    margin-bottom: 4px;
}

.jp-gg {
    color: #145efc;
    font-weight: 800;
    margin-bottom: 14px;
}

.jp-meta {
    padding: 14px;
    background: #fff;
    border: 1px solid #e6e2db;
    border-radius: 12px;
    margin-bottom: 22px;
    font-size: 0.95rem;
}

.jp-section {
    margin-bottom: 26px;
}

.jp-section-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 800;
    font-size: 1rem;
    margin-bottom: 6px;
}

.jp-section-title svg {
    width: 22px;
    height: 22px;
}

.jp-text {
    font-size: 0.92rem;
    line-height: 1.42;
    white-space: pre-wrap;
}

</style>
""", unsafe_allow_html=True)


# DATA ---------------------------------------------------------

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
    st.error("Job Profile.xlsx não encontrado.")
    st.stop()

# FILTROS ------------------------------------------------------

st.subheader("🔍 Explorador de Perfis")

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
if familia!="Selecione...":
    filtered = filtered[filtered["Job Family"] == familia]
if sub!="Selecione...":
    filtered = filtered[filtered["Sub Job Family"] == sub]
if trilha!="Selecione...":
    filtered = filtered[filtered["Career Path"] == trilha]

# PICKLIST -----------------------------------------------------

filtered["label"] = filtered.apply(
    lambda r: f"GG {str(r['Global Grade']).replace('.0','')} • {r['Job Profile']}",
    axis=1
)
label_map = dict(zip(filtered["label"], filtered["Job Profile"]))

selecionados_labels = st.multiselect(
    "Selecione até 3 perfis:",
    list(label_map.keys()),
    max_selections=3,
)

if not selecionados_labels:
    st.stop()

perfils = [label_map[l] for l in selecionados_labels]
cards = [filtered[filtered["Job Profile"] == p].iloc[0].to_dict() for p in perfils]

# ÍCONES SVG ---------------------------------------------------

def svg(name):
    return Path(f"assets/icons/sig/{name}").read_text()

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

sections = list(icons.keys())

# RENDER 3 CARDS ------------------------------------------------

st.markdown('<div class="jp-grid">', unsafe_allow_html=True)

for card in cards:

    job = html.escape(card.get("Job Profile", ""))
    gg = html.escape(str(card.get("Global Grade", "")))
    jf = html.escape(card.get("Job Family", ""))
    sf = html.escape(card.get("Sub Job Family", ""))
    cp = html.escape(card.get("Career Path", ""))
    fc = html.escape(card.get("Full Job Code", ""))

    st.markdown("<div class='jp-card'>", unsafe_allow_html=True)

    st.markdown(f"""
        <div class="jp-title">{job}</div>
        <div class="jp-gg">GG {gg}</div>

        <div class="jp-meta">
            <div><b>Job Family:</b> {jf}</div>
            <div><b>Sub Job Family:</b> {sf}</div>
            <div><b>Career Path:</b> {cp}</div>
            <div><b>Full Job Code:</b> {fc}</div>
        </div>
    """, unsafe_allow_html=True)

    # Uma seção por linha (sincronizada)
    for sec in sections:
        content = card.get(sec, "").strip()
        if not content:
            content = "—"

        st.markdown(f"""
            <div class="jp-section">
                <div class="jp-section-title">{icons[sec]} {sec}</div>
                <div class="jp-text">{html.escape(content)}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
