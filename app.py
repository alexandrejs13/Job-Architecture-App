import streamlit as st
from pathlib import Path

# carrega CSS onde estão os @font-face das fontes SIG
css_path = Path("assets/css/layout_global.css")
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# renderiza título + texto com fontes SIG
st.markdown(
    """
    <h1 style="
        font-family: 'PP-Sigflow-SemiBold';
        font-size: 40px;
        margin-bottom: 10px;
        color: #000;
    ">
        Job Architecture
    </h1>

    <p style="
        font-family: 'PP-Sigflow-Regular';
        font-size: 18px;
        line-height: 1.6;
        max-width: 900px;
        color: #000;
    ">
        Bem-vindo ao portal de Job Architecture. Aqui você encontra as estruturas organizadas 
        de famílias de cargos, perfis de posição, níveis, responsabilidades e competências 
        essenciais para garantir consistência, governança e alinhamento global.
        <br><br>
        Explore as seções ao lado para navegar por famílias, perfis, comparações, dashboards 
        e muito mais — tudo com a identidade visual SIG e uma experiência totalmente integrada.
    </p>
    """,
    unsafe_allow_html=True
)
