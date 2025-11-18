import streamlit as st
import base64
import os
import pandas as pd
import altair as alt

# ==========================================================
# CONFIG
# ==========================================================
st.set_page_config(page_title="Dashboard", layout="wide")

# ==========================================================
# FUNÇÃO PARA CARREGAR PNG INLINE
# ==========================================================
def load_icon_png(path: str) -> str:
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# ==========================================================
# PALETA SIG (aproximação das cores do guia)
# ==========================================================
SIG_BLUE = "#145EFC"
SIG_BLUE_DARK = "#00338D"
SIG_BLUE_LIGHT = "#D6E2FF"
SIG_GREY_LIGHT = "#F5F7FB"
SIG_GREY_MEDIUM = "#D0D4E4"
SIG_GREY_DARK = "#4A4F62"

SIG_ACCENT_1 = "#00A6A0"
SIG_ACCENT_2 = "#FFB547"
SIG_ACCENT_3 = "#FF6B6B"

SIG_CATEGORY_COLORS = [
    SIG_BLUE,
    SIG_ACCENT_1,
    SIG_ACCENT_2,
    SIG_ACCENT_3,
    "#6C5CE7",
    "#0984E3",
    "#00B894",
    "#E17055",
    "#636E72",
]

# ==========================================================
# HEADER — padrão SIG (igual todas as páginas, mas do Dashboard)
# ==========================================================
icon_path = "assets/icons/data_2_perfromance.png"
icon_b64 = load_icon_png(icon_path)

st.markdown(
    f"""
<div style="display:flex; align-items:center; gap:18px; margin-top:12px;">
    <img src="data:image/png;base64,{icon_b64}" style="width:56px; height:56px;">
    <h1 style="font-size:36px; font-weight:700; margin:0; padding:0;">
        Dashboard
    </h1>
</div>

<hr style="margin-top:14px; margin-bottom:26px;">
""",
    unsafe_allow_html=True,
)

# ==========================================================
# ESTILO GLOBAL (cards menores, espaçamento elegante)
# ==========================================================
st.markdown(
    f"""
<style>
/* Container geral para respeitar largura padrão e respiro */
.block-container {{
    padding-top: 0.5rem;
}}

/* Estilo dos cards numéricos */
.sig-metric-card {{
    background-color: {SIG_GREY_LIGHT};
    border-radius: 14px;
    padding: 14px 16px;
    border: 1px solid {SIG_GREY_MEDIUM};
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    margin-bottom: 10px;
}}

.sig-metric-label {{
    font-size: 12px;
    font-weight: 600;
    color: {SIG_GREY_DARK};
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 4px;
}}

.sig-metric-value {{
    font-size: 20px;
    font-weight: 700;
    color: {SIG_BLUE_DARK};
    margin-bottom: 2px;
}}

.sig-metric-subtext {{
    font-size: 11px;
    color: #7A8094;
}}

/* Ajuste fino de abas para ficar mais clean */
.stTabs [data-baseweb="tab-list"] {{
    gap: 2px;
}}
.stTabs [data-baseweb="tab"] {{
    padding-top: 6px;
    padding-bottom: 6px;
    font-size: 13px;
}}
</style>
""",
    unsafe_allow_html=True,
)

# ==========================================================
# CARGA DE DADOS
# ==========================================================
@st.cache_data
def load_job_profile_data(path: str = "data/Job Profile.xlsx") -> pd.DataFrame:
    df = pd.read_excel(path)

    # Garantir nomes de colunas consistentes
    # (usamos os nomes exatamente como aparecem no arquivo)
    expected_cols = [
        "Job Family",
        "Sub Job Family",
        "Job Profile",
        "Career Level",
        "Career Band Short",
        "Career Path",
        "Global Grade",
    ]
    missing = [c for c in expected_cols if c not in df.columns]
    if missing:
        st.warning(
            f"As seguintes colunas não foram encontradas no Job Profile.xlsx: {', '.join(missing)}. "
            "Alguns indicadores podem não aparecer no Dashboard."
        )
    return df


df = load_job_profile_data()

# ==========================================================
# CÁLCULOS GERAIS
# ==========================================================
# Sempre tratar valores nulos para evitar problemas nos gráficos
df["Job Family"] = df["Job Family"].fillna("Not defined")
df["Sub Job Family"] = df["Sub Job Family"].fillna("Not defined")
if "Job Profile" in df.columns:
    df["Job Profile"] = df["Job Profile"].fillna("Not defined")

# Métricas principais
qtd_familias = df["Job Family"].nunique()
qtd_subfamilias = df["Sub Job Family"].nunique()
qtd_job_profiles = df["Job Profile"].nunique() if "Job Profile" in df.columns else None
qtd_career_paths = df["Career Path"].nunique() if "Career Path" in df.columns else None
qtd_career_levels = df["Career Level"].nunique() if "Career Level" in df.columns else None

