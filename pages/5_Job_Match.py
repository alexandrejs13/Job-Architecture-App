import streamlit as st
import pandas as pd
import html
import streamlit.components.v1 as components
import base64
import os

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(page_title="Job Match", layout="wide")

# ==========================================================
# GLOBAL CSS (layout + botão + estados de erro)
# ==========================================================
st.markdown(
    """
<style>
/* ====== LAYOUT GERAL (igual às demais páginas) ====== */
.main > div {
    max-width: 1400px;
    margin-left: auto;
    margin-right: auto;
    padding-left: 20px;
    padding-right: 20px;
}
.stDataFrame {
    max-width: 1400px;
    margin-left: auto;
    margin-right: auto;
}
.block-container, .stColumn {
    max-width: 1400px !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* ====== TÍTULOS DE SEÇÃO DO FORM ====== */
.section-title-form {
    font-size: 20px;
    font-weight: 700;
    margin-top: 24px;
    margin-bottom: 6px;
}
.section-divider {
    height: 1px;
    background: #e4e1dc;
    margin-bottom: 18px;
}

/* ====== LABELS DOS CAMPOS ====== */
.field-label {
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 4px;
}
.field-label.error {
    color: #d32f2f;
}

/* wrapper pra conseguir pintar a borda do select em vermelho */
.field-wrapper.error div[data-baseweb="select"] {
    border-color: #d32f2f !important;
    box-shadow: 0 0 0 1px #d32f2f33;
}

/* ====== BOTÃO AZUL, UMA LINHA, ALINHADO ESQUERDA ====== */
.stButton > button {
    background: #145efc !important;
    color: #ffffff !important;
    border-radius: 12px !important;
    border: none !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    padding: 8px 26px !important;
    white-space: nowrap !important;   /* não quebra linha */
    width: auto !important;           /* largura só do texto */
}

/* ====== HTML DA DESCRIÇÃO (mesmo padrão Job Profile) ====== */
html, body {
    margin: 0;
    padding: 0;
}
.jobmatch-viewport {
    font-family: 'Segoe UI', sans-serif;
    background: #ffffff;
}
.jobmatch-card-top {
    background: #f5f3ee;
    border-radius: 16px;
    padding: 22px 24px;
    border: 1px solid #e3e1dd;
}
.jobmatch-title {
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 4px;
}
.jobmatch-gg {
    color: #145efc;
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 10px;
}
.jobmatch-meta {
    background: #ffffff;
    padding: 14px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    font-size: 14px;
}

/* seções */
.jobmatch-section-box {
    margin-top: 28px;
}
.jobmatch-section-title {
    font-size: 18px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 8px;
}
.jobmatch-section-line {
    height: 1px;
    background: #e8e6e1;
    width: 100%;
    margin: 8px 0 14px 0;
}
.jobmatch-section-text {
    font-size: 14px;
    line-height: 1.45;
    white-space: pre-wrap;
}
.jobmatch-icon-inline {
    width: 24px;
    height: 24px;
}
</style>
""",
    unsafe_allow_html=True,
)

# ==========================================================
# HELPERS – LOAD ICONS / DATA
# ==========================================================
def load_icon_png(path: str) -> str:
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except FileNotFoundError:
        return ""

def load_svg(path: str) -> str:
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# header icon (checkmark)
page_icon_b64 = load_icon_png("assets/icons/checkmark_success.png")

# ==========================================================
# HEADER
# ==========================================================
st.markdown(
    f"""
<div style="display:flex; align-items:center; gap:18px; margin-top:12px;">
    <img src="data:image/png;base64,{page_icon_b64}" style="width:56px; height:56px;">
    <h1 style="font-size:36px; font-weight:700; margin:0; padding:0;">
        Job Match
    </h1>
</div>
<hr style="margin-top:14px; margin-bottom:26px;">
""",
    unsafe_allow_html=True,
)

# ==========================================================
# LOAD JOB PROFILE DATA
# ==========================================================
@st.cache_data
def load_profiles():
    # caminho relativo dentro do app
    df = pd.read_excel("data/Job Profile.xlsx").fillna("")
    return df

df = load_profiles()

