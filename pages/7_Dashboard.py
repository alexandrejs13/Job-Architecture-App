# ==========================================================
# DASHBOARD COMPLETO — SIG Job Architecture (Final Revisado)
# ==========================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# ----------------------------------------------------------
# Carrega a base real
# ----------------------------------------------------------
file_path = "data/Job Profile.xlsx"
df = pd.read_excel(file_path)

# Normaliza colunas
df.columns = [c.strip().replace(" ", "_").lower() for c in df.columns]

# Checagem das colunas esperadas
expected_cols = ["job_family", "sub_job_family", "job_profile", "career_level"]
missing = [c for c in expected_cols if c not in df.columns]

if missing:
    st.error(f"Colunas ausentes no Excel: {missing}")
    st.stop()

# ----------------------------------------------------------
# Paleta SIG
# ----------------------------------------------------------
SIG_SKY     = "#145efc"
SIG_SPARK   = "#dca0ff"
SIG_BLACK   = "#000000"
SIG_FOREST2 = "#167665"
SIG_MOSS2   = "#c8c84e"

SIG_COLORS = [SIG_SKY, SIG_SPARK, SIG_BLACK, SIG_FOREST2, SIG_MOSS2]

# ----------------------------------------------------------
# Métricas principais
# ----------------------------------------------------------
qtd_familias     = df['job_family'].nunique()
qtd_subfamilias  = df['sub_job_family'].nunique()
qtd_cargos       = df['job_profile'].nunique()

cargos_por_familia = df.groupby('job_family')['job_profile'].nunique()
cargos_por_subfamilia = df.groupby('sub_job_family')['job_profile'].nunique()
carreiras_por_familia = df.groupby('job_family')['career_level'].nunique()
carreiras_por_subfam = df.groupby('sub_job_family')['career_level'].nunique()

# ----------------------------------------------------------
# CSS — estilo SIG
# ----------------------------------------------------------
st.markdown("""
<style>
.metric-card {
    background-color:#f7f7f7;
    padding:22px;
    border-radius:18px;
    font-size:18px;
    font-weight:600;
    text-align:center;
    border: 1px solid #e5e5e5;
}
.metric-value {
    font-size:36px;
    font-weight:800;
    color:#145efc;
}
.section-title {
    font-size:28px;
    font-weight:700;
    margin-top:40px;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# MÉTRICAS GERAIS — CARDS
# ----------------------------------------------------------
st.markdown("<div class='section-title'>Visão Geral</div>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
        <div class='metric-card'>
            Famílias<br>
            <span class='metric-value'>{qtd_familias}</span>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
        <div class='metric-card'>
            Subfamílias<br>
            <span class='metric-value'>{qtd_subfamilias}</span>
        </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
        <div class='metric-card'>
            Cargos<br>
            <span class='metric-value'>{qtd_cargos}</span>
        </div>
    """, unsafe_allow_html=True)


# ==========================================================
# SEÇÃO 1 — DISTRIBUIÇÃO DE CARGOS
# ==========================================================
with st.expander("📊 Distribuição Geral de Cargos (Família e Subfamília)", expanded=True):

    st.subheader("Cargos por Família")
    fig_fam = px.pie(
        names=cargos_por_familia.index,
        values=cargos_por_familia.values,
        hole=0.55,
        color_discrete_sequence=SIG_COLORS
    )
    fig_fam.update_traces(textinfo="percent+label")
    st.plotly_chart(fig_fam, use_container_width=True)

    st.subheader("Top 10 Subfamílias com mais Cargos")
    sub_top = cargos_por_subfamilia.sort_values(ascending=False).head(10)
    fig_sub = px.pie(
        names=sub_top.index,
        values=sub_top.values,
        hole=0.55,
        color_discrete_sequence=SIG_COLORS
    )
    st.plotly_chart(fig_sub, use_container_width=True)


