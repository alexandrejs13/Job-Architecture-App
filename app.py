import streamlit as st
from pathlib import Path

# ==========================================================
# CONFIG
# ==========================================================
st.set_page_config(page_title="Job Architecture", layout="wide")

# ==========================================================
# CSS GLOBAL — IDÊNTICO ÀS OUTRAS PÁGINAS
# (agora com o caminho ABSOLUTO correto)
# ==========================================================
css_path = Path("assets/css/layout_global.css")

if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.error("❌ layout_global.css não encontrado em assets/css/")

# ==========================================================
# HERO IMAGE — COM CANTOS MAIS ARREDONDADOS
# ==========================================================
img_path = Path("assets/home/home_card.jpg")

if img_path.exists():
    st.markdown(
        f"""
        <div style="margin-top: 18px; margin-bottom: 32px; display:flex; justify-content:center;">
            <img src="{img_path.as_posix()}" 
                 style="
                    width: 100%;
                    max-width: 1500px;
                    border-radius: 36px;
                    display: block;
                    object-fit: cover;
                    box-shadow: 0 4px 18px rgba(0,0,0,0.10);
                 ">
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.error("❌ Imagem não encontrada em assets/home/home_card.jpg")

# ==========================================================
# TÍTULO + TEXTO — FONTE SIG PPSIGFlow
# ==========================================================
st.markdown(
    """
    <div style="max-width:1500px; margin:0 auto;">

        <h1 style="
            font-family: 'PPSIGFlow';
            font-size: 40px;
            font-weight: 600;
            margin-bottom: 14px;
            color: #000;
            letter-spacing:-0.3px;
        ">
            Job Architecture
        </h1>

        <p style="
            font-family: 'PPSIGFlow';
            font-size: 18px;
            font-weight: 400;
            line-height: 1.6;
            color: #000;
            max-width: 900px;
            opacity:0.95;
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
