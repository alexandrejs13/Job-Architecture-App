import streamlit as st
import pandas as pd
import html
import streamlit.components.v1 as components
import base64
import os

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="Job Match", layout="wide")

# ---------------------------------------------------------
# FIXED GLOBAL LAYOUT — prevents infinite stretch
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

    /* CARD BLOCK */
    .card-block {
        background: #f7f5f2;
        padding: 22px 26px;
        border-radius: 16px;
        border: 1px solid #e6e2dc;
        margin-bottom: 24px;
    }

    .card-title {
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 14px;
        color: #111;
    }

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# PAGE HEADER
# ---------------------------------------------------------
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


# ---------------------------------------------------------
# JOB FAMILY — BASIC FILTERS
# ---------------------------------------------------------
st.markdown("## Job Family Information")

col_f1, col_f2 = st.columns([1, 1])

with col_f1:
    job_family = st.selectbox(
        "Job Family",
        [
            "Corporate Affairs/Communications",
            "Finance",
            "HR",
            "IT",
            "Marketing",
            "Operations",
            "Engineering",
            "Sales"
        ]
    )

with col_f2:
    sub_job_family = st.selectbox(
        "Sub Job Family",
        [
            "General Communications",
            "Internal Communications",
            "External Communications",
            "Media Relations",
            "Brand & Content"
        ]
    )


# ==========================================================
# MAIN QUESTIONNAIRE — THREE CARDS
# ==========================================================

st.write("")  # small spacer

cA, cB, cC = st.columns([1, 1, 1])


# ---------------------------------------------------------
# CARD 1 – Strategic Impact & Scope  (FIX: title inside card)
# ---------------------------------------------------------
with cA:
    st.markdown('<div class="card-block">', unsafe_allow_html=True)

    st.markdown('<div class="card-title">Strategic Impact & Scope</div>', unsafe_allow_html=True)

    job_category = st.selectbox(
        "Job Category *",
        ["Executive", "Manager", "Professional", "Technical Support", "Business Support", "Production"]
    )

    geo_scope = st.selectbox(
        "Geographic Scope *",
        ["Local", "Regional", "Multi-country", "Global"]
    )

    org_impact = st.selectbox(
        "Organizational Impact *",
        [
            "Team",
            "Department / Subfunction",
            "Function",
            "Multi-function / Business Unit",
            "Enterprise-wide"
        ]
    )

    span_control = st.selectbox(
        "Span of Control *",
        [
            "No direct reports",
            "Individual contributor with influence",
            "Supervises technicians/operators",
            "Leads professionals",
            "Leads multiple teams",
            "Leads managers",
            "Leads multi-layer organization"
        ]
    )

    st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# CARD 2 – Autonomy & Complexity (title inside)
# ---------------------------------------------------------
with cB:
    st.markdown('<div class="card-block">', unsafe_allow_html=True)

    st.markdown('<div class="card-title">Autonomy & Complexity</div>', unsafe_allow_html=True)

    autonomy = st.selectbox(
        "Autonomy Level *",
        [
            "Works under close supervision",
            "Works under regular guidance",
            "Works independently",
            "Sets direction for others",
            "Defines organizational strategy"
        ]
    )

    problem_solving = st.selectbox(
        "Problem Solving Complexity *",
        [
            "Routine / Standardized",
            "Moderate analysis",
            "Complex analysis",
            "Novel / ambiguous problems",
            "Strategic, organization-changing problems"
        ]
    )

    knowledge_depth = st.selectbox(
        "Knowledge Depth *",
        [
            "Basic / Entry-level knowledge",
            "Applied technical / professional knowledge",
            "Advanced specialized expertise",
            "Recognized expert",
            "World-class mastery / thought leader"
        ]
    )

    influence = st.selectbox(
        "Influence Level *",
        [
            "Internal team only",
            "Internal cross-team",
            "Internal multi-function",
            "External vendors/clients",
            "Influences industry-level practices"
        ]
    )

    st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# CARD 3 – Knowledge, KPIs & Competencies (title inside)
# ---------------------------------------------------------
with cC:
    st.markdown('<div class="card-block">', unsafe_allow_html=True)

    st.markdown('<div class="card-title">Knowledge, KPIs & Competencies</div>', unsafe_allow_html=True)

    education = st.selectbox(
        "Education Level *",
        [
            "High School",
            "Technical Degree",
            "Bachelor’s",
            "Post-graduate / Specialization",
            "Master’s",
            "Doctorate"
        ]
    )

    experience = st.selectbox(
        "Experience Level *",
        [
            "< 2 years",
            "2–5 years",
            "5–10 years",
            "10–15 years",
            "15+ years"
        ]
    )

    kpis = st.multiselect(
        "Primary KPIs * (select ≥1)",
        [
            "Financial",
            "Customer",
            "Operational",
            "Quality",
            "Safety",
            "Compliance",
            "Project Delivery",
            "People Leadership"
        ]
    )

    competencies = st.multiselect(
        "Core Competencies * (select ≥1)",
        [
            "Communication",
            "Collaboration",
            "Analytical Thinking",
            "Technical Expertise",
            "Leadership",
            "Innovation",
            "Strategic Thinking",
            "Customer Orientation"
        ]
    )

    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================================
# BUTTON
# ==========================================================
generate = st.button("Generate Job Match Description")

if generate:
    st.success("Job Match Description generated successfully!")
