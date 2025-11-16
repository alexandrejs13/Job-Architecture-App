import streamlit as st
import pandas as pd
from pathlib import Path

# ------------------------------------------------------------
# CONFIGURAÇÃO DE PÁGINA
# ------------------------------------------------------------
st.set_page_config(page_title="Job Maps", layout="wide")

# ------------------------------------------------------------
# HEADER PADRÃO (mesma função que você está usando nas outras páginas)
# ------------------------------------------------------------
def header(icon_path, title):
    col1, col2 = st.columns([0.08, 0.92])
    with col1:
        st.image(icon_path, width=48)
    with col2:
        st.markdown(f"""
            <h1 style="margin:0; padding:0; font-size:36px; font-weight:700;">
                {title}
            </h1>
        """, unsafe_allow_html=True)
    st.markdown("<hr style='margin-top:5px;'>", unsafe_allow_html=True)

header("assets/icons/globe_trade.png", "Job Maps")

# ------------------------------------------------------------
# VISÃO GERAL
# ------------------------------------------------------------
st.markdown("""
### Visão Geral

Os **Job Maps** representam a relação visual e hierárquica entre funções, subfamílias e níveis organizacionais.

Eles ajudam a compreender:

- as trilhas de carreira,
- as progressões possíveis,
- e como cargos se conectam dentro da estrutura global.

Abaixo você visualiza a estrutura oficial de níveis organizacionais da SIG, considerando Career Bands, Grades e Subníveis.
""")

# ------------------------------------------------------------
# CARREGAR ARQUIVO DE NÍVEIS
# ------------------------------------------------------------
file_path = Path("data/Level Structure.xlsx")

if not file_path.exists():
    st.error("Arquivo 'Level Structure.xlsx' não encontrado na pasta /data.")
    st.stop()

df = pd.read_excel(file_path)

# ------------------------------------------------------------
# APRESENTAÇÃO DA TABELA
# ------------------------------------------------------------
st.markdown("### Mapa de Estrutura Organizacional")
st.markdown("""
A tabela abaixo apresenta os níveis estruturais e permite visualizar conexões
entre Career Bands, Grades, Subníveis, Job Families e Job Profiles.
""")

st.dataframe(df, use_container_width=True)

# ------------------------------------------------------------
# RODAPÉ
# ------------------------------------------------------------
st.markdown("""
---
*Continue navegando para acessar o **Job Match** (GGS) e a **Structure Level**.*
""")