# ==========================================================
# SEÇÃO 2 — ESTRUTURA DE CARREIRA
# ==========================================================
with st.expander("🧱 Estrutura de Carreira (Career Level × Family)"):

    st.subheader("Heatmap — Career Level × Family")

    pivot = pd.pivot_table(
        df,
        values="job_profile",
        index="career_level",
        columns="job_family",
        aggfunc="count",
        fill_value=0
    )

    fig_heat = px.imshow(
        pivot,
        text_auto=True,
        color_continuous_scale=[SIG_SPARK, SIG_SKY]
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    st.subheader("Pirâmide de Senioridade (Distribuição)")
    senioridade = df['career_level'].value_counts().sort_index()

    fig_pyr = px.bar(
        x=senioridade.values,
        y=senioridade.index,
        orientation="h",
        color=senioridade.values,
        color_continuous_scale=[SIG_SPARK, SIG_SKY]
    )
    fig_pyr.update_layout(xaxis_title="Qtde", yaxis_title="Career Level")
    st.plotly_chart(fig_pyr, use_container_width=True)

    st.subheader("Profundidade de Carreira por Família")

    fam_sel = st.selectbox("Selecione a família:", cargos_por_familia.index)

    valor = carreiras_por_familia[fam_sel]
    max_val = carreiras_por_familia.max()

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=valor,
        title={'text': fam_sel},
        gauge={
            'axis': {'range': [0, max_val]},
            'bar': {'color': SIG_SKY},
            'steps': [
                {'range': [0, max_val*0.25], 'color': SIG_SPARK},
                {'range': [max_val*0.25, max_val*0.5], 'color': SIG_MOSS2},
                {'range': [max_val*0.5, max_val*0.75], 'color': SIG_FOREST2},
                {'range': [max_val*0.75, max_val], 'color': SIG_BLACK},
            ]
        }
    ))
    st.plotly_chart(fig_gauge, use_container_width=True)


# ==========================================================
# SEÇÃO 3 — GOVERNANÇA, GAPS E CONSISTÊNCIA
# ==========================================================
with st.expander("🧭 Governança, Gaps e Consistências (Auditoria Automática)"):

    st.subheader("Inconsistências de Nomenclatura")
    inconsist = df['job_profile'].str.lower().str.contains("jr|junior|sr|senior")
    st.dataframe(df[incons][['job_family','sub_job_family','job_profile']])

    st.subheader("Subfamílias com apenas 1 cargo")
    sub_1 = cargos_por_subfamilia[cargos_por_subfamilia==1]
    st.write(sub_1)

    st.subheader("Job Architecture Health Score")

    score = (
        (1 - (sub_1.count() / qtd_subfamilias)) * 0.4 +
        (cargos_por_familia.std() / cargos_por_familia.mean()) * (-0.3) +
        (carreiras_por_familia.mean() / carreiras_por_familia.max()) * 0.3
    )

    score_final = max(0, min(100, round(score*100,1)))
    st.metric("Health Score", f"{score_final}/100")


# ==========================================================
# SEÇÃO 4 — TRAJETÓRIA (SANKEY)
# ==========================================================
with st.expander("🔗 Trajetórias e Progressão (Sankey)"):

    st.subheader("Fluxo de Progressão — Career Level")

    df_sorted = df.sort_values(by="career_level").copy()
    df_sorted["next_level"] = df_sorted["career_level"].shift(-1)

    sankey = df_sorted.dropna(subset=["next_level"])

    labels = list(pd.unique(sankey["career_level"].tolist() + sankey["next_level"].tolist()))
    source = sankey["career_level"].apply(lambda x: labels.index(x))
    target = sankey["next_level"].apply(lambda x: labels.index(x))

    fig_sankey = go.Figure(data=[go.Sankey(
        node=dict(label=labels, pad=20, thickness=20),
        link=dict(source=source, target=target, value=[1]*len(source))
    )])

    st.plotly_chart(fig_sankey, use_container_width=True)


# ==========================================================
# SEÇÃO 5 — CLUSTERIZAÇÃO
# ==========================================================
with st.expander("🧬 Clusterização e Similaridade entre Cargos"):

    st.subheader("Clusterização por Complexidade (simplificada)")

    df["len"] = df["job_profile"].str.len()

    X = StandardScaler().fit_transform(df[["len"]])
    kmeans = KMeans(n_clusters=4, random_state=42).fit(X)
    df["cluster"] = kmeans.labels_

    fig_cluster = px.scatter(
        df,
        x="len",
        y="cluster",
        color=df["cluster"].astype(str),
        color_discrete_sequence=SIG_COLORS
    )

    st.plotly_chart(fig_cluster, use_container_width=True)

    st.write("Clusterização baseada no tamanho do nome como feature simplificada.")
