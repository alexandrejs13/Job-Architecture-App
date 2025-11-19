# pages/5_Job_Match.py
# ==========================================================
# JOB MATCH — ARQUITETURA PRO (UI + VALIDAÇÃO + CHAMADAS)
# ==========================================================
import os
import base64
import html

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from match_engine import compute_job_match
from html_renderer import render_job_description


# ----------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------
st.set_page_config(page_title="Job Match", layout="wide")


# ----------------------------------------------------------
# CSS GLOBAL — LAYOUT + BOTÃO + ERROS
# ----------------------------------------------------------
st.markdown(
    """
<style>
/* Layout centralizado, igual outras páginas */
.main > div {
    max-width: 1400px;
    margin-left: auto;
    margin-right: auto;
    padding-left: 20px;
    padding-right: 20px;
}
.block-container, .stColumn {
    max-width: 1400px !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* Títulos de seção do formulário */
.section-title-form {
    font-size: 20px;
    font-weight: 700;
    margin-top: 24px;
    margin-bottom: 6px;
}
.section-divider {
    height: 1px;
    width: 100%;
    background: #e0ddd6;
    margin: 6px 0 18px 0;
}

/* Label dos campos */
.field-label {
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 4px;
    color: #000000;
}
.field-label.error {
    color: #d32f2f;
}

/* Wrapper para aplicar borda vermelha nos selects/multiselects */
.field-wrapper {
    margin-bottom: 10px;
}
.field-wrapper.error div[data-baseweb="select"] {
    border-color: #d32f2f !important;
    box-shadow: 0 0 0 1px #d32f2f33;
}

/* Botão azul — largura do texto, alinhado à esquerda */
div.stButton > button {
    background-color: #145efc !important;
    color: #ffffff !important;
    border-radius: 10px !important;
    border: none !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    padding: 8px 30px !important;   /* garante espaço pro texto */
    white-space: nowrap !important; /* não quebra linha */
    width: auto !important;         /* não esticar full-width */
}
div.stButton > button:hover {
    background-color: #0f4ad6 !important;
}
</style>
""",
    unsafe_allow_html=True,
)


# ----------------------------------------------------------
# HEADER ICON
# ----------------------------------------------------------
def load_icon_png(path: str) -> str:
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


page_icon_b64 = load_icon_png("assets/icons/checkmark_success.png")

st.markdown(
    f"""
<div style="display:flex; align-items:center; gap:18px; margin-top:10px; margin-bottom:8px;">
    <img src="data:image/png;base64,{page_icon_b64}" style="width:48px; height:48px;">
    <h1 style="font-size:36px; font-weight:700; margin:0; padding:0;">
        Job Match
    </h1>
</div>
<hr style="margin-top:14px; margin-bottom:32px;">
""",
    unsafe_allow_html=True,
)


# ----------------------------------------------------------
# LOAD JOB PROFILE DATA (colunas ORIGINAIS)
# ----------------------------------------------------------
@st.cache_data
def load_job_profiles() -> pd.DataFrame:
    df = pd.read_excel("data/Job Profile.xlsx").fillna("")
    return df


df_profiles = load_job_profiles()


# ----------------------------------------------------------
# STATE — CAMPOS COM ERRO
# ----------------------------------------------------------
if "missing_fields" not in st.session_state:
    st.session_state.missing_fields = set()


# ----------------------------------------------------------
# HELPERS – CAMPOS COM LABEL DINÂMICO
# ----------------------------------------------------------
def select_with_error(label: str, options, key: str):
    has_error = key in st.session_state.missing_fields
    label_class = "field-label error" if has_error else "field-label"

    # título da caixa (fica vermelho se erro)
    st.markdown(
        f'<div class="{label_class}">{html.escape(label)}</div>',
        unsafe_allow_html=True,
    )

    # wrapper para borda vermelha
    wrapper_class = "field-wrapper error" if has_error else "field-wrapper"
    st.markdown(f'<div class="{wrapper_class}">', unsafe_allow_html=True)

    # label "." para evitar warning de label vazio
    value = st.selectbox(
        ".",
        options,
        key=key,
        label_visibility="collapsed",
    )

    st.markdown("</div>", unsafe_allow_html=True)
    return value


