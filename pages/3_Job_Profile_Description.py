import streamlit as st
import pandas as pd
import html
import re

from utils.data_loader import load_excel_data

# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================
st.set_page_config(page_title="Job Profile Description", layout="wide")

# ==========================================================
# HEADER (IDENTIDADE VISUAL NOVA)
# ==========================================================
def header(icon_path, title):
    col1, col2 = st.columns([0.08, 0.92])
    with col1:
        st.image(icon_path, width=48)
    with col2:
        st.markdown(f"""
            <h1 style="margin:0; padding:0; font-size:36px; font-weight:700;">
                {title}
            </h1>
        """, unsafe_allow_html=True)
    st.markdown("<hr style='margin-top:5px;'>", unsafe_allow_html=True)

header("assets/icons/business_review_clipboard.png", "Job Profile Description")

# ==========================================================
# CSS CLEAN – VISUAL NOVO SIG (NÃO ALTERA O HEADER)
# ==========================================================
st.markdown("""
<style>
/* fundo geral */
[data-testid="stAppViewContainer"] {
    background: #f5f3f0;
}

/* grid */
.comp-grid {
    display: grid;
    gap: 22px;
    margin-top: 25px;
}

.comp-card {
    background: white;
    border-radius: 10px;
    border: 1px solid #ddd;
    padding: 18px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.07);
}

/* títulos */
.comp-title {
    font-size: 1.2rem;
    font-weight: 800;
    color: #145efc;
    margin-bottom: 10px;
}

/* seções */
.section-block {
    border-left-width: 6px;
    border-left-style: solid;
    padding-left: 12px;
    margin-top: 12px;
}

.section-header {
    font-weight: 750;
    margin-bottom: 6px;
    font-size: 0.95rem;
}

.section-text {
    white-space: pre-wrap;
    color: #333;
}

/* meta */
.meta-item {
    margin-bottom: 4px;
    font-size: 0.90rem;
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# FUNÇÕES AUXILIARES
# ==========================================================
def normalize_grade(val):
    s = str(val).strip()
    if s.lower() in ("nan", "none", "", "na", "-"):
        return ""
    return re.sub(r"\.0$", "", s)

# ==========================================================
# LOAD DATA
# ==========================================================
data = load_excel_data()

df = data.get("job_profile", pd.DataFrame())
levels = data.get("level_structure", pd.DataFrame())

if df.empty:
    st.error("Erro: arquivo Job Profile não encontrado.")
    st.stop()

# LIMPEZA
df = df.copy()
df["Job Family"] = df["Job Family"].astype(str).str.strip()
df["Sub Job Family"] = df["Sub Job Family"].astype(str).str.strip().replace(["nan","None","<NA>",""], "-")
df["Career Path"] = df["Career Path"].astype(str).str.strip()
df["Global Grade"] = df["Global Grade"].apply(normalize_grade)
df["GG_Num"] = pd.to_numeric(df["Global Grade"], errors="coerce").fillna(0).astype(int)

if not levels.empty:
    levels["Global Grade"] = levels["Global Grade"].apply(normalize_grade)
    levels["GG_Num"] = pd.to_numeric(levels["Global Grade"], errors="coerce").fillna(0).astype(int)

# ==========================================================
# FILTROS (IGUAL ANTIGA FUNCIONALIDADE)
# ==========================================================
st.subheader("Explorar Perfis de Cargo")

col1, col2, col3 = st.columns(3)

with col1:
    fam = st.selectbox("Job Family", ["Selecione..."] + sorted(df["Job Family"].unique()))

with col2:
    subs = sorted(df[df["Job Family"] == fam]["Sub Job Family"].unique()) if fam != "Selecione..." else []
    subfam = st.selectbox("Sub Job Family", ["Selecione..."] + subs)

with col3:
    paths = sorted(df[(df["Sub Job Family"] == subfam)]["Career Path"].unique()) if subfam != "Selecione..." else []
    path = st.selectbox("Career Path", ["Selecione..."] + paths)

filtered = df.copy()
if fam != "Selecione...":
    filtered = filtered[filtered["Job Family"] == fam]
if subfam != "Selecione...":
    filtered = filtered[filtered["Sub Job Family"] == subfam]
if path != "Selecione...":
    filtered = filtered[filtered["Career Path"] == path]

if filtered.empty:
    st.info("Selecione filtros para visualizar os perfis.")
    st.stop()

# ==========================================================
# PICKLIST DE GG + JOB PROFILE
# ==========================================================
filtered["label"] = filtered.apply(lambda r: f"GG {r['Global Grade']} • {r['Job Profile']}", axis=1)
label_map = dict(zip(filtered["label"], filtered["Job Profile"]))

sel_labels = st.multiselect(
    "Selecione até 3 perfis para comparar:",
    options=list(label_map.keys()),
    max_selections=3
)

if not sel_labels:
    st.stop()

selected_profiles = [label_map[l] for l in sel_labels]

# ==========================================================
# CONSTRUIR GRID DOS PERFIS
# ==========================================================
st.markdown("### Comparação de Perfis")

cards = []
for p in selected_profiles:
    row = filtered[filtered["Job Profile"] == p]
    if row.empty:
        continue
    row = row.iloc[0]

    gg = row["Global Grade"]
    gg_num = row["GG_Num"]
    level_name = ""

    if not levels.empty:
        match = levels[levels["GG_Num"] == gg_num]
        if not match.empty:
            level_name = match["Level Name"].iloc[0]

    cards.append({
        "row": row,
        "level": level_name
    })

cols = f"grid-template-columns: repeat({len(cards)}, 1fr);"
html_out = f"<div class='comp-grid' style='{cols}'>"

# ----------------------------------------------------------
# BLOCOS (1) HEADER
# ----------------------------------------------------------
for c in cards:
    html_out += f"""
    <div class='comp-card'>
        <div class='comp-title'>{html.escape(c['row']['Job Profile'])}</div>
        <div><b>GG {c['row']['Global Grade']}</b> • {c['level']}</div>
    </div>
    """

# ----------------------------------------------------------
# BLOCOS (2) META
# ----------------------------------------------------------
for c in cards:
    r = c["row"]
    html_out += f"""
    <div class='comp-card'>
        <div class='meta-item'><b>Família:</b> {html.escape(r['Job Family'])}</div>
        <div class='meta-item'><b>Subfamília:</b> {html.escape(r['Sub Job Family'])}</div>
        <div class='meta-item'><b>Carreira:</b> {html.escape(r['Career Path'])}</div>
    </div>
    """

# ----------------------------------------------------------
# SEÇÕES COLORIDAS
# ----------------------------------------------------------
sections = [
    ("Sub Job Family Description", "#95a5a6"),
    ("Job Profile Description", "#e91e63"),
    ("Career Band Description", "#673ab7"),
    ("Role Description", "#145efc"),
    ("Grade Differentiator", "#ff9800"),
    ("Qualifications", "#009688")
]

for label, color in sections:
    for c in cards:
        txt = str(c["row"].get(label, "")).strip()
        if txt == "" or txt.lower() == "nan":
            html_out += "<div></div>"
        else:
            html_out += f"""
            <div class='comp-card section-block' style='border-left-color:{color}'>
                <div class='section-header' style='color:{color}'>{label}</div>
                <div class='section-text'>{html.escape(txt)}</div>
            </div>
            """

# footer vazio
for _ in cards:
    html_out += "<div></div>"

html_out += "</div>"
st.markdown(html_out, unsafe_allow_html=True)
