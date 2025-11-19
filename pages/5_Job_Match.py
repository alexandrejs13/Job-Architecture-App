import streamlit as st
import html
import base64
import os
import streamlit.components.v1 as components

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="Job Match Description", layout="wide")

# ---------------------------------------------------------
# LOAD PAGE ICON (PNG) AS BASE64
# ---------------------------------------------------------
def load_icon_png(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

page_icon_b64 = load_icon_png("assets/icons/business_review_clipboard.png")

# ---------------------------------------------------------
# HEADER — SIG STYLE
# ---------------------------------------------------------
st.markdown(f"""
<div style="display:flex; align-items:center; gap:18px; margin-bottom:6px; margin-top:10px;">
    <img src="data:image/png;base64,{page_icon_b64}" style="width:48px; height:48px;">
    <h1 style="font-size:36px; font-weight:700; margin:0; padding:0;">
        Job Match Description
    </h1>
</div>

<hr style="margin-top:14px; margin-bottom:36px;">
""", unsafe_allow_html=True)

st.markdown("### Job Match Generator (Advanced WTW Framework)")

# ---------------------------------------------------------
# GLOBAL LAYOUT — EXATAMENTE IGUAL AO JOB PROFILE DESCRIPTION
# ---------------------------------------------------------
st.markdown("""
<style>

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

/* Botão azul SIG */
div.stButton > button {
    background-color: #145efc !important;
    color: white !important;
    border-radius: 8px !important;
    height: 46px !important;
    font-size: 17px !important;
    font-weight: 600 !important;
    border: none !important;
}
div.stButton > button:hover {
    background-color: #0f4ad6 !important;
}

/* Títulos dos cards */
.section-header {
    font-size: 20px !important;
    font-weight: 700 !important;
    margin: 0 0 10px 0 !important;
    padding: 0 !important;
    height: 30px;
    display: flex;
    align-items: center;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# LOAD SVG ICONS — IGUAIS AO JOB PROFILE DESCRIPTION
# ---------------------------------------------------------
def load_svg(svg_name):
    path = f"assets/icons/sig/{svg_name}"
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

icons_svg = {
    "Job Scope & Impact": load_svg("Hierarchy.svg"),
    "Knowledge & Expertise": load_svg("Content_Book_Phone.svg"),
    "Leadership & Influence": load_svg("Setting_Cog.svg"),
}

# ---------------------------------------------------------
# JOB FAMILY + SUB JOB FAMILY (DINÂMICO)
# ---------------------------------------------------------
# Você deve carregar isso do seu arquivo real:
job_family_dict = {
    "Corporate Affairs/Communications": [
        "General Communications", "Internal Communications", "External Communications", 
        "Media Relations", "Brand & Content"
    ],
    "Finance": ["Accounting", "Controlling", "Tax", "Treasury"],
    "HR": ["HR Operations", "Compensation", "Talent Management", "Recruitment"],
    "IT": ["Infrastructure", "Applications", "Cybersecurity", "Data & Analytics"],
    "Marketing": ["Brand", "Performance", "Digital"],
    "Operations": ["Supply Chain", "Manufacturing", "Maintenance"],
    "Engineering": ["Civil", "Mechanical", "Electrical"],
    "Sales": ["B2B", "B2C", "Channel Partners"]
}


st.markdown("## Job Family Information")

col1, col2 = st.columns(2)

with col1:
    job_family = st.selectbox(
        "Job Family",
        ["Choose option"] + list(job_family_dict.keys())
    )

with col2:
    sub_job_family = st.selectbox(
        "Sub Job Family",
        ["Choose option"] if job_family == "Choose option"
        else ["Choose option"] + job_family_dict[job_family]
    )

# ---------------------------------------------------------
# FORMULÁRIO — 3 GRANDES SEÇÕES (MODELO WTW)
# ---------------------------------------------------------

# ========== SECTION 1: JOB SCOPE & IMPACT ==========
st.markdown("### Job Scope & Impact")
with st.container():
    colA, colB, colC = st.columns(3)

    with colA:
        work_nature = st.selectbox(
            "Natureza do Trabalho",
            ["Choose option", "Process-oriented", "Project-oriented", "Client-oriented",
             "Operations", "Strategy", "Innovation", "Governance"]
        )

        decision_type = st.selectbox(
            "Tipo de Decisão",
            ["Choose option", "Procedural", "Operational", "Analytical", "Financial",
             "Regulatory", "Strategic"]
        )

    with colB:
        financial_impact = st.selectbox(
            "Impacto Financeiro",
            ["Choose option", "No impact", "Cost control", "Budget owner",
             "Revenue influence", "P&L responsibility"]
        )

        stakeholder_complexity = st.selectbox(
            "Complexidade de Stakeholders",
            ["Choose option", "Internal team", "Cross-functional", "Business Unit",
             "Regional", "Global", "Clients", "Regulators", "Board"]
        )

    with colC:
        functional_breadth = st.selectbox(
            "Escopo Funcional",
            ["Choose option", "Single process", "Sub-function", "Function",
             "Multi-function", "Business Unit", "Company-wide", "Global"]
        )

        time_horizon = st.selectbox(
            "Horizonte Temporal das Decisões",
            ["Choose option", "Daily", "Weekly", "Monthly", "Quarterly",
             "Annually", "3 Years", "5+ Years"]
        )

# ========== SECTION 2: KNOWLEDGE & EXPERTISE ==========
st.markdown("### Knowledge & Expertise")
with st.container():
    colD, colE, colF = st.columns(3)

    with colD:
        specialization_level = st.selectbox(
            "Nível de Especialização",
            ["Choose option", "Generalist", "Functional specialist", "Technical expert",
             "Market-recognized expert", "Global authority"]
        )

    with colE:
        analytical_complexity = st.selectbox(
            "Complexidade Analítica",
            ["Choose option", "Basic", "Moderate", "Advanced", "Ambiguous", "Transformational"]
        )

    with colF:
        innovation_scale = st.selectbox(
            "Responsabilidade por Inovação / Mudança",
            ["Choose option", "Execution", "Improvement", "Recreation", "Transformation", "Disruption"]
        )

# ========== SECTION 3: LEADERSHIP & INFLUENCE ==========
st.markdown("### Leadership & Influence")
with st.container():
    colG, colH = st.columns(2)

    with colG:
        leadership_type = st.selectbox(
            "Tipo de Liderança",
            ["Choose option", "None", "Technical leadership", "Project leadership",
             "Direct people management", "Matrix leadership", "Global leadership"]
        )

    with colH:
        influence_level = st.selectbox(
            "Influência Organizacional",
            ["Choose option", "Team", "Department", "Function", "BU", "Company-wide", "Industry"]
        )

# ---------------------------------------------------------
# VALIDAÇÃO OBRIGATÓRIA
# ---------------------------------------------------------
all_fields = [
    job_family, sub_job_family,
    work_nature, decision_type, financial_impact,
    stakeholder_complexity, functional_breadth, time_horizon,
    specialization_level, analytical_complexity, innovation_scale,
    leadership_type, influence_level
]

missing = any(x == "Choose option" for x in all_fields)

# ---------------------------------------------------------
# BOTÃO — alinhado à esquerda
# ---------------------------------------------------------
btn_col = st.columns([1,5])[0]
generate = btn_col.button("Generate Job Match Description", use_container_width=False)

# ---------------------------------------------------------
# BLOQUEIA SE TIVER CAMPO FALTANDO
# ---------------------------------------------------------
if generate and missing:
    st.error("Please complete all fields before generating the Job Match Description.")
    st.stop()

# ---------------------------------------------------------
# HTML FINAL — IGUAL AO JOB PROFILE DESCRIPTION, 1 COLUNA
# ---------------------------------------------------------
def build_html():

    return f"""
<html>
<head>
<meta charset='UTF-8'>

<style>
html, body {{
    margin:0;
    padding:0;
    font-family:'Segoe UI',sans-serif;
    background:#faf9f7;
}}
#viewport {{
    height:100vh;
    display:flex;
    flex-direction:column;
    overflow:hidden;
}}
.grid-top {{
    display:grid;
    grid-template-columns:1fr;
    gap:24px;
    width:100%;
}}
.grid-desc {{
    display:grid;
    grid-template-columns:1fr;
    gap:28px;
    width:100%;
}}
.card-top {{
    background:#f5f3ee;
    border-radius:16px;
    padding:22px 24px;
    border:1px solid #e3e1dd;
}}
.title {{
    font-size:20px;
    font-weight:700;
}}
.gg {{
    color:#145efc;
    font-size:16px;
    font-weight:700;
    margin-top:6px;
}}
.meta {{
    background:white;
    padding:14px;
    margin-top:14px;
    border-radius:12px;
    box-shadow:0 2px 8px rgba(0,0,0,0.06);
    font-size:14px;
}}
.section-box {{
    padding-bottom:28px;
}}
.section-title {{
    font-size:16px;
    font-weight:700;
    display:flex;
    align-items:center;
    gap:6px;
}}
.section-line {{
    height:1px;
    background:#e8e6e1;
    width:100%;
    margin:8px 0 14px 0;
}}
.section-text {{
    font-size:14px;
    line-height:1.45;
    white-space:pre-wrap;
}}
.icon-inline {{
    width:20px;
    height:20px;
}}
#scroll-area {{
    flex:1;
    overflow-y:auto;
    padding:20px 4px 32px 4px;
}}
</style>

