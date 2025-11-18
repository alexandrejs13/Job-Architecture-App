import streamlit as st
from pathlib import Path

# ==========================================================
# CONFIG
# ==========================================================
st.set_page_config(
    page_title="Job Architecture",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# CSS GLOBAL (O QUE CARREGA AS FONTES SIG)
# ==========================================================
css_path = Path("assets/css/layout_global.css")
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.error("Arquivo layout_global.css não encontrado em assets/css/")

# ==========================================================
# HERO IMAGE — AGORA FUNCIONA
# ==========================================================
image_path = Path("assets/home/home_card.jpg")

if image_path.exists():
    st.image(str(image_path), use_column_width=True)
else:
    st.error("Imagem não encontrada em assets/home/home_card.jpg")

# ==========================================================
# BLOCO DE TÍTULO + TEXTO — USANDO FONTES SIG
# ==========================================================
st.markdown(
    """
    <div style="margin-top: 20px;">

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

    </div>
    """,
    unsafe_allow_html=True
)
