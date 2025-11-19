# ==========================================================
# 5_Job_Match.py — Página completa do Job Match
# ==========================================================

import streamlit as st
import pandas as pd
import base64
import os

from match_engine import compute_job_match
from html_renderer import render_job_description


# ----------------------------------------------------------
# CONFIG
# ----------------------------------------------------------
st.set_page_config(page_title="Job Match", layout="wide")


# ----------------------------------------------------------
# LOAD ICON
# ----------------------------------------------------------
def load_icon_png(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


icon_b64 = load_icon_png("assets/icons/checkmark_success.png")


# ----------------------------------------------------------
# HEADER PADRÃO SIG
# ----------------------------------------------------------
st.markdown(f"""
<div style="display:flex; align-items:center; gap:18px; margin-top:12px;">
    <img src="data:image/png;base64,{icon_b64}" style="width:56px; height:56px;">
    <h1 style="font-size:36px; font-weight:700; margin:0; padding:0;">
        Job Match
    </h1>
</div>
<hr style="margin-top:14px; margin-bottom:26px;">
""", unsafe_allow_html=True)


# ----------------------------------------------------------
# GLOBAL STYLE
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

    .error-title {
        color: #C62828 !important;
        font-weight: 700;
        margin-bottom: 3px;
    }

    .error-border {
        border: 2px solid #C62828 !important;
    }

    .generate-btn {
        background-color: #145efc;
        color: white !important;
        font-size: 20px;
        padding: 12px 26px;
        border-radius: 12px;
        border: none;
        cursor:pointer;
        font-weight:600;
    }

    .card {
        background: #f4f1ec;
        padding: 24px;
        border-radius: 20px;
        margin-bottom: 30px;
    }

    .job-title {
        font-size: 32px;
        font-weight: 800;
    }

    .gg {
        font-size: 20px;
        font-weight: 600;
        color: #145efc;
        margin-bottom: 14px;
    }

    .section-title {
        font-size: 22px;
        font-weight: 700;
        margin-top: 50px;
        margin-bottom: 12px;
        display:flex;
        gap:12px;
        align-items:center;
    }

    .section-text {
        font-size: 17px;
        line-height: 1.48;
        color: #333;
        margin-bottom: 30px;
    }

    .icon svg {
        width:28px;
        height:28px;
    }
</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------------
# LOAD SPREADSHEET
# ----------------------------------------------------------
df_profiles = pd.read_excel("Job Profile.xlsx").fillna("")


# Mapeamento das colunas esperadas
rename_map = {
    "Job Family": "job_family",
    "Sub Job Family": "sub_job_family",
    "Job Title": "job_title",
    "GG": "gg",
    "Career Path": "career_path",
    "Full Job Code": "full_job_code",
}

df_profiles.rename(columns=rename_map, inplace=True)


# ----------------------------------------------------------
# FORM INPUTS
# ----------------------------------------------------------
required_fields = {}
form = {}

# Helper
def field(label, options):
    selected = st.selectbox(label, ["Choose option"] + options)
    form[label] = selected
    required_fields[label] = (selected != "Choose option")
    return selected


# → Job Family
job_fams = sorted(df_profiles["job_family"].unique().tolist())
job_family = field("Job Family", job_fams)

# → Sub Job Family
if job_family == "Choose option":
    sub_job_family = st.selectbox("Sub Job Family", ["Choose option"])
else:
    sub_opts = df_profiles[df_profiles["job_family"] == job_family]["sub_job_family"].unique().tolist()
    sub_job_family = field("Sub Job Family", sorted(sub_opts))

# Outros campos (em ordem original)
job_category = field("Job Category", ["Executive", "Manager", "Professional", "Technical Support", "Business Support", "Production"])
geo_scope = field("Geographic Scope", ["Local", "Regional", "Multi-country", "Global"])
org_impact = field("Organizational Impact", ["Team", "Department / Subfunction", "Function", "Business Unit", "Enterprise-wide"])
autonomy = field("Autonomy Level", ["Close supervision", "Regular guidance", "Independent", "Sets direction for others", "Defines strategy"])
knowledge_depth = field("Knowledge Depth", ["Entry-level knowledge", "Applied knowledge", "Advanced expertise", "Recognized expert", "Thought leader"])
operational_complexity = field("Operational Complexity", ["Stable operations", "Some variability", "Complex operations", "High-variability environment"])
experience = field("Experience Level", ["< 2 years", "2–5 years", "5–10 years", "10–15 years", "15+ years"])
education = field("Education Level", ["High School", "Technical Degree", "Bachelor’s", "Post-graduate", "Master’s", "Doctorate"])


# ----------------------------------------------------------
# BOTÃO GERAR
# ----------------------------------------------------------
generate = st.button("Generate Job Match Description", key="btn", use_container_width=False)


# ----------------------------------------------------------
# EXECUTAR MATCH
# ----------------------------------------------------------
if generate:

    # Verificação
    missing = [k for k, ok in required_fields.items() if not ok]

    if missing:
        st.markdown(f"""
        <div style="background:#fdecea; padding:16px; border-radius:12px; color:#b71c1c; font-size:20px; margin-top:20px;">
            Please fill all required fields.
            <ul>{"".join([f"<li>{m}</li>" for m in missing])}</ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Input final
        form_inputs = {
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

        best = compute_job_match(form_inputs, df_profiles)

        if best:
            html = render_job_description(best["row"], best["final_score"])
            st.markdown(html, unsafe_allow_html=True)