# Distribuições
profiles_per_family = (
    df.groupby("Job Family")
    .agg(
        profiles=("Job Profile", "nunique")
        if "Job Profile" in df.columns
        else ("Job Family", "size")
    )
    .reset_index()
    .sort_values("profiles", ascending=False)
)

profiles_per_subfamily = (
    df.groupby("Sub Job Family")
    .agg(
        profiles=("Job Profile", "nunique")
        if "Job Profile" in df.columns
        else ("Sub Job Family", "size")
    )
    .reset_index()
    .sort_values("profiles", ascending=False)
)

subfamilies_per_family = (
    df.groupby("Job Family")["Sub Job Family"]
    .nunique()
    .reset_index(name="subfamilies")
    .sort_values("subfamilies", ascending=False)
)

# ==========================================================
# COMPONENTE DE CARD MÉTRICO
# ==========================================================
def render_metric_card(label: str, value, subtext: str = ""):
    st.markdown(
        f"""
    <div class="sig-metric-card">
        <div class="sig-metric-label">{label}</div>
        <div class="sig-metric-value">{value}</div>
        <div class="sig-metric-subtext">{subtext}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ==========================================================
# TABS (Overview / Family Micro-Analysis)
# ==========================================================
tab_overview, tab_micro = st.tabs(["Overview", "Family Micro-Analysis"])

# ==========================================================
# TAB 1 — OVERVIEW
# ==========================================================
with tab_overview:
    # ---- Cards menores, lado a lado, com espaçamento ----
    st.subheader("Job Architecture Overview")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_metric_card(
            "Job Families",
            qtd_familias,
            "Distinct Job Families in the architecture",
        )
    with col2:
        render_metric_card(
            "Sub Job Families",
            qtd_subfamilias,
            "Distinct Sub Job Families mapped",
        )
    with col3:
        if qtd_job_profiles is not None:
            render_metric_card(
                "Job Profiles",
                qtd_job_profiles,
                "Unique Job Profiles available",
            )
    with col4:
        if qtd_career_levels is not None:
            render_metric_card(
                "Career Levels",
                qtd_career_levels,
                "Distinct levels across profiles",
            )
        elif qtd_career_paths is not None:
            render_metric_card(
                "Career Paths",
                qtd_career_paths,
                "Defined career paths in architecture",
            )

    st.markdown("")

    # ---- Gráfico 1 — Horizontal bar (Profiles per Subfamily) ----
    st.markdown("### Profiles per Subfamily")

    if not profiles_per_subfamily.empty:
        # ordenar do maior para o menor (já está sorted, mas reforçamos dentro do chart)
        chart_data = profiles_per_subfamily.rename(
            columns={"Sub Job Family": "Sub Job Family", "profiles": "Profiles"}
        )

        bar_chart = (
            alt.Chart(chart_data)
            .mark_bar()
            .encode(
                x=alt.X(
                    "Profiles:Q",
                    sort="-y",
                    title="Number of Job Profiles",
                ),
                y=alt.Y(
                    "Sub Job Family:N",
                    sort="-x",
                    title="Sub Job Family",
                ),
                color=alt.value(SIG_BLUE),
                tooltip=[
                    alt.Tooltip("Sub Job Family:N", title="Sub Job Family"),
                    alt.Tooltip("Profiles:Q", title="Job Profiles"),
                ],
            )
            .properties(height=420)
        )

        st.altair_chart(bar_chart, use_container_width=True)
    else:
        st.info("No data available to display Profiles per Subfamily.")

    st.markdown("---")

    # ---- Gráfico 2 — Donut (Subfamily per Family) ----
    st.markdown("### Subfamilies per Family")

    if not subfamilies_per_family.empty:
        donut_data = subfamilies_per_family.rename(
            columns={"Job Family": "Job Family", "subfamilies": "Subfamilies"}
        )

        # Preparar escala de cores categóricas com paleta SIG
        color_scale = alt.Scale(
            range=SIG_CATEGORY_COLORS[: len(donut_data["Job Family"].unique())]
        )

        base = (
            alt.Chart(donut_data)
            .encode(
                theta=alt.Theta("Subfamilies:Q", stack=True),
                color=alt.Color(
                    "Job Family:N",
                    sort="-theta",
                    scale=color_scale,
                    legend=alt.Legend(title="Job Family"),
                ),
                tooltip=[
                    alt.Tooltip("Job Family:N", title="Job Family"),
                    alt.Tooltip("Subfamilies:Q", title="Subfamilies"),
                ],
            )
        )

        donut_chart = base.mark_arc(innerRadius=70)

        st.altair_chart(
            donut_chart.properties(height=380, width=600),
            use_container_width=True,
        )
    else:
        st.info("No data available to display Subfamilies per Family.")

# ==========================================================
# TAB 2 — FAMILY MICRO-ANALYSIS
# ==========================================================
with tab_micro:
    st.subheader("Family Micro-Analysis")

    families_sorted = sorted(df["Job Family"].unique())
    selected_family = st.selectbox("Select a Job Family", families_sorted)

    df_family = df[df["Job Family"] == selected_family].copy()

    # ---- Cards menores, lado a lado, com espaçamento ----
    col1, col2, col3, col4 = st.columns(4)

    family_subfamilies = df_family["Sub Job Family"].nunique()
    family_profiles = (
        df_family["Job Profile"].nunique()
        if "Job Profile" in df_family.columns
        else None
    )
    family_career_levels = (
        df_family["Career Level"].nunique()
        if "Career Level" in df_family.columns
        else None
    )
    family_global_grades = (
        df_family["Global Grade"].nunique()
        if "Global Grade" in df_family.columns
        else None
    )

    with col1:
        render_metric_card(
            "Sub Job Families (Family)",
            family_subfamilies,
            f"Sub Job Families in {selected_family}",
        )
    with col2:
        if family_profiles is not None:
            render_metric_card(
                "Job Profiles (Family)",
                family_profiles,
                f"Job Profiles in {selected_family}",
            )
    with col3:
        if family_career_levels is not None:
            render_metric_card(
                "Career Levels (Family)",
                family_career_levels,
                "Distinct levels covered",
            )
    with col4:
        if family_global_grades is not None:
            render_metric_card(
                "Global Grades (Family)",
                family_global_grades,
                "Distinct global grades mapped",
            )

    st.markdown("")

    # ---- Gráfico — Profiles per Subfamily (dentro da família) ----
    st.markdown("### Profiles per Subfamily (selected family)")

    family_profiles_per_sub = (
        df_family.groupby("Sub Job Family")
        .agg(
            profiles=("Job Profile", "nunique")
            if "Job Profile" in df_family.columns
            else ("Sub Job Family", "size")
        )
        .reset_index()
        .sort_values("profiles", ascending=False)
    )

    if not family_profiles_per_sub.empty:
        chart_data_family_sub = family_profiles_per_sub.rename(
            columns={"Sub Job Family": "Sub Job Family", "profiles": "Profiles"}
        )

        bar_family_sub = (
            alt.Chart(chart_data_family_sub)
            .mark_bar()
            .encode(
                x=alt.X(
                    "Profiles:Q",
                    sort="-y",
                    title="Number of Job Profiles",
                ),
                y=alt.Y(
                    "Sub Job Family:N",
                    sort="-x",
                    title="Sub Job Family",
                ),
                color=alt.value(SIG_BLUE),
                tooltip=[
                    alt.Tooltip("Sub Job Family:N", title="Sub Job Family"),
                    alt.Tooltip("Profiles:Q", title="Job Profiles"),
                ],
            )
            .properties(height=360)
        )

        st.altair_chart(bar_family_sub, use_container_width=True)
    else:
        st.info("No data available for Profiles per Subfamily in this Family.")

    st.markdown("---")

    # ---- Gráfico opcional — Profiles per Career Level na família ----
    if "Career Level" in df_family.columns:
        st.markdown("### Profiles per Career Level (selected family)")

        profiles_per_level = (
            df_family.groupby("Career Level")
            .agg(
                profiles=("Job Profile", "nunique")
                if "Job Profile" in df_family.columns
                else ("Career Level", "size")
            )
            .reset_index()
            .sort_values("profiles", ascending=False)
        )

        if not profiles_per_level.empty:
            chart_data_level = profiles_per_level.rename(
                columns={"Career Level": "Career Level", "profiles": "Profiles"}
            )

            bar_level = (
                alt.Chart(chart_data_level)
                .mark_bar()
                .encode(
                    x=alt.X(
                        "Career Level:N",
                        sort="-y",
                        title="Career Level",
                    ),
                    y=alt.Y(
                        "Profiles:Q",
                        sort="-x",
                        title="Number of Job Profiles",
                    ),
                    color=alt.value(SIG_ACCENT_1),
                    tooltip=[
                        alt.Tooltip("Career Level:N", title="Career Level"),
                        alt.Tooltip("Profiles:Q", title="Job Profiles"),
                    ],
                )
                .properties(height=320)
            )

            st.altair_chart(bar_level, use_container_width=True)
        else:
            st.info("No data available for Profiles per Career Level in this Family.")

    st.markdown("---")

    # ---- Tabela resumida (semelhante à microanálise) ----
    st.markdown("### Job Profiles detail (selected family)")

    cols_to_show = []
    for c in [
        "Job Family",
        "Sub Job Family",
        "Job Profile",
        "Career Level",
        "Global Grade",
        "Career Path",
    ]:
        if c in df_family.columns:
            cols_to_show.append(c)

    if cols_to_show:
        st.dataframe(
            df_family[cols_to_show].sort_values(
                ["Sub Job Family", "Job Profile"] if "Job Profile" in cols_to_show else cols_to_show
            ),
            use_container_width=True,
        )
    else:
        st.info("No columns available to display a detailed Job Profile table.")