</head>
<body>

<div id="viewport">

    <div id="top-area">
        <div class="grid-top">
            <div class="card-top">
                <div class="title">Job Match – Advanced WTW Framework</div>
                <div class="gg">GG TBD</div>

                <div class="meta">
                    <b>Job Family:</b> {html.escape(job_family)}<br>
                    <b>Sub Job Family:</b> {html.escape(sub_job_family)}<br>
                </div>
            </div>
        </div>
    </div>

    <div id="scroll-area">
        <div class="grid-desc">

            <!-- SECTION 1 -->
            <div class="section-box">
                <div class="section-title">
                    <span class="icon-inline">{icons_svg["Job Scope & Impact"]}</span>
                    Job Scope & Impact
                </div>
                <div class='section-line'></div>
                <div class='section-text'>
<b>Natureza do Trabalho:</b> {work_nature}
<b>Tipo de Decisão:</b> {decision_type}
<b>Impacto Financeiro:</b> {financial_impact}
<b>Complexidade de Stakeholders:</b> {stakeholder_complexity}
<b>Escopo Funcional:</b> {functional_breadth}
<b>Horizonte Temporal:</b> {time_horizon}
                </div>
            </div>

            <!-- SECTION 2 -->
            <div class="section-box">
                <div class="section-title">
                    <span class="icon-inline">{icons_svg["Knowledge & Expertise"]}</span>
                    Knowledge & Expertise
                </div>
                <div class='section-line'></div>
                <div class='section-text'>
<b>Nível de Especialização:</b> {specialization_level}
<b>Complexidade Analítica:</b> {analytical_complexity}
<b>Responsabilidade por Mudança/Inovação:</b> {innovation_scale}
                </div>
            </div>

            <!-- SECTION 3 -->
            <div class="section-box">
                <div class="section-title">
                    <span class="icon-inline">{icons_svg["Leadership & Influence"]}</span>
                    Leadership & Influence
                </div>
                <div class='section-line'></div>
                <div class='section-text'>
<b>Tipo de Liderança:</b> {leadership_type}
<b>Influência Organizacional:</b> {influence_level}
                </div>
            </div>

        </div>
    </div>

</div>

</body>
</html>
"""


# ---------------------------------------------------------
# RENDER HTML
# ---------------------------------------------------------
if generate:
    components.html(build_html(), height=1400, scrolling=True)
