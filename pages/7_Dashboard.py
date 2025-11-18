# ==========================================================
# HEADER — padrão SIG (56px, alinhado, sem erros)
# ==========================================================
import streamlit as st
import base64
import os

def load_icon_png(path):
    if not os.path.exists(path):
        return ""  # evita NameError mesmo se o arquivo não existir
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

icon_path = "assets/icons/data_2_perfromance.png"
icon_b64 = load_icon_png(icon_path)

st.markdown(f"""
<div style="display:flex; align-items:center; gap:18px; margin-top:12px;">
    <img src="data:image/png;base64,{icon_b64}" style="width:56px; height:56px;">
    <h1 style="font-size:36px; font-weight:700; margin:0; padding:0;">
        Dashboard
    </h1>
</div>

<hr style="margin-top:14px; margin-bottom:26px;">
""", unsafe_allow_html=True)

# ==========================================================
# DASHBOARD — Job Architecture (Remuneração / RH)
# ==========================================================
import pandas as pd
import numpy as np

# Paleta SIG (usando o azul como cor principal)
SIG_PRIMARY = "#145EFC"
SIG_DARK = "#002C6E"
SIG_LIGHT = "#E7EFFF"

# Pequeno ajuste visual para métricas
st.markdown(
    f"""
    <style>
    div[data-testid="stMetric"] > label {{
        color: {SIG_DARK};
        font-weight: 600;
    }}
    div[data-testid="stMetric"] > div {{
        color: {SIG_PRIMARY};
        font-weight: 700;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_data
def load_job_profile():
    path = os.path.join("data", "Job Profile.xlsx")
    df = pd.read_excel(path)
    return df

df = load_job_profile()

# Nomes de colunas conforme o arquivo Job Profile.xlsx
COL_FAMILY = "Job Family"
COL_SUBFAMILY = "Sub Job Family"
COL_PROFILE = "Job Profile"
COL_CAREER_PATH = "Career Path"
COL_BAND = "Career Band Short"
COL_LEVEL = "Career Level"
COL_GRADE = "Global Grade"
COL_FULL_CODE = "Full Job Code"

required_cols = [
    COL_FAMILY,
    COL_SUBFAMILY,
    COL_PROFILE,
    COL_CAREER_PATH,
    COL_BAND,
    COL_LEVEL,
    COL_GRADE,
    COL_FULL_CODE,
]

missing = [c for c in required_cols if c not in df.columns]

if missing:
    st.error(
        "As seguintes colunas obrigatórias não foram encontradas na base de Job Profile: "
        + ", ".join(missing)
    )
    st.stop()

# ======================================================================
# VISÃO GERAL — INDICADORES CHAVE
# ======================================================================
qtd_familias = df[COL_FAMILY].nunique()
qtd_subfamilias = df[COL_SUBFAMILY].nunique()
qtd_cargos = df[COL_PROFILE].nunique()
qtd_career_paths = df[COL_CAREER_PATH].nunique()
qtd_bands = df[COL_BAND].nunique()
qtd_grades = df[COL_GRADE].nunique()

st.markdown("### Visão geral da Job Architecture")

col1, col2, col3 = st.columns(3)
col1.metric("Famílias", qtd_familias)
col2.metric("Subfamílias", qtd_subfamilias)
col3.metric("Job Profiles únicos", qtd_cargos)

col4, col5, col6 = st.columns(3)
col4.metric("Career Paths", qtd_career_paths)
col5.metric("Career Bands", qtd_bands)
col6.metric("Grades globais", qtd_grades)

# ======================================================================
# DISTRIBUIÇÃO DE CARGOS POR FAMÍLIA
# ======================================================================
st.markdown("---")
st.markdown("### Distribuição de Job Profiles por Família")

familia_profiles = (
    df.groupby(COL_FAMILY)[COL_PROFILE]
    .nunique()
    .reset_index(name="Qtd de Job Profiles")
    .sort_values("Qtd de Job Profiles", ascending=False)
)

st.bar_chart(
    data=familia_profiles.set_index(COL_FAMILY)["Qtd de Job Profiles"]
)

with st.expander("Ver tabela detalhada por família"):
    st.dataframe(familia_profiles, use_container_width=True)

# ======================================================================
# DISTRIBUIÇÃO DE CARGOS POR SUBFAMÍLIA (TOP 15)
# ======================================================================
st.markdown("### Top 15 Subfamílias por número de Job Profiles")

subfamilia_profiles = (
    df.groupby([COL_FAMILY, COL_SUBFAMILY])[COL_PROFILE]
    .nunique()
    .reset_index(name="Qtd de Job Profiles")
    .sort_values("Qtd de Job Profiles", ascending=False)
)

top_sub = subfamilia_profiles.head(15)

st.bar_chart(
    data=top_sub.set_index(COL_SUBFAMILY)["Qtd de Job Profiles"]
)

with st.expander("Ver tabela completa de subfamílias"):
    st.dataframe(subfamilia_profiles, use_container_width=True)

# ======================================================================
# PERSPECTIVA DE CARREIRA — BAND, LEVEL, GRADE
# ======================================================================
st.markdown("---")
st.markdown("### Estrutura de Carreira (Band / Level / Grade)")

col_a, col_b = st.columns(2)

# Distribuição por Career Band
band_dist = (
    df.groupby(COL_BAND)[COL_PROFILE]
    .nunique()
    .reset_index(name="Qtd de Job Profiles")
    .sort_values("Qtd de Job Profiles", ascending=False)
)

with col_a:
    st.markdown("#### Distribuição por Career Band")
    if not band_dist.empty:
        st.bar_chart(
            data=band_dist.set_index(COL_BAND)["Qtd de Job Profiles"]
        )
    st.dataframe(band_dist, use_container_width=True)

# Distribuição por Grade Global (ordenada)
grade_dist = (
    df.groupby(COL_GRADE)[COL_PROFILE]
    .nunique()
    .reset_index(name="Qtd de Job Profiles")
    .sort_values(COL_GRADE)
)

with col_b:
    st.markdown("#### Distribuição por Grade Global")
    if not grade_dist.empty:
        st.bar_chart(
            data=grade_dist.set_index(COL_GRADE)["Qtd de Job Profiles"]
        )
    st.dataframe(grade_dist, use_container_width=True)

# Career Path — onde está concentrado o portfólio
st.markdown("### Top 10 Career Paths por número de Job Profiles")

career_path_dist = (
    df.groupby(COL_CAREER_PATH)[COL_PROFILE]
    .nunique()
    .reset_index(name="Qtd de Job Profiles")
    .sort_values("Qtd de Job Profiles", ascending=False)
)

top_career_paths = career_path_dist.head(10)

st.bar_chart(
    data=top_career_paths.set_index(COL_CAREER_PATH)["Qtd de Job Profiles"]
)

with st.expander("Ver todos os Career Paths"):
    st.dataframe(career_path_dist, use_container_width=True)

# ======================================================================
# PERSPECTIVA DE REMUNERAÇÃO / RH
# (qualidade da job architecture para suportar decisões)
# ======================================================================
st.markdown("---")
st.markdown("### Qualidade da Job Architecture (perspectiva Remuneração / RH)")

# 1) Perfis sem Grade / Band / Level
missing_grade = df[df[COL_GRADE].isna()]
missing_band = df[df[COL_BAND].isna()]
missing_level = df[df[COL_LEVEL].isna()]
missing_career_path = df[df[COL_CAREER_PATH].isna()]

col_q1, col_q2, col_q3, col_q4 = st.columns(4)
col_q1.metric("Job Profiles sem Grade", missing_grade[COL_PROFILE].nunique())
col_q2.metric("Job Profiles sem Band", missing_band[COL_PROFILE].nunique())
col_q3.metric("Job Profiles sem Level", missing_level[COL_PROFILE].nunique())
col_q4.metric("Job Profiles sem Career Path", missing_career_path[COL_PROFILE].nunique())

# 2) Duplicidade de Full Job Code (mesmo código, múltiplos perfis)
dup_code = df[df.duplicated(subset=[COL_FULL_CODE], keep=False)]
dup_code_grouped = (
    dup_code.groupby(COL_FULL_CODE)[COL_PROFILE]
    .nunique()
    .reset_index(name="Qtd de Job Profiles")
)
dup_code_problem = dup_code_grouped[dup_code_grouped["Qtd de Job Profiles"] > 1]

# 3) Famílias com poucos profiles (possível gap de desenho)
family_low = familia_profiles[familia_profiles["Qtd de Job Profiles"] <= 2]

with st.expander("Possíveis problemas de desenho / governança"):
    st.markdown("#### 1. Códigos de Job duplicados (mesmo Full Job Code para múltiplos perfis)")
    if not dup_code_problem.empty:
        st.dataframe(dup_code_problem, use_container_width=True)
        st.caption("Idealmente, cada Full Job Code deve estar associado a um único Job Profile.")
    else:
        st.success("Não foram encontradas duplicidades relevantes de Full Job Code em Job Profiles.")

    st.markdown("#### 2. Famílias com poucos Job Profiles (≤ 2)")
    if not family_low.empty:
        st.dataframe(family_low, use_container_width=True)
        st.caption(
            "Famílias com poucos profiles podem indicar oportunidades de melhor detalhamento / consolidação."
        )
    else:
        st.success("Todas as famílias possuem portfólio de Job Profiles razoavelmente distribuído.")

    st.markdown("#### 3. Job Profiles sem Career Path / Band / Grade / Level")
    st.write("**Sem Grade:**")
    if not missing_grade.empty:
        st.dataframe(
            missing_grade[[COL_FAMILY, COL_SUBFAMILY, COL_PROFILE, COL_GRADE]],
            use_container_width=True,
        )
    else:
        st.info("Não há Job Profiles sem Grade.")

    st.write("**Sem Band:**")
    if not missing_band.empty:
        st.dataframe(
            missing_band[[COL_FAMILY, COL_SUBFAMILY, COL_PROFILE, COL_BAND]],
            use_container_width=True,
        )
    else:
        st.info("Não há Job Profiles sem Band.")

    st.write("**Sem Level:**")
    if not missing_level.empty:
        st.dataframe(
            missing_level[[COL_FAMILY, COL_SUBFAMILY, COL_PROFILE, COL_LEVEL]],
            use_container_width=True,
        )
    else:
        st.info("Não há Job Profiles sem Level.")

    st.write("**Sem Career Path:**")
    if not missing_career_path.empty:
        st.dataframe(
            missing_career_path[
                [COL_FAMILY, COL_SUBFAMILY, COL_PROFILE, COL_CAREER_PATH]
            ],
            use_container_width=True,
        )
    else:
        st.info("Não há Job Profiles sem Career Path.")

# ======================================================================
# TABELA DE APOIO — VISÃO RESUMIDA POR FAMÍLIA E SUBFAMÍLIA
# ======================================================================
st.markdown("---")
st.markdown("### Resumo por Família e Subfamília")

resumo_family_sub = (
    df.groupby([COL_FAMILY, COL_SUBFAMILY])
    .agg(
        qtd_job_profiles=(COL_PROFILE, "nunique"),
        qtd_career_paths=(COL_CAREER_PATH, "nunique"),
        qtd_grades=(COL_GRADE, "nunique"),
    )
    .reset_index()
    .sort_values(["Job Family", "Sub Job Family"])
)

st.dataframe(resumo_family_sub, use_container_width=True)