def multiselect_with_error(label: str, options, key: str):
    has_error = key in st.session_state.missing_fields
    label_class = "field-label error" if has_error else "field-label"

    st.markdown(
        f'<div class="{label_class}">{html.escape(label)}</div>',
        unsafe_allow_html=True,
    )

    wrapper_class = "field-wrapper error" if has_error else "field-wrapper"
    st.markdown(f'<div class="{wrapper_class}">', unsafe_allow_html=True)

    value = st.multiselect(
        ".",
        options,
        key=key,
        label_visibility="collapsed",
    )

    st.markdown("</div>", unsafe_allow_html=True)
    return value


# ==========================================================
# FORMULÁRIO — MESMA ESTRUTURA DA VERSÃO UNIFICADA
# ==========================================================

# ------------- Job Family Information -------------
st.markdown(
    '<div class="section-title-form">Job Family Information</div>'
    '<div class="section-divider"></div>',
    unsafe_allow_html=True,
)

col_jf1, col_jf2 = st.columns(2)

job_families = sorted(df_profiles["Job Family"].dropna().unique().tolist())

with col_jf1:
    job_family = select_with_error(
        "Job Family",
        ["Choose option"] + job_families,
        key="job_family",
    )

with col_jf2:
    if job_family == "Choose option":
        sub_options = []
    else:
        sub_options = (
            df_profiles[df_profiles["Job Family"] == job_family]["Sub Job Family"]
            .dropna()
            .unique()
            .tolist()
        )

    sub_job_family = select_with_error(
        "Sub Job Family",
        ["Choose option"] + sorted(sub_options),
        key="sub_job_family",
    )

# ------------- Strategic Impact & Scope -------------
st.markdown(
    '<div class="section-title-form">Strategic Impact & Scope</div>'
    '<div class="section-divider"></div>',
    unsafe_allow_html=True,
)

c1a, c1b, c1c = st.columns(3)

with c1a:
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

with c1b:
    span_control = select_with_error(
        "Span of Control",
        [
            "Choose option",
            "No direct reports",
            "Supervises team",
            "Leads professionals",
            "Leads multiple teams",
            "Leads managers",
        ],
        key="span_control",
    )

    nature_work = select_with_error(
        "Nature of Work",
        [
            "Choose option",
            "Process-oriented",
            "Analysis-oriented",
            "Specialist",
            "Leadership-driven",
        ],
        key="nature_work",
    )

    financial_impact = select_with_error(
        "Financial Impact",
        [
            "Choose option",
            "No impact",
            "Cost center impact",
            "Department-level impact",
            "Business Unit impact",
            "Company-wide impact",
        ],
        key="financial_impact",
    )

with c1c:
    stakeholder_complexity = select_with_error(
        "Stakeholder Complexity",
        [
            "Choose option",
            "Internal team",
            "Cross-functional",
            "External vendors",
            "Customers",
            "Regulatory/Authorities",
        ],
        key="stakeholder_complexity",
    )

    decision_type = select_with_error(
        "Decision Type",
        ["Choose option", "Procedural", "Operational", "Tactical", "Strategic"],
        key="decision_type",
    )

    decision_horizon = select_with_error(
        "Decision Time Horizon",
        ["Choose option", "Daily", "Weekly", "Monthly", "Annual", "Multi-year"],
        key="decision_horizon",
    )

# ------------- Autonomy & Complexity -------------
st.markdown(
    '<div class="section-title-form">Autonomy & Complexity</div>'
    '<div class="section-divider"></div>',
    unsafe_allow_html=True,
)

c2a, c2b, c2c = st.columns(3)

with c2a:
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

    problem_solving = select_with_error(
        "Problem Solving Complexity",
        [
            "Choose option",
            "Routine/Standardized",
            "Moderate",
            "Complex",
            "Ambiguous/Novel",
            "Organization-level",
        ],
        key="problem_solving",
    )

with c2b:
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

with c2c:
    influence_level = select_with_error(
        "Influence Level",
        [
            "Choose option",
            "Team",
            "Cross-team",
            "Multi-function",
            "External vendors/clients",
            "Industry-level influence",
        ],
        key="influence_level",
    )

# ------------- Knowledge, KPIs & Competencies -------------
st.markdown(
    '<div class="section-title-form">Knowledge, KPIs & Competencies</div>'
    '<div class="section-divider"></div>',
    unsafe_allow_html=True,
)

c3a, c3b, c3c = st.columns(3)

with c3a:
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

