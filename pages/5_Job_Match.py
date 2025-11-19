# ==========================================================
# PAGE CONFIG + HEADER (PADRÃO SIG)
# ==========================================================
import streamlit as st
import pandas as pd
import numpy as np
import base64
import os
import html
import re
import streamlit.components.v1 as components

st.set_page_config(page_title="Job Match", layout="wide")

# ----------------------------------------------------------
# LOAD ICON
# ----------------------------------------------------------
def load_icon_png(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

icon_path = "assets/icons/checkmark_success.png"
icon_b64 = load_icon_png(icon_path)

st.markdown(f"""
<div style="
    display:flex;
    align-items:center;
    gap:18px;
    margin-top:12px;
">
    <img src="data:image/png;base64,{icon_b64}"
         style="width:56px; height:56px;">
    <h1 style="
        font-size:36px;
        font-weight:700;
        margin:0;
        padding:0;
    ">
        Job Match
    </h1>
</div>

<hr style="margin-top:14px; margin-bottom:26px;">
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# GLOBAL LAYOUT STYLE (SIG)
# ----------------------------------------------------------
st.markdown("""
<style>
.main > div {
    max-width: 1400px;
    margin-left: auto;
    margin-right: auto;
    padding-left: 20px;
    padding-right: 20px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# LOAD JOB PROFILE DATA
# ==========================================================
@st.cache_data
def load_profiles():
    return pd.read_excel("data/Job Profile.xlsx")

df = load_profiles()

# ==========================================================
# LOAD SVG ICONS
# ==========================================================
def load_svg(svg_name):
    path = f"assets/icons/sig/{svg_name}"
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

icons_svg = {
    "Sub Job Family Description": load_svg("Hierarchy.svg"),
    "Job Profile Description": load_svg("Content_Book_Phone.svg"),
    "Career Band Description": load_svg("File_Clipboard_Text.svg"),
    "Role Description": load_svg("Shopping_Business_Target.svg"),
    "Grade Differentiator": load_svg("User_Add.svg"),
    "Qualifications": load_svg("Edit_Pencil.svg"),
    "Specific parameters / KPIs": load_svg("Graph_Bar.svg"),
    "Competencies 1": load_svg("Setting_Cog.svg"),
    "Competencies 2": load_svg("Setting_Cog.svg"),
    "Competencies 3": load_svg("Setting_Cog.svg"),
}

sections = [
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

# ==========================================================
# HTML RENDER (1 COLUNA, LAYOUT PREMIUM)
# ==========================================================
def build_single_profile_html(p):

    job = html.escape(p["Job Profile"])
    gg = html.escape(str(p["Global Grade"]))
    jf = html.escape(p["Job Family"])
    sf = html.escape(p["Sub Job Family"])
    cp = html.escape(p["Career Path"])
    fc = html.escape(p["Full Job Code"])

    html_code = f"""
<html>
<head>
<meta charset="UTF-8">

<style>
html, body {{
    margin: 0; padding: 0; height: 100%;
    overflow: hidden;
    font-family: 'Segoe UI', sans-serif;
}}

#viewport {{
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}}

.card-top {{
    background: #f5f3ee;
    border-radius: 16px;
    padding: 22px 24px;
    border: 1px solid #e3e1dd;
}}

.title {{
    font-size: 20px;
    font-weight: 700;
}}

.gg {{
    color: #145efc;
    font-size: 16px;
    font-weight: 700;
    margin-top: 6px;
}}

.meta {{
    background: white;
    padding: 14px;
    margin-top: 14px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    font-size: 14px;
}}

#scroll-area {{
    flex: 1;
    overflow-y: auto;
    padding: 22px 4px 32px 0;
}}

.section-box {{
    padding-bottom: 26px;
}}

.section-title {{
    font-size: 16px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 6px;
}}

.section-line {{
    height: 1px;
    background: #e8e6e1;
    width: 100%;
    margin: 8px 0 14px 0;
}}

.section-text {{
    font-size: 14px;
    white-space: pre-wrap;
}}

.icon-inline {{
    width: 20px;
    height: 20px;
}}
</style>

</head>

<body>
<div id="viewport">

    <div id="top-area">
        <div class="card-top">
            <div class="title">{job}</div>
            <div class="gg">GG {gg}</div>

            <div class="meta">
                <b>Job Family:</b> {jf}<br>
                <b>Sub Job Family:</b> {sf}<br>
                <b>Career Path:</b> {cp}<br>
                <b>Full Job Code:</b> {fc}
            </div>
        </div>
    </div>

    <div id="scroll-area">
"""

    # sections
    for sec in sections:
        val = p.get(sec, "")
        icon = icons_svg.get(sec, "")

        html_code += f"""
        <div class="section-box">
            <div class="section-title">
                <span class="icon-inline">{icon}</span>
                {html.escape(sec)}
            </div>
            <div class="section-line"></div>
            <div class="section-text">{html.escape(str(val))}</div>
        </div>
        """

    html_code += """
    </div>

</div>
</body>
</html>
"""

    return html_code


# ==========================================================
# MATCH ENGINE: TAGGING + SCORING
# ==========================================================

def clean_text(t):
    if pd.isna(t): return ""
    t = str(t).lower()
    t = re.sub(r"[^a-z0-9\s]", " ", t)
    return t

def extract_keywords(text):
    text = clean_text(text)
    words = set(text.split())
    return words

def score_match(user_tags, job_profile_row):
    """ Weighted scoring model """

    weights = {
        "Grade Differentiator": 25,
        "Qualifications": 20,
        "Specific parameters / KPIs": 15,
        "Competencies 1": 10,
        "Competencies 2": 10,
        "Competencies 3": 10,
        "Job Profile Description": 5,
        "Role Description": 3,
        "Career Band Description": 2,
    }

    total = 0
    for col, w in weights.items():
        text = job_profile_row.get(col, "")
        kw = extract_keywords(text)

        overlap = len(user_tags.intersection(kw))
        total += overlap * w

    return total


# ==========================================================
# FORM QUESTIONS → TAG GENERATOR
# ==========================================================

st.subheader("Informações do cargo")

col1, col2 = st.columns(2)

with col1:
    family = st.selectbox("Job Family", sorted(df["Job Family"].dropna().unique()))

with col2:
    sublist = df[df["Job Family"] == family]["Sub Job Family"].dropna().unique()
    subfamily = st.selectbox("Sub Job Family", sorted(sublist))

flt = df[(df["Job Family"] == family) & (df["Sub Job Family"] == subfamily)]

if flt.empty:
    st.stop()

# ------------------------------
# PERGUNTAS (GENÉRICAS + DECISIVAS)
# ------------------------------

st.markdown("### Características da função")

# Autonomia
aut = st.radio("Nível de autonomia do cargo:",
               ["Baixa", "Moderada", "Alta"])

# Impacto
impact = st.radio("Impacto das decisões:",
                  ["Local", "Área/Unidade", "Organizacional/Global"])

# Complexidade do trabalho
complexity = st.radio("Complexidade do trabalho:",
                      ["Rotineiro", "Moderado", "Complexo"])

# Experiência
exp = st.radio("Nível de experiência típico:",
               ["Até 3 anos", "3-7 anos", "7-12 anos", "12+ anos"])

# Educação
edu = st.radio("Nível educacional típico:",
               ["Ensino Médio", "Técnico", "Graduação", "Pós/Especialização", "Mestrado/Doutorado"])

# Tipo de KPIs
kpi = st.multiselect(
    "Quais tipos de KPIs esse cargo acompanha?",
    ["Financeiros", "Clientes", "Operacionais", "Processos", "Projetos", "Segurança"]
)

# Competências comportamentais
comp = st.multiselect(
    "Competências comportamentais chave:",
    ["Trabalho em equipe", "Comunicação", "Influência", "Análise", "Orientação a resultados", "Inovação"]
)

# ----------------------------------------------------------
# BUILD USER TAGS
# ----------------------------------------------------------
user_tags = set()

# autonomia
if aut == "Alta": user_tags.update(["independent", "autonomy", "minimal", "self"])
if aut == "Moderada": user_tags.update(["guided", "partial"])
if aut == "Baixa": user_tags.update(["close supervision", "instructions"])

# impacto
if impact == "Local": user_tags.update(["local"])
if impact == "Área/Unidade": user_tags.update(["business unit", "cross functional"])
if impact == "Organizacional/Global": user_tags.update(["global", "enterprise"])

# complexidade
if complexity == "Complexo": user_tags.update(["complex", "advanced"])
if complexity == "Moderado": user_tags.update(["moderate"])
if complexity == "Rotineiro": user_tags.update(["routine"])

# educação
mapping_edu = {
    "Ensino Médio": ["basic"],
    "Técnico": ["technical"],
    "Graduação": ["degree", "bachelor"],
    "Pós/Especialização": ["specialist", "advanced"],
    "Mestrado/Doutorado": ["master", "doctorate", "phd"]
}
user_tags.update(mapping_edu.get(edu, []))

# experiência
mapping_exp = {
    "Até 3 anos": ["junior"],
    "3-7 anos": ["intermediate"],
    "7-12 anos": ["senior"],
    "12+ anos": ["expert", "leader"]
}
user_tags.update(mapping_exp.get(exp, []))

# KPIs
for k in kpi:
    user_tags.add(k.lower())

# competências
for c in comp:
    user_tags.add(c.lower())


# ==========================================================
# SCORE PROFILES
# ==========================================================
flt = flt.copy()
flt["score"] = flt.apply(lambda row: score_match(user_tags, row), axis=1)

best = flt.sort_values("score", ascending=False).iloc[0].to_dict()

st.success(f"Cargo identificado: **{best['Job Profile']}** — GG {best['Global Grade']}")

# ==========================================================
# RENDER FINAL DESCRIPTION (LAYOUT PREMIUM)
# ==========================================================
components.html(
    build_single_profile_html(best),
    height=900,
    scrolling=False
)