# ==========================================================
# SVG ICONS PARA A DESCRIÇÃO
# ==========================================================
icons_svg = {
    "Sub Job Family Description": load_svg("assets/icons/sig/Hierarchy.svg"),
    "Job Profile Description": load_svg("assets/icons/sig/Content_Book_Phone.svg"),
    "Career Band Description": load_svg("assets/icons/sig/File_Clipboard_Text.svg"),
    "Role Description": load_svg("assets/icons/sig/Shopping_Business_Target.svg"),
    "Grade Differentiator": load_svg("assets/icons/sig/User_Add.svg"),
    "Qualifications": load_svg("assets/icons/sig/Edit_Pencil.svg"),
    "Specific parameters / KPIs": load_svg("assets/icons/sig/Graph_Bar.svg"),
    "Competencies 1": load_svg("assets/icons/sig/Setting_Cog.svg"),
    "Competencies 2": load_svg("assets/icons/sig/Setting_Cog.svg"),
    "Competencies 3": load_svg("assets/icons/sig/Setting_Cog.svg"),
}

sections_order = [
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
# STATE: CAMPOS OBRIGATÓRIOS COM ERRO
# ==========================================================
if "missing_fields" not in st.session_state:
    st.session_state.missing_fields = set()

# ==========================================================
# FUNÇÃO PARA DESENHAR CADA CAMPO COM LABEL DINÂMICO
# ==========================================================
def select_with_error(label: str, options, key: str):
    has_error = key in st.session_state.missing_fields
    label_class = "field-label error" if has_error else "field-label"

    st.markdown(
        f'<div class="{label_class}">{html.escape(label)}</div>',
        unsafe_allow_html=True,
    )

    if has_error:
        st.markdown('<div class="field-wrapper error">', unsafe_allow_html=True)
    else:
        st.markdown('<div class="field-wrapper">', unsafe_allow_html=True)

    value = st.selectbox("", options, key=key, label_visibility="collapsed")

    st.markdown("</div>", unsafe_allow_html=True)

    return value

# ==========================================================
# FORMULÁRIO
# ==========================================================
# ---------- Job Family Information ----------
st.markdown('<div class="section-title-form">Job Family Information</div>', unsafe_allow_html=True)
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

col_jf1, col_jf2 = st.columns(2)

job_families = sorted(df["Job Family"].unique().tolist())

with col_jf1:
    job_family = select_with_error(
        "Job Family",
        ["Choose option"] + job_families,
        key="job_family",
    )

with col_jf2:
    if job_family == "Choose option":
        sub_list = []
    else:
        sub_list = (
            df[df["Job Family"] == job_family]["Sub Job Family"]
            .unique()
            .tolist()
        )
    sub_job_family = select_with_error(
        "Sub Job Family",
        ["Choose option"] + sorted(sub_list),
        key="sub_job_family",
    )

# ---------- Strategic Impact & Scope ----------
st.markdown('<div class="section-title-form">Strategic Impact & Scope</div>', unsafe_allow_html=True)
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    job_category = select_with_error(
        "Job Category",
        [
            "Choose option",
            "Executive",
            "Manager",
            "Professional",
            "Technical Support",
            "Business Support",
            "Production",
        ],
        key="job_category",
    )

    geo_scope = select_with_error(
        "Geographic Scope",
        ["Choose option", "Local", "Regional", "Multi-country", "Global"],
        key="geo_scope",
    )

    org_impact = select_with_error(
        "Organizational Impact",
        [
            "Choose option",
            "Team",
            "Department / Subfunction",
            "Function",
            "Business Unit",
            "Enterprise-wide",
        ],
        key="org_impact",
    )

with c2:
    autonomy = select_with_error(
        "Autonomy Level",
        [
            "Choose option",
            "Close supervision",
            "Regular guidance",
            "Independent",
            "Sets direction for others",
            "Defines strategy",
        ],
        key="autonomy",
    )

    knowledge_depth = select_with_error(
        "Knowledge Depth",
        [
            "Choose option",
            "Entry-level knowledge",
            "Applied knowledge",
            "Advanced expertise",
            "Recognized expert",
            "Thought leader",
        ],
        key="knowledge_depth",
    )

    operational_complexity = select_with_error(
        "Operational Complexity",
        [
            "Choose option",
            "Stable operations",
            "Some variability",
            "Complex operations",
            "High-variability environment",
        ],
        key="operational_complexity",
    )

with c3:
    experience = select_with_error(
        "Experience Level",
        [
            "Choose option",
            "< 2 years",
            "2–5 years",
            "5–10 years",
            "10–15 years",
            "15+ years",
        ],
        key="experience",
    )

    education = select_with_error(
        "Education Level",
        [
            "Choose option",
            "High School",
            "Technical Degree",
            "Bachelor’s",
            "Post-graduate",
            "Master’s",
            "Doctorate",
        ],
        key="education",
    )

# ==========================================================
# BOTÃO GERAR – ALINHADO À ESQUERDA
# ==========================================================
btn_col, _, _ = st.columns([1, 5, 1])
with btn_col:
    generate = st.button("Generate Job Match Description", key="generate_match")

# ==========================================================
# LÓGICA DE VALIDAÇÃO + CÁLCULO DO MATCH
# ==========================================================
match_profile = None
match_score = None

if generate:
    # verifica campos obrigatórios
    values = {
        "job_family": job_family,
        "sub_job_family": sub_job_family,
        "job_category": job_category,
        "geo_scope": geo_scope,
        "org_impact": org_impact,
        "autonomy": autonomy,
        "knowledge_depth": knowledge_depth,
        "operational_complexity": operational_complexity,
        "experience": experience,
        "education": education,
    }

    missing = {k for k, v in values.items() if v == "Choose option" or v == []}
    st.session_state.missing_fields = missing

    if missing:
        # não mostra banner gigantesco, só depende do vermelho nos campos
        st.stop()

    # ------- se passou na validação, limpa erros -------
    st.session_state.missing_fields = set()

    # ------- Match simples: dentro da mesma Job Family + Sub Job Family -------
    pool = df[
        (df["Job Family"] == job_family)
        & (df["Sub Job Family"] == sub_job_family)
    ].copy()

    if pool.empty:
        st.warning("No Job Profiles found for this Job Family / Sub Job Family.")
        st.stop()

    # mapeia experiência para um "GG alvo" aproximado
    exp_to_gg = {
        "< 2 years": 6,
        "2–5 years": 8,
        "5–10 years": 10,
        "10–15 years": 12,
        "15+ years": 14,
    }
    target_gg = exp_to_gg.get(experience, 10)

    pool["gg_num"] = pd.to_numeric(pool["Global Grade"], errors="coerce").fillna(
        target_gg
    )
    pool["gg_diff"] = (pool["gg_num"] - target_gg).abs()
    pool = pool.sort_values("gg_diff")

    match_profile = pool.iloc[0].to_dict()

    # score só pra ter um número simpático
    diff = float(pool.iloc[0]["gg_diff"])
    match_score = max(40, 100 - diff * 8)

# ==========================================================
# RENDERIZAÇÃO DA DESCRIÇÃO (UM PERFIL, UMA COLUNA)
# ==========================================================
if match_profile is not None:
    job = html.escape(str(match_profile.get("Job Profile", "")))
    gg = html.escape(str(match_profile.get("Global Grade", "")))
    jf = html.escape(str(match_profile.get("Job Family", "")))
    sf = html.escape(str(match_profile.get("Sub Job Family", "")))
    cp = html.escape(str(match_profile.get("Career Path", "")))
    fc = html.escape(str(match_profile.get("Full Job Code", "")))
    score_txt = f"{match_score:0.0f}%"

    html_desc = """
<div class="jobmatch-viewport">
  <div class="jobmatch-card-top">
    <div class="jobmatch-title">{job}</div>
    <div class="jobmatch-gg">GG {gg} • Match Score: {score}</div>
    <div class="jobmatch-meta">
      <b>Job Family:</b> {jf}<br>
      <b>Sub Job Family:</b> {sf}<br>
      <b>Career Path:</b> {cp}<br>
      <b>Full Job Code:</b> {fc}
    </div>
  </div>
""".format(
        job=job,
        gg=gg,
        score=html.escape(score_txt),
        jf=jf,
        sf=sf,
        cp=cp,
        fc=fc,
    )

    # seções na mesma ordem da página Job Profile Description
    for sec in sections_order:
        val = match_profile.get(sec, "")
        if val == "":
            continue

        icon_svg = icons_svg.get(sec, "")
        html_desc += """
  <div class="jobmatch-section-box">
    <div class="jobmatch-section-title">
      <span class="jobmatch-icon-inline">{icon}</span>
      {title}
    </div>
    <div class="jobmatch-section-line"></div>
    <div class="jobmatch-section-text">{text}</div>
  </div>
""".format(
            icon=icon_svg,
            title=html.escape(sec),
            text=html.escape(str(val)),
        )

    html_desc += "</div>"

    components.html(html_desc, height=900, scrolling=False)