with c3b:
    kpis_selected = multiselect_with_error(
        "Primary KPIs",
        [
            "Financial",
            "Customer",
            "Operational",
            "Quality",
            "Safety",
            "Compliance",
            "Project Delivery",
            "People Leadership",
        ],
        key="kpis_selected",
    )

    specialization_level = select_with_error(
        "Specialization Level",
        ["Choose option", "Generalist", "Specialist", "Deep Specialist"],
        key="specialization_level",
    )

with c3c:
    competencies_selected = multiselect_with_error(
        "Core Competencies",
        [
            "Communication",
            "Collaboration",
            "Analytical Thinking",
            "Technical Expertise",
            "Leadership",
            "Innovation",
            "Strategic Thinking",
            "Customer Orientation",
        ],
        key="competencies_selected",
    )

    innovation_resp = select_with_error(
        "Innovation Responsibility",
        [
            "Choose option",
            "Execution",
            "Incremental improvements",
            "Major improvements",
            "Innovation leadership",
        ],
        key="innovation_resp",
    )

c3d, c3e = st.columns(2)

with c3d:
    leadership_type = select_with_error(
        "Leadership Type",
        ["Choose option", "None", "Team Lead", "Supervisor", "Manager", "Senior Manager", "Director"],
        key="leadership_type",
    )

with c3e:
    org_influence = select_with_error(
        "Organizational Influence",
        ["Choose option", "Team", "Department", "Business Unit", "Function", "Enterprise-wide"],
        key="org_influence",
    )


# ----------------------------------------------------------
# BOTÃO GERAR — ALINHADO ESQUERDA (1ª COLUNA)
# ----------------------------------------------------------
btn_col, _, _ = st.columns([1, 5, 1])
with btn_col:
    generate = st.button("Generate Job Match Description", key="generate_match")


# ==========================================================
# VALIDAÇÃO + CHAMADA AO MOTOR DE MATCH
# ==========================================================
if generate:
    # montando dicionário de valores
    form_values = {
        "job_family": job_family,
        "sub_job_family": sub_job_family,
        "job_category": job_category,
        "geo_scope": geo_scope,
        "org_impact": org_impact,
        "span_control": span_control,
        "nature_work": nature_work,
        "financial_impact": financial_impact,
        "stakeholder_complexity": stakeholder_complexity,
        "decision_type": decision_type,
        "decision_horizon": decision_horizon,
        "autonomy": autonomy,
        "problem_solving": problem_solving,
        "knowledge_depth": knowledge_depth,
        "operational_complexity": operational_complexity,
        "influence_level": influence_level,
        "education": education,
        "experience": experience,
        "specialization_level": specialization_level,
        "innovation_resp": innovation_resp,
        "leadership_type": leadership_type,
        "org_influence": org_influence,
        "kpis_selected": kpis_selected,
        "competencies_selected": competencies_selected,
    }

    # identifica campos obrigatórios faltantes
    missing_keys = set()
    # selects
    select_keys = [
        "job_family",
        "sub_job_family",
        "job_category",
        "geo_scope",
        "org_impact",
        "span_control",
        "nature_work",
        "financial_impact",
        "stakeholder_complexity",
        "decision_type",
        "decision_horizon",
        "autonomy",
        "problem_solving",
        "knowledge_depth",
        "operational_complexity",
        "influence_level",
        "education",
        "experience",
        "specialization_level",
        "innovation_resp",
        "leadership_type",
        "org_influence",
    ]
    for k in select_keys:
        if form_values[k] == "Choose option" or form_values[k] == "":
            missing_keys.add(k)

    # multiselects obrigatórios
    if len(kpis_selected) == 0:
        missing_keys.add("kpis_selected")
    if len(competencies_selected) == 0:
        missing_keys.add("competencies_selected")

    st.session_state.missing_fields = missing_keys

    if missing_keys:
        # não mostra lista de erros; os campos em vermelho já indicam o que falta
        st.stop()

    # se passou, limpa flags
    st.session_state.missing_fields = set()

    # chama motor de match
    best = compute_job_match(form_values, df_profiles)

    if not best:
        st.error("No Job Profiles match the selected Job Family + Sub Job Family.")
    else:
        row = best["row"]
        score_pct = best["score_pct"]

        html_desc = render_job_description(row, score_pct)

        # descrição única, sem scroll interno, fundo branco (controlado no HTML)
        components.html(html_desc, height=1000, scrolling=False)
