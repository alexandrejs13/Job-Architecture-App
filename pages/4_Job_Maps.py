# -*- coding: utf-8 -*-
# pages/4_Job_Maps.py

import streamlit as st
import pandas as pd
from utils.data_loader import load_excel_data

# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================
st.set_page_config(page_title="Job Maps", layout="wide")


# ==========================================================
# HEADER PADRÃO (MESMO VISUAL DO NOVO APP)
# ==========================================================
def header(icon_path: str, title: str) -> None:
    col1, col2 = st.columns([0.08, 0.92])
    with col1:
        st.image(icon_path, width=48)
    with col2:
        st.markdown(
            f"""
            <h1 style="margin:0; padding:0; font-size:36px; font-weight:700;">
                {title}
            </h1>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("<hr style='margin-top:5px;'>", unsafe_allow_html=True)


header("assets/icons/globe_trade.png", "Job Maps")


# ==========================================================
# VISÃO GERAL (TEXTO IGUAL AO APP ANTIGO)
# ==========================================================
st.markdown(
    """
### Visão Geral

Os **Job Maps** representam a relação visual e hierárquica entre funções,
subfamílias e níveis organizacionais.

Eles ajudam a compreender:

- as trilhas de carreira,  
- as progressões possíveis,  
- e como cargos se conectam dentro da estrutura global.

Abaixo, você visualiza a estrutura oficial de níveis organizacionais da SIG,
considerando Career Bands, Grades e Subníveis.
""",
)


# ==========================================================
# CARREGAMENTO DO ARQUIVO DE NÍVEIS
# ==========================================================
data = load_excel_data()
df = data.get("level_structure", pd.DataFrame())

if df.empty:
    st.error(
        "Arquivo **'Level Structure.xlsx'** não encontrado na pasta `data/` "
        "ou o arquivo está vazio."
    )
    st.stop()


# ==========================================================
# APRESENTAÇÃO DO MAPA (TABELA)
# ==========================================================
st.markdown(
    """
### Mapa de Estrutura Organizacional

A tabela abaixo apresenta os níveis estruturais, permitindo visualizar
como cada nível se conecta às Job Families e Job Profiles.
"""
)

st.dataframe(df, use_container_width=True)

# ==========================================================
# RODAPÉ
# ==========================================================
st.caption(
    "Continue navegando para acessar o Job Match e a Structure Level."
)
